import logging as lg

from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext

import my_env as env
from AllowListFilter import AllowListFilter
from Connect4 import Connect4
from Connect4Bot import Connect4Bot

# Basic logging
lg.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=lg.INFO
)
logger = lg.getLogger(__name__)


def error_handler(update: Update, context: CallbackContext) -> None:
    # Log the error before we do anything else, so we can see it even if something breaks.
    logger.error(msg="Exception while handling an update:", exc_info=context.error)


def main():
    # Initialize bot (telegram)
    updater = Updater(token=env.connect4_token, use_context=True)
    dp = updater.dispatcher
    # Initialize Connect4 wrapper
    game = Connect4()
    my_bot = Connect4Bot(game)
    # Initialize allow list filter
    my_filter = AllowListFilter(env.user_allow_list)

    # Register commands with the Telegram Bot
    start_game_handler = CommandHandler('start_game', my_bot.start_game, filters=my_filter)
    p1_handler = CommandHandler('p1', my_bot.p1, filters=my_filter)
    p2_handler = CommandHandler('p2', my_bot.p2, filters=my_filter)
    quit_handler = CommandHandler('quit', my_bot.quit, filters=my_filter)

    dp.add_handler(start_game_handler)
    dp.add_handler(p1_handler)
    dp.add_handler(p2_handler)
    dp.add_handler(quit_handler)

    # Register player actions
    place_chip_handler = CallbackQueryHandler(my_bot.place_chip)
    dp.add_handler(place_chip_handler)

    # Log errors
    dp.add_error_handler(error_handler)

    # Start the Bot
    updater.start_polling()

    # Block until you press Ctrl-C
    updater.idle()


if __name__ == '__main__':
    main()

# Run in Pythom CLI with:
# >>> exec(open("connect4_bot_script.py").read())
