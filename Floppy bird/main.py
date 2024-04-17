from typing import Literal
from os.path import join
from datetime import datetime
import pygame
import os
import random


WIDTH = 336
HEIGHT = 512 + 112
VELO = 2
ACC = 0.3
FPS = 60
PIPE_DIS = 250
OPPOSITE_PIPE_DIS = 100

pygame.init()
pygame.mixer.init()

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Floppy bird")
pygame.display.set_icon(pygame.image.load("assets/favicon.ico"))

clock = pygame.time.Clock()


def load_background(bg_type: str):
    path = join("assets", "bg", bg_type + ".png")
    bg = pygame.image.load(path)
    bg = pygame.transform.scale(
        bg, (bg.get_width() * 7 / 6, bg.get_height() * 7 / 6))
    return bg


def load_bird(bird_type: str):
    dir = join("assets", "bird", bird_type)
    paths = os.listdir(dir)
    bird = [pygame.image.load(join(dir, path)).convert_alpha()
            for path in paths]
    return bird


def load_pipe(color: str, flip: Literal[0, 1]):
    path = join("assets", "pipe", color + ".png")
    pipe = pygame.image.load(path)
    return pygame.transform.flip(pipe, 0, flip)


def load_number(num: int):
    path = join("assets", "num", str(num) + ".png")
    return pygame.image.load(path)


def load_audio(name: str):
    path = join("assets", "audio", name + ".wav")
    return pygame.mixer.Sound(path)


class Object(pygame.sprite.Sprite):
    def __init__(self, surface: pygame.Surface, x: float, y: float):
        self.surface = surface
        self.rect = pygame.Rect(
            x, y, self.surface.get_width(), self.surface.get_height()
        )

    def draw(self, window: pygame.Surface):
        self.update()
        window.blit(self.surface, self.rect)

    def update(self):
        pass


class Background(Object):
    def __init__(self, bg_type: str = "day", x: float = 0, y: float = 0):
        super().__init__(load_background(bg_type), x, y)

    def draw(self, window: pygame.Surface):
        super().draw(window)

    def update(self):
        self.rect.x -= VELO
        if self.rect.x <= -WIDTH:
            self.rect.x = WIDTH * 2


class Base(Object):
    def __init__(self, x: float = 0, y: float = 0):
        super().__init__(pygame.image.load("assets/base.png"), x, y)
        self.mask = pygame.mask.from_surface(self.surface)

    def draw(self, window: pygame.Surface):
        super().draw(window)

    def update(self):
        self.rect.x -= VELO
        if self.rect.x <= -WIDTH:
            self.rect.x = WIDTH * 2


class Bird(Object):
    def __init__(self, bird_type: str = "red", x: float = 0, y: float = 0):
        self.surface = load_bird(bird_type)
        self.rect = pygame.Rect(
            x, y, self.surface[0].get_width(), self.surface[0].get_height()
        )

        self.mask = pygame.mask.from_surface(self.surface[0])
        self.y_velo = 0
        self.ani_count = 0
        self.alive = True

    def draw(self, window):
        self.update()
        self.ani_count += 1
        self.ani_count %= 30
        sur = pygame.transform.rotate(
            self.surface[self.ani_count // 10], -self.y_velo * 3
        )
        self.mask = pygame.mask.from_surface(sur)
        self.rect.width = sur.get_width()
        self.rect.height = sur.get_height()
        window.blit(sur, self.rect)

    def update(self):
        if self.alive:
            self.y_velo += ACC
            self.rect.y += self.y_velo

    def rise_up(self):
        pygame.mixer.Channel(0).play(load_audio("wing"))
        self.y_velo = -5.5


class Pipe(Object):
    def __init__(
        self, color: str = "green", flip: Literal[0, 1] = 0, x: float = 0, y: float = 0
    ):
        super().__init__(load_pipe(color, flip), x, y)
        self.flip = flip
        self.mask = pygame.mask.from_surface(self.surface)
        self.marked = 0

    def draw(self, window: pygame.Surface):
        super().draw(window)

    def update(self):
        self.rect.x -= VELO


def collide(bird: Bird, objects: list[Object]):
    for obj in objects:
        if pygame.sprite.collide_mask(bird, obj):
            pygame.mixer.Channel(0).play(load_audio("hit"))
            bird.alive = False
            break


def update_score(bird: Bird, pipes: list[Pipe]):
    for i in range(2):
        if pipes[i * 2].rect.x <= bird.rect.x and not pipes[i * 2].marked:
            pipes[i * 2].marked = 1
            pygame.mixer.Channel(1).play(load_audio("point"))
            return 1
    return 0


def render_score(current_scores: int, window: pygame.Surface):
    x = 10
    y = 10
    if not current_scores:
        window.blit(load_number(0), (x, y))
    else:
        nums = []
        nums_width = 24
        while current_scores:
            nums.insert(0, current_scores % 10)
            current_scores //= 10

        for i in range(len(nums)):
            window.blit(load_number(nums[i]), (x + i * nums_width, y))


def draw(window: pygame.Surface, objects: list[Object]):
    clock.tick(FPS)
    for obj in objects:
        obj.draw(window)


def gen_pipe_pos(pipes: list[Pipe], pipe_dis: int, oppo_pipe_dis: int):
    '''Generate the position for pair of opposite pipes'''

    if not len(pipes):
        for i in range(2):
            pipes.append(Pipe("green", 1, WIDTH + 250 *
                         i, random.randint(-225, 0)))
            pipes.append(
                Pipe(
                    "green",
                    0,
                    WIDTH + 250 * i,
                    pipes[i * 2].rect.y +
                    pipes[i * 2].rect.height + oppo_pipe_dis,
                )
            )

    else:
        for i in range(2):
            if pipes[i * 2].rect.x + pipes[i * 2].rect.width == 0:

                pipes[i * 2].rect.x += pipe_dis * 2
                pipes[i * 2 + 1].rect.x += pipe_dis * 2

                pipes[i * 2].rect.y = random.randint(-225, 0)
                pipes[i * 2 + 1].rect.y = (
                    pipes[i * 2].rect.y +
                    pipes[i * 2].rect.height + oppo_pipe_dis
                )
                pipes[i * 2].marked = pipes[i * 2 + 1].marked = 0
                break


def main(window: pygame.Surface):

    objects = []
    current_scores = 0
    now = datetime.now()

    if 18 <= now.hour <= 24 or 0 <= now.hour <= 5:
        type = "night"
    else:
        type = "day"

    for i in range(3):
        objects.append(Background(type, i * WIDTH, -50))

    pipes = []
    gen_pipe_pos(pipes, PIPE_DIS, OPPOSITE_PIPE_DIS)

    for p in pipes:
        objects.append(p)

    base = [Base(i * WIDTH, 512) for i in range(3)]
    for b in base:
        objects.append(b)

    bird = Bird("red", 0, 246)
    bird.rect.x = (WIDTH - bird.rect.width) // 2

    objects.append(bird)

    start_screen = pygame.image.load("assets/message.png")
    gameover_screen = pygame.image.load("assets/gameover.png")
    render_first_frame = True
    running = True
    started = False

    while running:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not started:
                    started = True
                elif bird.alive:
                    bird.rise_up()

        if bird.alive:
            collide(bird, [*base, *pipes])
        if not started:
            window.blit(
                start_screen,
                (
                    (WIDTH - start_screen.get_width()) // 2,
                    (HEIGHT - start_screen.get_height()) // 2 - 100,
                ),
            )
            if render_first_frame:
                draw(window, objects)
                render_first_frame = False
        else:
            if bird.alive:
                draw(window, objects)
            else:
                window.blit(
                    gameover_screen, ((
                        WIDTH - gameover_screen.get_width()) // 2, 100)
                )

        current_scores += update_score(bird, pipes)

        render_score(current_scores, window)

        gen_pipe_pos(pipes, PIPE_DIS, OPPOSITE_PIPE_DIS)

        pygame.display.update()
    pygame.quit()


if __name__ == "__main__":
    main(window)
