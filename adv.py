from room import Room
from player import Player
from world import World
from util import Queue, Stack
import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Fill this out with directions to walk
# handles when we need to go back because all exits to current have been visited
def opposite(direction):
  if direction == "n":
    return "s"
  elif direction == "s":
    return "n"
  elif direction == "e":
    return "w"
  elif direction == "w":
    return "e"
  else:
    return f'{bcolors.WARNING}Not a valid direction'

visited_rooms = set()                       # rooms we've visited in a tuple so we don't track duplicates
traversal_path = []                         # the traversal path our test will take to visit each room
player.current_room = world.starting_room   # init our player's starting room
current_directions = []                     # will store available exits when we call get_exits()

while len(visited_rooms) < 500:
    visited_rooms.add(player.current_room)      
    exits = player.current_room.get_exits()     # rooms available to us depenging on current room we're in (returns list)
    print(f'{player.current_room}')
    print(f'{bcolors.OKGREEN}MOVING ON')

    """
    Check if our directions exist in the directions list we get back from get_exits() (exits) AND if the room in that direction has been visited
        if so, we will append that direction to current_directions,
        also append to traversal_path,
        and set our player's current room to be the one in THAT direction (the one we did the checking for)
    """
    current = player.current_room
    if "n" in exits and current.get_room_in_direction("n") not in visited_rooms:
        current_directions.append('n')
        traversal_path.append('n')
        player.current_room = current.get_room_in_direction("n")

    elif "w" in exits and current.get_room_in_direction("w") not in visited_rooms:
        current_directions.append('w')
        traversal_path.append('w')
        player.current_room = current.get_room_in_direction("w")

    elif "s" in exits and current.get_room_in_direction("s") not in visited_rooms:
        current_directions.append('s')
        traversal_path.append('s')
        player.current_room = current.get_room_in_direction("s")

    elif "e" in exits and current.get_room_in_direction("e") not in visited_rooms:
        current_directions.append('e')
        traversal_path.append('e')
        player.current_room = current.get_room_in_direction("e")

    # Otherwise we want to go back to the previous room since all rooms we checked are already in the visited_rooms set, and set our player's current room to the one we came from
    else:
        previous_direction = current_directions.pop()
        opposite_direction = opposite(previous_direction)
        traversal_path.append(opposite_direction)
        player.current_room = player.current_room.get_room_in_direction(opposite_direction)


for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
