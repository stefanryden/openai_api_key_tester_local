@echo off
echo Installing dependencies...
pip install -r requirements.txt

echo Setting up Python path...
set PYTHONPATH=%PYTHONPATH%;%CD%

echo Starting GUI version...
python -m openai_api_key_tester.gui

rem For CLI version, uncomment the following line:
rem python -m openai_api_key_tester.api_key_tester

pause
