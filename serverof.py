from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import asyncio
import uvicorn
import logging
from typing import List
import time
import os
from dotenv import load_dotenv

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

class Message(BaseModel):
    role: str
    content: str

class Messages(BaseModel):
    model: str = "chinchilla"
    messages: List[Message]

class PoeResponse(BaseModel):
    choices: List[Message]

class PoeProvider:
    def __init__(
        self,
        POE_TOKENS: list = None,
        AI_MODEL: str = "chinchilla",
        proxy: str = None,
        **kwargs,
    ):
        self.POE_TOKENS = POE_TOKENS or []
        self.bad_tokens = []
        self.AI_MODEL = AI_MODEL.lower()
        self.current_token_index = 0
        self.proxy = proxy
        self.client = poe.Client(token=self._get_current_token(), proxy=self.proxy)

    def _get_current_token(self):
        return self.POE_TOKENS[self.current_token_index]

    def _rotate_token(self):
        if len(self.bad_tokens) == len(self.POE_TOKENS):
            self.bad_tokens = []  # Reset the bad tokens list if all tokens have been marked as bad

        self.current_token_index = (self.current_token_index + 1) % len(self.POE_TOKENS)
        while self._get_current_token() in self.bad_tokens:  # Skip over bad tokens
            self.current_token_index = (self.current_token_index + 1) % len(self.POE_TOKENS)

        self.client.token = self._get_current_token()

    async def instruct(self, messages: List[Message], tokens: int = 0, max_retries=3):
        for i in range(max_retries):
            try:
                if self.AI_MODEL not in self.client.bot_names:
                    self.AI_MODEL = self.client.get_bot_by_codename(self.AI_MODEL)
                
                # Get the last user message
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

            except poe.exceptions.RateLimitError as e:  # Handle rate limit errors
                logging.error(f"Rate limit error: {str(e)}")
                self._rotate_token()
                await asyncio.sleep(2**i)  # Exponential backoff

            except poe.exceptions.InvalidTokenError as e:  # Handle invalid token errors
                logging.error(f"Invalid token error: {str(e)}")
                self.bad_tokens.append(self._get_current_token())  # Mark the current token as bad
                self._rotate_token()
                await asyncio.sleep(2**i)  # Exponential backoff

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
        AI_MODEL="chinchilla",
        proxy=os.getenv("PROXY"),
    )

@app.post("/v1/chat/completions")
async def generate_response(request: Request, messages: Messages):
    try:
        response_message = await poe_provider.instruct(messages=messages.messages)
        return {
            'id': 'chatcmpl-xyz',  # You'll need to generate a real unique ID here
            'object': 'chat.completion',
            'created': int(time.time()),
            'model': messages.model,
            'choices': [{
                'message': {
                    'role': 'assistant',
                    'content': response_message['content']
                },
                'finish_reason': 'stop',
                'index': 0
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