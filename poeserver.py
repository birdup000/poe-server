from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import asyncio
import uvicorn

try:
    import poe
except ImportError:
    import subprocess
    import sys

    subprocess.check_call([sys.executable, "-m", "pip", "install", "poe-api"])
    import poe

app = FastAPI()

class Message(BaseModel):
    text: str

class PoeResponse(BaseModel):
    response: str

class PoeProvider:
    def __init__(self, POE_TOKENS: list = None, AI_MODEL: str = "chinchilla", **kwargs):
        self.requirements = ["poe-api"]
        self.POE_TOKENS = POE_TOKENS or []
        self.AI_MODEL = AI_MODEL.lower()
        self.current_token_index = 0

    def _get_current_token(self):
        return self.POE_TOKENS[self.current_token_index]

    def _rotate_token(self):
        self.current_token_index = (self.current_token_index + 1) % len(self.POE_TOKENS)

    async def instruct(self, prompt, tokens: int = 0):
        while True:
            try:
                client = poe.Client(token=self._get_current_token())
                if self.AI_MODEL not in client.bot_names:
                    try:
                        self.AI_MODEL = client.get_bot_by_codename(self.AI_MODEL)
                    except:
                        raise Exception(f"Invalid AI Model: {self.AI_MODEL}")
                for chunk in client.send_message(chatbot=self.AI_MODEL, message=prompt):
                    pass
                response = chunk["text"].replace("\n", "\n")
                return response
            except Exception as e:
                self._rotate_token()

@app.post("/generate-response", response_model=PoeResponse)
async def generate_response(request: Request, message: Message):
    poe_provider = PoeProvider(POE_TOKENS=["token1", "token2", "token3"], AI_MODEL="chinchilla")
    response_text = await poe_provider.instruct(prompt=message.text)
    return JSONResponse(content={"response": response_text})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
