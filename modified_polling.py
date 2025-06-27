import logging
import asyncio
import json
import random
from datetime import date, timedelta, time as dtime
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes
from telegram.error import TelegramError

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

TOKEN = "7518139033:AAH75ac4lJmvoFLigs4A23LlTuCQXQVMTj4"
USERS_FILE = "users.json"
STREAK_FILE = "streak.json"

def load_users():
    try:
        with open(USERS_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f)

def register_user(chat_id):
    users = load_users()
    if chat_id not in users:
        users.append(chat_id)
        save_users(users)
        logger.info(f"Registered new user: {chat_id}")

def load_streaks():
    try:
        with open(STREAK_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_streaks(streak_data):
    with open(STREAK_FILE, "w") as f:
        json.dump(streak_data, f)

def update_streak(chat_id):
    streak_data = load_streaks()
    today = date.today()
    user_streak = streak_data.get(str(chat_id), {"streak": 0, "last_date": None})

    last_date_str = user_streak.get("last_date")
    if last_date_str:
        last_date = date.fromisoformat(last_date_str)
        if today == last_date:
            return
        elif today == last_date + timedelta(days=1):
            user_streak["streak"] += 1
        else:
            user_streak["streak"] = 1
    else:
        user_streak["streak"] = 1

    user_streak["last_date"] = today.isoformat()
    streak_data[str(chat_id)] = user_streak
    save_streaks(streak_data)

def get_streak(chat_id):
    streak_data = load_streaks()
    return streak_data.get(str(chat_id), {"streak": 0, "last_date": None})["streak"]

def load_workouts():
    with open("workouts/cardio_hiit.txt", 'r') as file:
        cardio_hiit = file.read()
    with open("workouts/core.txt", 'r') as file:
        core = file.read()
    with open("workouts/flexibility.txt", 'r') as file:
        flexibility = file.read()
    with open("workouts/pilates.txt", 'r') as file:
        pilates = file.read()
    with open("workouts/strength.txt", 'r') as file:
        strength = file.read()
    return [cardio_hiit, core, flexibility, pilates, strength]

def choose_msg_to_send(workouts: list):
    return random.choice(workouts)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    register_user(chat_id)
    await update.message.reply_text("Welcome to fit-bot! You are now registered and will receive daily workouts.")

async def send_message(bot: Bot, chat_id: int, message: str):
    try:
        await bot.send_message(chat_id=chat_id, text=message)
        logger.info(f"Message sent to {chat_id}")
    except TelegramError as e:
        logger.error(f"Failed to send message to {chat_id}: {e}")

async def listen_for_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    update_streak(chat_id)
    streak = get_streak(chat_id)
    await update.message.reply_text(f"Congrats! Your current streak is {streak} days.")

async def broadcast_daily_workout(bot: Bot):
    workouts = load_workouts()
    msg = choose_msg_to_send(workouts)
    users = load_users()
    print("Message sent to all users")
    for chat_id in users:
        await send_message(bot, chat_id, msg)

async def manual_polling(application: ContextTypes.DEFAULT_TYPE, daily_broadcast_time=dtime(hour=18, minute=27, second=0)):
    global_last_update_id = None
    bot = application.bot

    # Calculate initial seconds until the next broadcast time
    import datetime
    def seconds_until_next_broadcast():
        now = datetime.datetime.now()
        target = daily_broadcast_time
        today_target = now.replace(hour=target.hour, minute=target.minute, second=target.second, microsecond=0)
        if now < today_target:
            delta = (today_target - now).total_seconds()
        else:
            # Next day
            tomorrow_target = today_target + datetime.timedelta(days=1)
            delta = (tomorrow_target - now).total_seconds()
        return delta

    # Schedule the next broadcast
    async def schedule_broadcast():
        while True:
            wait_time = seconds_until_next_broadcast()
            logger.info(f"Sleeping {wait_time} seconds until next daily workout broadcast")
            await asyncio.sleep(wait_time)
            await broadcast_daily_workout(bot)

    # Start the broadcast scheduler
    asyncio.create_task(schedule_broadcast())

    # Manual polling loop
    while True:
        updates = await bot.get_updates(offset=global_last_update_id)
        for update in updates:
            await application.process_update(update)
            global_last_update_id = update.update_id + 1
        await asyncio.sleep(1)

async def test_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await broadcast_daily_workout(context.bot)
    await update.message.reply_text("Test broadcast sent!")

async def main():
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, listen_for_reply))
    #application.add_handler(CommandHandler("test_broadcast", test_broadcast))
    
    await application.initialize()
    await application.start()
    await broadcast_daily_workout(application.bot)
    await manual_polling(application)  # This replaces run_polling() and idle()

if __name__ == "__main__":
    asyncio.run(main())
