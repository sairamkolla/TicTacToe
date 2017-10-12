import sys
import random
import time


class Player40:
    def __init__(self):
        print "file is successfully imported"
        # You may initialize your object here and use any variables for storing throughout the game
        pass

    def move(self, temp_board, temp_block, old_move, flag):
        print "I am " + str(flag)
        # print time.ctime()
        # print "flag is " + flag
        if old_move[0] == -1 and old_move[1] == -1:
	    return (3,3)
	cells = get_cells(temp_board, temp_block, old_move, flag)
        her_value = -100
        result = cells[0]
        print "my possible moves are"
        print cells
        for move in cells:
            make_move(temp_board, move, flag)
            temp_her_value = alphabeta(temp_board, temp_block, get_opponent(flag), flag, move, -100, 100, 0)
            if temp_her_value == 100:
                print "move returned is" + str(move)
                print "breaking"
                make_move(temp_board, move, '-')
                return move
            if temp_her_value > her_value:
                result = move
                her_value = temp_her_value
            make_move(temp_board, move, '-')
        # print time.ctime()

        print "move returned is" + str(result)
        return result




        # Choose a move based on some algorithm, here it is a random move.



        # return cells[random.randrange(len(cells))]


def make_move(game_board, move, symbol):
    game_board[move[0]][move[1]] = symbol
    # print str(move) + "  move made by " + symbol
    return


def alphabeta(present_config, block_config, player, main_player, old_move, alpha, beta, depth):
    if depth >= 4:
        return get_heruistics_score(present_config, main_player, block_config)

    moves = get_cells(present_config, block_config, old_move, player)
    for move in moves:
        make_move(present_config, move, player)
        val = alphabeta(present_config, block_config, get_opponent(player), main_player, move, alpha, beta, depth + 1)
        make_move(present_config, move, '-')
        if player == main_player:
            if val > alpha:
                alpha = val
            if alpha >= beta:
                return alpha
        else:
            if val < beta:
                beta = val
            if beta <= alpha:
                return beta
    if player == main_player:
        return alpha
    else:
        return beta


def get_cells(temp_board, temp_block, old_move, flag):
    block_number = get_old__block_number(old_move[0], old_move[1])
    blocks_allowed = get_valid_blocks(block_number, temp_block)
    #   print "blocks allowed are " + str(blocks_allowed)
    return get_cells_in_blocks(temp_board, blocks_allowed, temp_block)


def get_valid_blocks(block_number, game_map):
    try:
        initial_blocks = {
            0: [1, 3],
            1: [0, 2],
            2: [1, 5],
            3: [0, 6],
            4: [4],
            5: [2, 8],
            6: [3, 7],
            7: [6, 8],
            8: [5, 7]
        }[block_number]
    except:
        sys.exit(1)

    # print initial_blocks
    x = []
    for block in initial_blocks:
        if game_map[block] == '-':
            x.append(block)
    if x == []:
        for i in range(9):
            if game_map[block] == '-':
                x.append(i)
    # print x
    return x


def get_old__block_number(x, y):
    row = x % 3
    col = y % 3
    return row * 3 + col


def get_cells_in_blocks(board_arrangement, blocks_to_test, blocks_map):
    cells = []
    for block in blocks_to_test:
        id1 = block / 3
        id2 = block % 3
        for i in range(id1 * 3, id1 * 3 + 3):
            for j in range(id2 * 3, id2 * 3 + 3):
                if board_arrangement[i][j] == '-':
                    cells.append((i, j))
    if not len(cells):
        new_blal = []
        all_blal = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        for i in all_blal:
            if blocks_map[i] == '-':
                new_blal.append(i)

        for idb in new_blal:
            id1 = idb / 3
            id2 = idb % 3
            for i in range(id1 * 3, id1 * 3 + 3):
                for j in range(id2 * 3, id2 * 3 + 3):
                    if board_arrangement[i][j] == '-':
                        cells.append((i, j))
    return cells


def get_heruistics_score(game_map, symbol, blocks_map):
    prob = [0] * 9
    for i in range(9):

        if blocks_map[i] == symbol:
            prob[i] = 1
        elif blocks_map[i] == 'D':
            prob[i] = 0
        elif blocks_map[i] == get_opponent(symbol):
            prob[i] = -1
        else:
            prob[i] = get_local_heruistics(game_map, symbol, blocks_map, i)

    final_her = 0
    # print prob
    # print "final caluculating"
    # print "horizontal"
    # horizontal
    for i in range(3):
        local_sum = prob[3 * i] + prob[3 * i + 1] + prob[3 * i + 2]
        temp_her = calculator(local_sum)
        if temp_her == 100:
            return 100
        elif temp_her == -100:
            return -100
        else:
            final_her += temp_her

    # print "vertical"
    # vertical
    for i in range(3):
        local_sum = prob[i] + prob[i + 3] + prob[i + 6]
        temp_her = calculator(local_sum)
        if temp_her == 100:
            return 100
        elif temp_her == -100:
            return -100
        else:
            final_her += temp_her

    # print "diagnol"
    # diagnol1
    temp_her = calculator(prob[0] + prob[4] + prob[8])
    if temp_her == 100:
        return 100
    elif temp_her == -100:
        return -100
    else:
        final_her += temp_her

    # diagnol2
    temp_her = calculator(prob[2] + prob[4] + prob[6])
    if temp_her == 100:
        return 100
    elif temp_her == -100:
        return -100
    else:
        final_her += temp_her

    if final_her > 100:
        final_her = 100
    elif final_her < -100:
        final_her = -100

    # print "final her is " + str(final_her)
    return final_her


def calculator(local_sum):
    # print "local_sum is " + str(local_sum)
    if local_sum == -3:
        # print "returned 100"
        return -100
    elif local_sum > -3 and local_sum < -2:
        # print "returned " +str(90*local_sum)
        return -10 + (local_sum + 2) * 90
    elif local_sum == -2:
        # print "returned -10"
        return -10
    elif local_sum > -2 and local_sum < -1:
        # print "returned " + str(9*local_sum)
        return -1 + 9 * (local_sum + 1)
    elif local_sum == -1:
        # print "returned -1"
        return -1
    elif local_sum > -1 and local_sum < 0:
        # print "returned " + str(local_sum)
        return local_sum
    elif local_sum == 0:
        # print "returned 0"
        return 0
    elif local_sum > 0 and local_sum < 1:
        # print "returned " + str(local_sum)
        return local_sum
    elif local_sum == 1:
        # print "returned 1"
        return 1
    elif local_sum > 1 and local_sum < 2:
        # print "returned " + str(9 * local_sum)
        return 1 + 9 * (local_sum - 1)
    elif local_sum == 2:
        # print "returned 10"
        return 10
    elif local_sum > 2 and local_sum < 3:
        # print "returned " + str(90 * local_sum)
        return 10 + 90 * (local_sum - 2)
    elif local_sum == 3:
        # print "returned 100"
        return 100


def get_local_heruistics(game_map, symbol, blocks_map, block_number):
    col = (block_number % 3) * 3
    row = (block_number / 3) * 3

    vertical_score = 0
    horizontal_score = 0
    diagnol_score = 0

    # print "vertically"
    for i in range(col, col + 3):
        mysymbol_count = 0
        oppsymbol_count = 0
        spaces = 0
        for j in range(row, row + 3):
            if game_map[j][i] == symbol:
                mysymbol_count += 1
            elif game_map[j][i] == get_opponent(symbol):
                oppsymbol_count += 1
            elif game_map[j][i] == '-':
                spaces += 1

        if mysymbol_count == 1 and spaces == 2:
            vertical_score += 1
        elif mysymbol_count == 2 and spaces == 1:
            vertical_score += 10
        elif oppsymbol_count == 1 and spaces == 2:
            vertical_score -= 1
        elif oppsymbol_count == 2 and spaces == 1:
            vertical_score -= 10
        elif mysymbol_count == 3:
            vertical_score += 100
            return 1
        elif oppsymbol_count == 3:
            vertical_score -= 100
            return -1
    # Horizontal lines
    for i in range(row, row + 3):
        mysymbol_count = 0
        oppsymbol_count = 0
        spaces = 0
        for j in range(col, col + 3):
            if game_map[i][j] == symbol:
                mysymbol_count += 1
            elif game_map[i][j] == get_opponent(symbol):
                oppsymbol_count += 1
            elif game_map[i][j] == '-':
                spaces += 1
        if mysymbol_count == 1 and spaces == 2:
            horizontal_score += 1
        elif mysymbol_count == 2 and spaces == 1:
            horizontal_score += 10
        elif oppsymbol_count == 1 and spaces == 2:
            horizontal_score -= 1
        elif oppsymbol_count == 2 and spaces == 1:
            horizontal_score -= 10
        elif mysymbol_count == 3:
            horizontal_score += 100
            return 1
        elif oppsymbol_count == 3:
            horizontal_score -= 100
            return -1
    for direction in (1, -1):

        if direction == 1:
            temp_row = row
            temp_col = col
        elif direction == -1:
            temp_row = row
            temp_col = col + 2
        mysymbol_count = 0
        oppsymbol_count = 0
        spaces = 0

        for i in range(3):
            if game_map[temp_row + i][temp_col + i * direction] == symbol:
                mysymbol_count += 1
            elif game_map[temp_row + i][temp_col + i * direction] == get_opponent(symbol):
                oppsymbol_count += 1
            elif game_map[temp_row + i][temp_col + i * direction] == '-':
                spaces += 1

        if mysymbol_count == 1 and spaces == 2:
            diagnol_score += 1
        elif mysymbol_count == 2 and spaces == 1:
            diagnol_score += 10
        elif oppsymbol_count == 1 and spaces == 2:
            diagnol_score -= 1
        elif oppsymbol_count == 2 and spaces == 1:
            diagnol_score -= 10
        elif mysymbol_count == 3:
            diagnol_score += 100
            return 1
        elif oppsymbol_count == 3:
            diagnol_score -= 100
            return -1
    total_score = vertical_score + horizontal_score + diagnol_score
    # print "horizontal for  " + str(block_number) + "  is " + str(horizontal_score)
    # print "vertical for  " + str(block_number) + "  is " + str(vertical_score)
    # print "diagnol for  " + str(block_number) + "  is " + str(diagnol_score)

    # print "total for " + str(block_number) + "  is " + str(total_score)
    # print "----------------------------"

    # print "total for " + str(block_number) + "  is " + str(float(total_score) / float(100))
    return float(total_score) / float(100)


def get_opponent(a):
    return 'x' if a == 'o' else 'o'


def print_board(gb, bs):
    print '=========== Game Board ==========='
    for i in range(9):
        if i > 0 and i % 3 == 0:
            print
        for j in range(9):
            if j > 0 and j % 3 == 0:
                print " " + gb[i][j],
            else:
                print gb[i][j],

        print
    print "=================================="

    print "=========== Block Status ========="
    for i in range(0, 9, 3):
        print bs[i] + " " + bs[i + 1] + " " + bs[i + 2]
    print "=================================="
    print
