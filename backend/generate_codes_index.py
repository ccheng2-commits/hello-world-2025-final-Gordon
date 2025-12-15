"""
IRIS#1 - Digital Biometrics
Generate codes index JSON file for frontend to read latent codes.
This script scans data/codes/ and creates a JSON index file that the frontend can load via HTTP.
"""

import json
from pathlib import Path
from backend.config import CODES_DIR, DATA_DIR

def generate_codes_index():
    """
    Scan data/codes/ directory and generate a JSON index file.
    Returns list of latent codes with metadata.
    """
    codes_list = []
    
    # Find all .txt files in codes directory
    code_files = sorted(CODES_DIR.glob("code_*.txt"))
    
    for code_file in code_files:
        try:
            # Read the latent code from .txt file
            with open(code_file, 'r') as f:
                latent_code = f.read().strip()
            
            # Extract iris number from filename (e.g., "code_iris-001.txt" -> "iris-001")
            filename = code_file.stem  # "code_iris-001"
            iris_id = filename.replace("code_", "")  # "iris-001"
            
            # Also check if there's a corresponding JSON file for metadata
            json_file = code_file.with_suffix('.json')
            metadata = {}
            if json_file.exists():
                try:
                    with open(json_file, 'r') as f:
                        metadata = json.load(f)
                except:
                    pass
            
            codes_list.append({
                'id': iris_id,
                'code': latent_code,
                'filename': code_file.name,
                'metadata': metadata
            })
            
        except Exception as e:
            print(f"Warning: Could not read {code_file.name}: {e}")
            continue
    
    # Sort by iris number (iris-001, iris-002, etc.)
    codes_list.sort(key=lambda x: x['id'])
    
    return codes_list

def save_codes_index(output_path=None):
    """
    Generate codes index and save to JSON file.
    Default location: data/codes_index.json
    """
    if output_path is None:
        output_path = DATA_DIR / "codes_index.json"
    
    codes_list = generate_codes_index()
    
    index_data = {
        'version': '1.0',
        'count': len(codes_list),
        'codes': codes_list,
        'last_updated': None  # Will be set by frontend or can add timestamp here
    }
    
    with open(output_path, 'w') as f:
        json.dump(index_data, f, indent=2)
    
    print(f"✓ Generated codes index: {output_path}")
    print(f"  Found {len(codes_list)} latent codes")
    
    return output_path

if __name__ == "__main__":
    save_codes_index()

