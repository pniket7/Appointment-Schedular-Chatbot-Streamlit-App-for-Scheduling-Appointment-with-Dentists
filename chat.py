import openai
import streamlit as st
from utils import ChatSession

def main():
    st.title('Financial Bank Advisor Chatbot')

    # Load the OpenAI API key from Streamlit secrets
    openai.api_key = st.secrets["api_key"]

    # Define CSS for the chat window
    st.markdown("""
    <style>
    .chat-container {
        background-color: #f5f5f5;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        max-width: 800px;
        margin-bottom: 20px;
    }
    .user-msg {
        background-color: #ddeeff;
        border-radius: 5px;
        padding: 8px;
        margin-bottom: 5px;
        width: 70%;
        float: left;
    }
    .bot-msg {
        background-color: #e6e6e6;
        border-radius: 5px;
        padding: 8px;
        margin-bottom: 5px;
        width: 70%;
        float: right;
    }
    </style>
    """, unsafe_allow_html=True)

    # Create a container for the chat window
    chat_container = st.empty()

    # Create a Streamlit text area for user input
    user_input = st.text_area("User Input:")

    # Create a button to send the user input
    if st.button("Send"):
        if "sessionAdvisor" not in st.session_state:
            # Initialize the AdvisorGPT if it doesn't exist in session_state
            st.session_state.sessionAdvisor = ChatSession(gpt_name='Advisor')
            st.session_state.sessionAdvisor.inject(
                line="You are a financial advisor at a bank. Start the conversation by inquiring about the user's financial goals. If the user mentions a specific financial goal or issue, acknowledge it and offer to help. Be attentive to the user's needs and goals.",
                role="user"
            )
            st.session_state.sessionAdvisor.inject(line="Ok.", role="assistant")

        # Update the chat session with the user's input
        st.session_state.sessionAdvisor.chat(user_input=user_input, verbose=False)

        # Get the chat history
        chat_history = st.session_state.sessionAdvisor.messages

        # Display the chat window
        with st.container():
            for message in chat_history:
                role = message['role']
                content = message['content']
                if role == 'user':
                    st.markdown(f'<div class="user-msg">{content}</div>', unsafe_allow_html=True)
                elif role == 'assistant':
                    st.markdown(f'<div class="bot-msg">{content}</div>', unsafe_allow_html=True)

    # Create a button to start a new conversation
    if st.button("New Chat"):
        if "sessionAdvisor" in st.session_state:
            del st.session_state.sessionAdvisor
        st.text("New conversation started. You can now enter your query.")
        user_input = ""

    # Create a button to exit the current conversation
    if st.button("Exit Chat"):
        if "sessionAdvisor" in st.session_state:
            del st.session_state.sessionAdvisor
        st.text("Chatbot session exited. You can start a new conversation by clicking the 'New Chat' button.")

if __name__ == "__main__":
    main()

