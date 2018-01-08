import copy
import time

'''
input file
n  - width and height of square board (0<n<=26)
p  - # of diff types of fruits (0<p<=9)
t  - remaining time in sec (positive floating point no.)
n*n board

output file
your move - eg A15 or D7
n*n board with move
'''


def input_board( inputfile, board, n):
    for i in xrange(n):
        lst = [char for char in inputfile.readline().rstrip('\n')]
        board.append(lst)


def output_board(outputfile, board):
    lst1 = []
    for lst in board:
        string1 = ''.join(lst)
        lst1.append(string1)
    string = '\n'.join(lst1)
    outputfile.write(string)


def output_move(move):
    outputfile.write('%s' % chr(int(move[1])+65))
    outputfile.write('%s' % str(move[0]+1))
    outputfile.write('\n')


def generate_moves(board, n):
    move_2dlist = []
    move = 0
    temp_list = []
    move_dict = {}  # dictionary for move : tiles in that move
    # for last line
    if board[n-1][0] == '*':
        temp_list.append('*')
    else:
        temp_list.append('0')
        move_dict.setdefault('0', []).append((n-1,0))
    for j in range(1,n):
        if board[n-1][j] == '*':
            temp_list.append('*')
        elif board[n-1][j] == board[n-1][j-1]:
            temp_list.append(str(temp_list[-1]))
            move_dict.setdefault(str(move), []).append((n - 1, j))
        else:
            move += 1
            temp_list.append(str(move))
            move_dict.setdefault(str(move), []).append((n - 1, j))
    move_2dlist.append(temp_list)

    # other lines
    for i in range(n-2, -1, -1):
        temp_list1 = []
        # first element of the column
        if board[i][0] == '*':
            temp_list1.append('*')
        else:
            if board[i][0] == board[i+1][0]:
                temp_list1.append(move_2dlist[0][0])
                move_dict.setdefault(str(temp_list1[-1]), []).append((i, 0))
            else:
                move += 1
                temp_list1.append(str(move))
                move_dict.setdefault(str(temp_list1[-1]), []).append((i, 0))
        # other elements of the column
        for j in range(1, n, 1):
            if board[i][j] == '*':
                temp_list1.append('*')
                continue
            else:
                if board[i][j] == board[i][j-1] and board[i][j] == board[i+1][j]:
                    temp_list1.append(move_2dlist[0][j])
                    move_dict.setdefault(str(move_2dlist[0][j]), []).append((i, j))
                    temp_list1_copy = copy.deepcopy(temp_list1)
                    # change previous entries with move_2dlist[i+1][j]
                    for k in range(j-1,-1,-1):
                        if k == 0:
                            garbage = move_dict[str(temp_list1[k])].pop()
                            temp_list1[k] = temp_list1[-1]
                            move_dict.setdefault(str(temp_list1[k]), []).append(garbage)
                            break
                        elif temp_list1[k] == temp_list1_copy[k-1] and temp_list1[k] is not '*':
                            garbage = move_dict[str(temp_list1[k])].pop()
                            temp_list1[k] = temp_list1[-1]
                            move_dict.setdefault(str(temp_list1[k]), []).append(garbage)
                        else:
                            garbage = move_dict[str(temp_list1[k])].pop()
                            temp_list1[k] = temp_list1[-1]
                            move_dict.setdefault(str(temp_list1[k]), []).append(garbage)
                            break
                elif board[i][j] == board[i][j-1]:
                    temp_list1.append(temp_list1[-1])
                    move_dict.setdefault(str(temp_list1[-1]), []).append((i, j))
                elif board[i][j] == board[i+1][j]:
                    temp_list1.append(move_2dlist[0][j])
                    move_dict.setdefault(str(move_2dlist[0][j]), []).append((i, j))
                else:
                    move += 1
                    temp_list1.append(str(move))
                    move_dict.setdefault(str(temp_list1[-1]), []).append((i, j))
        move_2dlist.insert(0, temp_list1)
    for j in range (0,n):  # col
        for i in range(0,n-1):  #row
            if board[i][j] == board[i+1][j] and board[i][j] is not '*':
                move_2dlist[i+1][j] = move_2dlist[i][j]
    for i in range (0,n):  # row
        for j in range(n-1,0,-1):  # col
            if board[i][j] == board[i][j-1] and board[i][j] is not '*':
                move_2dlist[i][j-1] = move_2dlist[i][j]
    return move_dict


def apply_move(moved_board, n, move_dict, move):
    if move in move_dict:
        for value in move_dict[move]:
            moved_board[value[0]][value[1]] = '*'
    for j in range(0,n):  # loop for col in matrix
        for k in range(0,n):   # loop for swapping all the stars
            for i in range(n-1,0,-1):  # loop for row in matrix
                if moved_board[i][j] == '*' and moved_board[i-1][j] != '*':
                    moved_board[i][j] = moved_board[i-1][j]
                    moved_board[i - 1][j] = '*'
    return moved_board


def minimax(board,alpha,beta, n, depth):
    move_dict = generate_moves(board, n)
    available_moves = move_dict.keys()
    bmove = available_moves[0]  # best move
    bscore = float('-inf')  # best score
    for move in available_moves:
        c_board = copy.deepcopy(board)
        new_board = apply_move(c_board, n, move_dict, move)
        score = min_player(new_board,alpha,beta,n,depth)
        if score > bscore:
            bmove = move
            bscore = score
    return bmove


def min_player(a_board,alpha,beta,n,depth):
    move_dict = generate_moves(a_board, n)
    #print 'min depth : %d' % depth
    e_time = time.time() - s_time
    if depth == 4 or (e_time <= (t-10)):
        eval_score = 0
        for move in move_dict:
            l = move_dict[move]
            ll = len(l)
            if ll > eval_score:
                eval_score = ll
        return eval_score
    if len(move_dict.keys()) == 1:
        for move in move_dict:
            l = move_dict[move]
        return len(l)  # return score if game over
    available_moves = move_dict.keys()
    bscore = float('inf')  # best score
    for move in available_moves:
        b_board = copy.deepcopy(a_board)
        new_board = apply_move(b_board, n, move_dict, move)
        score = max_player(new_board,alpha,beta, n, depth+1)
        if score <= alpha:
            return alpha
        if score < beta:
            beta = score
    return beta


def max_player(a_board,alpha,beta,n,depth):
    move_dict = generate_moves(a_board, n)
    #print 'max depth : %d' % depth
    e_time = time.time() - s_time
    if depth == 4 or (e_time <= (t-10)):
        eval_score = 0
        for move in move_dict:
            l = move_dict[move]
            ll = len(l)
            if ll > eval_score:
                eval_score = ll
        return eval_score
    if len(move_dict.keys()) == 1:
        for move in move_dict:
            l = move_dict[move]
        return len(l) # return score if game over
    available_moves = move_dict.keys()
    bscore = float('-inf')  # best score
    for move in available_moves:
        b_board = copy.deepcopy(a_board)
        new_board = apply_move(b_board, n, move_dict, move)
        score = min_player(new_board,alpha,beta, n, depth+1)
        if score >= beta:
            return beta
        if score > alpha:
            alpha = score
    return alpha

s_time = time.time()
inputfile = open("input.txt", "r")
outputfile = open("output.txt", "w")

n = int(inputfile.readline())  # n is height-width of square board
p = int(inputfile.readline())  # no. of diff types of fruits
t = float(inputfile.readline())  # remaining time in sec
inputboard = []  # 2D list for board
input_board(inputfile, inputboard, n)
board = copy.deepcopy(inputboard)

move_dict = generate_moves(inputboard,n)

if t > 10:
    depth = 0  # initialize with zero and stop at 5
    move = minimax(board, float('-inf'), float('inf'), n, depth)
else:
    l = move_dict.keys()
    move = l[0]
print move

inputboard = apply_move(inputboard, n, move_dict, move)
move_vertice = move_dict[move][0]
output_move(move_vertice)
output_board(outputfile, inputboard)

inputfile.close()
outputfile.close()