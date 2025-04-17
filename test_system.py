#!/usr/bin/env python
"""
Test script for the Concert Tour Information System.
"""

import os
import sys
import importlib
from pathlib import Path
from dotenv import load_dotenv

def check_imports():
    """Check if all required packages are installed."""
    required_packages = [
        "streamlit",
        "langchain",
        "faiss",
        "sentence_transformers",
        "python_dotenv",
        "llama_cpp",
        "torch",
        "tqdm",
        "requests"
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            importlib.import_module(package)
            print(f"✓ {package} is installed")
        except ImportError:
            missing_packages.append(package)
            print(f"✗ {package} is not installed")
    
    if missing_packages:
        print("\nMissing packages. Please install them with:")
        print("pip install -r requirements.txt")
        return False
    
    return True

def check_env_file():
    """Check if .env file exists and has required variables."""
    env_file = Path(".env")
    if not env_file.exists():
        print("✗ .env file not found")
        return False
    
    load_dotenv()
    
    required_vars = ["LLM_MODEL_PATH", "SERPAPI_KEY"]
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
            print(f"✗ {var} not set in .env file")
        else:
            print(f"✓ {var} is set in .env file")
    
    if missing_vars:
        print("\nMissing environment variables. Please update your .env file.")
        return False
    
    return True

def check_model_file():
    """Check if the LLaMA model file exists."""
    model_path = os.getenv("LLM_MODEL_PATH")
    if not model_path:
        print("✗ LLM_MODEL_PATH not set in .env file")
        return False
    
    model_file = Path(model_path)
    if not model_file.exists():
        print(f"✗ Model file not found at {model_path}")
        print("  Please download the model using: python download_model.py")
        return False
    
    print(f"✓ Model file found at {model_path}")
    return True

def check_directories():
    """Check if all required directories exist."""
    required_dirs = [
        "data/document_store",
        "models",
        "services",
        "utils"
    ]
    
    missing_dirs = []
    
    for directory in required_dirs:
        if not Path(directory).exists():
            missing_dirs.append(directory)
            print(f"✗ Directory {directory} not found")
        else:
            print(f"✓ Directory {directory} exists")
    
    if missing_dirs:
        print("\nMissing directories. Please run: python setup.py")
        return False
    
    return True

def check_cuda():
    """Check if CUDA is available."""
    try:
        import torch
        if torch.cuda.is_available():
            print(f"✓ CUDA is available (Version {torch.version.cuda})")
            return True
        else:
            print("⚠ CUDA is not available. GPU acceleration will not be used.")
            return False
    except ImportError:
        print("⚠ PyTorch not installed. CUDA check skipped.")
        return False

def main():
    """Main test function."""
    print("=== Concert Tour Information System Test ===")
    
    # Check imports
    print("\nChecking required packages...")
    imports_ok = check_imports()
    
    # Check .env file
    print("\nChecking .env file...")
    env_ok = check_env_file()
    
    # Check model file
    print("\nChecking model file...")
    model_ok = check_model_file()
    
    # Check directories
    print("\nChecking directories...")
    dirs_ok = check_directories()
    
    # Check CUDA
    print("\nChecking CUDA...")
    cuda_ok = check_cuda()
    
    # Summary
    print("\n=== Test Summary ===")
    if imports_ok and env_ok and model_ok and dirs_ok:
        print("✓ All checks passed! The system is ready to use.")
        print("\nYou can start the application with:")
        print("streamlit run app.py")
    else:
        print("⚠ Some checks failed. Please fix the issues above.")
        print("\nYou can run the setup script to fix most issues:")
        print("python setup.py")

if __name__ == "__main__":
    main() 