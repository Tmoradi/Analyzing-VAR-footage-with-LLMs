import os
from dotenv import load_dotenv
from prompt import REFEREE_SYSTEM_PROMPT
from google.genai import Client , types
load_dotenv("../.env")
CLIENT = Client(api_key=os.getenv("GEMINI_API_KEY"))
MEDIA_TYPE = "video/quicktime"

def load_rules(fp) -> str:
    '''Here we are loading rules that were generated'''
    with open(fp,'r') as f: 
        file = f.read()
    return file

def load_var_footage(fp) -> bytes: 
    with open(fp, "rb") as video_file:
        video_data = video_file.read()
    return video_data

def analyzing_var_footage(video_fp):

    '''analyzing video footage for'''
    video_data = load_var_footage(video_fp) 
    rules = load_rules("rules.txt")
    response =  CLIENT.models.generate_content_stream(
    model='gemini-3-flash-preview',
    contents=[
            types.Part(inline_data=types.Blob(data=video_data,mime_type=MEDIA_TYPE)),
            types.Part(text=f"English Premier League Guidelines: {rules} "),
            types.Part(text=f"Based on the following rules and the video footage, would adjust the punishment of the player, or stick with your original decision?")
        ]
    ,
    config=types.GenerateContentConfig(
        system_instruction=REFEREE_SYSTEM_PROMPT,
        temperature=0
    ))
    response_text = ""
    for chunk in response: 
        response_text += chunk.text # type: ignore
        yield response_text
