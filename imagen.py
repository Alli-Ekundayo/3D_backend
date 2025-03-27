from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
import base64
import PIL.Image
from dotenv import load_dotenv, find_dotenv


def image_generator(content):
    client = genai.Client()

    contents = (content)

    response = client.models.generate_content(
        model="gemini-2.0-flash-exp-image-generation",
        contents=contents,
        config=types.GenerateContentConfig(
        response_modalities=['Image']
        )
    )

    for part in response.candidates[0].content.parts:
        if part.text is not None:
            print(part.text)
        elif part.inline_data is not None:
            image = Image.open(BytesIO((part.inline_data.data)))
    return image

def image_editor(image_path, prompt):
    image = PIL.Image.open(image_path)

    client = genai.Client()

    text_input = (prompt)

    response = client.models.generate_content(
        model="gemini-2.0-flash-exp-image-generation",
        contents=[text_input, image],
        config=types.GenerateContentConfig(
        response_modalities=['Image']
        )
    )

    for part in response.candidates[0].content.parts:
        if part.text is not None:
            print(part.text)
        elif part.inline_data is not None:
            image = Image.open(BytesIO(part.inline_data.data))
        return image
    

