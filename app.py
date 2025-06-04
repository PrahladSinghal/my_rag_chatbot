import streamlit as st
from scripts.rag_chain import get_answer

st.set_page_config(page_title="Customer Support Chatbot", page_icon="🤖", layout="centered")

st.title("📞 Customer Support Chatbot (RAG)")
st.write("Ask me anything from the support documentation. If I don't know the answer, I'll tell you.")

# Chat history state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display history
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).markdown(msg["content"])

# User input
if prompt := st.chat_input("Ask your question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            answer = get_answer(prompt)
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
