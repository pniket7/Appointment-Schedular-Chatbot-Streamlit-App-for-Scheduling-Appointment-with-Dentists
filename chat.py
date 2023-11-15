import openai
import streamlit as st
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
            line="You are a financial advisor at a bank. Start the conversation by inquiring about the user's financial goals. If the user mentions a specific financial goal or issue, acknowledge it and offer to help. Be attentive to the user's needs and goals. ",
            role="user"
        )
        st.session_state.sessionAdvisor.inject(line="Ok.", role="assistant")

    # Create containers for user and bot messages
    user_container = st.empty()
    bot_container = st.empty()

    # Display chat messages from history on app rerun
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            user_container.markdown(f'<div style="border: 1px solid #ccc; border-radius: 5px; padding: 10px; margin: 5px 0;"><span style="font-weight: bold; color: blue;">User:</span> {message["content"]}</div>', unsafe_allow_html=True)
        else:
            bot_container.markdown(f'<div style="border: 1px solid #ccc; border-radius: 5px; padding: 10px; margin: 5px 0;"><span style="font-weight: bold; color: green;">Bot:</span> {message["content"]}</div>', unsafe_allow_html=True)

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

    # Clear containers and display the updated messages
    user_container.empty()
    bot_container.empty()
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            user_container.markdown(f'<div style="border: 1px solid #ccc; border-radius: 5px; padding: 10px; margin: 5px 0;"><span style="font-weight: bold; color: blue;">User:</span> {message["content"]}</div>', unsafe_allow_html=True)
        else:
            bot_container.markdown(f'<div style="border: 1px solid #ccc; border-radius: 5px; padding: 10px; margin: 5px 0;"><span style="font-weight: bold; color: green;">Bot:</span> {message["content"]}</div>', unsafe_allow_html=True)

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

        # Display a message for a new conversation
        st.markdown("New conversation started. You can now enter your query.")

    # Create a button to exit the current conversation
    if st.button("Exit Chat"):
        # Clear the chat history to exit the chat
        st.session_state.chat_history = []

        # Display a message for exiting the chat
        st.markdown("Chatbot session exited. You can start a new conversation by clicking the 'New Chat' button.")

if __name__ == "__main__":
    main()
