# Local Installation Instructions

1. Extract the ZIP file contents
2. Open a terminal/command prompt in the extracted directory
3. Run the appropriate script for your system:
   - Windows: Double-click `run.bat` or run it from command prompt
   - Linux/Mac: Open terminal and run `chmod +x run.sh && ./run.sh`

## Manual Installation

If the automatic scripts don't work, follow these steps:

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Add the package directory to Python path:
   ```bash
   # Linux/Mac
   export PYTHONPATH="${PYTHONPATH:+$PYTHONPATH:}$(pwd)"
   
   # Windows
   set PYTHONPATH=%PYTHONPATH%;%CD%
   ```

3. Run the application:
   ```bash
   # For GUI
   python -m openai_api_key_tester.gui
   
   # For CLI
   python -m openai_api_key_tester.api_key_tester
   ```

## Troubleshooting

If you encounter a "Module not found" error:
1. Verify you're in the correct directory
2. Ensure PYTHONPATH includes the current directory
3. Check if all dependencies are installed
