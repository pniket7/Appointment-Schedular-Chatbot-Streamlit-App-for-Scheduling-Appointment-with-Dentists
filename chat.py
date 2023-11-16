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

    # Display chat messages from history on app rerun
    chat_container = st.empty()
    chat_messages = ""
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            chat_messages += f'<p style="background-color: #9400D3; color: white; padding: 10px; border-radius: 10px; float: left; clear: both;">🧑 {message["content"]}</p>'
        else:
            chat_messages += f'<p style="background-color: #0084ff; color: white; padding: 10px; border-radius: 10px; float: right; clear: both;">🤖 {message["content"]}</p>'
    chat_container.markdown(f'<div style="border: 1px solid black; padding: 10px; height: 400px; overflow-y: scroll;">{chat_messages}</div>', unsafe_allow_html=True)

    # Accept user input
    with st.form(key='user_input_form'):
        user_input = st.text_input("Type your message here...")
        submitted = st.form_submit_button(label='Send')

        # Submit the form when the enter key is pressed
        if user_input and (submitted or st.session_state.enter_pressed):
            st.session_state.enter_pressed = False
            st.form_submit_button(label='Send')

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
        chat_messages = ""
        chat_container.markdown(f'<div style="border: 1px solid black; padding: 10px; height: 400px; overflow-y: scroll;">{chat_messages}</div>', unsafe_allow_html=True)
        st.markdown("New conversation started. You can now enter your query.")

    # Create a button to exit the current conversation
    if st.button("Exit Chat"):
        # Clear the chat history to exit the chat
        st.session_state.chat_history = []

        # Display a message for exiting the chat
        chat_messages = ""
        chat_container.markdown(f'<div style="border: 1px solid black; padding: 10px; height: 400px; overflow-y: scroll;">{chat_messages}</div>', unsafe_allow_html=True)
        st.markdown("Chatbot session exited. You can start a new conversation by clicking the 'New Chat' button.")

if __name__ == "__main__":
    main()
