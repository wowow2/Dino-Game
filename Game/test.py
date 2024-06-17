import pygame
import sprites
import math

screen_width = 1400
screen_height = 900
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Scrolling Background Tutorial")
bg = sprites.track
clock = pygame.time.Clock()

scroll = 0

# CHANGE THE BELOW 1 TO UPPER NUMBER IF
# YOU GET BUFFERING OF THE IMAGE
# HERE 1 IS THE CONSTATNT FOR REMOVING BUFFERING
tiles = math.ceil(screen_width / bg.get_width()) + 1

# MAIN LOOP
while 1:
   # THIS WILL MANAGE THE SPEED OF
   # THE SCROLLING IN PYGAME
   clock.tick(33)

   # APPENDING THE IMAGE TO THE BACK
   # OF THE SAME IMAGE
   i = 0
   while (i < tiles):
      screen.blit(bg, (bg.get_width() * i + scroll, 0))
      i += 1
   # FRAME FOR SCROLLING
   scroll -= 20

   # RESET THE SCROLL FRAME
   if abs(scroll) > bg.get_width():
      scroll = 0
   # CLOSINF THE FRAME OF SCROLLING
   for event in pygame.event.get():
      if event.type == pygame.QUIT:
         quit()

   pygame.display.flip()

pygame.quit()