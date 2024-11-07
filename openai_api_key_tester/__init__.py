"""OpenAI API Key Tester package."""
from .api_key_tester import main as cli_main
from .gui import main as gui_main

__version__ = "0.1.0"

def main():
    """Entry point for CLI interface."""
    cli_main()

def gui():
    """Entry point for GUI interface."""
    gui_main()
