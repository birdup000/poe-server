from fastapi import FastAPI, Request, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import asyncio
import uvicorn
import logging
from typing import List, Optional
import time
import os
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

try:
    import poe
except ImportError:
    import subprocess
    import sys

    subprocess.check_call([sys.executable, "-m", "pip", "install", "poe-api"])
    import poe

# Set up logging
logging.basicConfig(filename="app.log", level=logging.INFO)

app = FastAPI()

origins = [
    "http://localhost:8000",  
    "https://bettergpt.chat",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True, 
    allow_methods=["*"], 
    allow_headers=["*"],
)

class Message(BaseModel):
    role: str
    content: str

class Messages(BaseModel):
    model: str 
    messages: List[Message]

class CompletionPayload(BaseModel):
    prompt: str
    max_tokens: int
    temperature: float

class PoeResponse(BaseModel):
    choices: List[Message]

class PoeProvider:
    def __init__(
        self,
        POE_TOKENS: list = None,
        PROXIES: list = None,
        AI_MODEL: str = "chinchilla",
        **kwargs,
    ):
        self.POE_TOKENS = POE_TOKENS or []
        self.PROXIES = PROXIES or []
        self.bad_tokens = []
        self.AI_MODEL = AI_MODEL.lower()
        self.current_token_index = 0
        self.current_proxy_index = 0
        self.client = poe.Client(token=self._get_current_token(), proxy=self._get_current_proxy())

    def _get_current_token(self):
        return self.POE_TOKENS[self.current_token_index]

    def _get_current_proxy(self):
        return self.PROXIES[self.current_proxy_index]

    def _rotate_token(self):
        if len(self.bad_tokens) == len(self.POE_TOKENS):
            self.bad_tokens = []  # Reset the bad tokens list if all tokens have been marked as bad

        self.current_token_index = (self.current_token_index + 1) % len(self.POE_TOKENS)
        while self._get_current_token() in self.bad_tokens:  # Skip over bad tokens
            self.current_token_index = (self.current_token_index + 1) % len(self.POE_TOKENS)

        self.client.token = self._get_current_token()

    def _rotate_proxy(self):
        self.current_proxy_index = (self.current_proxy_index + 1) % len(self.PROXIES)
        self.client.proxy = self._get_current_proxy()

    async def instruct(self, messages: List[Message], tokens: int = 0, max_retries=3):
        for i in range(max_retries):
            try:
                self._rotate_proxy()  # Rotate the proxy for every request

                if self.AI_MODEL not in self.client.bot_names:
                    self.AI_MODEL = self.client.get_bot_by_codename(self.AI_MODEL)
                
                last_user_message = [msg for msg in messages if msg.role == "user"][-1].content

                if last_user_message.strip():  # Check if the message is not empty
                    for chunk in self.client.send_message(
                        chatbot=self.AI_MODEL, message=last_user_message
                    ):
                        pass
                    return {"role": "assistant", "content": chunk["text"]}
                else:
                    logging.warning("Attempted to send an empty message, skipping.")
                    return {"role": "assistant", "content": ""}
                
            except Exception as e:  # Catch all other exceptions
                logging.error(f"Unexpected error during instruction: {str(e)}")
                self._rotate_token()
                await asyncio.sleep(2**i)  # Exponential backoff

        raise HTTPException(
            status_code=429, detail="Rate limit exceeded despite retries"
        )

poe_provider = None

@app.on_event("startup")
async def startup_event():
    global poe_provider
    poe_provider = PoeProvider(
        POE_TOKENS=os.getenv("POE_TOKENS").split(","),
        PROXIES=os.getenv("PROXIES").split(","),
        AI_MODEL="chinchilla",
    )

# This is a generator function that yields data in chunks
async def stream_response(data):
    if isinstance(data, dict):
        yield json.dumps(data)
    else:
        for chunk in data:
            yield json.dumps(chunk)


@app.post("/v1/chat/completions", status_code=status.HTTP_200_OK)
async def generate_chat_response(request: Request):
    try:
        # Parse the incoming stream as JSON
        messages = await request.json()

        # Validate the input data
        messages = Messages(**messages)

        # Generate the response
        response_message = await poe_provider.instruct(messages=messages.messages)

        response_data = {
            'id': 'chatcmpl-xyz',  # You'll need to generate a real unique ID here
            'object': 'chat.completion',
            'created': int(time.time()),
            'model': messages.model,  # This will be the model passed from the request
            'choices': [{
                'message': {
                    'role': 'assistant',
                    'content': response_message['content']
                },
                'finish_reason': 'stop',
                'index': 0,
                'delta': 0
            }]
        }

        # Use the stream_response function to send the data in chunks
        return StreamingResponse(stream_response(response_data), media_type='application/json')

    except HTTPException as e:
        logging.error(f"Error during response generation: {str(e)}")
        raise e
    except Exception as e:
        logging.error(f"Unhandled exception: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/v1/engines/{model}/completions", status_code=status.HTTP_200_OK, response_class=StreamingResponse)
async def generate_completion(request: Request, model: str, payload: CompletionPayload):
    messages = [
        Message(role="user", content=payload.prompt)
    ]
    try:
        response_message = await poe_provider.instruct(messages=messages)
        return {
            'id': 'chatcmpl-xyz',  # You'll need to generate a real unique ID here
            'object': 'text.completion',
            'created': int(time.time()),
            'model': model,
            'choices': [{
                'text': response_message['content'],
                'index': 0,
                'delta': 0
            }]
        }
    except HTTPException as e:
        logging.error(f"Error during response generation: {str(e)}")
        raise e
    except Exception as e:
        logging.error(f"Unhandled exception: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)