import streamlit as st
import os
from pathlib import Path
import time
import re

# Import our modules
from models.llm_loader import load_llama_model
from models.embedding_model import EmbeddingModel
from services.document_processor import DocumentProcessor
from services.rag_engine import RAGEngine
from services.query_engine import QueryEngine
from utils.web_search import WebSearchEngine

# Page configuration
st.set_page_config(
    page_title="Concert Tour Information System",
    page_icon="🎵",
    layout="wide"
)

# Initialize session state
if "initialized" not in st.session_state:
    st.session_state.initialized = False
    st.session_state.loading = False
    st.session_state.llm = None
    st.session_state.tokenizer = None

def initialize_system():
    """Initialize the system components"""
    st.session_state.loading = True
    
    with st.spinner("Loading models and initializing system... This may take a minute."):
        try:
            # Create data directory
            data_dir = Path("data/document_store")
            data_dir.mkdir(parents=True, exist_ok=True)
            
            # Load models
            llm, tokenizer = None, None
            try:
                llm, tokenizer = load_llama_model()
                st.session_state.llm = llm
                st.session_state.tokenizer = tokenizer
            except Exception as e:
                st.warning(f"Couldn't load LLM model. Running in reduced functionality mode. Error: {e}")
            
            # Initialize embedding model
            embedding_model = EmbeddingModel()
            
            # Initialize document processor
            document_processor = DocumentProcessor(
                storage_dir="data/document_store",
                llm=llm,
                tokenizer=tokenizer
            )
            
            # Initialize RAG engine
            rag_engine = RAGEngine(
                embedding_model=embedding_model,
                document_processor=document_processor
            )
            
            # Initialize query engine
            query_engine = QueryEngine(
                rag_engine=rag_engine,
                llm=llm,
                tokenizer=tokenizer
            )
            
            # Initialize web search engine (bonus functionality)
            web_search_engine = WebSearchEngine()
            
            # Store in session state
            st.session_state.embedding_model = embedding_model
            st.session_state.document_processor = document_processor
            st.session_state.rag_engine = rag_engine
            st.session_state.query_engine = query_engine
            st.session_state.web_search_engine = web_search_engine
            st.session_state.initialized = True
            
        except Exception as e:
            st.error(f"Error initializing system: {e}")
        
        st.session_state.loading = False

# Title
st.title("🎵 Concert Tour Information System")
st.write("A system to manage and query information about upcoming concert tours (2025-2026)")

# Initialize button
if not st.session_state.initialized and not st.session_state.loading:
    if st.button("Initialize System"):
        initialize_system()

# Show loading message if needed
if st.session_state.loading:
    st.info("Loading models and initializing system... This may take a minute.")
    
# Main interface (only show when initialized)
if st.session_state.initialized:
    # Tabs for different functionality
    tab1, tab2, tab3 = st.tabs(["Add Document", "Ask Questions", "Web Search"])
    
    # Tab 1: Document ingestion
    with tab1:
        st.header("Add Concert Tour Document")
        st.write("Paste a document about concert tours to add it to the database.")
        
        document_text = st.text_area(
            "Document Text", 
            height=300,
            placeholder="Paste your concert tour document here..."
        )
        
        if st.button("Process Document"):
            if document_text:
                with st.spinner("Processing document..."):
                    success, message = st.session_state.rag_engine.add_document(document_text)
                    
                    if success:
                        st.success("Document added successfully!")
                        st.subheader("Document Summary")
                        st.write(message)
                    else:
                        st.error(message)
            else:
                st.warning("Please paste a document first.")
    
    # Tab 2: Question answering
    with tab2:
        st.header("Ask Questions About Concert Tours")
        st.write("Ask questions about the concert tour documents you've added.")
        
        question = st.text_input(
            "Your Question",
            placeholder="e.g., Where is Lady Gaga performing in autumn 2025?"
        )
        
        if st.button("Get Answer"):
            if question:
                with st.spinner("Searching for answer..."):
                    answer = st.session_state.query_engine.answer_question(question)
                    
                    st.subheader("Answer")
                    st.write(answer)
            else:
                st.warning("Please enter a question first.")
    
    # Tab 3: Web Search (Bonus functionality)
    with tab3:
        st.header("Web Search for Concert Information")
        st.write("Search online for information about an artist's upcoming concerts (2025-2026)")
        
        # Check if web search is enabled
        if not st.session_state.web_search_engine.is_enabled():
            st.warning("Web search is not enabled. Please add a SERPAPI_KEY to your .env file.")
        
        artist_name = st.text_input(
            "Artist/Band Name",
            placeholder="e.g., Taylor Swift, BTS, Ed Sheeran"
        )
        
        if st.button("Search Online"):
            if artist_name:
                with st.spinner(f"Searching for concert information about {artist_name}..."):
                    success, message = st.session_state.web_search_engine.search_concert_info(artist_name)
                    
                    if success:
                        st.subheader(f"Concert Information for {artist_name}")
                        st.write(message)
                    else:
                        st.error(message)
                        st.info("If you're seeing a status code 520 error, this is a temporary issue with the search service. Please try again in a few minutes.")
            else:
                st.warning("Please enter an artist or band name first.")

# Show message if not initialized
if not st.session_state.initialized and not st.session_state.loading:
    st.info("Please initialize the system to start using it.")

# Create empty .env file if it doesn't exist
if not Path(".env").exists():
    with open(".env", "w") as f:
        f.write("# Add your API keys here\n")
        f.write("# LLM_MODEL_PATH=models/llama-2-7b-chat.Q4_K_M.gguf\n")
        f.write("# SERPAPI_KEY=your_serpapi_key_here\n")