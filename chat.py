import streamlit as st
import openai
from utils import ChatSession

def main():
    st.title('Financial Bank Advisor Chatbot')

    # Load the OpenAI API key from Streamlit secrets
    openai.api_key = st.secrets["api_key"]

    # Initialize chat history in session state if it doesn't exist
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Initialize sessionAdvisor if it doesn't exist
    if "sessionAdvisor" not in st.session_state:
        st.session_state.sessionAdvisor = ChatSession(gpt_name='Advisor')
        st.session_state.sessionAdvisor.inject(
            line="You are a financial advisor at a bank. Start the conversation by inquiring about the user's financial goals. If the user mentions a specific financial goal or issue, acknowledge it and offer to help. Be attentive to the user's needs and goals.",
            role="user"
        )
        st.session_state.sessionAdvisor.inject(line="Ok.", role="assistant")

    # Display chat messages from history on app rerun
    chat_messages = []
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            chat_messages.append({"role": "user", "message": message['content']})
        else:
            chat_messages.append({"role": "assistant", "message": message['content']})

    # Display the chat interface
    user_input = st.text_input("Type your message here...")
    if st.button("Send"):
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        st.session_state.sessionAdvisor.chat(user_input=user_input, verbose=False)
        advisor_response = st.session_state.sessionAdvisor.messages[-1]['content'] if st.session_state.sessionAdvisor.messages else ""
        st.session_state.chat_history.append({"role": "assistant", "content": advisor_response})
        chat_messages.append({"role": "assistant", "message": advisor_response})

    st.chat(chat_messages)

    # Create buttons for starting a new conversation and exiting the current one
    if st.button("New Chat"):
        st.session_state.chat_history = []
        st.session_state.sessionAdvisor = ChatSession(gpt_name='Advisor')
        st.session_state.sessionAdvisor.inject(
            line="You are a financial advisor at a bank. Start the conversation by inquiring about the user's financial goals. If the user mentions a specific financial goal or issue, acknowledge it and offer to help. Be attentive to the user's needs and goals.",
            role="user"
        )
        st.session_state.sessionAdvisor.inject(line="Ok.", role="assistant")

    if st.button("Exit Chat"):
        st.session_state.chat_history = []

if __name__ == "__main__":
    main()
