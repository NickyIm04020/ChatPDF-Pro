import os
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

PINECONE_KEY = os.getenv("PINECONE_API_KEY")
INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")

def ingest_docs(directory_path: str):
    """
    Ingests PDFs from a directory, chunks them, and upserts to Pinecone.
    """
    print(f"Loading PDFs from {directory_path}...")
    loader = DirectoryLoader(directory_path, glob="*.pdf", loader_cls=PyPDFLoader)
    documents = loader.load()
    print(f"Loaded {len(documents)} documents.")

    # Optimized Chunking for Context Retention (Resume Point)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, 
        chunk_overlap=200,
        add_start_index=True
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Created {len(chunks)} text chunks.")

    # Embedding & Vector Store
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    pc = Pinecone(api_key=PINECONE_KEY)
    
    # Check if index exists, create if not
    existing_indexes = [i['name'] for i in pc.list_indexes()]
    if INDEX_NAME not in existing_indexes:
        print(f"Creating index: {INDEX_NAME}")
        pc.create_index(
            name=INDEX_NAME,
            dimension=1536,
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1")
        )
    
    print("Upserting vectors to Pinecone...")
    PineconeVectorStore.from_documents(
        documents=chunks,
        embedding=embeddings,
        index_name=INDEX_NAME
    )
    print("Ingestion Complete!")

if __name__ == "__main__":
    # For manual testing
    ingest_docs("documents")