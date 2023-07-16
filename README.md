# Poe Server

This project is a FastAPI-based application that generates AI-generated responses using the Poe API (https://github.com/ading2210/poe-api).




## Project To-Do List

for this project:

- [x] Token rotational (working but doesn't flip back in beginning the list after running out of tokens)
- [x] Add OPEN AI format of api like (/v1/chat/completions) use serverof.py for this.
- [ ] Work on Stability so not overloaded easily




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

3. Define Proxy and Tokens inside code
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

> **Note:** If you're accessing the server locally with Docker, use your local IP address instead of `localhost`. For example: `http://192.168.0.45`.

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

You can configure the project by providing the following environment variables:

- `POE_TOKENS`: A comma-separated list of Poe API tokens.
- `AI_MODEL`: The codename of the AI model to use.

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

See the [LICENSE](LICENSE) file for details.
