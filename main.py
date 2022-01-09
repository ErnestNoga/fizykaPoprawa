#!/bin/python3.8
import os.path
import pygame
import pymunk
import sys
import configparser

if not os.path.isfile("config.ini"):
    print("Generating config.ini")
    config = configparser.ConfigParser()
    config["ENVIRONMENT"] = {
        "gravity_X": 0,
        "gravity_Y": 500,
        "fps": 240
    }
    config["MAIN"] = {
        "force_applied_X": 6000,
        "force_applied_Y": 0
    }
    with open("config.ini", "w") as configfile:
        config.write(configfile)
    sys.exit()
else:
    config = configparser.ConfigParser()
    config.read("config.ini")
    if int(config["ENVIRONMENT"]["fps"]) < 30:
        print("fps set to less than 30. Setting to 30")
        config["ENVIRONMENT"]["fps"] = "30"


def game_over(exit_code):
    if exit_code == 0:
        pygame.quit()
        sys.exit()


class Tower:
    def __init__(self):
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.body.position = (0, 600)
        self.shape = pymunk.Poly.create_box(self.body, (100, 600))
        space.add(self.body, self.shape)

    def draw(self):
        pygame.draw.rect(display, colors["black"], pygame.Rect((0, 300), (50, 1600)))


class Wall:
    def __init__(self, pos_x, pos_y, size_x, size_y):
        self.size_x = size_x
        self.size_y = size_y
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.body.position = (pos_x, pos_y)
        self.shape = pymunk.Poly.create_box(self.body, (size_x, size_y))
        space.add(self.body, self.shape)

    def draw(self):
        pygame.draw.rect(display, colors["black"], pygame.Rect((self.pos_x, self.pos_y), (self.size_x, self.size_y)))


class Ball:
    def __init__(self):
        self.body = pymunk.Body(10, 10, body_type=pymunk.Body.DYNAMIC)
        self.body.position = (25, 0)
        self.shape = pymunk.Circle(self.body, 25)
        space.add(self.body, self.shape)

    def draw(self):
        pygame.draw.circle(display, colors["white"], self.shape.body.position, 25)


pygame.init()

display = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()
space = pymunk.Space()
space.gravity = (int(config["ENVIRONMENT"]["gravity_X"]), int(config["ENVIRONMENT"]["gravity_Y"]))
fps = int(config["ENVIRONMENT"]["fps"])
colors = {
    "red": pygame.Color((255, 0, 0)),
    "green": pygame.Color((0, 255, 0)),
    "blue": pygame.Color((0, 0, 255)),
    "gray": pygame.Color((127, 127, 127)),
    "white": pygame.Color((255, 255, 255)),
    "black": pygame.Color((0, 0, 0))
}
ball = Ball()
tower = Tower()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over(0)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                ball.body.apply_impulse_at_local_point((int(config["MAIN"]["force_applied_X"]), int(config["MAIN"]["force_applied_Y"])), (25, 0))

    display.fill(colors["gray"])

    tower.draw()
    ball.draw()

    pygame.display.update()
    clock.tick(fps)
    space.step(1 / fps)
