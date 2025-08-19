# Embed-Robot

A Telegram inline bot that generates embeds for video URLs from YouTube, Instagram, Twitter, TikTok, and many other platforms.

## Quick Start

1. Get a bot token from [@BotFather](https://t.me/botfather)
2. Copy `example.env` to `.env` and add your `BOT_TOKEN`
3. Run the bot:

```bash
uv run --upgrade main.py
```

## Usage

Type `@your_bot_name <video_url>` in any Telegram chat to generate an embed.

## Configuration

Edit `.env` file:

- `BOT_TOKEN`: Your Telegram bot token (required)
- `YTDL_WORKERS`: Comma-separated list of worker URLs (optional)
- `PO_TOKEN`: YouTube po_token for enhanced access (optional)
- `COOKIES_BROWSER` & `COOKIES_PROFILE`: Browser cookies for restricted content (optional)

## Worker API

The project includes a Vercel-compatible worker API in the `worker/` directory that can be deployed and used in `YTDL_WORKERS` to avoid rate limits.

## Acknowledgments

- [`yt-dlp`](https://github.com/yt-dlp/yt-dlp): Video information extraction
- [`python-telegram-bot`](https://github.com/python-telegram-bot/python-telegram-bot): Telegram Bot API wrapper
