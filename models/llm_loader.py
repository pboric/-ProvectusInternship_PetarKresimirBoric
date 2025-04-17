import os
from llama_cpp import Llama
from dotenv import load_dotenv

def load_llama_model():
    """
    Load the LLaMA model for text generation.
    
    Returns:
        tuple: (llm, tokenizer) where llm is the model and tokenizer is the tokenizer
    """
    load_dotenv()
    
    # Get model path from environment variable or use default
    model_path = os.getenv("LLM_MODEL_PATH", "models/llama-2-7b-chat.Q4_K_M.gguf")
    
    # Check if model exists
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found at {model_path}. Please download a compatible GGUF model.")
    
    # Load the model
    try:
        llm = Llama(
            model_path=model_path,
            n_ctx=4096,  # Context window size
            n_gpu_layers=-1,  # Use all GPU layers if available
            verbose=False
        )
        
        # In llama-cpp-python, the model itself handles tokenization
        tokenizer = llm
        
        return llm, tokenizer
    except Exception as e:
        raise Exception(f"Error loading LLaMA model: {str(e)}") 