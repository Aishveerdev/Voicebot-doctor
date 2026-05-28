from gtts import gTTS
from playsound import playsound
from app.models.schema import Medical_Response
import asyncio


def speak_text(text ,  filename="response.mp3"):

    # convert text -> speech
    tts = gTTS(text=text,lang='en')
    # save audio
    tts.save(filename)

    return filename