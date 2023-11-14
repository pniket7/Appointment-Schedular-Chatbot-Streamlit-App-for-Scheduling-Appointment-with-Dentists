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

    # Display chat messages using st.chat
    with st.expander("Chat"):
        chat_history = [
            {"role": message["role"], "text": message["content"]} 
            for message in st.session_state.chat_history
        ]
        st.chat(chat_history)

    # Accept user input
    user_input = st.text_input("Type your message here...")

    # Create a button to send the user input
    if st.button("Send"):
        # Add the user's message to the chat history
        st.session_state.chat_history.append({"role": "user", "content": user_input})

        # Update the chat session with the user's input
        st.session_state.sessionAdvisor.chat(user_input=user_input, verbose=False)

        # Get the chatbot's response from OpenAI
        advisor_response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=user_input,
            max_tokens=50
        ).choices[0].text

        # Add the chatbot's response to the chat history
        st.session_state.chat_history.append({"role": "bot", "content": advisor_response})

if __name__ == "__main__":
    main()
