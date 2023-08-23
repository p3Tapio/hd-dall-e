import openai
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

openai.api_type = "azure"
openai.api_base = os.getenv("API_URL")
openai.api_version = "2023-06-01-preview"
openai.api_key = os.getenv("API_KEY")

app = FastAPI()

class Request(BaseModel):
    prompt: str
    n: int

@app.post("/img")
def get_image(prompt: Request):
    prompt_value = prompt.prompt 
    amount = prompt.n
    
    response = openai.Image.create(
        prompt=prompt_value,
        size='1024x1024',
        n=amount
    )

    return {"data": response["data"]}



