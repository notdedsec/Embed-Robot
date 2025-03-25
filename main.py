import logging

from dotenv import load_dotenv

from bot.bot import main

logging.basicConfig(level=logging.INFO)
logging.getLogger('httpx').setLevel(logging.WARNING)

load_dotenv('.env')


if __name__ == "__main__":
    main()
