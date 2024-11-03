from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (Application, CommandHandler, CallbackContext, CallbackQueryHandler, MessageHandler, filters,
                          ApplicationBuilder)
from game_info_fetcher import GameInfoFetcher
from dotenv import load_dotenv
import os
load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
RAWG_API_KEY = os.getenv("RAWG_API_KEY")

app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()


fetcher = GameInfoFetcher(RAWG_API_KEY)

async def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("Get Game Info", callback_data='game_info')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    welcome_text = (
        "Welcome to the Game Info Bot! 🎮\n"
        "Click the button below to get game details."
    )
    await update.message.reply_text(welcome_text, reply_markup=reply_markup)

async def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()  # Acknowledge the button press
    # Prompt user to enter the game name
    await query.edit_message_text(text="You can just type the name of the game to get details.")

async def game(update: Update, context: CallbackContext):
    """Fetch game details based on the user's message."""
    game_name = update.message.text.strip()  # Get the message text as the game name
    if not game_name:
        await update.message.reply_text("Please provide a valid game name.")
        return

    # Fetch details about the game
    image_url, game_details = fetcher.get_details(game_name)

    # Send the image first
    if image_url:
        await update.message.reply_photo(photo=image_url)  # Send image without a caption

    # Then send the game details
    await update.message.reply_text(game_details)

# Use a webhook to receive updates
app.run_webhook(listen="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
# Add the handlers after setting up the application
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_handler))  # Handle button presses
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, game))  # Handle game title input



