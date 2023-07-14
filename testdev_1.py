import requests

url = "http://localhost:8000/v1/chat/completions"

payload = {"text": "Hello, how are you?"}

headers = {"Content-Type": "application/json"}

response = requests.post(url, json=payload, headers=headers)

print(response.json())
