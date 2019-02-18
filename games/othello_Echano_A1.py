#   Alexis Trys It Again WOO THE 15,000th RETRY!
# Othello

# Name: Alexis Echano    Date: 01.2019

from random import randint

BLANK, WHITE, BLACK, BORDER = '.', 'W', 'B', '#'
TOKENS = [WHITE, BLACK]  # player 1 is white, player 2 is black (AI)
DIRECTIONS = {-1, 1, -9, 9, -10, 11, -11, 10}

BOARD = []  # BOARD is a list

PLAYER_W = 0  # white
PLAYER_B = 1  # black (AI)

def get_legal_moves():  #returns a list of two sets for valid moves
    possible = [[], []]
    dictionaryLIST = [{},{}]

    player_one_color = TOKENS[PLAYER_W]
    player_two_color = TOKENS[PLAYER_B]

    player_one_moves = get_each_legal(player_one_color, player_two_color)
    player_two_moves = get_each_legal(player_two_color, player_one_color)

    possible[PLAYER_W] = player_one_moves[0]
    dictionaryLIST[PLAYER_W] = player_one_moves[1]  #return a dictionary

    possible[PLAYER_B] = player_two_moves[0]
    dictionaryLIST[PLAYER_B] = player_two_moves[1]

    return possible, dictionaryLIST


def update_board(player, move, set_of_flippies):  # make_move (index)
    global BOARD
    color = TOKENS[player]
    BOARD[move] = color
    for s in set_of_flippies:
        BOARD[s] = color

def update_temp_board(copyboard, move, set_of_flippies):    #forecast move
    color = TOKENS[PLAYER_B]
    copyboard[move] = color
    for s in set_of_flippies:
        copyboard[s] = color
    return copyboard

def get_each_legal(player, oop): #combines first and second check
    moves = set()
    the_temp = {}

    for x in range(len(BOARD)):
        if BOARD[x] == BLANK:
            temp_ish = set()
            temp_ish = check_directions(x, player, oop, temp_ish)
            temp = temp_ish[1]
            for t in temp:
                moves.add(t)
                the_temp[t] = temp_ish[0]

    return moves, the_temp

def check_directions(index, player_color, oop_color, list_o_moves):    #first check
    ones_valid = set()

    for d in DIRECTIONS:
        temp_set = set()

        k = index + d

        if((k > 0 and k < len(BOARD)) and (BOARD[k] == oop_color)):
            while BOARD[k] != BORDER and BOARD[k] != BLANK:
                temp_set.add(k)
                if (BOARD[k] == player_color):
                    ones_valid = temp_set
                    list_o_moves.add(index)
                    #break

                k += d

    return ones_valid, list_o_moves



def eval(movez ,time): #time for B M E
    white_count = len(movez[0])
    black_count = len(movez[1])

    if(time == 'B'):
        return black_count
    elif(time == 'M'):
        return black_count - white_count
    else:
        return 0

def determine_time():
    white_count = counter(TOKENS[PLAYER_W])
    black_count = counter(TOKENS[PLAYER_B])

    if(white_count + black_count <= 20):
        return 'B'
    elif(white_count + black_count > 20 and white_count + black_count <= 40):
        return 'M'
    else:
        return 'E'

def AI_player(decision, legal_moves, T):    #decision is M (minimax) or A (alphabeta)            T = beginning, middle, end
    global BOARD

    if(decision == 'M'):
        return minimax(BOARD, legal_moves, T)   #index of move, eval function --> about 64% winning rate
    elif(decision == 'A'):
        return alphabeta(BOARD, legal_moves, -float("inf"), float("inf"), T) #index of move, eval function
    else:
        return random_player(legal_moves[0][1]), 1

def alphabeta(board, moves, a, b, time, depth = 3, maximizing_player=True):
    COPYBOARD = board.copy()

    if depth == 0 or len(moves[0][1]) == 0:   #terminal state
        return -1, eval(moves[0], time)   #eval(time) is eval func when built
    else:
        if(maximizing_player):  #max
            best_val = -float("inf")  # replace with eval function when ready

            for m in moves[0][1]:
                temp = update_temp_board(COPYBOARD, m, moves[1][PLAYER_B][m])
                test = alphabeta(temp, moves, a, b, time, depth - 1, not maximizing_player)[0]

                if test > best_val:
                    best_val = test

                a = max(a, best_val)

                if b <= a:
                    break
                print(best_val)
            return best_val, 0

        else:
            best_val = float("inf")  # replace with eval function when ready

            for m in moves[0][1]:
                temp = update_temp_board(COPYBOARD, m, moves[1][PLAYER_B][m])
                test = alphabeta(temp, moves, a, b, time, depth - 1, not maximizing_player)[0]  # either max or mi

                if test < best_val:
                    best_val = test

                b = min(b, best_val)

                if b <= a:
                    break
            return best_val, 0


def minimax(board, moves, time, depth = 3, maximizing_player=True):
    current_moves = list(moves[0][1])

    COPYBOARD = board.copy()

    if depth == 0 or len(current_moves) == 0:
        return -1, eval(moves[0], time)   #eval(time) is eval func when built
    else:
        get_action = max if maximizing_player else min

        best_val = 0    #replace with eval function when ready
        best_move = current_moves[0]

        for m in current_moves:
            temp = update_temp_board(COPYBOARD, m, moves[1][PLAYER_B][m])
            move, val = minimax(temp, moves, depth-1, not maximizing_player)

            test = get_action(val, best_val)    #either max or min

            if (test != best_val):                                              #change!!!!!
                best_val = val
                best_move = m

        return best_move, test


def display():  # intakes list
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

def counter(player_color):
    count = 0
    for i in BOARD:
        if i == player_color:
            count += 1
    return count

def winner_find():
    global BOARD
    white_count = counter(TOKENS[PLAYER_W])
    black_count = counter(TOKENS[PLAYER_B])

    if white_count > black_count: return 0, (white_count, black_count)
    elif black_count > white_count: return 1, (white_count, black_count)
    return -1, (white_count, black_count)    #no winner

def game_check(): #check if it is over
    if BLANK in BOARD:
        return False
    winner = winner_find()
    return True, winner[0], winner[1]

def create_start_state():   #s is input string
    global BOARD

    for i in range(100):
        if (i % 10 == 0 or i < 10 or (i >= 90 and i < 100) or i%10 == 9):
            BOARD.append(BORDER)
        elif (i == 44 or i == 55):
            BOARD.append(BLACK)
        elif (i == 45 or i == 54):
            BOARD.append(WHITE)
        else:
            BOARD.append(BLANK)

def human_player(color):
    input_string = "Put move index ("+ color+ "): "
    move = input(input_string)
    return move

def random_player(legals):
    legals = list(legals)
    if len(legals) == 0:
        return -1
    random_index = randint(0, len(legals) - 1)

    return legals[random_index]

def play_game():  # fix if any legal move list is empty
    global BOARD
    print("Starting Othello Game...Key for Legal Moves [WHITE, BLACK]")   #change either to human player if needed!
    ask_user = input("Play White as H or R (Human or Random): ").upper()
    print(" ")

    ask_for_AI = input("Play AI as M, A or R (Minimax, Alphabeta or Random): ").upper()
    print(" ")

    start_string = input("Input 64 char start string: ")
    create_start_state()

    display()
    legal_moves = get_legal_moves()

    while not game_check():

        print("Legal Moves: ", legal_moves[0]) #shows legal moves, first one is for white player
        print()

        t = determine_time()

        #AI
        AI_move = int(AI_player(ask_for_AI, legal_moves, t)[0])  #black, second list
        if AI_move != -1:  # skip
            print("BLACK Turn: ", AI_move)
            update_board(PLAYER_B, AI_move, legal_moves[1][PLAYER_B][AI_move])
        else:
            print("No Moves Left for this Player")

        display()
        print()

        #human or other random
        legal_moves = get_legal_moves()
        print("Legal Moves: ", legal_moves[0]) #shows legal moves, first one is for white player
        print()
        the_move = -1

        if(ask_user == "R"):
            the_move = int(random_player(legal_moves[0][0])) #int(human_player())  #white
        elif(ask_user == "H"):
            the_move = int(human_player(TOKENS[PLAYER_W]))  #white

        if the_move != -1:
            print("WHITE Turn: ", the_move)
            print()
            update_board(PLAYER_W, the_move, legal_moves[1][PLAYER_W][the_move])
        else:
            print("No Moves Left for this Player")

        display()
        print()

    print("END GAME...")
    check = game_check()

    print("# of White: ", check[2][0])
    print("# of Black: ", check[2][1])

    if(check[1] == PLAYER_W):
        print("WHITE WINS!")
    elif(check[1] == PLAYER_B):
        print("BLACK WINS!")
    else:
        print("NO ONE WINS!")

def clearboard():
    global BOARD
    BOARD = []

def play_game_100():    #check rates of winning
    global BOARD
    black_wins = 0

    print("checking winning rate for OTHELLO (RANDOM v. AI CHOICE)")   #change either to human player if needed!
    ask_for_AI = input("Play AI as M, A or R (Minimax, Alphabeta or Random): ").upper()
    print(" ")

    clearboard()
    for x in range(100):
        create_start_state()
        legal_moves = get_legal_moves()

        while not game_check():

            t = determine_time()
            AI_move = int(AI_player(ask_for_AI, legal_moves, t)[0])  #black, second list
            if AI_move != -1:  # skip
                update_board(PLAYER_B, AI_move, legal_moves[1][PLAYER_B][AI_move])


            legal_moves = get_legal_moves()
            the_move = int(random_player(legal_moves[0][0])) #int(human_player())  #white

            if the_move != -1:
                update_board(PLAYER_W, the_move, legal_moves[1][PLAYER_W][the_move])

        check = game_check()

        if(check[1] == PLAYER_B):
            black_wins += 1
        clearboard()

    result = "Winning Rate: " + str(black_wins) + "%"
    return result

def main():
    print(play_game_100())
    #play_game()

# runs the entire program...
if __name__ == '__main__':  main()