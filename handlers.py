from telegram import Update
from telegram.ext import ContextTypes, CommandHandler, MessageHandler, filters
import os


os.makedirs("./media", exist_ok=True)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    This function will be called when the user sends '/start command.
    """
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Hello! How can I help you today?")


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    This function will be called when the user sends '/help command.
    """
    await context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text=(
            "Hi! This is The Steward, Alferd Highman. "
            "You can order me by sending commands:\n"
            "- `/start` : to start a service\n"
            "- `/help` : to view the available commands\n"
            "- `/myphoto` : to download a photo\n"
            "- `/myfile` : to download a file\n"
            "\n"
            "You can send any photos and documents to me. I will save it for you. "
        )
    )


async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    This function will be called when the user sends a file to the bot. It will download the file and save under '/media' directory.
    """
    new_file = await update.message.effective_attachment.get_file()
    file_name = new_file.file_path.split("/")[-1]
    await new_file.download_to_drive(f"./media/{file_name}")
    await context.bot.send_message(chat_id=update.effective_chat.id, text="We got a file!")
    

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    This function will be called when the user sends a photo to the bot. It will download the photo and save under '/media' directory.
    """
    new_photo = await update.message.effective_attachment[-1].get_file()
    file_name = new_photo.file_path.split("/")[-1]
    print(file_name)
    await new_photo.download_to_drive(f"./media/{file_name}")
    await context.bot.send_message(chat_id=update.effective_chat.id, text="We got a photo!")


async def send_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    This function will be called when the user requests a photo.
    """
    with open("./media/mypic.png", "rb") as photo:
        await context.bot.send_photo(chat_id=update.effective_chat.id, photo=photo)
        

async def send_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    This function will be called when the user requests a file.
    """
    with open("./media/Toyota.html", "rb") as file:
        await context.bot.send_document(chat_id=update.effective_chat.id, document=file)
        

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    This function will be called when the user sends a message and echo the message back to the user.
    """
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)
    
    

start_handler = CommandHandler('start', start)
help_handler = CommandHandler('help', help)
send_photo_handler = CommandHandler('myphoto', send_photo)
send_file_handler = CommandHandler('myfile', send_file)
echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
file_handler = MessageHandler(filters.ATTACHMENT & (~filters.PHOTO), handle_file)
photo_handler = MessageHandler(filters.PHOTO, handle_photo)