import json
from app.core.redis_clieint import redis




async def add_message(session_id: str, role: str, content: str):

    
    key = f"chat:{session_id}"

    message = json.dumps({
        "role": role,
        "content": content})

    await redis.rpush (key,message)

    await redis.ltrim(key,-40,-1) # keep only last 40 messages for context , 20 conversation turns.

    await redis.expire(key, 60 * 60 * 24 * 7) # expire in 7 days


async def get_messages(session_id: str):

    key = f"chat:{session_id}"

    messages = await redis.lrange(key, 0, -1)

    return [json.loads(message) for message in messages]


async def clear_session(session_id: str):
    
    key = f"chat:{session_id}"

    await redis.delete(key)

async def rebuild_session(session_id: str,messages: list):

    key = f"chat:{session_id}"

    await redis.delete(key)

    if not messages:
        return

    serialized = [
        json.dumps(msg)
        for msg in messages
    ]

    await redis.rpush(key,*serialized)