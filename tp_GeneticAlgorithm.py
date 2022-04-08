# A Genetic Algorithm Approach to the Traveling Salesperson Problem

import random
from types import CoroutineType
import numpy as np
import math
import matplotlib.pyplot as plt

class TSP(object):

    # initialize variables and lists
    def __init__(self):

        self.population_size = 30
        self.pop = []
        self.pop_fitness = []
        self.average_fitness = []
        self.data = 0

    def add_data(self, data):
        self.data = data


    #start by making a random path for the initial solution

    def randomPath(self):
        number_of_cities = len(self.data)
        cities = list(range(1, number_of_cities))
        path = [0]

        for i in range(number_of_cities-1):
            random_index = random.randint(0, len(cities)-1)
            city = cities[random_index]
            path.append(city)
            cities.remove(city)

        return path


     # fitness function
    def fitness_function(self, population_member):
        length = 0
        for city_index in range(len(population_member)-1):
            city1 = population_member[city_index]
            city2 = population_member[city_index+1]
            length = length + self.data[city1][city2]
        return length

    # generate an initial population
    def inital_population(self):
        for i in range(self.population_size):
            population_member = self.randomPath()
            fitness = self.fitness_function(population_member)
            self.pop.append(population_member)
            self.pop_fitness.append(fitness)

    # roulette wheel selection - will find the index of parent from the parent population
    def parent_roulette(self):
        initial_pop_fitness = self.pop_fitness.copy()
        minimum = min(self.pop_fitness)
        roulette_wheel_scalings = [(element - minimum)**2 for element in initial_pop_fitness]
        roulette_wheel = np.cumsum(roulette_wheel_scalings)
        random_value = random.randint(0, max(roulette_wheel))
        parent_index = 0
        while random_value > roulette_wheel[parent_index]:
            parent_index = parent_index + 1

        
        return parent_index

    #cross over data from two parents
    # the method implemented can be found in the following paper  
    # https://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.875.5334&rep=rep1&type=pdf#:~:text=Genetic%20Algorithm%20which%20is%20a,is%20returned%20as%20the%20solution.
    def make_child(self):
        #generate parent indexes
        parent1_index = self.parent_roulette()
        parent2_index = self.parent_roulette()
        #generate parents
        parent1 = self.pop[parent1_index]
        parent2 = self.pop[parent2_index]

        city_start = parent1[0]
        city1 = parent1[1]
        city2 = parent2[1]

        length1 = self.data[city_start][city1]
        length2 = self.data[city_start][city2]

        if length1 > length2:
            child = parent2[:2] + parent1[2:]
            for item in child[2:]:
                if item == parent1[1]:
                    item = parent2[1]
        else:
            child = parent1[:2] + parent2[2:]
            for item in child[2:]:
                if item == parent2[1]:
                    item = parent1[1]

        self.mutate(child)

        return child

    # make a random mutation by swapping two cities with a probability of 0.05
    def mutate(self, child):
        if random.random() < 0.05:
            mutated_index1 = random.randint(0, len(child))-1
            mutated_index2 = random.randint(0, len(child))-1
            
            # swap over two random indexes 
            j = child[mutated_index1]
            i = child[mutated_index2]
            child[mutated_index1] = i
            child[mutated_index2] = j


    # create new generation
    def new_generation(self):
        counter = 0
        new_generation = []
        new_fitness = []
        while counter < self.population_size:
            child = self.make_child()
            if self.fitness_function(child) > 0:
                new_generation.append(child)
                new_fitness.append(self.fitness_function(child))
                counter = counter + 1
        
        self.pop = new_generation
        self.pop_fitness = new_fitness
        self.mean_fitness()

    # calcualte average fitness for a generation
    def mean_fitness(self):
        total = sum(self.pop_fitness)
        mean = total/self.population_size
        self.average_fitness.append(mean)



    #finally putting everything together
    def genetic_algorithm(self, gen_num):
        k.inital_population()
        for i in range(gen_num):
            k.new_generation()

        max_value = max(self.pop_fitness)
        max_index = self.pop_fitness.index(max_value)

        print("Final packing: " + str(self.pop[max_index]))
        print("Final value: " + str(max_value))
        self.print_graph(gen_num)

    
    # print out the average fitness of each generation on a graph
    def print_graph(self, gen_num):
        plt.plot(list(range(gen_num)), self.average_fitness, label = 'Mean Fitness')
        plt.title('Mean Fitness of Ppopulation per Generation')
        plt.xlabel('Generations')
        plt.ylabel('Fitness')
        plt.show()






data = [
            
[0,7,4,2,5,5,2,6,3,4,6,3,3,7,3,9,10,8,4,6,2,10,9,9,3,6,1,5,4,2,2,5,1,6,5,7,7,7,1,1,
4,6,7,5,9,8,10,6,4,2],
            
[7,0,7,8,5,1,3,2,3,5,6,5,9,6,10,7,10,3,7,3,7,7,1,3,3,7,9,4,8,7,1,7,4,10,1,5,5,5,8,4
,8,5,1,2,8,5,2,4,7,2],
            
[4,7,0,8,3,10,3,8,2,3,1,6,7,6,5,7,7,7,7,10,3,8,3,2,7,5,5,7,8,4,7,5,9,9,3,7,6,6,9,3,
4,2,10,7,5,7,6,7,6,8],
            
[2,8,8,0,6,10,3,2,2,1,5,5,4,8,7,8,10,10,2,2,7,1,6,6,9,5,4,7,8,6,4,2,6,3,1,8,3,5,7,4
,8,4,7,8,5,1,4,5,3,2],
            
[5,5,3,6,0,9,5,9,4,8,4,9,8,4,3,8,10,4,7,5,9,8,2,9,10,6,9,6,2,2,5,8,9,8,4,6,1,2,2,7,
5,2,5,2,1,9,6,10,7,6],
            
[5,1,10,10,9,0,9,9,10,1,9,7,10,6,5,9,3,5,10,6,9,8,6,3,7,1,7,7,8,9,10,8,6,10,6,1,2,9
,5,9,3,6,7,1,7,4,1,5,2,2],
            
[2,3,3,3,5,9,0,3,2,2,1,7,3,6,7,5,6,5,2,5,9,9,3,3,6,7,5,3,10,1,2,2,2,7,6,1,10,8,8,1,
9,10,10,9,8,6,2,4,2,1],
            
[6,2,8,2,9,9,3,0,10,4,3,4,5,7,1,9,6,9,4,5,1,2,7,4,9,2,10,6,8,10,3,5,5,8,9,2,2,4,1,6
,4,2,3,10,7,5,10,2,8,8],
            
[3,3,2,2,4,10,2,10,0,6,2,6,3,2,3,9,1,3,1,5,1,9,2,1,4,5,2,10,4,3,1,3,1,6,8,7,1,1,8,1,
0,6,2,9,4,3,8,1,1,7,7],
            
[4,5,3,1,8,1,2,4,6,0,6,8,8,8,3,7,6,4,1,8,4,7,8,2,2,6,5,9,8,8,1,1,1,8,10,7,2,8,2,2,7
,4,7,8,6,8,3,8,10,9],
            
[6,6,1,5,4,9,1,3,2,6,0,1,4,4,7,6,8,4,3,1,8,3,4,6,3,7,5,2,8,2,3,3,6,1,5,2,2,8,3,7,10
,5,7,8,5,7,2,10,2,3],
            
[3,5,6,5,9,7,7,4,6,8,1,0,8,5,8,4,3,1,7,5,5,7,1,4,8,7,2,2,1,1,5,7,8,6,2,7,2,2,1,2,2,
2,4,4,3,3,9,8,6,2],
            
[3,9,7,4,8,10,3,5,3,8,4,8,0,3,1,10,8,6,4,2,7,10,2,3,4,1,7,5,10,5,7,2,4,2,8,9,4,7,3,
6,9,6,4,3,5,5,4,6,8,5],
            
[7,6,6,8,4,6,6,7,2,8,4,5,3,0,5,2,1,3,4,7,10,10,5,3,8,8,8,8,2,7,5,3,1,9,2,2,7,9,6,8,
2,10,6,7,1,9,8,2,6,4],
            
[3,10,5,7,3,5,7,1,3,3,7,8,1,5,0,6,4,5,2,3,1,10,7,10,2,10,8,6,5,3,8,3,1,8,7,8,7,5,4,
9,4,9,8,9,6,7,10,5,1,9],
            
[9,7,7,8,8,9,5,9,9,7,6,4,10,2,6,0,7,4,10,3,7,7,4,2,1,5,2,8,4,9,8,6,2,10,3,10,3,4,1,
7,2,1,8,4,7,4,7,1,10,9],
            
[10,10,7,10,10,3,6,6,1,6,8,3,8,1,4,7,0,8,9,4,7,6,6,3,3,5,3,9,10,1,6,1,9,10,1,10,1,7
,8,6,9,9,7,2,3,2,1,2,7,10],
            
[8,3,7,10,4,5,5,9,3,4,4,1,6,3,5,4,8,0,4,5,10,10,7,10,8,4,7,3,3,7,6,5,7,8,6,6,6,6,1,
8,10,4,10,4,9,5,5,3,2,4],
            
[4,7,7,2,7,10,2,4,1,1,3,7,4,4,2,10,9,4,0,8,8,7,1,9,10,8,1,4,8,8,3,3,7,5,7,3,2,9,8,10,2,2,1,5,2,9,1,1,6,8],
            
[6,3,10,2,5,6,5,5,5,8,1,5,2,7,3,3,4,5,8,0,4,2,4,3,6,10,7,2,4,1,6,5,10,9,5,9,2,4,10,
10,8,7,4,10,2,8,7,9,4,8],
            
[2,7,3,7,9,9,9,1,1,4,8,5,7,10,1,7,7,10,8,4,0,9,4,6,10,6,4,7,4,8,5,5,7,10,4,9,8,10,1
,4,7,3,3,8,7,6,7,1,4,5],
            
[10,7,8,1,8,8,9,2,9,7,3,7,10,10,10,7,6,10,7,2,9,0,3,8,9,3,8,2,9,2,6,4,9,6,5,9,4,5,10,1,10,2,7,6,7,4,7,9,1,1],
            
[9,1,3,6,2,6,3,7,2,8,4,1,2,5,7,4,6,7,1,4,4,3,0,10,7,3,5,2,3,3,4,2,4,2,9,1,10,4,1,4,
8,8,6,7,9,1,4,1,2,8],
            
[9,3,2,6,9,3,3,4,1,2,6,4,3,3,10,2,3,10,9,3,6,8,10,0,8,9,6,1,10,9,3,6,10,8,9,5,5,6,3
,8,6,7,4,2,5,4,8,8,7,2],
            
[3,3,7,9,10,7,6,9,4,2,3,8,4,8,2,1,3,8,10,6,10,9,7,8,0,1,6,4,10,10,3,9,9,6,9,10,6,8,
6,1,5,7,6,4,10,9,9,4,6,9],
            
[6,7,5,5,6,1,7,2,5,6,7,7,1,8,10,5,5,4,8,10,6,3,3,9,1,0,10,7,3,7,1,5,7,10,9,5,8,5,10
,10,9,4,5,3,8,9,10,6,6,2],
            
[1,9,5,4,9,7,5,10,2,5,5,2,7,8,8,2,3,7,1,7,4,8,5,6,6,10,0,9,5,3,9,8,9,3,7,7,2,5,3,8,
3,9,9,4,5,7,9,7,6,4],
            
[5,4,7,7,6,7,3,6,10,9,2,2,5,8,6,8,9,3,4,2,7,2,2,1,4,7,9,0,5,8,9,8,1,7,5,5,2,9,4,3,4
,4,6,6,4,4,6,7,10,8],
            
[4,8,8,8,2,8,10,8,4,8,8,1,10,2,5,4,10,3,8,4,4,9,3,10,10,3,5,5,0,5,9,2,1,1,2,4,4,1,6
,1,2,7,9,10,6,10,6,6,4,5],
            
[2,7,4,6,2,9,1,10,3,8,2,1,5,7,3,9,1,7,8,1,8,2,3,9,10,7,3,8,5,0,5,1,9,1,5,9,4,7,9,9,
10,2,3,9,6,6,7,9,6,3],
            
[2,1,7,4,5,10,2,3,1,1,3,5,7,5,8,8,6,6,3,6,5,6,4,3,3,1,9,9,9,5,0,5,5,10,7,7,8,4,6,6,
2,6,7,5,9,8,4,5,4,8],
            
[5,7,5,2,8,8,2,5,3,1,3,7,2,3,3,6,1,5,3,5,5,4,2,6,9,5,8,8,2,1,5,0,8,5,7,10,8,8,2,4,6
,5,1,3,9,1,9,1,7,6],
            
[1,4,9,6,9,6,2,5,1,1,6,8,4,1,1,2,9,7,7,10,7,9,4,10,9,7,9,1,1,9,5,8,0,3,6,2,7,6,1,1,
2,1,5,9,7,6,9,1,10,2],
            
[6,10,9,3,8,10,7,8,6,8,1,6,2,9,8,10,10,8,5,9,10,6,2,8,6,10,3,7,1,1,10,5,3,0,6,2,6,1
,8,9,10,10,6,3,2,6,6,8,1,7],
            
[5,1,3,1,4,6,6,9,8,10,5,2,8,2,7,3,1,6,7,5,4,5,9,9,9,9,7,5,2,5,7,7,6,6,0,6,2,10,6,5,
10,7,5,9,6,6,7,4,3,6],
            
[7,5,7,8,6,1,1,2,7,7,2,7,9,2,8,10,10,6,3,9,9,9,1,5,10,5,7,5,4,9,7,10,2,2,6,0,9,5,2,
5,4,5,9,5,4,4,2,3,1,5],
            
[7,5,6,3,1,2,10,2,1,2,2,2,4,7,7,3,1,6,2,2,8,4,10,5,6,8,2,2,4,4,8,8,7,6,2,9,0,3,3,5,
2,5,8,3,8,1,4,1,3,1],
            
[7,5,6,5,2,9,8,4,1,8,8,2,7,9,5,4,7,6,9,4,10,5,4,6,8,5,5,9,1,7,4,8,6,1,10,5,3,0,2,2,
3,2,2,6,10,10,3,5,4,6],
            
[1,8,9,7,2,5,8,1,8,2,3,1,3,6,4,1,8,1,8,10,1,10,1,3,6,10,3,4,6,9,6,2,1,8,6,2,3,2,0,3
,1,5,2,1,10,5,10,8,1,7],
            
[1,4,3,4,7,9,1,6,10,2,7,2,6,8,9,7,6,8,10,10,4,1,4,8,1,10,8,3,1,9,6,4,1,9,5,5,5,2,3,
0,8,7,6,3,8,3,4,9,9,5],
            
[4,8,4,8,5,3,9,4,6,7,10,2,9,2,4,2,9,10,2,8,7,10,8,6,5,9,3,4,2,10,2,6,2,10,10,4,2,3,
1,8,0,4,7,10,10,6,4,9,5,10],
            
[6,5,2,4,2,6,10,2,2,4,5,2,6,10,9,1,9,4,2,7,3,2,8,7,7,4,9,4,7,2,6,5,1,10,7,5,5,2,5,7
,4,0,1,6,8,2,4,2,4,5],
            
[7,1,10,7,5,7,10,3,9,7,7,4,4,6,8,8,7,10,1,4,3,7,6,4,6,5,9,6,9,3,7,1,5,6,5,9,8,2,2,6
,7,1,0,6,1,6,3,3,3,2],
            
[5,2,7,8,2,1,9,10,4,8,8,4,3,7,9,4,2,4,5,10,8,6,7,2,4,3,4,6,10,9,5,3,9,3,9,5,3,6,1,3
,10,6,6,0,10,10,9,8,2,4],
            
[9,8,5,5,1,7,8,7,3,6,5,3,5,1,6,7,3,9,2,2,7,7,9,5,10,8,5,4,6,6,9,9,7,2,6,4,8,10,10,8
,10,8,1,10,0,2,1,4,7,7],
            
[8,5,7,1,9,4,6,5,8,8,7,3,5,9,7,4,2,5,9,8,6,4,1,4,9,9,7,4,10,6,8,1,6,6,6,4,1,10,5,3,
6,2,6,10,2,0,6,5,3,6],
            
[10,2,6,4,6,1,2,10,1,3,2,9,4,8,10,7,1,5,1,7,7,7,4,8,9,10,9,6,6,7,4,9,9,6,7,2,4,3,10
,4,4,4,3,9,1,6,0,8,8,6],
            
[6,4,7,5,10,5,4,2,1,8,10,8,6,2,5,1,2,3,1,9,1,9,1,8,4,6,7,7,6,9,5,1,1,8,4,3,1,5,8,9,
9,2,3,8,4,5,8,0,8,7],
            
[4,7,6,3,7,2,2,8,7,10,2,6,8,6,1,10,7,2,6,4,4,1,2,7,6,6,6,10,4,6,4,7,10,1,3,1,3,4,1,
9,5,4,3,2,7,3,8,8,0,2],
            
[2,2,8,2,6,2,1,8,7,9,3,2,5,4,9,9,10,4,8,8,5,1,8,2,9,2,4,8,5,3,8,6,2,7,6,5,1,6,7,5,10,5,2,4,7,6,6,7,2,0]    
        
       
]

k= TSP()
k.add_data(data)
k.genetic_algorithm(30)