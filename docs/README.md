# IRIS#1 - Digital Biometrics

Interactive installation for MFA Interaction Design "Hello World" final project.

## Project Overview

IRIS#1 transforms a visitor's iris photograph into a unique generative "Digital Iris" - a looping, animated circular pattern that represents their biometric signature.

### Concept

1. Visitor's iris is photographed with DSLR (Canon 5D Mark IV + 60mm macro)
2. Photo is automatically sent to Mac mini
3. Python backend processes the image:
   - Detects and crops iris region
   - Computes 2D FFT (Fast Fourier Transform)
   - Extracts features and generates latent code
4. Web frontend renders the Digital Iris from the latent code
5. New Digital Iris is added to the "Digital Iris Wall" gallery

## Project Structure

```
iris1-digital-biometrics/
├─ backend/                # Python processing pipeline
│  ├─ watch_folder.py      # Watches for new photos
│  ├─ iris_processor.py    # Crop iris region
│  ├─ fft_pipeline.py      # Compute FFT and visualization
│  ├─ latent_code.py       # Generate latent code strings
│  ├─ config.py            # Configuration
│  └─ tests/
│
├─ frontend/               # Web interface (p5.js)
│  ├─ index.html
│  ├─ sketch.js           # Main p5.js sketch
│  ├─ iris_renderer.js    # Digital Iris renderer
│  └─ ui_state_machine.js # UI state management
│
├─ data/                   # Runtime data (not in git)
│  ├─ incoming/            # Raw photos
│  ├─ processed/           # Cropped irises
│  ├─ fft/                 # FFT visualizations
│  ├─ codes/               # Latent codes
│  └─ logs/                # Logs
│
└─ docs/                   # Documentation
```

## Setup

### Backend Setup

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Place test iris photos in `data/incoming/`

3. Run processing pipeline:
```bash
# Process a single image
python -m backend.iris_processor
python -m backend.fft_pipeline
python -m backend.latent_code
```

### Frontend Setup

1. Open `frontend/index.html` in a web browser
2. Or use a local server:
```bash
cd frontend
python -m http.server 8000
# Then open http://localhost:8000
```

## State Machine

The frontend uses a state machine with these states:

- **EXHIBIT**: Shows Digital Iris Wall (gallery)
- **CAPTURE**: Capturing screen
- **TRANSFORM**: Algorithm running (shows iris + FFT)
- **DISPLAY_SINGLE**: Shows new visitor's Digital Iris
- **UPDATE_EXHIBIT**: Brief transition to add to wall

## Testing

### Frontend Testing

- Press **SPACE** to simulate capture
- Press **T** to test transform directly
- Press **R** to reset to exhibit

### Backend Testing

Each module can be run independently for testing:
- `iris_processor.py` - processes images in `data/incoming/`
- `fft_pipeline.py` - computes FFT for images in `data/processed/`
- `latent_code.py` - generates codes for images in `data/processed/`

## Latent Code Format

Latent codes encode iris features into a string:
```
IRIS/1?seed=2481739201&H0=212&dH=18&R0=0.41&ring=0.27&tex=0.63&λ=0.010
```

Parameters:
- `seed`: Deterministic seed for generative pattern
- `H0`: Average brightness
- `dH`: Contrast
- `R0`: Radial structure ratio
- `ring`: Ring pattern energy
- `tex`: Texture complexity
- `λ`: Frequency balance

## MVP Features

✅ Working frontend state machine  
✅ Digital Iris renderer from latent code  
✅ Basic Python processing pipeline  
✅ Simple center crop (no pupil detection yet)  
✅ FFT computation and visualization  
✅ Latent code generation  

## Future Enhancements

- Real-time camera integration
- Automatic pupil detection
- More sophisticated feature extraction
- 3D rendering options
- Physical output printing

## Notes

This is a learning project. Code is structured to be beginner-friendly with clear comments and incremental complexity.

