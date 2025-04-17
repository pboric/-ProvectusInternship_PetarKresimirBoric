# Frequently Asked Questions (FAQ)

## Installation and Setup

### Q: Why do I need to use WSL on Windows?
A: Some packages in this project, particularly `faiss-gpu`, have compatibility issues with native Windows. WSL provides a Linux environment that ensures all packages work correctly.

### Q: How do I install WSL?
A: Open PowerShell as Administrator and run `wsl --install`. Restart your computer and follow the prompts to complete the setup.

### Q: What if I don't have a CUDA-capable GPU?
A: You can still run the system, but it will be slower. Install `faiss-cpu` instead of `faiss-gpu` by modifying the requirements.txt file.

### Q: How do I get a SerpAPI key?
A: Visit [SerpAPI's website](https://serpapi.com/), sign up for an account, and get your API key from the dashboard.

## Model and Data

### Q: Where can I download the LLaMA model?
A: The model can be downloaded using the `download_model.py` script, which will fetch it from Hugging Face.

### Q: How much disk space does the LLaMA model require?
A: The LLaMA 2 7B Chat model in GGUF format requires approximately 4GB of disk space.

### Q: What types of documents can I upload?
A: The system accepts text documents (TXT) related to concert tours for 2025-2026. Documents about other topics will be rejected.

## Troubleshooting

### Q: I'm getting a "CUDA not available" error. What should I do?
A: Ensure you have the latest NVIDIA drivers installed and that CUDA is properly set up. You can check CUDA availability by running `python -c "import torch; print(torch.cuda.is_available())"`.

### Q: The model fails to load. What's wrong?
A: Check that the model path in your `.env` file is correct and that the model file exists at that location. Also ensure you have enough RAM (at least 8GB recommended).

### Q: How do I fix package installation issues?
A: Try installing packages one by one to identify problematic dependencies. For Windows users, use WSL as described in the README.

### Q: The web search functionality isn't working. Why?
A: Verify that your SerpAPI key is correctly set in the `.env` file. If you're seeing status code 520 errors, these are temporary Cloudflare issues that will resolve themselves.

## Usage

### Q: How do I add documents to the system?
A: Use the "Upload Documents" tab in the web interface to paste or upload concert tour documents.

### Q: How do I ask questions about concert tours?
A: Use the "Ask Questions" tab to type your question and get an answer based on the ingested documents.

### Q: Can I search for concert information online?
A: Yes, use the "Web Search" tab to search for information about artists' upcoming concerts.

### Q: How accurate are the answers?
A: The system uses Retrieval-Augmented Generation (RAG) to ensure answers are grounded in the provided documents, making them more accurate than general knowledge responses. 