"""
IRIS#1 - Digital Biometrics
Computes 2D FFT (Fast Fourier Transform) of iris images and generates
visual spectrum images for the generative rendering.
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from backend.config import FFT_DIR, FFT_IMAGE_SIZE, FFT_COLORMAP


def load_processed_iris(image_path):
    """
    Load a processed (cropped) iris image.
    
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


def compute_fft_2d(image):
    """
    Compute 2D FFT of an image and return the magnitude spectrum.
    
    Args:
        image: Input grayscale image (numpy array)
    
    Returns:
        Magnitude spectrum (numpy array, float)
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


def create_fft_visualization(magnitude_spectrum, output_size=FFT_IMAGE_SIZE, colormap=FFT_COLORMAP):
    """
    Create a visualization image from the FFT magnitude spectrum.
    
    Args:
        magnitude_spectrum: FFT magnitude spectrum (numpy array)
        output_size: Desired output image size (will be resized)
        colormap: Matplotlib colormap name
    
    Returns:
        RGB image as numpy array (0-255 uint8)
    """
    # Normalize to 0-1 range
    spectrum_norm = (magnitude_spectrum - magnitude_spectrum.min()) / (magnitude_spectrum.max() - magnitude_spectrum.min() + 1e-10)
    
    # Apply colormap
    cmap = plt.get_cmap(colormap)
    spectrum_colored = cmap(spectrum_norm)
    
    # Convert to 0-255 uint8 RGB (remove alpha channel if present)
    if spectrum_colored.shape[2] == 4:
        spectrum_colored = spectrum_colored[:, :, :3]
    spectrum_rgb = (spectrum_colored * 255).astype(np.uint8)
    
    # Resize to desired output size
    if spectrum_rgb.shape[0] != output_size or spectrum_rgb.shape[1] != output_size:
        spectrum_rgb = cv2.resize(spectrum_rgb, (output_size, output_size), interpolation=cv2.INTER_LINEAR)
    
    return spectrum_rgb


def process_iris_fft(processed_image_path, output_filename=None):
    """
    Main function: load processed iris, compute FFT, save visualization.
    
    Args:
        processed_image_path: Path to processed (cropped) iris image
        output_filename: Optional output filename. If None, uses input filename.
    
    Returns:
        Path to the saved FFT visualization image
    """
    # Load the processed iris image
    iris_img = load_processed_iris(processed_image_path)
    
    # Compute FFT
    fft_spectrum = compute_fft_2d(iris_img)
    
    # Create visualization
    fft_viz = create_fft_visualization(fft_spectrum, FFT_IMAGE_SIZE, FFT_COLORMAP)
    
    # Generate output filename
    if output_filename is None:
        input_path = Path(processed_image_path)
        output_filename = f"fft_{input_path.stem}.jpg"
    
    output_path = FFT_DIR / output_filename
    
    # Save the visualization (convert RGB to BGR for OpenCV)
    fft_bgr = cv2.cvtColor(fft_viz, cv2.COLOR_RGB2BGR)
    cv2.imwrite(str(output_path), fft_bgr)
    
    print(f"✓ FFT computed: {processed_image_path.name} -> {output_path.name}")
    return output_path, fft_spectrum


if __name__ == "__main__":
    # Simple test: process a sample image if it exists
    from backend.config import PROCESSED_DIR
    
    # Look for any processed image
    test_images = list(PROCESSED_DIR.glob("*.jpg")) + list(PROCESSED_DIR.glob("*.png"))
    
    if test_images:
        test_image = test_images[0]
        print(f"Testing FFT with: {test_image}")
        result, spectrum = process_iris_fft(test_image)
        print(f"FFT visualization saved to: {result}")
        print(f"Spectrum shape: {spectrum.shape}, min: {spectrum.min():.2f}, max: {spectrum.max():.2f}")
    else:
        print("No processed images found in data/processed/")
        print("Run iris_processor.py first to create processed images.")

