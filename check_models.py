from google import genai

client = genai.Client(api_key="AIzaSyB81F6xeqnoT5KyicVaLY7Swe3sNxmDdGs")

models = client.models.list()

for model in models:
    print(model.name)