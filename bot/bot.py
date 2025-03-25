import logging
import os
import uuid

from telegram import InlineQueryResultArticle, InputTextMessageContent, Update
from telegram.constants import ParseMode
from telegram.ext import ApplicationBuilder, ContextTypes, InlineQueryHandler

from bot.helpers import get_info

logger = logging.getLogger(__name__)


async def embed_inline(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.inline_query.query
    logger.info(f'Got inline query for {url}')

    info = get_info(url)
    logger.info(f'Extracted info for {url}')

    message = InputTextMessageContent(
        message_text=f'[{info["title"]}]({info["url"]})',
        parse_mode=ParseMode.MARKDOWN
    )
    result = InlineQueryResultArticle(
        id=uuid.uuid4(),
        title=info["title"],
        description=info['description'],
        thumbnail_url=info['thumbnail'],
        input_message_content=message,
    )

    await update.inline_query.answer([result])


def main():
    BOT_TOKEN = os.getenv('BOT_TOKEN')
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(InlineQueryHandler(embed_inline, pattern=r'https?://.*'))
    app.run_polling()
