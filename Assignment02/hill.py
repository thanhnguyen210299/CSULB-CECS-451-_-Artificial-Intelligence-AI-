from board import Board
import time
import copy

class HillClimbingWithRandomRestart:
    def __init__(self, n_queens):
        # stores the number of the queens
        self.n_queens = n_queens
        #self.max_restart_times = restart_times
        #self.attempts = 0
        # stores the solution that meets the 5-queens problem
        self.best_solution = None

    """
        Hill climbing algorithm which allows restart after getting stuck from the initial state by randomly changing the position of 5 queens
    """
    def hill_climbing_with_restart(self):
        # If it gets too long to find solution (given 1000 trials)
        while True:
            #self.attempts += 1
            # Generate the intial board randomly
            self.best_solution = Board(self.n_queens)
            #self.best_solution.map = [[0,0,1,0,0],[0,0,0,0,1],[0,1,0,0,0],[0,0,0,1,0],[1,0,0,0,0]]

            if self.best_solution.get_fitness() == 0:
                return

            # If the new board has not met the requirement yet - number of attacking pairs >< 0
            if self.best_solution.get_fitness() != 0:
                # For each row of the board
                for i in range(self.n_queens):
                    current_board = copy.deepcopy(self.best_solution)
                    # Find the location where the queen is placed on row i
                    queen = 0
                    for j in range(self.n_queens):
                        if current_board.get_map()[i][j] == 1:
                            queen = j

                    # Change the status of that location from 1 to 0
                    current_board.flip(i, queen)

                    # Move the queen to its 4 neighbors to discover the best location (smallest number of attacking pairs)
                    for j in range(self.n_queens):
                        if j != queen:
                            neighbor = copy.deepcopy(current_board)
                            neighbor.flip(i, j)
                            #print(neighbor.get_map(), neighbor.get_fitness(), self.best_solution.get_fitness(), self.attempts)
                            if neighbor.get_fitness() < self.best_solution.get_fitness():
                                self.best_solution = copy.deepcopy(neighbor)

                    # If the solution is found then go back to main to print result
                    if self.best_solution.get_fitness() == 0:
                        return

    """
        Print the best solution of 5-Queens problem
    """
    def printBoard(self):
        for i in range(self.n_queens):
            row = "";
            for j in range(self.n_queens - 1):
                if self.best_solution.get_map()[i][j] == 1:
                    row += "1 "
                else:
                    row += "- "
            if self.best_solution.get_map()[i][self.n_queens - 1] == 1:
                row += "1"
            else:
                row += "-"
            print(row)
        #print(self.best_solution.get_map())

if __name__ == '__main__':
    
    hill_climber = HillClimbingWithRandomRestart(5)
    
    start_time = time.time()
    hill_climber.hill_climbing_with_restart()
    end_time = time.time()
    
    running_time = (end_time - start_time) * 1000  # in milliseconds
    print(f"Running time: {running_time:.0f}ms")
    hill_climber.printBoard()
