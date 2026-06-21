import os
import json
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
MEDIA_URL = os.getenv("MEDIA_URL")

BUTTON_1_TEXT = os.getenv("BUTTON_1_TEXT", "Channel 1")
BUTTON_1_URL = os.getenv("BUTTON_1_URL")
BUTTON_2_TEXT = os.getenv("BUTTON_2_TEXT", "Channel 2")
BUTTON_2_URL = os.getenv("BUTTON_2_URL")
MESSAGE_TEXT = os.getenv("MESSAGE_TEXT", "🔥 Tap below")

STATE_FILE = "state.json"


def load_last_message_id():
    try:
        with open(STATE_FILE, "r") as f:
            return json.load(f).get("last_message_id")
    except:
        return None


def save_last_message_id(message_id):
    with open(STATE_FILE, "w") as f:
        json.dump({"last_message_id": message_id}, f)


async def post_message(context: ContextTypes.DEFAULT_TYPE):
    old_message_id = load_last_message_id()

    if old_message_id:
        try:
            await context.bot.delete_message(
                chat_id=CHANNEL_ID,
                message_id=old_message_id
            )
            print(f"Deleted old message: {old_message_id}")
        except Exception as e:
            print(f"Could not delete old message: {e}")

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(BUTTON_1_TEXT, url=BUTTON_1_URL),
            InlineKeyboardButton(BUTTON_2_TEXT, url=BUTTON_2_URL),
        ]
    ])

    msg = await context.bot.send_animation(
        chat_id=CHANNEL_ID,
        animation=MEDIA_URL,
        caption=MESSAGE_TEXT,
        reply_markup=keyboard
    )

    save_last_message_id(msg.message_id)
    print(f"Sent new message: {msg.message_id}")


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.job_queue.run_repeating(
        post_message,
        interval=300,
        first=5,
        name="auto_post"
    )

    print("Bot started. Posting every 5 minutes.")
    app.run_polling()


if __name__ == "__main__":
    main()
