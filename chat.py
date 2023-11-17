import openai
import streamlit as st
import pandas as pd
from utils import ChatSession

# Read the CSV file
data = pd.read_csv('database.csv')

def display_matching_data(query):
    # Filter the data based on the user query
    matching_data = data[data['Responsibilities_Expertise'].str.contains(query, case=False)]

    # Display specific details from matching rows
    for index, row in matching_data.iterrows():
        st.markdown(f"**Name:** {row['NAME']}")
        st.markdown(f"**Role:** {row['ROLE']}")
        st.markdown(f"**LinkedIn Profile:** [{row['NAME']}]({row['LinkedIn_Profile']})")
        st.markdown(f"**Responsibilities/Expertise:** {row['Responsibilities_Expertise']}")

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
        # Inject initial information
        st.session_state.sessionAdvisor.inject(
            line="You are a CSV reader chatbot app. Answer user queries based on this information - The CSV file contains details of three employees: Senguttuvan, Jenifer Monica, and Poonkodi. Each employee has a respective LinkedIn profile, role, and a list of responsibilities/expertise. Here are the specifics:\n\nSenguttuvan:\nRole: Founder\nLinkedIn Profile: Senguttuvan's LinkedIn Profile\nResponsibilities/Expertise: Leadership, Research & Development, Chatbot Projects, Global Expansion, Analytical Abilities\n\nJenifer Monica:\nRole: Managing Director\nLinkedIn Profile: Jenifer Monica's LinkedIn Profile\nResponsibilities/Expertise: Technical and Managerial Expertise, Team Leadership, Project Management\n\nPoonkodi:\nRole: Technical Lead\nLinkedIn Profile: Poonkodi's LinkedIn Profile\nResponsibilities/Expertise: System Oversight, AI Chatbot Initiatives, AI/ML Solutions, Technical Stacks (Angular, PHP, Yii2, Laravel, MySQL, MongoDB, Slackbot, DevOps), AWS, Git\n\nPlease answer user queries based on this information. ",
            role="user"
        )
        st.session_state.sessionAdvisor.inject(line="Ok.", role="assistant")

    # Display chat messages from history on app rerun
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            st.markdown("🧑 " + message['content'], unsafe_allow_html=True)
        else:
            st.markdown("🤖 " + message['content'], unsafe_allow_html=True)

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

        # Display the latest response
        st.markdown("🤖 " + advisor_response, unsafe_allow_html=True)

    # Create a button to start a new conversation
    if st.button("New Chat"):
        # Clear the chat history to start a new conversation
        st.session_state.chat_history = []

        # Reinitialize sessionAdvisor for a new conversation
        st.session_state.sessionAdvisor = ChatSession(gpt_name='Advisor')
        # Inject initial information
        st.session_state.sessionAdvisor.inject(
            line="You are a CSV reader chatbot app. Answer user queries based on this information - The CSV file contains details of three employees: Senguttuvan, Jenifer Monica, and Poonkodi. Each employee has a respective LinkedIn profile, role, and a list of responsibilities/expertise. Here are the specifics:\n\nSenguttuvan:\nRole: Founder\nLinkedIn Profile: Senguttuvan's LinkedIn Profile\nResponsibilities/Expertise: Leadership, Research & Development, Chatbot Projects, Global Expansion, Analytical Abilities\n\nJenifer Monica:\nRole: Managing Director\nLinkedIn Profile: Jenifer Monica's LinkedIn Profile\nResponsibilities/Expertise: Technical and Managerial Expertise, Team Leadership, Project Management\n\nPoonkodi:\nRole: Technical Lead\nLinkedIn Profile: Poonkodi's LinkedIn Profile\nResponsibilities/Expertise: System Oversight, AI Chatbot Initiatives, AI/ML Solutions, Technical Stacks (Angular, PHP, Yii2, Laravel, MySQL, MongoDB, Slackbot, DevOps), AWS, Git\n\nPlease answer user queries based on this information. ",
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

    # Check if the user input is a query to display CSV details
    if user_input.lower().startswith('show details for'):
        query = user_input.lower().replace('show details for', '').strip()
        display_matching_data(query)

    # Integrate functionality from the added code snippet
    st.title('Person Information Viewer')

    # Dropdown to select a person
    selected_person = st.selectbox('Select a person:', data['NAME'])

    if st.button('Get Info'):
        # Get the details of the selected person
        person_details = data[data['NAME'] == selected_person].iloc[0]
        role = person_details['ROLE']
        linkedin_profile = person_details['LinkedIn_Profile']
        responsibilities = person_details['Responsibilities_Expertise']

        # Display the details
        st.markdown(f"**Role:** {role}")
        st.markdown(f"**LinkedIn Profile:** [{selected_person}]({linkedin_profile})")
        st.markdown(f"**Responsibilities/Expertise:** {responsibilities}")

if __name__ == "__main__":
    main()
