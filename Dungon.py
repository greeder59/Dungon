# Dungon Game.
# by kenneth Love.
# With improvements by Gordon Reeder
# -------------
# STILL to DO
# - See about setting the Dungon_size tuple with optional command line arguments.
# - Make it Object oriented. In progress, much work to do.

import random

# ** Define some game paramerers

Dungon_size = (5, 4)    # Size of dungon

# ** Define some classes.
       
class Thing:
    """Thing is the base class for all the things in the dungon."""

    def __init__(self, arg_here):
        self.position = (arg_here)
        self.state = 'active'

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
    """player is the user controled thing. It can pick up and carry stuff."""
   
    def __init__(self, arg_here):
        self.position = (arg_here)
        self.state = 'active'
        self.has = []    # List of stuff that the player has

    def pick_up(self, stuff):
        self.has.append(stuff)

    def put_down(self, stuff):
        if stuff in self.has:
            self.has.remove(stuff)

    def does_have(self, stuff):
        return stuff in self.has


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
    """The playing area. 
    Call as: Gulag = play_area((size_x, size_y))"""

    def __init__(self, arg_size):
        self.size = (arg_size)
        self.CELLS =[(x,y) for y in range(arg_size[1]) for x in range(arg_size[0])]

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

    def get_size(self):
        return self.size



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
                    print(tile.format('m|'))    
                else:
                    print(tile.format('_|'))            
            else:
                if cell == player.position:
                    print(tile.format('X'), end='')
                elif cell == monster.position:
                    print(tile.format('m'), end='')
                else:
                    print(tile.format('_'), end='')  


# ** Game begins here **
#** First we will create instances of the objects and set their initial locations.

dungon = Play_area(Dungon_size)
key = Thing(dungon.random_location())
sword = Thing(dungon.random_location())
door = Thing(dungon.random_location())
monster = Monster(dungon.random_location())
player = Player(dungon.random_location())

print("""
    Welcome to the dungon!
    Find your way to the door to escape. 
    But watch out for the hungry grue! """)

while True:
    moves = dungon.get_moves(player)

    draw_map(player, monster, dungon.get_size())
    print("You (X) are in room {}".format(player.position))
    if monster.state == 'active':
        print("monster (m) is in {}".format(monster.position))
    print("You can move {}".format(moves))
    print("enter 'QUIT' to Quit")

    move = input("> ")
    move = move.upper()

    if move == 'QUIT':
        break

    if move == 'CHEAT':
        print("monster is in {}".format(monster.position))
        print("sword is in {}".format(sword.position))
        print("door is at {}".format(door.position))
        print("key is in {}".format(key.position))
        continue
 
    if move in ['LEFT', 'RIGHT', 'UP', 'DOWN']:
        if move in moves:
            player.move(move)

        else:
            print("\n** Walls are hard. Stop walking into them! **")
        
        monster.chase(player)

    else:
        print("\n ** What?? **")
        continue

    if player.position == monster.position:
        if player.does_have('sword'):
            print("\n**  You have slain the grue!")
            monster.make_inactive()
        else:  
            print("\nChomp, Chomp: You just got eaten by the grue.\n")
            break        # You loose! Nothing else matters.

    if player.position == key.position:
        print("\n** You found a key!")
        player.pick_up('key')
        key.make_inactive()
    
    if player.position == sword.position:
        print("\n** You found a sword!")
        player.pick_up('sword')
        sword.make_inactive()

    if player.position == door.position:
        if player.does_have('key'):
            print("\nYou found the door. You unlock it and step out to freedom.\n")
            break
        else:
            print("\nYou found the door. But it is locked. You can't get out.")
