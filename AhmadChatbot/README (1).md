# Rumi — AI Chat Assistant

A chatbot powered by the Groq API (`openai/gpt-oss-20b`), available as both a
terminal app and a web chat interface.

## Setup

1. **Create and activate a virtual environment** (PowerShell):
   ```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

2. **Install dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```

3. **Add your API key:**
   - Copy `.env.example` to `.env`
   - Get a free API key from https://console.groq.com/keys
   - Paste it into `.env`:
     ```
     GROQ_API_KEY=your_actual_key_here
     ```

## Run the terminal version

```powershell
python main.py
```
- Type a message and press Enter.
- Type `reset` to clear history, `exit`/`quit` to stop.

## Run the web version

```powershell
python app.py
```
Then open **http://127.0.0.1:5000** in your browser (or on your phone if it's
on the same Wi-Fi, using your computer's local IP instead of 127.0.0.1).

## Project structure

```
AhmadChatbot/
├── core.py            # Shared chatbot logic (Groq API calls, history)
├── main.py             # Terminal chat interface
├── app.py               # Flask web server + chat API
├── templates/
│   └── index.html      # Chat page
├── static/
│   ├── style.css        # Rumi's dark navy / blue-purple gradient theme
│   └── script.js         # Chat UI behavior
├── requirements.txt
├── .env.example
├── .env                  # Your actual API key (not committed)
├── .gitignore
└── README.md
```

## Notes on the web version

- Conversation history is currently stored **in memory per browser session**
  and resets when the server restarts. That's fine for testing — swap in a
  real database (SQLite/Postgres) before you have real users.
- `app.secret_key` in `app.py` is a placeholder — change it to something
  random before deploying anywhere public.

## Next steps (toward the mobile app)

- The `/api/chat` and `/api/reset` endpoints in `app.py` are ready to be
  called from a native app (Flutter / React Native) instead of the bundled
  web page — the frontend and backend are already separated.
- Add user accounts + a real database to persist conversations per user.
- Deploy the Flask app (Render, Railway, Fly.io, etc.) and point the mobile
  app at the public URL.
- Add rate limiting / usage tracking if you plan to monetize.
