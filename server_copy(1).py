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
logging.basicConfig(filename='app.log', level=logging.INFO)

app = FastAPI()

class Message(BaseModel):
    text: str

class PoeResponse(BaseModel):
    response: str

class PoeProvider:
    def __init__(self, POE_TOKENS: list = None, AI_MODEL: str = "chinchilla", proxy: str = None, **kwargs):
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

    async def instruct(self, prompt, tokens: int = 0, max_retries=3):
        for i in range(max_retries):
            try:
                if self.AI_MODEL not in self.client.bot_names:
                    self.AI_MODEL = self.client.get_bot_by_codename(self.AI_MODEL)

                for chunk in self.client.send_message(chatbot=self.AI_MODEL, message=prompt):
                    pass
                return chunk["text"]
            except Exception as e:  # Catch all exceptions as the correct ones are unknown
                logging.error(f"Error during instruction: {str(e)}")
                self._rotate_token()
                time.sleep(2 ** i)  # Exponential backoff

        raise HTTPException(status_code=429, detail="Rate limit exceeded despite retries")

# Initialize PoeProvider here
poe_provider = PoeProvider(
    POE_TOKENS=["3iri66XKmCCXYwvgB4mMng%3D%3D", "fY96RYHgy8I4-TUygsNvzQ%3D%3D", "fY96RYHgy8I4-TUygsNvzQ%3D%3D"],
    AI_MODEL="chinchilla",
    proxy="socks5://user:pass@server:port"
)

@app.post("/generate-response", response_model=PoeResponse)
async def generate_response(request: Request, message: Message):
    try:
        response_text = await poe_provider.instruct(prompt=message.text)
        return JSONResponse(content={"response": response_text})
    except Exception as e:
        logging.error(f"Error during response generation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)