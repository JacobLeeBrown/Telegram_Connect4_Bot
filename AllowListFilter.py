from telegram.ext import MessageFilter


class AllowListFilter(MessageFilter):
    def __init__(self, allow_list):
        self.allow_list = allow_list

    def filter(self, message):
        return message.from_user.id in self.allow_list