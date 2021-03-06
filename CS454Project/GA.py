import math
from numpy import random
from mutpy import commandline
from ExamplePrograms.unittest_generator import unittest_generator
import time
from collections.abc import Iterable

def fitness(sequence, fun_name):    
    unittest_generator('ExamplePrograms.' + fun_name, fun_name, sequence) # filename 수정
    mutation_score = commandline.main('ExamplePrograms.' + fun_name, 'test_calculator')
    return mutation_score

def softmax(lst):
    result = []
    sigma = sum(lst)
    for value in lst:
        result.append(value/sigma)
    return result

def fitnesses(population, best_value, fun_name, fitness_step):
    result = []
    for sequence in population:
        temp_value = fitness(sequence, fun_name)
        result.append(temp_value)
        if temp_value > best_value:
            best_value = temp_value
        fitness_step += 1
        if fitness_step % 100 == 0:
            print('fitness step = {}, best_value = {}'.format(fitness_step, best_value))
    return result, fitness_step

def mutation(parameter, mutation_rate):
    if isinstance(parameter, Iterable):
        result = []
        for i in parameter:
            result.append(mutation(i))
    else:
        if random.random() < mutation_rate:
            result = random.randint() #constraints
        else:
            result = parameter
    return result


def step(population, fitnesses_result, population_size, mutation_rate):
    numbers = len(population[0])
    input_size = len(population[0][0])
    indexes = list(range(0, len(population)))
    roulette = softmax(fitnesses_result)
    new_population = []
    for i in range(population_size):
        parents_index1, parents_index2 = random.choice(indexes, p=roulette), random.choice(indexes, p=roulette)
        parents_1, parents_2 = population[parents_index1], population[parents_index2]
        crossover = random.randint(0, numbers + 1)
        offspring = parents_1[:crossover] + parents_2[crossover:]
        offspring = mutation(offspring, mutation_rate)
        new_population.append(offspring)
    return new_population    

def ga(population, mutation_rate, fun_name, fitness_step):
    step = 0
    best_value = 0
    population_size = len(population)
    fitnesses_result, fitness_step = fitnesses(population, best_value, fun_name, fitness_step)
    best_index = fitnesses_result.index(max(fitnesses_result))
    best_value = fitnesses_result[best_index]
    best_input = population[best_index]
    if best_value >= 100:
        return best_input, best_value, fitness_step
    while step < 25:
        new_population = step(population, fitnesses_result, population_size, mutation_rate)
        fitnesses_result, fitness_step = fitnesses(population, best_value, fun_name, fitness_step)
        best_index = fitnesses_result.index(max(fitnesses_result))
        if fitnesses_result[best_index] > best_value:
            best_value = fitnesses_result[best_index]
            best_input = population[best_index]
        if best_value >= 100:
            return best_input, best_value, fitness_step
        step += 1 
    return best_input, best_value, fitness_step

def main(population, mutation_rate, fun_name):
    start = time.time()
    best_input, best_value, fitness_step = ga(population, mutation_rate, fun_name, 0)
    running_time = time.time() - start
    return best_input, best_value, fitness_step, running_time
