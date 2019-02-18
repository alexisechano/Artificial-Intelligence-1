#Alexis Echano
#Tic-Tac-Toe    12/3/2018

#global variables:
#board

#state = string of the input
#state_dict = dictionary of indexes and their X and O values

def main_method():
    global board
    input_string = input("Enter input string: ")

    if(len(input_string) != 9):
        print("Invalid input")

    else:
        print("GAME START!!!")
        positions = create_map_positions()
        curr_sym, board = determine_start(input_string)
        display(board)

        if(check_finished(board, 'X')):
            print("Game Over! X Wins!")
        elif(check_finished(board, 'O')):
            print("Game Over! O Wins!")
        else:
            #initiate game
            if(curr_sym == 'O'):
                user_turn_solver(positions)

            print("Computer's Turn")
            board, u = AI_turn_solver(board)
            display(board)

            if (check_finished(board, 'O')):
                print("Game Over! O Wins!")
            if (check_finished(board, 'X')):
                print("Game Over! X Wins!")

            else:
                while(not complete(board)):
                    user_turn_solver(positions)
                    if(not complete(board)):
                        print("Computer's Turn")
                        board, u = AI_turn_solver(board)
                        display(board)
                    if(check_finished(board, 'O')):
                        print("Game Over! O Wins!")
                        break
                    if(check_finished(board, 'X')):
                        print("Game Over! X Wins!")
                        break
                    elif(complete(board)):
                        print("No One Wins")

def complete(state):
    if (check_finished(state, 'O')):
        return True
    elif (check_finished(state, 'X')):
        return True
    for i in state.keys():
        if(state[i] == '.'):
            return False
    return True

def determine_start(state):    #returns start_symbol, map
    state_dict_create, symbol = create_map_symbols(state)
    return symbol, state_dict_create

def user_turn_solver(p):    #allows user to solve
    for choice in give_user_choices(board, p):
        print(choice)

    print(" ")
    choice_spot = int(input("What's your move? (input index) "))

    board[choice_spot] = 'O'
    display(board)

def AI_turn_solver(state_dict):
    global board
    board, u = minmax_decision(state_dict)
    return board, u

def minmax_decision(state_dict):

    copydict = state_dict.copy()    #creates a temp
    v, value = max_val(state_dict, -1)  #returns the -1, 0, 1 AND the index
    copydict[value] = 'X'   #sets that index to an X or the AI turn

    state_dict = copydict
    return state_dict, v    #returns the -1, 0, or 1 (to determine who wins) and the dictioanry

def max_val(state_dict, i):   #each state needs to be assigned -1, 0 ,1
    test = terminal_test(state_dict)    #checks if done and returns -1, 0, 1

    if test[0]: #checks if terminal
        return (test[1], i) #returns the number and the index

    v = -10000

    for s in sucessors(state_dict): #goes through indexes with a '.'
        state_dict[s] = 'X'
        v = max(v, min_val(state_dict, s)[0])   #finds the mathematical max between the current v and the previous
        i = s   #i is the index
    return v, i

def min_val(state_dict, i):
    test = terminal_test(state_dict)

    if test[0]:
        return (test[1], i)

    v = 10000
    index = -2
    for s in sucessors(state_dict):     #successors need to be entire dictionaries
        state_dict[s] = 'X'
        v = min(v, max_val(state_dict, s)[0])
        index = s
    return v, index

def sucessors(state_dict):  #returns a list of the indexes
    list_empties = []

    for val in state_dict.keys():
        if(state_dict[val] == '.'):
            list_empties.append(val)  #utility val
    return list_empties

def give_user_choices(state_dict, positions):   #JUST PRINTS the empty spaces where O can go
    list_of_choices = []

    for val in state_dict.keys():
        if(state_dict[val] == '.'):
            string_output = '[' + str(val) + ']' + " " + str(positions[val])
            list_of_choices.append(string_output)

    return list_of_choices

def terminal_test(state_dict):    #if both are -1, then return 0
    val_x = check_finished(state_dict, 'X')
    val_o = check_finished(state_dict, 'O')

    if(val_o):
        value = 1
    elif(val_x):
        value = -1
    elif(not val_x and not val_o):
        value = 0
    return complete(board) or val_x or val_o, value

def check_finished(state, symbol):   #return -1 if not, 1 if one works
    if((state[0] == symbol and state[4] == symbol and state[8] == symbol) or
            (state[2] == symbol and state[4] == symbol and state[6] == symbol)or
            (state[0] == symbol and state[1] == symbol and state[2] == symbol)or
            (state[3] == symbol and state[4] == symbol and state[5] == symbol)or
            (state[6] == symbol and state[7] == symbol and state[8] == symbol)or
            (state[0] == symbol and state[3] == symbol and state[6] == symbol)or
            (state[1] == symbol and state[4] == symbol and state[7] == symbol)or
            (state[2] == symbol and state[5] == symbol and state[8] == symbol)):
        return True

    return False

def create_map_symbols(state):  #creates the current and assumes X has first move
    return_dict = {}

    num_x = 0
    num_o = 0

    index = 0
    for s in state:
        return_dict[index] = s
        if(s == 'X'):
            num_x += 1
        elif(s == 'O'):
            num_o += 1
        index += 1

    if(num_x > num_o):
        return return_dict, 'O' # user turns first
    elif(num_x == num_o):
        return return_dict, 'X'  # AI turns first


def create_map_positions():   #index: (row, col)
    map_game = {}

    x = 0
    i = 0

    while i < 9:
        while x < 3:
            y = 0
            while y < 3:
                map_game[i] = (y,x)
                y += 1
                i += 1
            x += 1

    return map_game

def display(state_dict):
    print(" ")
    for val in state_dict.keys():
        print(state_dict[val], end=" ")
        if val == 2 or val == 5 or val == 8:
            print("")
    print(" ")


#run the main
main_method()