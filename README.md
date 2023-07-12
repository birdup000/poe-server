# Poe Server

This project is a FastAPI-based application that generates AI-generated responses using the Poe API.

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

3. Run the FastAPI server:

```shell
python server.py
`

The server will start and listen on `http://localhost:8000`.

## API Endpoints

### Generate AI Response

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
