# IRIS#1 - How to Run the Complete Project

## Quick Start

### 1. Start the HTTP Server

```bash
python3 start_server.py
```

This will start a server at `http://localhost:8000`

### 2. Open the Frontend

Open your browser and go to:
```
http://localhost:8000/index.html
```

Or simply:
```
http://localhost:8000
```

### 3. View Your Digital Irises

The frontend will automatically load all latent codes from `data/codes_index.json` and display them in the Digital Iris Wall.

## Complete Workflow

### Step 1: Process Images (if you have new photos)

```bash
# Activate virtual environment
source venv/bin/activate

# Rename incoming photos
python3 -m backend.rename_incoming

# Process iris photos
python3 -m backend.iris_processor

# Generate FFT analysis
python3 -m backend.analysis

# Generate latent codes
python3 -m backend.latent_code

# Update codes index (or it updates automatically)
python3 -m backend.generate_codes_index
```

### Step 2: Start Backend Watcher (Optional)

If you want automatic processing when new photos arrive:

```bash
python3 -m backend.watch_folder
```

This watches `data/incoming/` for new photos and processes them automatically.

### Step 3: Start Frontend Server

```bash
python3 start_server.py
```

### Step 4: View in Browser

Open `http://localhost:8000` in your browser.

## Frontend Controls

- **SPACE**: Simulate capture (generates new Digital Iris)
- **T**: Test transform with random code
- **R**: Reset to EXHIBIT state
- **C**: Reload codes from backend

## Auto-Refresh

The frontend automatically refreshes codes from the backend every 5 seconds, so new Digital Irises will appear automatically.

## Troubleshooting

### Frontend shows "Could not load codes from backend"

1. Make sure `data/codes_index.json` exists:
   ```bash
   python3 -m backend.generate_codes_index
   ```

2. Make sure the server is running and accessible at `http://localhost:8000`

3. Check browser console (F12) for errors

### No Digital Irises showing

1. Check if you have processed images:
   ```bash
   ls data/processed/iris-*.jpg
   ```

2. Generate codes if missing:
   ```bash
   python3 -m backend.latent_code
   ```

3. Update index:
   ```bash
   python3 -m backend.generate_codes_index
   ```

### CORS Errors

The server includes CORS headers, but if you're using a different server (like Live Server), make sure it allows loading from `../data/` directory.

## File Structure

```
project/
├── start_server.py          # HTTP server (run this)
├── frontend/
│   ├── index.html          # Main page
│   ├── sketch.js           # p5.js sketch (loads codes from backend)
│   ├── iris_renderer.js    # Digital Iris renderer
│   └── ui_state_machine.js # State machine
├── backend/
│   ├── generate_codes_index.py  # Creates codes_index.json
│   ├── latent_code.py           # Generates codes (auto-updates index)
│   └── ...
└── data/
    ├── codes_index.json    # Frontend reads this
    └── codes/               # Individual code files
```

## Development Mode

For development, you can use VS Code's Live Server extension, but make sure to:
1. Set the root to the project root (not frontend/)
2. Or update the path in `sketch.js` to match your setup

