from asyncio.log import logger
import os
from faster_whisper import WhisperModel

# load model once
model = WhisperModel("base",device="cpu")

async def transcribe_audio(audio):
    try:
        # SAVE AUDIO
        audio_path = f"temp_{audio.filename}"
        with open(audio_path, "wb") as f:
            f.write(await audio.read())
        logger.debug("Saved audio file to %s", audio_path)

        segments = model.transcribe(
            audio_path,
            beam_size=5,
            vad_filter=True
        )
        segments = list(segments)

        for segment in segments:
            print("Patient query:", segment.text)

        patient_query_text = " ".join(
            [segment.text for segment in segments]
        )

        
        # Delete temp audio file
        try:
            os.remove(audio_path)
            logger.debug("Deleted temp audio file %s", audio_path)
        except OSError as e:
            logger.error("Error occurred while deleting temp audio file %s: %s", audio_path, e)

        return patient_query_text
            
    except Exception as e:
        raise e

