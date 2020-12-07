# The GameMaster class keeps track of the players.
class GameMaster:
    def __init__(self, num_of_players):
        # Create the players.
        if num_of_players == 1:
            self.players = [HumanPlayer("Player 1"), HumanPlayer("The Computer")]
        else:
            self.players = [HumanPlayer("Player 1"), HumanPlayer("Player 2")]

        # Set eachother as opponents.
        self.players[0].set_opponent(self.players[1])
        self.players[1].set_opponent(self.players[0])

    def play(self):
        # Positioning the fleets.
        self.players[0].position_fleet()
        self.players[1].position_fleet() 
        # Next, begin the game.
        input("The boats are ready... it's time to play.  Press enter to begin!")
        winner = False
        first_players_turn = True
        # Repeat the game-play loop as long as there is not a winner.
        while not winner:
            # Take a turn for the next player.
            if first_players_turn:
                winner = self.players[0].take_turn()
                # Check to see if the game is over.
                if winner:
                    print("Game over!", self.players[0].player_name, "wins!")
            else:
                winner = self.players[1].take_turn()
                # Check to see if the game is over.
                if winner:
                    print("Game over!", self.players[1].player_name, "wins!")

            # Swap the turn to the other player.
            first_players_turn = not first_players_turn


# The Board class keeps track of the board.
# Boat:" B", Empty:" _", Hit:"X", Miss:"_O"
class Board:

    # Initialize the board to a 10x10 grid of empty cells
    def __init__(self):
        # The grid
        self.grid = [[" _"]*10 for i in range(10)]
        # hit_count is used to count successful attacks. 
        # When the hit count reaches 17, the game is over.  
        self.hit_count = 0

    # Converts the grid to a string for printing.
    def __str__(self):
        str_val = "  0 1 2 3 4 5 6 7 8 9\n"
        for i in range(10):
            str_val += str(i)
            for j in range(10):
                str_val += self.grid[i][j]
            if i != 9:
                str_val += "\n"
        return str_val

    # Makes the grid into a string
    # Used to show the board to the opponent.
    def get_public_view(self):
        str_val = "  0 1 2 3 4 5 6 7 8 9\n"
        for i in range(10):
            str_val += str(i)
            for j in range(10):
                if self.grid[i][j] == " B":
                    str_val += " _"
                else:
                    str_val += self.grid[i][j]
            if i != 9:
                str_val += "\n"
        return str_val

    # Adds a boat to the board.  
    def add_boat(self, boat):
        # First check to make sure the boat position is within range.
        width = 1
        height = 1
        if boat.orientation == "v":
            height = boat.size
        else:
            width = boat.size
        if (boat.x < 0) or (boat.y < 0) or (boat.x+width > 10) or (boat.y+height > 10):
            return False

        # Next check to see if the boat's position works
        for x in range(width):
            for y in range(height):
                if self.grid[boat.y + y][boat.x + x] != " _":
                    return False

        # Update the board.
        for x in range(width):
            for y in range(height):
                self.grid[boat.y + y][boat.x + x] = " B"
        return True

    # attack records an attack
    def attack(self, x, y):
        # See what is at the position.
        current_value = self.grid[y][x]
        # Hit if boat
        if current_value == " B":
            self.grid[y][x] = " X"
            self.hit_count += 1
            return True
        # If the cell is empty, mark as a miss.
        elif current_value == " _":
            self.grid[y][x] = " O"
            return False
        # If anything else, its been hit.
        else:
            return False

    # Check if any boats are left
    def is_defeated(self):
        if self.hit_count == 17:
            return True
        else:
            return False


# The boat class keeps track of the boats.
class Boat:
    # Initialize the boat and its size
    def __init__(self, label, size):
        self.label = label
        self.size = size
        self.x = None
        self.y = None
        self.orientation = None

    # Set the boat position. x,y is the top-left of the boat
    def set_position(self, x, y):
        self.x = x
        self.y = y

    # Set the boat orientation. verticle or horizontal
    def set_orientation(self, orientation):
        self.orientation = orientation


# The HumanPlayer class is a player controlled user.
class HumanPlayer:
    # Initialize the player.
    def __init__(self, player_name):
        self.player_name = player_name
        self.board = Board()
        self.fleet = [Boat("Aircraft Carrier", 5), Boat("Battleship", 4), Boat("Submarine", 3), Boat("Destroyer", 3), \
                      Boat("Patrol Boat", 2)]
        self.opponent = None

    # Connect the player to his/her opponent.
    def set_opponent(self, opponent):
        self.opponent = opponent

    # Position the fleet.
    def position_fleet(self):
        input(self.player_name+": Are you ready to position your fleet?  Press enter to begin!")

        # Position the boats.
        for boat in self.fleet:
            self.position_boat(boat)

        # show the final board.
        print("Your fleet is ready to play.  Your board is positioned as follows:")
        print(self.board)

    # Positions a single boat.
    def position_boat(self, boat):
        # Show the board before this boat is positioned.
        print(self.board)
        print("You need to position a", boat.label, "of length", boat.size, "on the board above.")
        # Ask the user if the boat will be horizontal or vertical.
        orientation = None
        while orientation is None:
            orientation = input("Would you like to use a vertical or horizontal orientation? (v/h) ")
            if (orientation != "v") and (orientation != "h"):
                print("You must enter a 'v' or a 'h'.  Please try again.")
                orientation = None
        # Ask the user for top-left position of the boat.
        position = None
        while position is None:
            try:
                position = input("Please enter the position for the top-left location of the boat. " + \
                                 " Use the form x,y (e.g., 1,3): ")
                coords = position.split(",")
                x = int(coords[0])
                y = int(coords[1])
                boat.set_orientation(orientation)
                boat.set_position(x,y)
                # Add the boat to the board.
                if not self.board.add_boat(boat):
                    # Check if the boat is valid
                    raise Exception
            except ValueError:
                print("You must a valid position for the boat.  Please try again.")
                position = None
            except:
                print("You must choose a position that is (a) on the board and (b) doesn't intersect" + \
                      "with any other boats.")
                position = None

    # take_turn runs a single turn.
    def take_turn(self):
        # Display boards.
        print(self.player_name+"'s board:")
        print(self.board)
        print()
        print("Your view of "+self.opponent.player_name+"'s board:")
        print(self.opponent.board.get_public_view())

        # Get attack position.
        position = None
        while position is None:
            try:
                position = input("Please enter the position you would like to attack.  Use the form x,y (e.g., 1,3): ")
                coords = position.split(",")
                x = int(coords[0])
                y = int(coords[1])
                if (x < 0) or (x > 9) or (y < 0) or (y > 9):
                    raise Exception
            except:
                print("You must a valid position in the form x,y where both x and y are integers in the range of" + \
                      "0-9. Please try again.")
                position = None

        # Attack.
        hit_flag = self.opponent.board.attack(x, y)
        if hit_flag:
            print("You hit a boat!")
        else:
            print("You missed.")

        # Pause the game until the player hits enter for the next player's turn.
        input("Press enter to continue to next player's turn: ")


        # Check if there are any boats left.
        if self.opponent.board.is_defeated():
            return True
        else:
            return False




print("*************** Welcome to BATTLESHIP! ***************")
num_of_players = None
while num_of_players == None:
    try:
        num_of_players = int(input("Would you like to play with 1 player or 2? "))
        if (num_of_players != 1) and (num_of_players != 2):
            raise Exception()
    except:
        print("You must enter either 1 or 2.  Please try again.")
        num_of_players = None

# Create the new game for the correct number of players.  Then start the game!
game = GameMaster(num_of_players)
game.play()
