import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()  # reads .env file into environment variables

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise RuntimeError(
        "GROQ_API_KEY not found. Did you create a .env file with your key in it? "
        "See .env.example for the format."
    )

client = Groq(api_key=GROQ_API_KEY)

# Single place to change the model later
MODEL_NAME = "llama-3.3-70b-versatile"

# Skipy's personality / identity
SYSTEM_PROMPT = (
    "You are Skipy, a helpful, friendly, and knowledgeable AI assistant. "
    "You communicate clearly and concisely, but you're happy to go deep when "
    "the user wants detail. You have a warm, approachable personality."
)


def stream_chat(messages: list[dict]):
    """
    Takes a list of {role, content} dicts (the conversation so far)
    and yields text chunks as Groq generates them.
    """
    # Prepend Skipy's system prompt so it always knows who it is
    full_messages = [{"role": "system", "content": SYSTEM_PROMPT}] + messages

    stream = client.chat.completions.create(
        model=MODEL_NAME,
        messages=full_messages,
        temperature=0.7,
        max_tokens=2048,
        stream=True,
    )

    for chunk in stream:
        delta = chunk.choices[0].delta.content
        if delta:
            yield delta
