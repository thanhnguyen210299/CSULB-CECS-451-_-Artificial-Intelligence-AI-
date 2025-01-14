from board import Board
import random
import numpy as np
import time

#Necessary to be able to update the board with wanted values
#Makes the board have all 0's in order to create the mutated board
def reset_board(board):
	for i in range(5):
		for j in range(5):
			board.get_map()[i][j] = 0
	return board

#Updates the board to the given state by using a blank board
def update_board(board,state):
	for num in range(len(state)):
		board.get_map()[num][int(state[num]) - 1] = 1
		

#Retrieves the numeric string associated with a board
#in order to make it easier to do the crossover
def get_chromosome_status(chromosome):
    n_queens = 5
    chromo = ''
    for i in range(n_queens):
        for j in range(n_queens):
            if chromosome.get_map()[i][j] == 1:
                chromo += str(j)
    return chromo


#Part A of the algorithm
#Generates the intial states, 8 in this case
def generate_initial_population(population_size):
    population = []
    for i in range(population_size):
        population.append(Board(5))
    return population


#Part B
#Fitness function that determines the parents of the offsprings
#Creates a dictionary of the percentages that each state has a chance of being selected as a parent
#rounded to two decimal

3points
def fitness(population_fitness_scores, attacking_pairs):
    check_percent = 0
    percentages = {}
    for chromosome in population_fitness_scores:
        percentages.update({chromosome:round((10 - population_fitness_scores.get(chromosome))/attacking_pairs,2)})
        check_percent += percentages.get(chromosome)
    for x, y in percentages.items():
        print(x, y)
    print(check_percent)
    return percentages
	

#Part C: Selection for reproduction
#Using the percentages for each state the program assigns it a letter value
#it randomly generates a number and if it falls under that range it selects that number like in the slides
#returns a list of the selected parents
def pair_selection(state_percentages):
    letters = ["A","B","C","D","E","F","G","H"]
    letter_percentages = {}
    letter_state = {}
    for letter,state in zip(letters,state_percentages):
        letter_percentages.update({letter: state_percentages.get(state)})
        letter_state.update({letter: state})
    pairs_selected = []
    for i in range(8):
        r = round(random.random(),2)
        #print(r)
        if r <=  letter_percentages.get("A"):
            pairs_selected.append("A")
        elif r <= (letter_percentages.get("A") + letter_percentages.get("B")):
            pairs_selected.append("B")
        elif r <= (letter_percentages.get("A") + letter_percentages.get("B") + letter_percentages.get("C")):
            pairs_selected.append("C")
        elif r <= letter_percentages.get("A") + letter_percentages.get("B") + letter_percentages.get("C") +letter_percentages.get("D"):
            pairs_selected.append("D")
        elif r <= letter_percentages.get("A") + letter_percentages.get("B") + letter_percentages.get("C") +letter_percentages.get("D") + letter_percentages.get("E"):
            pairs_selected.append("E")
        elif r <= letter_percentages.get("A") + letter_percentages.get("B") + letter_percentages.get("C") +letter_percentages.get("D") + letter_percentages.get("E") + letter_percentages.get("F"):
            pairs_selected.append("F")
        elif r <= letter_percentages.get("A") + letter_percentages.get("B") + letter_percentages.get("C") +letter_percentages.get("D") + letter_percentages.get("E") + letter_percentages.get("F") + letter_percentages.get("G"):
            pairs_selected.append("G")
        else:
            pairs_selected.append("H")
    print(pairs_selected)

    states_selected = []
    for letter in pairs_selected:
        states_selected.append(letter_state.get(letter))
    print(states_selected)
    return states_selected
        

            


#Part D: Crossover
#Splices the parents into the children by selecting a random index as the point to split at
#Creates the children from these parents and returns a list of children
def crossover(parents):
    random_index = random.randint(1,4)
    pairs = []
    for i in range(0, len(parents),2):
        pair = [parents[i],parents[i+1]]
        pairs.append(pair)
    #print("PAIRS",pairs)

    children = []
    for pair in pairs:
        child1 = pair[0][:random_index] + pair[1][random_index:]
        child2 = pair[1][:random_index] + pair[0][random_index:]
        children.append(child1)
        children.append(child2)
    #print(children)
    return children

#Part E
#Mutates the given chromosome by selecting a random index
#Once the random index is selected it is changed between the number 1 and 5 
#Once the string is changed we revert it back to a string and return the 
#new chromosome
def mutate(chromosome):
	#print("OG", chromosome)
	random_gene = random.randint(0,len(chromosome))
	for i in range(len(chromosome)):
		if i == random_gene:
			random_change = random.randint(1,5)
			modified = list(chromosome)
			modified[i] = random_change
			chromosome = ''
			for i in modified:
				chromosome += str(i)
	#print("mutated",chromosome)
	return chromosome
def printBoard(board):
        for i in range(5):
            row = "";
            for j in range(5 - 1):
                if board.get_map()[i][j] == 1:
                    row += "1 "
                else:
                    row += "- "
            if board.get_map()[i][5 - 1] == 1:
                row += "1"
            else:
                row += "-"
            print(row)

if __name__ == '__main__':
    population_size = 8
    solution = None

    #Creates the initial population
    population = generate_initial_population(population_size)

   # while solution != 0:
        #Creates the numeric strings for each board
    converted_population = []
    for chromosome in population:
        converted_population.append(get_chromosome_status(chromosome))
    print(converted_population)

        #Creates a relationship between the numeric string and board
    population_to_status = {}
    for converted, chromo in zip(converted_population, population):
        population_to_status.update({converted: chromo})
    #print(population_to_status)

        #Creates a relation between the fitness score and numeric string
        #Also gathers the number of attacking pairs
    total_attacking_pairs = 0
    status_fitness = {}
    for coverted in converted_population:
        status_fitness.update({converted: population_to_status.get(coverted).get_fitness()})
        total_attacking_pairs += 10 - status_fitness.get(converted)
        print(status_fitness)
    print(total_attacking_pairs)

    percentages_for_crossover = fitness(status_fitness,total_attacking_pairs)
    parents = pair_selection(percentages_for_crossover)
    print(parents)
"""
        children = crossover(parents)
        #print("CHILD",children)

        mutants = []
        for child in children:
            new_child = mutate(child)
            mutants.append(new_child)
        #print("Mutated children", mutants)

        for mutant in mutants:
            mutated_board = Board(5)
            reset_board(mutated_board)
            update_board(mutated_board, mutant)
            #mutated_board.show_map()
            solution = mutated_board.get_fitness()
            if solution == 0:
                printBoard(mutated_board)
                print()
                break
    end_time = time.perf_counter()
    overall_time = end_time - start_time
    print("Running time:", overall_time, "ms")
    """
