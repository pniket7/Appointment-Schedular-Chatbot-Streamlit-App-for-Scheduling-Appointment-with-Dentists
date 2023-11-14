import openai
import streamlit as st
from utils import ChatSession

def display_chat_history():
    chat_history = st.session_state.chat_history[::-1]  # Reverse the order to display latest messages at the top
    for message in chat_history:
        if message["role"] == "user":
            st.chat.send_message(message['content'], "USER")
        else:
            st.chat.send_message(message['content'], "BOT")

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
            line="You are a financial advisor at a bank. Start the conversation by inquiring about the user's financial goals. If the user mentions a specific financial goal or issue, acknowledge it and offer to help. Be attentive to the user's needs and goals. ",
            role="user"
        )
        st.session_state.sessionAdvisor.inject(line="Ok.", role="assistant")

    # Display chat messages from history on app rerun
    display_chat_history()

    # Accept user input
    user_input = st.text_input("Type your message here...")

    # Create a button to send the user input
    if st.button("Send"):
        # Add the user's message to the chat history
        st.session_state.chat_history.append({"role": "user", "content": user_input})

        # Update the chat session with the user's input
        st.session_state.sessionAdvisor.chat(user_input=user_input, verbose=False)

        # Get the chatbot's response from the last message in the history
        advisor_response = st.session_state.sessionAdvisor.messages[-1]['content'] if st.session_state.sessionAdvisor.messages else ""

        # Add the chatbot's response to the chat history
        st.session_state.chat_history.append({"role": "bot", "content": advisor_response})

        # Display the latest response using the chat interface
        if advisor_response:
            st.chat.send_message(advisor_response, "BOT")

    # Create a button to start a new conversation
    if st.button("New Chat"):
        # Clear the chat history to start a new conversation
        st.session_state.chat_history = []

        # Reinitialize sessionAdvisor for a new conversation
        st.session_state.sessionAdvisor = ChatSession(gpt_name='Advisor')
        st.session_state.sessionAdvisor.inject(
            line="You are a financial advisor at a bank. Start the conversation by inquiring about the user's financial goals. If the user mentions a specific financial goal or issue, acknowledge it and offer to help. Be attentive to the user's needs and goals. ",
            role="user"
        )
        st.session_state.sessionAdvisor.inject(line="Ok.", role="assistant")

if __name__ == "__main__":
    main()
