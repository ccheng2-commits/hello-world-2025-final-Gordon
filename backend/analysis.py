"""
IRIS#1 - Digital Biometrics
Biological feature extraction from donut iris images.
Extracts features including 1D waveform from 2D FFT spectrum.
"""

import cv2
import numpy as np
from pathlib import Path
import json
from backend.config import PROCESSED_DIR


def load_donut_image(image_path):
    """
    Load a donut iris image (Safe Zone ring).
    
    Args:
        image_path: Path to the processed iris image
    
    Returns:
        Grayscale image as numpy array
    """
    image_path = Path(image_path)
    if not image_path.exists():
        raise FileNotFoundError(f"Image not found: {image_path}")
    
    img = cv2.imread(str(image_path), cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise ValueError(f"Could not load image: {image_path}")
    
    return img


def compute_fft_spectrum(image):
    """
    Compute 2D FFT magnitude spectrum from the iris image.
    
    Args:
        image: Grayscale iris image
    
    Returns:
        2D magnitude spectrum (centered, log-scaled)
    """
    # Convert to float for FFT
    img_float = image.astype(np.float32)
    
    # Compute 2D FFT
    fft_result = np.fft.fft2(img_float)
    
    # Shift zero frequency to center
    fft_shifted = np.fft.fftshift(fft_result)
    
    # Compute magnitude spectrum (log scale for better visualization)
    magnitude = np.abs(fft_shifted)
    magnitude_log = np.log1p(magnitude)  # log1p = log(1+x) to avoid log(0)
    
    return magnitude_log


def extract_radial_profile_waveform(spectrum, target_length=64):
    """
    Extract 1D radial profile waveform from 2D FFT spectrum.
    Converts 2D frequency spectrum into a 1D radial profile array.
    
    Args:
        spectrum: 2D magnitude spectrum (centered)
        target_length: Target length of output waveform (default 64)
    
    Returns:
        List of floats representing the radial profile waveform (normalized 0-1)
    """
    h, w = spectrum.shape
    center_y, center_x = h // 2, w // 2
    
    # Calculate distance of each pixel from center
    y, x = np.ogrid[:h, :w]
    distances = np.sqrt((x - center_x)**2 + (y - center_y)**2)
    
    # Convert distances to integer radii
    radii = distances.astype(int)
    max_radius = int(np.max(radii))
    
    # Bin pixels by radius and calculate average magnitude for each ring
    spectrum_array = []
    for r in range(max_radius + 1):
        # Find all pixels at this radius
        mask = (radii == r)
        if np.any(mask):
            # Calculate average magnitude for this radius ring
            avg_magnitude = float(np.mean(spectrum[mask]))
            spectrum_array.append(avg_magnitude)
        else:
            # If no pixels at this radius, use 0
            spectrum_array.append(0.0)
    
    # Normalize to 0.0 - 1.0
    if len(spectrum_array) > 0:
        min_val = min(spectrum_array)
        max_val = max(spectrum_array)
        if max_val > min_val:
            spectrum_array = [(x - min_val) / (max_val - min_val) for x in spectrum_array]
        else:
            # All values are the same, set to 0
            spectrum_array = [0.0] * len(spectrum_array)
    
    # Downsample to target_length (64 data points)
    if len(spectrum_array) > target_length:
        # Resample using linear interpolation
        indices = np.linspace(0, len(spectrum_array) - 1, target_length)
        waveform = np.interp(indices, range(len(spectrum_array)), spectrum_array)
        waveform = [float(x) for x in waveform]
    elif len(spectrum_array) < target_length:
        # Upsample using linear interpolation
        indices = np.linspace(0, len(spectrum_array) - 1, target_length)
        waveform = np.interp(indices, range(len(spectrum_array)), spectrum_array)
        waveform = [float(x) for x in waveform]
    else:
        # Already the right length
        waveform = spectrum_array
    
    return waveform


def extract_basic_features(image):
    """
    Extract basic features: seed, energy, complexity.
    These are kept for compatibility with existing code.
    
    Args:
        image: Grayscale iris image
    
    Returns:
        Dictionary with seed, energy, complexity
    """
    img_norm = image.astype(np.float32) / 255.0
    
    # Only analyze non-zero pixels (ring region)
    mask = img_norm > 0.01
    ring_pixels = img_norm[mask]
    
    if len(ring_pixels) == 0:
        return {
            "seed": 0,
            "energy": 0.0,
            "complexity": 0.0
        }
    
    # Energy: total intensity
    energy = float(np.sum(ring_pixels))
    
    # Complexity: entropy-like measure
    # Compute gradient magnitude
    grad_x = cv2.Sobel(img_norm, cv2.CV_32F, 1, 0, ksize=3)
    grad_y = cv2.Sobel(img_norm, cv2.CV_32F, 0, 1, ksize=3)
    gradient_magnitude = np.sqrt(grad_x**2 + grad_y**2)
    complexity = float(np.std(gradient_magnitude[mask]))
    
    # Seed: deterministic value based on features
    seed_str = f"{energy:.6f}{complexity:.6f}"
    seed = abs(hash(seed_str)) % (2**32)
    
    return {
        "seed": int(seed),
        "energy": energy,
        "complexity": complexity
    }


def analyze_iris(image_path, output_path=None):
    """
    Analyze an iris image and extract features including 1D waveform from FFT spectrum.
    
    Args:
        image_path: Path to the iris image
        output_path: Optional path to save JSON results
    
    Returns:
        Dictionary of extracted features including waveform
    """
    image_path = Path(image_path)
    
    print(f"Analyzing: {image_path.name}")
    
    # Load image
    image = load_donut_image(image_path)
    
    # Compute FFT spectrum
    spectrum = compute_fft_spectrum(image)
    
    # Extract 1D radial profile waveform
    waveform = extract_radial_profile_waveform(spectrum, target_length=64)
    
    # Extract basic features (seed, energy, complexity)
    basic_features = extract_basic_features(image)
    
    # Load confidence score from metadata if available
    confidence = 0.0
    metadata_path = image_path.parent / f"metadata_{image_path.stem}.json"
    if metadata_path.exists():
        try:
            import json
            with open(metadata_path, 'r') as f:
                metadata = json.load(f)
                confidence = metadata.get("confidence", 0.0)
        except:
            pass
    
    # Combine all features
    features = {
        **basic_features,
        "waveform": waveform,
        "confidence": confidence
    }
    
    # Save results if output path provided
    if output_path:
        output_path = Path(output_path)
        with open(output_path, 'w') as f:
            json.dump(features, f, indent=2)
        print(f"  Results saved to: {output_path.name}")
    
    # Print summary
    print(f"  Extracted features:")
    print(f"    Seed: {features['seed']}")
    print(f"    Energy: {features['energy']:.2f}")
    print(f"    Complexity: {features['complexity']:.4f}")
    print(f"    Waveform length: {len(features['waveform'])} points")
    print(f"    Waveform range: {min(features['waveform']):.3f} - {max(features['waveform']):.3f}")
    
    return features


if __name__ == "__main__":
    # Test: analyze all processed iris images
    processed_images = sorted(PROCESSED_DIR.glob("iris-*.jpg"))
    
    if not processed_images:
        print("No processed iris images found in data/processed/")
        print("Run iris_processor.py first to generate donut images.")
    else:
        print(f"Analyzing {len(processed_images)} iris images:\n")
        
        for img_path in processed_images:
            try:
                # Save analysis results
                output_path = PROCESSED_DIR / f"analysis_{img_path.stem}.json"
                analyze_iris(img_path, output_path)
                print()
            except Exception as e:
                print(f"  ✗ Error: {e}\n")
                import traceback
                traceback.print_exc()

