import telebot
import datetime
import os
import random
from pytz import timezone
from keep_alive import keep_alive

keep_alive()

API_TOKEN = '7026322321:AAH9I8VzohHLrak7TT7ytiJ82NVHNaj--ZY'

bot = telebot.TeleBot(API_TOKEN)

# Function to get the greeting based on Indian Standard Time (IST)
def get_greeting():
    # Set the time zone to Indian Standard Time (IST)
    ist = timezone('Asia/Kolkata')
    current_time = datetime.datetime.now(ist) # Format as HH:MM

    # Determine the appropriate greeting based on the current time
    if current_time.hour < 12:
        return "Good morning"
    elif current_time.hour < 17:
        return "Good afternoon"
    else:
        return "Good evening"

# Function to send welcome GIF
def send_welcome_gif(chat_id):
    # Path to the directory where your GIFs are stored
    gifs_folder = 'gif'

    # List all files in the GIFs folder
    gif_files = os.listdir(gifs_folder)

    # Randomly select a GIF file
    random_gif = random.choice(gif_files)
    gif_path = os.path.join(gifs_folder, random_gif)

    # Send the selected GIF
    with open(gif_path, 'rb') as gif:
        bot.send_document(chat_id, gif)


@bot.message_handler(commands=['admin'])
def show_admins(message):
    bot.send_message(message.chat.id, f"Admins in this group:\n@APPUKANNADIGA01(Owner&Content)\n@MITHUNGOWDA_B(Owner&Developer\n#Nithin(CoOwner&Investor)")

# Handle '/start' command
@bot.message_handler(commands=['start'])
def send_live_message(message):
    bot.reply_to(message, "I am live!")





# Handle new chat members
@bot.message_handler(content_types=['new_chat_members'])
def welcome_new_members(message):
    for new_user in message.new_chat_members:
        
        if new_user.username:
            display_name = f'@{new_user.username}'
        else:
            display_name = new_user.first_name

        send_welcome_gif(message.chat.id)

        # Get the greeting message based on IST
        greeting = get_greeting()

        # Get current IST time
        ist = timezone('Asia/Kolkata')
        current_ist_time = datetime.datetime.now(ist).strftime('%H:%M')

        # Create an inline keyboard
        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.row(
            telebot.types.InlineKeyboardButton("KGHBussidBot", url="https://t.me/KannadaGamrsHub_bot"),
            telebot.types.InlineKeyboardButton("CamPishingBot", url="https://t.me/CameraPishing_Bot")
        )

        # Construct the welcome message with IST time
        welcome_message = f'{greeting}, {display_name}!\n\n' \
                          f'Current IST:{current_ist_time}' \
                          f'Welcome to KannadaGamrsHub. We are delighted to have you here. ' \
                          f'Explore our bots and enjoy your time in the group!'

        # Send the welcome message with the inline keyboard to the new member
        bot.send_message(message.chat.id, welcome_message, reply_markup=keyboard)

# Start the bot
bot.polling()