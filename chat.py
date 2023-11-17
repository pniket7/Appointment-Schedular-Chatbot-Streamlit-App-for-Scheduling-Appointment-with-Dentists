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
            line="You are a CSV reader chatbot app. answer user queries based on this information-The CSV file contains details of three employees: Senguttuvan, Jenifer Monica, and Poonkodi. Each employee has a respective LinkedIn profile, role, and a list of responsibilities/expertise. Here are the specifics:

Senguttuvan:
Role: Founder
LinkedIn Profile: Senguttuvan's LinkedIn Profile
Responsibilities/Expertise: Leadership, Research & Development, Chatbot Projects, Global Expansion, Analytical Abilities
Jenifer Monica:
Role: Managing Director
LinkedIn Profile: Jenifer Monica's LinkedIn Profile
Responsibilities/Expertise: Technical and Managerial Expertise, Team Leadership, Project Management
Poonkodi:
Role: Technical Lead
LinkedIn Profile: Poonkodi's LinkedIn Profile
Responsibilities/Expertise: System Oversight, AI Chatbot Initiatives, AI/ML Solutions, Technical Stacks (Angular, PHP, Yii2, Laravel, MySQL, MongoDB, Slackbot, DevOps), AWS, Git
Please answer user queries based on this information",
            role="user"
        )
        st.session_state.sessionAdvisor.inject(line="Ok.", role="assistant")

    # Initialize enter_pressed if it doesn't exist
    if "enter_pressed" not in st.session_state:
        st.session_state.enter_pressed = False

    # Display chat messages from history on app rerun
    chat_container = st.empty()
    chat_messages = ""
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            chat_messages += f'<p style="background-color: #9400D3; color: white; padding: 10px; border-radius: 10px; float: left; clear: both;">🧑 {message["content"]}</p>'
        else:
            chat_messages += f'<p style="background-color: #0084ff; color: white; padding: 10px; border-radius: 10px; float: right; clear: both;">🤖 {message["content"]}</p>'
    
    # Render the chat messages
    chat_container.markdown(f'<div style="border: 1px solid black; padding: 10px; height: 400px; overflow-y: scroll;">{chat_messages}</div>', unsafe_allow_html=True)

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

        # Clear the chat container
        chat_container.empty()

        # Display the latest messages
        chat_messages = ""
        for message in st.session_state.chat_history:
            if message["role"] == "user":
                chat_messages += f'<p style="background-color: #9400D3; color: white; padding: 10px; border-radius: 10px; float: left; clear: both;">🧑 {message["content"]}</p>'
            else:
                chat_messages += f'<p style="background-color: #0084ff; color: white; padding: 10px; border-radius: 10px; float: right; clear: both;">🤖 {message["content"]}</p>'
        
        # Render the updated chat messages
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

        # Clear the chat container for the new conversation
        chat_container.empty()

        # Display a message for a new conversation
        st.markdown("New conversation started. You can now enter your query.")

    # Create a button to exit the current conversation
    if st.button("Exit Chat"):
        # Clear the chat history to exit the chat
        st.session_state.chat_history = []

        # Clear the chat container for exiting the chat
        chat_container.empty()

        # Display a message for exiting the chat
        st.markdown("Chatbot session exited. You can start a new conversation by clicking the 'New Chat' button.")

if __name__ == "__main__":
    main()
