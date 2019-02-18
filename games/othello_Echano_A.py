# Alexis Echano
# Kim, PD 7
# Othello/Reversi Game

#STRING 64 chars: ...........................@o......o@...........................

#IMPORTS
import random

#IMPORTANT VARIABLES
BLANK, WHITE, BLACK, BORDER = '.', 'O', 'X', '?'    # representations
TOKENS = [WHITE, BLACK]  # player 1 is white, player 2 is black (AI)
DIRECTIONS = [-1, 1, -9, 9, -10, 11, -11, 10]

BOARD = []  # BOARD is a list, indexes 0-99

PLAYER_W = 0  # white
PLAYER_B = 1  # black (AI)

VALID_DIR = {}  #dictionary to keep track of the valid directions...key is the index/move while value is the set of valid directions

#   for eval functions, indexes of corners in BOARD
CORNERS = [11, 18, 81, 88]

#   more complicated eval
#   for triangle ones/diagonal spaces
UPPER_LEFT_TRI = [[11], [12, 21], [13, 22, 31] , [14, 23, 32, 41]]
UPPER_RIGHT_TRI = [[18], [17, 28], [16, 27, 38], [15, 26, 37, 48]]
LOWER_LEFT_TRI = [[81], [71, 82], [61, 72, 83], [51, 62, 73, 84]]
LOWER_RIGHT_TRI = [[88], [78, 87], [68, 77, 86], [58, 67, 76, 85]]

# the 8x8 inside with weights of each position: corner being the best hence heavier weighting
WEIGHTS = [5, -3, 2, 2, 2, 2, -3, 5,
            -3, -5, -1, -1, -1, -1, -5, -3,
            2, -1, 1, 0, 0, 1, -1, 2,
            2, -1, 0, 1, 1, 0, -1, 2,
            2, -1, 0, 1, 1, 0, -1, 2,
            2, -1, 1, 0, 0, 1, -1, 2,
            -3, -5, -1, -1, -1, -1, -5, -3,
            5, -3, 2, 2, 2, 2, -3, 5]

#BASIC METHODS:
def string_to_list_BOARD(s):    #s is input string
    reset()

    temp_inner = []
    for char in s:
        temp_inner.append(char)

    for i in range(100):
        if (i % 10 == 0 or i < 10 or (i >= 90 and i < 100) or i%10 == 9):
            BOARD.append(BORDER)
        else:
            BOARD.append(temp_inner.pop(0))


def display():  # intakes list or string and prints out the board when playing in PyCharm
    index = 0
    print("     1 2 3 4 5 6 7 8 ")
    while index < len(BOARD):
        for x in range(10):
            if(x != 0 and x != 9):
                number = str(x) + "0"
            else:
                number = "  "
            print(number, end=" ")
            for y in range(10):
                print(BOARD[index], end=" ")
                index += 1
            print()
    print()

def counter(player):  # counts number of tiles on board for one player
    player_color = TOKENS[player]

    count = 0
    for i in BOARD:
        if i == player_color:
            count += 1
    return count

def reset():    #resets the board and dictionary of valid directions
    BOARD.clear()
    VALID_DIR.clear()

def create_start_state():   #for when input string is not utilized
    reset()
    for i in range(100):
        if (i % 10 == 0 or i < 10 or (i >= 90 and i < 100) or i%10 == 9):
            BOARD.append(BORDER)
        elif (i == 44 or i == 55):
            BOARD.append(BLACK)
        elif (i == 45 or i == 54):
            BOARD.append(WHITE)
        else:
            BOARD.append(BLANK)

#ESSENTIAL GAMEPLAY METHODS:
def legal(player):    #returns set for legal moves for input player
    #retrieves proper color
    color = TOKENS[player]

    moves = set()

    VALID_DIR.clear()   #each time this resets

    #creates a starting set for blanks
    blanks = set()
    for pos in range(len(BOARD)):
        if BOARD[pos] == '.':
            blanks.add(pos)

    #uses the blanks set to find valid moves, through directions
    for b in blanks:
        check = valid(b, color)
        if check[0]:  #first index is T or F, second is the set of directions that are valid
            moves.add(b)
            VALID_DIR[b] = check[1] #key is index, value is the set of directions to go

    #returns set of valid moves!
    return moves

def valid(move, color):    #helper method to check validity of moves
    valid = False   #boolean for checking
    valid_directions = set()   #use for move methods

    for d in DIRECTIONS:    #loops through directions of index
        current = move + d

        if BOARD[current] == color:
            continue
        else:
            # if an empty space or it goes out of bounds, no line is formed
            while current > 0 and current < len(BOARD) and BOARD[current] != BLANK and BOARD[current] != BORDER:
                # if it reaches color, it forms a line! so it is valid
                if BOARD[current] == color:
                    valid = True
                    valid_directions.add(d)
                    break
                # move the index according to the direction
                current += d

    #returns the boolean and its valid directions, if any
    return valid, valid_directions

#for checking win rate
def quick_make_move(move, player):
    if move != -1:
        #uses tokens and player num index to get color
        player_color = TOKENS[player]

        #other player's color (0 or 1)
        other_color = TOKENS[1-player]

        #retrieves directions of movement
        flippies = VALID_DIR[move]

        #places one of the player's chips on current move
        BOARD[move] = player_color

        #loops through the set of directions from VALID_DIR
        for f in flippies:
            current_index = move + f #begins here

            #until my own color is hit, remain flipping tiles
            while BOARD[current_index] != player_color:
                #   continue until the BOARD hits the player's own color
                if BOARD[current_index] != BLANK and BOARD[current_index] == other_color:
                    BOARD[current_index] = player_color
                current_index += f

def make_move(move, player):
    #checks if move is playable
    if move == -1:
        print("NO MOVES LEFT!")
    else:

        #uses tokens and player num index to get color
        player_color = TOKENS[player]

        #other player's color (0 or 1)
        other_color = TOKENS[1-player]

        #retrieves directions of movement
        flippies = VALID_DIR[move]

        #places one of the player's chips on current move
        BOARD[move] = player_color

        for f in flippies:
            current_index = move + f #begins here

            #until my own color is hit, remain flipping tiles
            while BOARD[current_index] != player_color:
                if BOARD[current_index] != BLANK and BOARD[current_index] == other_color:
                    BOARD[current_index] = player_color
                current_index += f

    #displays current board after move
    display()

def ultimate(moves, player, num):   #work in progress, a mixture of alphabeta and minimax depending on how many pieces
    if num < 25:
        return minimax(moves, player)
    else:
        return alphabeta(moves, player)

#RANDOM PLAYER --> can be used for either player, just input the right moves set
def rand(moves):
    legals = list(moves)
    if len(legals) == 0:
        return -1
    print("White's Possible Moves:", moves)
    random.shuffle(legals)
    return legals[0]

#HUMAN PLAYER --> can be used for either player, just input the right moves set
def human(moves):
    if len(moves) != 0:
        print("Your Possible Moves:", moves)
    else:
        print("No Possible Moves, Press Enter")
    choice = input("Put your move index: ")
    return int(choice)

#EVAL FUNCTIONS FOR PARTS OF GAME
def get_plays(player):  #like counter but specific to eval functions and returns the actual values of each taken pos
    set_of_pos = set()
    for b in range(len(BOARD)):
        if BOARD[b] == TOKENS[player]:
            set_of_pos.add(b)
    return set_of_pos

def eval(moves, player):    #determines which function to use based on the above method's return length

    ONE_occupied = get_plays(player)    #current player
    TWO_occupied = get_plays(1-player)  #opponent

    together = ONE_occupied & TWO_occupied  #combines the two sets --> basically non blank spaces
    together_area = len(ONE_occupied) - len(TWO_occupied)   #FOR AREA EVALUATION AND FOR THE END

    num_taken = len(together)   #used to determine beginning, middle or end

    #each one uses simple to determine mobility
    if num_taken <= 16:  #beginning
        return simple(moves)
    elif num_taken <= 35:   #middle, triangle eval used to be here
        return simple(moves) + weighted(together, player)
    else:   #end of game
        return simple(moves) + together_area

#returns valid moves length
def simple(moves):
    return len(moves)

#returns the score based on the WEIGHTS list above
def weighted(locations, player):
    score = 0
    color = TOKENS[player]

    #goes through moves and weights the positions
    for p in locations:
        if BOARD[p] == color:   #if own color, add to the score
            score += WEIGHTS[p-11]
        else:
            score -= WEIGHTS[p-11]  #if not, subtract
    return score


#NOT IN USE...EXTRA #4 EVAL FUNC
def triangle(locations, player):    #uses triangle evaluation to determine location --> DIAGONALS!
    score = 0
    color = TOKENS[player]

    #combines the indexes so it just checks all at once
    TRIANGLES = UPPER_LEFT_TRI & UPPER_RIGHT_TRI & LOWER_LEFT_TRI & LOWER_RIGHT_TRI

    for l in locations: #if part of triangle (corners + adjacents)
        for t in TRIANGLES:
            if l in t:
                if BOARD[l] == color:
                    score += 5
                else:
                    score -= 5

        if l in CORNERS:    #the corners are worth a lot more than the other places
            if BOARD[l] == color:
                score += 10
            else:
                score -= 10
        else:
            if BOARD[l] == color:
                score += 1
            else:
                score -= 1
    return score

#AKA SMART-er AI!
def temp_board(move, player):    #forecast move, essentially like move
    #copies the board
    COPY = BOARD.copy()

    # uses tokens and player num index to get color
    player_color = TOKENS[player]

    # other player's color (0 or 1)
    other_color = TOKENS[1 - player]

    # retrieves directions of movement
    flippies = VALID_DIR[move]

    # places one of the player's chips on current move
    COPY[move] = player_color

    for f in flippies:
        current_index = move + f  # begins here

        # until my own color is hit, remain flipping tiles
        while COPY[current_index] != player_color:
            if COPY[current_index] != BLANK and COPY[current_index] == other_color:
                COPY[current_index] = player_color
            current_index += f

    #returns a copy of board with temp move
    return COPY

#MINIMAX PLAYER
def minimax(moves, player):
    #if it is a corner, that is the best move!
    for mo in moves:
        if mo in CORNERS:
            return mo

    #just an initializer to clean up and streamline methods
    return minimax_helper(BOARD, moves, player, 3, -1)[0]   #only returns the move!

def minimax_helper(board, moves, player, depth, a_move, maximizing_player = True):  #returns pos, eval
    #   base case, returns if no more depth left or empty legal moves
    if depth == 0 or len(moves) == 0:
        #returns current move in args and the eval func for given time
        return a_move, eval(moves, player)
    else:
        #goes if max player
        if maximizing_player:
            #sets up arbitrary initial vals
            best_value = -float("inf")
            best_move = a_move

            #loops through moves
            for m in moves:
                temp = temp_board(m, player)
                #recurs after forecasting move
                new_move, val = minimax_helper(temp, moves, player, depth - 1, m, not maximizing_player)

                #finds max and sets the new values accordingly
                if val > best_value:
                    best_value = val
                    best_move = new_move
            #returns
            return best_move, best_value

        #same as above, just with min player
        elif not maximizing_player:
            best_value = float("inf")
            best_move = a_move

            for m in moves:
                temp = temp_board(m, player)
                new_move, val = minimax_helper(temp, moves, player, depth - 1, m, not maximizing_player)

                if val < best_value:
                    best_value = val
                    best_move = new_move
            return best_move, best_value

#ALPHABETA PLAYER (minimax + pruning)
def alphabeta(moves, player):
    # if it is a corner, that is the best move!
    for mo in moves:
        if mo in CORNERS:
            return mo

    #just an initializer to clean up and streamline methods
    return alphabeta_helper(BOARD, moves, player, 4, -float("inf"), float("inf"), -1)[0]   #only returns the move!

def alphabeta_helper(board, moves, player, depth, a, b, a_move, maximizing_player = True):  #returns pos, eval
    #   base case, returns if no more depth left or empty legal moves
    if depth == 0 or len(moves) == 0:
        # returns current move in args and the eval func for given time
        return a_move, eval(moves, player)
    else:
        #max player, so it changes alpha
        if maximizing_player:
            #sets v to - infinity
            v = -float("inf")
            best_move = a_move

            #loops thru moves
            for m in moves:
                #forecasts move and recurs
                temp = temp_board(m, player)
                new_move, val = alphabeta_helper(temp, moves, player, depth - 1, a, b, m, not maximizing_player)

                if val > v: #finds max
                    v = val
                    best_move = new_move
                #sets alpha to the larger of the v OR alpha itself
                a = max(a, v)

                #b is the best val in MIN so once it is less than a, WE HAVE FOUND THE BEST VALUE AND MOVE
                if b <= a:
                    break
            #returns the move and val
            return best_move, v

        #like above but min
        elif not maximizing_player:
            v = float("inf")
            best_move = a_move

            for m in moves:
                temp = temp_board(m, player)
                new_move, val = alphabeta_helper(temp, moves, player, depth - 1, a, b, m, not maximizing_player)

                if val < v: #finds min
                    v = val
                    best_move = new_move
                b = min(b, v)
                if b <= a:
                    break
            return best_move, v

#MAIN METHOD + PLAYING
def play():
    #sets up game
    print("PLAYING OTHELLO")
    print()

    #input from user
    PLAYER_B_CHOICE = input("Play AI as R (RANDOM), M (MINIMAX), or A (ALPHABETA): ").upper()
    PLAYER_W_CHOICE = input("Play as R (RANDOM), or H (HUMAN): ").upper()

    #sets up and prints the board
    #create_start_state()
    display()

    while BLANK in BOARD:   #while there are still blanks, play the game
        #generates sets of legal moves each turn
        black_moves = legal(PLAYER_B)
        if len(black_moves)!= 0:
            print("AI's Possible Moves:", black_moves)

        # black, usually the AI, goes first
        if PLAYER_B_CHOICE == 'R':
            black_move = rand(black_moves)                                        #CHANGE TYPE OF GAMEPLAY HERE!
        elif PLAYER_B_CHOICE == 'M':
            black_move = minimax(black_moves, PLAYER_B)
        elif PLAYER_B_CHOICE == 'A':
            black_move = alphabeta(black_moves, PLAYER_B)
            #black_move = ultimate(black_moves, PLAYER_B, counter(PLAYER_B))
        else:
            print("INVALID CHOICE! WILL PLAY AS RANDOM")
            black_move = rand(black_moves)

        # makes the move
        print("Black Moves to", black_move)
        make_move(black_move, PLAYER_B)

        #######################################################
        print("-----------------------")

        #generates sets of legal moves each turn
        white_moves = legal(PLAYER_W)

        #white next
        if PLAYER_W_CHOICE == 'R':
            white_move = rand(white_moves)                                        #CHANGE TYPE OF GAMEPLAY HERE!
        elif PLAYER_W_CHOICE == 'H':
            white_move = human(white_moves)
        else:
            print("INVALID CHOICE! WILL PLAY AS RANDOM")
            white_move = rand(black_moves)

        #makes the move
        if white_move != -1:
            print("White Moves to", white_move)
        make_move(white_move, PLAYER_W)
        print("-----------------------")

    #checks who wins by counting the number of pieces
    num_blacks = counter(PLAYER_B)
    num_whites = counter(PLAYER_W)

    #shows the score
    print("# of BLACK:", num_blacks)
    print("# of WHITE:", num_whites)

    #determines winner
    if num_blacks > num_whites:
        print("BLACK WINS!")
    elif num_blacks < num_whites:
        print("WHITE WINS!")
    else:
        print("TIE!")

def play100():                                                                   #check win rate, plays 100 times
    print("CHECKING WIN RATE FOR OTHELLO")
    wins = 0

    for i in range(100):
        create_start_state()
        while BLANK in BOARD:  # while there are still blanks, play the game

            # generates sets of legal moves each turn
            black_moves = legal(PLAYER_B)

            # black, usually the AI, goes first

            #black_move = rand(black_moves)                                    #CHANGE TYPE OF GAMEPLAY HERE!
            #black_move = minimax(black_moves, PLAYER_B)
            #black_move = alphabeta(black_moves, PLAYER_B)
            black_move = ultimate(black_moves, PLAYER_B, counter(PLAYER_B))

            quick_make_move(black_move, PLAYER_B)

            #######################################################

            # generates sets of legal moves each turn
            white_moves = legal(PLAYER_W)

            # white next
            white_move = rand(white_moves)  # CHANGE TYPE OF GAMEPLAY HERE!
            quick_make_move(white_move, PLAYER_W)

        num_blacks = counter(PLAYER_B)

        if num_blacks > 32:
            wins += 1
        print(i)
        #time.sleep(2)

    print("Win Rate:", wins)

def main():
    #"""

    #main gameplay
    input_string = input("ENTER 64 CHAR STRING: ")
    if len(input_string) != 64:
        print("not proper length")
    else:
        string_to_list_BOARD(input_string)
        play()


    #"""

    #to check winning rate --> VERY VARIABLE!!! CHANGE IN METHOD FOR SETTINGS
    #play100()

# runs the entire program...
if __name__ == '__main__':  main()
#XXXXXXX..XXXOOOO.XOOXOOOXXOXOXOOOXOOOOO..X.OOXXOXXXXXXXX....OXXX