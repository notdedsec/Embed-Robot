import logging
import os
import uuid

from telegram import InlineQueryResultArticle, InputTextMessageContent, Update
from telegram.constants import ParseMode
from telegram.ext import ApplicationBuilder, ContextTypes, InlineQueryHandler

from bot.helpers import clean_url, get_info

logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv('BOT_TOKEN')


async def embed_inline(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.inline_query.query
    logger.info(f'Got inline query for {url}')

    try:
        info = get_info(url)
        if info.get('error'):
            raise Exception(info['error'])

    except Exception as e:
        error = str(e).replace('ERROR: ', '').split('Use --')[0]
        logger.error(f'Error extracting info for {url}: {error}')
        results = [
            InlineQueryResultArticle(
                id=uuid.uuid4(),
                title='No Embed?',
                description=error,
                input_message_content=InputTextMessageContent(error)
            )
        ]
        await update.inline_query.answer(results, cache_time=0)
        return

    logger.info(f'Extracted info for {url}')

    message = InputTextMessageContent(
        message_text=f'[\u200B]({info["url"]}) [{info["title"]}]({clean_url(url)})',
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
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(InlineQueryHandler(embed_inline, pattern=r'https?://.*'))
    app.run_polling()
