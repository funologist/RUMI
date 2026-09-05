"""
Rumi - AI Chat Assistant (terminal version)

Run:
    python main.py

Requires a .env file with GROQ_API_KEY set (see .env.example).
"""

from core import load_client, new_conversation, trim_history, get_response


def main():
    client = load_client()
    messages = new_conversation()

    print("=" * 50)
    print(" RUMI — AI Chat Assistant")
    print(" type 'exit' or 'quit' to stop, 'reset' to clear history")
    print("=" * 50)

    while True:
        try:
            user_input = input("\nYou: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            break

        if not user_input:
            continue

        if user_input.lower() in ("exit", "quit"):
            print("Goodbye!")
            break

        if user_input.lower() == "reset":
            messages = new_conversation()
            print("[Conversation history cleared]")
            continue

        messages.append({"role": "user", "content": user_input})
        messages = trim_history(messages)

        reply = get_response(client, messages)
        print(f"\nRumi: {reply}")

        messages.append({"role": "assistant", "content": reply})


if __name__ == "__main__":
    main()
