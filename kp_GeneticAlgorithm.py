# A Genetic Algorithm Approach to the Knapsack Problem

import random
import numpy as np
import matplotlib.pyplot as plt

class Knapsack(object):

    # initialize variables and lists
    def __init__(self):

        self.weights_limit = 20
        self.num_items = 6
        self.population_size = 30
        self.items = []
        self.pop = []
        self.pop_fitness = []
        self.average_fitness = []

    # create the initial data
    def generate_data(self):

        weights = random.sample(range(3, 10), self.num_items)
        values = random.sample(range(10, 30), self.num_items)
        
        for i in range (self.num_items):
            self.items.append([i, weights[i], values[i]])

        print("Initial data: ")
        print(self.items)


    #generate a single random solution
    def random_packing(self):
        weight = 0
        value = 0
        binary_code = []
        items = self.items.copy()
        for i in range(self.num_items):
            binary_code.append(0)
        
        while weight <= self.weights_limit:
            random_index = random.randint(0, (len(binary_code)-1))

            if binary_code[random_index] == 0:
                item = items[random_index]

                if (weight + item[1]) <= self.weights_limit:
                    binary_code[random_index] = 1
                    weight = weight + item[1]
                    value = value + item[2]   
                
                else:
                    break
           
        return binary_code


    # generate an initial population of size num
    def inital_population(self):
        for i in range(self.population_size):
            population_member = self.random_packing()
            fitness = self.fitness_function(population_member)
            self.pop.append(population_member)
            self.pop_fitness.append(fitness)



    # fitness function
    def fitness_function(self, population_member):
        weight = 0
        value = 0
        for num in range(len(population_member)):
            item = population_member[num]
            if item != 0:
                weight = weight + self.items[num][1]
                value = value + self.items[num][2]
        if weight > self.weights_limit:
            return 0
        else:
            return value

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
    def make_child(self):
        #generate parent indexes
        parent1_index = self.parent_roulette()
        parent2_index = self.parent_roulette()
        #generate parents
        parent1 = self.pop[parent1_index]
        parent2 = self.pop[parent2_index]

        
        crossover_point = random.randint(0, self.num_items)
        child = parent1[:crossover_point] + parent2[crossover_point:]
        self.mutate(child)

        return child


    # make a random mutation with a probability of 0.05
    def mutate(self, child):
        if random.random() < 0.05:
            mutated_index1 = random.randint(0, self.num_items)-1
            mutated_index2 = random.randint(0, self.num_items)-1
            
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



k = Knapsack()
k.generate_data()
k.genetic_algorithm(30)
