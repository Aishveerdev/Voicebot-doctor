from faster_whisper import WhisperModel

# load model once
model = WhisperModel("base",device="cpu")

async def transcribe_audio(audio_path):
    try:
        segments, info = model.transcribe(
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

        return patient_query_text
    except Exception as e:
        raise e

