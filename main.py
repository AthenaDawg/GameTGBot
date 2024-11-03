from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackContext, CallbackQueryHandler, MessageHandler, filters
from game_info_fetcher import GameInfoFetcher
from dotenv import load_dotenv
import os
load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
RAWG_API_KEY = os.getenv("RAWG_API_KEY")

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

def main():
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))  # Handle button presses
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, game))  # Handle game title input
    application.run_polling()

if __name__ == '__main__':
    main()


