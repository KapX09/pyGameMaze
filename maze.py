import pygame
import sys

pygame.init()

''' Window settings '''
GRID_WIDTH = 20  # 20 tiles horizontally
GRID_HEIGHT = 15  # 15 tiles vertically
TILE_SIZE = 40
# Calculate screen size based on number of tiles
WIDTH = GRID_WIDTH * TILE_SIZE
HEIGHT = GRID_HEIGHT * TILE_SIZE
# Screen settings
# WIDTH, HEIGHT = 640, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Game")

# Clock controls the frame rate (how fast the game updates)
clock = pygame.time.Clock()

#Render the maze
# TILE_SIZE = 40 # Each tile (wall or path) will be 40x40 pixels

# Colors in RGB format
WHITE = (255, 255, 255) # player
BLUE = (0, 0, 255) # wall
BLACK = (0, 0, 0 ) # Background
GREEN = (0, 255, 0) # Goal


'''Maze Layout (2D Grid)'''
#2d Grid to represent the maze

# Each character represents a tile
# 'W' = Wall, ' ' (space) = Path

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

'''Player and Goal Setup'''
# Player's starting position in grid coordinates (x, y)
player_x, player_y = 1, 1

# Goal position (tile to reach to win)
GOAL_POS = (13, 13)


''' Drawing Functions'''
def draw_maze():
    """Draw the walls of the maze on screen"""
    for y, row in enumerate(maze):  # Go through each row
        for x, tile in enumerate(row):  # Go through each column
            if tile == 'W':  # If it's a wall tile
                pygame.draw.rect(
                    screen,
                    BLUE,
                    (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                )

def draw_player():
    """Draw the player as a white square"""
    pygame.draw.rect(
        screen,
        WHITE,
        (player_x * TILE_SIZE + 5, player_y * TILE_SIZE + 5, TILE_SIZE - 10, TILE_SIZE - 10)
    )

def draw_goal():
    """Draw the goal as a green square"""
    pygame.draw.rect(
        screen,
        GREEN,
        (GOAL_POS[0] * TILE_SIZE + 5, GOAL_POS[1] * TILE_SIZE + 5, TILE_SIZE - 10, TILE_SIZE - 10)
    )


''' Main loop'''
running = True
while running:
    clock.tick(10)  # Limit to 10 Frame per Sec(FPS) slows moments a bit
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False # will close the game window

    '''Handle Key press to move the for player'''
    # Get all currently pressed keys
    keys = pygame.key.get_pressed()
    
    # Movement: Check boundaries and wall collision
    new_x, new_y = player_x, player_y  # Store current position
    
    if keys[pygame.K_LEFT]:
        new_x -= 1
    elif keys[pygame.K_RIGHT]:
        new_x += 1
    elif keys[pygame.K_UP]:
        new_y -= 1
    elif keys[pygame.K_DOWN]:
        new_y += 1

    # Only move player if new position is not a wall
    if maze[new_y][new_x] != 'W':
        player_x, player_y = new_x, new_y

    '''Check Win condition'''
    if (player_x, player_y) == GOAL_POS:
        print("You reached the goal! You win!")
        running = False  # Exit game loop

    ''' Drawing functions'''
    screen.fill(BLACK)  # Clear screen with black
    draw_maze() # calling the maze function
    draw_goal()
    draw_player() # calling the player function 
    pygame.display.flip()

pygame.quit()
sys.exit()

