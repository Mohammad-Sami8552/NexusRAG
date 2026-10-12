# NexusRAG: Enterprise Document Intelligence System

NexusRAG is a modular, full-stack Retrieval-Augmented Generation (RAG) application. It allows users to upload multiple PDF documents and ask questions about their content in real-time. The system ensures that all AI responses are strictly grounded in the provided context, effectively eliminating hallucinations, and provides exact source citations.

## Features
- **Batch PDF Processing:** Upload and process multiple documents simultaneously.
- **Semantic Search:** Uses Google's Gemini embeddings and ChromaDB for high-speed, persistent vector retrieval.
- **Grounded Generation:** Leverages Gemini 3.5 Flash to synthesize answers strictly from retrieved context.
- **Source Tracking:** Exposes exact pages and metadata for every claim made by the AI.
- **Interactive UI:** Clean, intuitive Streamlit interface built on top of a highly modular FastAPI backend.

## Tech Stack
- **Backend API:** FastAPI, Uvicorn, Python
- **AI & Orchestration:** LangChain, Google Generative AI (`gemini-3.5-flash`, `gemini-embedding-001`)
- **Vector Database:** ChromaDB
- **Frontend:** Streamlit

## Project Structure
```text
nexus-rag/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── core/
│   │   └── config.py           # Environment variables and settings
│   ├── api/
│   │   └── endpoints.py        # API routing (upload, query)
│   └── services/
│       └── rag_engine.py       # LangChain and ChromaDB business logic
├── data/                       # Local storage for uploaded PDFs
├── chroma_data/                # Persistent vector store
├── frontend.py                 # Streamlit chat interface
├── requirements.txt            # Project dependencies
└── .env                        # API keys (Not committed to version control)
```

## Setup & Installation

**1. Clone the repository and set up a virtual environment**
```bash
git clone [https://github.com/Mohammad-Sami8552/nexus-rag.git](https://github.com/Mohammad-Sami8552/nexus-rag.git)
cd nexus-rag
python -m venv .nexus-rag

# On Windows:
.nexus-rag\Scripts\activate

# On Mac/Linux:
source .nexus-rag/bin/activate
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Configure Environment Variables**
Create a `.env` file in the root directory and add your Google Gemini API key:
```env
GOOGLE_API_KEY="your_google_api_key_here"
```

## Running the Application

You will need two terminal windows to run both the backend API and the frontend UI.

**Terminal 1: Start the FastAPI Backend**
```bash
# Ensure your virtual environment is activated
uvicorn app.main:app --reload
```
*The API will be available at `http://127.0.0.1:8000` (Swagger UI at `/docs`).*

**Terminal 2: Start the Streamlit Frontend**
```bash
# Ensure your virtual environment is activated
streamlit run frontend.py
```
*The chat interface will automatically open in your browser at `http://localhost:8501`.*

## Usage
1. Open the Streamlit UI in your browser.
2. Use the sidebar to upload one or more PDF documents.
3. Click **"Process Documents"** to chunk the text and generate vector embeddings.
4. Type a question in the chat input. The system will retrieve relevant text and generate an accurate, context-aware response along with citations.
