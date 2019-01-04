class Connect4():
    
    def __init__(self, rows_=6, cols_=7, in_a_row_=4):
        self.rows = rows_
        self.cols = cols_
        self.spaces = self.rows * self.cols
        self.in_a_row = in_a_row_
        self.board = [[0 for i in range(self.cols)] for j in range(self.rows)]
        self.bottom = [(self.rows-1) for i in range(self.cols)]
        self.move_count = 0
    
    def placeChip(self, player, column):
        # Returns:
        #    -1 - Invalid placement
        #     0 - Valid placement
        #     1 - Valid placement, player won
        #     2 - Valid placement, game is tied
        
        col = column - 1
        row = self.bottom[col]
        
        # Invalid move
        if(row == -1 or col < 0 or col >= self.cols):
            return -1
        # Valid placement
        elif(self.board[row][col] == 0):
            self.board[row][col] = player
            self.bottom[col] -= 1
            self.move_count += 1
            
            if(self.checkForWin(row, col, player)):
                return 1
            elif(self.move_count == self.spaces):
                return 2
            else:
                return 0
            
    def checkForWin(self, row, col, player):
        # Spirally checks all directions of the current location to see if the
        # designated player has won, in which case it returns True
        win = self.in_a_row
        
        # Bottom left to top right
        if(  self.checkForWinDir(row+1, col-1, player, 1, -1) + 
             self.checkForWinDir(row-1, col+1, player, -1, 1) + 1 >= win):
            return True
        # Left to right
        elif(self.checkForWinDir(row, col-1, player, 0, -1) + 
             self.checkForWinDir(row, col+1, player, 0,  1) + 1 >= win):
            return True
        # Top left to bottom right
        elif(self.checkForWinDir(row-1, col-1, player, -1, -1) + 
             self.checkForWinDir(row+1, col+1, player,  1,  1) + 1 >= win):
            return True
        # Down
        elif(self.checkForWinDir(row+1, col, player,  1,  0) + 1 >= win):
            return True
        # No 4-in-a-row :(
        else:
            return False
        
    def checkForWinDir(self, row, col, player, row_inc, col_inc):
        # Boundary check
        if(row < 0 or row >= self.rows or col < 0 or col >= self.cols):
            return 0
        # Valid location, check for valid chip
        elif(not(self.board[row][col] == player)):
            return 0
        # Valid location and valid chip, recurse
        else:
            return self.checkForWinDir(row+row_inc, 
                                       col+col_inc, 
                                       player, 
                                       row_inc, 
                                       col_inc) + 1
    
    def reset(self):
        self.__init__()
    
    def printBoard(self):
        for row in self.board:
            print(row)
    
    def boardToString(self):
        res = ''
        for i in range(self.rows):
            res = res + str(self.board[i]) + '\n'
        return res[:-1]
