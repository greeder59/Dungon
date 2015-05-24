import random

class Thing:
    """Thing is the base class for all the things in the dungon.
    At a minimum, position should be set when instantiating.
    name should also be set if it will be picked up by a player object.
    """

    def __init__(self, **kwargs):
        self.position = (0,0)
        self.state = 'active'
        self.name = ''

        for key, value in kwargs.items():
            setattr(self, key, value)


    def make_inactive(self):
        self.state = 'inactive'
        self.position = (-1, -1)

    
class Moveable(Thing):
    """A thing that can move"""

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

        
class Player(Moveable):
    """player is the user controled thing. It can pick up and carry stuff. And fight monsters"""
   
    def __init__(self, **kwargs):
        self.position = (0.0)
        self.state = 'active'
        self.name = ''
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

    def fight(self, enemy):
        if 'sword' in self.has:
            print("\n**  You have slain the {}!".format(enemy.name))
            enemy.make_inactive()
            return 1
        else:  
            print("\nChomp, Chomp: You just got eaten by the {}.\n".format(enemy.name))
            return 0


class Monster(Moveable):
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
