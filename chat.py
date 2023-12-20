import openai
import streamlit as st
from utils import ChatSession

def main():
    st.title('Appointment Scheduler Chatbot')

    openai.api_key = st.secrets["api_key"]

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    if "sessionAdvisor" not in st.session_state:
        st.session_state.sessionAdvisor = ChatSession(gpt_name='Advisor')
        # Insert initial information for appointment scheduler
        st.session_state.sessionAdvisor.inject(
            line="""You are an appointment scheduler chatbot app for scheduling user appointments with dentist doctors. Your main goal is to converse with the user and schedule an appointment for the user with the dentist. The user should be able to get details from you about the doctor's name, availability, and services offered (root canal, teeth cleaning, etc.). After collecting the details and getting confirmation from the user, you should give a message to the user about their appointment confirmation and appointment details which includes any random specific time from the available hours of that particular doctor. Be brief in your responses. Proceed with follow-up questions based solely on the user's immediate response, maintaining a strictly sequential flow. Ask one question at a time, waiting for and responding to each user input individually. Ensure that each response from the advisor contains only a single query or request for information, refraining from posing multiple questions or requests within the same reply. This is the data in JSON format about the doctor details - 
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
            }""",
            role="user"
        )
        st.session_state.sessionAdvisor.inject(line="Ok.", role="assistant")

    # Function to create a styled chat bubble using HTML and CSS
    def styled_chat_bubble(content, role):
        if role == "user":
            return f'<div style="background-color: #00008B; padding: 10px; border-radius: 15px; margin: 5px 20px;">🧑 {content}</div>'
        else:
            return f'<div style="background-color: #006400; padding: 10px; border-radius: 15px; margin: 5px 20px;">🤖 {content}</div>'

    for message in st.session_state.chat_history:
        if message["role"] == "user":
            st.markdown(styled_chat_bubble(message['content'], "user"), unsafe_allow_html=True)
        else:
            st.markdown(styled_chat_bubble(message['content'], "assistant"), unsafe_allow_html=True)

    user_input = st.text_input("Type your message here...")

    if st.button("Send"):
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        st.session_state.sessionAdvisor.chat(user_input=user_input, verbose=False)
        advisor_response = st.session_state.sessionAdvisor.messages[-1]['content'] if st.session_state.sessionAdvisor.messages else ""
        st.session_state.chat_history.append({"role": "bot", "content": advisor_response})
        st.markdown(styled_chat_bubble(advisor_response, "assistant"), unsafe_allow_html=True)

    if st.button("New Chat"):
        st.session_state.chat_history = []
        st.session_state.sessionAdvisor = ChatSession(gpt_name='Advisor')
        st.session_state.sessionAdvisor.inject(
            line="""You are an appointment scheduler chatbot app for scheduling user appointments with dentist doctors. Your main goal is to converse with the user and schedule an appointment for the user with the dentist. The user should be able to get details from you about the doctor's name, availability, and services offered (root canal, teeth cleaning, etc.). After collecting the details and getting confirmation from the user, you should give a message to the user about their appointment confirmation and appointment details which includes any random specific time from the available hours of that particular doctor. Be brief in your responses. Proceed with follow-up questions based solely on the user's immediate response, maintaining a strictly sequential flow. Ask one question at a time, waiting for and responding to each user input individually. Ensure that each response from the advisor contains only a single query or request for information, refraining from posing multiple questions or requests within the same reply. This is the data in JSON format about the doctor details - 
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
            }""",
            role="user"
        )
        st.session_state.sessionAdvisor.inject(line="Ok.", role="assistant")
        st.markdown("New conversation started. You can now enter your query.")

    if st.button("Exit Chat"):
        st.session_state.chat_history = []
        st.markdown("Chatbot session exited. You can start a new conversation by clicking the 'New Chat' button.")

if __name__ == "__main__":
    main()
