"""
IRIS#1 - Digital Biometrics
Processes iris photos: extracts a robust 'Safe Zone' ring from the iris.
Uses pupil detection and ring mask to avoid eyelids and eyelashes.
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


def detect_pupil(image):
    """
    Detect pupil center and radius using threshold/contour method.
    More robust version with multiple detection strategies.
    
    Args:
        image: Input image (numpy array, BGR format)
    
    Returns:
        Tuple of (cx, cy, r_pupil, confidence) or None if detection fails
        confidence: float between 0.0 and 1.0, indicating detection quality
    """
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    h, w = gray.shape
    
    # Strategy 1: OTSU threshold (works well for high contrast)
    blurred = cv2.GaussianBlur(gray, (9, 9), 2)
    _, thresh1 = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    
    # Strategy 2: Adaptive threshold (works better for varying lighting)
    thresh2 = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                     cv2.THRESH_BINARY_INV, 11, 2)
    
    # Strategy 3: Simple threshold at low value (pupil is very dark)
    _, thresh3 = cv2.threshold(blurred, 30, 255, cv2.THRESH_BINARY_INV)
    
    # Try each strategy
    for thresh in [thresh1, thresh2, thresh3]:
        # Find contours
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if not contours:
            continue
        
        # Filter contours by area and circularity
        valid_contours = []
        for contour in contours:
            area = cv2.contourArea(contour)
            if area < 100:  # Too small
                continue
            
            # Check circularity
            perimeter = cv2.arcLength(contour, True)
            if perimeter == 0:
                continue
            circularity = 4 * np.pi * area / (perimeter * perimeter)
            
            # Pupil should be somewhat circular (circularity > 0.5)
            if circularity > 0.5:
                valid_contours.append((contour, area))
        
        if not valid_contours:
            continue
        
        # Get the largest valid contour (should be the pupil)
        largest_contour, _ = max(valid_contours, key=lambda x: x[1])
        
        # Fit a circle to the contour
        (cx, cy), radius = cv2.minEnclosingCircle(largest_contour)
        cx, cy, r_pupil = int(cx), int(cy), int(radius)
        
        # Validate: pupil should be reasonably sized and not too close to edges
        min_radius = max(10, min(h, w) // 20)  # At least 5% of image
        max_radius = min(h, w) // 3  # At most 33% of image
        
        if min_radius <= r_pupil <= max_radius:
            # Check if center is reasonably positioned (not at extreme edges)
            margin = min(h, w) // 10
            if margin < cx < w - margin and margin < cy < h - margin:
                # Calculate confidence score based on multiple factors
                confidence = calculate_detection_confidence(
                    largest_contour, area, circularity, r_pupil, h, w, cx, cy
                )
                return (cx, cy, r_pupil, confidence)
    
    # All strategies failed
    return None


def calculate_detection_confidence(contour, area, circularity, radius, img_h, img_w, cx, cy):
    """
    Calculate confidence score for pupil detection (0.0 to 1.0).
    
    Factors considered:
    - Circularity (how round the pupil is)
    - Size appropriateness (not too small or too large)
    - Position (centered vs edge)
    - Contour smoothness
    
    Args:
        contour: Detected contour
        area: Contour area
        circularity: Circularity measure (0-1)
        radius: Pupil radius
        img_h, img_w: Image dimensions
        cx, cy: Pupil center coordinates
    
    Returns:
        Confidence score (0.0 to 1.0)
    """
    confidence = 0.0
    
    # Factor 1: Circularity (0-0.4 weight)
    # Perfect circle = 1.0, good circle > 0.7
    circularity_score = min(circularity / 0.7, 1.0)  # Normalize to 0-1
    confidence += circularity_score * 0.4
    
    # Factor 2: Size appropriateness (0-0.3 weight)
    # Ideal size: 10-15% of image dimension
    ideal_min = min(img_h, img_w) * 0.10
    ideal_max = min(img_h, img_w) * 0.15
    if ideal_min <= radius <= ideal_max:
        size_score = 1.0
    elif radius < ideal_min:
        size_score = radius / ideal_min  # Too small
    else:
        size_score = max(0, 1.0 - (radius - ideal_max) / ideal_max)  # Too large
    confidence += size_score * 0.3
    
    # Factor 3: Position (0-0.2 weight)
    # More centered = higher confidence
    center_x, center_y = img_w / 2, img_h / 2
    distance_from_center = np.sqrt((cx - center_x)**2 + (cy - center_y)**2)
    max_distance = np.sqrt(center_x**2 + center_y**2)
    position_score = 1.0 - min(distance_from_center / max_distance, 1.0)
    confidence += position_score * 0.2
    
    # Factor 4: Contour smoothness (0-0.1 weight)
    # Check how smooth the contour is (fewer points = smoother)
    perimeter = cv2.arcLength(contour, True)
    if perimeter > 0:
        # Approximate contour to reduce points
        epsilon = 0.02 * perimeter
        approx = cv2.approxPolyDP(contour, epsilon, True)
        smoothness_score = min(len(approx) / 20.0, 1.0)  # Fewer points = smoother
        confidence += smoothness_score * 0.1
    
    return min(confidence, 1.0)  # Cap at 1.0


def create_ring_mask(image_shape, cx, cy, r_pupil, inner_ratio=1.1, outer_ratio=2.2):
    """
    Create a ring mask (donut shape) around the pupil.
    
    Args:
        image_shape: Shape of the image (height, width)
        cx, cy: Center coordinates of the pupil
        r_pupil: Pupil radius
        inner_ratio: Inner radius multiplier (default 1.1 to exclude pupil)
        outer_ratio: Outer radius multiplier (default 2.2 for safe zone)
    
    Returns:
        Binary mask (white ring on black background)
    """
    h, w = image_shape[:2]
    mask = np.zeros((h, w), dtype=np.uint8)
    
    # Calculate ring radii
    r_inner = int(r_pupil * inner_ratio)
    r_outer = int(r_pupil * outer_ratio)
    
    # Draw white outer circle
    cv2.circle(mask, (cx, cy), r_outer, 255, -1)
    
    # Draw black inner circle to create the donut hole
    cv2.circle(mask, (cx, cy), r_inner, 0, -1)
    
    return mask


def extract_safe_zone_ring(image, crop_size=IRIS_CROP_SIZE):
    """
    Extract a clean 'Safe Zone' ring from the iris using pupil detection.
    This avoids eyelids and eyelashes by only extracting the middle ring.
    
    Args:
        image: Input image (numpy array, BGR format)
        crop_size: Size of the output square crop in pixels
    
    Returns:
        Tuple of (cropped ring image, confidence_score)
        cropped ring image: numpy array with black background
        confidence_score: float between 0.0 and 1.0
    """
    h, w = image.shape[:2]
    
    # Detect pupil
    pupil_result = detect_pupil(image)
    
    if pupil_result is None:
        # Fallback: use center crop if detection fails
        print("⚠️  Pupil detection failed, using center crop fallback")
        cropped = center_crop_fallback(image, crop_size)
        return cropped, 0.0  # No confidence for fallback
    
    cx, cy, r_pupil, confidence = pupil_result
    print(f"✓ Pupil detected: center=({cx}, {cy}), radius={r_pupil}, confidence={confidence:.2f}")
    
    # Create ring mask (donut shape)
    mask = create_ring_mask(image.shape, cx, cy, r_pupil)
    
    # Apply mask to extract the ring (preserve color)
    # Create black background first
    masked_bgr = np.zeros_like(image)
    # Apply mask to each channel
    for c in range(image.shape[2]):
        masked_bgr[:, :, c] = cv2.bitwise_and(image[:, :, c], image[:, :, c], mask=mask)
    
    # Find bounding box of the ring
    # Get non-zero pixels from mask
    coords = np.column_stack(np.where(mask > 0))
    if len(coords) == 0:
        return center_crop_fallback(image, crop_size)
    
    y_min, x_min = coords.min(axis=0)
    y_max, x_max = coords.max(axis=0)
    
    # Add some padding
    padding = 10
    x_min = max(0, x_min - padding)
    y_min = max(0, y_min - padding)
    x_max = min(w, x_max + padding)
    y_max = min(h, y_max + padding)
    
    # Crop the ring region
    ring_crop = masked_bgr[y_min:y_max, x_min:x_max]
    
    # Resize to high resolution while preserving quality
    crop_h, crop_w = ring_crop.shape[:2]
    
    # Calculate scale to fit in crop_size (high resolution)
    scale = min(crop_size / crop_w, crop_size / crop_h)
    new_w = int(crop_w * scale)
    new_h = int(crop_h * scale)
    
    # Use high-quality interpolation for resizing
    # LANCZOS4 is best for upscaling, CUBIC for downscaling
    if scale > 1.0:
        # Upscaling: use LANCZOS4 for best quality
        resized = cv2.resize(ring_crop, (new_w, new_h), interpolation=cv2.INTER_LANCZOS4)
    else:
        # Downscaling: use CUBIC for good quality
        resized = cv2.resize(ring_crop, (new_w, new_h), interpolation=cv2.INTER_CUBIC)
    
    # Create final output with black background at high resolution
    result = np.zeros((crop_size, crop_size, 3), dtype=image.dtype)
    
    # Center the resized ring in the output
    offset_y = (crop_size - new_h) // 2
    offset_x = (crop_size - new_w) // 2
    result[offset_y:offset_y+new_h, offset_x:offset_x+new_w] = resized
    
    return result, confidence


def center_crop_fallback(image, crop_size=IRIS_CROP_SIZE):
    """
    Fallback method: simple center crop if pupil detection fails.
    
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
    
    # Calculate crop boundaries
    half_size = crop_size // 2
    x1 = max(0, center_x - half_size)
    y1 = max(0, center_y - half_size)
    x2 = min(w, center_x + half_size)
    y2 = min(h, center_y + half_size)
    
    # Crop the image
    cropped = image[y1:y2, x1:x2]
    
    # If the crop is smaller than desired, pad it with black
    if cropped.shape[0] < crop_size or cropped.shape[1] < crop_size:
        result = np.zeros((crop_size, crop_size, 3), dtype=image.dtype)
        offset_y = (crop_size - cropped.shape[0]) // 2
        offset_x = (crop_size - cropped.shape[1]) // 2
        result[offset_y:offset_y+cropped.shape[0], 
               offset_x:offset_x+cropped.shape[1]] = cropped
        return result
    
    return cropped


def get_next_iris_number():
    """
    Get the next available iris number (001, 002, etc.)
    Checks existing files in PROCESSED_DIR to find the highest number.
    
    Returns:
        Next available number as integer
    """
    # Find all existing iris-XXX.jpg files
    existing_files = list(PROCESSED_DIR.glob("iris-*.jpg"))
    
    if not existing_files:
        return 1
    
    # Extract numbers from filenames
    numbers = []
    for file in existing_files:
        # Extract number from iris-XXX.jpg format
        try:
            # Remove "iris-" prefix and ".jpg" suffix
            num_str = file.stem.replace("iris-", "")
            num = int(num_str)
            numbers.append(num)
        except ValueError:
            # Skip files that don't match the pattern
            continue
    
    if not numbers:
        return 1
    
    # Return next number (highest + 1)
    return max(numbers) + 1


def process_iris_photo(input_path, output_filename=None, match_incoming_number=None):
    """
    Main function: load a photo, extract Safe Zone ring from iris, save the result.
    
    Args:
        input_path: Path to input image (str or Path)
        output_filename: Optional output filename. If None, auto-generates iris-XXX.jpg format.
        match_incoming_number: Optional number to match incoming-XXX naming (for tracking)
    
    Returns:
        Tuple of (output_path, confidence_score)
        output_path: Path to the saved processed image
        confidence_score: float between 0.0 and 1.0
    """
    # Load the image
    img = load_image(input_path)
    
    # Extract Safe Zone ring (robust method avoiding eyelids/eyelashes)
    cropped, confidence = extract_safe_zone_ring(img, IRIS_CROP_SIZE)
    
    # Generate output filename
    if output_filename is None:
        if match_incoming_number is not None:
            # Match the incoming number for tracking
            output_filename = f"iris-{match_incoming_number:03d}.jpg"
        else:
            # Auto-generate iris-XXX.jpg format
            next_num = get_next_iris_number()
            output_filename = f"iris-{next_num:03d}.jpg"
    
    output_path = PROCESSED_DIR / output_filename
    
    # Save the cropped image
    cv2.imwrite(str(output_path), cropped)
    
    # Save confidence score to metadata file
    metadata_path = PROCESSED_DIR / f"metadata_{Path(output_filename).stem}.json"
    import json
    metadata = {
        "iris_file": output_filename,
        "confidence": float(confidence),
        "input_file": str(Path(input_path).name)
    }
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    input_path_obj = Path(input_path)
    print(f"✓ Processed iris: {input_path_obj.name} -> {output_path.name} (confidence: {confidence:.2f})")
    return output_path, confidence


if __name__ == "__main__":
    # Process images from renamed folder (after rename_incoming.py has run)
    from backend.config import RENAMED_DIR
    
    # Get all images from renamed folder (incoming-XXX.jpg format)
    test_images = sorted(RENAMED_DIR.glob("incoming-*.jpg")) + \
                  sorted(RENAMED_DIR.glob("incoming-*.jpeg")) + \
                  sorted(RENAMED_DIR.glob("incoming-*.png")) + \
                  sorted(RENAMED_DIR.glob("incoming-*.webp"))
    
    if test_images:
        print(f"Processing {len(test_images)} images from data/renamed/:\n")
        for img in test_images:
            try:
                # Extract number from incoming-XXX.jpg to match numbering
                incoming_num_str = img.stem.replace("incoming-", "")
                incoming_num = int(incoming_num_str)
                
                # Process with matching number
                result, confidence = process_iris_photo(img, match_incoming_number=incoming_num)
                print(f"  Mapping: incoming-{incoming_num:03d} -> iris-{incoming_num:03d} (confidence: {confidence:.2f})\n")
            except Exception as e:
                print(f"  ✗ Error processing {img.name}: {e}\n")
    else:
        print("No renamed images found in data/renamed/")
        print("Run 'python -m backend.rename_incoming' first to rename photos.")

