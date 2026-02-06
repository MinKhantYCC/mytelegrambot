# Build a File-Saving Telegram Bot with Python (Step by Step)

This tutorial walks through a real project that uses [`python-telegram-bot`](https://github.com/python-telegram-bot/python-telegram-bot) to:

- respond to commands (`/start`, `/help`)
- echo text messages
- receive photos and documents
- save uploaded media to disk
- send files back to the user

The code is organized around two files:

- `main.py`: application startup and handler registration
- `handlers.py`: bot behavior for commands, text, and media

## 1. What You Are Building

By the end, your bot will support:

- `/start` -> welcome message
- `/help` -> list of available commands
- `/myphoto` -> sends a local image
- `/myfile` -> sends a local document
- text message -> bot echoes the same text
- uploaded photo/document -> bot downloads and stores it

This follows the official extension style from the PTB wiki: create an `Application` with `ApplicationBuilder`, then attach `CommandHandler` and `MessageHandler` callbacks.

## 2. Project Structure

Current project layout:

```text
.
|- main.py
|- handlers.py
|- requirements.txt
|- .env
|- README.md
|- images/profile.jpg
```

## 3. Install Dependencies

Create and activate a virtual environment, then install packages:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Your `requirements.txt` includes:

- `python-telegram-bot==22.6`
- `python-dotenv==1.2.1`

## 4. Create Your Bot Token

Use Telegram `@BotFather`:

1. Send `/newbot`
2. Choose a bot name and username
3. Copy the generated token

Add it to `.env`:

```env
TELEGRAM_TOKEN=your_bot_token_here
```

`main.py` reads this token via `python-dotenv`.

## 5. Bootstrap the Application (`main.py`)

The startup flow is:

1. configure logging
2. load environment variables
3. build the application with `ApplicationBuilder`
4. register handlers
5. start polling

Core setup:

```python
dotenv.load_dotenv()
TOKEN: Final = os.getenv("TELEGRAM_TOKEN")

application = (
    ApplicationBuilder()
    .token(TOKEN)
    .concurrent_updates(True)
    .build()
)
```

Then handlers are added and polling starts:

```python
application.add_handlers([...])
application.run_polling(poll_interval=1)
```

This matches the PTB "first bot" pattern, where the application dispatches updates to handlers.

## 6. Implement Command Handlers (`handlers.py`)

### `/start`

`start()` sends a simple welcome message:

```python
await context.bot.send_message(
    chat_id=update.effective_chat.id,
    text="Hello! How can I help you today?"
)
```

### `/help`

`help()` returns usage instructions with your available commands.

Both callbacks are connected using `CommandHandler`:

```python
start_handler = CommandHandler('start', start)
help_handler = CommandHandler('help', help)
```

## 7. Add a Text Echo Handler

For non-command text messages:

```python
echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
```

The filter combo is important:

- `filters.TEXT` matches text messages
- `~filters.COMMAND` excludes `/command` messages

This keeps command handling and regular text handling cleanly separated.

## 8. Receive and Save Files/Photos

The project creates a storage folder on startup:

```python
os.makedirs("/media", exist_ok=True)
```

### File upload callback

```python
new_file = await update.message.effective_attachment.get_file()
await new_file.download_to_drive("/media")
```

### Photo upload callback

```python
new_photo = await update.message.effective_attachment[-1].get_file()
await new_photo.download_to_drive("/media")
```

Why `[-1]` for photos? Telegram sends multiple photo sizes; the last one is typically the largest. This follows PTB media guidance.

Handlers:

```python
file_handler = MessageHandler(filters.ATTACHMENT & (~filters.PHOTO), handle_file)
photo_handler = MessageHandler(filters.PHOTO, handle_photo)
```

## 9. Send Local Media Back to Users

Two command callbacks send local files:

```python
with open("media/mypic.png", "rb") as photo:
    await context.bot.send_photo(chat_id=update.effective_chat.id, photo=photo)
```

```python
with open("media/Toyota.html", "rb") as file:
    await context.bot.send_document(chat_id=update.effective_chat.id, document=file)
```

These are wired to:

- `/myphoto`
- `/myfile`

## 10. Register Handlers in Order

In `main.py`, handlers are added in one list:

```python
application.add_handlers([
    start_handler,
    help_handler,
    send_file_handler,
    send_photo_handler,
    echo_handler,
    file_handler,
    photo_handler,
])
```

Handler order matters in PTB. More specific handlers should generally come before broad catch-all logic.

## 11. Run and Test the Bot

Start the bot:

```bash
python main.py
```

Manual test checklist:

1. Send `/start`
2. Send `/help`
3. Send plain text and verify echo
4. Upload a document and verify saved file + confirmation message
5. Upload a photo and verify saved image + confirmation message
6. Send `/myphoto`
7. Send `/myfile`

## 12. Practical Improvements

If you publish or continue this project, these are solid next upgrades:

1. Use a consistent media path (`/media` vs `media`) to avoid path issues across environments.
2. Add an unknown-command handler (placed last) for better UX.
3. Validate file type and size before saving.
4. Add error handlers and structured logs for production debugging.
5. Consider webhook deployment for cloud hosting.

## Final Notes

This bot is a clean example of PTB's handler-driven design:

- `CommandHandler` for explicit commands
- `MessageHandler` + filters for content routing
- `effective_attachment` and `download_to_drive()` for media workflows

That architecture scales well as you add features like inline mode, callback queries, and job queues.

## References

- https://github.com/python-telegram-bot/python-telegram-bot/wiki/Extensions---Your-first-Bot
- https://github.com/python-telegram-bot/python-telegram-bot/wiki/Types-of-Handlers
- https://github.com/python-telegram-bot/python-telegram-bot/wiki/Working-with-Files-and-Media
- https://docs.python-telegram-bot.org/
