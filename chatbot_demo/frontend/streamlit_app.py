import streamlit as st
import requests

FASTAPI_URL = "http://127.0.0.1:8000"

def get_chat_history(session_id):
    '''Retrieves chat history associated with SESSION_ID.
    If request is not OK, returns empty history.'''

    response = requests.get(f"{FASTAPI_URL}/history/{session_id}")
    if response.status_code == 200:
        return response.json().get("history", [])
    else:
        return []

def send_message(user_message: str, session_id: str):
    '''Sends USER_MESSAGE under SESSION_ID as a request.
    Returns the bot_message, or an error message if request is not OK.'''
    
    response = requests.post(f"{FASTAPI_URL}/chat", json={"message": user_message, "session_id": session_id})

    if response.status_code == 200:
        data = response.json()
        bot_message = data.get("response", "No response from bot")
        return bot_message
    else:
        return "Error: Could not get response from bot"

def validate_session(session_id: str):
    '''Validates the existence of SESSION_ID in server history store.
    If request fails, returns False.'''

    response = requests.get(f"{FASTAPI_URL}/validate_session/{session_id}")
    if (response.json()["valid"]) == "True":
        return True
    else:
        return False

def main():
    '''Main routine using streamlit interface.'''

    validated: bool = False
    local_session_id: str = None
    local_history = {}

    st.title("Chatbot")
    if not validated:
        session_id_input = st.text_input("Enter your session ID:")
        if session_id_input:
            if validate_session(session_id_input):
                local_session_id = session_id_input
                local_history = get_chat_history(session_id_input)
                validated = True
#todo    
    if validated:
        if user_input := st.chat_input("Type your response here"):
            bot_response = send_message(user_input, local_session_id)
            local_history.append({"role": "user", "content": user_input})
            local_history.append({"role": "assistant", "content": bot_response})

        for message in local_history:
            if message["role"] != "system":
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])


if __name__ == "__main__":
    main()

