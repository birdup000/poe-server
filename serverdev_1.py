from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import asyncio
import uvicorn
import time
import logging

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


class PoeResponse(BaseModel):
    response: str


class ChatCompletionRequest(BaseModel):
    model: str
    messages: list[Message]


class PoeProvider:
    def __init__(
        self,
        POE_TOKENS: list = None,
        AI_MODEL: str = "chinchilla",
        proxy: str = None,
        **kwargs,
    ):
        self.POE_TOKENS = POE_TOKENS or []
        self.AI_MODEL = AI_MODEL.lower()
        self.current_token_index = 0
        self.proxy = proxy
        self.client = poe.Client(token=self._get_current_token(), proxy=self.proxy)

    def _get_current_token(self):
        return self.POE_TOKENS[self.current_token_index]

    def _rotate_token(self):
        self.current_token_index = (self.current_token_index + 1) % len(self.POE_TOKENS)
        self.client.token = self._get_current_token()

    async def chat_completion(self, messages:list, tokens: int = 0, max_retries=3):
        for i in range(max_retries):
            try:
                if self.AI_MODEL not in self.client.bot_names:
                    self.AI_MODEL = self.client.get_bot_by_codename(self.AI_MODEL)

                responses = []
                for msg in messages:
                    print(f"Sending message: {msg}")
                    response = self.client.send_message(
                        chatbot=self.AI_MODEL, message=msg['content']
                    )
                    responses.append(response)
                return responses
                
            except poe.exceptions.RateLimitError as e:  # Handle rate limit errors
                logging.error(f"Rate limit error: {str(e)}")
                self._rotate_token()
                time.sleep(2**i)  # Exponential backoff

            except poe.exceptions.InvalidTokenError as e:  # Handle invalid token errors
                logging.error(f"Invalid token error: {str(e)}")
                self._rotate_token()
                time.sleep(2**i)  # Exponential backoff

            except Exception as e:  # Catch all other exceptions
                logging.error(f"Unexpected error during instruction: {str(e)}")
                self._rotate_token()
                time.sleep(2**i)  # Exponential backoff

        raise HTTPException(
            status_code=429, detail="Rate limit exceeded despite retries"
        )


# Initialize PoeProvider here
poe_provider = PoeProvider(
    POE_TOKENS=[
        "token",
        "token",
    ],
    AI_MODEL="chinchilla",
    proxy="socks5://USER:PASS.SERVER:PORT",
)


@app.post("/v1/chat/completions", response_model=PoeResponse)
async def generate_response(chat_request: ChatCompletionRequest):
    try:
        print(f"Received chat request: {chat_request}")
        poe_provider.AI_MODEL = chat_request.model
        response_text = await poe_provider.chat_completion(messages=[m.dict() for m in chat_request.messages])
        return {"response": response_text}
    except Exception as e:
        logging.error(f"Error during response generation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)