
import time
import time_util as t
import random as r
import logging as lg

P1, P2 = range(2)

msg_formats = [
    "Oi! {}! It's ya turn!",
    "Please make your move, {}.",
    "If {} is happy and they know it, they'll make their move!",
    "{}, friendly reminder that it's your turn.",
    "Do you think {} is always this slow?",
    "Waiting for {} to make their move is like watching grass grow.",
    "Maybe watching paint dry is faster than {} making their move."
]


class Reminder(object):

    def __init__(self, bot, chat_id, p1_name, p2_name, wait_sec=300, pause_sec=20):
        self.bot = bot
        self.chat_id = chat_id
        self.names = {P1: p1_name, P2: p2_name}
        self.cur_player = P1
        self.wait_ms = wait_sec * 1000
        self.pause_sec = pause_sec
        self.last_move = t.current_milli_time()
        self.active = False
        self.alive = True

    def reminder_thread(self):
        lg.debug('reminder_thread - starting')
        while self.alive:
            if self.active and ((t.current_milli_time() - self.last_move) > self.wait_ms):
                cur_player_name = self.names[self.cur_player]
                lg.info('reminder_thread - Sending reminder to: Name=%s, Chat_id=%d', cur_player_name, self.chat_id)
                rand_int = r.randrange(len(msg_formats))
                text = msg_formats[rand_int].format(cur_player_name)
                self.bot.send_message(chat_id=self.chat_id, text=text)
                self.active = False
            else:
                lg.debug('reminder_thread - Sleeping %d s', self.pause_sec)
                time.sleep(self.pause_sec)

    def new_turn(self, player):
        self.last_move = t.current_milli_time()
        self.cur_player = player
        self.active = True
