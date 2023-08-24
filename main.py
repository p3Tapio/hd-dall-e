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
    style: Optional[str] = None
    n: int

def create_image_prompt(prompt: str):

    message_prompt = f'''
        Read this article: "{prompt}".
        Then make a haiku about the article.
    '''

    response = openai.ChatCompletion.create(
                engine="gpt-35-turbo",
                temperature=1.2,
                api_version="2023-03-15-preview",
                api_base=os.getenv("CHAT_API_URL"),
                api_key=os.getenv("CHAT_API_KEY"),
                messages=[
                        {"role": "system", "content": "You are a poet."},
                        {"role": "user", "content": message_prompt },
                ])

    return response["choices"][0]["message"]["content"]

@app.post("/img")
def get_image(image_req: ImageRequest):
    try: 
        n = image_req.n
        prompt = ''

        if n > 5 or n < 1:
             raise Exception("n should be between 1 and 5")

        style = image_req.style if image_req.style else 'photorealistic'
        image_prompt = create_image_prompt(image_req.prompt)

        prompt = f'''
            {style} image:
           {image_prompt}. 
        '''

        response = openai.Image.create(
            api_version="2023-07-01-preview",
            api_base=os.getenv("API_URL"),
            api_key=os.getenv("API_KEY"),
            prompt=prompt,
            size='1024x1024',
            n=n
        )

        return {"data": response["data"], "prompt": prompt}
        
    except Exception as e:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail={"prompt": prompt, "error": str(e)}
            )
