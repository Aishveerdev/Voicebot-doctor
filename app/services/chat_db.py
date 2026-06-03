from app.core.supabase_client import supabase


# Chat sesison
async def create_chat_session(user_id: str,report_id: str):
    
    response = ( supabase.table("chat_session").insert({
        "user_id": user_id,
        "report_id": report_id
    })
    .execute()
    )
    return response.data[0]["id"] 

# Get session by id , this is created because through this 
async def get_chat_session(session_id: str):
    response = (supabase.table("chat_session")
                .select("*")
                .eq("id", session_id)
                .execute()
    )
    return response.data[0] if response.data else None

# Chat message
async def save_message(session_id: str,role: str,content: str):
    response = ( supabase.table("chat_message").insert({
        "session_id": session_id,
        "role": role,
        "content": content
    })
    .execute()
    )
    return response.data[0]


async def get_chat_history(session_id: str):
    response = (supabase.table("chat_message")
                .select("role,content")
                .eq("session_id", session_id)
                .order("created_at")
                .execute()
    )
    return response.data