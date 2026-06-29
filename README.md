# Skipy 🤖

A ChatGPT-style chat app powered by Groq's API.

## Project structure

```
skipy/
├── backend/
│   ├── main.py          # FastAPI app — routes + serves frontend
│   ├── groq_client.py   # Talks to Groq, handles streaming
│   ├── models.py         # Request/response data shapes
│   └── requirements.txt
├── frontend/
│   ├── index.html       # Chat UI
│   ├── style.css
│   └── script.js         # Sends messages, renders streamed replies
├── .env.example          # Template — copy to .env and add your real key
└── .gitignore
```

## 1. Run it locally

### Step 1 — Get a Groq API key
Go to https://console.groq.com/keys and create a key.

### Step 2 — Set up your environment file
In the project root (`skipy/`), copy the example file:

```bash
cp .env.example .env
```

Open `.env` and replace the placeholder with your real key:

```
GROQ_API_KEY=gsk_your_real_key_here
```

**Never commit `.env` to git or share it with anyone** — `.gitignore` is already set up to exclude it.

### Step 3 — Install dependencies
```bash
cd backend
pip install -r requirements.txt
```

### Step 4 — Run the server
```bash
uvicorn main:app --reload --port 8000
```

Open your browser to **http://localhost:8000** — Skipy should be live.

> Note: `main.py` loads `.env` from the project root via `python-dotenv`. Run uvicorn from inside `backend/` as shown above so the relative path to `.env` resolves correctly.

---

## 2. Deploy to Render (free tier works)

1. Push this whole `skipy/` folder to a GitHub repo (`.env` will NOT be pushed, thanks to `.gitignore` — that's correct and intentional).
2. Go to https://render.com → **New** → **Web Service** → connect your repo.
3. Configure:
   - **Root Directory**: `backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Under **Environment Variables**, add:
   - Key: `GROQ_API_KEY`
   - Value: *(paste your real key here — this is the one safe place to put it)*
5. Click **Deploy**. Render will give you a live URL like `https://skipy.onrender.com`.

That's it — one service, serving both the API and the chat UI.

---

## How it works (quick mental model)

```
Browser  --POST /api/chat-->  FastAPI (main.py)
                                    |
                                    v
                          groq_client.py --> Groq API
                                    |
                    (streams tokens back as they're generated)
                                    |
Browser  <--- streamed text --------
```

- Your Groq API key lives only on the server (`.env` locally, Render's env vars in production). The browser never sees it.
- Conversation history is kept in the browser's memory (a JS array) — refreshing the page clears it. No database, by design, to keep this simple. You can add persistence later (e.g. SQLite) if you want chats to survive a refresh.

## Customizing Skipy

- **Personality**: edit `SYSTEM_PROMPT` in `backend/groq_client.py`.
- **Model**: edit `MODEL_NAME` in the same file. Other Groq options include `llama-3.1-8b-instant` (faster, less capable).
- **Colors/branding**: edit the CSS variables at the top of `frontend/style.css`.
