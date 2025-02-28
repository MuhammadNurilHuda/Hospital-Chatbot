# app\chatbot.py

import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

client = OpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url="https://api.deepseek.com/v1"
)

async def get_response(user_input:str) -> str:
    response = await client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role" : "user", "content" : user_input}
        ]
    )

    return response.choices[0].message["content"]
