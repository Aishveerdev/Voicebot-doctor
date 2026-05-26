from gtts import gTTS
from playsound import playsound
from models import Medical_Response
import asyncio


async def speak_text(text ,  filename="response.mp3"):

    # convert text -> speech
    tts = gTTS(text=text,lang='en')
    # save audio
    tts.save(filename)
    print("Playing response...")
    # play audio
    await asyncio.to_thread(playsound, filename)