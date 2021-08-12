import random

# BOARD = [
#     ['_', '_', '_', '_', '_'],
#     ['_', '_', '_', '_', '_'],
#     ['_', '_', '_', '_', '_'],
#     ['_', '_', '_', '_', '_'],
#     ['_', '_', '_', '_', '_']
# ]

BOARD = [
    ['_', '_', '_'],
    ['_', '_', '_'],
    ['_', '_', '_']
]

alpha_default_value = -9999
beta_default_value = 9999

def final_score_checker(board, bot_player):
    
    if ( board[0][0] == board[1][1] and
         board[1][1] == board[2][2]
        #  board[2][2] == board[3][3] and
        #  board[4][4] == board[4][4]
         ):
        if(board[0][0] == bot_player):
            return 1
        elif (board[0][0] != '_'):
            return -1

    if ( board[2][0] == board[1][1] and
         board[1][1] == board[0][2]
        #  board[2][2] == board[1][3] and
        #  board[1][3] == board[0][4]
         ):
        if ( board[2][2] == bot_player):
            return 1
        elif ( board[2][2] != '_'):
            return -1
    
    for i in range(len(board)):

        if ( board[i][0] == board[i][1] and
             board[i][1] == board[i][2]
            #  board[i][2] == board[i][3] and
            #  board[i][3] == board[i][4]
             ):
            if (board[i][0] == bot_player):
                return 1
            elif (board[i][0] != '_'):
                return -1

        if ( board[0][i] == board[1][i] and
             board[1][i] == board[2][i]
            #  board[2][i] == board[3][i] and
            #  board[3][i] == board[4][i]
             ):
            if (board[0][i] == bot_player):
                return 1
            elif (board[0][i] != '_'):
                return -1 
    
    return 0

def any_space_left(board):

    for i in board:
        for j in i:
            if (j == '_'):
                return True

    return False


def minmax (board, is_maximizer, bot_player, alpha, beta):
    
    if (final_score_checker(board,bot_player) == 1):
        return 1
    
    if (final_score_checker(board, bot_player) == -1):
        return -1

    if (not any_space_left(board)):
        return 0    

    human_player = 'N'

    if (bot_player == 'x'):
        human_player = 'o'
    elif (bot_player == 'o'):
        human_player = 'x'

    
    if (is_maximizer):

        this_node_score = -9999

        for i in range(len(board)):
            for j in range(len(board)):

                if (board[i][j] == '_'):

                    board[i][j] = bot_player

                    this_node_score = max(this_node_score, minmax(board, False, bot_player, alpha, beta))

                    board[i][j] = '_'
                    
                    alpha = max(alpha, this_node_score)

                    if (alpha >= beta):
                        break
                        

        return this_node_score

    if (not is_maximizer):

        this_node_score = 9999

        for i in range(len(board)):
            for j in range(len(board)):

                if (board[i][j] == '_'):

                    board[i][j] = human_player

                    this_node_score = min(this_node_score, minmax(board, True, bot_player, alpha, beta))

                    board[i][j] = '_'

                    beta = min(beta, this_node_score)

                    if (alpha >= beta):
                        break

        return this_node_score
    
def make_a_move(board, bot_player):

    best_score = -9999
    position = [-1,-1]
    for i in range(len(board)):
            for j in range(len(board)):

                if (board[i][j] == '_'):

                    board[i][j] = bot_player
                    child_node_score = minmax(board, False, bot_player, alpha_default_value, beta_default_value)
                    board[i][j] = '_'

                    if (child_node_score > best_score):
                        best_score = child_node_score
                        position[0] = i
                        position[1] = j   

    return position

def human_move(player_notation):

    while(True):
        x = int(input("enter x position of " + player_notation + " : "))
        y = int(input("enter y position of " + player_notation + " : "))
        if (BOARD[y-1][x-1] == '_'
            and x > 0 and x < 4
            and y > 0 and y < 4
        ):
            BOARD[y-1][x-1] = player_notation
            return
        else:
            continue

def print_board(board):
    for i in board:
        for j in i:
            print (j, end="  |  ")
        print("\n")

def game_loop():

    bot_move_pos = [-1,-1]

    turn = True
    bot_player = 'N'
    player_notation = input("what do you choose x/o : ")
    hard_level = int(input("choose a level 1 is hard, 2 is insane : "))
    player_turn = input("do you want to go first y/n : ")



    if (player_notation == 'o'):
        player = 'o'
        bot_player = 'x'
    elif (player_notation == 'x'):
        player = 'x'
        bot_player = 'o'



    if (player_turn == 'y' or player_turn == 'Y'):
        turn = True
    elif (player_turn == 'n' or player_turn == 'N'):
        turn = False



    while(True):
        if (turn):
            human_move(player)
            turn = False
        else:
            if (hard_level == 2):
                BOARD[random.randint(0,2)][random.randint(0,2)] = bot_player
            bot_move_pos = make_a_move(BOARD, bot_player)
            BOARD[bot_move_pos[0]][bot_move_pos[1]] = bot_player
            turn = True
        print_board(BOARD)
        print('************************')

game_loop()

        
    

