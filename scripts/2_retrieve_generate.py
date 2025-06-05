from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.prompts import PromptTemplate
from transformers import pipeline
from langchain_community.llms import HuggingFacePipeline

# Load embedding model (384 dim matching your index)
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Load FAISS vector store from correct relative path
vectordb = FAISS.load_local("../embeddings", embeddings=embedding_model, allow_dangerous_deserialization=True)

# Create retriever with k=3
retriever = vectordb.as_retriever(search_kwargs={"k": 3})

# Load Hugging Face pipeline for text generation with sufficient max_new_tokens
hf_pipeline = pipeline(
    "text2text-generation",
    model="google/flan-t5-small",
    tokenizer="google/flan-t5-small",
    max_new_tokens=512,
)

llm = HuggingFacePipeline(pipeline=hf_pipeline)

print("Chatbot is ready! Ask your questions. (type 'exit' to quit)")
while True:
    query = input("\nYou: ")
    if query.lower() in ["exit", "quit"]:
        break

    try:
        # Retrieve documents using .invoke() per new API
        docs = retriever.invoke(query)
        print("\nRetrieved Context Preview:")
        for i, d in enumerate(docs, 1):
            print(f"{i}.", d.page_content[:300].replace("\n", " "), "\n")

        # Join retrieved context for prompt
        joined_context = "\n\n".join([doc.page_content for doc in docs])

        prompt = f"""Answer the question using only the context below. 
If the answer is not present in the context, say "I don't know".

Context:
{joined_context}

Question: {query}
Helpful Answer:"""

        # Generate answer with .invoke()
        result = llm.invoke(prompt)

        print(f"\nAnswer: {result.strip()}")

    except Exception as e:
        print(f"Error:\n{e}")
