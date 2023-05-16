import os
import telegram
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater, ConversationHandler, CallbackContext


TELEGRAM_API_TOKEN = os.getenv('TELEGRAM_API_TOKEN')
PORT = int(os.environ.get('PORT', '8443'))
APP_URL = os.environ.get("APP_URL")


def process_message(update, context):
    message_text = update.message.text
    if "SELL GOLD SIGNAL" in message_text or "BUY GOLD SIGNAL" in message_text:
        is_sell_signal = "SELL GOLD SIGNAL" in message_text

        # Extract relevant information from the message
        entry = message_text.split("Entry: ")[1].split("\n")[0]
        tp1 = message_text.split("TP1: ")[1].split("\n")[0]
        tp2 = message_text.split("TP2: ")[1].split("\n")[0]
        sl = message_text.split("SL: ")[1].split("\n")[0]

        # Generate the formatted signal
        signal_type = "SELL" if is_sell_signal else "BUY"
        signal = f"{signal_type} STOP XAUUSD\nEntry {entry}\nSL {sl}\nTP {tp1}\nTP {tp2}"

        # Send the signal as a reply
        context.bot.send_message(chat_id=update.effective_chat.id, text=signal)

def main():

    # get the dispatcher to register handlers
    updater = Updater(TELEGRAM_API_TOKEN, use_context=True)

    dp = updater.dispatcher


    # Register the message handler
    dp.add_handler(MessageHandler(Filters.text, process_message))

    # Start the bot
    updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=TELEGRAM_API_TOKEN, webhook_url=APP_URL + TELEGRAM_API_TOKEN)

    updater.idle()

if __name__ == '__main__':
    main()
