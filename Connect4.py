
class Connect4:

    BLANK, P1, P2 = range(3)
    BAD_MOVE, GOOD_MOVE, WIN_MOVE, TIE_MOVE = range(-1, 3)

    def __init__(self, rows_=6, cols_=7, in_a_row_=4):
        """
        Parameters
        ----------
        rows_ : int
            Number of rows this Connect4 instance will have.
        cols_ : int
            Number of columns this Connect4 instance will have.
        in_a_row_ : int
            Number of chips a player needs in-a-row to win.
        """
        self.rows = rows_
        self.cols = cols_
        self.spaces = self.rows * self.cols
        self.in_a_row = in_a_row_
        self.board = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.bottom = [(self.rows - 1) for _ in range(self.cols)]
        self.move_count = 0

    def place_chip(self,
                   player: int,
                   col: int
                   ) -> int:
        """ Attempts to place a chip for the player in the designated column.

        Parameters
        ----------
        player : int
            Which player is making this move.
                1 = Player 1
                2 = Player 2
        col : int
            1-Indexed column value for chip to be placed

        Returns
        -------
        int
           -1 - Invalid placement
            0 - Valid placement
            1 - Valid placement, player won
            2 - Valid placement, game is tied
        """

        col = col - 1
        row = self.bottom[col]  # Gets the row the chip would land

        # Invalid move
        if row == -1 or col < 0 or col >= self.cols or self.board[row][col] != 0:
            return self.BAD_MOVE

        self.board[row][col] = player
        self.bottom[col] -= 1
        self.move_count += 1

        if self._check_for_win(player, row, col):
            return self.WIN_MOVE
        elif self.move_count == self.spaces:
            return self.TIE_MOVE
        else:
            return self.GOOD_MOVE

    def _check_for_win(self,
                       player: int,
                       row: int,
                       col: int):
        """ Spirally checks all directions of the current location to see if the
        designated player has won, in which case it returns True.

        Parameters
        ----------
        player : int
            Which player to check for a win.
                1 = Player 1
                2 = Player 2
        row : int
            0-Indexed row value (y-position) for initial chip
        col : int
            0-Indexed column value (x-position) for initial chip

        Returns
        -------
        bool
           True if player has at least self.in_a_row chips in a row (has won the
           game), false otherwise
        """
        win = self.in_a_row

        # Bottom left to top right
        if (self._check_for_win_dir(player, row + 1, col - 1, 1, -1) +
                self._check_for_win_dir(player, row - 1, col + 1, -1, 1) + 1 >= win):
            return True
        # Left to right
        elif (self._check_for_win_dir(player, row, col - 1, 0, -1) +
              self._check_for_win_dir(player, row, col + 1, 0, 1) + 1 >= win):
            return True
        # Top left to bottom right
        elif (self._check_for_win_dir(player, row - 1, col - 1, -1, -1) +
              self._check_for_win_dir(player, row + 1, col + 1, 1, 1) + 1 >= win):
            return True
        # Down
        elif self._check_for_win_dir(player, row + 1, col, 1, 0) + 1 >= win:
            return True
        # Not enough chips in any direction to win :(
        else:
            return False

    def _check_for_win_dir(self,
                           player: int,
                           row: int,
                           col: int,
                           row_inc: int,
                           col_inc: int):
        """ Recursively traverses the board to return how many chips belong to
        the player going in the specified direction, which is determined by the
        row and column increment parameters.

        Parameters
        ----------
        player : int
            Which player to check for a win.
                1 = Player 1
                2 = Player 2
        row : int
            0-Indexed row value (y-position) for current chip
        col : int
            0-Indexed column value (x-position) for current chip
        row_inc : int
            Increment for y-position for next chip
                -1 = Going up in the board
                0 = Going horizontally
                1 = Going down
        col_inc : int
            Increment for x-position for next chip
                -1 = Going left in the board
                0 = Going vertically
                1 = Going right

        Returns
        -------
        int
           Number of chips belonging to the player going in the specified
           direction, starting with the chip at the given row and column.
        """
        # Boundary check
        if row < 0 or row >= self.rows or col < 0 or col >= self.cols:
            return 0
        # Valid location, check for valid chip
        elif not (self.board[row][col] == player):
            return 0
        # Valid location and valid chip, recurse
        else:
            return self._check_for_win_dir(player,
                                           row + row_inc,
                                           col + col_inc,
                                           row_inc,
                                           col_inc) + 1

    def reset(self):
        """ Resets this Connect4 instance to initial state. """
        self.__init__(self.rows, self.cols, self.in_a_row)

    def _print_board(self):
        """ Debugging method """
        for row in self.board:
            print(row)

    def _board_to_string(self):
        """ Debugging method """
        res = ''
        for i in range(self.rows):
            res = res + str(self.board[i]) + '\n'
        return res[:-1]
