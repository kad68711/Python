import numpy as np
import random
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


def bot_O():
    # cor_o = list(map(int, input(
    #     '''Position for O in row space column format eg 1 2 which is 2nd row
    #
    #         3rd column since counting in python starts from 0: ''').split()))   this code not required for the bot

    def checkforcompletex_row():

        z = 0
        for row in tic_tacbox:
            i = 0

            for value in row:

                if value == "X":
                    i += 1
                if i == 2:
                    for l in range(len(row)+1):

                        if tic_tacbox[z][l] == " ":
                            tic_tacbox[z][l] = "O"
                            z=0
                            return False
                        else:
                            z=0
                            return True

            z += 1
        return True

    def checkforcompletex_rowaftertransposing():

        global tic_tacbox
        tic_tacbox = tic_tacbox.transpose()
        z = 0
        for row in tic_tacbox:
            i = 0

            for value in row:

                if value == "X":
                    i += 1
                if i == 2:
                    for l in range(len(row)+1):

                        if tic_tacbox[z][l] == " ":
                            tic_tacbox[z][l] = "O"
                            tic_tacbox = tic_tacbox.transpose()
                            z=0
                            return False
                        else:
                            tic_tacbox = tic_tacbox.transpose()
                            z=0
                            return True

                z += 1
        tic_tacbox = tic_tacbox.transpose()
        return True

    if checkforcompletex_row():

        if checkforcompletex_rowaftertransposing():

            x = random.randint(0, 2)
            y = random.randint(0, 2)
            if tic_tacbox[x][y] == " ":
                tic_tacbox[x][y] = "O"

            else:
                # "ALready filled" thus repeating
                bot_O()


def winner_checker():
    global game_on
    z = 0
    for row in tic_tacbox:
        for value in row:
            if value == " ":
                z += 1
                if z == 0:
                    return False

    for row in tic_tacbox:
        i = 0
        j = 0
        for item in row:
            if item == "X":
                i += 1
            elif item == "Y":
                j += 1
        if i == 3:
            print("X wins")
            return False
        elif j == 3:
            print("Y wins")
            return False
    tranposed_box = tic_tacbox.transpose()
    for row in tranposed_box:
        i = 0
        j = 0
        for item in row:
            if item == "X":
                i += 1
            elif item == "Y":
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
    if winner_checker() == False:
        break
    box_printer()
    bot_O()  # change from the 2 player code
    if winner_checker() == False:
        break
