import os
import json
import faiss
import numpy as np
from pathlib import Path
import re

class RAGEngine:
    """
    Retrieval Augmented Generation engine for concert tour information.
    """
    
    def __init__(self, embedding_model, document_processor, chunk_size=512, overlap=100):
        """
        Initialize the RAG engine.
        
        Args:
            embedding_model: Model for creating text embeddings
            document_processor: Processor for handling documents
            chunk_size (int): Size of document chunks for indexing
            overlap (int): Overlap between chunks
        """
        self.embedding_model = embedding_model
        self.document_processor = document_processor
        self.chunk_size = chunk_size
        self.overlap = overlap
        
        # Set up vector storage
        self.index_dir = self.document_processor.storage_dir / "vector_index"
        self.index_dir.mkdir(exist_ok=True)
        
        self.chunk_dir = self.document_processor.storage_dir / "chunks"
        self.chunk_dir.mkdir(exist_ok=True)
        
        # Initialize FAISS index
        self.embedding_size = self.embedding_model.get_embedding_size()
        self.index = faiss.IndexFlatL2(self.embedding_size)
        
        # Load existing index if available
        self.chunk_info = {}
        self._load_index()
    
    def _load_index(self):
        """Load existing index and chunk information if available."""
        index_path = self.index_dir / "vector.index"
        chunk_info_path = self.index_dir / "chunk_info.json"
        
        if index_path.exists() and chunk_info_path.exists():
            try:
                # Load index
                self.index = faiss.read_index(str(index_path))
                
                # Load chunk info
                with open(chunk_info_path, "r", encoding="utf-8") as f:
                    self.chunk_info = json.load(f)
            except Exception as e:
                # If error loading, initialize new index
                self.index = faiss.IndexFlatL2(self.embedding_size)
                self.chunk_info = {}
    
    def _save_index(self):
        """Save the current index and chunk information."""
        try:
            # Save index
            faiss.write_index(self.index, str(self.index_dir / "vector.index"))
            
            # Save chunk info
            with open(self.index_dir / "chunk_info.json", "w", encoding="utf-8") as f:
                json.dump(self.chunk_info, f, indent=2)
            
            return True
        except Exception as e:
            return False
    
    def _chunk_document(self, text, doc_id):
        """
        Split document into overlapping chunks.
        
        Args:
            text (str): Document text
            doc_id (str): Document ID
            
        Returns:
            list: List of chunk texts
        """
        # Split by paragraphs first
        paragraphs = re.split(r'\n\s*\n', text)
        chunks = []
        
        # Special handling for paragraph-based chunking
        current_chunk = ""
        for para in paragraphs:
            para = para.strip()
            if not para:
                continue
                
            # If adding this paragraph would exceed chunk size, finalize current chunk
            if len(current_chunk) + len(para) > self.chunk_size and current_chunk:
                chunks.append(current_chunk)
                
                # Start new chunk with overlap
                words = current_chunk.split()
                overlap_text = " ".join(words[-self.overlap:]) if len(words) > self.overlap else ""
                current_chunk = overlap_text + " " + para
            else:
                # Add paragraph to current chunk with space
                if current_chunk:
                    current_chunk += " " + para
                else:
                    current_chunk = para
        
        # Add the final chunk if not empty
        if current_chunk:
            chunks.append(current_chunk)
        
        # Save chunks to files
        for i, chunk in enumerate(chunks):
            chunk_id = f"{doc_id}_{i}"
            with open(self.chunk_dir / f"{chunk_id}.txt", "w", encoding="utf-8") as f:
                f.write(chunk)
            
            # Store chunk info
            self.chunk_info[chunk_id] = {
                "doc_id": doc_id,
                "chunk_index": i,
                "length": len(chunk)
            }
        
        return chunks
    
    def add_document(self, text):
        """
        Process and add a document to the RAG system.
        
        Args:
            text (str): Document text
            
        Returns:
            tuple: (success, message)
        """
        # Process the document
        success, message = self.document_processor.process_document(text)
        
        if not success:
            return success, message
        
        # If document was processed successfully, add to RAG
        doc_id = self.document_processor.generate_document_id(text)
        
        try:
            # Chunk the document
            chunks = self._chunk_document(text, doc_id)
            
            # Get embeddings for all chunks
            embeddings = self.embedding_model.get_embeddings(chunks)
            
            # Add embeddings to index
            if len(embeddings) > 0:
                self.index.add(np.array(embeddings).astype('float32'))
                
                # Save the updated index
                self._save_index()
            
            return True, message
        except Exception as e:
            return False, f"Error adding document to RAG system: {str(e)}"
    
    def search(self, query, top_k=5):
        """
        Search for relevant document chunks.
        
        Args:
            query (str): Search query
            top_k (int): Number of results to return
            
        Returns:
            list: List of relevant chunks
        """
        # Normalize query for better matching
        # Convert to lowercase for case-insensitive matching
        normalized_query = query.lower()
        
        # Get query embedding
        query_embedding = self.embedding_model.get_embeddings([normalized_query])[0].reshape(1, -1).astype('float32')
        
        # Search the index
        if self.index.ntotal == 0:
            return []
            
        # Limit top_k to the number of documents
        top_k = min(top_k, self.index.ntotal)
        
        distances, indices = self.index.search(query_embedding, top_k)
        
        # Get chunk IDs for the results
        chunk_ids = [list(self.chunk_info.keys())[idx] for idx in indices[0]]
        
        # Load the chunks
        results = []
        for chunk_id in chunk_ids:
            chunk_path = self.chunk_dir / f"{chunk_id}.txt"
            if chunk_path.exists():
                with open(chunk_path, "r", encoding="utf-8") as f:
                    chunk_text = f.read()
                
                # Get doc_id from chunk_id
                doc_id = self.chunk_info[chunk_id]["doc_id"]
                
                results.append({
                    "doc_id": doc_id,
                    "chunk_id": chunk_id,
                    "text": chunk_text
                })
        
        return results 