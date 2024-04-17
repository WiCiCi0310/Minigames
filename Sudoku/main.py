import sys
from puzzle_generator import *
from gui_component import *

pygame.init()


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

    puz = None
    solution = None
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
                tmp = SudokuPuzzle(mode)
                puz = tmp.getPuzzle()
                solution = tmp.getSolution()

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
                                       cell_size, cell_size, puz)
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


if __name__ == "__main__":
    main()
