import os
from sentence_transformers import SentenceTransformer
import torch
import numpy as np

class EmbeddingModel:
    """
    Class for creating text embeddings using a pre-trained model.
    """
    
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        """
        Initialize the embedding model.
        
        Args:
            model_name (str): Name of the sentence transformer model to use
        """
        # Use GPU if available
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        
        # Load the model
        try:
            self.model = SentenceTransformer(model_name, device=self.device)
            self.embedding_size = self.model.get_sentence_embedding_dimension()
        except Exception as e:
            raise Exception(f"Error loading embedding model: {str(e)}")
    
    def get_embeddings(self, texts):
        """
        Get embeddings for a list of texts.
        
        Args:
            texts (list): List of text strings to embed
            
        Returns:
            numpy.ndarray: Array of embeddings
        """
        if not texts:
            return np.array([])
            
        # Convert to list if single text is provided
        if isinstance(texts, str):
            texts = [texts]
            
        try:
            embeddings = self.model.encode(texts)
            return embeddings
        except Exception as e:
            raise Exception(f"Error generating embeddings: {str(e)}")
    
    def get_embedding_size(self):
        """
        Get the size of the embeddings.
        
        Returns:
            int: Size of the embedding vectors
        """
        return self.embedding_size 