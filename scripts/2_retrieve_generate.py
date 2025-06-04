from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.prompts import PromptTemplate
from transformers import pipeline
from langchain_community.llms import HuggingFacePipeline

# ✅ Load embedding model
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# ✅ Load FAISS vector store
vectordb = FAISS.load_local("../embeddings", embeddings=embedding_model, allow_dangerous_deserialization=True)

# ✅ Create retriever
retriever = vectordb.as_retriever(search_kwargs={"k": 3})

# ✅ Load Hugging Face model pipeline
hf_pipeline = pipeline(
    "text2text-generation",
    model="google/flan-t5-small",
    tokenizer="google/flan-t5-small",
    max_new_tokens=512,
)

llm = HuggingFacePipeline(pipeline=hf_pipeline)

# ✅ Chat loop
print("✅ Chatbot is ready! Ask your questions. (type 'exit' to quit)")
while True:
    query = input("\nYou: ")
    if query.lower() in ["exit", "quit"]:
        break

    try:
        # 🔍 Retrieve relevant documents
        docs = retriever.invoke(query)
        print("\n📄 Retrieved Context Preview:")
        for i, d in enumerate(docs, 1):
            print(f"{i}.", d.page_content[:300].replace("\n", " "), "\n")

        # 🧠 Join retrieved context
        joined_context = "\n\n".join([doc.page_content for doc in docs])

        # 💬 Use LLM to generate answer
        result = llm.invoke(f"""Answer the question using only the context below. 
If the answer is not present in the context, say "I don't know".

Context:
{joined_context}

Question: {query}
Helpful Answer:""")

        print(f"\n🤖 Answer: {result.strip()}")

    except Exception as e:
        print(f"❌ Error:\n{e}")
