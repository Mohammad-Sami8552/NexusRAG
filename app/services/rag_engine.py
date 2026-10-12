from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from app.core.config import settings

class RAGService:
    def __init__(self):
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model="models/gemini-embedding-001",
            google_api_key=settings.GOOGLE_API_KEY
        )
        
        self.vector_store = Chroma(
            persist_directory=settings.CHROMA_PERSIST_DIR, 
            embedding_function=self.embeddings
        )
        
        # Initialize the Gemini LLM for text generation
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-3.5-flash", # Use exactly this string
            google_api_key=settings.GOOGLE_API_KEY
        )   
        
    def process_document(self, file_path: str):
        loader = PyPDFLoader(file_path)
        documents = loader.load()
        
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, 
            chunk_overlap=200
        )
        chunks = text_splitter.split_documents(documents)
        
        self.vector_store.add_documents(chunks)
        return len(chunks)

    def query(self, question: str) -> dict:
        docs = self.vector_store.similarity_search(question, k=3)
        context = "\n\n".join([doc.page_content for doc in docs])
        
        prompt = f"""
        Answer the question using ONLY the provided context. 
        Respond directly with the answer. Do NOT start your response with phrases like "Based on the provided context", "According to the document", or "The context states".
        
        Context: {context}
        Question: {question}
        """
        
        # Use the LangChain LLM instead of requests.post
        try:
            response = self.llm.invoke(prompt)
            if isinstance(response.content,list):
                answer = response.content[0].get("text", str(response.content))
            else:
                answer = response.content
        except Exception as e:
            answer = f"LLM Generation Error: {str(e)}"
        
        return {
            "answer": answer,
            "sources": [doc.metadata for doc in docs]
        }

rag_service = RAGService()