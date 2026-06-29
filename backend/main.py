from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
import os

from models import ChatRequest
from groq_client import stream_chat

app = FastAPI(title="Skipy API")

# Allow the frontend (even on a different origin during local dev) to call us.
# In production, since we serve the frontend from this same app, this is just a safety net.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten this to your real domain once deployed, if you split frontend/backend
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health_check():
    """Quick endpoint to confirm the server is alive."""
    return {"status": "ok", "service": "Skipy"}


@app.post("/api/chat")
def chat(request: ChatRequest):
    """
    Main chat endpoint. Receives the full conversation, streams Skipy's
    reply back token-by-token using Server-Sent-Events-style chunks.
    """
    messages = [{"role": m.role, "content": m.content} for m in request.messages]

    def event_generator():
        for chunk in stream_chat(messages):
            # Each chunk is sent as plain text; the frontend appends it live.
            yield chunk

    return StreamingResponse(event_generator(), media_type="text/plain")


# Serve the frontend (index.html, style.css, script.js) as static files.
# This means ONE deployment serves both the API and the UI.
frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend")
app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")
