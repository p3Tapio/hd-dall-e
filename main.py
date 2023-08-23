import openai
from fastapi import FastAPI
from pydantic import BaseModel


openai.api_type = "azure"
openai.api_base = ""
openai.api_version = "2023-06-01-preview"
openai.api_key = ""

app = FastAPI()

class Request(BaseModel):
    prompt: str

@app.post("/img")
def get_image(prompt: Request):
    prompt_value = prompt.prompt 
    
    response = openai.Image.create(
        prompt=prompt_value,
        size='1024x1024',
        n=1
    )


    image_url = response["data"][0]["url"]
    return {"imageUrl": image_url}



