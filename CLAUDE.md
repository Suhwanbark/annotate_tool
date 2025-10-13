# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview
This is a lightweight ESG report annotation tool built in pure Python. It's a desktop application that allows a single annotator to efficiently analyze ESG reports locally without requiring servers or complex security configurations. The tool supports the complete workflow from PDF preprocessing to candidate mining, manual verification, and CSV/JSON export.

## Development Commands

### Installation and Setup
```bash
pip install -r requirements.txt
```

### Running the Application
```bash
python main.py --data_dir ./pdfs --project myproj
# Optional: enable OCR for images/tables
python main.py --data_dir ./pdfs --project myproj --ocr
```

### Export Annotations
```bash
python -m annotation.export --project myproj --pdf ./pdfs/report.pdf --uid annotatorA --company tsmc
```

### Testing
```bash
# Syntax check
python -m py_compile $(git ls-files '*.py')

# Run tests
pytest
```

## Architecture

### Core Components
- **pdf_loader.py**: PDF preprocessing using PyMuPDF to generate page-by-page PNG images and text extraction, with optional Tesseract OCR
- **ui.py**: Tkinter-based UI with three panels - left metric tree, center page canvas for box drawing, right candidate/input panel
- **annotation/store.py**: JSON-based storage with autosave and timestamped backups for each metric
- **candidate_miner/**: Auto-candidate mining system with both heuristic and LLM-based approaches
- **annotation/export.py**: Export system generating RegCom-required formats

### Data Flow
1. PDF preprocessing creates `pages/` directory with PNG images and metadata
2. Auto-candidate mining uses regex heuristics (units like `%`, `tCO2e`, `GJ`, `m³`) and optional LLM API calls
3. UI allows manual annotation with keyboard shortcuts (`←/→/↑/↓` navigation, `b` add box, `c` complete, `del` delete)
4. All changes auto-save to metric-specific JSON files in `annotations/` directory
5. Export generates `tsmc_5.csv`, `full_report_agg.csv`, `single_page_pairs.csv`, and `metadata.json`

### LLM Integration
- Configure `config/config.json` with `llm_base_url`, `llm_model`, and `api_key`
- Calls `/responses` endpoint with strict JSON Schema defined in `candidate_miner/prompts.py`
- Uses `CandidateList` schema for structured candidate mining responses

### Project Structure
```
myproj/
  pages/         # Page PNGs and metadata.json
  annotations/   # Auto-saved JSON annotation data
  exports/       # CSV/JSON export results
  metric_sid_map.json
```

## Development Guidelines

### Lightweight Principles
- Essential dependencies: PyMuPDF, Pillow, Tkinter (pytesseract and requests are optional)
- No databases or server configurations
- Pure Python, cross-platform compatible (Windows/Mac/Linux)
- Python 3.9+ required

### Code Conventions
- All user documentation in Korean
- Auto-save all UI interactions to metric-specific JSON with timestamped backups
- Maintain three-panel Tkinter UI structure
- Support keyboard shortcuts for efficient annotation workflow
- Export data in RegCom-required formats: `tsmc_5.csv`, `full_report_agg.csv`, `single_page_pairs.csv`, `metadata.json`

### Testing Requirements
- Run syntax check with `python -m py_compile $(git ls-files '*.py')` before commits
- Run `pytest` to verify functionality
- Tests cover heuristic candidate mining, storage operations, and export format validation