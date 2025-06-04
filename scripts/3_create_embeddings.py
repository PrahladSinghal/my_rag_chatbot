# scripts/3_create_embeddings.py

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.schema import Document
import os

CHUNK_FILE = "../data/processed_chunks.txt"
INDEX_DIR = "../embeddings"
EMBED_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

def main():
    os.makedirs(INDEX_DIR, exist_ok=True)

    # Load processed chunks
    with open(CHUNK_FILE, "r", encoding="utf-8") as f:
        chunks = [chunk.strip() for chunk in f.read().split("\n\n") if chunk.strip()]

    print(f"[📄] Loaded {len(chunks)} chunks from {CHUNK_FILE}")
    docs = [Document(page_content=chunk) for chunk in chunks]

    # Load embedding model
    embedding_model = HuggingFaceEmbeddings(model_name=EMBED_MODEL_NAME)
    print(f"[📐] Sample embedding vector shape: {len(embedding_model.embed_query('test'))}")

    # Create FAISS vectorstore and save
    vectorstore = FAISS.from_documents(docs, embedding_model)
    vectorstore.save_local(INDEX_DIR)

    print(f"[✅] Embeddings created for {len(docs)} chunks.")
    print(f"[📦] FAISS vectorstore saved to: {INDEX_DIR}")

if __name__ == "__main__":
    main()
