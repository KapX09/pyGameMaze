import pygame
import sys

pygame.init()

''' Window settings '''
TILE_SIZE = 40
GRID_WIDTH = 20
GRID_HEIGHT = 15
WIDTH = GRID_WIDTH * TILE_SIZE
HEIGHT = GRID_HEIGHT * TILE_SIZE

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Game")
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)  # player
BLUE = (0, 0, 255)       # wall
BLACK = (0, 0, 0)        # background
GREEN = (0, 255, 0)      # goal

''' Maze Layout '''
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

''' Player and Goal Setup '''
player_x, player_y = 1, 1
GOAL_POS = (13, 13)

# NEW: Score Tracking Variables 
start_time = pygame.time.get_ticks()  #  Start the timer
move_count = 0                        #  Count the player's moves

''' Drawing Functions '''
def draw_maze():
    for y, row in enumerate(maze):
        for x, tile in enumerate(row):
            if tile == 'W':
                pygame.draw.rect(
                    screen,
                    BLUE,
                    (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                )

def draw_player():
    pygame.draw.rect(
        screen,
        WHITE,
        (player_x * TILE_SIZE + 5, player_y * TILE_SIZE + 5, TILE_SIZE - 10, TILE_SIZE - 10)
    )

def draw_goal():
    pygame.draw.rect(
        screen,
        GREEN,
        (GOAL_POS[0] * TILE_SIZE + 5, GOAL_POS[1] * TILE_SIZE + 5, TILE_SIZE - 10, TILE_SIZE - 10)
    )

''' Main loop '''
# Main Game Loop
running = True
while running:
    clock.tick(10)  # 10 frames per second

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Calculate elapsed time in seconds
    elapsed_time = (pygame.time.get_ticks() - start_time) // 1000

    # Check for timeout first
    if elapsed_time >= timeout_limit:
        print("Time's up! Try again next time.")
        game_over = True
        screen.fill(BLACK)
        draw_maze()
        draw_goal()
        draw_player()
        draw_score(elapsed_time, move_count)
        draw_timeout_message()
        pygame.display.flip()
        pygame.time.delay(3000)  # Show message for 3 seconds
        break  # Exit the loop

    # Handle player movement only if game is not over
    keys = pygame.key.get_pressed()
    new_x, new_y = player_x, player_y

    if keys[pygame.K_LEFT]:
        new_x -= 1
    elif keys[pygame.K_RIGHT]:
        new_x += 1
    elif keys[pygame.K_UP]:
        new_y -= 1
    elif keys[pygame.K_DOWN]:
        new_y += 1

    # Move player if allowed
    if maze[new_y][new_x] != 'W':
        if (new_x, new_y) != (player_x, player_y):
            move_count += 1
        player_x, player_y = new_x, new_y

    # Check for win
    if (player_x, player_y) == GOAL_POS:
        print("You reached the goal!")
        print(f"Time taken: {elapsed_time} seconds")
        print(f"Moves taken: {move_count}")
        game_over = True
        screen.fill(BLACK)
        draw_maze()
        draw_goal()
        draw_player()
        draw_score(elapsed_time, move_count)
        pygame.display.flip()
        pygame.time.delay(3000)  # Show final screen for 3 seconds
        break  # Exit the loop

    # Draw everything
    screen.fill(BLACK)
    draw_maze()
    draw_goal()
    draw_player()
    draw_score(elapsed_time, move_count)
    pygame.display.flip()

pygame.quit()
sys.exit()

