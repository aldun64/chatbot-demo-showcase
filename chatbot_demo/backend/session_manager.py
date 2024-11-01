import requests
from typing import Optional

FASTAPI_URL = "http://127.0.0.1:8000"

def format_history(chat_history_store):
    '''Formats chat_history_store to have a newline character after every entry
    and chat message, duplicate in chatbot_service'''

    buffer = ""
    items = chat_history_store.items()
    for key, val in items:
        transcript_buffer = ""
        for line in val:
            transcript_buffer += f"{line}\n"
        buffer += f"ID: {key},\nTRANSCRIPT: {transcript_buffer}\n"
    return buffer

def create_session(session_id: Optional[str] = None):
    '''Creates session, optionally taking a session_id. 
    If session_id is not given, creates a session with random session_id and returns the server response.
    If session_id is given, creates a session with the given session_id and returns the server response.
    Returns an error message and response if the request is unsuccessful.'''

    if session_id is not None:
        response = requests.post(f"{FASTAPI_URL}/create_session/{session_id}")
        if response.status_code == 200:
            return f"create: {response.json()}"
        else:
            return f"Error while creating session: {response.status_code}"
    else:
        response = requests.post(f"{FASTAPI_URL}/create_session")
        if response.status_code == 200:
            return f"create: {response.json()}"
        else:
            return f"Error while creating session: {response.status_code}"

def delete_session(session_id: str):
    '''Attempts to delete the session with given session_id.
    If request is unsuccessful, returns an error message and the server response.'''

    response = requests.delete(f"{FASTAPI_URL}/delete_session/{session_id}")
    if response.status_code == 200:
        return f"delete: {response.json()}"
    else:
        return f"Error while deleting session: {response.status_code}"

def info_session(session_id: Optional[str] = None):
    '''Returns information, optionally taking a session_id.
    Currently, always returns entire chat_history_store.
    TODO: when session_id is provided, return information only about that session.'''

    response = requests.get(f"{FASTAPI_URL}/history_store")
    if response.status_code == 200:
        return f"History store retrieved successfully:\n{format_history(response.json().get("history_store"))}"
    else:
        return f"Error while retrieving history store:\n{response.status_code}"

def main():
    '''Main routine for session manager, taking user input and parsing it.
    If command syntax is wrong, returns helpful message.
    If command syntax is correct, execute the command and prints command's return value.'''


    user_input = ""

    while True:
        #initializes output message string
        out = ""
        #gets input and splits it into an array of words.
        user_input = input("type a command:")
        user_input_tokens = user_input.split()

        #parses first word, based on implemented commands: create, delete, info, quit.
        if (user_input_tokens[0] == "create"):
            #creates session or sets output to an error message based on number of input arguments.
            if len(user_input_tokens) == 1:
                out = create_session()
            elif len(user_input_tokens) == 2:
                out = create_session(user_input_tokens[1])
            else:
                out = "'create' command called with too many arguements"
        elif (user_input_tokens[0] == "delete"):
            #deletes session or sets output to an error message based on number of input arguments.
            if len(user_input_tokens) == 1:
                out = "'delete' command called with only one argument"
            elif len(user_input_tokens) == 2:
                out = delete_session(user_input_tokens[1])
            else:
                out = "'delete' command called with too many arguements"
        elif (user_input_tokens[0] == "info"):
            #sets output to output of session_info.
            out = info_session()
        elif (user_input_tokens[0] == "quit"):
            #breaks out of loop, ending the routine.
            break
        else:
            #command not pattern-matched, hence sets output to invalid command error message.
            out = f"invalid command: {user_input_tokens[0]}"
        #prints the output, either an error message or a return value of a successfully executed command
        print(out)

main()
print("The session manager has shut down.")