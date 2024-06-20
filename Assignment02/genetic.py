from board import Board
import time
import copy
import random

class GeneticAlgorithm:
    def __init__(self, n_queens, population_size):
        # stores number of queens
        self.n_queens = n_queens
        # store number of states
        self.population_size = population_size
        # store the population which is the states that will be used
        self.population = []
        # stores the string that represents the status of each board in the population
        self.converted_population = []
        # stores the max number of attacking pairs max_attacking)pairs = n * (n-1) // 2
        self.max_attacking_pairs = n_queens * (n_queens - 1) // 2
        # stores the best solution that meets the requirement of N-queens problem
        self.best_solution = None

    """
        Generate 8 intial states for the population
    """
    def generate_initial_population(self):
        for i in range(self.population_size):
            self.population.append(Board(self.n_queens))

    """
        Convert a state of the population into string.
        Element i in the string will represent the colunm that the queen is placed in row i
    """
    def encoding(self):
        for i in range(self.population_size):
            chromo = ''
            for j in range(self.n_queens):
                for k in range(self.n_queens):
                    if self.population[i].get_map()[j][k] == 1:
                        chromo += str(k)
            #print(chromo, self.population[i].get_fitness())
            self.converted_population.append(chromo)

    """
        Calulate the total non-attacking pairs in the population and assign the probabilities of the boards based on the number of non-attacking pairs
        Return:
            total_non_attacking_pairs
            fitness_scores - a list that stores the probability of each board in the population
    """
    def get_fitness_scores(self):
        # Calculate the total number of attcaking pairs
        total_non_attacking_pairs = 0
        for chromosome in self.population:
            total_non_attacking_pairs += self.max_attacking_pairs - chromosome.get_fitness()

        # Calculate the percentage of each board in the population based on the number of non-attacking pairs
        fitness_scores = []
        for board in self.population:
            fitness_scores.append(round((self.max_attacking_pairs - board.get_fitness()) * 100 / total_non_attacking_pairs, 0))

        return total_non_attacking_pairs, fitness_scores

    """
        Select 8 states based on the random choices (choose 2 chromosomes k = 2) and initial states' probabilities for reproduction
        Input: the probabilites of the population
        Output: 8 selected states to pair
    """
    def selection_1(self, probabilities):
        selected_chromo = []

        for i in range(self.population_size // 2):
            selected_indices = random.choices(range(self.population_size), probabilities, k = 2)
            #print(selected_indices)
            for index in selected_indices:
                selected_chromo.append(self.converted_population[index])

        #print(selected_chromo)
        
        return selected_chromo

    """
        Select 8 states based on the random number and initial states' probabilities for reproduction
        Input: the probabilites of the population
        Output: 8 selected states to pair
    """
    def selection(self, probabilities):
        added_percentages = []
        temp = 0
        for i in range(self.population_size):
            temp += probabilities[i]
            added_percentages.append(temp)
        #print(added_percentages)

        selected_chromo = []
        for i in range(self.population_size):
            r = random.randint(0, added_percentages[self.population_size - 1])
            j = 0
            while r > added_percentages[j] and j < (self.population_size - 1):
                j += 1
            #print(r, j)
            selected_chromo.append(self.converted_population[j])
        #print(selected_chromo)
        
        return selected_chromo

    """
        For each pair from the selected states, choose a random position to exchange the genes
        Input: 8 selected states
        Output: 8 states after getting crossover
    """
    def crossover(self, parents):
        offsprings = []
        for i in range(0, self.population_size, 2):
            crossover_point = random.randint(0, self.n_queens - 1)
            offspring1 = str(parents[i])[:crossover_point] + str(parents[i + 1])[crossover_point:]
            offspring2 = str(parents[i + 1])[:crossover_point] + str(parents[i])[crossover_point:]
            offsprings.append(offspring1)
            offsprings.append(offspring2)
        #print(offsprings)

        return offsprings

    """
        Mutate each chromosome in the population by choosing a random gene to get changed in range from 1 to 5 which is the position where the queen will be placed
        Input: a chromosome
        Output: a mutated chromosome
    """
    def mutation(self, chromosome):
        random_gene = random.randint(0, self.n_queens - 1)
        for i in range(self.n_queens):
            if i == random_gene:
                r = random.randint(0, self.n_queens - 1)
                listed_chromosome = list(chromosome)
                listed_chromosome[random_gene] = str(r)
        
        return("".join(listed_chromosome))

    """
        Convert a 5-element string to the a 5x5 board
        Input:
            position - the position of the chromosome in the population
            chromosome - a string that represents one state of a population
    """
    def decoding(self, position, chromosome):
        for i in range(self.n_queens):
            for j in range(self.n_queens):
                self.population[position].map[i][j] = 0
        
        for i in range(len(chromosome)):
            self.population[position].map[i][int(chromosome[i])] = 1

    """
        Genetic Algorithm
    """
    def genetic_algorithm(self):
        # Generate 8 initial states
        self.generate_initial_population()
        #self.population[3].map = [[0,0,1,0,0],[0,0,0,0,1],[0,1,0,0,0],[0,0,0,1,0],[1,0,0,0,0]]
        for i in range(self.population_size):
            if self.population[i].get_fitness() == 0:
                self.best_solution = copy.deepcopy(self.population[i])
                return
        while True:
            # Convert 8 boards into 8 strings for next steps
            self.encoding()
            # Calculate the total fitness scores of the population and the probabilities of each state in the population
            total_fitness, board_fitness_scores = self.get_fitness_scores()
            #print(total_fitness)
            selected_parents = self.selection_1(board_fitness_scores)
            offsprings = self.crossover(selected_parents)
            for i in range(self.population_size):
                new_child = self.mutation(offsprings[i])
                #print(new_child)
                # Convert the string that represents the chromosome back to 5x5 board
                self.decoding(i, new_child)
                #print(self.population[i].get_map(), self.population[i].get_fitness())
                # If the get_fitness() return 0 which means that the requirement is met - no attacking pairs
                if self.population[i].get_fitness() == 0:
                    self.best_solution = copy.deepcopy(self.population[i])
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
    # Genetic Algorithm for 5-Queens problem using 8 distinct states
    genetic = GeneticAlgorithm(5, 8)
    
    start_time = time.time()
    genetic.genetic_algorithm()
    end_time = time.time()
    
    running_time = (end_time - start_time) * 1000  # in milliseconds
    print(f"Running time: {running_time:.0f}ms")
    genetic.printBoard()
