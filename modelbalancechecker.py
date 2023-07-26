import poe
import concurrent.futures
from tqdm import tqdm

# MODEL_MAPPING as per your provided list
MODEL_MAPPING = {
    "assistant": "capybara",
    "claude-instant": "a2",
    "claude-2-100k": "a2_2",
    "claude-instant-100k": "a2_100k",
    "gpt-3.5-turbo-0613": "chinchilla",
    "gpt-3.5-turbo": "chinchilla",
    "gpt-3.5-turbo-16k-0613": "agouti",
    "gpt-3.5-turbo-16k": "agouti",
    "gpt-4": "beaver",
    "gpt-4-0613": "beaver",
    "gpt-4-32k": "vizcacha",
    "chat-bison-001": "acouchy",
}

def load_from_file(file_path: str) -> list:
    with open(file_path, "r") as file:
        items = [item.strip() for item in file.readlines() if item.strip()]
    return items

# Load the POE_TOKENS from a file called "tokens.txt"
POE_TOKENS_FILE = "tokens.txt"
POE_TOKENS = load_from_file(POE_TOKENS_FILE)

# Load the PROXIES from a file called "proxies.txt"
PROXY_LIST_FILE = "proxies.txt"
PROXIES = load_from_file(PROXY_LIST_FILE)

current_proxy_index = 0

def check_remaining_messages(token, proxy, model):
    client = poe.Client(token=token, proxy=proxy)
    remaining_messages = client.get_remaining_messages(model)
    return remaining_messages if remaining_messages is not None else 0

for model in MODEL_MAPPING.values():
    total_remaining_messages = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(check_remaining_messages, token, PROXIES[i % len(PROXIES)], model): token for i, token in enumerate(POE_TOKENS)}
        for future in tqdm(concurrent.futures.as_completed(futures), total=len(futures), desc=f"Processing {model}"):
            total_remaining_messages += future.result()
    print(f"Model: {model}, Total Remaining Messages: {total_remaining_messages}")