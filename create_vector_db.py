# File: create_vector_db.py

import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
import time # Import the time library for potential delays

# Load environment variables (needs GOOGLE_API_KEY)
load_dotenv()

# Define the paths for the source documents and the persistent database
PDF_DIRECTORY = "documents"
PERSIST_DIRECTORY = "db"

def main():
    """
    Main function to perform the ETL process with batching:
    1. Extract text from PDFs.
    2. Chunk the text.
    3. Create embeddings and store them in ChromaDB in batches.
    """
    if not os.path.exists(PDF_DIRECTORY):
        os.makedirs(PDF_DIRECTORY)
        print(f"Created '{PDF_DIRECTORY}' directory. Please add your PDF files there and run this script again.")
        return
    
    # 1. Extract (Load Documents)
    print(f"Loading documents from {PDF_DIRECTORY}...")
    loader = PyPDFDirectoryLoader(PDF_DIRECTORY)
    documents = loader.load()
    if not documents:
        print("No documents found. Please add PDFs to the 'documents' directory.")
        return
    print(f"Loaded {len(documents)} document(s).")

    # 2. Chunk (Transform Documents)
    print("Chunking documents...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = text_splitter.split_documents(documents)
    print(f"Created {len(chunks)} text chunks.")

    # 3. Store (Load into Vector DB in Batches)
    print("Creating embeddings and storing in ChromaDB...")
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    
    # --- NEW: BATCHING LOGIC ---
    batch_size = 100 # Process 100 chunks at a time. You can adjust this number.
    
    # Create the database with the first batch
    print(f"Processing batch 1 of {len(chunks) // batch_size + 1}...")
    db = Chroma.from_documents(
        chunks[:batch_size], 
        embeddings, 
        persist_directory=PERSIST_DIRECTORY
    )
    
    # Process the rest of the chunks in subsequent batches
    for i in range(batch_size, len(chunks), batch_size):
        print(f"Processing batch {i // batch_size + 1} of {len(chunks) // batch_size + 1}...")
        # Add the next batch of documents to the existing database
        db.add_documents(chunks[i:i + batch_size])
        # Optional: add a small delay to avoid overwhelming the API
        time.sleep(1) 
    # --- END OF BATCHING LOGIC ---
    
    # Persist the database after all batches are added
    db.persist()
    print(f"✅ Successfully created and saved the vector database in '{PERSIST_DIRECTORY}'.")

if __name__ == "__main__":

    main()
