# Kautsar Sedot PDF

## Purpose
This project is designed to automate the process of extracting and organizing data from PDF files. The main functionality is handled by `main.py`, which processes PDFs using Python libraries, while `reset.bat` provides a convenient way to reset the environment or clear temporary files.

## Logic
1. **PDF Processing**: `main.py` uses PyPDF2 to extract text and metadata from PDF files.
2. **Data Organization**: Extracted data is saved in structured formats (e.g., CSV or JSON) for further analysis.
3. **Reset Functionality**: `reset.bat` clears temporary files and logs to ensure a clean state for subsequent runs.

## Installation
1. **Python Setup**: Ensure Python 3.9+ is installed. [Download Python](https://www.python.org/downloads/)
2. **Dependencies**: Install required packages via pip:
   ```bash
   pip install -r requirements.txt
   ```
3. **Virtual Environment**: 
   - Create a virtual environment:
     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```
   - For macOS/Linux:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```
3. **Git Ignore**: The `.gitignore` file excludes unnecessary files (e.g., logs, caches) from version control.

## How to Run
1. **Run Main Script**:
   ```bash
   python main.py
   ```
   This will process PDFs in the current directory and save outputs to `output/`.

2. **Reset Environment**:
   ```bash
   reset.bat
   ```
   This will delete temporary files and logs, preparing the environment for a fresh run.

## Notes
- Ensure all PDF files are in the root directory or subfolders for full processing.
- The `reset.bat` script is optimized for Windows environments. For macOS/Linux, use equivalent shell commands.
