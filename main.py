import logging
import os
from typing import Final

import dotenv
from telegram.ext import ApplicationBuilder

from handlers import (
    echo_handler,
    file_handler,
    help_handler,
    photo_handler,
    send_file_handler,
    send_photo_handler,
    start_handler,
)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# load env variables
dotenv.load_dotenv()
TOKEN: Final = os.getenv("TELEGRAM_TOKEN")


# initialize Telegram application
application = (
    ApplicationBuilder()
    .token(TOKEN)
    .concurrent_updates(True)
    .build()
)

# add handlers
application.add_handlers([
    start_handler,
    help_handler,
    send_file_handler,
    send_photo_handler,
    echo_handler,
    file_handler,
    photo_handler,
])

# Run polling data from Telegram server
application.run_polling(poll_interval=1)
