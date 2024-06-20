'''
title: Dinosaur Game
author: Abbas Rizvi
date: June 15, 2024
'''

# Imports
import pygame
import sprites
import random


# Initialize pygame
pygame.init()

# set font
font = pygame.font.Font("freesansbold.ttf", 30)

# set screen
screen = pygame.display.set_mode((1200, 600))
screen.fill((245, 230, 220))

# set game clock
clock = pygame.time.Clock()


# Dinosaur class
class Dinosaur:
    def __init__(self):
        # Dinosaur states
        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False


        self.step = 0 # Animation step

        self.jump_speed = 8.5
        self.image = sprites.dino_start # Dinosaur image

        self.dino_box = self.image.get_rect() # Get the "hit box"

        # set x and y of the hit box
        self.dino_box.x = 100
        self.dino_box.y = 450
    def update_dino(self, key_pressed):
        if self.dino_duck:
            self.duck()
        if self.dino_run:
            self.run()
        if self.dino_jump:
            self.jump()

        if self.step >= 10: # animates the dino
            self.step = 0

        # handles changes in states of the dino
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
        self.image = sprites.dino_duck[self.step // 5] # animation
        # adjust hit box for ducking
        self.dino_box = self.image.get_rect()
        self.dino_box.x = 100
        self.dino_box.y = 483
        self.step += 1

    def run(self):
        self.image = sprites.dino_run[self.step // 5] # animation
        # adjust hit box for running
        self.dino_box = self.image.get_rect()
        self.dino_box.x = 100
        self.dino_box.y = 450
        self.step += 1
    def jump(self):
        self.image = sprites.dino_jump

        if self.dino_jump:
            self.dino_box.y -= self.jump_speed * 5 # moves the dino into the air
            pygame.time.delay(2)
            self.jump_speed -= 0.8 # gravity effect
        # stop condition for jump state
        if self.jump_speed <= -8.5:
            self.dino_jump = False
            self.jump_speed = 8.5

    def paint(self):
        screen.blit(self.image, (self.dino_box.x, self.dino_box.y))
    def get_rect(self):
        return self.image.get_rect()

# Track class
class Track:
    def __init__(self):
        self.image = sprites.track
        self.width = self.image.get_width()
        self.pos_x = 0
        self.pos_y = 530

    def paint(self, game_speed):
        screen.blit(self.image, (self.pos_x, self.pos_y)) # blit track and a copy off the screen
        screen.blit(self.image, (self.width + self.pos_x, self.pos_y))

        self.pos_x -= game_speed # moves track to the left
        if self.pos_x <= -self.width:
            # once track is off the screen, blit a copy again for an infinite loop
            screen.blit(self.image, (self.width + self.pos_x, self.pos_y))
            self.pos_x = 0

# Cactus class
class Cactus:
    def __init__(self):
        self.size = random.randint(0, 1) # 0 is big cactus, 1 is small
        self.group = random.randint(0,2) # picks from subtypes of each

        if self.size == 0:
            self.image = sprites.large_cactus[self.group]
        elif self.size == 1:
            self.image = sprites.small_cactus[self.group]

        self.pos_x = 1200 # off the screen
        self.rect = self.image.get_rect()

    def paint(self, game_speed):
        self.pos_x -= game_speed
        # different y coordinate for different size
        if self.size == 0:
            screen.blit(self.image, (self.pos_x, 445))
            self.rect.topleft = (self.pos_x, 445) # adjust hit box
        else:
            screen.blit(self.image, (self.pos_x, 469))
            self.rect.topleft = (self.pos_x, 469) # adjust hit box
    def get_rect(self):
        return self.image.get_rect()
    def check_screen(self):
        # checks if cactus is off the screen to the left
        return self.pos_x < self.get_rect().width - 150
class Bird:
    def __init__(self):
        self.image = sprites.bird[random.randint(0,1)] # picks bird sprite
        self.pos_y = random.choice([300, 410]) # picks height
        self.pos_x = 1200
        self.rect = self.image.get_rect()
    def paint(self, game_speed):
        # blits and adjusts hit box
        self.pos_x -= game_speed
        screen.blit(self.image, (self.pos_x, self.pos_y))
        self.rect.topleft = (self.pos_x, self.pos_y)
    def check_screen(self):
        # checks if bird is off the screen to the left
        return self.pos_x < self.get_rect().width - 150
    def get_rect(self):
        return self.image.get_rect()
def points(score, game_speed):
    # adds score every tick and accelerates game speed every 100 points
    score += 1
    if score % 100 == 0:
        game_speed += 1
    text = font.render('Score: '+str(score), True, (0, 0, 0))
    screen.blit(text, (950,0))

    return score, game_speed
def main():
    running = True
    Dino = Dinosaur()
    Background = Track()
    game_speed = 15
    spawn_time = 0
    score = 0
    game_over = False
    Obstacles = []

    while running:
        screen.fill((245, 230, 220))

        # event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN and game_over:
                if event.key == pygame.K_r:
                    main()
                elif event.key == pygame.K_q:
                    exit()

        key_pressed = pygame.key.get_pressed() # gets key pressed

        if not game_over:
            Dino.paint()
            Dino.update_dino(key_pressed)

            Background.paint(game_speed)

            # as game speed goes up, more obstacles spawn
            if pygame.time.get_ticks() - spawn_time > random.randrange(17000, 22000) / game_speed:
                if random.random() < 0.75:
                    Obstacles.append(Cactus())
                else:
                    Obstacles.append(Bird())
                spawn_time = pygame.time.get_ticks()

            for obstacle in Obstacles[:]:
                # spawn obstacles
                obstacle.paint(game_speed)
                # check collision
                if Dino.dino_box.colliderect(obstacle.rect):
                    game_over = True
                if obstacle.check_screen():
                    Obstacles.remove(obstacle)

            score, game_speed = points(score, game_speed) # update score and game speed

        else:
            # game over screen
            game_over_text = font.render('You LOSE! Press R to Restart, Q to quit', True, (0, 0, 0))
            screen.blit(game_over_text, (310, 300))
            screen.blit(sprites.game_over, (400, 250))

        pygame.display.update()
        clock.tick(60)

if __name__ == '__main__':
    main()
