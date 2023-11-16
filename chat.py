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
        st.session_state.sessionAdvisor = None

    if st.session_state.sessionAdvisor is None:
        st.session_state.sessionAdvisor = ChatSession(gpt_name='Advisor')
        st.session_state.sessionAdvisor.inject(
            line="You are a financial advisor at a bank. Start the conversation by inquiring about the user's financial goals. If the user mentions a specific financial goal or issue, acknowledge it and offer to help. Be attentive to the user's needs and goals. ",
            role="user"
        )
        st.session_state.sessionAdvisor.inject(line="Ok.", role="assistant")

    # Display chat messages from history on app rerun
    chat_container = st.empty()

    # Accept user input
    user_input = st.text_input("Type your message here...")

    # Create a button to send the user input
    if st.button("Send") or (not st.session_state.enter_pressed and user_input):
        # Add the user's message to the chat history
        st.session_state.chat_history.append({"role": "user", "content": user_input})

        # Update the chat session with the user's input
        st.session_state.sessionAdvisor.chat(user_input=user_input, verbose=False)

        # Get the chatbot's response from the last message in the history
        advisor_response = st.session_state.sessionAdvisor.messages[-1]['content'] if st.session_state.sessionAdvisor.messages else ""

        # Add the chatbot's response to the chat history
        st.session_state.chat_history.append({"role": "bot", "content": advisor_response})

        # Clear the chat container before updating with new messages
        chat_container.empty()

        # Display all messages in the updated chat history
        chat_messages = ""
        for message in st.session_state.chat_history:
            if message["role"] == "user":
                chat_messages += f'<p style="background-color: #9400D3; color: white; padding: 10px; border-radius: 10px; float: left; clear: both;">🧑 {message["content"]}</p>'
            else:
                chat_messages += f'<p style="background-color: #0084ff; color: white; padding: 10px; border-radius: 10px; float: right; clear: both;">🤖 {message["content"]}</p>'

        # Display the entire updated chat history in the chat container
        chat_container.markdown(f'<div style="border: 1px solid black; padding: 10px; height: 400px; overflow-y: scroll;">{chat_messages}</div>', unsafe_allow_html=True)

        # Set enter_pressed to True
        st.session_state.enter_pressed = True

    # Set enter_pressed to False when the user releases the Enter key
    if not user_input:
        st.session_state.enter_pressed = False

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

        # Clear the chat container before starting a new conversation
        chat_container.empty()

        # Display a message for a new conversation
        chat_container.markdown(f'<div style="border: 1px solid black; padding: 10px; height: 400px; overflow-y: scroll;"></div>', unsafe_allow_html=True)
        st.markdown("New conversation started. You can now enter your query.")

if __name__ == "__main__":
    main()
