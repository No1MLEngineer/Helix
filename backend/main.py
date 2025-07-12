from fastapi import FastAPI

app = FastAPI()

from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from transformers import pipeline
import torch

app = FastAPI()

# Load models
hashtag_generator = pipeline("text-generation", model="HuggingFaceH4/zephyr-7b-beta")
post_generator = pipeline("text-generation", model="HuggingFaceH4/zephyr-7b-beta")
# For video generation, we'll use a placeholder as it's a more complex task
# and requires specialized models and libraries.
# video_generator = pipeline("text-to-video", model="damo-vilab/text-to-video-ms-1.7b")

class Product(BaseModel):
    name: str
    description: str

@app.post("/generate_hashtags")
async def generate_hashtags(product: Product):
    prompt = f"Generate 5 trending hashtags for a product named {product.name} with description: {product.description}"
    hashtags = hashtag_generator(prompt, max_length=50, num_return_sequences=1)
    return {"hashtags": hashtags[0]['generated_text']}

@app.post("/create_post")
async def create_post(product: Product):
    prompt = f"Create a social media post for a product named {product.name} with description: {product.description}"
    post = post_generator(prompt, max_length=280, num_return_sequences=1)
    return {"post": post[0]['generated_text']}

@app.post("/generate_video")
async def generate_video(product: Product):
    # This is a placeholder for video generation.
    # In a real-world application, this would involve a more complex pipeline
    # with a model like Damo-vilab's text-to-video.
    return {"message": "Video generation is not yet implemented."}

@app.get("/")
def read_root():
    return {"message": "Welcome to the Helix AI API"}
