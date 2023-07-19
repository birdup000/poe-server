import openai

openai.api_key = "anyrandomstring"
openai.api_base = "https://api.greengecko.ml/v1"

response = openai.ChatCompletion.create(
    model='chinchilla',
    messages=[
        {'role': 'user', 'content': "Hello"},
    ]
)

print(response)
