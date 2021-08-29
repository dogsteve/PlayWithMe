import random
import time
# các biến cục bộ : người chơi, bàn cờ

BOT = 'x'
HUMAN = 'o'

# BOARD = [
#         ['x', 'x', '_'],
#         ['x', 'o', '_'],
#         ['_', '_', '_']
# ]

# 5x5 board
BOARD = [
    ['x', '_', '_', 'o', 'o'],
    ['x', 'x', 'o', 'o', '_'],
    ['x', 'x', 'o', 'o', '_'],
    ['o', 'o', 'o', 'o', '_'],
    ['x', 'x', 'x', 'x', '_']
]

# trạng thái mặc định của alpha và beta
ALPHA_DEFAULT = -9999
BETA_DEFAULT = 9999

# hàm tính toán các vị trí còn lại để tính điểm (heuristic)


def get_absolute_score(board):
    count = 0
    for i in board:
        for j in i:
            if (j == '_'):
                count = count + 1
    return count


# hàm tính điểm khi trạng thái kết thúc của game (1 trong 2 đã thắng)
# sửa một chút cho phù hợp với bảng 5x5
def get_score(board):
    # hàng ngang / dọc
    for i in range(len(board)):
        # cột
        if (board[i][0] == board[i][1] and board[i][1] == board[i][2] and board[i][2] == board[i][3] and board[i][3] == board[i][4]):
            if (board[i][0] == BOT):
                # cộng thêm 1 vì trong trường hợp thắng mà không còn ô nào trống thì không bị nhập nhằng với hòa
                return (get_absolute_score(board) + 1)
            if (board[i][0] == HUMAN):
                # người là min và bot là max
                return 0 - (get_absolute_score(board) + 1)
        # hàng
        if (board[0][i] == board[1][i] and board[1][i] == board[2][i] and board[2][i] == board[3][i] and board[3][i] == board[4][i]):
            if (board[0][i] == BOT):
                return (get_absolute_score(board) + 1)
            if (board[0][i] == HUMAN):
                return 0 - (get_absolute_score(board) + 1)
        # chéo xuôi "/"
        if (board[4][0] == board[3][1] and board[3][1] == board[2][2] and board[2][2] == board[1][3] and board[1][3] == board[0][4]):
            if (board[2][2] == BOT):
                return (get_absolute_score(board) + 1)
            if (board[2][2] == HUMAN):
                return 0 - (get_absolute_score(board) + 1)
        # chéo ngược \
        if (board[0][0] == board[1][1] and board[1][1] == board[2][2] and board[2][2] == board[3][3] and board[3][3] == board[4][4]):
            if (board[2][2] == BOT):
                return (get_absolute_score(board) + 1)
            if (board[2][2] == HUMAN):
                return 0 - (get_absolute_score(board) + 1)
    return 0


# hàm min max
# thêm độ sâu để giới hạn thời gian di tính toán
def min_max(board, is_max, alpha, beta, depth, start_time):
    score = get_score(board)
    # nếu đến độ sâu giới hạn mà chưa xong cây thì trả về giá trị của node đang tính
    if(depth == 0 or time.time()  > start_time + 5):
        return score
    if(score > 0):
        return score
    if(score < 0):
        return score
    # nếu chưa ai win mà hết vị trí return 0 (draw)
    if(get_absolute_score(board) == 0):
        return 0
    # lượt của max
    if (is_max):
        # mặc định điểm tốt nhất của max là -infinity
        best_score = -9999
        # tìm xem điểm nào chưa đi thì đi vào với giá trị của maximizer (bot)
        for i in range(len(board)):
            for j in range(len(board)):
                if (board[i][j] == '_'):
                    board[i][j] = BOT
                    # tìm giá trị của node đang xét với turn của max (giá trị lớn nhất của các node con)
                    # các nốt dưới max là min turn , chúng sẽ đệ quy cho đến trạng thái kết thúc rồi quay ngược lại về để gán giá trị vào node của max
                    best_score = max(best_score, min_max(
                        board, not is_max, alpha, beta, depth - 1, start_time))
                    # alpha là max của tất cả các nút đến thời điểm xét
                    alpha = max(best_score, alpha)
                    # sau khi có gtri của node (best_score) thì xóa đi node đã đi để tránh nhập nhằng cho lần đệ quy sau
                    board[i][j] = '_'
                    if (alpha >= beta):
                        break
        # trả về giá trị của node
        return best_score
    # tương tự với lượt của min
    if (not is_max):
        # mặc định điểm tốt nhất của min là +infinity
        best_score = 9999
        # tìm xem điểm nào chưa đi thì đi vào với giá trị của human
        for i in range(len(board)):
            for j in range(len(board)):
                if (board[i][j] == '_'):
                    board[i][j] = HUMAN
                    # ở đây lấy min
                    # các nốt con là max turn
                    best_score = min(best_score, min_max(
                        board, is_max, alpha, beta, depth - 1, start_time))
                    # beta là min của tát cả các nút đến thời điểm xét
                    beta = min(best_score, beta)
                    # sau khi có gtri của node (best_score) thì xóa đi node đã đi để tránh nhập nhằng cho lần đệ quy sau
                    board[i][j] = '_'
                    if (alpha >= beta):
                        break
        # trả về giá trị của node
        return best_score


# hàm di chuyển của bot
def bot_move(board):
    # như min_max nhưng chỉ lấy phần max vì bot là max
    # đây là điểm giả sử của node
    best_score = -9999
    # tọa độ mặc định của nước đi
    position = [-1, -1]
    time_start = time.time()
    for i in range(len(board)):
        for j in range(len(board)):
            if (board[i][j] == '_'):
                board[i][j] = BOT
                child_value = min_max(
                    board, False, ALPHA_DEFAULT, BETA_DEFAULT, 25, time_start)
                board[i][j] = '_'
                if (child_value > best_score):
                    best_score = child_value
                    position[0] = i
                    position[1] = j
    # print("this is best_core " + str(best_score))
    # print("position " + str(position))
    return position


# gameplay
def set_anotation(bot, human):
    global BOT
    global HUMAN
    BOT = bot
    HUMAN = human
    print("Bot will be " + BOT + " and You will be " + HUMAN)


def print_board(board):
    for i in board:
        for j in i:
            print(j, end="  |  ")
        print("\n")


def human_move():
    while(True):
        x = int(input("Enter x position of " + HUMAN + " : "))
        y = int(input("Enter y position of " + HUMAN + " : "))
        if (BOARD[y-1][x-1] == '_'
                    and x > 0 and x < 6
                    and y > 0 and y < 6
                ):
            BOARD[y-1][x-1] = HUMAN
            return
        else:
            print("Not valid move !")
            continue


def game_loop():
    turn = True
    human_player = input("Choose your symbol : ")
    if (human_player == 'x'):
        bot_player = 'o'
    else:
        bot_player = 'x'
    set_anotation(bot_player, human_player)
    turn_selection = input("You wanna go first ? ")
    if (turn_selection == 'y' or turn_selection == 'Y'):
        turn = False
    else:
        turn = True
    while(True):
        if (turn):
            position = bot_move(BOARD)
            BOARD[position[0]][position[1]] = BOT
            turn = False
            print("----- Bot turn -----")
        else:
            human_move()
            turn = True
            print("---- Human turn ----")
        print_board(BOARD)


# hủy comment để chạy trương trình
# game_loop()

print(bot_move(BOARD))
