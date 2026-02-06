from fastapi import FastAPI
from fastapi.responses import JSONResponse, HTMLResponse, FileResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any
from session import Session
from time import perf_counter
import os

app = FastAPI(title="BarCloudTask API")

sessions = {}


class ChatRequest(BaseModel):
    """Chat request model."""
    session_id: str
    message: str
    context: Optional[Dict[str, Any]] = None

@app.post("/api/chat")
async def chat(request: ChatRequest):
    """Core chat API endpoint.

    Accepts a chat message with session_id and optional context.
    Returns the AI response and latency in milliseconds.
    """
    try:
        start = perf_counter()
        session = sessions.get(request.session_id)
        if not session:
            session = Session(request.session_id)
            sessions[request.session_id] = session
        query, answer, prompt_tokens, completion_tokens, total_tokens = session.call_user_message(request.message)
        end = perf_counter()
        latency_ms = (end - start) * 1000.0
        return JSONResponse({
            "natural_language_answer": answer,
            "sql_query": query,
            "token_usage": {
                "prompt_tokens": prompt_tokens,
                "completion_tokens": completion_tokens,
                "total_tokens": total_tokens
            },
            "provider": os.getenv("PROVIDER"),
            "latency_ms": round(latency_ms, 2),
            "status": "ok"
        })
    except Exception as e:
        return JSONResponse({
            "error": str(e),
            "status": "error"
        }, status_code=500)

@app.get("/")
async def root():
        """Serve the chat HTML file located at `static/chat.html`."""
        here = os.path.dirname(__file__)
        path = os.path.join(here, "static", "chat.html")
        return FileResponse(path, media_type='text/html')

