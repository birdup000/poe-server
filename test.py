import requests

url = "http://localhost:8080/generate-response"

payload = {"text": "Hello, how are you?"}

headers = {"Content-Type": "application/json"}

response = requests.post(url, json=payload, headers=headers)

print(response.json())
