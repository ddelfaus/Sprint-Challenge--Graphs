# There are a few smaller graphs in the file which you can test your traversal method on before committing to the large graph. You may find these easier to debug.



# You can find the path to the shortest unexplored room by using a breadth-first search for a room with a '?' for an exit.
#  If you use the bfs code from the homework, you will need to make a few modifications.

# Instead of searching for a target vertex, you are searching for an exit with a '?' as the value. 
# If an exit has been explored, you can put it in your BFS queue like normal.

# BFS will return the path as a list of room IDs. You will need to convert this to a list of n/s/e/w directions before you can add it to your traversal path.

# If all paths have been explored, you're done!

from room import Room
from player import Player
from world import World

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
print(len(world.rooms), "this is the length of world")
player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []
visited_rooms = set()

#added current room to visited
visited_rooms.add(player.current_room)

# Start by writing an algorithm that picks a random unexplored direction from the player's current room

def random_direction():
    #get room exits
    exits = player.current_room.get_exits()
    print(exits, "test")
    #get random direction
    direction = exits[random.randint(0, len(exits) - 1)]
    #travel
    player.travel(direction)
    visited_rooms.add(player.current_room)
    print(player.current_room.print_room_description(player))

    while (len(visited_rooms) < len(world.rooms)):
        exits = player.current_room.get_exits()
        direction = exits[random.randint(0, len(exits) - 1)]
        player.travel(direction)
        visited_rooms.add(player.current_room)
        print(player.current_room.print_room_description(player))

#  travels and logs that direction, then loops. 




# This should cause your player to walk a depth-first traversal. When you reach a dead-end (i.e. a room with no unexplored paths)
# , walk back to the nearest room that does contain an unexplored path.


#
























# TRAVERSAL TEST

player.current_room = world.starting_room
visited_rooms.add(player.current_room)
print(random_direction())
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
