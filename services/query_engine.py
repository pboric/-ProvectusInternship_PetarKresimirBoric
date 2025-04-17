class QueryEngine:
    """
    Engine for answering questions based on RAG.
    """
    
    def __init__(self, rag_engine, llm=None, tokenizer=None):
        """
        Initialize the query engine.
        
        Args:
            rag_engine: RAG engine for retrieving relevant document chunks
            llm: Language model for generating answers
            tokenizer: Tokenizer for the language model
        """
        self.rag_engine = rag_engine
        self.llm = llm
        self.tokenizer = tokenizer
    
    def _format_context(self, chunks):
        """
        Format retrieved chunks into context for the language model.
        
        Args:
            chunks (list): List of retrieved chunks
            
        Returns:
            str: Formatted context
        """
        if not chunks:
            return "No relevant information found."
        
        formatted_chunks = []
        for i, chunk in enumerate(chunks):
            formatted_chunk = f"[DOCUMENT {i+1}]\n{chunk['text']}"
            formatted_chunks.append(formatted_chunk)
        
        return "\n\n".join(formatted_chunks)
    
    def answer_question(self, question, search_results_count=3):
        """
        Answer a question based on retrieved documents.
        
        Args:
            question (str): Question to answer
            search_results_count (int): Number of chunks to retrieve
            
        Returns:
            str: Answer to the question
        """
        # Retrieve relevant chunks
        chunks = self.rag_engine.search(question, top_k=search_results_count)
        
        # If no chunks found, return a message
        if not chunks:
            return "I don't have any information about that in my database. Please add relevant concert tour documents first."
        
        # Format context
        context = self._format_context(chunks)
        
        # If LLM is not available, return context
        if self.llm is None or self.tokenizer is None:
            return f"Based on the available information:\n\n{context}\n\nI cannot generate a more specific answer without a language model."
        
        try:
            # Prompt for the LLM to answer the question
            prompt = f"""
            You are a helpful AI assistant that answers questions about concert tours scheduled for 2025-2026.
            
            Below are relevant excerpts from documents about concert tours that have been uploaded to your database:
            
            {context}
            
            Based ONLY on the information provided above, answer the following question. 
            If the information needed to answer the question is not available in the provided 
            context, say "I don't have that information in my database."
            
            IMPORTANT: When matching artist names, band names, or city names, be case-insensitive. 
            For example, if the user asks about "lady gaga" but the document mentions "Lady Gaga", 
            or if they ask about "new york" but the document mentions "New York", treat them as the same.
            
            Question: {question}
            
            Answer:
            """
            
            # Generate answer using LLM
            output = self.llm(prompt, max_tokens=1024, temperature=0.2, stop=["Question:", "\n\n"])
            answer = output['choices'][0]['text'].strip()
            
            return answer
        except Exception as e:
            # Fallback to returning context on error
            return f"I found some information, but couldn't generate a complete answer. Here's what I found:\n\n{context}" 