import pygame
import random
import sys
import asyncio

async def main():
    # Initialize Pygame
    pygame.init()
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Flappy Bird")
    clock = pygame.time.Clock()

    # Game variables
    gravity = 0.4
    jump_velocity = -8
    bird_x = SCREEN_WIDTH // 4
    bird_y = SCREEN_HEIGHT // 2
    initial_background = (135, 206, 235)
    score = 0
    best_score = 0
    running = True
    game_over = False
    bird_velocity = 0
    background_color = initial_background

    # Pipe dimensions
    pipe_width = 64
    pipe_height = 600
    pipe_gap = 200

    # Ground properties
    ground_height = 50
    ground_color = random.choice([(139, 69, 19), (255, 215, 0)])

    # Load images
    try:
        bird_image = pygame.image.load("sprite-bird.png")
        bird_image = pygame.transform.scale(bird_image, (64, 33))
        bird_image.set_colorkey((255, 255, 255))
    except pygame.error:
        print("Error loading bird image")
        return

    try:
        pipe_top_image = pygame.image.load("sprite-pipe-top.png")
        pipe_bottom_image = pygame.image.load("sprite-pipe-bottom.png")
        pipe_top_image.set_colorkey((255, 255, 255))
        pipe_bottom_image.set_colorkey((255, 255, 255))
    except pygame.error:
        print("Error loading pipe images")
        return

    # Get bird dimensions
    bird_width = bird_image.get_width()
    bird_height = bird_image.get_height()
    bird_half_width = bird_width // 2
    bird_half_height = bird_height // 2

    class Pipe:
        def __init__(self):
            self.x = SCREEN_WIDTH
            self.top_height = random.randint(100, SCREEN_HEIGHT - 300)
            self.bottom_height = pipe_height
            self.passed = False

        def draw(self):
            top_pipe_y = - (pipe_height - self.top_height)
            screen.blit(pipe_top_image, (self.x, top_pipe_y))
            bottom_pipe_y = self.top_height + pipe_gap
            screen.blit(pipe_bottom_image, (self.x, bottom_pipe_y))

        def update(self):
            self.x -= 2

        def offscreen(self):
            return self.x < -pipe_width

        def get_top_rect(self):
            return pygame.Rect(self.x, 0, pipe_width, self.top_height)

        def get_bottom_rect(self):
            return pygame.Rect(self.x, self.top_height + pipe_gap, pipe_width, self.bottom_height)

    # Game state
    pipes = []
    spawn_counter = 0
    game_over = False
    bird_velocity = 0
    background_color = initial_background

    # Fonts
    font = pygame.font.Font(None, 36)

    def draw_bird():
        screen.blit(bird_image, (bird_x - bird_half_width, int(bird_y) - bird_half_height))

    def reset_game():
        nonlocal bird_y, bird_velocity, pipes, score, background_color, game_over
        bird_y = SCREEN_HEIGHT // 2
        bird_velocity = 0
        pipes = []
        score = 0
        background_color = random.choice([(135, 206, 235), (123, 104, 238), (245, 173, 112)])
        game_over = False

    def game_over_screen():
        nonlocal best_score
        best_score = max(best_score, score)
        screen.fill(background_color)
        text = font.render(f"Best Score: {best_score}", True, (0, 0, 0))
        text_rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50))
        screen.blit(text, text_rect)
        text2 = font.render("Press SPACE to Restart", True, (0, 0, 0))
        text2_rect = text2.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        screen.blit(text2, text2_rect)
        pygame.display.flip()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if game_over:
                    if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_SPACE:
                        reset_game()
                elif event.key == pygame.K_SPACE:
                    bird_velocity = jump_velocity

        if not game_over:
            bird_velocity += gravity
            bird_y += bird_velocity

            if spawn_counter <= 0:
                pipes.append(Pipe())
                spawn_counter = random.randint(100, 150)
            else:
                spawn_counter -= 1

            for pipe in pipes:
                pipe.update()
                if pipe.x + pipe_width < bird_x and not pipe.passed:
                    score += 1
                    pipe.passed = True
                if pipe.offscreen():
                    pipes.remove(pipe)

            ground_collision = bird_y + bird_half_height > SCREEN_HEIGHT - ground_height
            for pipe in pipes:
                bird_rect = pygame.Rect(bird_x - bird_half_width, bird_y - bird_half_height, bird_width, bird_height)
                if bird_rect.colliderect(pipe.get_top_rect()) or bird_rect.colliderect(pipe.get_bottom_rect()):
                    game_over = True
            if ground_collision:
                game_over = True

            screen.fill(background_color)
            for pipe in pipes:
                pipe.draw()
            pygame.draw.rect(screen, ground_color, (0, SCREEN_HEIGHT - ground_height, SCREEN_WIDTH, ground_height))
            draw_bird()
            score_text = font.render(f"Score: {score}", True, (0, 0, 0))
            screen.blit(score_text, (SCREEN_WIDTH - 150, 20))
            pygame.display.flip()

        else:
            game_over_screen()

        await asyncio.sleep(0)
        clock.tick(60)

asyncio.run(main())
