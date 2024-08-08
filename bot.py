from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, CallbackContext
from datetime import datetime, timedelta
import os

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
BOT_TOKEN = '7362045643:AAHWiOHy7rVBjqSKDGdJQOMzYHNK4na0jD4'

# Function to read codes from a text file
def read_codes_from_file(file_path):
    with open(file_path, 'r') as file:
        codes = [line.strip() for line in file if line.strip()]
    return codes

# Function to write codes back to the text file
def write_codes_to_file(file_path, codes):
    with open(file_path, 'w') as file:
        for code in codes:
            file.write(code + '\n')

# Function to get the last usage time of a user
def get_last_usage_time(user_id, command):
    file_path = f'{command}_last_usage.txt'
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            for line in file:
                user, timestamp = line.strip().split(',')
                if int(user) == user_id:
                    return datetime.fromisoformat(timestamp)
    return None

# Function to set the last usage time of a user
def set_last_usage_time(user_id, command):
    file_path = f'{command}_last_usage.txt'
    last_usage_time = datetime.utcnow().isoformat()
    with open(file_path, 'a') as file:
        file.write(f"{user_id},{last_usage_time}\n")

# Function to send and remove first 4 codes
def send_and_remove_codes(chat_id: int, bot: Bot, file_path: str):
    codes = read_codes_from_file(file_path)
    
    if len(codes) < 4:
        bot.send_message(chat_id=chat_id, text="Not enough codes available.")
        return
    
    selected_codes = codes[:4]
    remaining_codes = codes[4:]

    write_codes_to_file(file_path, remaining_codes)

    # Send all the codes in a single message, separating each code by a newline
    codes_text = '\n'.join([f'`{code}`' for code in selected_codes])
    bot.send_message(chat_id=chat_id, text=codes_text, parse_mode='Markdown')

# Command Handlers
def clone(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    user_id = update.message.from_user.id
    last_usage_time = get_last_usage_time(user_id, 'clone')

    if last_usage_time:
        now = datetime.utcnow()
        if now - last_usage_time < timedelta(days=1):
            update.message.reply_text('You have already used this command today. Please wait until tomorrow.')
            return

    send_and_remove_codes(chat_id, context.bot, 'clone.txt')
    set_last_usage_time(user_id, 'clone')

def train(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    user_id = update.message.from_user.id
    last_usage_time = get_last_usage_time(user_id, 'train')

    if last_usage_time:
        now = datetime.utcnow()
        if now - last_usage_time < timedelta(days=1):
            update.message.reply_text('You have already used this command today. Please wait until tomorrow.')
            return

    send_and_remove_codes(chat_id, context.bot, 'train.txt')
    set_last_usage_time(user_id, 'train')

def cube(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    user_id = update.message.from_user.id
    last_usage_time = get_last_usage_time(user_id, 'cube')

    if last_usage_time:
        now = datetime.utcnow()
        if now - last_usage_time < timedelta(days=1):
            update.message.reply_text('You have already used this command today. Please wait until tomorrow.')
            return

    send_and_remove_codes(chat_id, context.bot, 'cube.txt')
    set_last_usage_time(user_id, 'cube')

def bike(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    user_id = update.message.from_user.id
    last_usage_time = get_last_usage_time(user_id, 'bike')

    if last_usage_time:
        now = datetime.utcnow()
        if now - last_usage_time < timedelta(days=1):
            update.message.reply_text('You have already used this command today. Please wait until tomorrow.')
            return

    send_and_remove_codes(chat_id, context.bot, 'bike.txt')
    set_last_usage_time(user_id, 'bike')

def total(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    bike_codes = read_codes_from_file('bike.txt')
    cube_codes = read_codes_from_file('cube.txt')
    clone_codes = read_codes_from_file('clone.txt')
    train_codes = read_codes_from_file('train.txt')
    
    bike_count = len(bike_codes)
    cube_count = len(cube_codes)
    clone_count = len(clone_codes)
    train_count = len(train_codes)
    
    response = (
        f"Bike - {bike_count}\n"
        f"Cube - {cube_count}\n"
        f"Clone - {clone_count}\n"
        f"Train - {train_count}"
    )
    update.message.reply_text(response)

def start(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    welcome_message = """
👋 Welcome! I'm a bot that provides promo codes.

To use this bot, you need to subscribe to our channel: @sol_extractor_bot.

Here is a list of available commands:
/bike - Get bike promo codes
/clone - Get clone promo codes
/cube - Get cube promo codes
/train - Get train promo codes
/total - Check the total number of remaining promo codes

Please note that you can use each command only once per day.

Develop: @nothing_4k
"""
    update.message.reply_text(welcome_message)

def main():
    """Start the bot."""
    updater = Updater(BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Register command handlers
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('total', total))
    dispatcher.add_handler(CommandHandler('clone', clone))
    dispatcher.add_handler(CommandHandler('train', train))
    dispatcher.add_handler(CommandHandler('cube', cube))
    dispatcher.add_handler(CommandHandler('bike', bike))

    # Start the Bot
    print('Working...')
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
