import requests

from config.config import Config


def get_chat_id():
    bot_token = Config.TELEGRAM_BOT_TOKEN

    url = f"https://api.telegram.org/bot{bot_token}/getUpdates"

    print("Instructions:")
    print("1. Start a conversation with your bot on Telegram")
    print("2. Send any message to the bot (like /start)")
    print("3. Run this script to get your chat ID")
    print()

    try:
        response = requests.get(url, timeout=10)
        data = response.json()

        if data.get("ok"):
            updates = data.get("result", [])
            if updates:
                for update in updates[-5:]:
                    if "message" in update:
                        chat = update["message"]["chat"]
                        print(
                            f"Chat ID: {chat['id']} | Type: {chat['type']} | Name: {chat.get('first_name', 'N/A')}"
                        )
            else:
                print("No messages found. Make sure you've sent a message to the bot first!")
        else:
            print(f"Error: {data.get('description')}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    get_chat_id()
