import numpy as np
tic_tacbox = np.array([
    [" ", " ", " "],
    [" ", " ", " "],
    [" ", " ", " "]])


def box_printer():
    i = 0
    z = 0
    for rows in tic_tacbox:
        i += 1
        for r in rows:
            z += 1
            if z < 3:
                print(r, end=" | ")
            else:
                z = 0
                print(r, end=" ")
        print("")
        if i < 3:
            print("---------")


def X():
    cor_x = list(map(int, input(
        '''Position for X in row space column format eg 1 2 which is 2nd row 
            3rd column since counting in python starts from 0: ''').split()))
    try:
        if tic_tacbox[cor_x[0]][cor_x[1]] == " ":
            tic_tacbox[cor_x[0]][cor_x[1]] = "X"
        else:
            print("ALready filled")
            X()

    except:
        print("OUT OF RANGE")
        X()


def O():
    cor_o = list(map(int, input(
        '''Position for O in row space column format eg 1 2 which is 2nd row 
            3rd column since counting in python starts from 0: ''').split()))
    try:
        if tic_tacbox[cor_o[0]][cor_o[1]] == " ":
            tic_tacbox[cor_o[0]][cor_o[1]] = "O"
        else:
            print("ALready filled")
            O()
    except:
        print("OUT OF RANGE")
        O()


def winner_checker():
    global game_on
    for row in tic_tacbox:
        i = 0
        j = 0
        for item in row:
            if item == "X":
                i += 1
            elif item == "O":
                j += 1
        if i == 3:
            print("X wins")
            return False
        elif j == 3:
            print("O wins")
            return False
    tranposed_box = tic_tacbox.transpose()
    for row in tranposed_box:
        i = 0
        j = 0
        for item in row:
            if item == "X":
                i += 1
            elif item == "O":
                j += 1
        if i == 3:
            print("X wins")
            return False
        elif j == 3:
            print("O wins")
            return False
    if np.array_equal(np.diag(tic_tacbox), np.array(["O", "O", "O"])):
        print("O wins")
        return False
    elif np.array_equal(np.diag(tic_tacbox), np.array(["X", "X", "X"])):
        print("X wins asgag")
        return False


game_on = True

while game_on:
    box_printer()
    X()
    if winner_checker()==False:
        break
    box_printer()
    O()
    if winner_checker()==False:
        break
    
