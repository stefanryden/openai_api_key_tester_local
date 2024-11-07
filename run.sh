#!/bin/bash
# Install dependencies
pip install -r requirements.txt

# Add package directory to Python path
export PYTHONPATH="${PYTHONPATH:+$PYTHONPATH:}$(pwd)"

# Run GUI version
echo "Starting GUI version..."
python -m openai_api_key_tester.gui

# For CLI version, uncomment the following line:
# python -m openai_api_key_tester.api_key_tester
