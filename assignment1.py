# Name this file to assignment1.py when you submit
import math


def distance(node, goal):
    return math.sqrt(pow((goal[0] - node[0]), 2) + pow((goal[1] - node[1]), 2))


# def compare(node1, node2):
#     if (node1[1] + node1[2]) < (node2[1] + node2[2]):
#         return 1
#     elif (node1[1] + node1[2]) > (node2[1] + node2[2]):
#         return -1
#     else:
#         return 0
def compare(node1):
    return node1[1] + node1[2]


def pathfinding(input_filepath):
    # input_filepath contains the full path to a CSV file with the input grid
    file = open(input_filepath, 'r')
    maze = []
    for line in file:
        line = line.rstrip('\n')
        lines = line.split(",")
        maze.append(lines)

    start = []
    goal = []

    for i in range(len(maze)):
        for j in range(len(maze[i])):
            if maze[i][j] == 'S':
                start = [i, j]
                break

    for i in range(len(maze)):
        for j in range(len(maze[i])):
            if maze[i][j] == 'G':
                goal = [i, j]
                break

    frontier = [[start, 0, distance(start, goal)]]

    # optimal_path is a list of tuples indicated the optimal path from start to goal
    # explored_list is the list of nodes explored during search
    # optimal_path_cost is the cost of the optimal path from the start state to the goal state

    explored = []
    explored_list = []
    hazard = []
    optimal_path = []

    def danger(node):
        x = node[0]  # row of the hazard node
        y = node[1]  # column of the hazard node
        if not [x, y] in hazard:
            hazard.append([x, y])  # add hazard node to hazard list
        if x - 1 >= 0:
            if not [x - 1, y] in hazard:
                hazard.append([x - 1, y])  # add the top hazard node to hazard list
        if x + 1 < len(maze):
            if not [x + 1, y] in hazard:
                hazard.append([x + 1, y])  # add the bottom hazard node to hazard list
        if y - 1 >= 0:
            if not [x, y - 1] in hazard:
                hazard.append([x, y - 1])  # add the left hazard node to hazard list
        if y + 1 < len(maze[0]):
            if not [x, y + 1] in hazard:
                hazard.append([x, y + 1])  # add the right hazard node to hazard list

    while frontier:
        current = frontier.pop(0)
        if current in explored:
            pass
        else:
            explored.append(current)
        if current[0] == goal:
            optimal_path.append(current[0])
            state = current[0]
            total_explored = len(explored) - 1
            while total_explored > 0:

                if state == explored[total_explored][0]:
                    optimal_path.append(explored[total_explored][3])
                    state = explored[total_explored][3]
                total_explored = total_explored - 1
            optimal_path.reverse()
            for path in explored:
                if path[0] in explored_list:
                    pass
                else:
                    explored_list.append(path[0])
            optimal_path_cost = current[1]
            return optimal_path, explored_list, optimal_path_cost
        else:
            row = current[0][0]
            column = current[0][1]
            up = row - 1
            down = row + 1
            left = column - 1
            right = column + 1
            if up >= 0:
                if (up - 1) >= 0 and maze[up - 1][column] == 'H':
                    danger([up - 1, column])
                if left >= 0 and maze[up][left] == 'H':
                    danger([up, left])
                if right < len(maze[0]) and maze[up][right] == 'H':
                    danger([up, right])
                if not (hazard.count([up, column]) > 0) and not maze[up][column] == 'X' and not (
                        frontier.count([[up, column],
                                        current[1] + 1, distance([up, column], goal)]) in frontier):
                    frontier.append([[up, column],
                                     current[1] + 1, distance([up, column], goal), [row, column]])
                    frontier.sort(key=compare)
            if down < len(maze):
                if (down + 1) < len(maze) and maze[down + 1][column] == 'H':
                    danger([down + 1, column])
                if left >= 0 and maze[down][left] == 'H':
                    danger([down, left])
                if right < len(maze[0]) and maze[down][right] == 'H':
                    danger([down, right])
                if not (([down, column]) in hazard) and not maze[down][column] == 'X' \
                        and not ([[down, column], current[1] + 1, distance([down,
                                                                                           column],
                                                                                          goal)] in frontier):
                    frontier.append([[down, column], current[1] + 1, distance([down,
                                                                               column], goal), [row, column]])
                frontier.sort(key=compare)
            if left >= 0:
                if (left - 1) >= 0 and maze[row][left - 1] == 'H':
                    danger([row, left - 1])
                if up >= 0 and maze[up][left] == 'H':
                    danger([up, left])
                if down < len(maze) and maze[down][left] == 'H':
                    danger([down, left])
                if not ([row, left] in hazard) and not maze[row][left] == 'X' \
                        and not ([[row, left], current[1] + 1, distance([row,
                                                                                        left],
                                                                                       goal)] in frontier):
                    frontier.append([[row, left], current[1] + 1, distance([row,
                                                                            left],
                                                                           goal), [row, column]])
                    frontier.sort(key=compare)
            if right < len(maze[0]):
                if (right + 1) < len(maze[0]) and maze[row][right + 1] == 'H':
                    danger([row, right + 1])
                if up >= 0 and maze[up][right] == 'H':
                    danger([up, right])
                if down < len(maze) and maze[down][right] == 'H':
                    danger([down, right])
                if not ([row, right] in hazard) and not maze[row][right] == 'X' \
                        and not ([[row, right], current[1] + 1, distance([row,
                                                                           right],
                                                                          goal)] in frontier):
                    frontier.append([[row, right], current[1] + 1, distance([row,
                                                                             right],
                                                                            goal), [row, column]])
                    frontier.sort(key=compare)


if __name__ == '__main__':
    data = pathfinding('D:\\Downloads\\Examples\\Examples\\Example3\\input.txt')
    print("optimal path: ")
    print(data[0])
    print()
    print("explored: ")
    print(data[1])
    print()
    print("path cost")
    print(data[2])
