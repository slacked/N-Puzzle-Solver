import sys
import heapq

class Algorithm:
    def __init__(self, puzzle):
        self.puzzle = puzzle
        self.init_frontier_queue()
        self.nodes_expanded = 0

    def search(self):
        visited = set()
        frontier = set()
        frontier.add(self.puzzle)
        nodes_expanded = 0
        nodes_in_frontier = 1
        frontier_max = 1
        while not self.is_frontier_empty():
            frontier_max = max(frontier_max, self.frontier_size())
            current = self.get_next()
            visited.add(current.state)
            if current.state == Puzzle.goal_state(self.puzzle.size):
                node = current
                path = []
                while node.parent:
                    path.insert(0, str(node))
                    node = node.parent
                return {
                    'possible': True,
                    'path': path,
                    'nodes_expanded': nodes_expanded,
                    'nodes_in_frontier': nodes_in_frontier,
                    'frontier_size': frontier_max
                }
            elif nodes_expanded == 100000:
                return {
                'possible': False,
                'path': None,
                'nodes_expanded': nodes_expanded,
                'nodes_in_frontier': nodes_in_frontier,
                'frontier_size': frontier_max,
                }
            nodes_expanded += 1
            for child in current.children():
                if child.state not in visited and child.state not in frontier:
                    self.insert(child)
                    frontier.add(child.state)
                    nodes_in_frontier += 1

class BFS(Algorithm):
    def init_frontier_queue(self):
        self.frontier = Queue()
        self.frontier.enqueue(self.puzzle)

    def insert(self, node):
        self.frontier.enqueue(node)

    def get_next(self):
        return self.frontier.dequeue()

    def is_frontier_empty(self):
        return len(self.frontier) == 0

    def frontier_size(self):
        return len(self.frontier)

class AStarManhattan(Algorithm):
    def init_frontier_queue(self):
        self.frontier = PQueue()
        self.frontier.push(self.puzzle, self.puzzle.cost)

    def insert(self, node):
        self.frontier.push(node, node.cost + node.manhattan_distance(Puzzle.goal_state(self.puzzle.size), self.puzzle.size))

    def get_next(self):
        return self.frontier.pop()

    def is_frontier_empty(self):
        return len(self.frontier) == 0

    def frontier_size(self):
        return len(self.frontier)

class AStarMisplaced(Algorithm):
    def init_frontier_queue(self):
        self.frontier = PQueue()
        self.frontier.push(self.puzzle, self.puzzle.cost)

    def insert(self, node):
        self.frontier.push(node, node.cost + node.misplaced_tiles(Puzzle.goal_state(self.puzzle.size), self.puzzle.size))

    def get_next(self):
        return self.frontier.pop()

    def is_frontier_empty(self):
        return len(self.frontier) == 0

    def frontier_size(self):
        return len(self.frontier)

class Queue:
    def __init__(self):
        self.items = []
    def enqueue(self, item):
        self.items.insert(0, item)
    def dequeue(self):
        return self.items.pop()
    def isEmpty(self):
        return self.items == []
    def __len__(self):
        return len(self.items)

class PQueue:
    def __init__(self):
        self.queue = []
        self.index = 0
    def push(self, item, priority):
        heapq.heappush(self.queue, (priority, self.index, item))
        self.index += 1
    def pop(self):
        return heapq.heappop(self.queue)[-1]
    def __len__(self):
        return len(self.queue)

class Puzzle:
    def __init__(self, state, size, parent = None, cost = 0):
        self.size = size
        self.state = state
        self.parent = parent
        self.cost = cost

    def left(state, size):
        return (state.index(0) % size) != 0

    def move_left(state, size):
        s = list(state)
        i = s.index(0)
        s[i - 1], s[i] = s[i], s[i - 1]
        return tuple(s)

    def right(state, size):
        return (state.index(0) % size) != (size - 1)

    def move_right(state, size):
        s = list(state)
        i = s.index(0)
        s[i + 1], s[i] = s[i], s[i + 1]
        return tuple(s)

    def up(state, size):
        return state.index(0) >= size

    def move_up(state, size):
        s = list(state)
        i = s.index(0)
        s[i - size], s[i] = s[i], s[i - size]
        return tuple(s)

    def down(state, size):
        return (state.index(0) / size) < (size - 1)

    def move_down(state, size):
        s = list(state)
        i = s.index(0)
        s[i + size], s[i] = s[i], s[i + size]
        return tuple(s)

    def goal_state(size):
        goal_state = []
        for i in range(size ** 2):
            goal_state.append(i)
        return tuple(goal_state)

    def __str__(self):
        to_return = ""
        for i in range(self.size):
            for j in range(self.size):
                if str(self.state[self.size*i+j]) == "0":
                    to_return += ". "
                else:
                    to_return += str(self.state[self.size*i+j]) + " "
            to_return += "\n"
        return to_return

    def children(self):
        children = []
        if Puzzle.left(self.state, self.size):
            children.append(Puzzle(Puzzle.move_left(self.state, self.size), self.size, self, self.cost + 1))
        if Puzzle.right(self.state, self.size):
            children.append(Puzzle(Puzzle.move_right(self.state, self.size), self.size, self, self.cost + 1))
        if Puzzle.up(self.state, self.size):
            children.append(Puzzle(Puzzle.move_up(self.state, self.size), self.size, self, self.cost + 1))
        if Puzzle.down(self.state, self.size):
            children.append(Puzzle(Puzzle.move_down(self.state, self.size), self.size, self, self.cost + 1))
        return tuple(children)

    def manhattan_distance(self, goal_state, size):
        distance = 0
        for value in range(1, (size ** 2 - 1)):
            xs = self.state.index(value) % size
            ys = self.state.index(value) / size
            xg = goal_state.index(value) % size
            yg = goal_state.index(value) / size
            distance += abs(xs - xg) + abs(ys - yg)
        return distance

    def misplaced_tiles(self, goal_state, size):
        num_misplaced = 0
        for value in range(1, (size ** 2 - 1)):
            if self.state.index(value) != goal_state.index(value):
                num_misplaced += 1
        return num_misplaced

def start_state(filename):
    start_state = []
    puzzle_file = open(filename)
    lines = puzzle_file.readlines()
    length = 0
    for line in lines:
        length += 1
        line_numbers = line.strip().split(" ")
        for i in range(len(line_numbers)):
            if (line_numbers[i] == '.'):
                start_state.append(0)
            else:
                start_state.append(int(line_numbers[i]))
    return Puzzle(tuple(start_state), length)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Not enough arguments.")
        sys.exit(1)
    if len(sys.argv) > 3:
        print("Too many arguments.")
        sys.exit(1)
    start_state = start_state(sys.argv[2])
    method = None
    if sys.argv[1] == 'bfs':
        method = BFS(start_state)
    elif sys.argv[1] == 'astar_manhattan':
        method = AStarManhattan(start_state)
    elif sys.argv[1] == 'astar_misplaced':
        method = AStarMisplaced(start_state)
    else:
        print("Invalid search method")
        sys.exit(1)

    solved = method.search()
    if solved['possible']:
        print(start_state)
        for i in range(len(solved['path'])):
            print(solved['path'][i])
        print("-------- Efficiency Metrics --------\n")
        print("Num nodes added to frontier queue: %s\n" % solved['nodes_in_frontier'])
        print("Num nodes selected for expansion: %s\n" % solved['nodes_expanded'])
        print("Max size of queue at any given time: %s\n" % solved['frontier_size'])
    else:
        print("-------- Efficiency Metrics --------\n")
        print("No solution found (100k limit reached)\n")
        print("Num nodes added to frontier queue: %s\n" % solved['nodes_in_frontier'])
        print("Num nodes selected for expansion: %s\n" % solved['nodes_expanded'])
        print("Max size of queue at any given time: %s\n" % solved['frontier_size'])
