# app.py

import streamlit as st
from scripts.rag_chain import get_answer

st.set_page_config(page_title="Customer Support Chatbot", page_icon="🤖", layout="centered")

st.title("📞 Customer Support Chatbot (RAG)")
st.info("📚 This chatbot answers questions based only on Angel One's support & knowledge center documentation.")

# Chat history state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).markdown(msg["content"])

# Input from user
if prompt := st.chat_input("Ask your question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                answer = get_answer(prompt)
            except Exception as e:
                answer = "Sorry, something went wrong. Please try again later."
                st.error(f"Error: {e}")
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
