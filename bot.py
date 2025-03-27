import telebot
import requests
import logging
from config import API_TOKEN, SMMWINGS_API_KEY, ALLOWED_CHANNELS, SERVICE_ID, QUANTITY

# Bot Initialization
bot = telebot.TeleBot(API_TOKEN)

# Logging Setup
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logging.info("Bot started...")

@bot.channel_post_handler(func=lambda message: True)
def handle_channel_post(message):
    try:
        logging.info(f"Received message ID: {message.message_id} from Chat ID: {message.chat.id}")

        # Media Group Messages Ignore karega
        if hasattr(message, 'media_group_id'):
            logging.info("Skipping media group message")
            return  

        chat_id = message.chat.id
        message_id = message.message_id
        chat_info = bot.get_chat(chat_id)
        username = chat_info.username

        if username:
            logging.info(f"Channel username detected: @{username}")
        else:
            logging.warning("No username found for the channel!")
            return

        # Check if the channel is allowed
        if username in ALLOWED_CHANNELS:
            link = f"https://t.me/{username}/{message_id}"
            url = f"https://smmwings.in/api/v2?key={SMMWINGS_API_KEY}&action=add&service={SERVICE_ID}&link={link}&quantity={QUANTITY}"
            
            response = requests.get(url)
            res = response.json()

            logging.info(f"API Response: {res}")

            # Order confirmation message
            bot.send_message(chat_id, f"✅ Order placed successfully!\n\n🔗 Link: {link}\n🆔 Service ID: {SERVICE_ID}\n📦 Quantity: {QUANTITY}")

        else:
            logging.warning(f"Unauthorized channel: @{username}. Ignoring message.")

    except Exception as e:
        logging.error(f"Error: {e}")

# Run Bot
bot.polling()
