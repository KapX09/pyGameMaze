import pygame
import sys

pygame.init()

# -----------------------------
# Settings and Initialization
# -----------------------------
TILE_SIZE = 40
GRID_WIDTH, GRID_HEIGHT = 20, 15
WIDTH, HEIGHT = GRID_WIDTH * TILE_SIZE + 200, GRID_HEIGHT * TILE_SIZE

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Game")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 32)

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GRAY = (100, 100, 100)

WALL_COLOR = (30, 60, 200)   # Soft deep blue
PATH_COLOR = (15, 15, 15)    # Softer background

# Timeout settings
TIME_LIMIT = 30  # seconds

# -----------------------------
# Maze Layout
# -----------------------------
maze = [
    "WWWWWWWWWWWWWWW",
    "W   W       W W",
    "W W W WWWWW W W",
    "W W W     W W W",
    "W W WWWWW W W W",
    "W W     W W   W",
    "W WWWWW W WWWWW",
    "W     W W     W",
    "WWW W W W WWW W",
    "W   W W W W   W",
    "W WWWWW W W W W",
    "W       W W W W",
    "W WWWWWWW W W W",
    "W           W W",
    "WWWWWWWWWWWWWWW"
]

# -----------------------------
# Drawing Functions
# -----------------------------
def draw_maze():
    screen.fill(PATH_COLOR) #set bg

    for y, row in enumerate(maze):
        for x, tile in enumerate(row):
            if tile == 'W':
                pygame.draw.rect(screen, WALL_COLOR, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

def draw_player(x, y):
    # pygame.draw.rect(screen, WHITE, (x * TILE_SIZE + 5, y * TILE_SIZE + 5, TILE_SIZE - 10, TILE_SIZE - 10))
    pygame.draw.circle(
        screen,
        WHITE,
        (x * TILE_SIZE + TILE_SIZE // 2, y * TILE_SIZE + TILE_SIZE // 2),
        TILE_SIZE // 3
    )

def draw_goal(goal_pos):
    pygame.draw.rect(screen, (240,234,214), (goal_pos[0] * TILE_SIZE + 5, goal_pos[1] * TILE_SIZE + 5, TILE_SIZE - 10, TILE_SIZE - 10))
    # pygame.draw.rect(
    #     screen,
    #     (0, 200, 0),
    #     (goal_pos[0] * TILE_SIZE + 8, goal_pos[1] * TILE_SIZE + 8, TILE_SIZE - 16, TILE_SIZE - 16),
    #     border_radius=6
    # )

def draw_score(time_sec, moves):
    title = font.render("Maze Status", True, WHITE)
    screen.blit(title, (GRID_WIDTH * TILE_SIZE + 20, 10))

    score_text = font.render(f"Time: {time_sec}s", True, WHITE)
    move_text = font.render(f"Moves: {moves}", True, WHITE)
    screen.blit(score_text, (GRID_WIDTH * TILE_SIZE + 20, 40))
    screen.blit(move_text, (GRID_WIDTH * TILE_SIZE + 20, 80))

# -----------------------------
# End Screen with Buttons
# -----------------------------
def show_end_screen(message, time_sec, moves):
    # Fonts
    title_font = pygame.font.SysFont(None, 48)  # Bigger for title
    label_font = pygame.font.SysFont(None, 32)  # Standard labels
    button_font = pygame.font.SysFont(None, 28)  # Buttons

    while True:
        screen.fill(BLACK)

        # Center Y positioning
        y_start = HEIGHT // 2 - 120

        # Title message ("You Win!" or "Time's up!")
        title = title_font.render(message, True, GREEN if message == "You Win!" else RED)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, y_start))

        # Time and moves info
        time_text = label_font.render(f"Time: {time_sec} seconds", True, WHITE)
        move_text = label_font.render(f"Moves: {moves}", True, WHITE)
        screen.blit(time_text, (WIDTH // 2 - time_text.get_width() // 2, y_start + 50))
        screen.blit(move_text, (WIDTH // 2 - move_text.get_width() // 2, y_start + 90))

        # Buttons
        play_again_btn = pygame.Rect(WIDTH // 2 - 120, y_start + 150, 110, 40)
        exit_btn = pygame.Rect(WIDTH // 2 + 10, y_start + 150, 100, 40)

        pygame.draw.rect(screen, GRAY, play_again_btn)
        pygame.draw.rect(screen, GRAY, exit_btn)

        # Button Text
        play_text = button_font.render("Play Again", True, BLACK)
        exit_text = button_font.render("Exit", True, BLACK)

        screen.blit(play_text, (
            play_again_btn.centerx - play_text.get_width() // 2,
            play_again_btn.centery - play_text.get_height() // 2
        ))
        screen.blit(exit_text, (
            exit_btn.centerx - exit_text.get_width() // 2,
            exit_btn.centery - exit_text.get_height() // 2
        ))

        pygame.display.flip()

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_again_btn.collidepoint(event.pos):
                    return True  # Restart
                elif exit_btn.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

# -----------------------------
# Main Game Function
# -----------------------------
def run_game():
    player_x, player_y = 1, 1
    GOAL_POS = (13, 13)
    move_count = 0
    start_time = pygame.time.get_ticks()

    while True:
        clock.tick(10)
        elapsed_time = (pygame.time.get_ticks() - start_time) // 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Check timeout
        if elapsed_time >= TIME_LIMIT:
            return show_end_screen("Time's up!", elapsed_time, move_count)

        # Handle key presses
        keys = pygame.key.get_pressed()
        new_x, new_y = player_x, player_y

        if keys[pygame.K_LEFT]: new_x -= 1
        elif keys[pygame.K_RIGHT]: new_x += 1
        elif keys[pygame.K_UP]: new_y -= 1
        elif keys[pygame.K_DOWN]: new_y += 1

        # Valid move
        if maze[new_y][new_x] != 'W':
            if (new_x, new_y) != (player_x, player_y):
                move_count += 1
            player_x, player_y = new_x, new_y

        # Check win
        if (player_x, player_y) == GOAL_POS:
            return show_end_screen("You Win!", elapsed_time, move_count)

        # Draw everything
        screen.fill(BLACK)
        draw_maze()
        draw_goal(GOAL_POS)
        draw_player(player_x, player_y)
        draw_score(elapsed_time, move_count)
        pygame.display.flip()

# -----------------------------
# Run the Game Loop
# -----------------------------
while True:
    restart = run_game()
    if not restart:
        break
