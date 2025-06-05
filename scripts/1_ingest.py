from langchain.document_loaders import PyPDFLoader  # or any loader you're using
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# Load document
loader = PyPDFLoader("../data/sample.pdf")  # Update path and loader type if needed
docs = loader.load()
print("Loaded document:", docs[0].metadata['source'])

#  Split into chunks
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = splitter.split_documents(docs)

# Create embeddings
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vectordb = FAISS.from_documents(chunks, embedding_model)

# Save vectorstore
vectordb.save_local("../embeddings")
print("Ingestion complete. Embeddings saved to ../embeddings")
