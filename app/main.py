# main.py

import os
import time
import uvicorn
import asyncio
from fastapi import FastAPI, HTTPException, Header, Depends
from pydantic import BaseModel, HttpUrl
from typing import List, Optional
from config import settings
from rag.rag_system import generate_prompts
from generator.llm import call_gemini_api

app = FastAPI(title="Insurance RAG QA Service")

# ─── Schemas ──────────────────────────────────────────────────────────────────

class QueryRequest(BaseModel):
    documents: str # ❗ change from List[HttpUrl] to List[str]
    questions: List[str]

class QueryResponse(BaseModel):
    answers: List[str]

# ─── Auth Dependency ───────────────────────────────────────────────────────────
def verify_token(authorization: str = Header(...)) -> None:
    """
    Verifies the Bearer token in the Authorization header.
    Equivalent to the JS authMiddleware function.
    """
    scheme, _, token = authorization.partition(" ")

    if scheme.lower() != "bearer" or token != settings.AUTH_TOKEN:
        raise HTTPException(
            status_code=403,
            detail="Invalid authentication token."
        )
    

@app.get("/", tags=["demo"])
def hello():
    return {"msg": "Use POST /api/v1/hackrx/run to submit your questions."}

# ─── Health Check ─────────────────────────────────────────────────────────────
@app.get("/health", tags=["health"])
async def health():
    return {"status": "ok", "message": "Service is running."}

# ─── RAG Endpoint with Retry Logic ────────────────────────────────────────────
@app.post(
    "/api/v1/hackrx/run",
    response_model=QueryResponse,
    dependencies=[Depends(verify_token)],
    tags=["query"]
)
async def run_hackrx(req: QueryRequest):
    # Validate input
    if not req.questions:
        raise HTTPException(status_code=400, detail="`questions` must be a non-empty list.")
    
    docs = req.documents if req.documents else ""
    attempts = 0

    while attempts < settings.MAX_RETRIES:
        try:
            # 1) Generate prompts (this will also index any new docs)
            prompts = generate_prompts(docs, req.questions)

            # 2) Call your LLM here for each prompt.
            #    Replace the placeholder below with a real API call to Gemini/GPT.
            answers: List[str] = []
            # for prompt in prompts:
            #     # e.g. answer = await call_gemini_api(prompt)
            #     answers.append(prompt)  # placeholder
            # #print("Generated answers:", answers)
            # return QueryResponse(answers=answers)
            # Fire off all Gemini calls in parallel
            # (adjust concurrency if needed to avoid rate limits)
            tasks = [call_gemini_api(prompt) for prompt in prompts]
            try:
                answers = await asyncio.gather(*tasks)
            except Exception as e:
                # handle errors in one or more calls
                raise HTTPException(status_code=500, detail=f"LLM error: {e}")

            # Clean up numbering if any
            answers = [ans.lstrip("0123456789. ").strip() for ans in answers]

            return QueryResponse(answers=answers)

        except Exception as e:
            attempts += 1
            is_retryable = attempts < settings.MAX_RETRIES
            if not is_retryable:
                raise HTTPException(status_code=500, detail=str(e))
            
            delay = settings.INITIAL_RETRY_DELAY_MS * (2 ** (attempts - 1)) / 1000.0
            time.sleep(delay)

# ─── Entry Point ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.getenv("PORT", 8000)), reload=True)
