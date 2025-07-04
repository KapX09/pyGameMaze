# pyGameMaze
---

Current code for the game will represent
1. Player ctrl with arrow keys
   - player as a white square
   - contolled using arrow keys
   - can only move on paths and not through walls

2. Maze structure
   - using 2D list of string
   - 'W' = wall blue block
   - ' ' space = Walkable path

3. Collison Detection
   - Prevent player form walking into walls
   - only update pos if next tile is a path

4. Goal Tile
   - Greeb sqr placed at target loction
   - If player reaches it -> game ends with msg
 
5. Basic Game loop
   - uses pygame's main loop
   - processes events (Keyboard, quit)
   - Updates display properly each frame
