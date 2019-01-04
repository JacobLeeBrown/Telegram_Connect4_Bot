
from my_env import get_token

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import logging as lg

from Connect4 import Connect4
from Connect4_Bot import Connect4_Bot

# Basic logging
lg.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
               level=lg.INFO)
logger = lg.getLogger(__name__)

def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    # Initialize bot (telegram)
    updater = Updater(token=get_token())
    dp = updater.dispatcher
    # Initialize Connect4 wrapper
    game = Connect4()
    my_bot = Connect4_Bot(game)

    # Register commands with the Telegram Bot
    start_game_handler  = CommandHandler('start_game', my_bot.start_game)
    p1_handler          = CommandHandler('p1', my_bot.p1)
    p2_handler          = CommandHandler('p2', my_bot.p2)
    quit_handler        = CommandHandler('quit', my_bot.quit)

    dp.add_handler(start_game_handler)
    dp.add_handler(p1_handler)
    dp.add_handler(p2_handler)
    dp.add_handler(quit_handler)

    # Register player actions
    place_chip_handler  = MessageHandler(Filters.text, my_bot.place_chip)
    dp.add_handler(place_chip_handler)

    # Log errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Block until you press Ctrl-C
    updater.idle()


if __name__ == '__main__':
    main()