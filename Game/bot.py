'''
title: NEAT Bot
author: Abbas Rizvi
date: June 20, 2024
'''
import math
from main import *
import neat
def distance(pos1, pos2):
    # distance between 2 points
    dx = abs(pos1[0] - pos2[0])
    dy = abs(pos1[1] - pos2[1])
    dist = math.sqrt(dx ** 2 + dy ** 2)
    return dist
def run(config_file):
    # set up neat
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    pop = neat.Population(config) # population count
    pop.add_reporter(neat.StdOutReporter(True))
    # stats
    stats = neat.StatisticsReporter()
    pop.add_reporter(stats)
    # checkpoints
    pop.add_reporter(neat.Checkpointer(500))

    winner = pop.run(eval_genomes, 10000) # 10000 is just a test number
    with open('winner.txt', 'w') as f:
        f.write(str(winner))
    print(winner)
def eval_genomes(genomes, config):
    Nets = []
    Dinos = []
    Genomes = []
    Obstacles = []

    Background = Track()
    game_speed = 15
    spawn_time = 0
    score = 0
    running = True

    for genome_id, genome in genomes:
        # assign each genome a fitness score, neural net, and a dinosaur
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        Nets.append(net)
        Dinos.append(Dinosaur())
        Genomes.append(genome)
        genome.fitness = 0

    while running:
        screen.fill((245, 230, 220))

        # event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        if len(Dinos) == 0:
            break

        for i, Dino in enumerate(Dinos):
            if len(Obstacles) > 0:
                obstacle = Obstacles[0]
                # calculate distance between obstacle and dinosaur
                dist = distance((Dino.dino_box.x, Dino.dino_box.y), (obstacle.pos_x, obstacle.rect.y))
                # set inputs for neural net
                inputs = (
                    score,
                    dist,
                    obstacle.rect.y,
                    game_speed
                )
                output = Nets[i].activate(inputs) # activate neural net

                Dino.paint()
                decision = output.index(max(output))
                Dino.update_dino(decision)

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
            for i, Dino in enumerate(Dinos):
                if Dino.dino_box.colliderect(obstacle.rect):
                    Genomes[i].fitness -= 1
                    Dinos.pop(i)
                    Nets.pop(i)
                    Genomes.pop(i)

            if obstacle.check_screen():
                Obstacles.remove(obstacle)

        score, game_speed, high_score = points(score, game_speed)  # update score and game speed

        for genome in Genomes: # add fitness to leftover genomes
            genome.fitness += 0.1


        pygame.display.update()
        clock.tick(60)





if __name__ == '__main__':
    config_path = 'config.txt'
    run(config_path)


