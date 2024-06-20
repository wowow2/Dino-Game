'''
title: Dino Game sprites
author: Abbas Rizvi
date: June 15, 2024
'''
import pygame

dino_run = (pygame.image.load('../images/Dino/DinoRun1.png'), pygame.image.load('../images/Dino/DinoRun2.png'))
dino_jump = pygame.image.load('../images/Dino/DinoJump.png')
dino_duck = (pygame.image.load('../images/Dino/DinoDuck1.png'), pygame.image.load('../images/Dino/DinoDuck2.png'))
dino_start = pygame.image.load('../images/Dino/DinoStart.png')

large_cactus = (pygame.image.load('../images/Cactus/LargeCactus1.png'),
                pygame.image.load('../images/Cactus/LargeCactus2.png'),
                pygame.image.load('../images/Cactus/LargeCactus3.png'))

small_cactus = (pygame.image.load('../images/Cactus/SmallCactus1.png'),
                pygame.image.load('../images/Cactus/SmallCactus2.png')
                , pygame.image.load('../images/Cactus/SmallCactus3.png'))

bird = (pygame.image.load('../images/Bird/Bird1.png'), pygame.image.load('../images/Bird/Bird2.png'))

track = pygame.image.load('../images/Other/Track.png')

game_over = pygame.image.load('../images/Other/GameOver.png')