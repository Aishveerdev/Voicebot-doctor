from asyncio.log import logger
from app.services.process_image_query import analyze_query
from app.services.process_text_querry import process_text_query
from app.services.query_preprocessing import preprocess_query
from app.services.supabase_db import create_chat_session , get_chat_session


async def orchestrate_chat(user, audio=None, text_query=None, image=None, session_id=None):
    
    if session_id is None:
        # Create chat session if session_id is not provided (new conversation)
        session_id = await create_chat_session(user.id)
        logger.info("Creating chat session for user_id=%s", user.id)
        
    elif session_id is not None:
        session = await get_chat_session(session_id) 
        logger.debug("Fetched session for session_id=%s -> %s", session_id, getattr(session, 'id', None) if session else None)
        logger.info("Existing session_id=%s provided, processing query in context of this session", session_id)
    
    else:
        raise ValueError("Invalid session_id provided")
    logger.info("invalid session_id provided by user_id=%s, session_id=%s", user.id, session_id)


    # Preprocess query to get patient_query
    patient_query = await preprocess_query(audio=audio, text_query=text_query)
    if image:
         return await analyze_query(user=user,image=image ,patient_query=patient_query, session_id=session_id)
    elif image is None:
          return await process_text_query(user=user, patient_query=patient_query, session_id=session_id)
    else:
          raise ValueError("Invalid query: No input provided")












# FOR NOW , IF A REPORT IS CREATED , USER CANT ADD IMAGE LATER , FOR THAT HE HAD TO START NEW CHAT/SESSION 
    # IN FUTURE WE CAN ALLOW USER TO ADD IMAGE LATER IN THE SAME SESSION AS WELL , FOR THAT WE NEED TO CHECK IF REPORT IS CREATED OR NOT , IF REPORT IS CREATED THEN WE CAN ALLOW USER TO ADD IMAGE AND THEN UPDATE THE REPORT WITH NEW IMAGE ANALYSIS AND THEN PROVIDE UPDATED RESPON        # Get session
   