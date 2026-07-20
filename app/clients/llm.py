import os
from PIL import Image
from google import genai
from app.models.schema import Medical_Response
from dotenv import load_dotenv
from app.core.gemini_retry import generate_with_retry



load_dotenv()




google_api_key = os.getenv("GOOGLE_API_KEY")

#initialize client
client = genai.Client(api_key=google_api_key)




async def ask_vision_model(image_path, query:str =None , prompt:str=None):

    async def call_fn():
     #load image
     image = Image.open(image_path)


     contents = [image]
     if query:
        contents.append(query)
    
      #CONFIG
     medical_config = {
        "response_mime_type": "application/json",
        "response_schema": Medical_Response
     }

   
     #generate response
     response = await client.aio.models.generate_content(
        model="gemini-3-flash-preview",
        contents=[image, query , prompt],
        config=medical_config
     )
     structured_output = response.parsed
     return structured_output  
    return await generate_with_retry(call_fn)                     




async def ask_language_model_strucutred(prompt:str) -> Medical_Response:

    async def call_fn():

     medical_config = {
        "response_mime_type": "application/json",
        "response_schema": Medical_Response
     }

     response = await client.aio.models.generate_content(
        model="gemini-2.5-flash",
        contents=[prompt] , 
        config=medical_config
     )
     structured_response = response.parsed
     return structured_response 
    return await generate_with_retry(call_fn)




async def ask_language_model_formal(prompt:str):
    async def call_fn():
     response = client.models.generate_content(
        model="gemini-2.5-flash" ,
        contents=[prompt]
     )
     return response.text
    return await generate_with_retry(call_fn)