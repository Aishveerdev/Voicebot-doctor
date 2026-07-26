# app/utils/gemini_retry.py

import asyncio
from google.genai.errors import ServerError

async def generate_with_retry(model, prompt, max_retries=5):
    for attempt in range(max_retries):
        try:
            return await model.generate_content(prompt)

        except ServerError as e:
            if getattr(e, "status_code", None) == 503:
                wait_time = 2 ** attempt
                print(f"Gemini overloaded. Retrying in {wait_time}s...")
                await asyncio.sleep(wait_time)
            else:
                raise

    raise Exception("Gemini unavailable after maximum retries")