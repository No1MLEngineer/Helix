import streamlit as st
import requests
import json

st.set_page_config(layout="wide", page_title="Helix AI", page_icon="🤖")

st.title("Helix AI 🤖")
st.caption("Your AI-powered content creation assistant")

with st.sidebar:
    st.header("About Helix AI")
    st.write("""
    Helix AI is a powerful tool that helps you generate trending hashtags, create engaging social media posts, and even generate videos for your products.
    """)
    st.write("---")
    st.header("How to use")
    st.write("""
    1. Enter your product name and description in the text boxes below.
    2. Click the buttons to generate hashtags, create a post, or generate a video.
    3. The generated content will appear on the right.
    """)

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
