'''
title: output of bot training
author: Abbas Rizvi
date: June 24, 2024
'''
import neat
import pickle
from main import *
from bot import distance
import time

def run_winner(config_file, winner_file):
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    # Load the winner genome
    with open(winner_file, 'rb') as f:
        winner = pickle.load(f)

    # recreate neural net
    net = neat.nn.FeedForwardNetwork.create(winner, config)

    Obstacles = []
    Dino = Dinosaur()
    Background = Track()
    game_speed = 15
    spawn_time = 0
    score = 0
    running = True
    game_over = False


    while running:
        screen.fill((245, 230, 220))

        # event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        if not game_over:
            Dino.paint()
            Background.paint(game_speed)
            if len(Obstacles) > 0:
                obstacle = Obstacles[0]
                is_bird = False
                if obstacle.rect.y == 300 or obstacle.rect.y == 410:
                    is_bird = True
                # calculate distance between obstacle and dinosaur
                dist = distance((Dino.dino_box.x, Dino.dino_box.y), (obstacle.pos_x, obstacle.rect.y))
                # set inputs for neural net
                inputs = (
                    dist,
                    game_speed / dist,
                    obstacle.rect.y,
                    is_bird

                )
                output = net.activate(inputs)  # activate neural net

                decision = output.index(max(output))
                Dino.update_dino(decision)

            # as game speed goes up, more obstacles spawn
            if pygame.time.get_ticks() - spawn_time > random.randrange(17000, 22000) / game_speed:
                if random.random() < 0.85:
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

            score, game_speed, high_score = points(score, game_speed)  # update score and game speed
        else:
            time.sleep(1)
            run_winner('config.txt','winner.pkl')

        pygame.display.update()
        clock.tick(60)

if __name__ == '__main__':
    config_path = 'config.txt'
    winner_path = 'winner.pkl'
    run_winner(config_path, winner_path)