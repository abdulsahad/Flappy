import pygame
import random
import sys
import time

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
BIRD_WIDTH = 30
BIRD_HEIGHT = 30
PIPE_WIDTH = 60
PIPE_GAP = 150
GRAVITY = 0.25
JUMP_STRENGTH = -6
PIPE_VELOCITY = 3
BIRD_COLOR = (255, 255, 0)  # Yellow
PIPE_COLOR = (0, 255, 0)  # Green
BACKGROUND_COLOR = (135, 206, 235)  # Sky blue
BUTTON_COLOR = (255, 100, 100)  # Light red
FPS = 60

# Create screen object
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Load fonts
font = pygame.font.SysFont("Arial", 24)

# Bird class
class Bird:
    def __init__(self):
        self.x = 50
        self.y = SCREEN_HEIGHT // 2
        self.velocity = 0

    def jump(self):
        self.velocity = JUMP_STRENGTH

    def move(self):
        self.velocity += GRAVITY
        self.y += self.velocity

    def draw(self):
        pygame.draw.rect(screen, BIRD_COLOR, (self.x, self.y, BIRD_WIDTH, BIRD_HEIGHT))

# Pipe class
class Pipe:
    def __init__(self):
        self.x = SCREEN_WIDTH
        self.height = random.randint(100, SCREEN_HEIGHT - PIPE_GAP - 100)
        self.top = self.height
        self.bottom = self.height + PIPE_GAP

    def move(self):
        self.x -= PIPE_VELOCITY

    def draw(self):
        pygame.draw.rect(screen, PIPE_COLOR, (self.x, 0, PIPE_WIDTH, self.top))
        pygame.draw.rect(screen, PIPE_COLOR, (self.x, self.bottom, PIPE_WIDTH, SCREEN_HEIGHT - self.bottom))

    def off_screen(self):
        return self.x < -PIPE_WIDTH

    def collide(self, bird):
        # Check for collision with pipes
        if bird.x + BIRD_WIDTH > self.x and bird.x < self.x + PIPE_WIDTH:
            if bird.y < self.top or bird.y + BIRD_HEIGHT > self.bottom:
                return True
        return False

# Function to draw a button
def draw_button(text, y_pos):
    button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 50, y_pos, 100, 50)
    pygame.draw.rect(screen, BUTTON_COLOR, button_rect)
    button_text = font.render(text, True, (255, 255, 255))
    screen.blit(button_text, (SCREEN_WIDTH // 2 - button_text.get_width() // 2, y_pos + 10))
    return button_rect

# Function to show countdown
def show_countdown():
    for count in range(3, 0, -1):
        screen.fill(BACKGROUND_COLOR)
        countdown_text = font.render(str(count), True, (0, 0, 0))
        screen.blit(countdown_text, (SCREEN_WIDTH // 2 - countdown_text.get_width() // 2, SCREEN_HEIGHT // 2 - countdown_text.get_height() // 2))
        pygame.display.update()
        time.sleep(1)  # Wait for 1 second

# Game Over Screen
def game_over_screen(score):
    screen.fill(BACKGROUND_COLOR)
    final_score_text = font.render(f"Final Score: {score}", True, (0, 0, 0))
    screen.blit(final_score_text, (SCREEN_WIDTH // 2 - final_score_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
    
    # Draw "Start Again" button
    start_again_button = draw_button("Start Again", SCREEN_HEIGHT // 2 + 10)
    pygame.display.update()
    
    # Wait for "Start Again" button click
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if start_again_button.collidepoint(mouse_x, mouse_y):
                    return  # Exit to restart the game

# Main game function
def main():
    while True:
        bird = Bird()
        pipes = [Pipe()]
        score = 0
        clock = pygame.time.Clock()
        game_active = False

        # Game loop
        while True:
            screen.fill(BACKGROUND_COLOR)

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and game_active:
                    if event.key == pygame.K_SPACE:
                        bird.jump()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if not game_active:  # If the game is not started, check for button click
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        if start_button.collidepoint(mouse_x, mouse_y):
                            show_countdown()  # Show the countdown before starting the game
                            game_active = True  # Start the game

            if game_active:
                # Bird movement
                bird.move()

                # Check if bird hits the bottom of the screen
                if bird.y >= SCREEN_HEIGHT - BIRD_HEIGHT:
                    game_over_screen(score)  # Show Game Over screen and final score
                    break  # Restart the main loop

                # Move pipes and add new ones
                for pipe in pipes:
                    pipe.move()
                    pipe.draw()

                # Remove pipes that are off-screen
                if pipes[0].off_screen():
                    pipes.pop(0)
                    pipes.append(Pipe())
                    score += 1

                # Check for collisions
                for pipe in pipes:
                    if pipe.collide(bird):
                        game_over_screen(score)  # Show Game Over screen and final score
                        break  # Restart the main loop

                # Draw bird
                bird.draw()

                # Display score
                score_text = font.render(f"Score: {score}", True, (0, 0, 0))
                screen.blit(score_text, (10, 10))
            else:
                # Draw the start button when the game is not active
                start_button = draw_button("Start", SCREEN_HEIGHT // 2 - 25)

            # Update display
            pygame.display.update()
            clock.tick(FPS)

if __name__ == "__main__":
    main()
