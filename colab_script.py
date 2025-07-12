# Install dependencies
!pip install fastapi uvicorn python-multipart transformers torch sentencepiece streamlit requests pyngrok

# Create backend directory and files
!mkdir -p backend
with open("backend/main.py", "w") as f:
    f.write("""
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
""")

# Create frontend directory and files
!mkdir -p frontend
with open("frontend/app.py", "w") as f:
    f.write("""
import streamlit as st
import requests
import json

st.set_page_config(layout="wide", page_title="Helix AI", page_icon="🤖")

st.title("Helix AI 🤖")
st.caption("Your AI-powered content creation assistant")

with st.sidebar:
    st.header("About Helix AI")
    st.write("
    Helix AI is a powerful tool that helps you generate trending hashtags, create engaging social media posts, and even generate videos for your products.
    ")
    st.write("---")
    st.header("How to use")
    st.write("
    1. Enter your product name and description in the text boxes below.
    2. Click the buttons to generate hashtags, create a post, or generate a video.
    3. The generated content will appear on the right.
    ")

col1, col2 = st.columns(2)

with col1:
    st.header("Product Details")
    product_name = st.text_input("Product Name")
    product_description = st.text_area("Product Description")

    if st.button("Generate Hashtags"):
        if product_name and product_description:
            with st.spinner("Generating hashtags..."):
                response = requests.post("http://127.0.0.1:8000/generate_hashtags", json={"name": product_name, "description": product_description})
                if response.status_code == 200:
                    hashtags = response.json()["hashtags"]
                    st.session_state.hashtags = hashtags
                else:
                    st.error("Error generating hashtags. Please try again.")
        else:
            st.warning("Please enter a product name and description.")

    if st.button("Create Post"):
        if product_name and product_description:
            with st.spinner("Creating post..."):
                response = requests.post("http://127.0.0.1:8000/create_post", json={"name": product_name, "description": product_description})
                if response.status_code == 200:
                    post = response.json()["post"]
                    st.session_state.post = post
                else:
                    st.error("Error creating post. Please try again.")
        else:
            st.warning("Please enter a product name and description.")

    if st.button("Generate Video"):
        if product_name and product_description:
            with st.spinner("Generating video..."):
                response = requests.post("http://127.0.0.1:8000/generate_video", json={"name": product_name, "description": product_description})
                if response.status_code == 200:
                    message = response.json()["message"]
                    st.session_state.video_message = message
                else:
                    st.error("Error generating video. Please try again.")
        else:
            st.warning("Please enter a product name and description.")

with col2:
    st.header("Generated Content")
    if "hashtags" in st.session_state:
        st.subheader("Hashtags")
        st.write(st.session_state.hashtags)
    if "post" in st.session_state:
        st.subheader("Post")
        st.write(st.session_state.post)
    if "video_message" in st.session_state:
        st.subheader("Video")
        st.info(st.session_state.video_message)
""")

# Run backend
import subprocess
process = subprocess.Popen(["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"])

# Expose backend with ngrok
from pyngrok import ngrok
public_url = ngrok.connect(8000)
print(f"Backend is running at: {public_url}")

# Run frontend
!streamlit run frontend/app.py --server.port 8501
