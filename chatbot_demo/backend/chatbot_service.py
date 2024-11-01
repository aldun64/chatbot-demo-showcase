from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from openai import OpenAI
import uuid
import logging
import prompt_builder.builder as prompt_builder
from dotenv import load_dotenv
import os

#loads .env file 
load_dotenv()
#prompt build, later will use database
prompt = prompt_builder.build_prompt("default")
bot_config = prompt_builder.get_bot_config("default")
intro_message = bot_config["intro_message"]
chat_history_base = [
        {"role": "system", "content":prompt},
        {"role": "assistant", "content":intro_message}
]

#storage of chat histories with session ids as keys
chat_history_store = {
    "test": chat_history_base.copy()
}

#fastAPI setup
app = FastAPI()
#logging setup
logging.basicConfig(level=logging.INFO)
#openai setup
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
#types
class ChatRequest(BaseModel):
    session_id: str
    message: str
#helpers
def format_transcripts():
    '''Formats chat_history_store to have a newline character after every entry and chat message'''

    buffer = ""
    items = chat_history_store.items()
    for key, val in items:
        transcript_buffer = ""
        for line in val:
            transcript_buffer += f"{line}\n"
        buffer += f"ID: {key}, TRANSCRIPT: {transcript_buffer}\n"
    return buffer

#start
@app.post("/chat")
async def chat(request: ChatRequest):
    '''Attempts to generate a response given a chat request consisting of session_id and message.'''
    
    #extracts and logs data in request
    session_id = request.session_id
    user_message = request.message
    logging.info(f"Received and recorded message from user with session id: {session_id}.\nmessage: {user_message}")

    #raises exception if session_id does not exist in chat_history_store
    if session_id not in chat_history_store:
        raise HTTPException(status_code=404, detail="Session does not exist")
    
    #otherwise, it must exist, hence gets it safely and logs
    chat_history = chat_history_store[session_id]
    logging.info(f"Retreived chat history:\n{chat_history}")

    #appends user message to history to generate the prompt for AI
    chat_history.append({"role": "user", "content": user_message})

    #tries to generate and log response
    try:
        response = client.chat.completions.create(
            model= "gpt-4o-mini",
            messages= chat_history
        )
        bot_message = response.choices[0].message.content
        logging.info(f"Bot response generated: {bot_message}")
        
        #appends the response to the history and returns it
        chat_history.append({"role": "assistant", "content": bot_message})
        response = {"response": bot_message}

        return response
    
    #if exception is caught, logs it and returns error JSONResponse
    except Exception as e:
        logging.error(f"Error during OpenAI API call: {str(e)}")
        return JSONResponse(content={"error": str(e)}, status_code=500)
    
@app.get("/history/{session_id}")
async def get_chat_history(session_id: str):
    '''Retrieves history from chat_history_store. Raises HTTPError 404 if session_id not in store.'''

    if session_id in chat_history_store:
        return {"history": chat_history_store[session_id]}
    else:
        raise HTTPException(status_code=404, detail="Session does not exist")
    
@app.get("/validate_session/{session_id}")
async def validate_session(session_id: str):
    '''Validates a session_id by checking if it exists in chat_history_store.'''

    return {"valid": str(session_id in chat_history_store)}

@app.post("/create_session")
async def create_random_session():
    '''Creates a session with a random uuid4.
    Returns the new session id.'''

    new_session_id = str(uuid.uuid4())
    chat_history_store[new_session_id] = chat_history_base.copy()
    return {"session_id": new_session_id}

@app.post("/create_session/{session_id}")
async def create_session(session_id: str):
    '''Attempts to create a session with given uuid.
    Raises HTTPError 400 if uuid already exists.'''

    if session_id in chat_history_store:
        raise HTTPException(status_code=400, detail="Session already exists")
    else:
        chat_history_store[session_id] = chat_history_base.copy()
        return {"session_id": session_id}

@app.delete("/delete_session/{session_id}")
async def delete_session(session_id: str):
    '''Attempts to delete a session with given uuid.
    Raises HTTPError 404 if uuid does not exist.'''

    if session_id in chat_history_store:
        return {"history": chat_history_store.pop(session_id)}
    else:
        raise HTTPException(status_code=404, detail="Session does not exist")

@app.get("/history_store")
async def get_history_store():
    '''Returns chat_history_store.'''

    return {"history_store": chat_history_store}
