import requests

url = "http://localhost:8000/generate-response"
payload = {"text": "Hello, how are you?"}
headers = {"Content-Type": "application/json"}

num_requests = 100  # Change this to the desired number of requests

for _ in range(num_requests):
    response = requests.post(url, json=payload, headers=headers)
    print(response.json())
