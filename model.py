import requests
import openai
from . import API_KEY, BASE_URL, CONFIG_MODEL



def chat_model(prompt):
    client = openai.OpenAI(api_key=API_KEY,base_url=BASE_URL)
    
    response = client.chat.completions.create(
        model=CONFIG_MODEL,
        messages=[{'role':"user",'content':prompt}]
    )

    return response.choices[0].message.content