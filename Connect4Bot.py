from telegram import ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup


class Connect4Bot(object):

    def __init__(self, game):
        # Universal Values
        self.game = game
        self.setupHasStarted = False
        self.gameHasStarted = False
        self.P1 = 0
        self.P2 = 1
        self.p_cur = self.P1
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
        self.rm_markup = ReplyKeyboardRemove()

    # /start_game
    def start_game(self, update, context):

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
            if not (self.p_set[self.P1]):
                text = r'Player 1 still needs to be set. Use /p1 to do so.'
            elif not (self.p_set[self.P2]):
                text = r'Player 2 still needs to be set. Use /p2 to do so.'
        # Game has started
        else:
            text = 'The game has already started silly goose!'

        context.bot.send_message(chat_id=chat_id, text=text)

    # /p1
    def p1(self, update, context):

        bot = context.bot
        chat_id = update.message.chat_id
        user = update.message.from_user

        # Player 1 has yet to be set
        if not self.setupHasStarted or (self.setupHasStarted and not (self.p_set[self.P1])):
            self.setupHasStarted = True
            self.p_set[self.P1] = True
            self.p_id[self.P1] = user.id
            self.p_name[self.P1] = user.first_name
            text = self.p_name[self.P1] + ' has been set as Player 1.'
            bot.send_message(chat_id=chat_id, text=text)
        # Player 1 is set but game has not started
        elif self.p_set[self.P1] and not self.gameHasStarted:
            text = self.p_name[self.P1] + ' is already Player 1!'
            bot.send_message(chat_id=chat_id, text=text)

        # If both players are set, start the game!
        if self.p_set[self.P2] and not self.gameHasStarted:
            self.start_for_real(bot, chat_id)

    # /p2
    def p2(self, update, context):

        bot = context.bot
        chat_id = update.message.chat_id
        user = update.message.from_user

        # Player 2 has yet to be set
        if not self.setupHasStarted or (self.setupHasStarted and not (self.p_set[self.P2])):
            self.setupHasStarted = True
            self.p_set[self.P2] = True
            self.p_id[self.P2] = user.id
            self.p_name[self.P2] = user.first_name
            text = self.p_name[self.P2] + ' has been set as Player 2.'
            bot.send_message(chat_id=chat_id, text=text)
        # Player 2 is set but game has not started
        elif self.p_set[self.P2] and not self.gameHasStarted:
            text = self.p_name[self.P2] + ' is already Player 2!'
            bot.send_message(chat_id=chat_id, text=text)

        # If both players are set, start the game!
        if self.p_set[self.P1] and not self.gameHasStarted:
            self.start_for_real(bot, chat_id)

    # /quit
    def quit(self, update, context):

        chat_id = update.message.chat_id
        user_id = update.message.from_user.id
        text = ''

        if not self.setupHasStarted:
            text = ("You can't quit a game that hasn't even started yet..."
                    '\n' + r'Use /start_game to being setup.')
        elif not self.gameHasStarted:
            text = 'Resetting setup.'
            self.reset_game()
        elif self.p_id[self.P1] == user_id:
            text = (self.p_name[self.P1] + ' is a quitter! '
                                           '' + self.p_name[self.P2] + ' wins!')
            self.reset_game()
        elif self.p_id[self.P2] == user_id:
            text = (self.p_name[self.P2] + ' is a quitter! '
                                           '' + self.p_name[self.P1] + ' wins!')
            self.reset_game()

        context.bot.send_message(chat_id=chat_id, text=text,
                                 reply_markup=self.rm_markup)

    # Command Helpers

    def start_for_real(self, bot, chat_id):
        self.gameHasStarted = True
        text = 'Let the games begin!'
        bot.send_message(chat_id=chat_id, text=text)
        text = (self.p_name[self.P1] + '\'s turn!'
                                       '\n' + self.game.board_to_emojis())
        bot.send_message(chat_id=chat_id, text=text,
                         reply_markup=self.inline_markup)

    def reset_game(self):
        self.game.reset()
        self.setupHasStarted = False
        self.gameHasStarted = False
        self.p_cur = self.P1

        self.p_set = [False, False]
        self.p_id = [0, 0]
        self.p_name = ['', '']

    # Player Actions

    def place_chip(self, update, context):

        query = update.callback_query
        inline_text = query.data
        user_id = query.from_user.id

        if inline_text.isdigit() and 1 <= int(inline_text) <= 7:
            if self.gameHasStarted:
                if ((self.p_cur == self.P1 and not (self.p_id[self.P1] == user_id)) or
                        (self.p_cur == self.P2 and not (self.p_id[self.P2] == user_id))):
                    new_text = ("It's not your turn!"
                                '\n' + self.game.board_to_emojis())
                    query.edit_message_text(text=new_text)
                else:
                    self.handle_move(query, int(inline_text))

    # Helpers

    def next_player(self):
        if self.p_cur == self.P1:
            self.p_cur = self.P2
        elif self.p_cur == self.P2:
            self.p_cur = self.P1

    def handle_move(self, query, col):

        res = self.game.place_chip(self.p_cur + 1, col)
        emoji_board = self.game.board_to_emojis()

        if res == -1:
            text = ("You can't place a chip there! Try again."
                    '\n' + emoji_board)
            query.edit_message_text(text=text)
            query.edit_message_reply_markup(reply_markup=self.inline_markup)
        elif res == 0:
            self.next_player()
            text = (self.p_name[self.p_cur] + '\'s turn!'
                                              '\n' + emoji_board)
            query.edit_message_text(text=text)
            query.edit_message_reply_markup(reply_markup=self.inline_markup)
        elif res == 1:
            text = (self.p_name[self.p_cur] + ' wins!'
                                              '\n' + emoji_board)
            self.reset_game()
            query.edit_message_text(text=text)
            query.edit_message_reply_markup(reply_markup=self.rm_markup)
        else:
            text = ('Well... it\'s a tie... good job... I guess.'
                    '\n' + emoji_board)
            self.reset_game()
            query.edit_message(text=text)
            query.edit_message_reply_markup(reply_markup=self.rm_markup)
