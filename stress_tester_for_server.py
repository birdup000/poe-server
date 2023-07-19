import openai
import time
import concurrent.futures

openai.api_key = "anyrandomstring"
openai.api_base = "http://localhost:8000/v1"

def send_request():
    response = openai.ChatCompletion.create(
        model='chinchilla',
        messages=[
            {'role': 'user', 'content': "Hello"},
        ]
    )
    return response

def stress_test(num_requests=100):
    start_time = time.time()

    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        futures = [executor.submit(send_request) for _ in range(num_requests)]
        for future in concurrent.futures.as_completed(futures):
            try:
                print(future.result())
            except Exception as e:
                print(f"An error occurred: {e}")
  
    end_time = time.time()
    print(f"Time taken to send {num_requests} requests: {end_time - start_time} seconds")

if __name__ == "__main__":
    stress_test()