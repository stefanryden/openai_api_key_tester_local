from .api_key_tester import main as cli_main
from .gui import main as gui_main

__version__ = "0.1.0"

def main():
    """Entry point for the application."""
    try:
        gui_main()
    except Exception as e:
        print(f"GUI failed to start: {str(e)}. Falling back to CLI mode.")
        cli_main()
