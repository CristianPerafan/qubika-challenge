import os
import base64

import streamlit as st

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

def text_to_speech(input_text: str, message_id: str) -> str:
    filepath: str = f"audio/{message_id}.aac"
    with client.audio.speech.with_streaming_response.create(
            model="tts-1",
            voice="alloy",
            input=input_text,
            response_format='aac'
    ) as response:
        response.stream_to_file(filepath)

    return filepath

def verify_audio_exists(message_id: str) -> bool:
    filepath: str = f"audio/{message_id}.aac"
    return os.path.exists(filepath)

def get_audio_path(message_id: str) -> str:
    return f"audio/{message_id}.aac"

def autoplay_audio(file_path: str):
    with open(file_path, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode("utf-8")
        md = f"""
        <audio autoplay>
        <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
        </audio>
        """
        st.markdown(md, unsafe_allow_html=True)


