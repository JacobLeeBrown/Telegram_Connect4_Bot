import logging as lg
from telegram.ext import MessageFilter

logger = lg.getLogger(__name__)


class AllowListFilter(MessageFilter):
    def __init__(self, allow_list):
        self.allow_list = allow_list

    def filter(self, message):
        user = message.from_user
        if user.id in self.allow_list:
            return True
        logger.warning('%s %s (%d) sent message but is not in the allow list', user.first_name, user.last_name, user.id)
        return False
