import string
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove

class Connect4_Bot(object):

    def __init__(self, game):
        ## Bookkeeping Globals ##
        # Universal Values
        self.game            = game
        self.setupHasStarted = False
        self.gameHasStarted  = False
        self.p_cur      = 0
        # Player values
        self.p_set           = [False, False]
        self.p_id            = [0, 0]
        self.p_name          = ['', '']
        # Keyboard Markup
        custom_keyboard = [['1', '2', '3', '4', '5', '6', '7']]
        self.rp_markup = ReplyKeyboardMarkup(custom_keyboard)
        self.rm_markup = ReplyKeyboardRemove()

    ### The Commands ###

    # /start_game
    def start_game(self, bot, update):

        chat_id = update.message.chat_id
        text = ''

        # Setup has yet to begin
        if(not(self.setupHasStarted)):
            self.setupHasStarted = True
            text = (r'~~~~ Welcome to Connect 4! ~~~~' + '\n'
                    r'  Player 1, please select /p1' + '\n'
                    r'  Player 2, please select /p2')
        # Setup has begun, but a player still needs to be set
        elif(not(self.gameHasStarted)):
            if(not(self.p_set[0])):
                text = r'Player 1 still needs to be set. Use /p1 to do so.'
            elif(not(self.p_set[1])):
                text = r'Player 2 still needs to be set. Use /p2 to do so.'
        # Game has started
        else:
            text = 'The game has already started silly goose!'

        bot.send_message(chat_id=chat_id, text=text)

    # /p1
    def p1(self, bot, update):

        chat_id = update.message.chat_id
        user = update.message.from_user

        # Player 1 has yet to be set
        if(not(self.setupHasStarted) or 
           (self.setupHasStarted and not(self.p_set[0]))):
            self.setupHasStarted = True
            self.p_set[0]  = True
            self.p_id[0]   = user.id
            self.p_name[0] = user.first_name
            text = self.p_name[0] + r' has been set as Player 1.'
            bot.send_message(chat_id=chat_id, text=text)
        # Player 1 is set but game has not started
        elif(self.p_set[0] and not(self.gameHasStarted)):
            text = self.p_name[0] + r' is already Player 1!'
            bot.send_message(chat_id=chat_id, text=text)
        
        # If both players are set, start the game!
        if(self.p_set[1] and not(self.gameHasStarted)):
            self.start_for_real(bot, chat_id)

    # /p2
    def p2(self, bot, update):

        chat_id = update.message.chat_id
        user = update.message.from_user

        # Player 2 has yet to be set
        if(not(self.setupHasStarted) or 
           (self.setupHasStarted and not(self.p_set[1]))):
            self.setupHasStarted = True
            self.p_set[1]  = True
            self.p_id[1]   = user.id
            self.p_name[1] = user.first_name
            text = self.p_name[1] + r' has been set as Player 2.'
            bot.send_message(chat_id=chat_id, text=text)
        # Player 2 is set but game has not started
        elif(self.p_set[1] and not(self.gameHasStarted)):
            text = self.p_name[1] + r' is already Player 2!'
            bot.send_message(chat_id=chat_id, text=text)
        
        # If both players are set, start the game!
        if(self.p_set[0] and not(self.gameHasStarted)):
            self.start_for_real(bot, chat_id)

    # /quit
    def quit(self, bot, update):

        chat_id = update.message.chat_id
        text = ''

        if(not(self.setupHasStarted)):
            text = (r"You can't quit a game that hasn't even started yet..."
                    '\n' + r'Use /start_game to being setup.')
        elif(not(self.gameHasStarted)):
            text = 'Resetting setup.'
            self.reset_game()
        elif(self.p_id[0] == user_id):
            text = self.p_name[0]+' is a quitter! ' + self.p_name[1]+' wins!'
            self.reset_game()
        elif(self.p_id[1] == user_id):
            text = self.p_name[1]+' is a quitter! ' + self.p_name[0]+' wins!'
            self.reset_game()

        bot.send_message(chat_id=chat_id, text=text, 
                         reply_markup=self.rm_markup)

    ### Command Helpers ###

    def start_for_real(self, bot, chat_id):
        self.gameHasStarted = True
        text = 'Let the games begin!'
        bot.send_message(chat_id=chat_id, text=text)
        text = self.p_name[0] + '\'s turn!' + '\n' + self.game.boardToString()
        bot.send_message(chat_id=chat_id, text=text, 
                         reply_markup=self.rp_markup)

    def reset_game(self):
        self.game.reset()
        self.setupHasStarted = False
        self.gameHasStarted = False
        self.p_cur = 0
        
        self.p_set = [False, False]
        self.p_id = [0, 0]
        self.p_name = ['', '']

    ### Player Actions ###

    def place_chip(self, bot, update):

        text = update.message.text
        chat_id = update.message.chat_id
        user_id = update.message.from_user.id

        if(text in string.digits and int(text) >= 1 and int(text) <= 7):
            if(self.gameHasStarted):
                if((self.p_cur == 1 and not(self.p_id[0] == user_id)) or
                   (self.p_cur == 2 and not(self.p_id[1] == user_id))):
                    text = 'It is not your turn!'
                    bot.send_message(chat_id=chat_id, text=text)
                else:
                    self.handle_move(bot, chat_id, int(text))

    ### Helpers ###

    def next_player(self):
        if(self.p_cur == 0):
            self.p_cur = 1
        elif(self.p_cur == 1):
            self.p_cur = 0

    def handle_move(self, bot, chat_id, col):
        
        res = self.game.placeChip(self.p_cur+1, col)
        
        if(res == -1):
            text = "You can't place a chip there! Try again."
            bot.send_message(chat_id=chat_id, text=text)
        elif(res == 0):
            self.next_player()
            text = (self.p_name[self.p_cur] + '\'s turn!'
                    '\n' + self.game.boardToString())
            bot.send_message(chat_id=chat_id, text=text)
        elif(res == 1):
            text = (self.p_name[self.p_cur] + ' wins the game!'
                    '\n' + self.game.boardToString())
            self.reset_game()
            bot.send_message(chat_id=chat_id, text=text, 
                             reply_markup=self.rm_markup)
        else:
            text = 'Well... it\'s a tie... good job... I guess.'
            self.reset_game()
            bot.send_message(chat_id=chat_id, text=text, 
                             reply_markup=self.rm_markup)
