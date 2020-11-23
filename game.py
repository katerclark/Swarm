import arcade

"""
Array Backed Grid

Show how to use a two-dimensional list/array to back the display of a
grid on-screen.

Note: Regular drawing commands are slow. Particularly when drawing a lot of
items, like the rectangles in this example.

For faster drawing, create the shapes and then draw them as a batch.
See array_backed_grid_buffered.py

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.array_backed_grid
"""
import arcade

ROW_COUNT = 10
COLUMN_COUNT = 10

# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 45
HEIGHT = 45

# This sets the margin between each cell
# and on the edges of the screen.
MARGIN = 2

# Do the math to figure out our screen dimensions
SCREEN_WIDTH = (WIDTH + MARGIN) * COLUMN_COUNT + MARGIN
SCREEN_HEIGHT = (HEIGHT + MARGIN) * ROW_COUNT + MARGIN
SCREEN_TITLE = "Battleship"

class Window(arcade.Window):
    """
    Main application class.
    """

    def __init__(self, width, height, title):
        """
        Set up the application.
        """

        super().__init__(width, height, title)

        # Create a 2 dimensional array. A two dimensional
        # array is simply a list of lists.
        self.grid = []
        for row in range(ROW_COUNT):
            # Add an empty array that will hold each cell
            # in this row
            self.grid.append([])
            for column in range(COLUMN_COUNT):
                self.grid[row].append(0)  # Append a cell

        arcade.set_background_color(arcade.color.BLUE_SAPPHIRE)

    def on_draw(self, tile):
        """
        Render the screen.
        """
        # This command has to happen before we start drawing
        arcade.start_render()
        tile.ship = False

        # Draw the grid
        for row in range(ROW_COUNT):
            for column in range(COLUMN_COUNT):
                # Figure out what color to draw the box
                if self.grid[row][column] == 1 and tile.ship == False:
                    tile.hit == False
                    color = arcade.color.LIGHT_BLUE
                elif self.grid[row][column] == 1 and tile.ship == True:
                    tile.hit == True
                    color = arcade.color.RED
                else:
                    color = arcade.color.BLUE_GREEN

                # Do the math to figure out where the box is
                x = (MARGIN + WIDTH) * column + MARGIN + WIDTH // 2
                y = (MARGIN + HEIGHT) * row + MARGIN + HEIGHT // 2

                # Draw the box
                arcade.draw_rectangle_filled(x, y, WIDTH, HEIGHT, color)
    
    def on_mouse_press(self, x, y, button, modifiers):
        """
        Called when the user presses a mouse button.
        """

        # Change the x/y screen coordinates to grid coordinates
        column = int(x // (WIDTH + MARGIN))
        row = int(y // (HEIGHT + MARGIN))

        print(f"Click coordinates: ({x}, {y}). Grid coordinates: ({row}, {column})")

        # Make sure we are on-grid. It is possible to click in the upper right
        # corner in the margin and go to a grid location that doesn't exist
        if row < ROW_COUNT and column < COLUMN_COUNT:
            if self.grid[row][column] == 0:
                self.grid[row][column] = 1
            
    
# Holds the array where the ships are (1) and aren't (0)
class Tile:

    def __init__(self):
        self.hit = False
        self.ship = False
    
    def has_ship(self, x, y):
        return ship[y][x]

    # def is_hit(self, x, y):
    #     if self.hit == False:
    #         window.color = arcade.color.LIGHT_BLUE
    #     elif self.hit == True:
    #         window.color = arcade.color.RED
    #     else:
    #         window.color = arcade.color.BLUE_GREEN

# Tracks mouse clicks and translates them to the other classes
class Player(arcade.Window):
    pass

class GameMaster:

    def play(self):
        window = Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        tile = Tile()
        arcade.run()


if __name__ == "__main__":
    game = GameMaster()
    game.play()

# https://arcade.academy/examples/array_backed_grid.html#array-backed-grid
# http://learn.arcade.academy/chapters/25_array_backed_grids/array_backed_grids.html
# https://www.youtube.com/watch?v=5d1CfnYT-KM 