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
        "force_applied": 6000,
        "ball_mass": 10,
        "ball_moment": 10,
        "wall_elasticity": 0.95,
        "ball_elasticity": 0.95
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
    if int(config["MAIN"]["ball_mass"]) <= 0 or int(config["MAIN"]["ball_moment"]) <= 0:
        print("ball settings too low. Ignoring")
        config["MAIN"]["ball_mass"] = "1"
        config["MAIN"]["ball_moment"] = "1"


def game_over(exit_code):
    if exit_code == 0:
        pygame.quit()
        sys.exit()


class Tower:
    def __init__(self):
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.body.position = ((display.get_width() / 2), (display.get_height() / 2) + 200)
        self.shape = pymunk.Poly.create_box(self.body, (25, 600))
        space.add(self.body, self.shape)

    def draw(self):
        pygame.draw.rect(display, colors["black"], pygame.Rect(((display.get_width() / 2) - (25 / 2),
                                                                (display.get_height() / 2) - (600 / 2) + 200),
                                                               (25, 1600)))

    def remove(self):
        space.remove(self.body, self.shape)


class Wall:
    def __init__(self, pos_x, pos_y, size_x, size_y):
        self.size_x = size_x
        self.size_y = size_y
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.body.position = (pos_x, pos_y)
        self.shape = pymunk.Poly.create_box(self.body, (size_x, size_y))
        self.shape.elasticity = float(config["MAIN"]["wall_elasticity"])
        space.add(self.body, self.shape)

    def draw(self):
        pygame.draw.rect(display, colors["black"], pygame.Rect((self.pos_x - (self.size_x / 2), self.pos_y - (self.size_y / 2)), (self.size_x, self.size_y)))


class Ball:
    def __init__(self):
        self.body = pymunk.Body(int(config["MAIN"]["ball_mass"]), int(config["MAIN"]["ball_moment"]),
                                body_type=pymunk.Body.DYNAMIC)
        self.body.position = (display.get_width() / 2, 50)
        self.shape = pymunk.Circle(self.body, 25)
        self.shape.elasticity = float(config["MAIN"]["ball_elasticity"])
        space.add(self.body, self.shape)

    def draw(self):
        pygame.draw.circle(display, colors["white"], self.shape.body.position, 25)

    def push_x(self, loc, force):
        self.body.apply_impulse_at_local_point((force, 0), (loc, 0))

    def push_y(self, loc, force):
        self.body.apply_impulse_at_local_point((0, force), (0, loc))


pygame.init()

display = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.mouse.set_visible(False)
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
wall1 = Wall(0, display.get_height() / 2, 0, display.get_height())
wall2 = Wall(display.get_width() / 2, 0, display.get_width(), 0)
wall3 = Wall(display.get_width(), display.get_height() / 2, 0, display.get_height())
wall4 = Wall(display.get_width() / 2, display.get_height(), display.get_width(), 0)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over(0)
        if event.type == pygame.KEYDOWN:
            if "tower" in globals():
                tower.remove()
                del tower
            if event.key == pygame.K_ESCAPE:
                game_over(0)
            if event.key == pygame.K_RIGHT:
                ball.push_x(-25, int(config["MAIN"]["force_applied"]))
            if event.key == pygame.K_LEFT:
                ball.push_x(25, -int(config["MAIN"]["force_applied"]))
            if event.key == pygame.K_UP:
                ball.push_y(-25, -int(config["MAIN"]["force_applied"]))
            if event.key == pygame.K_DOWN:
                ball.push_y(25, int(config["MAIN"]["force_applied"]))

    display.fill(colors["gray"])

    if "tower" in globals():
        tower.draw()
    ball.draw()
    wall1.draw()
    wall2.draw()
    wall3.draw()
    wall4.draw()

    pygame.display.update()
    clock.tick(fps)
    space.step(1 / fps)
