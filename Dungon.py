# Dungon Game.
# by kenneth Love of Treehouse.
# With many improvements by Gordon Reeder
# -------------
# POSSIBLE IMPROVEMENTS
# - See about setting the Dungon_size tuple with optional command line arguments.
# - Multiple levels, Multiple monsters (Trolls, witches, orcs, zombies, dragons, huge snakes, etc)
# - Multiple weapons with various effectivness agains different monsters.
# - Give monsters and players attributes of: 
#   strength, 
#   health, 
#   experience.
#   Monsters will also have attributes of: 
#   Agression (does monster back off, hold ground, or press counter attack when attacked),
#   Mobility (move on every turn?).
# - Web or OS GUI interface.
# - Need to be able to draw more than two things on the map.

import random
import sys

# ** Define some game paramerers.
#   These are put here for user convienience.
#   By editing them, you can change the way the game plays.

Dungon_size = (5, 4)    # Size of dungon. You can edit these values if you want.

# ** Define some classes.
       
class Thing:
    """Thing is the base class for all the things in the dungon.
    At a minimum, position should be set when instantiating.
    name should also be set if it will be picked up by a player object.
    """

    def __init__(self, **kwargs):
        self.position = (0,0)
        self.state = 'active'
        self.name = 'thing'

        for key, value in kwargs.items():
            setattr(self, key, value)

    def move(self, move):
        x, y = self.position

        if move == 'LEFT':
            x -= 1

        elif move == 'RIGHT':
            x += 1

        elif move == 'UP':
            y -= 1

        elif move == 'DOWN':
            y += 1

        self.position = (x, y)

    def make_inactive(self):
        self.state = 'inactive'
        self.position = (-1, -1)

        
class Player(Thing):
    """player is the user controled thing. It can pick up and carry stuff. And fight monsters"""
   
    def __init__(self, **kwargs):
        self.position = (0.0)
        self.state = 'active'
        self.has = []    # List of stuff that the player has

        for key, value in kwargs.items():
            setattr(self, key, value)

    def pick_up(self, stuff):
        print("\n** You found a {}!".format(stuff.name))
        stuff.make_inactive()
        self.has.append(stuff.name)

    def put_down(self, stuff):
        if stuff.name in self.has:
            self.has.remove(stuff.name)

    def does_have(self, stuff):
        return stuff.name in self.has

    def fight(self, enemy, weapon):
        if weapon.name in self.has:
            print("\n**  You have slain the grue!")
            enemy.make_inactive()
        else:  
            print("\nChomp, Chomp: You just got eaten by the grue.\n")
            sys.exit()        # You loose! Nothing else matters.


class Monster(Thing):
    """The computer controled enemy thing. 
        It can chase other things"""

    def chase(self, prey):
        moves = ['LEFT', 'RIGHT', 'UP', 'DOWN']

        if self.state == 'active':

            if self.position[0] <= prey.position[0]:
                moves.remove('LEFT')

            if self.position[0] >= prey.position[0]:
                moves.remove('RIGHT')

            if self.position[1] <= prey.position[1]:
                moves.remove('UP')

            if self.position[1] >= prey.position[1]:
                moves.remove('DOWN')

            if len(moves) == 0:
                moves.append('HOLD')

            self.move(random.choice(moves))


class Play_area:
    """The playing area. Set the size when instantiating.
    Hands out unique random locations, and determines which
    directional moves are possible for a player.
    """

    def __init__(self, **kwargs):
        self.size = (1,1)
        self.CELLS = []

        for key, value in kwargs.items():
            setattr(self, key, value)

        self.randomize()

    def get_moves(self, player):
        moves = ['LEFT', 'RIGHT', 'UP', 'DOWN']

        if player.position[0] == 0:
            moves.remove('LEFT')
        if player.position[0] == self.size[0] - 1:
            moves.remove('RIGHT')
        if player.position[1] == 0:
            moves.remove('UP')
        if player.position[1] == self.size[1] - 1:
            moves.remove('DOWN')
        return moves

    def randomize(self):
        self.CELLS =[(x,y) for y in range(self.size[1]) for x in range(self.size[0])]

    def random_location(self):
        a_cell = random.choice(self.CELLS)
        self.CELLS.remove(a_cell)
        return a_cell


class Ui:
    """The class which encapsulates the user interface"""

    vocabulary = ['LEFT', 'RIGHT', 'UP', 'DOWN', 'QUIT', 'CHEAT', 'HELP'] #, 'ATTACK', 'L', 'R', 'U', 'D']

    def __init__(self, **kwargs):
        
        for key, value in kwargs.items():
            setattr(self, key, value)

    def get_user_move():

        while True:
            move = input("> ").upper()
            if move in Ui.vocabulary:
                if move == 'QUIT':
                    print("OK. Bye.")
                    sys.exit()
                elif move == 'HELP':
                    Ui.show_help()
                else:    
                    return move
            else:
                print('\n** What? **')

    def draw_map(player, monster, size):
        x, y = size
        print(" _" * x)
        tile = '|{}'

        for iy in range(y):
            for ix in range(x):
                cell = (ix,iy)
                if ix == x - 1:
                    if cell == player.position:
                        print(tile.format('X|'))
                    elif cell == monster.position:
                        print(tile.format('g|'))    
                    else:
                        print(tile.format('_|'))            
                else:
                    if cell == player.position:
                        print(tile.format('X'), end='')
                    elif cell == monster.position:
                        print(tile.format('g'), end='')
                    else:
                        print(tile.format('_'), end='')

        print("You (X) are in room {}".format(player.position))
        if monster.state == 'active':
            print("grue (g) is in {}".format(monster.position))

    def show_help():
        print("""   Move by typing LEFT, RIGHT, UP, or DOWN.
        The monster will chase you. Try to avoid him.
        There is a sword in the dungeon. If you find it,
        you can kill the monster. Killing the monster is 
        optional.
        There is a key in the dungeon. You must find it or
        you will not be able to open the door and escape.
        """)


def game():
    """This function contins the init code and the main loop for the game."""

# Initialize game.
#** First we will create instances of the objects and set their initial locations.

    dungon = Play_area(size = Dungon_size)
    key = Thing(position = dungon.random_location(), name = 'key')
    sword = Thing(position = dungon.random_location(), name = 'sword')
    door = Thing(position = dungon.random_location())
    monster = Monster(position = dungon.random_location())
    player = Player(position = dungon.random_location())

    print("""
        Welcome to the dungeon!
        Find your way to the door to escape. 
        But watch out for the hungry grue! 
        Type QUIT to quit the game.
        Type HELP for additional instructions.
        """)

    # Then we enter the main loop. Use sys.exit() to terminate.

    while True:

        Ui.draw_map(player, monster, dungon.size)

        moves = dungon.get_moves(player)
        print("You can move {}".format(moves)) 
        move = Ui.get_user_move()
       
        if move == 'CHEAT':
            print("""
        sword is in {}.
        door is at {}.
        key is in {}.""".format(sword.position, door.position, key.position))
            continue    

        elif move in moves:
            player.move(move)
        else:
            print("\n** Walls are hard. Stop walking into them! **")
        
        monster.chase(player)

        # Now that everyone has had their chance to move, figure out what happened.

        if player.position == monster.position:
            player.fight(monster, sword)

        if player.position == key.position:
            player.pick_up(key)
        
        if player.position == sword.position:
            player.pick_up(sword)

        if player.position == door.position:
            if player.does_have(key):
                print("\nYou found the door. You unlock it and step out to freedom.\n")
                sys.exit()
            else:
                print("\nYou found the door. But it is locked. You can't get out.")


if __name__ == "__main__":
    game()
