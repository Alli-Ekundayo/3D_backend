from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
import os
from dotenv import load_dotenv
import PIL.Image

load_dotenv()

# Retrieve API key from environment for better security
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

def image_generator(prompt):
    client = genai.Client(api_key="AIzaSyCPL0gY94xars0XwF1xSPA1L56iB7gc2dM")

    contents = ([prompt])

    response = client.models.generate_content(
        model="gemini-2.0-flash-exp-image-generation",
        contents=contents,
        config=types.GenerateContentConfig(
        response_modalities=['Text', 'Image']
        )
    )
    
    for part in response.candidates[0].content.parts:
        if part.text is not None:
            print(part.text)
        elif part.inline_data is not None:
            image = Image.open(BytesIO(part.inline_data.data))
            image_dir = os.path.join("3D's", "images")
            os.makedirs(image_dir, exist_ok=True)
            image_path = os.path.join(image_dir, "image.png")
            image.save(image_path)
            return image_path
        

def image_editor(image, edits):

    image = PIL.Image.open(image)

    client = genai.Client(api_key="AIzaSyCPL0gY94xars0XwF1xSPA1L56iB7gc2dM")

    text_input = (edits)

    response = client.models.generate_content(
        model="gemini-2.0-flash-exp-image-generation",
        contents=[text_input, image],
        config=types.GenerateContentConfig(
        response_modalities=['Text', 'Image']
        )
    )
    
    for part in response.candidates[0].content.parts:
        if part.text is not None:
            print(part.text)
        elif part.inline_data is not None:
            image = Image.open(BytesIO(part.inline_data.data))
            image_dir = os.path.join("3D's", "images")
            os.makedirs(image_dir, exist_ok=True)
            image_path = os.path.join(image_dir, "image.png")
            image.save(image_path)
            return image_path