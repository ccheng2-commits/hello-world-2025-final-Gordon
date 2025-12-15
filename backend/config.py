"""
IRIS#1 - Digital Biometrics
Central configuration file for paths, sizes, thresholds, etc.
"""

import os
from pathlib import Path

# Get the project root directory (parent of backend/)
PROJECT_ROOT = Path(__file__).parent.parent

# Data directories
DATA_DIR = PROJECT_ROOT / "data"
INCOMING_DIR = DATA_DIR / "incoming"      # Raw iris photos from camera (original names)
RENAMED_DIR = DATA_DIR / "renamed"        # Renamed photos (incoming-001.jpg, etc.)
PROCESSED_DIR = DATA_DIR / "processed"    # Cropped 1:1 iris images
FFT_DIR = DATA_DIR / "fft"                # FFT spectrum visualization images
CODES_DIR = DATA_DIR / "codes"            # Latent code JSON/txt files
LOGS_DIR = DATA_DIR / "logs"              # Backend logs

# Ensure all data directories exist
for dir_path in [INCOMING_DIR, RENAMED_DIR, PROCESSED_DIR, FFT_DIR, CODES_DIR, LOGS_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)

# Image processing settings
IRIS_CROP_SIZE = 2048  # Size of the 1:1 square crop (pixels) - High resolution for quality
IRIS_CENTER_OFFSET_X = 0  # For now, we'll do center crop (no pupil detection yet)
IRIS_CENTER_OFFSET_Y = 0

# FFT settings
FFT_IMAGE_SIZE = 512  # Output size for FFT visualization
FFT_COLORMAP = "viridis"  # Matplotlib colormap for spectrum visualization

# Latent code settings
LATENT_CODE_VERSION = "I"  # IRIS/I? (matching original design)
LATENT_SEED_BASE = 1000000000  # Base for seed generation (not used in new format)

# File watching settings
WATCH_PATTERNS = ["*.jpg", "*.jpeg", "*.png"]  # File patterns to watch
WATCH_INTERVAL = 1.0  # Check interval in seconds (for polling fallback)

