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

def iterative_deepening_search (maze, row, col, pos) :
    depth = 0
    count = 0

    while True :
        founded_pos, count = depth_limited_search(maze, row, col, pos, depth, count)
        if founded_pos[0] != -1 and founded_pos[1] != -1 :
            return depth, count
        depth = depth + 1

def depth_limited_search (maze, row, col, start, depth, count) :
    count = count + 1
    if maze[start[1]][start[0]] == 4 :
        return start, count
    elif depth <= 0 :
        return [-1, -1], count

    #if start[0] >= col or start[1] >= row or start[0] < 0 or start[1] < 0 :
    #    return [-1, -1], count

    for i in direction :
        pos = []
        pos.append(start[0] + i[0])
        pos.append(start[1] + i[1])

        # case of over map size
        if pos[0] >= col or pos[1] >= row or pos[0] < 0 or pos[1] < 0 :
            continue

        if maze[pos[1]][pos[0]] == 4 :
            pass
        elif maze[pos[1]][pos[0]] != 2 :
            continue

        if maze[pos[1]][pos[0]] == 2 :
            maze[pos[1]][pos[0]] = 5

        #print("new road with depth ", str(depth))
        #print_maze(maze, row, col)

        founded, count = depth_limited_search(maze, row, col, pos, depth - 1, count)
        if founded != [-1, -1] :
            return founded, count
        maze[pos[1]][pos[0]] = 2

    return [-1, -1], count

maze, row, col = get_maze()
start = find_start_point(maze, row, col)
if start == [-1, -1] :
    print("no starting point")
    exit()
depth, count = iterative_deepening_search(maze, row, col, start)
write_maze (maze, depth, count)
