from app.services.speech_to_text import transcribe_audio


async def preprocess_query(audio=None, text_query=None):
    # Preporcessing query and passing only as patient query to the respective function.
    if audio :
        patient_query = await transcribe_audio(audio)  
    else:    
        patient_query = text_query

    return patient_query