# Dungon Game.
# by kenneth Love.
# With improvements by Gordon Reeder
# -------------
# STILL to DO
# - Any function that depends on the size of the dungon needs to reference
#   Dungon_size  
#   Also, set these with optional command line arguments.

import random

# Define some game paramerers

Dungon_size = (5, 4)    # Size of dungon

CELLS =[(x,y) for y in range(Dungon_size[1]) for x in range(Dungon_size[0])]

#for y in range(0, Dungon_size[1]):
#    for x in range(0, Dungon_size[0]):
#        CELLS.append((x, y))

#CELLS = [(0,0), (1,0), (2,0), (3,0),
#       (0,1), (1,1), (2,1), (3,1),
#      (0,2), (1,2), (2,2), (3,2),
#     (0,3), (1,3), (2,3), (3,3)]


player_has = {'sword': False, 'key': False} # Things the player is carrying

def set_locations():
    monster = random.choice(CELLS)
    door = random.choice(CELLS)
    start = random.choice(CELLS)
    weapon = random.choice(CELLS)
    key = random.choice(CELLS)

    if monster == start or start == door:
        return set_locations()

    return monster, door, start, weapon, key


def move_player(player, move):
    # also moves monster
    x, y = player

    if move == 'LEFT':
        x -= 1

    elif move == 'RIGHT':
        x += 1

    elif move == 'UP':
        y -= 1

    elif move == 'DOWN':
        y += 1

    return x, y


def get_moves(player):
    moves = ['LEFT', 'RIGHT', 'UP', 'DOWN']

    if player[0] == 0:
        moves.remove('LEFT')
    if player[0] == Dungon_size[0] - 1:
        moves.remove('RIGHT')
    if player[1] == 0:
        moves.remove('UP')
    if player[1] == Dungon_size[1] - 1:
        moves.remove('DOWN')

    return moves


def get_chase_move(hunter, prey):
    moves = ['LEFT', 'RIGHT', 'UP', 'DOWN']

    if hunter[0] <= prey[0]:
        moves.remove('LEFT')

    if hunter[0] >= prey[0]:
        moves.remove('RIGHT')

    if hunter[1] <= prey[1]:
        moves.remove('UP')

    if hunter[1] >= prey[1]:
        moves.remove('DOWN')

    if len(moves) == 0:
        moves.append('HOLD')
    return random.choice(moves)


def draw_map(player, monster, size):
    x, y = size
    print(" _" * x)
    tile = '|{}'
    last_col =[i for i in range(x-1, x * y, x)]

    for idx, cell in enumerate(CELLS):
        if idx in last_col:
            if cell == player:
                print(tile.format('X|'))
            elif cell == monster:
                print(tile.format('m|'))    
            else:
                print(tile.format('_|'))            
        else:
            if cell == player:
                print(tile.format('X'), end='')
            elif cell == monster:
                print(tile.format('m'), end='')
            else:
                print(tile.format('_'), end='')   


def pick_up(thing):
     player_has[thing] = True
     return Dungon_size


monster, door, player, sword, key = set_locations()

print("""
    Welcome to the dungon!
    Find your way to the door to escape. 
    But watch out for the hungry grue! """)

if player == key:
    print("  Lucky you. The key for the door is right at your feet")
    key = pick_up('key')

if player == sword:
    print("  Lucky you. A sword is laying right at your feet")
    sword = pick_up('sword')

while True:
    moves = get_moves(player)
    
    draw_map(player, monster, Dungon_size)
    print("You (X) are in room {}".format(player))
    if monster < Dungon_size:
        print("Monster (m) is in room {}".format(monster))
    print("You can move {}".format(moves))
    print("enter 'QUIT' to Quit") 

    move = input("> ")
    move = move.upper()

    if move == 'QUIT':
        break

    if move == 'CHEAT':
        print("monster is in {}".format(monster))
        print("sword is in {}".format(sword))
        print("door is at {}".format(door))
        print("key is in {}".format(key))
        continue

    if move in ['LEFT', 'RIGHT', 'UP', 'DOWN']:
        if move in moves:
            player = move_player(player, move)

        else:
            print("\n** Walls are hard. Stop walking into them! **")
        
        if monster < Dungon_size:
            chase_move = get_chase_move(monster, player)
            monster = move_player(monster, chase_move)
    else:
        print("\n ** What?? **")
        continue
   
    if player == monster:
        if player_has['sword']:
            print("\n**  You have slain the grue!")
            monster = Dungon_size #Move monster out of the dungon
        else:  
            print("\nChomp, Chomp: you just got eaten by the grue.\n")
            break        # You loose! Nothing else matters.

    if player == key:
        print("\n** You found a key!")
        key = pick_up('key')
    
    if player == sword:
        print("\n** You found a sword!")
        sword = pick_up('sword')

    if player == door:
        if player_has['key'] == True:
            print("\nYou found the door. You unlock it and step out to freedom.\n")
            break
        else:
            print("\nYou found the door. But it is locked. You can't get out.")
            