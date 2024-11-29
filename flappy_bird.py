import pygame
import sys


pygame.init()

SCREEN_LENGTH = 1500
SCREEN_HEIGHT = 750
BG_COLOR = (255, 255, 255)


game_display = pygame.display.set_mode((SCREEN_LENGTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird Game")
game_display.fill(BG_COLOR)

def display_screen():
    clock = pygame.time.Clock()

    while True:
        
        for game in pygame.event.get():
            if game.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
       

if __name__ == "__main__":
    display_screen()


