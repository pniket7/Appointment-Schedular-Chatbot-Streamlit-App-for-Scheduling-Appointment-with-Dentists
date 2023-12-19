import openai
import streamlit as st
import pandas as pd
from utils import ChatSession


def main():
    st.title('Database Reader Chatbot')

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
            line="You are a appointment scheduler chatbot app for scheduling user appointments with dentist doctors. Your main goal is to converse with the user and schedule a appointment for the user with the dentist. The user should be able to get details from you about the doctor name, his availability and timings, service the doctor offers(root canal, teeth cleaning, etc.). After collecting the details and getting the conformation from the user, you should give message to the user about his  appointment conformation and appointment details. Be brief in your responses. Proceed with follow-up questions based solely on the user's immediate response, maintaining a strictly sequential flow. Ask one question at a time, waiting for and responding to each user input individually. Ensure that each response from the advisor contains only a single query or request for information, refraining from posing multiple questions or requests within the same reply. This is the data in json format about the doctor details-
{
  "doctors": [
    {
      "name": "Dr. John Smith",
      "service": "Tooth Replacement",
      "availability": [
        {
          "day": "Monday",
          "timings": "10am-6pm"
        },
        {
          "day": "Tuesday",
          "timings": "10am-6pm"
        },
        {
          "day": "Friday",
          "timings": "10am-6pm"
        }
      ]
    },
    {
      "name": "Dr. Roger Blake",
      "service": "Root Canal",
      "availability": [
        {
          "day": "Wednesday",
          "timings": "11am-3pm"
        },
        {
          "day": "Friday",
          "timings": "11am-3pm"
        }
      ]
    },
    {
      "name": "Dr. Ryan Harris",
      "service": "Tooth Cleaning",
      "availability": [
        {
          "day": "Monday",
          "timings": "9am-6pm"
        },
        {
          "day": "Thursday",
          "timings": "9am-6pm"
        },
        {
          "day": "Saturday",
          "timings": "9am-6pm"
        }
      ]
    },
    {
      "name": "Dr. Millie James",
      "service": "Tooth Replacement",
      "availability": [
        {
          "day": "Friday",
          "timings": "9am-7pm"
        },
        {
          "day": "Saturday",
          "timings": "9am-7pm"
        }
      ]
    },
    {
      "name": "Dr. Crystal Miles",
      "service": "Tooth Cleaning",
      "availability": [
        {
          "day": "Wednesday",
          "timings": "9am-3pm"
        },
        {
          "day": "Friday",
          "timings": "9am-3pm"
        },
        {
          "day": "Saturday",
          "timings": "9am-3pm"
        }
      ]
    },
    {
      "name": "Dr. Jessica Brown",
      "service": "Tooth Replacement",
      "availability": [
        {
          "day": "Monday",
          "timings": "8am-6pm"
        },
        {
          "day": "Tuesday",
          "timings": "8am-6pm"
        },
        {
          "day": "Thursday",
          "timings": "8am-6pm"
        }
      ]
    },
    {
      "name": "Dr. Jenna Starc",
      "service": "Root Canal",
      "availability": [
        {
          "day": "Wednesday",
          "timings": "10am-7pm"
        },
        {
          "day": "Thursday",
          "timings": "10am-7pm"
        }
      ]
    },
    {
      "name": "Dr. David Ness",
      "service": "Root Canal",
      "availability": [
        {
          "day": "Thursday",
          "timings": "8am-6pm"
        },
        {
          "day": "Friday",
          "timings": "8am-6pm"
        },
        {
          "day": "Saturday",
          "timings": "8am-6pm"
        }
      ]
    }
  ]
}",
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
            line="You are a appointment scheduler chatbot app for scheduling user appointments with dentist doctors. Your main goal is to converse with the user and schedule a appointment for the user with the dentist. The user should be able to get details from you about the doctor name, his availability and timings, service the doctor offers(root canal, teeth cleaning, etc.). After collecting the details and getting the conformation from the user, you should give message to the user about his  appointment conformation and appointment details. Be brief in your responses. Proceed with follow-up questions based solely on the user's immediate response, maintaining a strictly sequential flow. Ask one question at a time, waiting for and responding to each user input individually. Ensure that each response from the advisor contains only a single query or request for information, refraining from posing multiple questions or requests within the same reply. This is the data in json format about the doctor details-
{
  "doctors": [
    {
      "name": "Dr. John Smith",
      "service": "Tooth Replacement",
      "availability": [
        {
          "day": "Monday",
          "timings": "10am-6pm"
        },
        {
          "day": "Tuesday",
          "timings": "10am-6pm"
        },
        {
          "day": "Friday",
          "timings": "10am-6pm"
        }
      ]
    },
    {
      "name": "Dr. Roger Blake",
      "service": "Root Canal",
      "availability": [
        {
          "day": "Wednesday",
          "timings": "11am-3pm"
        },
        {
          "day": "Friday",
          "timings": "11am-3pm"
        }
      ]
    },
    {
      "name": "Dr. Ryan Harris",
      "service": "Tooth Cleaning",
      "availability": [
        {
          "day": "Monday",
          "timings": "9am-6pm"
        },
        {
          "day": "Thursday",
          "timings": "9am-6pm"
        },
        {
          "day": "Saturday",
          "timings": "9am-6pm"
        }
      ]
    },
    {
      "name": "Dr. Millie James",
      "service": "Tooth Replacement",
      "availability": [
        {
          "day": "Friday",
          "timings": "9am-7pm"
        },
        {
          "day": "Saturday",
          "timings": "9am-7pm"
        }
      ]
    },
    {
      "name": "Dr. Crystal Miles",
      "service": "Tooth Cleaning",
      "availability": [
        {
          "day": "Wednesday",
          "timings": "9am-3pm"
        },
        {
          "day": "Friday",
          "timings": "9am-3pm"
        },
        {
          "day": "Saturday",
          "timings": "9am-3pm"
        }
      ]
    },
    {
      "name": "Dr. Jessica Brown",
      "service": "Tooth Replacement",
      "availability": [
        {
          "day": "Monday",
          "timings": "8am-6pm"
        },
        {
          "day": "Tuesday",
          "timings": "8am-6pm"
        },
        {
          "day": "Thursday",
          "timings": "8am-6pm"
        }
      ]
    },
    {
      "name": "Dr. Jenna Starc",
      "service": "Root Canal",
      "availability": [
        {
          "day": "Wednesday",
          "timings": "10am-7pm"
        },
        {
          "day": "Thursday",
          "timings": "10am-7pm"
        }
      ]
    },
    {
      "name": "Dr. David Ness",
      "service": "Root Canal",
      "availability": [
        {
          "day": "Thursday",
          "timings": "8am-6pm"
        },
        {
          "day": "Friday",
          "timings": "8am-6pm"
        },
        {
          "day": "Saturday",
          "timings": "8am-6pm"
        }
      ]
    }
  ]
} ",
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
