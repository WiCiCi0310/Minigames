import sys
import pygame

# Bot engine


def is_in_board(x, y):
    return 0 <= x < size and 0 <= y < size


def is_win(x, y, player):
    '''
    Check if player or computer wins the game
    '''
    global turn
    if turn:
        score_system = get_4_dir_score(x, y, player)
        if 1 in score_system[5].values():
            print(player + ' win')
            turn = False


def get_possible_moves():
    '''
    Return the list of blank cells which locate within the
    region of radius 3 centered at an occupied cell
    '''
    occupied_cells = []
    moves = []
    for i in range(size):
        for j in range(size):
            if board[j][i] != '_':
                occupied_cells.append((i, j))
    for oc in occupied_cells:
        x, y = oc
        for i in range(max(0, x - 2), min(15, x + 3)):
            for j in range(max(0, y - 2), min(15, y + 3)):
                if (i, j) not in moves and (i, j) not in occupied_cells:
                    moves.append((i, j))
    return moves


def init_score_system(score4dir):
    '''
    Init a score system from dictionary whose keys are directions
    and values are the list get from get_list_score()
    '''
    score_system = {0: {}, 1: {}, 2: {}, 3: {}, 4: {}, 5: {}, -1: {}}
    for key in score4dir.keys():
        for score in score4dir[key]:
            if key in score_system[score].keys():
                score_system[score][key] += 1
            else:
                score_system[score][key] = 1
    return score_system


def sum_of_score_system(score_system):
    '''
    Sum all the values of all directions of a score
    '''
    for score in score_system:
        if score == 5:
            score_system[5] = int(1 in score_system[5].values())
        else:
            score_system[score] = sum(score_system[score].values())


def get_list_of_cc(coord_s, coord_d, dx, dy):
    '''
    Get the list of the consecutive cells from (x_s, y_s) to (x_d, y_d)
    _s for source, _d for destination
    '''
    list = []
    x_s, y_s = coord_s
    x_d, y_d = coord_d
    while x_s != x_d + dx or y_s != y_d + dy:
        list.append(board[y_s][x_s])
        x_s += dx
        y_s += dy
    return list


def count_list(list, player):
    '''
    Count the frequencies of the player's symbol to calculate score
    '''
    blank = list.count('_')
    p_filled = list.count(player)
    if blank + p_filled < 5:
        return -1
    elif blank == 5:
        return 0
    return p_filled


def get_list_score(coord_s, coord_d, dx, dy, player):
    '''
    Count the frequencies of the player's symbol of all
    subarray length 5 from a list of consecutive cells
    '''
    p_scores = []
    list = get_list_of_cc(coord_s, coord_d, dx, dy)
    for i in range(len(list) - 4):
        score = count_list(list[i:i+5], player)
        p_scores.append(score)
    return p_scores


def get_coord(x, y, dx, dy, length):
    '''
    Return the coordinate of the cell that have the max distance
    to (x,y) within length
    '''
    x += dx * length
    y += dy * length
    while not is_in_board(x, y):
        x -= dx
        y -= dy
    return (x, y)


def get_4_dir_score(x, y, player):
    '''
    Calculate scores of 4 directions of a cell
    '''
    score4dir = {'r': [], 'c': [], 'd1': [], 'd2': []}
    global testx, testy, testplay
    testx = x
    testy = y
    testplay = player

    score4dir['r'].extend(get_list_score(
        get_coord(x, y, -1, 0, 4),
        get_coord(x, y, 1, 0, 4), 1, 0, player))

    score4dir['c'].extend(get_list_score(
        get_coord(x, y, 0, -1, 4),
        get_coord(x, y, 0, 1, 4), 0, 1, player))

    score4dir['d1'].extend(get_list_score(
        get_coord(x, y, -1, -1, 4),
        get_coord(x, y, 1, 1, 4), 1, 1, player))

    score4dir['d2'].extend(get_list_score(
        get_coord(x, y, 1, -1, 4),
        get_coord(x, y, -1, 1, 4), -1, 1, player))

    a = init_score_system(score4dir)

    return a


def winning_case_34(score3, score4):
    '''
    This is the winning case which have a direction that have four
    consecutive player's symbol with at most one bound (bị chặn một đầu),
    and a different direction that have three consecutive player's symbol
    with no bound (không bị chặn đầu nào)
    '''
    for dir4 in score4:
        if score4[dir4] >= 1:
            for dir3 in score3:
                if dir3 != dir4 and score3[dir3] >= 2:
                    return True
    return False


def winning_case(score_system):
    '''
    Return the values of the corresponding winning case
    '''
    if 1 in score_system[5].values():
        return 5
    elif len(score_system[4]) >= 2 or \
            (len(score_system[4]) >= 1 and max(score_system[4].values()) >= 2):
        return 4
    elif winning_case_34(score_system[3], score_system[4]):
        return 4
    else:
        score3 = sorted(score_system[3].values(), reverse=True)
        if len(score3) >= 2 and score3[0] >= score3[1] >= 2:
            return 3
    return 0


def score(x, y, player, const):
    '''
    Calculate the score of a player if they make a move to (x,y)
    const is a big number use to multiply with the winning_case() values
    to make that move be prioritized
    '''
    res = 0
    board[y][x] = player
    score_system = get_4_dir_score(x, y, player)
    res += winning_case(score_system) * const
    sum_of_score_system(score_system)
    res += score_system[-1] + score_system[1]*2 + \
        score_system[2]*4 + score_system[3]*8 + score_system[4]*16
    board[y][x] = '_'
    return res


def get_move_score(x, y, player):
    '''
    Evaluate the total score of 2 player if they make a move to (x,y)
    '''
    enemy = 'X'
    return score(x, y, player, 1000) + score(x, y, enemy, 900)


def make_decision(player):
    '''
    Choose the best moves which has the largest scores
    '''
    moves = get_possible_moves()
    current_choice = (0, 0)
    max_score = -1
    for move in moves:
        x, y = move
        score = get_move_score(x, y, player)
        if score > max_score:
            max_score = score
            current_choice = move
    return current_choice

# end of bot engine


pygame.init()

size = 15
board = [['_']*size for i in range(size)]
symb = ["O", "X"]


cell_size = 40
width, height = cell_size * size, cell_size * size
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Gomoku (with tictactoe symbols) go brrrrrrr")


white = (255, 255, 255)
black = (0, 0, 0)

font = pygame.font.Font(None, 30)
text = [font.render("O", True, (0, 0, 255)),
        font.render("X", True, (255, 0, 0))]
text_rect = {}

turn = True
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and turn:
            mx, my = pygame.mouse.get_pos()
            for x_p in range(size):
                for y_p in range(size):
                    if (x_p*cell_size < mx < (x_p+1)*cell_size and y_p*cell_size < my < (y_p+1)*cell_size):
                        if (str(x_p) + str(y_p)) not in text_rect.keys():
                            text_rect[str(x_p) + str(y_p)] = [text[int(turn)], text[int(turn)
                                                                                    ].get_rect(center=(x_p*cell_size + cell_size/2, y_p*cell_size + cell_size/2))]
                            board[y_p][x_p] = symb[int(turn)]
                            is_win(x_p, y_p, symb[int(turn)])
                            if turn:
                                x_c, y_c = make_decision(symb[int(not turn)])
                                text_rect[str(x_c) + str(y_c)] = [text[int(not turn)], text[int(not turn)
                                                                                            ].get_rect(center=(x_c*cell_size + cell_size/2, y_c*cell_size + cell_size/2))]
                                board[y_c][x_c] = symb[int(not turn)]
                                is_win(x_c, y_c, symb[int(not turn)])

    # Draw the board
    screen.fill(white)
    for k in text_rect.keys():
        screen.blit(text_rect[k][0], text_rect[k][1])

    # Draw horizontal lines
    for i in range(1, size):
        pygame.draw.line(screen, black, (0, i * cell_size),
                         (width, i * cell_size), 2)

    # Draw vertical lines
    for i in range(1, size):
        pygame.draw.line(screen, black, (i * cell_size, 0),
                         (i * cell_size, height), 2)

    pygame.display.flip()

pygame.quit()
sys.exit()
