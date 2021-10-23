import logging as lg
import threading
from typing import Union

from emoji import emojize
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, Bot, CallbackQuery
from telegram.ext import CallbackContext

from Connect4 import Connect4
from Reminder import Reminder

P1, P2, P1_WIN, P2_WIN, BLANK = range(5)
emoji_map = {P1: emojize(":red_circle:", use_aliases=True),
             P2: emojize(":large_blue_circle:", use_aliases=True),
             P1_WIN: emojize(":100:", use_aliases=True),
             P2_WIN: emojize(":cyclone:", use_aliases=True),
             BLANK: emojize(":white_circle:", use_aliases=True)}


class Connect4Bot(object):

    def __init__(self,
                 game: Connect4):
        # Universal Values
        self.game = game
        self.setupHasStarted = False
        self.gameHasStarted = False
        self.p_cur = P1  # Player 1 goes first
        self.game_message = None
        # Player values
        self.p_set = [False, False]
        self.p_id = [0, 0]
        self.p_name = ['', '']
        # Keyboard Markup
        custom_keyboard = [[InlineKeyboardButton('1', callback_data='1'),
                            InlineKeyboardButton('2', callback_data='2'),
                            InlineKeyboardButton('3', callback_data='3'),
                            InlineKeyboardButton('4', callback_data='4'),
                            InlineKeyboardButton('5', callback_data='5'),
                            InlineKeyboardButton('6', callback_data='6'),
                            InlineKeyboardButton('7', callback_data='7')]]
        self.inline_markup = InlineKeyboardMarkup(custom_keyboard)

    # /start_game
    def start_game(self,
                   update: Update,
                   context: CallbackContext):

        chat_id = update.message.chat_id
        text = ''

        # Setup has yet to begin
        if not self.setupHasStarted:
            self.setupHasStarted = True
            text = ("~~~~ Welcome to Connect 4! ~~~~\n" +
                    "Player 1, please select /p1\n" +
                    "Player 2, please select /p2")
        # Setup has begun, but a player still needs to be set
        elif not self.gameHasStarted:
            if not (self.p_set[P1]):
                text = r'Player 1 still needs to be set. Use /p1 to do so.'
            elif not (self.p_set[P2]):
                text = r'Player 2 still needs to be set. Use /p2 to do so.'
        # Game has started
        else:
            text = 'The game has already started silly goose!'

        context.bot.send_message(chat_id=chat_id, text=text)

    # /p1
    def p1(self,
           update: Update,
           context: CallbackContext):

        bot = context.bot
        chat_id = update.message.chat_id
        user = update.message.from_user

        # Player 1 has yet to be set
        if not self.setupHasStarted or (self.setupHasStarted and not (self.p_set[P1])):
            self.setupHasStarted = True
            self.p_set[P1] = True
            self.p_id[P1] = user.id
            self.p_name[P1] = user.first_name
            text = self.p_name[P1] + ' has been set as Player 1.'
            bot.send_message(chat_id=chat_id, text=text)
            lg.debug(text)
        # Player 1 is set but game has not started
        elif self.p_set[P1] and not self.gameHasStarted:
            text = self.p_name[P1] + ' is already Player 1!'
            bot.send_message(chat_id=chat_id, text=text)

        # If both players are set, start the game!
        if self.p_set[P2] and not self.gameHasStarted:
            self._start_for_real(bot, chat_id)

    # /p2
    def p2(self,
           update: Update,
           context: CallbackContext):

        bot = context.bot
        chat_id = update.message.chat_id
        user = update.message.from_user

        # Player 2 has yet to be set
        if not self.setupHasStarted or (self.setupHasStarted and not (self.p_set[P2])):
            self.setupHasStarted = True
            self.p_set[P2] = True
            self.p_id[P2] = user.id
            self.p_name[P2] = user.first_name
            text = self.p_name[P2] + ' has been set as Player 2.'
            bot.send_message(chat_id=chat_id, text=text)
            lg.debug(text)
        # Player 2 is set but game has not started
        elif self.p_set[P2] and not self.gameHasStarted:
            text = self.p_name[P2] + ' is already Player 2!'
            bot.send_message(chat_id=chat_id, text=text)

        # If both players are set, start the game!
        if self.p_set[P1] and not self.gameHasStarted:
            self._start_for_real(bot, chat_id)

    # /quit
    def quit(self,
             update: Update,
             context: CallbackContext):

        bot = context.bot
        chat_id = update.message.chat_id
        user_id = update.message.from_user.id

        if not self.setupHasStarted:
            text = ("You can't quit a game that hasn't even started yet...\n" +
                    'Use /start_game to begin setup.')
            bot.send_message(chat_id=chat_id, text=text)
        elif not self.gameHasStarted:
            text = 'Resetting setup. Please wait for completion.'
            bot.send_message(chat_id=chat_id, text=text)
            lg.debug(text)
            self._reset_game()
            text = 'Resetting complete.'
            bot.send_message(chat_id=chat_id, text=text)
            lg.debug(text)
        elif self.p_id[P1] == user_id:
            text = (self.p_name[P1] + ' is a quitter! ' +
                    self.p_name[P2] + ' wins!\n' +
                    _board_to_emojis(self.game.board))
            bot.edit_message_text(chat_id=chat_id, text=text, message_id=self.game_message.message_id)
            self._reset_game()
            lg.debug('Player 1 Quit. Reset complete.')
        elif self.p_id[P2] == user_id:
            text = (self.p_name[P2] + ' is a quitter! ' +
                    self.p_name[P1] + ' wins!\n' +
                    _board_to_emojis(self.game.board))
            bot.edit_message_text(chat_id=chat_id, text=text, message_id=self.game_message.message_id)
            self._reset_game()
            lg.debug('Player 2 Quit. Reset complete.')

    # Command Helpers

    def _start_for_real(self,
                        bot: Bot,
                        chat_id: Union[int, str]):
        lg.debug('Starting game! Chat_id=%d', chat_id)
        self.gameHasStarted = True

        text = 'Let the games begin!'
        bot.send_message(chat_id=chat_id, text=text)

        text = (self.p_name[P1] + '\'s turn!\n' +
                _board_to_emojis(self.game.board))
        self.game_message = bot.send_message(chat_id=chat_id, text=text, reply_markup=self.inline_markup)

        # Start Reminder
        lg.debug('Reminder Thread - Initializing')
        self.reminder = Reminder(bot, chat_id, self.p_name[P1], self.p_name[P2], wait_sec=10, pause_sec=2)
        self.reminder_thread = threading.Thread(target=self.reminder.reminder_thread(), daemon=True)
        self.reminder.new_turn(P1)
        self.reminder_thread.start()
        lg.debug('Reminder Thread - Kick off logic complete')

    def _reset_game(self,
                    chat_id: Union[int, str]):
        lg.debug('Resetting game! Chat_id=%d', chat_id)
        self.game.reset()
        self.setupHasStarted = False
        self.gameHasStarted = False
        self.p_cur = P1
        self.game_message = None

        self.p_set = [False, False]
        self.p_id = [0, 0]
        self.p_name = ['', '']

        self.reminder.alive = False
        self.reminder_thread.join(self.reminder.pause_sec)

    # Player Actions

    def place_chip(self,
                   update: Update,
                   context: CallbackContext):

        query = update.callback_query
        query.answer()

        inline_text = query.data

        user = query.from_user
        user_id = user.id

        if inline_text.isdigit() and 1 <= int(inline_text) <= 7:
            if self.gameHasStarted:
                if ((self.p_cur == P1 and not (self.p_id[P1] == user_id)) or
                        (self.p_cur == P2 and not (self.p_id[P2] == user_id))):
                    new_text = (user.first_name + ", it's not your turn!\n" +
                                _board_to_emojis(self.game.board))
                    query.edit_message_text(text=new_text, reply_markup=self.inline_markup)
                else:
                    self._handle_move(query, int(inline_text))

    # Helpers

    def _next_player(self):
        if self.p_cur == P1:
            self.p_cur = P2
        elif self.p_cur == P2:
            self.p_cur = P1

    def _handle_move(self,
                     query: CallbackQuery,
                     col: int):

        res = self.game.place_chip(self.p_cur + 1, col)
        emoji_board = _board_to_emojis(self.game.board)

        if res == -1:
            text = ("You can't place a chip there! Try again.\n" +
                    emoji_board)
            query.edit_message_text(text=text, reply_markup=self.inline_markup)
            self.reminder.new_turn(self.p_cur)
        elif res == 0:
            self._next_player()
            text = (self.p_name[self.p_cur] + '\'s turn!\n' +
                    emoji_board)
            query.edit_message_text(text=text, reply_markup=self.inline_markup)
            self.reminder.new_turn(self.p_cur)
        elif res == 1:
            text = (self.p_name[self.p_cur] + ' wins!\n' +
                    emoji_board)
            self._reset_game()
            query.edit_message_text(text=text)
            self.reminder.alive = False
        else:
            text = ('Well... it\'s a tie... good job... I guess.\n' +
                    emoji_board)
            self._reset_game()
            query.edit_message_text(text=text)
            self.reminder.alive = False


def _board_to_emojis(board):
    # Column Headers
    headers = emojize(":keycap_1: :keycap_2: :keycap_3: :keycap_4: :keycap_5: :keycap_6: :keycap_7:",
                      use_aliases=True)
    p1_chip = emoji_map[P1]
    p2_chip = emoji_map[P2]
    blank = emoji_map[BLANK]

    res = headers + '\n'

    for row in board:
        r = ''
        for entry in row:
            if entry == 0:
                r += blank + ' '
            elif entry == 1:
                r += p1_chip + ' '
            elif entry == 2:
                r += p2_chip + ' '
        r = r[:-1]
        res += r + '\n'

    res += headers

    return res
