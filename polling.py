#polling.py

import logging
import asyncio
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from telegram.error import TelegramError
import random
import json
from datetime import date, time

logging.getLogger("httpx").setLevel(logging.WARNING)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

TOKEN = "7518139033:AAH75ac4lJmvoFLigs4A23LlTuCQXQVMTj4"
CHAT_ID = "8004855340"  # Your chat ID here

# Global variable to store the sent message's ID
sent_message_id = None
last_update_id = None

STREAK_FILE = "streak.json"

def load_streak():
    try:
        with open(STREAK_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {"streak": 0, "last_date": None}

def update_streak():
    streak_data = load_streak()
    today = date.today()
    last_date_str = streak_data.get("last_date")

    if last_date_str:
        last_date = date.fromisoformat(last_date_str)
        if today == last_date:
            # Already updated today
            return
        elif today == last_date + timedelta(days=1):
            streak_data["streak"] += 1
        else:
            streak_data["streak"] = 1  # reset streak
    else:
        streak_data["streak"] = 1  # first day

    streak_data["last_date"] = today.isoformat()
    save_streak(streak_data)

def save_streak(streak_data):
    with open(STREAK_FILE, "w") as f:
        json.dump(streak_data, f)


def load_workouts():
    with open("workouts\\cardio_hiit.txt", 'r') as file:
        cardio_hiit = file.read()
    with open("workouts\\core.txt", 'r') as file:
        core = file.read()
    with open("workouts\\flexibility.txt", 'r') as file:
        flexibility = file.read()
    with open("workouts\\pilates.txt", 'r') as file: #maybe remove this
        pilates = file.read()
    with open("workouts\\strength.txt", 'r') as file:
        strength = file.read()

    return [cardio_hiit, core, flexibility, pilates, strength]


def choose_msg_to_send(workouts: list):
    return random.choice(workouts)
    

async def send_message(message: str):
    global sent_message_id
    bot = Bot(token=TOKEN)
    try:
        sent_message = await bot.send_message(chat_id=CHAT_ID, text=message)
        sent_message_id = sent_message.message_id  # Save the sent message's ID
        logger.info(f"Message sent successfully with ID: {sent_message_id}")
    except TelegramError as e:
        logger.error(f"Failed to send message: {e}")

async def listen_for_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global sent_message_id
   
    # Check if the message is a reply to the previously sent message
    if update.message.reply_to_message and update.message.reply_to_message.message_id == sent_message_id:
        logger.info(f"Received reply: {update.message.text}")
        update_streak()
        await update.message.reply_text(str(load_streak())) #this will contain the number of days in your current streak, it will wait 24h

async def manual_polling(application: ContextTypes.DEFAULT_TYPE):
    """Manually poll for updates and process them"""
    global last_update_id

    while True:
        # Get updates from the Telegram API
        updates = await application.bot.get_updates(offset=last_update_id)
        for update in updates:
            # Process each update with the application handlers
            await application.process_update(update)
            # Update the last processed update ID
            last_update_id = update.update_id + 1
        await asyncio.sleep(1)  # Sleep for 1 second between requests

async def main(msg):
    # Create the application
    application = ApplicationBuilder().token(TOKEN).build()

    # Initialize the application 
    await application.initialize()

    # Add handlers for replies
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, listen_for_reply))

    # Send the initial message
    await send_message(msg)

    # Manually poll updates
    await manual_polling(application)

if __name__ == "__main__":
    workouts = load_workouts()
    msg = choose_msg_to_send(workouts)
    asyncio.run(main(msg))
