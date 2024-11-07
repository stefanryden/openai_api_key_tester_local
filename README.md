# OpenAI API Key Tester

A comprehensive Python tool to test and validate OpenAI API keys, featuring both GUI and CLI interfaces.

[Svenska instruktioner (Swedish instructions)](README.sv.md)

## Features

- Modern graphical user interface (GUI) with intuitive controls
- Command-line interface (CLI) for automation
- Validates API key format
- Tests API key functionality with OpenAI's API
- Supports testing multiple OpenAI models:
  - GPT-4 and variants (gpt-4, gpt-4-turbo-preview, gpt-4-1106-preview)
  - GPT-4 Vision Preview
  - GPT-3.5 Turbo and variants (gpt-3.5-turbo, gpt-3.5-turbo-16k, gpt-3.5-turbo-1106)
  - DALL-E 3
  - Text Embeddings (text-embedding-ada-002)
- Provides clear feedback on API key status and model accessibility
- Displays usage statistics and billing information:
  - API status
  - Quota availability
  - Timestamp of last check
- Minimal token usage for testing
- Secure key handling with show/hide functionality
- Progress tracking for model testing
- Comprehensive error handling

## Requirements

- Python 3.7 or higher
- OpenAI Python package

## Installation

### Option 1: Install from PyPI (Recommended)

```bash
pip install openai-api-key-tester
```

### Option 2: Install from Local Source

1. Download the package:
   - Clone this repository, or
   - Download and extract the ZIP file

2. Navigate to the package directory:
```bash
cd openai-api-key-tester
```

3. Install the package:
```bash
# Install in development mode
pip install -e .

# Or install regularly
pip install .
```

### Option 3: Run Directly from Source

1. Download and extract the package
2. Install requirements:
```bash
pip install -r requirements.txt
```

3. Run the scripts directly:
```bash
# For GUI
python -m openai_api_key_tester.gui

# For CLI
python -m openai_api_key_tester.api_key_tester
```

## Usage

### GUI Mode

Launch the GUI using one of these methods:
```bash
# If installed via pip
openai-key-tester-gui

# If running from source
python -m openai_api_key_tester.gui
```

### CLI Mode

1. Set your OpenAI API key as an environment variable:
```bash
# Linux/macOS
export OPENAI_API_KEY='your-api-key-here'

# Windows Command Prompt
set OPENAI_API_KEY=your-api-key-here

# Windows PowerShell
$env:OPENAI_API_KEY='your-api-key-here'
```

2. Run the CLI tool:
```bash
# If installed via pip
openai-key-tester

# If running from source
python -m openai_api_key_tester.api_key_tester
```

## Available Models

- GPT-4 (gpt-4)
- GPT-4 Turbo Preview (gpt-4-turbo-preview)
- GPT-4 1106 Preview (gpt-4-1106-preview)
- GPT-4 Vision Preview (gpt-4-vision-preview)
- GPT-3.5 Turbo (gpt-3.5-turbo)
- GPT-3.5 Turbo 16k (gpt-3.5-turbo-16k)
- GPT-3.5 Turbo 1106 (gpt-3.5-turbo-1106)
- DALL-E 3 (dall-e-3)
- Text Embedding Ada 002 (text-embedding-ada-002)

## Error Messages

The tool provides different error messages based on the issue:
- Invalid key format
- Invalid API key
- Model-specific access errors
- Connection errors
- Quota exceeded errors
- Other API-related errors

## Security Notes

- API keys are never stored permanently
- GUI provides a secure input field with show/hide functionality
- Keys are cleared from memory after testing
- Environment variable usage in CLI mode for secure key handling

## Note

This tool uses minimal tokens for testing to avoid unnecessary API usage. Each model test uses only 1 token to verify accessibility, except for DALL-E 3 and Vision models which require specific test inputs.

## Troubleshooting

### Common Issues

1. Module not found error:
   - Ensure you're in the correct directory
   - Verify that requirements are installed
   - Try running with the full module path: `python -m openai_api_key_tester.gui`

2. GUI doesn't start:
   - Verify tkinter is available (included with Python)
   - Try running from the command line to see error messages

3. API key issues:
   - Verify the key format (should start with 'sk-')
   - Check if the key is properly set in environment variables
   - Ensure the key has not expired or been revoked
