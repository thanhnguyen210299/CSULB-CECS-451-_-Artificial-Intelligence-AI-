from board import Board
import time
import copy
import numpy as np

class HillClimbingWithRandomRestart:
    def __init__(self, n_queens, max_restarts):
        self.n_queens = n_queens
        self.max_restarts = max_restarts
        self.best_solution = None
        self.best_fitness = n_queens * (n_queens - 1) // 2
        self.running_time = 0

    def hill_climbing_with_restart(self):
        attempts = 0
        start_time = time.time()

        while attempts < self.max_restarts:
            current_board = Board(self.n_queens)
            current_fitness = current_board.get_fitness()

            while current_fitness > 0:
                neighbor_boards = []

                for i in range(self.n_queens):
                    for j in range(self.n_queens):
                        if current_board.get_map()[i][j] == 0:
                            neighbor = copy.deepcopy(current_board)
                            neighbor.flip(i, j)
                            neighbor_fitness = neighbor.get_fitness()
                            neighbor_boards.append((neighbor, neighbor_fitness, i, j))

                neighbor_boards.sort(key=lambda x: x[1])

                if neighbor_boards[0][1] < current_fitness:
                    current_board = neighbor_boards[0][0]
                    current_fitness = neighbor_boards[0][1]
                else:
                    break

            if current_fitness < self.best_fitness:
                self.best_solution = current_board.get_map()
                self.best_fitness = current_fitness

            attempts += 1

        end_time = time.time()
        self.running_time = (end_time - start_time) * 1000  # in milliseconds

    def printBoard(self):
        print(f"Running time: {self.running_time:.0f}ms")
        for i in range(self.n_queens):
            row = "";
            for j in range(self.n_queens):
                if self.best_solution[i][j] == 1:
                    row += "1"
                else:
                    row += "-"
            print(row)
        print(self.best_solution)

if __name__ == '__main__':
    n_queens = 5
    hill_climber = HillClimbingWithRandomRestart(n_queens, 1000)
    hill_climber.hill_climbing_with_restart()
    hill_climber.printBoard()
