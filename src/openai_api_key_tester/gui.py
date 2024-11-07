import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import os
from typing import List, Optional
from .api_key_tester import (
    validate_key_format, test_model, get_usage_stats,
    validate_ollama_url, test_ollama_model, get_ollama_status,
    OPENAI_MODELS, OLLAMA_MODELS
)
from openai import OpenAI, APIError, APIConnectionError
import requests

class APIKeyTesterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("API Key Tester")
        self.root.geometry("800x900")
        
        # Configure styles
        self.configure_styles()
        
        # Create main container with padding
        main_container = ttk.Frame(root, padding="20", style="Main.TFrame")
        main_container.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(
            main_container, 
            text="API Key Tester",
            style="Title.TLabel"
        )
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # OpenAI Section
        openai_section = ttk.LabelFrame(
            main_container, 
            text="OpenAI API Configuration", 
            padding="10",
            style="Section.TLabelframe"
        )
        openai_section.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15))
        
        ttk.Label(
            openai_section, 
            text="OpenAI API Key:",
            style="Heading.TLabel"
        ).grid(row=0, column=0, sticky=tk.W, pady=5)
        
        # API key input with frame
        key_input_frame = ttk.Frame(openai_section)
        key_input_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.api_key_var = tk.StringVar(value='')
        self.api_key_entry = ttk.Entry(
            key_input_frame, 
            textvariable=self.api_key_var, 
            width=50, 
            show="*",
            style="APIKey.TEntry"
        )
        self.api_key_entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 10))
        
        # Key management buttons
        self.show_key = tk.BooleanVar(value=False)
        self.toggle_key_btn = ttk.Button(
            key_input_frame, 
            text="Show Key",
            style="Action.TButton",
            command=self.toggle_key_visibility
        )
        self.toggle_key_btn.pack(side=tk.LEFT, padx=2)
        
        self.clear_key_btn = ttk.Button(
            key_input_frame, 
            text="Clear Key",
            style="Action.TButton",
            command=self.clear_api_key
        )
        self.clear_key_btn.pack(side=tk.LEFT, padx=2)

        # Ollama Section
        ollama_section = ttk.LabelFrame(
            main_container, 
            text="Ollama API Configuration", 
            padding="10",
            style="Section.TLabelframe"
        )
        ollama_section.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15))
        
        ttk.Label(
            ollama_section, 
            text="Ollama API URL:",
            style="Heading.TLabel"
        ).grid(row=0, column=0, sticky=tk.W, pady=5)
        
        # Ollama URL input with frame
        ollama_input_frame = ttk.Frame(ollama_section)
        ollama_input_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.ollama_url_var = tk.StringVar(value='http://localhost:11434')
        self.ollama_url_entry = ttk.Entry(
            ollama_input_frame, 
            textvariable=self.ollama_url_var, 
            width=50,
            style="APIKey.TEntry"
        )
        self.ollama_url_entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 10))
        
        # Model Selection Section
        model_section = ttk.LabelFrame(
            main_container, 
            text="Model Selection", 
            padding="10",
            style="Section.TLabelframe"
        )
        model_section.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15))
        
        # Create notebook for OpenAI and Ollama models
        model_notebook = ttk.Notebook(model_section)
        model_notebook.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        
        # OpenAI models frame
        openai_models_frame = ttk.Frame(model_notebook)
        model_notebook.add(openai_models_frame, text='OpenAI Models')
        
        ttk.Label(
            openai_models_frame, 
            text="Select OpenAI Models to Test:",
            style="Heading.TLabel"
        ).pack(anchor=tk.W, pady=5)
        
        self.openai_model_listbox = tk.Listbox(
            openai_models_frame,
            selectmode=tk.MULTIPLE,
            height=8,
            font=('Segoe UI', 10),
            bg='#ffffff',
            selectbackground='#0078D4',
            activestyle='none'
        )
        self.openai_model_listbox.pack(fill=tk.X, pady=5)
        for model in OPENAI_MODELS:
            self.openai_model_listbox.insert(tk.END, model)
            
        # Ollama models frame
        ollama_models_frame = ttk.Frame(model_notebook)
        model_notebook.add(ollama_models_frame, text='Ollama Models')
        
        ttk.Label(
            ollama_models_frame, 
            text="Select Ollama Models to Test:",
            style="Heading.TLabel"
        ).pack(anchor=tk.W, pady=5)
        
        self.ollama_model_listbox = tk.Listbox(
            ollama_models_frame,
            selectmode=tk.MULTIPLE,
            height=8,
            font=('Segoe UI', 10),
            bg='#ffffff',
            selectbackground='#0078D4',
            activestyle='none'
        )
        self.ollama_model_listbox.pack(fill=tk.X, pady=5)
        for model in OLLAMA_MODELS:
            self.ollama_model_listbox.insert(tk.END, model)
            
        # Model selection buttons
        button_frame = ttk.Frame(model_section)
        button_frame.grid(row=2, column=0, columnspan=3, pady=(10, 0))
        ttk.Button(
            button_frame,
            text="Select All",
            style="Action.TButton",
            command=lambda: self.select_all_models(model_notebook.index("current"))
        ).pack(side=tk.LEFT, padx=5)
        ttk.Button(
            button_frame,
            text="Clear Selection",
            style="Action.TButton",
            command=lambda: self.clear_model_selection(model_notebook.index("current"))
        ).pack(side=tk.LEFT)
        
        # Test Button
        self.test_button = ttk.Button(
            main_container,
            text="Test APIs",
            style="Primary.TButton",
            command=self.run_tests
        )
        self.test_button.grid(row=4, column=0, columnspan=3, pady=15)
        
        # Results Section
        results_section = ttk.LabelFrame(
            main_container,
            text="Test Results",
            padding="10",
            style="Section.TLabelframe"
        )
        results_section.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 15))
        
        # Results text area with custom style
        self.results_text = scrolledtext.ScrolledText(
            results_section,
            width=70,
            height=15,
            font=('Consolas', 10),
            bg='#ffffff',
            wrap=tk.WORD
        )
        self.results_text.grid(row=0, column=0, pady=5)
        
        # Progress bar with custom style
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            main_container,
            length=300,
            mode='determinate',
            variable=self.progress_var,
            style="Custom.Horizontal.TProgressbar"
        )
        self.progress_bar.grid(row=6, column=0, columnspan=3, pady=5, sticky=(tk.W, tk.E))
        
        # Configure grid weights
        main_container.columnconfigure(0, weight=1)
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        
        # Bind window closing event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def configure_styles(self):
        """Configure custom styles for the application"""
        style = ttk.Style()
        
        # Configure colors
        style.configure(".",
            background="#f0f2f5",
            foreground="#000000",
            font=('Segoe UI', 10)
        )
        
        # Title style
        style.configure("Title.TLabel",
            font=('Segoe UI', 16, 'bold'),
            padding=10
        )
        
        # Heading style
        style.configure("Heading.TLabel",
            font=('Segoe UI', 11, 'bold')
        )
        
        # Section frame style
        style.configure("Section.TLabelframe",
            background="#ffffff",
            padding=10
        )
        style.configure("Section.TLabelframe.Label",
            font=('Segoe UI', 11, 'bold'),
            foreground="#0078D4"
        )
        
        # Button styles
        style.configure("Action.TButton",
            padding=5
        )
        
        style.configure("Primary.TButton",
            padding=10,
            font=('Segoe UI', 11, 'bold')
        )
        
        # Entry style
        style.configure("APIKey.TEntry",
            padding=5
        )
        
        # Progress bar style
        style.configure("Custom.Horizontal.TProgressbar",
            troughcolor='#f0f2f5',
            background='#0078D4',
            thickness=15
        )

    def clear_api_key(self):
        """Clear API key from memory"""
        self.api_key_var.set("")
        self.api_key_entry.delete(0, tk.END)

    def on_closing(self):
        """Handle window closing"""
        self.clear_api_key()
        self.root.destroy()

    def toggle_key_visibility(self):
        """Toggle API key visibility"""
        if self.show_key.get():
            self.api_key_entry.configure(show="*")
            self.toggle_key_btn.configure(text="Show Key")
        else:
            self.api_key_entry.configure(show="")
            self.toggle_key_btn.configure(text="Hide Key")
        self.show_key.set(not self.show_key.get())

    def select_all_models(self, tab_index):
        """Select all models in the current tab"""
        if tab_index == 0:  # OpenAI models
            self.openai_model_listbox.select_set(0, tk.END)
        else:  # Ollama models
            self.ollama_model_listbox.select_set(0, tk.END)

    def clear_model_selection(self, tab_index):
        """Clear all model selections in the current tab"""
        if tab_index == 0:  # OpenAI models
            self.openai_model_listbox.selection_clear(0, tk.END)
        else:  # Ollama models
            self.ollama_model_listbox.selection_clear(0, tk.END)

    def get_selected_models(self) -> tuple[List[str], List[str]]:
        """Get list of selected models for both APIs"""
        openai_models = [self.openai_model_listbox.get(idx) for idx in self.openai_model_listbox.curselection()]
        ollama_models = [self.ollama_model_listbox.get(idx) for idx in self.ollama_model_listbox.curselection()]
        return openai_models, ollama_models

    def update_results(self, text: str, clear: bool = False):
        """Update results area"""
        if clear:
            self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, text + "\n")
        self.results_text.see(tk.END)
        self.root.update_idletasks()

    def run_tests(self):
        """Run API tests"""
        self.update_results("", clear=True)
        self.progress_var.set(0)
        
        openai_models, ollama_models = self.get_selected_models()
        total_steps = len(openai_models) + len(ollama_models) + 2  # +2 for initial checks
        current_step = 0
        
        # Test OpenAI API
        api_key = self.api_key_var.get().strip()
        if api_key:
            if not validate_key_format(api_key):
                messagebox.showerror("Error", "Invalid OpenAI API key format. OpenAI API keys should start with 'sk-'")
                return

            self.update_results("Testing OpenAI API...")
            try:
                client = OpenAI(api_key=api_key)
                self.update_results("✅ OpenAI API client initialized successfully\n")
                
                # Get usage statistics
                stats = get_usage_stats(client)
                self.update_results("\n" + "="*50)
                if stats["status"] == "success":
                    data = stats["data"]
                    self.update_results("📊 OpenAI API Status Check:")
                    self.update_results(f"- Checked at: {data['checked_at']}")
                    self.update_results(f"- API Status: {data['api_status']}")
                    self.update_results(f"- Quota Status: {data['quota_status']}")
                else:
                    self.update_results(f"❌ Failed to retrieve OpenAI API status:\n{stats['error']}")

                current_step += 1
                self.progress_var.set((current_step / total_steps) * 100)

                if openai_models:
                    self.update_results("\nTesting OpenAI models:")
                    for model in openai_models:
                        success, message = test_model(client, model)
                        self.update_results(message)
                        current_step += 1
                        self.progress_var.set((current_step / total_steps) * 100)
                        
            except Exception as e:
                self.update_results(f"\n❌ OpenAI API Error: {str(e)}")
        else:
            self.update_results("ℹ️ OpenAI API key not provided, skipping OpenAI tests.")
            current_step += 1
            self.progress_var.set((current_step / total_steps) * 100)

        # Test Ollama API
        ollama_url = self.ollama_url_var.get().strip()
        if validate_ollama_url(ollama_url):
            self.update_results("\nTesting Ollama API...")
            try:
                # Get Ollama status
                stats = get_ollama_status(ollama_url)
                self.update_results("\n" + "="*50)
                if stats["status"] == "success":
                    data = stats["data"]
                    self.update_results("📊 Ollama API Status Check:")
                    self.update_results(f"- Checked at: {data['checked_at']}")
                    self.update_results(f"- API Status: {data['api_status']}")
                    self.update_results(f"- Available Models: {data['available_models']}")

                    if ollama_models:
                        self.update_results("\nTesting Ollama models:")
                        for model in ollama_models:
                            success, message = test_ollama_model(ollama_url, model)
                            self.update_results(message)
                            current_step += 1
                            self.progress_var.set((current_step / total_steps) * 100)
                else:
                    self.update_results(f"❌ Failed to retrieve Ollama API status:\n{stats['error']}")
            except Exception as e:
                self.update_results(f"\n❌ Ollama API Error: {str(e)}")
        else:
            self.update_results("\nℹ️ Invalid Ollama API URL, skipping Ollama tests.")

        self.update_results("\n✅ Test completed.")
        self.progress_var.set(100)

def main():
    root = tk.Tk()
    app = APIKeyTesterGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
