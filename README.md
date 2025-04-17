# Concert Tour Information System

A powerful system for ingesting, processing, and querying concert tour information using advanced AI techniques.

## Features

- **Document Ingestion**: Upload and process concert tour documents
- **Question Answering**: Ask questions about concert tours and get accurate answers
- **Web Search**: Search the web for additional concert tour information
- **RAG Implementation**: Retrieval-Augmented Generation for accurate and up-to-date responses

## Approach and Design Choices

### Architecture

The system is built with a modular architecture that separates concerns and allows for easy extension:

1. **Frontend**: Streamlit-based UI for user interaction
2. **Backend Services**:
   - Document Processor: Handles document ingestion and validation
   - RAG Engine: Implements Retrieval-Augmented Generation
   - Query Engine: Processes user questions and generates responses
   - Web Search: Provides additional context from the web

### Key Design Decisions

1. **LLaMA Model**: We chose LLaMA for its excellent performance on text generation tasks while being lightweight enough to run on consumer hardware.

2. **FAISS Vector Database**: For efficient similarity search and retrieval of relevant document chunks.

3. **Sentence Transformers**: For creating high-quality embeddings of text chunks.

4. **RAG Implementation**: Combines retrieval of relevant information with generative AI to provide accurate, context-aware responses.

5. **Modular Design**: Each component is designed to be independent, making it easy to replace or upgrade individual parts.

## Prerequisites

- Python 3.8 or higher
- CUDA-capable GPU (recommended for better performance)
- 8GB+ RAM
- 5GB+ free disk space

## Installation

### Windows Users (Recommended Setup)

For Windows users, we recommend using WSL (Windows Subsystem for Linux) and Conda to avoid compatibility issues with some packages:

1. **Install WSL**:
   - Open PowerShell as Administrator and run: `wsl --install`
   - Restart your computer
   - Complete the WSL setup

2. **Install Conda**:
   - Download and install [Miniconda](https://docs.conda.io/en/latest/miniconda.html)
   - Open WSL terminal and create a new environment:
     ```
     conda create -n concert_bot python=3.10
     conda activate concert_bot
     ```

3. **Clone the Repository**:
   ```
   git clone https://github.com/yourusername/concert_bot.git
   cd concert_bot
   ```

4. **Run the Setup Script**:
   ```
   python setup.py
   ```
   This will:
   - Check your Python version
   - Verify CUDA availability
   - Create necessary directories
   - Generate a `.env` file template

5. **Install Dependencies**:
   ```
   pip install -r requirements.txt
   ```

6. **Download the LLaMA Model**:
   ```
   python download_model.py
   ```

7. **Configure Environment Variables**:
   - Copy `.env.example` to `.env`
   - Update the paths and API keys in `.env`

### Linux/Mac Users

1. **Clone the Repository**:
   ```
   git clone https://github.com/yourusername/concert_bot.git
   cd concert_bot
   ```

2. **Create a Virtual Environment**:
   ```
   python -m venv venv
   source venv/bin/activate  # On Linux/Mac
   ```

3. **Run the Setup Script**:
   ```
   python setup.py
   ```

4. **Install Dependencies**:
   ```
   pip install -r requirements.txt
   ```

5. **Download the LLaMA Model**:
   ```
   python download_model.py
   ```

6. **Configure Environment Variables**:
   - Copy `.env.example` to `.env`
   - Update the paths and API keys in `.env`

## Running the Service

1. **Test the System**:
   ```
   python test_system.py
   ```
   This will verify that all components are working correctly.

2. **Start the Application**:
   ```
   streamlit run app.py
   ```

3. **Access the Web Interface**:
   - Open your browser and navigate to `http://localhost:8501`

## Usage

1. **Upload Documents**:
   - Click on the "Upload Documents" tab
   - Select one or more concert tour documents (PDF, TXT, DOCX)
   - Click "Upload" to process the documents

2. **Ask Questions**:
   - Click on the "Ask Questions" tab
   - Type your question about concert tours
   - Click "Ask" to get an answer

3. **Web Search**:
   - Click on the "Web Search" tab
   - Enter your search query
   - Click "Search" to get results from the web

## Troubleshooting

### Common Issues

1. **CUDA Not Available**:
   - Ensure you have the latest NVIDIA drivers installed
   - Verify that CUDA is properly installed
   - Check that PyTorch is installed with CUDA support

2. **Model Loading Errors**:
   - Verify that the model path in `.env` is correct
   - Ensure the model file exists at the specified path
   - Check that you have enough RAM to load the model

3. **Package Installation Issues**:
   - Try installing packages one by one to identify problematic dependencies
   - For Windows users, consider using WSL as described above
   - Check the [FAQ](docs/FAQ.md) for specific package installation guidance

### Getting Help

If you encounter issues not covered here:

1. Check the [FAQ](docs/FAQ.md) for common problems and solutions
2. Open an issue on the GitHub repository
3. Contact the maintainers for support

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- LLaMA model from Meta AI
- LangChain framework
- FAISS library from Facebook Research
- Sentence Transformers by UKP Lab
