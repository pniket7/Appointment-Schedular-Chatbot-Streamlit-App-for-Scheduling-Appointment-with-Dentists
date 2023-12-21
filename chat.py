import openai
import streamlit as st
import pickle
import time
import numpy as np
import pandas as pd
from typing import Optional, Union

def main():
    st.title('Appointment Scheduler Chatbot')

    openai.api_key = st.secrets["api_key"]

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    if "sessionAdvisor" not in st.session_state:
        st.session_state.sessionAdvisor = ChatSession(gpt_name='Advisor')
        # Insert initial information for appointment scheduler
        st.session_state.sessionAdvisor.inject(
            line="""You are an appointment scheduler chatbot app for scheduling user appointments with dentist doctors. Your main goal is to converse with the user and schedule an appointment for the user with the dentist in the week starting from 24 December, 2023 and ending on 30 December, 2023. The user should be able to get details from you about the doctor's name, availability, and services offered (root canal, teeth cleaning, etc.). After collecting the details from user and finalizing the day and date in the week starting from 24 December, 2023 and ending on 30 December, 2023, you should give a message to the user about their appointment confirmation and appointment details which includes any random specific time from the available hours of that particular doctor and the decided appointment date. So you should informed the user about the finalized date and time and end the conversation. Be brief in your responses. Proceed with follow-up questions based solely on the user's immediate response, maintaining a strictly sequential flow. Ask one question at a time, waiting for and responding to each user input individually. Ensure that each response from the advisor contains only a single query or request for information, refraining from posing multiple questions or requests within the same reply. Strickly avoid phrases like 'Hold on a moment while I fetch the information' in your responses. Don't keep the user waiting. Keep asking follow up questions. This is the data in JSON format about the doctor details - 
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
            line="""You are an appointment scheduler chatbot app for scheduling user appointments with dentist doctors. Your main goal is to converse with the user and schedule an appointment for the user with the dentist in the week starting from 24 December, 2023 and ending on 30 December, 2023. The user should be able to get details from you about the doctor's name, availability, and services offered (root canal, teeth cleaning, etc.). After collecting the details from user and finalizing the day and date in the week starting from 24 December, 2023 and ending on 30 December, 2023, you should give a message to the user about their appointment confirmation and appointment details which includes any random specific time from the available hours of that particular doctor and the decided appointment date. So you should informed the user about the finalized date and time and end the conversation. Be brief in your responses. Proceed with follow-up questions based solely on the user's immediate response, maintaining a strictly sequential flow. Ask one question at a time, waiting for and responding to each user input individually. Ensure that each response from the advisor contains only a single query or request for information, refraining from posing multiple questions or requests within the same reply. Strickly avoid phrases like 'Hold on a moment while I fetch the information' in your responses. Don't keep the user waiting. Keep asking follow up questions. This is the data in JSON format about the doctor details  - 
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

def ErrorHandler(f, *args, **kwargs):
    def wrapper(*args, **kwargs):
        while True:
            try:
                f(*args, **kwargs)
                break
            # RateLimitError
            except openai.error.RateLimitError:
                print('Rate limit exceeded. I will be back shortly, please wait for a minute.')
                time.sleep(60)
            # AuthenticationError
            except openai.error.AuthenticationError as e:
                print(e)
                raise
    return wrapper

class ChatSession:

    completions = {
            1: dict(
                completion=openai.ChatCompletion, model="gpt-3.5-turbo", text='message.content', prompt='messages'
            ),
            0: dict(
                completion=openai.Completion, model="text-davinci-003", text='text', prompt='prompt'
            )
        }

    def __init__(self, gpt_name='GPT') -> None:
        # History of all messages in the chat.
        self.messages = []

        # History of completions by the model.
        self.history = []

        # The name of the model.
        self.gpt_name = gpt_name

    def chat(self, user_input: Optional[Union[dict, str]] = None, verbose=True, *args, **kwargs):
        """ Say something to the model and get a reply. """

        completion_index = 0 if kwargs.get('logprobs', False) or kwargs.get('model') == 'text-davinci-003' else 1

        completion = self.completions[completion_index]

        user_input = self.__get_input(user_input=user_input, log=True)
        user_input = self.messages if completion_index else self.messages[-1]['content']

        kwargs.update({completion['prompt']: user_input, 'model': completion['model']})

        self.__get_reply(completion=completion['completion'], log=True, *args, **kwargs)

        self.history[-1].update({'completion_index': completion_index})

        if verbose:
            self.__call__(1)



    def inject(self, line, role):
        """ Inject lines into the chat. """

        self.__log(message={"role": role, "content": line})

    def clear(self, k=None):
        """ Clears session. If provided, last k messages are cleared. """
        if k:
            self.messages = self.messages[:-k]
            self.history = self.history[:-k]
        else:
            self.__init__()

    def save(self, filename):
        """ Saves the session to a file. """

        with open(filename, 'wb') as f:
            pickle.dump(self, f)

    def load(self, filename):
        """ Loads up the session. """

        with open(filename, 'rb') as f:
            temp = pickle.load(f)
            self.messages = temp.messages
            self.history = temp.history

    def merge(self, filename):
        """ Merges another session from a file with this one. """

        with open(filename, 'rb') as f:
            temp = pickle.load(f)
            self.messages += temp.messages
            self.history += temp.history

    def __get_input(self, user_input, log: bool = False):
        """ Converts user input to the desired format. """

        if user_input is None:
            user_input = input("> ")
        if not isinstance(user_input, dict):
            user_input = {"role": 'user', "content": user_input}
        if log:
            self.__log(user_input)
        return user_input

    @ErrorHandler
    def __get_reply(self, completion, log: bool = False, *args, **kwargs):
        """ Calls the model. """
        reply = completion.create(*args, **kwargs).choices[0]
        if log:
            if hasattr(reply, 'message'):
                self.__log(message=reply.message, history=reply)
            else:
                self.__log(message={"role": 'assistant', "content": reply.text}, history=reply)
        return reply

    def __log(self, message: dict, history=None):
        self.messages.append(message)
        if history is not None:
            assert isinstance(history, dict)
            self.history.append(history)

    def __call__(self, k: Optional[int] = None):
        """ Display the full chat log or the last k messages. """

        k = len(self.messages) if k is None else k
        for msg in self.messages[-k:]:
            message = msg['content']
            who = {'user': 'User: ', 'assistant': f'{self.gpt_name}: '}[msg['role']]
            print(who + message.strip() + '\n')

if __name__ == "__main__":
    main()
