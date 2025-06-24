#bot.py

from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, CallbackContext, Updater
from telegram.error import TelegramError
import logging
#import asyncio

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

TOKEN = "7518139033:AAH75ac4lJmvoFLigs4A23LlTuCQXQVMTj4"

CHAT_ID = "8004855340"

sent_message_id = None


def send_message(message):
    global sent_message_id
    
    bot = Bot(token=TOKEN)
    try:
        sent_message =  bot.send_message(chat_id=CHAT_ID, text=message)
        sent_message_id = sent_message.message_id  # Save the sent message's ID
        logger.info(f"Message sent successfully with ID: {sent_message_id}")
    except TelegramError as e:
        logger.error(f"Failed to send message: {e}")


def listen_for_reply(update: Update, context: CallbackContext):
    global sent_message_id

    # Check if the message is a reply to the previously sent message
    if update.message.reply_to_message and update.message.reply_to_message.message_id == sent_message_id:
        # The message is a reply to the one we sent earlier
        logger.info(f"Received reply: {update.message.text}")
        # You can now respond to the user or handle the reply as needed
        update.message.reply_text("Thank you for your reply!")



def main():
    #updater = Updater(TOKEN, use_context=True)
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, listen_for_reply))
    
    send_message("Hello, please reply to this message!")
    updater.start_polling()
    updater.idle()


    
if __name__ == "__main__":
    main()
    #main()
    #asyncio.run(send_message("Hello, this is a message from fitness-bot."))

#async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    #await update.message.reply_text(f'Hello {update.effective_user.first_name}')


#app = ApplicationBuilder().token(TOKEN).build()

#app.add_handler(CommandHandler("hello", hello))

#app.run_polling()
