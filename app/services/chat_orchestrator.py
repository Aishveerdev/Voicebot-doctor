from app.services.process_image_query import analyze_query
from app.services.process_text_querry import process_text_query


async def orchestrate_chat(user, audio=None, image=None , session_id=None, request=None):
    
    if image:
        return await analyze_query(user, audio, image)
    else:
     return await process_text_query(user, session_id, request)