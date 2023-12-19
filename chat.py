import openai
import streamlit as st

def initialize_chatbot():
    session = ChatSession(gpt_name='Advisor')
    session.inject(
        line="You are a CSV reader chatbot app. Answer user queries based on this information - The CSV file contains details of three employees: Senguttuvan, Jenifer Monica, and Poonkodi. Each employee has a respective LinkedIn profile, role, and a list of responsibilities/expertise. Here are the specifics:\n\nSenguttuvan:\nRole: Founder\nLinkedIn Profile: Senguttuvan's LinkedIn Profile\nResponsibilities/Expertise: Leadership, Research & Development, Chatbot Projects, Global Expansion, Analytical Abilities\n\nJenifer Monica:\nRole: Managing Director\nLinkedIn Profile: Jenifer Monica's LinkedIn Profile\nResponsibilities/Expertise: Technical and Managerial Expertise, Team Leadership, Project Management\n\nPoonkodi:\nRole: Technical Lead\nLinkedIn Profile: Poonkodi's LinkedIn Profile\nResponsibilities/Expertise: System Oversight, AI Chatbot Initiatives, AI/ML Solutions, Technical Stacks (Angular, PHP, Yii2, Laravel, MySQL, MongoDB, Slackbot, DevOps), AWS, Git\n\nPlease answer user queries based on this information. ",
        role="user"
    )
    session.inject(line="Ok.", role="assistant")
    return session

def main():
    st.title('Database Reader Chatbot')

    openai.api_key = st.secrets["api_key"]

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    if "sessionAdvisor" not in st.session_state:
        st.session_state.sessionAdvisor = initialize_chatbot()

    for message in st.session_state.chat_history:
        if message["role"] == "user":
            st.markdown("🧑 " + message['content'], unsafe_allow_html=True)
        else:
            st.markdown("🤖 " + message['content'], unsafe_allow_html=True)

    user_input = st.text_input("Type your message here...")

    if st.button("Send"):
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        st.session_state.sessionAdvisor.chat(user_input=user_input, verbose=False)
        advisor_response = st.session_state.sessionAdvisor.messages[-1]['content'] if st.session_state.sessionAdvisor.messages else ""
        st.session_state.chat_history.append({"role": "bot", "content": advisor_response})
        st.markdown("🤖 " + advisor_response, unsafe_allow_html=True)

    if st.button("New Chat"):
        st.session_state.chat_history = []
        st.session_state.sessionAdvisor = initialize_chatbot()
        st.markdown("New conversation started. You can now enter your query.")

    if st.button("Exit Chat"):
        st.session_state.chat_history = []
        st.markdown("Chatbot session exited. You can start a new conversation by clicking the 'New Chat' button.")

if __name__ == "__main__":
    main()
