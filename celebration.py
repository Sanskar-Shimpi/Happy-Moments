import pygame
import random
import math
import sys

from typing import List

# config
MIN_SIDES = 3
MAX_SIDES = 7
MIN_SIZE = 3
MAX_SIZE = 7

VEL_X = 1.5
MIN_VEL_Y = 0
MAX_VEL_Y = 10

TERMINAL_VEL = 10
GRAVITY = 0.1

MIN_ROT = 0
MAX_ROT = 0.3

COLOR_INT = 10

# setup
pygame.init()
pygame.font.init()

# defs
font = pygame.font.SysFont('Times New Roman', 37)
clock = pygame.time.Clock()

width, height = 720, 1020

screen = pygame.display.set_mode((720,1020))
pygame.display.set_caption("Happy New Year!")


# util
def polygon(color, x, y, sides, size, rot=0):
    """
    Rot: 0-2PI
    Sides: ...
    """

    points = []
    step = 2 * math.pi / sides

    for i in range(0, sides):
        ang = i * step + rot
        points.append((x + size * math.cos(ang), y + size * math.sin(ang)))

    pygame.draw.polygon(screen, color, points)


# confetti
confettis: List['Confetti'] = []
colors = [(0, 123, 255), (50, 0, 255), (255, 0, 255), (255, 0, 128),
          (221, 21, 21), (0, 255, 190), (0, 197, 36), (15, 105, 31),
          (255, 200, 0), (255, 109, 0)]


def make_confetti(x, y):
    for _ in range(0, random.randint(10, 50)):
        confettis.append(Confetti(x, y))


class Confetti:

    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.color = random.choice(colors)

        self.rot = random.uniform(0, 2 * math.pi)
        self.rot_amt = random.uniform(MIN_ROT, MAX_ROT)

        self.sides, self.sizes = random.randint(MIN_SIDES,
                                                MAX_SIDES), random.randint(
                                                    MIN_SIZE, MAX_SIZE)

        self.velx = random.uniform(-VEL_X, VEL_X)
        self.vely = -random.uniform(MIN_VEL_Y, MAX_VEL_Y)

    def draw(self):
        polygon(self.color, self.x, self.y, self.sides, self.sizes, self.rot)

        self.x += self.velx

        if self.vely < TERMINAL_VEL:
            self.vely += GRAVITY

        self.y += self.vely
        self.rot += self.rot_amt


# text
new_year = font.render("Happy New Year 2023!", True, (255, 255, 255))
new_year_w, new_year_h = new_year.get_size()

instr = font.render("Click to make Confetti! ", True, (255, 255, 255))
instr_w, instr_h = instr.get_size()

# draw
bg_color = (random.randint(125,
                           255), random.randint(125,
                                                255), random.randint(125, 255))
count = 0

while True:
    clock.tick(70)

    len_c = len(confettis)
    if len_c < 255:
        screen.fill((len_c, len_c, len_c))
    else:
        screen.fill(bg_color)
        count += 1
        if count > COLOR_INT:
            bg_color = (random.randint(125, 255), random.randint(125, 255),
                        random.randint(125, 255))
            count = 0

    screen.blit(new_year, ((width - new_year_w) / 2, height / 2 - new_year_h))
    screen.blit(instr, ((width - instr_w) / 2, height / 2 + instr_h))

    for confetti in confettis:
        if confetti.x < 0 or confetti.x > width or confetti.y > height:
            confettis.remove(confetti)
            continue

        confetti.draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)

        if event.type == pygame.MOUSEBUTTONUP:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            make_confetti(mouse_x, mouse_y)

    pygame.display.update()
