# Generating a UI with gradio
import gradio as gr
from dotenv import load_dotenv
from google.genai import Client
import os

load_dotenv()
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

def genai_response(my_file, user_input, api_key=None):
    # Handle quit conditions
    if user_input and user_input.lower() in ['quit', 'q', 'exit']:
        return "# GoodBye..."
    
    # Use provided API key or default to environment variable
    if not api_key or api_key.strip() == "":
        api_key = GOOGLE_API_KEY
    
    # Basic validation
    if not api_key:
        return "**Error:** Please provide a valid Google API key."
    
    if not my_file:
        return "**Error:** Please upload an image file."
    
    if not user_input or user_input.strip() == "":
        return "**Error:** Please enter a question about the image."
    
    try:
        client = Client(api_key=api_key)
        uploaded_file = client.files.upload(file=my_file)
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=[uploaded_file, user_input]
        )
        return response.text
    
    except Exception as e:
        return f"**Error:** {str(e)}"

view = gr.Interface(
    fn=genai_response,
    inputs=[
        gr.Image(label="Upload an image...", type="filepath"),
        gr.Textbox(label="User Query", placeholder="Ask something about the image..."),
        gr.Textbox(label="API Key (optional)", placeholder="Leave empty to use default", type="password")
    ],
    outputs=gr.Markdown(label="AI Response"),
    title="🖼️ Gemini Image Analysis",
    description="Upload an image and ask questions about it using Google's Gemini AI.",
    theme=gr.themes.Soft()
).launch(share=True, debug=True)