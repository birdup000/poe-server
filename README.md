# Poe Server

This project is a FastAPI-based application that generates AI-generated responses using the Poe API (https://github.com/ading2210/poe-api).




## Project To-Do List

- [x] Token rotational
- [x] Proxy rotational
- [x] Add Streaming Support and make it compatible with Bettergpt.chat (Much thanks PaniniCo!!)
- [x] Add OPEN AI format of api like (/v1/chat/completions) use serverof.py for this
- [x] Work on Stability so not overloaded easily (rate limiting added)
- [ ] Add a retry logic if a model has reached daily limit
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

3. Define Proxy and Tokens inside the .env file
(Proxy is required)
if you don't define proxy you will have this error

Please follow this issue page to add proxy

```
tls_client.exceptions.TLSClientExeption: failed to build client out of request input: parse "socks5://user:pass@server:port": invalid port ":port" after host
```

[Proxy instructions]  https://github.com/greengeckowizard/poe-server/issues/3


4. Running the FastAPI Server Locally

You have two options for running the server: Using Python directly, or using Docker.

#### **Option A: Python**

To run the server with Python, execute the following command in your shell:

```shell
python server.py
```

#### **Option B: Docker**

To run the server with Docker, you need to build and start the Docker container. Run the following commands:

To change between using serverof (OpenAI format) change the line in the Dockerfile from serverof in this CMD ```["uvicorn", "serverof:app", "--host", "0.0.0.0", "--port", "8000"]``` to ```CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]``` then rebuild the dockerfile and you can docker-compose up. For running in Daemon mode use -d flag ``` docker-compose up -d ```

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


## API Endpoints

### Generate AI Response
use the server.py for this type of request
```

- **Endpoint**: `/generate-response`
- **Method**: POST
- **Request Body**:

    ```json
    {
        "message": {
            "text": "Your prompt message"
        }
    }
    ```

- **Response Body**:

    ```json
    {
        "response": "AI-generated response"
    }
    ```

```
You can make a request like this use the serverof.py to use this type request

```
import openai

openai.api_key = "anyrandomstring"
openai.api_base = "http://localhost:8000/v1"

response = openai.ChatCompletion.create(
    model='chinchilla',
    messages=[
        {'role': 'user', 'content': "Hello"},
    ]
)

print(response)
```

## Configuration

You can configure the project by providing the following environment variables (.env):

- `POE_TOKENS`: A comma-separated list of Poe API tokens.
- `PROXIES`: A comma-separated list of proxies.

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
see the [LICENSE](LICENSE) file for details.


## Credits

Thank you to PaniniCo for adding streaming support and model corresponding to names to Poe Models!!