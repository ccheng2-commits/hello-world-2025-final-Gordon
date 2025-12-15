"""
IRIS#1 - Digital Biometrics
Rename incoming photos to unified format and move to renamed folder.
This allows tracking which original photo corresponds to which processed result.

Workflow:
1. Photos in data/incoming/ (original names)
2. Rename to incoming-001.jpg, incoming-002.jpg, etc.
3. Move to data/renamed/
4. Then process from renamed/ folder
"""

import shutil
from pathlib import Path
from backend.config import INCOMING_DIR, RENAMED_DIR


def get_next_incoming_number():
    """
    Get the next available incoming photo number (001, 002, etc.)
    Checks existing files in RENAMED_DIR to find the highest number.
    
    Returns:
        Next available number as integer
    """
    # Find all existing incoming-XXX files in renamed folder
    existing_files = list(RENAMED_DIR.glob("incoming-*.jpg")) + \
                     list(RENAMED_DIR.glob("incoming-*.jpeg")) + \
                     list(RENAMED_DIR.glob("incoming-*.png")) + \
                     list(RENAMED_DIR.glob("incoming-*.webp"))
    
    if not existing_files:
        return 1
    
    # Extract numbers from filenames
    numbers = []
    for file in existing_files:
        try:
            # Extract number from incoming-XXX.ext format
            num_str = file.stem.replace("incoming-", "")
            num = int(num_str)
            numbers.append(num)
        except ValueError:
            continue
    
    if not numbers:
        return 1
    
    # Return next number (highest + 1)
    return max(numbers) + 1


def rename_and_move_incoming_photos():
    """
    Rename all photos in incoming folder to unified format: incoming-001.jpg, incoming-002.jpg, etc.
    Move renamed files to renamed/ folder.
    
    Returns:
        Dictionary mapping original names to new names
    """
    # Get all image files (excluding already renamed ones)
    image_extensions = ['.jpg', '.jpeg', '.png', '.webp', '.JPG', '.JPEG', '.PNG', '.WEBP']
    original_files = []
    
    for ext in image_extensions:
        # Find files that don't start with "incoming-"
        files = [f for f in INCOMING_DIR.glob(f"*{ext}") 
                 if not f.name.startswith("incoming-")]
        original_files.extend(files)
    
    if not original_files:
        print("No new photos to rename in data/incoming/")
        return {}
    
    print(f"Found {len(original_files)} photos to rename and move:\n")
    
    rename_map = {}
    next_num = get_next_incoming_number()
    
    for original_file in sorted(original_files):
        # Get file extension
        ext = original_file.suffix.lower()
        # Normalize extension
        if ext in ['.jpeg']:
            ext = '.jpg'
        
        # Generate new filename
        new_name = f"incoming-{next_num:03d}{ext}"
        new_path = RENAMED_DIR / new_name
        
        # Copy file to renamed folder with new name
        try:
            shutil.copy2(original_file, new_path)
            rename_map[original_file.name] = new_name
            print(f"  ✓ {original_file.name} -> {new_name} (moved to data/renamed/)")
            next_num += 1
        except Exception as e:
            print(f"  ✗ Error renaming {original_file.name}: {e}")
    
    print(f"\n✅ Renamed and moved {len(rename_map)} photos to data/renamed/")
    print(f"   Original files remain in data/incoming/")
    return rename_map


if __name__ == "__main__":
    print("Renaming incoming photos to unified format...\n")
    rename_map = rename_and_move_incoming_photos()
    
    if rename_map:
        print("\nRenamed files mapping:")
        for original, new_name in rename_map.items():
            print(f"  {original} -> {new_name}")
        print(f"\nAll renamed files are in: data/renamed/")
        print(f"Original files remain in: data/incoming/")
    else:
        print("\nNo files to rename.")
