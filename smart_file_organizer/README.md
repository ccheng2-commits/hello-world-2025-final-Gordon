# SmartFileOrganizer

A robust, local-first file organization daemon for macOS that intelligently organizes files using a hybrid routing system.

## Architecture

SmartFileOrganizer uses a **3-layer hybrid routing logic**:

1. **Layer 1 (Fast Track):** Regex/Prefix matching - 100% deterministic, instant processing
2. **Layer 2 (Versioning):** Detects file versions and manages history
3. **Layer 3 (AI Fallback):** Semantic categorization using local Qwen2.5 via Ollama

## Philosophy

**"Rule-based first, AI-based second."** This ensures accuracy and saves compute by only using AI when necessary.

## Development Status

### ✅ Phase 1: Watchdog Observer (COMPLETE)
- File system monitoring using `watchdog`
- Event handling for file creation, modification, deletion
- Logging infrastructure
- Configuration management

### 🔄 Phase 2: Hybrid Router & Prefix Rules (PENDING)
- Implement Layer 1 routing logic
- Prefix and regex rule matching
- File movement operations

### 🔄 Phase 3: Versioning System (PENDING)
- Detect file versions (e.g., `_v2`, `_v3`)
- Replace old versions and archive to `_History`

### 🔄 Phase 4: Ollama/Qwen Integration (PENDING)
- Local LLM integration for semantic categorization
- Fallback routing when rules don't match

## Installation

### Prerequisites
- Python 3.10+
- macOS (designed for macOS, but may work on other Unix systems)

### Setup

1. Install dependencies:
```bash
pip install watchdog ollama
```

2. Ensure Ollama is running (for Phase 4):
```bash
ollama serve
ollama pull qwen2.5
```

## Configuration

Edit `config.py` to customize:

- `DEFAULT_WATCH_DIR`: Directory to monitor (default: `~/Desktop`)
- `DEFAULT_ARCHIVE_DIR`: Where organized files are moved (default: `~/Documents/SmartFileArchive`)
- `PREFIX_RULES`: Dictionary of prefix patterns to destination folders
- `REGEX_RULES`: List of regex patterns to destination folders

## Usage

Run the daemon:

```bash
python smart_file_organizer/main.py
```

The daemon will:
- Monitor the configured watch directory
- Log all file events to `~/Documents/SmartFileArchive/_logs/organizer.log`
- Process files according to the hybrid routing logic (once Phase 2+ is implemented)

Press `Ctrl+C` to stop the daemon.

## Privacy

All processing is done locally. No external API calls are made. The AI component uses a local Ollama instance running on your machine.

## Project Structure

```
smart_file_organizer/
├── __init__.py          # Package initialization
├── config.py            # Configuration settings
├── main.py              # Main daemon entry point (Phase 1)
├── router.py            # Hybrid routing logic (Phase 2)
├── versioning.py        # Version detection system (Phase 3)
├── ai_categorizer.py    # Ollama/Qwen integration (Phase 4)
└── README.md            # This file
```

## License

[Your License Here]

