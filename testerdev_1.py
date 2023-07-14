from fastapi.testclient import TestClient
import json

# Import your FastAPI application
from servertest import app

client = TestClient(app)

def test_chat_completions():
    response = client.post(
        "/v1/chat/completions",
        data=json.dumps({
            "model": "chinchilla",
            "messages": [
                {"role": "user", "content": "Hello"}
            ]
        }),
        headers={"Content-Type": "application/json"}
    )

    assert response.status_code == 200

    # Add more assertions here to check the response body, etc.

    # For example, to check that the response body contains a 'response' key:
    assert 'response' in response.json()

if __name__ == "__main__":
    test_chat_completions()