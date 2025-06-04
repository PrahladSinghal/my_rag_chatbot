# scripts/rag_chain.py

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from transformers import pipeline
from langchain_community.llms import HuggingFacePipeline

# Load embedding model and FAISS vectorstore
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vectordb = FAISS.load_local("embeddings", embeddings=embedding_model, allow_dangerous_deserialization=True)
retriever = vectordb.as_retriever(search_kwargs={"k": 3})

# Prompt
prompt_template = """Use the following context to answer the question concisely:
{context}
Question: {question}
Helpful Answer:"""
PROMPT = PromptTemplate(template=prompt_template, input_variables=["context", "question"])

# HuggingFace pipeline
hf_pipeline = pipeline("text2text-generation", model="google/flan-t5-small", tokenizer="google/flan-t5-small", max_new_tokens=512)
llm = HuggingFacePipeline(pipeline=hf_pipeline)

# RAG chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever,
    return_source_documents=False,
    chain_type_kwargs={"prompt": PROMPT},
)


def get_answer(query: str) -> str:
    result = qa_chain.invoke({"query": query})

    answer = result.get("result", "").strip()

    if not answer or "i don't know" in answer.lower():
        return "I don't know"

    return answer
