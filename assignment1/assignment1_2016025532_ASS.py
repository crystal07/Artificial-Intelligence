# direction list : up, left, down, right
direction = [[0, 1], [-1, 0], [0, -1], [1, 0]]

# read maze file and get row, column size and maze
def get_maze (file_name = "input.txt") :
    # read input.txt file and parsing it to data.
    with open(file_name) as input_file:
        size = input_file.readline()
        size = size.split()
        row = int(size[0])
        col = int(size[1])
        maze = input_file.read().split()
        maze = list(map(int, maze))
        maze = [maze[i : i + col] for i in range(0, len(maze), col)]
    return maze, row, col

# return start position
def find_start_point (maze, row, col) :
    start = []
    for i in range(row) :
        for j in range(col) :
            if maze[i][j] == 3 :
                start.append(j)
                start.append(i)
                return start
    return [-1, -1]

def find_destination_point (maze, row, col) :
    destination_list = []
    for i in range(row) :
        for j in range(col) :
            if maze[i][j] == 4 :
                destination = []
                destination.append(j)
                destination.append(i)
                destination_list.append(destination)
    return destination_list

def write_maze (maze, depth, count, file_name = "output.txt") :
    output_file = open(file_name, "w")
    for i in maze :
        for j in i :
            output_file.write("{} ".format(j))
        output_file.write("\n")
    output_file.write("---\n")
    output_file.write("length={}\n".format(str(depth-1)))
    output_file.write("time={}\n".format(str(count)))

def print_maze (maze, row, col) :
    for i in range(row) :
        for j in range(col) :
            print(str(maze[i][j]), end = " ")
        print()

def trace_back (maze, row, col, parent, start, destination) :

    for i in range(row) :
        for j in range(col) :
            if maze[i][j] == 5 :
                maze[i][j] = 2

    depth = 0
    current = destination
    while start != current :
        depth = depth + 1
        current = parent[current[1]][current[0]]
        if current != start :
            maze[current[1]][current[0]] = 5
    return depth

def get_huristic_value (current_pos, destination_pos) :
    return min(list(map(lambda destination : (abs(destination[1] - current_pos[1])) + abs((destination[0] - current_pos[0])), destination_pos)))

def get_cost_from_start (parent, start, current) :
	pos = current
	cost = 0
	while start != pos :
		cost = cost + 1
		pos = parent[pos[1]][pos[0]]

	return cost

def a_star_search (maze, row, col, start) :
    parent_list = [[[-1, -1] for i in range(col)] for j in range(row)]

    priority_queue = []
    count = 0
    dest_list = find_destination_point(maze, row, col)
    huristic = get_huristic_value(start, dest_list) + get_cost_from_start(parent_list, start, start)
    priority_queue.append([huristic, start])

    
    while (len(priority_queue) != 0) :
        pos = min(priority_queue, key= lambda pq : pq[0])
        priority_queue.remove(pos)
        pos = pos[1]

        if maze[pos[1]][pos[0]] == 4 :
            return pos, parent_list, count + 1
        else :
            parent_pos = pos
            for i in direction :
                new_pos = [-1, -1]
                new_pos[0] = parent_pos[0] + i[0]
                new_pos[1] = parent_pos[1] + i[1]

                if (0 <= new_pos[0] < col and 0 <= new_pos[1] < row) == False:
                    continue

                if maze[new_pos[1]][new_pos[0]] == 4 :
                    parent_list[new_pos[1]][new_pos[0]] = parent_pos
                    huristic = get_huristic_value(new_pos, dest_list) + get_cost_from_start(parent_list, start, new_pos)
                    priority_queue.insert(0, [huristic, new_pos])
                    break
                elif maze[new_pos[1]][new_pos[0]] != 2 :
                    continue

                count = count + 1
                parent_list[new_pos[1]][new_pos[0]] = parent_pos

                if maze[new_pos[1]][new_pos[0]] == 2 :
                    maze[new_pos[1]][new_pos[0]] = 5
                    huristic = get_huristic_value (new_pos, dest_list) + get_cost_from_start(parent_list, start, new_pos)
                    priority_queue.insert(0, [huristic, new_pos])

                #print("current maze with priority queue", str(priority_queue))
                #print_maze(maze, row, col)

    return [-1, -1], parent_list, count

maze, row, col = get_maze()
start = find_start_point(maze, row, col)
if start == [-1, -1] :
    print("no starting point")
    exit()

dest, parent, count = a_star_search (maze, row, col, start)
if dest == [-1, -1] :
    print("destination not founded")
    exit()

depth = trace_back (maze, row, col, parent, start, dest)
write_maze (maze, depth, count)
