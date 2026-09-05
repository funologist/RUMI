"""
app.py - Flask web server for Rumi.

Run:
    python app.py

Then open http://127.0.0.1:5000 in your browser.
Requires a .env file with GROQ_API_KEY set (see .env.example).
"""

import uuid
from flask import Flask, render_template, request, jsonify, session

from core import load_client, new_conversation, trim_history, get_response

app = Flask(__name__)
app.secret_key = "rumi-dev-secret-change-me"  # replace before deploying publicly

client = load_client()

# In-memory store: { session_id: [messages] }
# NOTE: resets when the server restarts. Fine for local dev / prototyping.
# Swap for a real database (SQLite/Postgres) before shipping to real users.
conversations = {}


def get_session_id() -> str:
    if "sid" not in session:
        session["sid"] = str(uuid.uuid4())
    return session["sid"]


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    user_message = (data.get("message") or "").strip()

    if not user_message:
        return jsonify({"error": "Empty message"}), 400

    sid = get_session_id()
    messages = conversations.get(sid) or new_conversation()

    messages.append({"role": "user", "content": user_message})
    messages = trim_history(messages)

    reply = get_response(client, messages)
    messages.append({"role": "assistant", "content": reply})

    conversations[sid] = messages

    return jsonify({"reply": reply})


@app.route("/api/reset", methods=["POST"])
def reset():
    sid = get_session_id()
    conversations[sid] = new_conversation()
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
