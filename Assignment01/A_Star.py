"""
    *** Thanh Nguyen _ ID: 026843815
    *** CECS 451 - AI
    *** Assignment 01 - A* Algorithm
"""

import sys
import math
import heapq

""" Reading coordinates.txt file to get the location of cities
    Input: the file path
    Return: a dictionary - city name as key and their coordinates
"""
def getCityCoordinates(filePath):
    cities = {}
    with open(filePath, "r") as f:
        for line in f:
            name, coordinates = line.strip().split(':')
            lat, long = coordinates.strip('()').split(',')
            cities[name] = {'name': name, 'latitude': float(lat), 'longitude': float(long)}
    return cities

""" Reading map.txt file to get the map between cities
    Input: the path of a file
    Return: a dictionary - each city is a key and a list of neighbors with distance
"""
def createMap(filePath):
    graph = {}
    with open(filePath, "r") as f:
        for line in f:
            vertice, edges = line.strip().split('-')
            graph[vertice] = []
            pairs = edges.split(',')
            # Get adjacency list
            for pair in pairs:
                neighbor, distance = pair.strip('()').split('(')
                graph[vertice].append((neighbor, float(distance)))
    return graph

""" Caculate the straight-line distance between two cities
    Input: two cities that need to be calculated
    Return: float number - the straight-line distance between theese cities
"""
def calculateHaversineDistance(city1, city2):
    if city1 != city2:
        latDis = math.radians(city2['latitude'] - city1['latitude'])
        longDis = math.radians(city2['longitude'] - city1['longitude'])

        r = 3958.8

        d = 2 * r * math.asin(math.sqrt(math.sin(latDis / 2) ** 2 + math.cos(math.radians(city1['latitude'])) * math.cos(math.radians(city2['latitude'])) * math.sin(longDis / 2) ** 2))

        return d
    else:
        return 0

""" Node class is used to store information at each node in a graph """
class Node:
    def __init__(self, city, parent = None):
        self.city = city
        self.parent = parent
        # g is the actual cost
        self.g = 0
        # h is the heuristic value
        self.h = 0
        # f = g + h
        self.f = 0

    """ Override the equality operator """
    def __eq__(self, other):
        return self.city == other.city

    """ Override the hash function to allow nodes to be used in set """
    def __hash__(self):
        return hash(self.city['name'])

    """ Override the less-than operator to compare nodes based on their combined cost
        which is used in heappush function
    """
    def __lt__(self, other):
        return self.f < other.f

""" Implement the A* algorithm to find the best route between two cities
    Input: start city, destination, and the map
    Return: the path from the start city to the destination if there is one
"""
def AStarAlgorithm(start, goal, graph):
    # Create the start and goal city as 'Node' intances
    startCity = Node(start)
    endCity = Node(goal)

    # Stores a priority queue
    openSet = []
    # Stores explored nodes
    closedSet = set()

    heapq.heappush(openSet, startCity)

    # Loop until the queue is empty
    while openSet:
        # Get the node that has the lowest f value
        currentCity = heapq.heappop(openSet)

        # If the current node is the goal
        if currentCity.city == endCity.city:
            # Construct the path from the goal to the start city by traversing the parent node
            path = []
            current = currentCity
            while current is not None:
                path.append(current.city)
                current = current.parent
    
            return path[::-1]

        # If the current is already explored, then skip
        if currentCity in closedSet:
            continue
        # Or else mark it as explored
        closedSet.add(currentCity)

        # Add neighbors of the current node to the list
        for neighbor, distance in graph[currentCity.city['name']]:
            node = Node(cities[neighbor], parent = currentCity)
            
            node.g = currentCity.g + distance
            node.h = calculateHaversineDistance(node.city, endCity.city)
            node.f = node.g + node.h

            heapq.heappush(openSet, node)

    return None # No path is found between the start city to the goal

""" Caculate the total cost from start city to destination follow the selected path
    Input: selected path, and the map
    Return: float number - the total distance
"""
def calculateTotalDistance(path, graph):
    totalDistance = 0
    for i in range(len(path) - 1):
        currentCity = path[i]['name']
        nextCity = path[i + 1]['name']
        for neighbor, distance in graph[currentCity]:
            if neighbor == nextCity:
                totalDistance += distance
                break
    return totalDistance

if __name__ == "__main__":

    # Reading files
    cities = getCityCoordinates("coordinates.txt")
    graph = createMap("map.txt")

    # Getting input arguments
    departing = sys.argv[1]
    arriving = sys.argv[2]

    print("From city:", departing)
    print("To city:", arriving)

    # Check input values
    if departing not in cities or arriving not in cities:
        print("Invalid Input.")
    else:
        # Find a best route from the start city to the destination using A* algorithm
        bestRoute = AStarAlgorithm(cities[departing], cities[arriving], graph)

        # If there is a path from the start city to the destination
        if bestRoute:
            # Get the total cost from start city to destination follow the selected path
            totalDistance = calculateTotalDistance(bestRoute, graph)

            print("Best Route:", ' - '.join(city['name'] for city in bestRoute))
            print(f"Total distance: {totalDistance:.2f} mi")
        else: # If there is no path from the start city to the destination
            print("No route found.")
