#strategy.py
#Alexis Echano
#Kim PD. 7
import time
import random



class Strategy():
    # IMPORTANT VARIABLES
    BLANK, WHITE, BLACK, BORDER = '.', 'o', '@', '?'
    TOKENS = [WHITE, BLACK]  # player 1 is white, player 2 is black (AI)
    DIRECTIONS = [-1, 1, -9, 9, -10, 11, -11, 10]

    BOARD = []  # BOARD is a list

    PLAYER_W = 0  # white
    PLAYER_B = 1  # black (AI)

    VALID_DIR = {}  # dictionary to keep track of the valid directions

    #   for eval functions
    EDGES = [12, 13, 14, 15, 16, 17, 21, 28, 31, 38, 41, 48, 51, 58, 61, 68, 71, 78, 82, 83, 84, 85, 86, 87]
    CORNERS = [11, 18, 81, 88]
    ADJ_TO_CORNERS = [12, 21, 17, 28, 71, 82, 78, 87]  # positions near corners
    EDGES_NOT_ADJ = [13, 14, 15, 16, 31, 38, 41, 48, 51, 58, 61, 68, 83, 84, 85, 86]
    #   more complicated eval
    UPPER_LEFT_TRI = [[11], [12, 21], [13, 22, 31], [14, 23, 32, 41]]
    UPPER_RIGHT_TRI = [[18], [17, 28], [16, 27, 38], [15, 26, 37, 48]]
    LOWER_LEFT_TRI = [[81], [71, 82], [61, 72, 83], [51, 62, 73, 84]]
    LOWER_RIGHT_TRI = [[88], [78, 87], [68, 77, 86], [58, 67, 76, 85]]
    WALLS = [13, 14, 15, 16, 31, 41, 51, 61, 83, 84, 85, 86, 38, 48, 58, 68]

    more_fun = [5, -3, 2, 2, 2, 2, -3, 5,
                -3, -5, -1, -1, -1, -1, -5, -3,
                2, -1, 1, 0, 0, 1, -1, 2,
                2, -1, 0, 1, 1, 0, -1, 2,
                2, -1, 0, 1, 1, 0, -1, 2,
                2, -1, 1, 0, 0, 1, -1, 2,
                -3, -5, -1, -1, -1, -1, -5, -3,
                5, -3, 2, 2, 2, 2, -3, 5]

    def best_strategy(self, board, player, best_move, still_running):
        self.string_to_list_BOARD(board)

        player_num = -1

        if player == '@':
            player_num = self.PLAYER_B
        elif player == 'o':
            player_num = self.PLAYER_W

        depth = 2

        while True:
            legal_moves = self.legal(player_num)
            # self.rand(legal_moves)
            best_move.value = self.ultimate(legal_moves, player_num, self.counter(player_num), depth)
            depth += 1


    # BASIC METHODS:
    def clear(self):
        self.BOARD.clear()

    def string_to_list_BOARD(self, s):  # s is input string
        self.reset()
        for char in s:
            self.BOARD.append(char)

    def counter(self, player):  # counts number of tiles on board for one player
        player_color = self.TOKENS[player]

        count = 0
        for i in self.BOARD:
            if i == player_color:
                count += 1
        return count

    def reset(self):
        self.clear()
        self.VALID_DIR.clear()


    # ESSENTIAL GAMEPLAY METHODS:
    def legal(self, player):  # returns set for legal moves for input player
        # retrieves proper color
        color = self.TOKENS[player]

        moves = set()

        self.VALID_DIR.clear()  # each time this resets

        # creates a starting set for blanks
        blanks = set()
        for pos in range(len(self.BOARD)):
            if self.BOARD[pos] == '.':
                blanks.add(pos)

        # uses the blanks set to find valid moves, through directions
        for b in blanks:
            check = self.valid(b, color)
            if check[0]:  # first index is T or F, second is the set of directions that are valid
                moves.add(b)
                self.VALID_DIR[b] = check[1]  # key is index, value is the set of directions to go

        # returns set of valid moves!
        return moves

    def valid(self, move, color):  # helper method to check validity of moves
        valid = False  # boolean for checking
        valid_directions = set()  # use for move methods

        for d in self.DIRECTIONS:  # loops through directions of index
            current = move + d

            if self.BOARD[current] == color:
                continue
            else:
                # if an empty space or it goes out of bounds, no line is formed
                while current > 0 and current < len(self.BOARD) and self.BOARD[current] != self.BLANK and self.BOARD[current] != self.BORDER:
                    # if it reaches color, it forms a line! so it is valid
                    if self.BOARD[current] == color:
                        valid = True
                        valid_directions.add(d)
                        break
                    # move the index according to the direction
                    current += d

        # returns the boolean and its valid directions, if any
        return valid, valid_directions


    def ultimate(self, moves, player, num, d):
        for mo in moves:
            if mo in self.CORNERS:
                return mo

        return self.alphabeta(moves, d, player)

    # RANDOM PLAYER --> can be used for either player, just input the right moves set
    def rand(self, moves):
        legals = list(moves)
        if len(legals) == 0:
            return -1
        random.shuffle(legals)
        return legals[0]


    # EVAL FUNCTIONS FOR PARTS OF GAME
    def get_plays(self, player):
        color = self.TOKENS[player]
        set_of_pos = set()
        for b in range(len(self.BOARD)):
            if self.BOARD[b] == self.TOKENS[player]:
                set_of_pos.add(b)
        return set_of_pos

    def eval(self, moves, player):

        white_occupied = self.get_plays(self.PLAYER_W)
        black_occupied = self.get_plays(self.PLAYER_B)

        together = white_occupied & black_occupied

        num_taken = len(together)

        together_area = len(black_occupied) - len(white_occupied)


        if num_taken <= 8:  # beginning
            return self.simple(moves)
        elif num_taken <= 15:  # middle part 1
            return self.simple(moves) + self.triangle(together, player)
        elif num_taken <= 35:
            return self.simple(moves) + together_area
        else:  # end of game
            return self.simple(moves) + self.weighted(together, player)

    # returns valid moves length
    def simple(self, moves):
        return len(moves)

    def weighted(self, locations, player):
        score = 0
        color = self.TOKENS[player]

        # goes through moves and weights the positions
        for p in locations:
            if self.BOARD[p] == color:
                score += self.more_fun[p-11]
            else:
                score -= self.more_fun[p-11]
        return score


    def triangle(self, locations, player):  # uses triangle evaluation to determine location
        score = 0
        color = self.TOKENS[player]

        TRIANGLES = self.UPPER_LEFT_TRI & self.UPPER_RIGHT_TRI & self.LOWER_LEFT_TRI & self.LOWER_RIGHT_TRI

        for l in locations:  # if part of triangle (corners + adjacents)
            for t in TRIANGLES:
                if l in t:
                    if self.BOARD[l] == color:
                        score += 5
                    else:
                        score -= 5

            if l in self.CORNERS:  # the corners are worth a lot more than the other places
                if self.BOARD[l] == color:
                    score += 10
                else:
                    score -= 10
            else:
                if self.BOARD[l] == color:
                    score += 1
                else:
                    score -= 1
        return score

    # AKA SMART-er AI!
    def temp_board(self, move, player):  # forecast move, essentially like move
        # copies the board
        COPY = self.BOARD.copy()

        # uses tokens and player num index to get color
        player_color = self.TOKENS[player]

        # other player's color (0 or 1)
        other_color = self.TOKENS[1 - player]

        # retrieves directions of movement
        flippies = self.VALID_DIR[move]

        # places one of the player's chips on current move
        COPY[move] = player_color

        for f in flippies:
            current_index = move + f  # begins here

            # until my own color is hit, remain flipping tiles
            while COPY[current_index] != player_color:
                if COPY[current_index] != self.BLANK and COPY[current_index] == other_color:
                    COPY[current_index] = player_color
                current_index += f

        # returns a copy of board with temp move
        return COPY

    # MINIMAX PLAYER
    def minimax(self, moves, d, player):
        # if it is a corner, that is the best move!
        for mo in moves:
            if mo in self.CORNERS:
                return mo
            elif mo in self.EDGES_NOT_ADJ:
                return mo

        # just an initializer to clean up and streamline methods
        return self.minimax_helper(self.BOARD, moves, player, d, -1)[0]  # only returns the move!

    def minimax_helper(self, board, moves, player, depth, a_move, maximizing_player=True):  # returns pos, eval
        if depth == 0 or len(moves) == 0:
            return a_move, self.eval(moves, player)
        else:
            if maximizing_player:
                best_value = -float("inf")
                best_move = a_move

                for m in moves:
                    temp = self.temp_board(m, player)
                    new_move, val = self.minimax_helper(temp, moves, player, depth - 1, m, not maximizing_player)

                    if val > best_value:
                        best_value = val
                        best_move = new_move
                return best_move, best_value

            elif not maximizing_player:
                best_value = float("inf")
                best_move = a_move

                for m in moves:
                    temp = self.temp_board(m, player)
                    new_move, val = self.minimax_helper(temp, moves, player, depth - 1, m, not maximizing_player)

                    if val < best_value:
                        best_value = val
                        best_move = new_move
                return best_move, best_value

    # ALPHABETA PLAYER (minimax + pruning)
    def alphabeta(self, moves, d, player):

        # just an initializer to clean up and streamline methods
        return self.alphabeta_helper(self.BOARD, moves, player, d, -float("inf"), float("inf"), -1)[0]  # only returns the move!

    def alphabeta_helper(self, board, moves, player, depth, a, b, a_move, maximizing_player=True):  # returns pos, eval
        if depth == 0 or len(moves) == 0:
            return a_move, self.eval(moves, player)
        else:
            if maximizing_player:
                v = -float("inf")
                best_move = a_move

                for m in moves:
                    temp = self.temp_board(m, player)
                    new_move, val = self.alphabeta_helper(temp, moves, player, depth - 1, a, b, m, not maximizing_player)

                    if val > v:  # finds max
                        v = val
                        best_move = new_move
                    a = max(a, v)
                    if b <= a:
                        break
                return best_move, v

            elif not maximizing_player:
                v = float("inf")
                best_move = a_move

                for m in moves:
                    temp = self.temp_board(m, player)
                    new_move, val = self.alphabeta_helper(temp, moves, player, depth - 1, a, b, m, not maximizing_player)

                    if val < v:  # finds min
                        v = val
                        best_move = new_move
                    b = min(b, v)
                    if b <= a:
                        break
                return best_move, v

