import random
import sys
import pygame

puz = [[0] * 9 for i in range(9)]


row = [{j: False for j in range(1, 10)} for i in range(9)]
col = [{j: False for j in range(1, 10)} for i in range(9)]
block = [{j: False for j in range(1, 10)} for i in range(9)]

# Puzzle generator logic


def block_idx(x, y):
    """Find the index of 3x3 block corresponding to (x, y)"""
    if 0 <= x < 3:
        if 0 <= y < 3:
            return 0
        elif 3 <= y < 6:
            return 3
        else:
            return 6
    if 3 <= x < 6:
        if 0 <= y < 3:
            return 1
        elif 3 <= y < 6:
            return 4
        else:
            return 7
    if 6 <= x < 9:
        if 0 <= y < 3:
            return 2
        elif 3 <= y < 6:
            return 5
        else:
            return 8


def reset():
    """Reset the row, col and block dict to empty dict"""
    global row, col, block
    row = [{j: False for j in range(1, 10)} for i in range(9)]
    col = [{j: False for j in range(1, 10)} for i in range(9)]
    block = [{j: False for j in range(1, 10)} for i in range(9)]


def its(row, col, block):
    """Find the intersection between row, column and block lists"""
    return {
        item: True for item in row.keys() if not (row[item] or col[item] or block[item])
    }


def sol_gen(x, y):
    """Generate a sodoku solution"""
    if y == 9:
        return True
    elif x == 9:
        return sol_gen(0, y + 1)

    choices = its(row[y], col[x], block[block_idx(x, y)])

    while len(choices) > 0:
        puz[y][x] = random.choice(list(choices.keys()))
        row[y][puz[y][x]] = col[x][puz[y][x]
                                   ] = block[block_idx(x, y)][puz[y][x]] = True
        if sol_gen(x + 1, y):
            return True

        choices.pop(puz[y][x], None)

        row[y][puz[y][x]] = col[x][puz[y][x]] = False
        block[block_idx(x, y)][puz[y][x]] = False

        puz[y][x] = 0
    return False


def puz_gen(mode: str):
    """Generate the puzzle"""
    if mode == "h":
        k = 60
    elif mode == "m":
        k = 52
    else:
        k = 44

    possible_coor = {}

    for y in range(9):
        for x in range(9):
            possible_coor[(x, y)] = True

    while k > 0:
        k -= 1

        x, y = random.choice(list(possible_coor.keys()))
        puz[y][x] = 0
        possible_coor.pop((x, y), None)


def print_soduku():

    print("-" * 12 + " " + "-" * 11 + " " + "-" * 12 + " ")
    for y in range(9):
        print("| ", end="")
        for x in range(9):
            if puz[y][x] == 0:
                tmp = ' '
            else:
                tmp = str(puz[y][x])
            print(tmp + " | ", end="")
        print()
        if (y - 2) * (y - 5) * (y - 8) == 0:
            print("-" * 12 + " " + "-" * 11 + " " + "-" * 12 + " ")

# end of logic


# UI

pygame.init()


class InputBox:

    def __init__(self, x, y, w, h, text=''):
        self.x, self.y = x, y
        self.cs = w  # cs: cell size
        self.rect = pygame.Rect(x, y, w, h)
        self.color = (255, 255, 255)
        self.text = text
        self.txt_surface = pygame.font.Font(
            None, 32).render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = (30, 30, 255) if self.active else (255, 255, 255)
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    if self.text != '':
                        puz[self.y // self.cs][self.x //
                                               self.cs] = int(self.text)
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif len(self.text) == 0:
                    if str(event.unicode).isdigit():
                        self.text += event.unicode
                elif len(self.text) == 1:
                    if str(event.unicode).isdigit():
                        self.text = ''
                        self.text += event.unicode
                # Re-render the text.
                self.txt_surface = pygame.font.Font(
                    None, 32).render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)


def main():

    cell_size = 60
    width, height = cell_size*9, cell_size*9
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Sudoku")

    black = (0, 0, 0)
    white = (255, 255, 255)
    gray = (200, 200, 200)
    blue = (50, 50, 255)
    red = (255, 30, 30)
    green = (30, 255, 30)

    button_width, button_height = 150, 50
    button_x = [(width - button_width) // 2 for i in range(3)]
    button_y = [i*70 + 150 for i in range(1, 4)]
    choice = [['e', 'Easy'], ['m', 'Medium'], ['h', 'Hard']]

    input_boxes = []

    running = True
    playing = False
    created = False
    boxes = False
    mode = None

    solution = [[0]*9 for i in range(9)]
    marked = [[0]*9 for i in range(9)]

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif not playing and event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for i in range(3):
                    if (
                        button_x[i] < mouse_x < button_x[i] + button_width
                        and button_y[i] < mouse_y < button_y[i] + button_height
                    ):
                        playing = True
                        mode = choice[i][0]

            for box in input_boxes:
                box.handle_event(event)

        screen.fill(white)

        if playing:

            if not created:
                reset()
                sol_gen(0, 0)
                for y in range(9):
                    for x in range(9):
                        solution[y][x] = puz[y][x]
                print_soduku()
                puz_gen(mode)
                created = True

            if boxes:
                for box in input_boxes:
                    box.draw(screen)

            for i in range(1, 9):
                if i % 3 != 0:
                    border_size = 2
                else:
                    border_size = 6
                pygame.draw.line(screen, black, (0, i * cell_size),
                                 (width, i * cell_size), border_size)

            for i in range(1, 9):
                if i % 3 != 0:
                    border_size = 2
                else:
                    border_size = 6
                pygame.draw.line(screen, black, (i * cell_size, 0),
                                 (i * cell_size, height), border_size)

            for y in range(9):
                for x in range(9):
                    if puz[y][x]:
                        if puz[y][x] == solution[y][x] and marked[y][x]:
                            color = green
                        elif puz[y][x] == solution[y][x]:
                            color = black
                        else:
                            color = red
                        text = pygame.font.Font(None, 48).render(
                            str(puz[y][x]), True, color)
                        screen.blit(text, text.get_rect(
                            center=(x*cell_size + cell_size//2, y*cell_size + cell_size//2)))

                    elif not boxes:
                        box = InputBox(x*cell_size, y * cell_size,
                                       cell_size, cell_size)
                        marked[y][x] = 1
                        input_boxes.append(box)

            boxes = True

        else:
            text = pygame.font.Font(None, 84).render(
                "Sudoku", True, blue)
            screen.blit(text, text.get_rect(
                center=(button_x[0] + button_width // 2, 100)))

            for i in range(3):
                pygame.draw.rect(screen, gray, (button_x[i], button_y[i],
                                                button_width, button_height))
                pygame.draw.rect(screen, black, (button_x[i], button_y[i],
                                                 button_width, button_height), 2)
                text = pygame.font.Font(None, 32).render(
                    choice[i][1], True, black)
                screen.blit(text, text.get_rect(
                    center=(button_x[i] + button_width // 2, button_y[i] + button_height // 2)))

        pygame.display.flip()

    pygame.quit()
    sys.exit()


main()
