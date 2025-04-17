#!/usr/bin/env python
"""
Script to download the LLaMA model for the Concert Tour Information System.
"""

import os
import sys
import requests
from pathlib import Path
import argparse
from tqdm import tqdm

def download_file(url, destination):
    """
    Download a file with progress bar.
    
    Args:
        url (str): URL to download from
        destination (str): Path to save the file to
    """
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(destination), exist_ok=True)
    
    with open(destination, 'wb') as file, tqdm(
        desc=os.path.basename(destination),
        total=total_size,
        unit='iB',
        unit_scale=True,
        unit_divisor=1024,
    ) as progress_bar:
        for data in response.iter_content(chunk_size=1024):
            size = file.write(data)
            progress_bar.update(size)

def main():
    parser = argparse.ArgumentParser(description='Download LLaMA model for Concert Tour Information System')
    parser.add_argument('--model', type=str, default='llama-2-7b-chat.Q4_K_M.gguf',
                        help='Model name to download (default: llama-2-7b-chat.Q4_K_M.gguf)')
    parser.add_argument('--output', type=str, default='models/llama-2-7b-chat.Q4_K_M.gguf',
                        help='Output path for the model (default: models/llama-2-7b-chat.Q4_K_M.gguf)')
    
    args = parser.parse_args()
    
    # Model URLs (these are examples, you would need to provide actual URLs)
    model_urls = {
        'llama-2-7b-chat.Q4_K_M.gguf': 'https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/resolve/main/llama-2-7b-chat.Q4_K_M.gguf',
        'llama-2-13b-chat.Q4_K_M.gguf': 'https://huggingface.co/TheBloke/Llama-2-13B-Chat-GGUF/resolve/main/llama-2-13b-chat.Q4_K_M.gguf',
    }
    
    if args.model not in model_urls:
        print(f"Error: Model {args.model} not found. Available models: {', '.join(model_urls.keys())}")
        sys.exit(1)
    
    url = model_urls[args.model]
    destination = args.output
    
    print(f"Downloading {args.model} to {destination}...")
    try:
        download_file(url, destination)
        print(f"Download complete! Model saved to {destination}")
        print("\nDon't forget to update your .env file with the correct model path:")
        print(f"LLM_MODEL_PATH={destination}")
    except Exception as e:
        print(f"Error downloading model: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 