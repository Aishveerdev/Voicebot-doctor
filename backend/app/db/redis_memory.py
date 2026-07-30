import logging

from app.db.supabase_db import get_chat_history
from app.db.redis_func import get_messages, rebuild_session

logger = logging.getLogger(__name__)


# here we keeping the same variable for both as its ultimately the same data just in different storage.
async def get_chat_context(session_id: str):
    logger.debug("get_chat_context called for session_id=%s", session_id)

    # Try to get from Redis first
    history = await get_messages(session_id)
    if history:
        logger.debug("chat history found in Redis for session_id=%s, entries=%d", session_id, len(history))
        return history

    logger.debug("no Redis history for session_id=%s, loading from DB", session_id)
    # If not in Redis, get from DB and rebuild Redis
    history = await get_chat_history(session_id)
    if history is not None:
        logger.debug("chat history loaded from DB for session_id=%s, entries=%d", session_id, len(history))
        await rebuild_session(session_id, history)
        logger.debug("Redis session rebuilt for session_id=%s", session_id)
        return history

    logger.debug("no chat history found for session_id=%s, returning empty list", session_id)
    return []