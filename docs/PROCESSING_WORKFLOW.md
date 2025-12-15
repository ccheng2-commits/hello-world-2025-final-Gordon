# IRIS#1 Processing Workflow

## Step-by-Step Process

### Step 1: Place Photos in Incoming Folder
- Put your original photos (any name) in `data/incoming/`
- Supported formats: `.jpg`, `.jpeg`, `.png`, `.webp`

### Step 2: Rename Photos
```bash
python -m backend.rename_incoming
```
- Renames all photos to unified format: `incoming-001.jpg`, `incoming-002.jpg`, etc.
- Copies renamed files to `data/renamed/` folder
- **Original files remain in `data/incoming/`** (for reference)

### Step 3: Process Photos (Extract Donut Ring)
```bash
python -m backend.iris_processor
```
- Processes photos from `data/renamed/` folder
- Extracts Safe Zone ring (donut) from each photo
- Saves results as `iris-001.jpg`, `iris-002.jpg`, etc. in `data/processed/`
- **Numbering matches**: `incoming-001.jpg` → `iris-001.jpg`

### Step 4: Analyze Photos (Extract Waveform)
```bash
python -m backend.analysis
```
- Analyzes processed iris images
- Extracts FFT waveform and features
- Saves analysis as `analysis_iris-001.json`, etc.

## File Tracking

### Numbering System
- `incoming-001.jpg` → `iris-001.jpg` → `analysis_iris-001.json`
- Same number = same photo throughout the pipeline
- Easy to track which original photo corresponds to which result

### Folder Structure
```
data/
├─ incoming/     # Original photos (any names) - KEPT FOR REFERENCE
├─ renamed/      # Renamed photos (incoming-001.jpg, etc.)
├─ processed/    # Processed donut rings (iris-001.jpg, etc.)
└─ codes/        # Analysis results (analysis_iris-001.json, etc.)
```

## Identifying Problem Photos

If a processed image looks wrong:
1. Check the number: `iris-003.jpg` = problem
2. Find the original: Look for `incoming-003.jpg` in `data/renamed/`
3. Check the original: The original file name is preserved in `data/incoming/` (before renaming)

## Example Workflow

```bash
# 1. Place photos in incoming/
cp ~/Photos/eye1.jpg data/incoming/
cp ~/Photos/eye2.jpg data/incoming/

# 2. Rename them
python -m backend.rename_incoming
# Result: incoming-001.jpg, incoming-002.jpg in data/renamed/

# 3. Process (extract donut)
python -m backend.iris_processor
# Result: iris-001.jpg, iris-002.jpg in data/processed/

# 4. Analyze
python -m backend.analysis
# Result: analysis_iris-001.json, analysis_iris-002.json in data/processed/
```

## Troubleshooting

**Problem:** `iris-003.jpg` looks wrong
**Solution:**
1. Check `data/renamed/incoming-003.jpg` - this is the renamed version
2. Check `data/incoming/` - find the original file that became incoming-003
3. The original might be a bad photo (not a close-up iris, wrong angle, etc.)






