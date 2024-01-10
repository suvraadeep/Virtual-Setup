import google.generativeai as genai 
import os 
import streamlit as st 
from PIL import Image 
from dotenv import load_dotenv
load_dotenv()

genai.configure(api_key=os.getenv("google_api_key"))

def output(input,image,prompt):
    model=genai.GenerativeModel("gemini-pro-vision")
    response=model.generate_content([input,image[0],prompt])
    return response.text

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()
        image_parts =[
        {
        "mime_type": uploaded_file.type, # Get the mime type of the uploaded file
        "data": bytes_data
        }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")
    
st.set_page_config(page_title="Analyze the Image")
st.header("Upload your image and ask questions")
uploaded_file=st.file_uploader("Upload Your Image",type=["jpg","jpeg","png"])

image=""
if uploaded_file is not None:
    image=Image.open(uploaded_file)
    st.image(image,caption="uploaded image",use_column_width=True)

question=st.text_input("Ask a Question")
inputp="""
You're an expert in reading text on images.
I will give you a Image and ask a question.
You carefully go through the Image and answer my Question
"""

submit=st.button("Ask Question")

if submit:
    img_dat=input_image_setup(uploaded_file)
    ans=output(inputp,img_dat,question)
    st.subheader("The Response is")
    st.write(ans)