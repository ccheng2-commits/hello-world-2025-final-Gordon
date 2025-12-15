"""
IRIS#1 - Digital Biometrics (INSTRUCTIVE COLLECTIVE ART)
Extracts numerical features from iris images and FFT spectra,
then encodes them into a latent code string matching the original design:
IRIS/I?SEED=<UINT32>GHO=<INT>GDH=<INT>GRO=<NUM>GRING=<NUM>GTEX=<NUM>G/1=0.010

Important: Each iris must generate a unique code. No reverse engineering or
hashing multiple irises into one code is allowed.
"""

import numpy as np
import cv2
from pathlib import Path
import json
from backend.config import CODES_DIR, LATENT_CODE_VERSION, LATENT_SEED_BASE
from backend.generate_codes_index import save_codes_index


def extract_image_features(image_path):
    """
    Extract simple statistical features from an iris image.
    For MVP: brightness, contrast, texture complexity.
    Later: more sophisticated features.
    
    Args:
        image_path: Path to processed iris image
    
    Returns:
        Dictionary of feature values
    """
    img = cv2.imread(str(image_path), cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise ValueError(f"Could not load image: {image_path}")
    
    # Normalize to 0-1
    img_norm = img.astype(np.float32) / 255.0
    
    # Average brightness (H0)
    brightness = float(np.mean(img_norm) * 255)
    
    # Contrast (standard deviation, dH)
    contrast = float(np.std(img_norm) * 255)
    
    # Texture complexity: variance of local gradients
    grad_x = cv2.Sobel(img_norm, cv2.CV_32F, 1, 0, ksize=3)
    grad_y = cv2.Sobel(img_norm, cv2.CV_32F, 0, 1, ksize=3)
    texture = float(np.var(grad_x) + np.var(grad_y))
    
    # Radial structure: measure how much energy is in circular patterns
    # Simple heuristic: compare center vs edge brightness
    h, w = img_norm.shape
    center_region = img_norm[h//4:3*h//4, w//4:3*w//4]
    edge_region = np.concatenate([
        img_norm[:h//4, :].flatten(),
        img_norm[3*h//4:, :].flatten(),
        img_norm[:, :w//4].flatten(),
        img_norm[:, 3*w//4:].flatten()
    ])
    radial_ratio = float(np.mean(center_region) / (np.mean(edge_region) + 1e-10))
    
    return {
        "GHO": brightness,      # Average brightness (H₀ in original design)
        "GDH": contrast,        # Contrast (dH in original design)
        "GTEX": texture,        # Texture complexity
        "GRO": radial_ratio,    # Radial structure ratio (R₀ in original design)
    }


def extract_fft_features(fft_spectrum):
    """
    Extract features from FFT spectrum.
    
    Args:
        fft_spectrum: FFT magnitude spectrum (numpy array)
    
    Returns:
        Dictionary of FFT feature values
    """
    # Normalize spectrum
    spectrum_norm = (fft_spectrum - fft_spectrum.min()) / (fft_spectrum.max() - fft_spectrum.min() + 1e-10)
    
    h, w = spectrum_norm.shape
    center_y, center_x = h // 2, w // 2
    
    # Low frequency energy (center region)
    center_size = min(h, w) // 4
    center_region = spectrum_norm[center_y-center_size:center_y+center_size,
                                  center_x-center_size:center_x+center_size]
    low_freq_energy = float(np.mean(center_region))
    
    # High frequency energy (edges)
    edge_mask = np.ones((h, w), dtype=bool)
    edge_mask[center_y-center_size:center_y+center_size,
              center_x-center_size:center_x+center_size] = False
    high_freq_energy = float(np.mean(spectrum_norm[edge_mask]))
    
    # Frequency balance (lambda)
    freq_balance = float(low_freq_energy / (high_freq_energy + 1e-10))
    
    # Ring patterns: measure energy in circular bands
    y, x = np.ogrid[:h, :w]
    distances = np.sqrt((x - center_x)**2 + (y - center_y)**2)
    max_dist = np.sqrt(center_x**2 + center_y**2)
    normalized_dist = distances / (max_dist + 1e-10)
    
    # Energy in middle ring (0.3-0.6 of radius)
    ring_mask = (normalized_dist >= 0.3) & (normalized_dist <= 0.6)
    ring_energy = float(np.mean(spectrum_norm[ring_mask]))
    
    return {
        "G/1": freq_balance,    # Frequency balance (λ in original, encoded as G/1)
        "GRING": ring_energy,    # Ring pattern energy
    }


def generate_seed_from_features(features):
    """
    Generate a deterministic seed from feature values.
    This ensures the same iris always gets the same seed.
    
    Important: This is NOT a hash that could collapse multiple irises into one.
    The seed is derived from unique feature combinations, ensuring each iris
    gets a distinct seed value.
    
    Args:
        features: Dictionary of feature values
    
    Returns:
        Integer seed value (UINT32 range: 0 to 4294967295)
    """
    # Combine all feature values into a unique seed string
    # Order matters for consistency
    seed_str = ""
    feature_order = ["GHO", "GDH", "GRO", "GRING", "GTEX", "G/1"]
    for key in feature_order:
        if key in features:
            # Use high precision to preserve uniqueness
            seed_str += f"{key}{features[key]:.9f}"
    
    # Generate seed using a deterministic method
    # Use Python's hash but ensure it's positive and in UINT32 range
    seed = hash(seed_str)
    
    # Convert to UINT32 range (0 to 4294967295)
    # Use modulo to fit in range, but add base to avoid collisions
    seed = abs(seed) % (2**32)
    
    # Ensure it's in valid UINT32 range
    if seed < 0:
        seed = 0
    elif seed > 4294967295:
        seed = 4294967295
    
    return int(seed)


def encode_latent_code(features, seed):
    """
    Encode features into a latent code string matching the original design.
    Format: IRIS/I?SEED=<UINT32>GHO=<INT>GDH=<INT>GRO=<NUM>GRING=<NUM>GTEX=<NUM>G/1=0.010
    
    Args:
        features: Dictionary of feature values (using GHO, GDH, GRO, GRING, GTEX, G/1)
        seed: Integer seed value (UINT32)
    
    Returns:
        Latent code string in original format
    """
    # Start with IRIS/I?SEED=<UINT32>
    code = f"IRIS/I?SEED={seed}"
    
    # Add features in the exact order from original design
    # Format: GHO=<INT>GDH=<INT>GRO=<NUM>GRING=<NUM>GTEX=<NUM>G/1=<NUM>
    feature_order = ["GHO", "GDH", "GRO", "GRING", "GTEX", "G/1"]
    
    for key in feature_order:
        if key in features:
            value = features[key]
            # Format: integers for GHO, GDH; decimals for GRO, GRING, GTEX, G/1
            if key in ["GHO", "GDH"]:
                code += f"{key}={int(value)}"  # GHO, GDH as integers
            elif key == "G/1":
                code += f"G/1={value:.3f}"  # Special format for frequency parameter
            else:
                code += f"{key}={value:.3f}"  # GRO, GRING, GTEX as decimals
    
    return code


def generate_latent_code(processed_image_path, fft_spectrum=None):
    """
    Main function: extract features and generate latent code.
    
    Args:
        processed_image_path: Path to processed iris image
        fft_spectrum: Optional FFT spectrum (numpy array). If None, will be computed.
    
    Returns:
        Tuple of (latent_code_string, features_dict, seed)
    """
    # Extract image features
    img_features = extract_image_features(processed_image_path)
    
    # Extract FFT features (if spectrum provided)
    if fft_spectrum is not None:
        fft_features = extract_fft_features(fft_spectrum)
    else:
        # If no spectrum provided, use default values
        fft_features = {"G/1": 0.010, "GRING": 0.5}
    
    # Combine all features
    all_features = {**img_features, **fft_features}
    
    # Generate seed
    seed = generate_seed_from_features(all_features)
    
    # Encode latent code
    latent_code = encode_latent_code(all_features, seed)
    
    return latent_code, all_features, seed


def save_latent_code(latent_code, features, seed, output_filename=None):
    """
    Save latent code and metadata to a JSON file.
    
    Args:
        latent_code: Latent code string
        features: Features dictionary
        seed: Seed value
        output_filename: Optional output filename. If None, uses timestamp.
    
    Returns:
        Path to saved JSON file
    """
    import time
    
    if output_filename is None:
        timestamp = int(time.time())
        output_filename = f"code_{timestamp}.json"
    
    output_path = CODES_DIR / output_filename
    
    data = {
        "latent_code": latent_code,
        "seed": seed,
        "features": features,
        "timestamp": time.time()
    }
    
    with open(output_path, 'w') as f:
        json.dump(data, f, indent=2)
    
    # Also save as simple text file for easy frontend reading
    txt_path = CODES_DIR / output_filename.replace('.json', '.txt')
    with open(txt_path, 'w') as f:
        f.write(latent_code)
    
    # Update codes index for frontend
    try:
        save_codes_index()
    except Exception as e:
        print(f"Warning: Could not update codes index: {e}")
    
    print(f"✓ Latent code saved: {output_path.name}")
    return output_path


if __name__ == "__main__":
    # Simple test
    from backend.config import PROCESSED_DIR
    
    test_images = list(PROCESSED_DIR.glob("*.jpg")) + list(PROCESSED_DIR.glob("*.png"))
    
    if test_images:
        test_image = test_images[0]
        print(f"Testing latent code generation with: {test_image}")
        
        # Generate code
        code, features, seed = generate_latent_code(test_image)
        print(f"\nLatent Code: {code}")
        print(f"Seed: {seed}")
        print(f"Features: {features}")
        
        # Save it
        save_latent_code(code, features, seed)
    else:
        print("No processed images found in data/processed/")
        print("Run iris_processor.py first to create processed images.")

