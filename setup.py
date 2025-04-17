#!/usr/bin/env python
"""
Setup script for the Concert Tour Information System.
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 8):
        print("Error: Python 3.8 or higher is required.")
        sys.exit(1)
    print(f"Python version: {sys.version.split()[0]} ✓")

def check_cuda():
    """Check if CUDA is available."""
    try:
        import torch
        if torch.cuda.is_available():
            print(f"CUDA available: Yes (Version {torch.version.cuda}) ✓")
        else:
            print("CUDA available: No (GPU acceleration will not be used) ⚠")
    except ImportError:
        print("PyTorch not installed. CUDA check skipped.")

def create_env_file():
    """Create .env file if it doesn't exist."""
    env_file = Path(".env")
    if not env_file.exists():
        print("Creating .env file...")
        with open(env_file, "w") as f:
            f.write("# Path to your LLaMA model\n")
            f.write("LLM_MODEL_PATH=models/llama-2-7b-chat.Q4_K_M.gguf\n\n")
            f.write("# For web search functionality (SerpAPI key)\n")
            f.write("SERPAPI_KEY=your_serpapi_key_here\n")
        print(".env file created ✓")
    else:
        print(".env file already exists ✓")

def create_directories():
    """Create necessary directories."""
    directories = [
        "data/document_store",
        "models",
        "services",
        "utils"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"Directory {directory} created/verified ✓")

def check_wsl():
    """Check if running in WSL on Windows."""
    if platform.system() == "Linux":
        try:
            with open("/proc/version", "r") as f:
                if "microsoft" in f.read().lower():
                    print("Running in WSL on Windows ✓")
                    return True
        except:
            pass
    return False

def main():
    """Main setup function."""
    print("=== Concert Tour Information System Setup ===")
    
    # Check Python version
    check_python_version()
    
    # Check if running in WSL on Windows
    is_wsl = check_wsl()
    if platform.system() == "Windows" and not is_wsl:
        print("\n⚠ WARNING: Some packages may not work correctly on native Windows.")
        print("  Consider using WSL2 as described in the README.md")
    
    # Create directories
    create_directories()
    
    # Create .env file
    create_env_file()
    
    # Check CUDA
    check_cuda()
    
    print("\n=== Setup Complete ===")
    print("\nNext steps:")
    print("1. Install dependencies: pip install -r requirements.txt")
    print("2. Download the LLaMA model: python download_model.py")
    print("3. Update your .env file with your SerpAPI key")
    print("4. Run the application: streamlit run app.py")

if __name__ == "__main__":
    main() 