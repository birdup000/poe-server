import requests

url = "http://10.144.22.98:8080/generate-response"

payload = {"text": "Hello, how are you?"}

headers = {"Content-Type": "application/json"}

response = requests.post(url, json=payload, headers=headers)

print(response.json())