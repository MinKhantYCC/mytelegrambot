# Telegram Bot Tutorial

A small, practical Telegram bot built with `python-telegram-bot` that can:

- respond to `/start` and `/help`
- echo text messages
- receive photos and documents
- save uploaded media to disk
- send local files back to the user

## Project Structure

```text
.
|- main.py
|- handlers.py
|- requirements.txt
|- .env
|- README.md
|- media/
|   |- profile.jpg
|   |- mypic.png
|   |- Toyota.html
```

## Requirements

- Python 3.10+
- Telegram bot token from `@BotFather`

## Setup

1. Create and activate a virtual environment:

```bash
python -m venv .venv
.venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Add your bot token to `.env`:

```env
TELEGRAM_TOKEN=your_bot_token_here
```

## Run the Bot

```bash
python main.py
```

The bot runs in polling mode.

## Supported Commands

- `/start` -> welcome message
- `/help` -> usage details
- `/myphoto` -> sends a local image from `media/mypic.png`
- `/myfile` -> sends a local document from `media/Toyota.html`

## Media Uploads

- Photos and documents sent to the bot are downloaded to `/media`.
- Photos use the largest available size (`effective_attachment[-1]`).

Note: The project currently saves uploads to `/media` but reads outgoing files from `media/`. If you run into file path issues, align these paths in `handlers.py`.

## Development Notes

- Handlers are defined in `handlers.py`.
- Handlers are registered in `main.py` using `ApplicationBuilder` and `add_handlers()`.

## Troubleshooting

- If the bot doesn’t start, confirm `TELEGRAM_TOKEN` is set in `.env`.
- If file sending fails, verify the files exist at `media/mypic.png` and `media/Toyota.html`.
- If uploads aren’t saved, check that the process has permission to write to `/media`.

## References

- https://github.com/python-telegram-bot/python-telegram-bot/wiki/Extensions---Your-first-Bot
- https://github.com/python-telegram-bot/python-telegram-bot/wiki/Types-of-Handlers
- https://github.com/python-telegram-bot/python-telegram-bot/wiki/Working-with-Files-and-Media
