import os
import json
import hashlib
import time
from pathlib import Path
import re

class DocumentProcessor:
    """
    Class for processing and storing documents in the concert tour domain.
    """
    
    def __init__(self, storage_dir="data/document_store", llm=None, tokenizer=None):
        """
        Initialize the document processor.
        
        Args:
            storage_dir (str): Directory to store processed documents
            llm: Language model for text generation
            tokenizer: Tokenizer for the language model
        """
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.llm = llm
        self.tokenizer = tokenizer
        
        # Create subdirectories
        self.docs_dir = self.storage_dir / "documents"
        self.docs_dir.mkdir(exist_ok=True)
        
        self.summaries_dir = self.storage_dir / "summaries"
        self.summaries_dir.mkdir(exist_ok=True)
        
        # Keywords related to concert tours
        self.concert_keywords = [
            'concert', 'tour', 'performance', 'venue', 'stage', 'music', 'band', 
            'artist', 'musician', 'singer', 'performer', 'ticket', 'show', 'event',
            'festival', 'gig', 'audience', 'fan', 'live', 'tour date', 'world tour'
        ]
    
    def is_concert_related(self, text):
        """
        Check if a document is related to concert tours.
        
        Args:
            text (str): Document text
            
        Returns:
            bool: True if document is concert-related
        """
        text_lower = text.lower()
        
        # Count how many concert-related keywords appear in the text
        keyword_count = sum(1 for keyword in self.concert_keywords if keyword.lower() in text_lower)
        
        # Check for years 2025-2026
        year_pattern = re.compile(r'(202[5-6])')
        has_relevant_years = bool(year_pattern.search(text_lower))
        
        # Check for non-concert related keywords that might indicate a different topic
        non_concert_keywords = [
            'biodiversity', 'conservation', 'species', 'ecosystem', 'research', 'study',
            'climate', 'environment', 'forest', 'wildlife', 'endangered', 'habitat',
            'scientific', 'data', 'analysis', 'report', 'findings', 'survey'
        ]
        
        non_concert_count = sum(1 for keyword in non_concert_keywords if keyword.lower() in text_lower)
        
        # Document is considered concert-related if:
        # 1. It has sufficient concert keywords (at least 3)
        # 2. It has relevant years (2025-2026)
        # 3. It doesn't have too many non-concert keywords (less than 5)
        return keyword_count >= 3 and has_relevant_years and non_concert_count < 5
    
    def generate_document_id(self, text):
        """
        Generate a unique ID for a document.
        
        Args:
            text (str): Document text
            
        Returns:
            str: Unique document ID
        """
        # Create a hash of the text content
        return hashlib.md5(text.encode('utf-8')).hexdigest()
    
    def generate_summary(self, text):
        """
        Generate a summary of a document using the LLM.
        
        Args:
            text (str): Document text
            
        Returns:
            str: Summary of the document
        """
        # First check if the document is concert-related
        if not self.is_concert_related(text):
            return "This document does not appear to be related to concert tours for 2025-2026. It will not be processed."
            
        if self.llm is None or self.tokenizer is None:
            # Simplified summary when LLM is not available
            words = text.split()
            return ' '.join(words[:100]) + "..." if len(words) > 100 else text
        
        try:
            # Prompt for the LLM to summarize concert tour information
            prompt = f"""
            Below is a document about concert tours for 2025-2026. Please summarize the key information, including:
            - Artists or bands mentioned
            - Dates and venues of performances
            - Special guests or features
            - Any notable logistics or arrangements
            
            Document:
            {text}
            
            Summary:
            """
            
            # Generate summary using LLM
            output = self.llm(prompt, max_tokens=1024, temperature=0.1, stop=["Document:", "\n\n"])
            summary = output['choices'][0]['text'].strip()
            
            return summary
        except Exception as e:
            # Fallback to simple truncation on error
            words = text.split()
            return ' '.join(words[:100]) + "..." if len(words) > 100 else text
    
    def store_document(self, doc_id, text, summary):
        """
        Store a document and its summary.
        
        Args:
            doc_id (str): Document ID
            text (str): Document text
            summary (str): Document summary
            
        Returns:
            bool: Success status
        """
        try:
            # Store original document
            with open(self.docs_dir / f"{doc_id}.txt", "w", encoding="utf-8") as f:
                f.write(text)
            
            # Store summary and metadata
            metadata = {
                "id": doc_id,
                "timestamp": time.time(),
                "summary": summary,
                "length": len(text)
            }
            
            with open(self.summaries_dir / f"{doc_id}.json", "w", encoding="utf-8") as f:
                json.dump(metadata, f, indent=2)
                
            return True
        except Exception as e:
            return False
    
    def process_document(self, text):
        """
        Process a new document.
        
        Args:
            text (str): Document text
            
        Returns:
            tuple: (success, message)
                success (bool): Whether the processing was successful
                message (str): Summary of the document or error message
        """
        # Check if document is concert-related
        if not self.is_concert_related(text):
            return False, "Sorry, I cannot ingest documents with other themes. This document does not appear to be related to concert tours for 2025-2026. Please provide content specifically about concert tours, including artist names, venues, and dates for 2025-2026."
        
        # Generate document ID
        doc_id = self.generate_document_id(text)
        
        # Check if document already exists
        if (self.docs_dir / f"{doc_id}.txt").exists():
            return False, "This document has already been ingested."
        
        # Generate summary
        summary = self.generate_summary(text)
        
        # Store document and summary
        if self.store_document(doc_id, text, summary):
            return True, summary
        else:
            return False, "Error storing the document."
    
    def get_document(self, doc_id):
        """
        Retrieve a document by ID.
        
        Args:
            doc_id (str): Document ID
            
        Returns:
            str: Document text or None if not found
        """
        doc_path = self.docs_dir / f"{doc_id}.txt"
        if doc_path.exists():
            with open(doc_path, "r", encoding="utf-8") as f:
                return f.read()
        return None
    
    def get_all_documents(self):
        """
        Get all document IDs.
        
        Returns:
            list: List of document IDs
        """
        return [f.stem for f in self.docs_dir.glob("*.txt")] 