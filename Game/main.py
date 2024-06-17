'''
title: Dinosaur Game
author: Abbas Rizvi
date: June 15, 2024
'''
import pygame
import sprites
import math
# Window

pygame.init()
screen = pygame.display.set_mode((1600, 900))
screen.fill((245, 230, 220))
clock = pygame.time.Clock()


# Dinosaur class
class Dinosaur:
    def __init__(self):
        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False

        self.step = 0
        self.jump_speed = 9
        self.image = sprites.dino_start

        self.dino_box = self.image.get_rect()
        self.dino_box.x = 100
        self.dino_box.y = 650
    def update_dino(self, key_pressed):
        if self.dino_duck:
            self.duck()
        if self.dino_run:
            self.run()
        if self.dino_jump:
            self.jump()

        if self.step >= 10:
            self.step = 0

        if key_pressed[pygame.K_SPACE] and not self.dino_jump:
            self.dino_duck = False
            self.dino_run = False
            self.dino_jump = True
        elif key_pressed[pygame.K_DOWN] and not self.dino_jump:
            self.dino_duck = True
            self.dino_run = False
            self.dino_jump = False
        elif not (self.dino_jump or key_pressed[pygame.K_DOWN]):
            self.dino_duck = False
            self.dino_run = True
            self.dino_jump = False

    def duck(self):
        print('hi')
        self.image = sprites.dino_duck[self.step // 5]
        self.dino_box = self.image.get_rect()
        self.dino_box.x = 100
        self.dino_box.y = 683
        self.step += 1

    def run(self):
        self.image = sprites.dino_run[self.step // 5]
        self.dino_box = self.image.get_rect()
        self.dino_box.x = 100
        self.dino_box.y = 650
        self.step += 1
    def jump(self):
        self.image = sprites.dino_jump
        if self.dino_jump:
            self.dino_box.y -= self.jump_speed * 5
            self.jump_speed -= 1
        if self.jump_speed <= -9:
            self.dino_jump = False
            self.jump_speed = 9
    def paint(self):
        screen.blit(self.image, (self.dino_box.x, self.dino_box.y))
class Background:
    def __init__(self):
        self.image = sprites.track
        self.width = self.image.get_width()
        self.pos_x = 0
        self.pos_y = 730

    def paint(self, game_speed):
        screen.blit(self.image, (self.pos_x, self.pos_y))
        screen.blit(self.image, (self.width + self.pos_x, self.pos_y))

        self.pos_x -= game_speed
        if self.pos_x <= -self.width:
            screen.blit(self.image, (self.width + self.pos_x, self.pos_y))
            self.pos_x = 0

if __name__ == '__main__':
    running = True
    Dino = Dinosaur()
    Background = Background()

    while running:
        screen.fill((245, 230, 220))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        key_pressed = pygame.key.get_pressed()

        Dino.paint()
        Dino.update_dino(key_pressed)

        Background.paint(20)

        pygame.display.update()
        clock.tick(60)
