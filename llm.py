import os
from PIL import Image
from google import genai
from models import Medical_Response
from dotenv import load_dotenv

load_dotenv()

google_api_key = os.getenv("GOOGLE_API_KEY")


async def ask_vision_model(image_path, query):

    
    #load image
    image = Image.open(image_path)

    #initialize model
    client = genai.Client(api_key=google_api_key)

    #CONFIG
    medical_config = {
        "response_mime_type": "application/json",
        "response_schema": Medical_Response
    }


    #generate response
    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=[image, query],
        config=medical_config
    )

    structured_output = response.parsed
    
    return structured_output                       
