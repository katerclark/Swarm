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
        # Positioning the swarms.
        self.players[0].position_swarm()
        self.players[1].position_swarm() 
        # Next, begin the game.
        input("The bugs are ready... it's time to play.  Press enter to begin!")
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
# bug:" B", Empty:" _", Hit:"X", Miss:"_O"
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

    # Adds a bug to the board.  
    def add_bug(self, bug):
        # First check to make sure the bug position is within range.
        width = 1
        height = 1

        # Next check to see if the bug's position works
        for x in range(width):
            for y in range(height):
                if self.grid[bug.y + y][bug.x + x] != " _":
                    return False

        # Update the board.
        for x in range(width):
            for y in range(height):
                self.grid[bug.y + y][bug.x + x] = " B"
        return True

    # attack records an attack
    def attack(self, x, y):
        # See what is at the position.
        current_value = self.grid[y][x]
        # Hit if bug
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

    # Check if any bugs are left
    def is_defeated(self):
        if self.hit_count == 17:
            return True
        else:
            return False


# The bug class keeps track of the bugs.
class Bug:
    # Initialize the bug and its size
    def __init__(self, label, size):
        self.label = label
        self.size = size
        self.x = None
        self.y = None

    # Set the bug position. x,y is the top-left of the bug
    def set_position(self, x, y):
        self.x = x
        self.y = y

# The HumanPlayer class is a player controlled user.
class HumanPlayer:
    # Initialize the player.
    def __init__(self, player_name):
        self.player_name = player_name
        self.board = Board()
        self.swarm = [Bug("Bug", 1)]*17
        self.opponent = None

    # Connect the player to his/her opponent.
    def set_opponent(self, opponent):
        self.opponent = opponent

    # Position the swarm.
    def position_swarm(self):
        input(self.player_name+": Are you ready to position your swarm?  Press enter to begin!")

        # Position the bugs.
        for bug in self.swarm:
            self.position_bug(bug)

        # show the final board.
        print("Your swarm is ready to play.  Your board is positioned as follows:")
        print(self.board)

    # Positions a single bug.
    def position_bug(self, bug):
        # Show the board before this bug is positioned.
        print(self.board)
        print("Place a bug on the board.")
        # Ask the user for position of the bug.
        position = None
        while position is None:
            try:
                position = input("Please enter the position for the bug. " + \
                                 " Use the form x,y (e.g., 1,3): ")
                coords = position.split(",")
                x = int(coords[0])
                y = int(coords[1])
                bug.set_position(x,y)
                # Add the bug to the board.
                if not self.board.add_bug(bug):
                    # Check if the bug is valid
                    raise Exception
            except ValueError:
                print("You must a valid position for the bug.  Please try again.")
                position = None
            except:
                print("You must choose a position that is (a) on the board and (b) doesn't intersect" + \
                      "with any other bugs.")
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
            print("You hit a bug!")
        else:
            print("You missed.")

        # Pause the game until the player hits enter for the next player's turn.
        input("Press enter to continue to next player's turn: ")


        # Check if there are any bugs left.
        if self.opponent.board.is_defeated():
            return True
        else:
            return False




print("*************** Welcome to SWARM! ***************")
num_of_players = 2
while num_of_players == None:
    try:
        print("yay!")
        if (num_of_players != 1) and (num_of_players != 2):
            raise Exception()
    except:
        print("You must enter either 1 or 2.  Please try again.")
        num_of_players = None

# Create the new game for the correct number of players.  Then start the game!
game = GameMaster(num_of_players)
game.play()
