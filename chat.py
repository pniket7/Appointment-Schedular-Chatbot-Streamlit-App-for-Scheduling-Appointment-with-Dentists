import openai
import streamlit as st
from utils import ChatSession

def main():
    st.title('Financial Bank Advisor Chatbot')

    # Load the OpenAI API key from Streamlit secrets
    openai.api_key = st.secrets["api_key"]

    # Create a Streamlit chat input widget for user input with a unique key
    user_input = st.chat_input("User:")

    # Create a Streamlit button with a unique key to send the user input
    if st.button("Send", key="send_button"):
        if "sessionAdvisor" not in st.session_state:
            # Initialize the AdvisorGPT if it doesn't exist in session_state
            st.session_state.sessionAdvisor = ChatSession(gpt_name='Advisor')

            # Instruct GPT to become a financial advisor.
            st.session_state.sessionAdvisor.inject(
                line="You are a financial advisor at a bank. Start the conversation by inquiring about the user's financial goals. If the user mentions a specific financial goal or issue, acknowledge it and offer to help. Be attentive to the user's needs and goals. ",
                role="user"
            )
            st.session_state.sessionAdvisor.inject(line="Ok.", role="assistant")

        # Update the chat session with the user's input
        st.session_state.sessionAdvisor.chat(user_input=user_input, verbose=False)

        # Get the chat history, which includes the chatbot's response
        chat_history = st.session_state.sessionAdvisor.messages

        # Extract the chatbot's response from the last message in the history
        advisor_response = chat_history[-1]['content'] if chat_history else ""

        # Display the chatbot's response with text wrapping
        with st.chat_message("Advisor:"):
            st.write(advisor_response)

    # Create a button to start a new conversation
    if st.button("New Chat", key="new_chat_button"):
        if "sessionAdvisor" in st.session_state:
            # Remove the existing sessionAdvisor from session_state
            del st.session_state.sessionAdvisor
        st.text("New conversation started. You can now enter your query.")

        # Clear the user input field by updating the user_input variable
        user_input = ""

    # Create a button to exit the current conversation
    if st.button("Exit Chat", key="exit_chat_button"):
        if "sessionAdvisor" in st.session_state:
            # Remove the existing sessionAdvisor from session_state to exit the chat
            del st.session_state.sessionAdvisor

        st.text("Chatbot session exited. You can start a new conversation by clicking the 'New Chat' button.")

if __name__ == "__main__":
    main()
