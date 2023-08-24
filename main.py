import openai
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import Optional
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())


app = FastAPI()

openai.api_type = "azure"

class ImageRequest(BaseModel):
    prompt: str
    style: Optional[str] = str | None
    n: int

def create_image_prompt(prompt: str):

    message_prompt = f'''
        Using this news article: "{prompt}" 
        Create a brief no longer than 50 words for an image that is suitable for the news story.
    '''

    response = openai.ChatCompletion.create(
                engine="gpt-35-turbo",
                temperature=0.7,
                api_version="2023-03-15-preview",
                api_base=os.getenv("CHAT_API_URL"),
                api_key=os.getenv("CHAT_API_KEY"),
                messages=[
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": message_prompt },
                ])

    return response["choices"][0]["message"]["content"]

@app.post("/img")
def get_image(image_req: ImageRequest):
    try: 
        amount = image_req.n
        image_prompt = ''

        if amount > 5 or amount < 1:
             raise Exception("n should be between 1 and 5")

        style = image_req.style if image_req.style else 'realistic'
        image_prompt = create_image_prompt(image_req.prompt)

        prompt = f'''
           {image_prompt}. The image should be in {style} style.
        '''

        response = openai.Image.create(
            api_version="2023-07-01-preview",
            api_base=os.getenv("API_URL"),
            api_key=os.getenv("API_KEY"),
            prompt=prompt,
            size='1024x1024',
            n=amount
        )

        return {"data": response["data"], "prompt": image_prompt}
        
    except Exception as e:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail={"prompt": image_prompt, "error": str(e)}
            )
