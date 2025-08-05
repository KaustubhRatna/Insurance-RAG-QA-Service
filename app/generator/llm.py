# embedder/llm.py

import asyncio
import httpx
from fastapi import HTTPException
from typing import Optional
from config import settings

GEMINI_QNA_URL = (
    f"{settings.GEMINI_API_BASE_URL}"
    f"{settings.GEMINI_QNA_MODEL}:generateContent"
)

async def call_gemini_api(
    prompt: str,
    timeout: Optional[float] = 120.0,
    max_retries: int = 3,
    backoff_factor: float = 1.0
) -> str:
    """
    Sends the prompt to Gemini. Retries on 5xx errors with exponential backoff.
    """
    api_key = settings.GEMINI_API_KEY
    if not api_key:
        raise HTTPException(status_code=500, detail="GEMINI_API_KEY not configured")

    headers = {
        "Content-Type": "application/json",
        "X-goog-api-key": api_key,
    }
    payload = { "contents": [{ "parts": [{"text": prompt}] }] }

    for attempt in range(1, max_retries + 1):
        try:
            async with httpx.AsyncClient(timeout=timeout) as client:
                resp = await client.post(GEMINI_QNA_URL, json=payload, headers=headers)
                resp.raise_for_status()
                data = resp.json()
            # Extract text safely
            return (
                data.get("candidates", [{}])[0]
                    .get("content", {})
                    .get("parts", [{}])[0]
                    .get("text", "")
            ).strip()

        except httpx.HTTPStatusError as e:
            status = e.response.status_code
            # Retry on 5xx
            if 500 <= status < 600 and attempt < max_retries:
                delay = backoff_factor * (2 ** (attempt - 1))
                await asyncio.sleep(delay)
                continue
            # For client errors or final failure, raise
            raise HTTPException(
                status_code=502,
                detail=f"Gemini API error: {status} {e.response.text}"
            )
        except (httpx.TransportError, asyncio.TimeoutError) as e:
            # Network or timeout error: retry if attempts remain
            if attempt < max_retries:
                delay = backoff_factor * (2 ** (attempt - 1))
                await asyncio.sleep(delay)
                continue
            raise HTTPException(status_code=504, detail=f"Gemini request failed: {e}")

    # Should never reach here
    raise HTTPException(status_code=500, detail="Unknown Gemini integration error")
