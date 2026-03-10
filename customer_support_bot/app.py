import streamlit as st

from agent import handle_query



st.set_page_config(page_title="Pranathi AI Support", layout="wide")


# -------------------------------
# Session State
# -------------------------------

if "history" not in st.session_state:
    st.session_state.history = []

if "conversations" not in st.session_state:
    st.session_state.conversations = []


# -------------------------------
# Sidebar
# -------------------------------

st.sidebar.title("Conversations")

for i, conv in enumerate(st.session_state.conversations):
    if st.sidebar.button(conv, key=i):
        st.session_state.history = []

if st.sidebar.button("New Chat"):
    st.session_state.history = []


# -------------------------------
# Title
# -------------------------------

st.title("Pranathi Software Services AI Support")


# -------------------------------
# Show Previous Messages
# -------------------------------

for msg in st.session_state.history:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])



# -------------------------------
# User Input
# -------------------------------

query = st.chat_input("Ask your question")

if query:
    print("User query:", query)
    # Show user message
    with st.chat_message("user"):
        st.write(query)

    # Get response
    answer = handle_query(query)

    # Show assistant response
    with st.chat_message("assistant"):
        st.write(answer)
    
    print(st.session_state.history)
    # Save history
    st.session_state.history.append(
        {"role": "user", "content": query}
    )

    st.session_state.history.append(
        {"role": "assistant", "content": answer}
    )

    # Save conversation title
    if len(st.session_state.history) == 2:
        st.session_state.conversations.append(query)