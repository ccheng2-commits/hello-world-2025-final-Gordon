"""
IRIS#1 - Digital Biometrics
Processes iris photos: loads image, crops 1:1 square around iris region.
For MVP: simple center crop. Later: add automatic pupil detection.
"""

import cv2
import numpy as np
from pathlib import Path
from backend.config import PROCESSED_DIR, IRIS_CROP_SIZE


def load_image(image_path):
    """
    Load an image from file path.
    
    Args:
        image_path: Path to the image file (str or Path)
    
    Returns:
        numpy array of the image (BGR format from OpenCV)
    """
    image_path = Path(image_path)
    if not image_path.exists():
        raise FileNotFoundError(f"Image not found: {image_path}")
    
    img = cv2.imread(str(image_path))
    if img is None:
        raise ValueError(f"Could not load image: {image_path}")
    
    return img


def center_crop_iris(image, crop_size=IRIS_CROP_SIZE):
    """
    Crop a square region from the center of the image.
    This is a simple MVP version - later we'll detect the pupil center.
    
    Args:
        image: Input image (numpy array, BGR format)
        crop_size: Size of the square crop in pixels
    
    Returns:
        Cropped image (numpy array)
    """
    h, w = image.shape[:2]
    
    # Calculate center point
    center_x = w // 2
    center_y = h // 2
    
    # Calculate crop boundaries (ensure we don't go out of bounds)
    half_size = crop_size // 2
    x1 = max(0, center_x - half_size)
    y1 = max(0, center_y - half_size)
    x2 = min(w, center_x + half_size)
    y2 = min(h, center_y + half_size)
    
    # Crop the image
    cropped = image[y1:y2, x1:x2]
    
    # If the crop is smaller than desired (near edges), pad it
    if cropped.shape[0] < crop_size or cropped.shape[1] < crop_size:
        # Create a black canvas
        result = np.zeros((crop_size, crop_size, 3), dtype=image.dtype)
        # Place cropped image in center
        offset_y = (crop_size - cropped.shape[0]) // 2
        offset_x = (crop_size - cropped.shape[1]) // 2
        result[offset_y:offset_y+cropped.shape[0], 
               offset_x:offset_x+cropped.shape[1]] = cropped
        return result
    
    return cropped


def process_iris_photo(input_path, output_filename=None):
    """
    Main function: load a photo, crop the iris region, save the result.
    
    Args:
        input_path: Path to input image (str or Path)
        output_filename: Optional output filename. If None, uses input filename.
    
    Returns:
        Path to the saved processed image
    """
    # Load the image
    img = load_image(input_path)
    
    # Crop the iris region (center crop for MVP)
    cropped = center_crop_iris(img, IRIS_CROP_SIZE)
    
    # Generate output filename
    if output_filename is None:
        input_path = Path(input_path)
        output_filename = f"iris_{input_path.stem}.jpg"
    
    output_path = PROCESSED_DIR / output_filename
    
    # Save the cropped image
    cv2.imwrite(str(output_path), cropped)
    
    print(f"✓ Processed iris: {input_path.name} -> {output_path.name}")
    return output_path


if __name__ == "__main__":
    # Simple test: process a sample image if it exists
    from backend.config import INCOMING_DIR
    
    # Look for any image in incoming folder
    test_images = list(INCOMING_DIR.glob("*.jpg")) + list(INCOMING_DIR.glob("*.png"))
    
    if test_images:
        test_image = test_images[0]
        print(f"Testing with: {test_image}")
        result = process_iris_photo(test_image)
        print(f"Result saved to: {result}")
    else:
        print("No test images found in data/incoming/")
        print("Place a test iris photo there to test the processor.")

