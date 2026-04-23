import pygame
import sys
import random

pygame.init() # Initialize pygame modules (graphics, sound, etc.)


''' Settings and Initialization '''
# size of tile and grid
TILE_SIZE = 40
GRID_WIDTH, GRID_HEIGHT = 17, 17 #must be odds

TITLE_HEIGHT = 60  # extra vertical space for title # adding title to add it into Height
WIDTH = GRID_WIDTH * TILE_SIZE + 200 # Width includes extra space for sidebar
# HEIGHT = GRID_HEIGHT * TILE_SIZE # updating height to add title 
HEIGHT = GRID_HEIGHT * TILE_SIZE + TITLE_HEIGHT
 

#to align in a center
MAZE_WIDTH_PX = GRID_WIDTH * TILE_SIZE
MAZE_HEIGHT_PX = GRID_HEIGHT * TILE_SIZE
# Calculate offsets to center maze
MAZE_OFFSET_X = (WIDTH - 200 - MAZE_WIDTH_PX) // 2  # left space, excluding sidebar
# MAZE_OFFSET_Y = (HEIGHT - MAZE_HEIGHT_PX) // 2 updating for title
MAZE_OFFSET_Y = TITLE_HEIGHT + (HEIGHT - TITLE_HEIGHT - MAZE_HEIGHT_PX) // 2

#Globally setting the goal post
GOAL_POS = (GRID_WIDTH - 2, GRID_HEIGHT - 2)

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Coffee Maze Game")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 32)  # Default font, size 32


# -----------------------------
# Color Palette (Coffee Theme)
# -----------------------------

WALL_COLOR = (97, 71, 55)       # espresso brown
PATH_COLOR = (240, 234, 214)    # light latte cream
PLAYER_COLOR = (255, 248, 250)  # soft vanilla (light beige)
# PLAYER_COLOR = 	(255, 255, 255)
GOAL_COLOR = (149, 125, 106)    # mocha
TEXT_COLOR = (60, 40, 30)       # deep coffee
SIDEBAR_BG = (220, 210, 190)    # muted almond
GRID_LINE_COLOR = (200, 190, 170)  # subtle grid


# Game timer
TIME_LIMIT = 30  # seconds

# -----------------------------
# Drawing Functions
# -----------------------------

def draw_maze():
    '''
    Draws the maze layout on the screen with wall and background colors.
    '''
    screen.fill(PATH_COLOR)  # Latte-colored background

    for y, row in enumerate(maze):
        for x, tile in enumerate(row):
            if tile == 'W':
                # pygame.draw.rect(screen, WALL_COLOR, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                pygame.draw.rect(screen,WALL_COLOR,(MAZE_OFFSET_X + x * TILE_SIZE, MAZE_OFFSET_Y + y * TILE_SIZE,TILE_SIZE,TILE_SIZE),border_radius=1)#to align centre


def draw_player(x, y):
    '''
    Draws the player as a glowing circle (drop shadow).
    '''
    center_x = MAZE_OFFSET_X + x * TILE_SIZE + TILE_SIZE // 2 # adding offset to align center
    center_y = MAZE_OFFSET_Y + y * TILE_SIZE + TILE_SIZE // 2
    radius = TILE_SIZE // 3

    # Draw subtle shadow (behind player)
    # shadow_color = (210, 200, 180)  # slightly darker than background
    # shadow_color = (255,200,20)
    # pygame.draw.circle(screen, shadow_color, (center_x + 2, center_y + 2), radius)

    # Draw main player circle
    pygame.draw.circle(screen, PLAYER_COLOR, (center_x, center_y), radius)
    # Draw circle border (outline)
    BORDER_COLOR = (100, 100, 100)  # choose any contrasting color
    border_width = 3  # thickness of border
    pygame.draw.circle(screen, BORDER_COLOR, (center_x, center_y), radius, border_width)


def draw_goal(goal_pos):
    '''
    Draws the goal as a rounded mocha rectangle.
    '''
    pygame.draw.rect(
        screen, GOAL_COLOR,(MAZE_OFFSET_X + goal_pos[0] * TILE_SIZE + 8, MAZE_OFFSET_Y + goal_pos[1] * TILE_SIZE + 8, TILE_SIZE - 16, TILE_SIZE - 16),border_radius=6)


def draw_score(time_sec, moves):
    '''
    Draws the sidebar with time and move count.
    '''
    # Draw sidebar background panel
    pygame.draw.rect(screen, SIDEBAR_BG, (GRID_WIDTH * TILE_SIZE, 0, 200, HEIGHT))

    # Title and stats
    title = font.render("Maze Stats", True, TEXT_COLOR)
    time_text = font.render(f"Time: {time_sec}s", True, TEXT_COLOR)
    move_text = font.render(f"Moves: {moves}", True, TEXT_COLOR)

    screen.blit(title, (GRID_WIDTH * TILE_SIZE + 20, 20))
    screen.blit(time_text, (GRID_WIDTH * TILE_SIZE + 20, 60))
    screen.blit(move_text, (GRID_WIDTH * TILE_SIZE + 20, 100))


def show_instructions():
    '''
    Display instructions screen before the game starts.
    '''
    # Fonts
    font_title = pygame.font.SysFont("Arial", 64, bold=True)
    font_subtitle = pygame.font.SysFont("Comic Sans MS", 28, italic=True)  # Handwriting style
    font_section = pygame.font.SysFont(None, 40)
    font_body = pygame.font.SysFont(None, 30)
    font_button = pygame.font.SysFont(None, 28)

    while True:
        screen.fill(PATH_COLOR)

        # --- Main Title ---
        title_surface = font_title.render("MazeGame", True, TEXT_COLOR)
        screen.blit(title_surface, (
            WIDTH // 2 - title_surface.get_width() // 2,
            40
        ))

        # --- Subtitle (handwriting style) ---
        subtitle_surface = font_subtitle.render("Let the ice find Mocha", True, TEXT_COLOR)
        screen.blit(subtitle_surface, (
            WIDTH // 2 - subtitle_surface.get_width() // 2,
            110
        ))

        # --- Section Header ---
        section_title = font_section.render("How to Play", True, TEXT_COLOR)
        screen.blit(section_title, (
            WIDTH // 2 - section_title.get_width() // 2,
            180
        ))

        # --- Instructions List ---
        instructions = [
            "Player is represented with white circle.",
            "Use arrow keys to move circle.",
            "Reach the mocha-colored goal.",
            "You have 30 seconds!",
            "Avoid the espresso-brown walls.",
            "Enjoy your coffee-themed maze journey!"
        ]

        for i, line in enumerate(instructions):
            text = font_body.render(line, True, TEXT_COLOR)
            screen.blit(text, (
                WIDTH // 2 - text.get_width() // 2,
                240 + i * 35
            ))

        # --- Start Game Button ---
        start_btn = pygame.Rect(WIDTH // 2 - 90, HEIGHT - 100, 180, 50)
        pygame.draw.rect(screen, SIDEBAR_BG, start_btn, border_radius=8)

        btn_text = font_button.render("Start Game", True, TEXT_COLOR)
        screen.blit(btn_text, (
            start_btn.centerx - btn_text.get_width() // 2,
            start_btn.centery - btn_text.get_height() // 2
        ))

        # --- Event Handling ---
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_btn.collidepoint(event.pos):
                    return  # start game


# not using 
# def draw_grid():
#     '''
#     Draws subtle grid lines for visual structure.
#     '''
#     for x in range(GRID_WIDTH):
#         pygame.draw.line(screen, GRID_LINE_COLOR, (x * TILE_SIZE, 0), (x * TILE_SIZE, HEIGHT))
#     for y in range(GRID_HEIGHT):
#         pygame.draw.line(screen, GRID_LINE_COLOR, (0, y * TILE_SIZE), (GRID_WIDTH * TILE_SIZE, y * TILE_SIZE))




# -----------------------------
# End Screen Function
# -----------------------------

def show_end_screen(message, time_sec, moves):
    '''
    Displays win/lose message and final stats with play again and exit options.
    '''
    title_font = pygame.font.SysFont(None, 48)
    label_font = pygame.font.SysFont(None, 32)
    button_font = pygame.font.SysFont(None, 28)

    while True:
        screen.fill(PATH_COLOR)

        y_start = HEIGHT // 2 - 120

        # Title message
        title_color = GOAL_COLOR if message == "You Win!" else (180, 60, 60)
        title = title_font.render(message, True, title_color)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, y_start))

        # Stats
        time_text = label_font.render(f"Time: {time_sec} seconds", True, TEXT_COLOR)
        move_text = label_font.render(f"Moves: {moves}", True, TEXT_COLOR)
        screen.blit(time_text, (WIDTH // 2 - time_text.get_width() // 2, y_start + 50))
        screen.blit(move_text, (WIDTH // 2 - move_text.get_width() // 2, y_start + 90))

        # Buttons
        play_again_btn = pygame.Rect(WIDTH // 2 - 120, y_start + 150, 110, 40)
        exit_btn = pygame.Rect(WIDTH // 2 + 10, y_start + 150, 100, 40)

        pygame.draw.rect(screen, SIDEBAR_BG, play_again_btn)
        pygame.draw.rect(screen, SIDEBAR_BG, exit_btn)

        play_text = button_font.render("Play Again", True, TEXT_COLOR)
        exit_text = button_font.render("Exit", True, TEXT_COLOR)

        screen.blit(play_text, (
            play_again_btn.centerx - play_text.get_width() // 2,
            play_again_btn.centery - play_text.get_height() // 2
        ))
        screen.blit(exit_text, (
            exit_btn.centerx - exit_text.get_width() // 2,
            exit_btn.centery - exit_text.get_height() // 2
        ))

        pygame.display.flip()

        # Handle input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_again_btn.collidepoint(event.pos):
                    return True
                elif exit_btn.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()



# -----------------------------
# Generating maze
# -----------------------------
import random
def generate_maze(width, height):
    """
    Generate a maze using recursive backtracking.
    Maze dimensions should be odd (e.g., 21x21) for proper wall structure.
    Returns a list of strings with 'W' for wall and ' ' for path.
    """
    # Internal dimensions must be odd
    maze = [['W' for _ in range(width)] for _ in range(height)]

    def carve(x, y):
        directions = [(0, -2), (2, 0), (0, 2), (-2, 0)]
        random.shuffle(directions)
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 < nx < width - 1 and 0 < ny < height - 1 and maze[ny][nx] == 'W':
                maze[ny][nx] = ' '
                maze[y + dy // 2][x + dx // 2] = ' '
                carve(nx, ny)

    # Start in top-left corner (1,1)
    maze[1][1] = ' '
    carve(1, 1)

    # Place exit in bottom-right (guaranteed path)
    maze[height - 2][width - 2] = ' '

    return [''.join(row) for row in maze]


# -----------------------------
# Maze Layout (W = wall, space = path)
# -----------------------------
maze = generate_maze(GRID_WIDTH, GRID_HEIGHT)

# -----------------------------
# Main Game Function
# -----------------------------

def run_game():
    '''
    Main game loop: handles input, updates, rendering, and win/lose logic.
    '''
    player_x, player_y = 1, 1
    # GOAL_POS = (13, 13)# using formula instead
    # GOAL_POS = (GRID_WIDTH - 2, GRID_HEIGHT - 2)# using global
    move_count = 0
    start_time = pygame.time.get_ticks()
    
    while True:
        clock.tick(10)
        elapsed_time = (pygame.time.get_ticks() - start_time) // 1000

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Time check
        if elapsed_time >= TIME_LIMIT:
            return show_end_screen("Time's up!", elapsed_time, move_count)

        # Movement handling
        keys = pygame.key.get_pressed()
        new_x, new_y = player_x, player_y

        if keys[pygame.K_LEFT]: new_x -= 1
        elif keys[pygame.K_RIGHT]: new_x += 1
        elif keys[pygame.K_UP]: new_y -= 1
        elif keys[pygame.K_DOWN]: new_y += 1

        # Check walls and update player position
        if maze[new_y][new_x] != 'W':
            if (new_x, new_y) != (player_x, player_y):
                move_count += 1
            player_x, player_y = new_x, new_y

        # Win condition
        if (player_x, player_y) == GOAL_POS:
            return show_end_screen("You Win!", elapsed_time, move_count)

        # Drawing everything 
        draw_maze()
        draw_goal(GOAL_POS)
        draw_player(player_x, player_y)
        draw_score(elapsed_time, move_count)
        # draw_grid()  # optional grid lines
        pygame.display.flip()

# -----------------------------
# Game Loop
# -----------------------------
show_instructions()
while True:
    restart = run_game()
    if not restart:
        break
