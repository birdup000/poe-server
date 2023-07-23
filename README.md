# Poe Server

This project is a FastAPI-based application that generates AI-generated responses using the Poe API Wrapper (https://github.com/ading2210/poe-api).

# Project Status

![API Wrapper Status](https://img.shields.io/badge/API%20Wrapper-Broken-red)

## Details

Due to recent changes, our project may experience occasional downtimes linked to issues with a crucial API wrapper it depends on. This could lead to periods where the project does not function as expected.

Thankfully, you don't have to be in the dark about this. We're actively tracking these potential disruptions and will immediately update the operational status of the API wrapper on this README. This way, you can quickly check here to know if our project is currently up and running or facing some downtime.

We appreciate your understanding during this time. Rest assured, we're working diligently to ensure consistent functionality. Remember to check this space for the latest status updates.

Thank you for your patience.

last checked version:
```
poe-api 0.4.13
``` 


## Project To-Do List

- [x] Token rotational
- [x] Proxy rotational
- [x] Add Streaming Support and make it compatible with Bettergpt.chat (Much thanks PaniniCo!!)
- [x] Add OPEN AI format of api like (/v1/chat/completions) use serverof.py for this
- [x] Work on Stability so not overloaded easily (rate limiting added)
- [x] Add a retry logic and switch to a different token if a model has reached daily limit
- [ ] Add Anse Support (https://github.com/anse-app/anse)
- [ ] Add One-Api Support (https://github.com/songquanpeng/one-api)
- [ ] Add Embeddings to OPEN AI format (/api/v1/embedding)



## Installation

To install the project dependencies, run the following command:

```shell
pip install -r requirements.txt
```

## Getting Started

1. Clone the repository:

```shell
git clone https://github.com/greengeckowizard/poe-server
cd poe-server
```

2. Install the dependencies:

```shell
pip install -r requirements.txt
```

3. Define Proxy and Tokens inside the proxies.txt for the proxies and for the tokens put inside the tokens.txt file
(Proxy and Tokens are required to operate this Project WE DO NOT PROVIDE ANY PROXIES OR TOKENS UNDER ANY CIRCUMSTANCES)
<br>
if you don't define a proxy or token you will have errors. Note:Any of the proxies that work inside the poe-api will work in this project.
<br>

4. Running the FastAPI Server Locally

You have two options for running the server: Using Python directly, or using Docker.

#### **Option A: Python**

To run the server with Python, execute the following command in your shell:

```shell
python server.py
```
another
#### **Option B: Docker**

To run the server with Docker, you need to build and start the Docker container. Run the following commands:

```CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]``` then rebuild the dockerfile and you can docker-compose up. For running in Daemon mode use -d flag ``` docker-compose up -d ```

```shell
docker-compose build
docker-compose up
```

If you want the server to run in the background (daemonized), add the `-d` flag:

```shell
docker-compose up -d
```

After running these commands, the server will start and listen on the following URL:

```
http://localhost:8000
```
> **Important:** When interacting with the server locally via Docker, it's recommended to use the IP address assigned to your device instead of `http://localhost:8000`. For instance, if your local device's IP is `192.168.0.45`, the appropriate address to use would be `http://192.168.0.45:8000`.
#### **Finding Your Local IP Address**

To find your local IP address, run the following command:

- On Linux:

    ```shell
    ifconfig
    ```

- On Windows:

    ```shell
    ipconfig
    ```

- On MacOS:

    ```shell
    ifconfig | grep "inet " | grep -v 127.0.0.1
    ```

This command will display a list of all network interfaces. The `grep "inet "` command filters this list to include only entries that have an IP address (inet stands for internet). The second `grep -v 127.0.0.1` command excludes the loopback address, which is typically 127.0.0.1. The IP address you're likely interested in will most likely be the one associated with `en0` or `en1` - these are usually the primary Ethernet and Wi-Fi interfaces, respectively.

Remember, IP addresses that start with 192.168 or 10.0 are local addresses - they're only valid on your local network. If you're trying to give someone your IP address to connect to over the internet, you'll need your public IP address, which you can find by searching 'what is my IP' on Google or any other search engine.

## Model Mapping 

```
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
```



You can make a request like this use the server.py to use this type request

```
import openai

openai.api_key = "anyrandomstring"
openai.api_base = "http://localhost:8000/v1"

response = openai.ChatCompletion.create(
    model='gpt-3.5-turbo',
    messages=[
        {'role': 'user', 'content': "Hello"},
    ]
)

print(response)
```

## Configuration

You can configure the project by providing the following (set inside the text files):

- `Inside the tokens.txt`: A new line for each Poe API token.
- `Inside the proxies.txt`: A new line for each proxy server.

## Contributing

If you want to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch.
3. Make your changes.
4. Test your changes.
5. Commit your changes.
6. Push your changes to your forked repository.
7. Create a pull request.

## License

This project uses the [GNU General Public License v3.0]
see the [LICENSE](LICENSE) file for more details.


## Credits

Thank you to PaniniCo for adding streaming support and model corresponding to names to Poe Models!!
