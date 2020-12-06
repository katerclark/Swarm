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
SCREEN_TITLE = "Swarm"

# How many bugs a player can place on each their grid
NUMBER_OF_BUGS = 15

class GameMaster(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        # creates one grid for each player
        self.player_one_grid = Grid()
        self.player_two_grid = Grid()

        # creates two players and tells them which grid belongs to them and which one belongs to the other player
        self.player_one = Player(self.player_one_grid, self.player_two_grid)
        self.player_two = Player(self.player_two_grid, self.player_one_grid)
       
        self.input_service = InputService()
        self.output_service = OutputService

    def play(self):
        self.player_one.populate_map(self.player_one_grid)
        self.player_two.populate_map(self.player_two_grid)
        
        while player_one.is_alive and player_two.is_alive:
            arcade.run()


class Player:

    def __init__(self, my_grid, their_grid):
        self._my_grid = my_grid
        self._their_grid = their_grid
        self.bugs_on_map = NUMBER_OF_BUGS
        self.is_alive = True

    def get_my_grid(self):
        return self._my_grid

    def get_their_grid(self):
        return self._their_grid

    def attack_tile(self, grid):
        get_their_grid().process_attack(row, column)

    def place_bug(self, grid):
        get_my_grid().process_bug_placement(row, column)

    # player can add their bugs to the map
    def populate_map(self, grid):
        for i in range(NUMBER_OF_BUGS):
            place_bug(get_my_grid())

    # play is alive if they have more than 0 living bugs on the map
    def is_player_alive(self):
        if self.bugs_on_map <= 0:
            self.is_alive = False
        return self.is_alive


class Grid:
    """Contains tiles"""

    def __init__(self):
        
        self.tiles = []
        for row in range(ROW_COUNT):
            self.tiles.append([])
            for column in range(COLUMN_COUNT):
                self.tiles[row].append(Tile())

    def get_tile(self, row, column):
        return self.tiles[row][column]

    # tells tile when has been attacked
    def process_attack(self, row, column):
        tile = get_tile(row, column)
        tile._has_been_attacked = True

    # tells a tile when a bug has been placed on it
    def process_bug_placement(self, row, column):
        tile = get_tile(row, column)
        tile._is_bug = True


class Tile:
    """Contains tile state"""

    def __init__(self):
        # describes tile - does not contain a bug
        self._is_bug = False
        # describes tile - has not been clicked (attacked)
        self._has_been_attacked = False

        # we can put this next section either here or in OutputService (where it is currently)
        # bug is dead
        if self._is_bug == True and self._has_been_attacked == True:
            pass
        # bug is alive
        if self._is_bug == True and self._has_been_attacked == False:
            pass
        # failed attempt (bug was not in selected tile)
        if self._is_bug == False and self._has_been_attacked == True:
            pass


class InputService:

    def on_mouse_press(self, x, y, button, modifiers):
        
        # turns x and y into row and column
        column = int(x // (WIDTH + MARGIN))
        row = int(y // (HEIGHT + MARGIN))

        # determines if we are clicking in the grid
        if row < ROW_COUNT and column < COLUMN_COUNT:
            if grid.tiles[row][column] == 0:
                grid.tiles[row][column] = 1

        print(f"Tile coordinates: ({row}, {column})")

        return row, column


class OutputService:

    def on_draw(self):
        arcade.set_background_color(arcade.color.BLACK)
        arcade.start_render()

        for tile in player.get_my_grid():
            # bug is dead
            if tile._is_bug == True and tile._has_been_attacked == True:
                player.bugs_on_map = player.bugs_on_map - 1
                color = arcade.color.RED
            # bug is alive
            elif tile._is_bug == True and tile._has_been_attacked == False:
                color = arcade.color.ORANGE
            # failed attempt (bug was not in selected tile)
            elif tile._is_bug == False and tile._has_been_attacked == True:
                color = arcade.color.BLACK
            else:
                color = arcade.color.CHARCOAL

        for tile in player.get_their_grid():
            # bug is dead
            if tile._is_bug == True and tile._has_been_attacked == True:
                color = arcade.color.RED
            # bug is alive
            elif tile._is_bug == True and tile._has_been_attacked == False:
                color = arcade.color.CHARCOAL
            # failed attempt (bug was not in selected tile)
            elif tile._is_bug == False and tile._has_been_attacked == True:
                color = arcade.color.BLACK
            else:
                color = arcade.color.CHARCOAL

            x = (MARGIN + WIDTH) * column + MARGIN + WIDTH // 2
            y = (MARGIN + HEIGHT) * row + MARGIN + HEIGHT // 2
    
            arcade.draw_rectangle_filled(x, y, WIDTH, HEIGHT, color)


if __name__ == "__main__":
    game = GameMaster(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.play()


# ________________FIRST WORKING VERSION___________________


# ROW_COUNT = 10
# COLUMN_COUNT = 10

# # This sets the WIDTH and HEIGHT of each grid location
# WIDTH = 45
# HEIGHT = 45

# # This sets the margin between each cell
# # and on the edges of the screen.
# MARGIN = 2

# # Do the math to figure out our screen dimensions
# SCREEN_WIDTH = (WIDTH + MARGIN) * COLUMN_COUNT + MARGIN
# SCREEN_HEIGHT = (HEIGHT + MARGIN) * ROW_COUNT + MARGIN
# SCREEN_TITLE = "Battleship"

# class Window(arcade.Window):
#     """
#     Main application class.
#     """

#     def __init__(self, width, height, title):
#         """
#         Set up the application.
#         """

#         super().__init__(width, height, title)

#         # Create a 2 dimensional array. A two dimensional
#         # array is simply a list of lists.
#         self.grid = []
#         for row in range(ROW_COUNT):
#             # Add an empty array that will hold each cell
#             # in this row
#             self.grid.append([])
#             for column in range(COLUMN_COUNT):
#                 self.grid[row].append(0)  # Append a cell

#         arcade.set_background_color(arcade.color.BLACK)

#     def on_draw(self):
#         """
#         Render the screen.
#         """
#         # This command has to happen before we start drawing
#         arcade.start_render()
#         # tile.ship = False

#         # Draw the grid
#         for row in range(ROW_COUNT):
#             for column in range(COLUMN_COUNT):
#                 # Figure out what color to draw the box
#                 if self.grid[row][column] == 1: #and tile.ship == False:
#                     # tile.hit == False
#                     color = arcade.color.ORANGE
#                 elif self.grid[row][column] == 1: #and tile.ship == True:
#                     # tile.hit == True
#                     color = arcade.color.RED
#                 else:
#                     color = arcade.color.CHARCOAL

#                 # Do the math to figure out where the box is
#                 x = (MARGIN + WIDTH) * column + MARGIN + WIDTH // 2
#                 y = (MARGIN + HEIGHT) * row + MARGIN + HEIGHT // 2

#                 # Draw the box
#                 arcade.draw_rectangle_filled(x, y, WIDTH, HEIGHT, color)
    
#     def on_mouse_press(self, x, y, button, modifiers):
#         """
#         Called when the user presses a mouse button.
#         """

#         # Change the x/y screen coordinates to grid coordinates
#         column = int(x // (WIDTH + MARGIN))
#         row = int(y // (HEIGHT + MARGIN))

#         print(f"Click coordinates: ({x}, {y}). Grid coordinates: ({row}, {column})")

#         # Make sure we are on-grid. It is possible to click in the upper right
#         # corner in the margin and go to a grid location that doesn't exist
#         if row < ROW_COUNT and column < COLUMN_COUNT:
#             if self.grid[row][column] == 0:
#                 self.grid[row][column] = 1
            
    
# # Holds the array where the ships are
# class Tile:

#     def __init__(self):
#         self.hit = False
#         self.ship = False
    
#     def has_ship(self, x, y):
#         # return ship[y][x]
#         pass

#     def has_been_attacked(self, x, y):
#         # if self.hit == False:
#         #     window.color = arcade.color.LIGHT_BLUE
#         # elif self.hit == True:
#         #     window.color = arcade.color.RED
#         # else:
#         #     window.color = arcade.color.BLUE_GREEN
#         pass

# # Tracks mouse clicks and translates them to the other classes
# class Player(arcade.Window):
#     pass

# class GameMaster:

#     def __init__(self):
#         self.window = Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

#     def play(self):
#         arcade.run()


# if __name__ == "__main__":
#     game = GameMaster()
#     game.play()

# # https://arcade.academy/examples/array_backed_grid.html#array-backed-grid
# # http://learn.arcade.academy/chapters/25_array_backed_grids/array_backed_grids.html
# # https://www.youtube.com/watch?v=5d1CfnYT-KM 