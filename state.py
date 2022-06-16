def is_on_board(x, y):
    return 0 <= x <= 7 and 0 <= y <= 7

class State(object):
    def __init__(self, board=None):
        if board != None:
            self._board = board
        else:
            self._board = [["0", "0", "0", "0", "0", "0", "0", "0"],
                           ["0", "0", "0", "0", "0", "0", "0", "0"],
                           ["0", "0", "0", "0", "0", "0", "0", "0"],
                           ["0", "0", "0", "●", "⭘", "0", "0", "0"],
                           ["0", "0", "0", "⭘", "●", "0", "0", "0"],
                           ["0", "0", "0", "0", "0", "0", "0", "0"],
                           ["0", "0", "0", "0", "0", "0", "0", "0"],
                           ["0", "0", "0", "0", "0", "0", "0", "0"]]

    def get_value(self, i, j):
        return self._board[i][j]

    @property
    def board(self):
        return self._board

    @board.setter
    def board(self, value):
        self._board = value

    def is_end(self):
        if self.get_valid_moves("⭘") == [] and self.get_valid_moves("●") == []:
            return True
        return False

    def declare_winner(self):
        black, white = self.get_board_score()
        if black > white:
            winner = "Black"
        elif white > black:
            winner = "White"
        else:
            winner = "Tie"
        return winner

    def get_board_score(self):
        black = 0
        white = 0
        for x in range(8):
            for y in range(8):
                if self._board[x][y] == '⭘':
                    black += 1
                if self._board[x][y] == '●':
                    white += 1
        return black, white

    def get_color_score(self,color):
        score = 0
        for x in range(8):
            for y in range(8):
                if self._board[x][y] == color:
                    score += 1
        return score

    def move_validation(self, x0, y0, color):
        if color not in "⭘●":
            return False

        if self._board[x0][y0] != "0" or not is_on_board(x0, y0):
            return False

        self._board[x0][y0] = color
        if color == "●":
            other_color = "⭘"
        else:
            other_color = "●"

        values_to_flip = []
        for xdir, ydir in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
            x, y = x0, y0
            x += xdir
            y += ydir
            if is_on_board(x, y) and self._board[x][y] == other_color:
                x += xdir
                y += ydir
                if not is_on_board(x, y):
                    continue
                while self._board[x][y] == other_color:
                    x += xdir
                    y += ydir
                    if not is_on_board(x, y):
                        break
                if not is_on_board(x, y):
                    continue
                if self._board[x][y] == color:
                    while True:
                        x -= xdir
                        y -= ydir
                        if x == x0 and y == y0:
                            break
                        values_to_flip.append([x, y])

        self._board[x0][y0] = "0"
        if len(values_to_flip) == 0:
            return False
        return values_to_flip

    def play_move(self, x0, y0, color):
        values_to_flip = self.move_validation(x0, y0, color)
        if values_to_flip == False:
            return False
        self._board[x0][y0] = color
        for x, y in values_to_flip:
            self._board[x][y] = color
        return True

    def get_valid_moves(self, color):
        valid_moves = []
        for x in range(8):
            for y in range(8):
                if self.move_validation(x, y, color) != False:
                    valid_moves.append([x, y])
        return valid_moves

    def dynamic_heuristic_evaluation(self):
        my_color = "●"
        opp_color = "⭘"
        grid = self._board
        my_tiles = 0
        opp_tiles = 0
        my_front_tiles = 0
        opp_front_tiles = 0
        p = 0
        c = 0
        l = 0
        m = 0
        f = 0
        d = 0

        X1 = [-1, -1, 0, 1, 1, 1, 0, -1]
        Y1 = [0, 1, 1, 1, 0, -1, -1, -1]

        V = []
        V.append([20, -3, 11, 8, 8, 11, -3, 20])
        V.append([-3, -7, -4, 1, 1, -4, -7, -3])
        V.append([11, -4, 2, 2, 2, 2, -4, 11])
        V.append([8, 1, 2, -3, -3, 2, 1, 8])
        V.append([8, 1, 2, -3, -3, 2, 1, 8])
        V.append([11, -4, 2, 2, 2, 2, -4, 11])
        V.append([-3, -7, -4, 1, 1, -4, -7, -3])
        V.append([20, -3, 11, 8, 8, 11, -3, 20])

        for i in range(0, 8):
            for j in range(0, 8):
                if grid[i][j] == my_color:
                    d += V[i][j]
                    my_tiles += 1
                elif grid[i][j] == opp_color:
                    d -= V[i][j]
                    opp_tiles += 1
                if grid[i][j] != "0":
                    for k in range(0, 8):
                        x = i + X1[k]
                        y = j + Y1[k]
                        if 0 <= x < 8 and 0 <= y < 8 and grid[x][y] == "0":
                            if grid[i][j] == my_color:
                                my_front_tiles += 1
                            else:
                                opp_front_tiles += 1
                            break

        if my_tiles > opp_tiles:
            p = (100.0 * my_tiles) / (my_tiles + opp_tiles)
        elif my_tiles < opp_tiles:
            p = -(100.0 * opp_tiles) / (my_tiles + opp_tiles)
        else:
            p = 0

        if my_front_tiles > opp_front_tiles:
            f = -(100.0 * my_front_tiles) / (my_front_tiles + opp_front_tiles)
        elif my_front_tiles < opp_front_tiles:
            f = (100.0 * opp_front_tiles) / (my_front_tiles + opp_front_tiles)
        else:
            f = 0

        my_tiles = opp_tiles = 0
        if grid[0][0] == my_color:
            my_tiles += 1
        elif grid[0][0] == opp_color:
            opp_tiles += 1
        if grid[0][7] == my_color:
            my_tiles += 1
        elif grid[0][7] == opp_color:
            opp_tiles += 1
        if grid[7][0] == my_color:
            my_tiles += 1
        elif grid[7][0] == opp_color:
            opp_tiles += 1
        if grid[7][7] == my_color:
            my_tiles += 1
        elif grid[7][7] == opp_color:
            opp_tiles += 1
        c = 25 * (my_tiles - opp_tiles)

        my_tiles = opp_tiles = 0
        if grid[0][0] == '0':
            if grid[0][1] == my_color:
                my_tiles += 1
            elif grid[0][1] == opp_color:
                opp_tiles += 1
            if grid[1][1] == my_color:
                my_tiles += 1
            elif grid[1][1] == opp_color:
                opp_tiles += 1
            if grid[1][0] == my_color:
                my_tiles += 1
            elif grid[1][0] == opp_color:
                opp_tiles += 1

        if grid[0][7] == '0':
            if grid[0][6] == my_color:
                my_tiles += 1
            elif grid[0][6] == opp_color:
                opp_tiles += 1
            if grid[1][6] == my_color:
                my_tiles += 1
            elif grid[1][6] == opp_color:
                opp_tiles += 1
            if grid[1][7] == my_color:
                my_tiles += 1
            elif grid[1][7] == opp_color:
                opp_tiles += 1

        if grid[7][0] == '0':
            if grid[7][1] == my_color:
                my_tiles += 1
            elif grid[7][1] == opp_color:
                opp_tiles += 1
            if grid[6][1] == my_color:
                my_tiles += 1
            elif grid[6][1] == opp_color:
                opp_tiles += 1
            if grid[6][0] == my_color:
                my_tiles += 1
            elif grid[6][0] == opp_color:
                opp_tiles += 1

        if grid[7][7] == '0':
            if grid[6][7] == my_color:
                my_tiles += 1
            elif grid[6][7] == opp_color:
                opp_tiles += 1
            if grid[6][6] == my_color:
                my_tiles += 1
            elif grid[6][6] == opp_color:
                opp_tiles += 1
            if grid[7][6] == my_color:
                my_tiles += 1
            elif grid[7][6] == opp_color:
                opp_tiles += 1

        l = -12.5 * (my_tiles - opp_tiles)
        """
        my_tiles = len(self.get_valid_moves(my_color))
        opp_tiles = len(self.get_valid_moves(opp_color))

        if my_tiles > opp_tiles:
            m = (100.0 * my_tiles) / (my_tiles + opp_tiles)
        elif my_tiles < opp_tiles:
            m = -(100.0 * opp_tiles) / (my_tiles + opp_tiles)
        else:
            m = 0
        """
        score = (10 * p) + (801.724 * c) + (382.026 * l) + (78.922 * m) + (74.396 * f) + (10 * d)
        return score

    def __str__(self):
        ret = "\n\n"
        ret += '    0   1   2   3   4   5   6   7\n'
        ret += '  +---+---+---+---+---+---+---+---+\n'
        for x in range(8):
            ret += (str(x) + ' ')
            for y in range(8):
                if self._board[x][y] != "0":
                    ret += '| ' + self._board[x][y] + ' '
                else:
                    ret += '|   '
            ret += '|\n'
            ret += '  +---+---+---+---+---+---+---+---+\n'

        return ret