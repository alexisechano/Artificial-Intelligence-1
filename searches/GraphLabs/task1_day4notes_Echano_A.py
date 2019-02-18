# Alexis Echano
# Day 4 Notes: Task 1 (Revisit lab 1)

def findInversion(state):   #finds inversions of state and returns value
    inversions = 0

    for i in range(8):
        for j in range(1,9):
            if(state[i] > state[j]):
                inversions+=1
    return inversions

def randomGeneratorStates(s): #function to find all permutations of goal state
    if(len(s) == 1):    #when the length of the input string is only a char
        return s

    thePerm = randomGeneratorStates(s[1:])    #recursive function beginning at the 2nd char
    c = s[0]    #the first char
    newArr = [] #new list for the permutations

    for p in thePerm:   #for all of the possibilities from the recursive
        for i in range(len(p) + 1):
            newPerm = p[:i] + c + p[i:] #creates a new permutation by adding the char
            newArr.append(newPerm)
    return newArr   #returns the list


def main():
    #opens file for writing:
    solvable_text = open("solvable_8_puzzle.txt", 'w')

    allStates = randomGeneratorStates("012345678")
    solvables = [] #solvable states, should be 181440 items

    for s in allStates: #checks every single state
        inv = findInversion(s)  #finds inversion value of each state
        if(inv%2 == 0): #if inversion is even , it is solvable
            solvables.append(s) #added to solvable list

    for item in solvables:  #writes to text file
        solvable_text.write(item + "\n")
    print("Number of Solvable States: ", len(solvables))

    solvable_text.close()

if __name__ == '__main__':
    main()