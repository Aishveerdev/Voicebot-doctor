from redis.asyncio import Redis
from dotenv import load_dotenv
import os

load_dotenv()



redis = Redis(
    host=os.getenv("REDIS_HOST"),
    port=int(os.getenv("REDIS_PORT")),
    decode_responses=True
)