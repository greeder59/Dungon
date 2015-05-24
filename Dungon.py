# Dungon Game.
# by kenneth Love of Treehouse.
# With many improvements by Gordon Reeder
# -------------
# POSSIBLE IMPROVEMENTS
# - See about setting the Dungon_size tuple with optional command line arguments.
# - Multiple levels, Multiple monsters (Trolls, witches, orcs, zombies, dragons, huge snakes, etc)
# - Possibly have a friendly creature that the user needs to defend to get out.
# - Multiple weapons with various effectivness agains different monsters.
# - Give monsters and players attributes of: 
#   strength, 
#   health, 
#   experience.
#   Monsters will also have attributes of: 
#   Agression (does monster back off, hold ground, or press counter attack when attacked),
#   Mobility (move on every turn?).
# - Web or OS GUI interface.

import random
import sys
from Things import *

class Level:
    """The container for the levels of the game. There are four user editable
    lists here. Each list shall have the same number of entries. One entry for 
    each level of the game.
    """
    #** To add a level to the game.
    # > Add a tuple to Dungon-size that is the x,y dimension of the dungon.
    # > Add a number to Number_of_monsters list.
    # > Add a string to Welcome_message. This string will be displayed at the start of the level.
    # > Add a string to Exit_message. This string will be displayed at the completeion of the level.
    
    Current_level = 0
    Dungon_size = [(5, 4), (3, 7), (8, 6)]
    Number_of_monsters = [1, 1, 2] 

    Welcome_message = ["""
            Welcome to the dungeon!
            Find your way to the door to escape. 
            But watch out for the hungry monster!
            Type QUIT to quit the game.
            Type HELP for additional instructions.
            """,
             '  So, you thought you were free?',
             '  HA HA HA, another level.']

    Exit_message =['\n  You found the door. You unlock it and ...',
                    '\n  The door! You swing the door open to...',
                    '\n  You found the door. You unlock it and step out to freedom.\n' ]

    def Level_max():
        return len(Level.Dungon_size)



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

        self.initilize()

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

    def initilize(self):
        self.CELLS =[(x,y) for y in range(self.size[1]) for x in range(self.size[0])]

    def random_location(self):
        a_cell = random.choice(self.CELLS)
        self.CELLS.remove(a_cell)
        return a_cell


class Ui:
    """The class which encapsulates the user interface. This class is used without instantiation"""

    vocabulary = ['LEFT', 'RIGHT', 'UP', 'DOWN', 'QUIT', 'CHEAT', 'HELP', 'L', 'R', 'U', 'D'] #, 'ATTACK']
    show = [] #List of stuff that is in the play_area. Used mostly by draw_map().

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
                elif move == 'L':
                    return 'LEFT'
                elif move == 'R':
                    return 'RIGHT'
                elif move == 'U':
                    return 'UP'
                elif move == 'D':
                    return 'DOWN'                       
                else:    
                    return move
            else:
                print('\n** What? **')


    def cleanup():
        Ui.show = []           

    def put_in(thing):
        Ui.show.append(thing)

    def take_out(thing):
        if thing in Ui.show:
            Ui.show.remove(thing)        

    def draw_map(size):
        x, y = size
        print(" _" * x)

        for iy in range(y):
            for ix in range(x):
                cell = (ix,iy)
                if ix == x - 1:
                    tile = '|_|'
                    for item in Ui.show:
                        if cell == item.position:
                            tile = '|' + item.name[0] +'|'
                    print(tile)            
                else:
                    tile = '|_'
                    for item in Ui.show:
                        if cell == item.position:
                            tile = '|' + item.name[0]
                    print(tile, end='')
              

    def show_help():
        print("""  HELP: You are the X.
        Move by typing LEFT, RIGHT, UP, or DOWN.
            or just 'U' 'D' 'L' 'R'
        The monster will chase you. Try to avoid him.
        There is a sword in the dungeon. If you find it,
        you can kill the monster. Killing the monster is 
        optional.
        There is a key in the dungeon. You must find it or
        you will not be able to open the door and escape.
        """)


def game(g_level):
    """This function contains the startup code and the main loop for the game."""

# Initialize game.
#** First we will create instances of the objects and set their initial locations.

    monster_count = Level.Number_of_monsters[g_level]
    dungon = Play_area(size = Level.Dungon_size[g_level])
    key = Thing(position = dungon.random_location(), name = 'key')
    sword = Thing(position = dungon.random_location(), name = 'sword')
    door = Thing(position = dungon.random_location())
    monster = []
    for idx in range(monster_count):
        monster.append(Monster(position = dungon.random_location(), name = 'grue'))
        Ui.put_in(monster[idx])

    player = Player(position = dungon.random_location(), name = 'X')
    Ui.put_in(player)

    print(Level.Welcome_message[g_level])

    # Then we enter the main loop. Use sys.exit() to terminate.

    while True:

        Ui.draw_map(dungon.size)

        moves = dungon.get_moves(player)
        print("You can move {}".format(moves)) 
        move = Ui.get_user_move()
       
        if move == 'CHEAT':
            print("""
        sword is in {}.
        key is at {}.
        door is in {}.""".format(sword.position, key.position, door.position))
            continue    

        elif move in moves:
            player.move(move)
        else:
            print("\n** Walls are hard. Stop walking into them! **")
        
        for creature in monster:
            creature.chase(player) 

        # Now that everyone has had their chance to move, figure out what happened.

        for creature in monster: #as above
            if player.position == creature.position:
                if player.fight(creature):
                    pass
                else:
                    sys.exit() # You loose, nothing else matters.

        if player.position == key.position:
            player.pick_up(key)
        
        if player.position == sword.position:
            player.pick_up(sword)

        if player.position == door.position:
            if player.does_have(key):
                print(Level.Exit_message[g_level])
                Ui.cleanup()
                return
            else:
                print("\nYou found the door. But it is locked. You can't get out.")


if __name__ == "__main__":
    for lvl in range(Level.Level_max()):
        game(lvl)
