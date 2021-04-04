import logging as lg
from emoji import UNICODE_EMOJI
from telegram.ext import MessageFilter

logger = lg.getLogger(__name__)


class EmojiMessageFilter(MessageFilter):

    def filter(self, message):
        potential_emoji = message.text
        return potential_emoji in UNICODE_EMOJI
