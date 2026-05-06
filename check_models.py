from google import genai

client = genai.Client(api_key="API_KEY")

models = client.models.list()

for model in models:
    print(model.name)
