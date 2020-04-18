# There are a few smaller graphs in the file which you can test your traversal method on before committing to the large graph. You may find these easier to debug.


# You can find the path to the shortest unexplored room by using a breadth-first search for a room with a '?' for an exit.
#  If you use the bfs code from the homework, you will need to make a few modifications.

# Instead of searching for a target vertex, you are searching for an exit with a '?' as the value.
# If an exit has been explored, you can put it in your BFS queue like normal.

# BFS will return the path as a list of room IDs. You will need to convert this to a list of n/s/e/w directions before you can add it to your traversal path.

# If all paths have been explored, you're done!

# plan



from util import Stack, Queue
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
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()
print(len(world.rooms), "this is the length of world")
player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']

# added current room to visited


# store possible directions
def unexplored_rooms(room_id):
 # set each direction to a ?
    possible_directions = {}

    if "n" in room_graph[room_id][1].keys():
        possible_directions['n'] = '?'

    if "e" in room_graph[room_id][1].keys():
        possible_directions['e'] = '?'
    if "s" in room_graph[room_id][1].keys():
        possible_directions['s'] = '?'
    if "w" in room_graph[room_id][1].keys():
        possible_directions['w'] = '?'

    return possible_directions
    # broke code
    # for path in player.current_room.get_exits():
    #     unexplored.append("?")
    #     print(unexplored)

# need to add opposites when looking at next room, since when entering a room it should swap the opposite
def next_room_exits(next_id, next_direction):

    opposites = {'n': 's', 's': 'n', 'e': 'w', 'w': 'e'}
    next_array = []
    previous_array = []

    for direction in room_graph[next_id][1].keys():

        if direction == 'n':
            next_array.append('s')

        if direction == 's':
            next_array.append('n')

        if direction == 'e':
            next_array.append('w')

        if direction == 'w':
            next_array.append('e')

    for item in room_graph[next_id][1].keys():
        previous_array.append(opposites[item])

    if next_direction in next_array:

        return True
    else:
        return False


# BFT to find the nearest unexplored exit with '?'

# Start by writing an algorithm that picks a random unexplored direction from the player's current room


def maze_pathfinding(start_room):
    # id
    room_id = (start_room)
    # getting start directions
    visited = {start_room: unexplored_rooms(start_room)}
    room_choice_len = len(room_graph[start_room][1].keys())
    opposites = {'n': 's', 's': 'n', 'e': 'w', 'w': 'e'}
    current_room = start_room
    moves = []
    # DFS type loop
    while (len(visited) < len(world.rooms)):

        # keeping running until out of ? or dead end
        while '?' in visited[current_room].values():

            # current room directions
            room_directions = visited[current_room]
            room_exits = []
            index = 0
            # setting room exits
            for item in list(room_directions.values()):
                if item == '?':
                    room_exits.append(list(room_directions.keys())[index])

                index += 1
            # break loop if dead end
            if len(room_exits) == 0:
        
                break

            # pick a random direction

            new_direction = room_exits[random.randrange(len(room_exits))]
            # print(new_direction)
            next_room = room_graph[current_room][1][new_direction]
            # print(next_room)

            check_next_room = next_room_exits(next_room, new_direction)

            # traversal_path.append(new_direction)
            moves.append(new_direction)

            if check_next_room == True:

                print(new_direction)

                visited[current_room][new_direction] = next_room

                if next_room not in visited:
                    visited[next_room] = unexplored_rooms(next_room)
                    print(visited[next_room])
                    visited[next_room][opposites[new_direction]] = current_room

                else:
                    visited[next_room][opposites[new_direction]] = current_room

            if check_next_room == False:
                if next_room not in visited:

                    visited[current_room][new_direction] = next_room
                    visited[next_room] = unexplored_rooms(next_room)

            current_room = next_room

        # BFS
        while len(visited) < len(world.rooms) and '?' not in visited[current_room].values():

            queue = Queue()
            player_room_directions = visited[current_room]
            v = set()
            for key, value in player_room_directions.items():
                queue.enqueue([value,[key]])

            while queue.size() > 0:
             
                this_one = queue.dequeue()
                room = this_one[0]
                if room not in v:
             
                    if '?' in visited[room].values():
                    
                        current_room = room
                        moves += this_one[1]
                        break
                v.add(room)

                player_room_directions = visited[room]
                for key, value in player_room_directions.items():
                    path_copy = this_one[1].copy()
                    path_copy.append(key)
                    queue.enqueue([value, path_copy])
                

 
        print(len(visited))

    return moves






# This should cause your player to walk a depth-first traversal. When you reach a dead-end (i.e. a room with no unexplored paths)
# , walk back to the nearest room that does contain an unexplored path.

#

# TRAVERSAL TEST

total_steps = maze_pathfinding(player.current_room.id)
traversal_path = total_steps
visited_rooms = set()

player.current_room = world.starting_room
visited_rooms.add(player.current_room)
# print(random_direction())







for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
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





def random_direction():
    # get room exits
    exits = player.current_room.get_exits()
    visited_rooms.add(player.current_room)

    print(unexplored_rooms(player.current_room.id))
    # get random direction
    direction = exits[random.randint(0, len(exits) - 1)]
    # travel
    player.travel(direction)
    visited_rooms.add(player.current_room)
    #  travels and logs that direction,
    print(player.current_room.print_room_description(player))
    # then loops.
    while (len(visited_rooms) < len(world.rooms)):

        exits = player.current_room.get_exits()
        print(unexplored_rooms(player.current_room.id))
        direction = exits[random.randint(0, len(exits) - 1)]
        print(direction, "this is a direction")
        player.travel(direction)
        traversal_path.append(player.current_room)
        visited_rooms.add(player.current_room)
        print(player.current_room.print_room_description(
            player), "faewafeafaewfeaw")
