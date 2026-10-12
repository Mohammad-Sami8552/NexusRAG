import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/api/v1"

st.set_page_config(page_title="NexusRAG", page_icon="📄")
st.title("📄 NexusRAG: Document Intelligence")
st.markdown("Upload a PDF and ask questions based on its context.")

# Sidebar for file upload
# Sidebar for file upload
with st.sidebar:
    st.header("Document Upload")
    # Enable multiple files
    uploaded_files = st.file_uploader("Choose PDF files", type="pdf", accept_multiple_files=True)
    
    if uploaded_files and st.button("Process Documents"):
        with st.spinner("Chunking and generating embeddings..."):
            # Format the payload for multiple files under the key "files"
            files_payload = [
                ("files", (file.name, file.getvalue(), "application/pdf")) 
                for file in uploaded_files
            ]
            
            response = requests.post(f"{API_URL}/upload", files=files_payload)
            
            if response.status_code == 200:
                st.success(response.json().get("message", "Success!"))
            else:
                st.error("Failed to process documents.")
# Main chat interface
question = st.chat_input("Ask a question about the uploaded document...")

if question:
    # Display user question
    with st.chat_message("user"):
        st.write(question)
        
    # Fetch and display AI response
    with st.chat_message("assistant"):
        with st.spinner("Searching documents..."):
            response = requests.post(f"{API_URL}/query", json={"question": question})
            
            if response.status_code == 200:
                data = response.json()
                st.write(data.get("answer", "No answer generated."))
                
                # Expandable section to prove it's actually RAG (great for portfolios)
                with st.expander("View Retrieved Sources"):
                    for idx, source in enumerate(data.get("sources", [])):
                        st.caption(f"**Source {idx + 1}:** Page {source.get('page', 'Unknown')}")
            else:
                st.error("Failed to connect to the backend API.")