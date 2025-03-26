import logging

from dotenv import load_dotenv

load_dotenv('.env')

from bot.bot import main

logging.basicConfig(level=logging.INFO)
logging.getLogger('httpx').setLevel(logging.WARNING)


if __name__ == "__main__":
    main()
