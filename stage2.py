import tkinter as tk
from tkinter import ttk
import random
import time
import heapq

# Node class for A* algorithm


class Node:
    def __init__(self, position, parent=None):
        self.position = position
        self.parent = parent
        self.g = 0
        self.h = 0
        self.f = 0

    def __lt__(self, other):
        return self.f < other.f

# Heuristic function for A* algorithm


def heuristic(current, goal):
    return abs(current[0] - goal[0]) + abs(current[1] - goal[1])

# A* search algorithm


def astar_search(start, goal, obstacles, board_size):
    open_list = []
    closed_set = set()
    start_node = Node(start)
    goal_node = Node(goal)
    heapq.heappush(open_list, start_node)

    while open_list:
        current_node = heapq.heappop(open_list)
        closed_set.add(current_node.position)

        if current_node.position == goal:
            path = []
            while current_node is not None:
                path.append(current_node.position)
                current_node = current_node.parent
            return path[::-1]

        for next_move in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_position = (current_node.position[0] + next_move[0], current_node.position[1] + next_move[1])

            if 0 <= new_position[0] < board_size and 0 <= new_position[1] < board_size \
                    and new_position not in obstacles and new_position not in closed_set:
                new_node = Node(new_position, current_node)
                new_node.g = current_node.g + 1
                new_node.h = heuristic(new_position, goal)
                new_node.f = new_node.g + new_node.h

                heapq.heappush(open_list, new_node)

    return None

# Backtracking algorithm


def backtrack(current, end_point, obstacles, board_size, visited):
    if current == end_point:
        return [current]

    visited.add(current)

    for next_move in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        new_position = (current[0] + next_move[0], current[1] + next_move[1])
        if 0 <= new_position[0] < board_size and 0 <= new_position[1] < board_size \
                and new_position not in obstacles and new_position not in visited:
            path = backtrack(new_position, end_point, obstacles, board_size, visited.copy())
            if path:
                return [current] + path

    return None

# Forest Navigation Game class


class ForestNavigationGame:
    def __init__(self, root, board_size=10):
        self.root = root
        self.board_size = board_size
        self.root.title("Forest Navigation - Compare Algorithms")
        self.root.geometry("800x600")

        self.stage_board = None
        self.obstacles = set()

        self.create_stage_board()
        self.place_obstacles()

        # Buttons to start each algorithm
        start_backtracking_button = ttk.Button(self.root, text="Start Backtracking", command=self.start_backtracking)
        start_backtracking_button.place(x=150, y=550)

        start_astar_button = ttk.Button(self.root, text="Start A*", command=self.start_astar)
        start_astar_button.place(x=450, y=550)
        self.backtracking_time = None
        self.astar_time = None
        self.time_display = ttk.Label(self.root, text="")
        self.time_display.place(x=350, y=520)

    def create_stage_board(self):
        board_frame = ttk.Frame(self.root, width=self.board_size * 55, height=self.board_size * 55, borderwidth=2,
                                relief="ridge")
        board_frame.place(x=50, y=50)

        self.stage_board = []
        for i in range(self.board_size):
            row = []
            for j in range(self.board_size):
                cell_color = "white"
                cell = tk.Canvas(board_frame, width=50, height=50, bg=cell_color, highlightthickness=0)
                cell.grid(row=i, column=j, padx=2, pady=2)
                row.append(cell)
            self.stage_board.append(row)

    def place_obstacles(self):
        for _ in range(10):
            i, j = random.randint(0, self.board_size - 1), random.randint(0, self.board_size - 1)
            while (i, j) in self.obstacles:
                i, j = random.randint(0, self.board_size - 1), random.randint(0, self.board_size - 1)
            self.obstacles.add((i, j))
            self.stage_board[i][j].configure(bg="red")

    def start_backtracking(self):
        self.obstacle_counter = 0  # Ajout d'un compteur d'obstacles pour backtracking
        start_point = (0, 0)
        end_point = (self.board_size - 1, self.board_size - 1)
        start_time = time.perf_counter()
        path = backtrack(start_point, end_point, self.obstacles, self.board_size, set())
        end_time = time.perf_counter()
        self.display_path(path, "blue")
        print("Backtracking Time:", end_time - start_time)

        self.backtracking_time = end_time - start_time
        self.update_time_display()
        for pos in path:
            if pos in self.obstacles:
                self.obstacle_counter += 1
        score = self.calculate_score(self.backtracking_time, self.obstacle_counter)
        print("Backtracking Score:", score)

    def start_astar(self):
        self.obstacle_counter = 0  # Ajout d'un compteur d'obstacles pour A*
        start_point = (0, 0)
        end_point = (self.board_size - 1, self.board_size - 1)
        start_time = time.perf_counter()
        path = astar_search(start_point, end_point, self.obstacles, self.board_size)
        end_time = time.perf_counter()
        self.display_path(path, "green")
        print("A* Time:", end_time - start_time)

        self.astar_time = end_time - start_time
        self.update_time_display()
        for pos in path:
            if pos in self.obstacles:
                self.obstacle_counter += 1
        score = self.calculate_score(self.astar_time, self.obstacle_counter)
        print("A* Score:", score)

    def display_path(self, path, color):
        if path:
            for pos in path:
                self.stage_board[pos[0]][pos[1]].configure(bg=color)
                self.root.update()
                time.sleep(0.5)

    def update_time_display(self):
        text = "Backtracking: {:.4f} s, A*: {:.4f} s".format(
            self.backtracking_time if self.backtracking_time is not None else 0,
            self.astar_time if self.astar_time is not None else 0
        )
        self.time_display.config(text=text)

    def compare_algorithms(self):
        if self.backtracking_time is not None and self.astar_time is not None:
            if self.backtracking_time < self.astar_time:
                result = "Backtracking is faster"
            elif self.backtracking_time > self.astar_time:
                result = "A* is faster"
            else:
                result = "Both algorithms took the same time"
            print(result)

    def calculate_score(self, time, obstacles_passed):
        # Vous pouvez ajuster la formule de score selon vos besoins
        return 1000 / (time + obstacles_passed)


root = tk.Tk()
game = ForestNavigationGame(root)
root.mainloop()

# Comparaison des algorithmes une fois que le jeu est terminé
game.compare_algorithms()
