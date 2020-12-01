from utils import generate_random_range, generate_random_int_range, read_dict_from_json
from .neural_bird import NeuralBird

import random


class Chromosome:
    def __init__(self, bird: NeuralBird, fitness=0, generations_alive=0, ancestor_generations=0):
        self.bird = bird
        self.fitness = fitness
        self.generations_alive = generations_alive
        self.ancestor_generations = ancestor_generations

    def mutate(self, mutation_probability=0.2):
        for index in range(len(self.bird.weights)):
            if random.random() < mutation_probability:
                self.bird.weights[index] = generate_random_range()

    @staticmethod
    def reproduce(father, mother, crossover_probability):
        if random.random() < crossover_probability:
            slice_index = generate_random_int_range(max_range=len(mother.bird.weights) - 2,
                                                    min_range=1)
            weights = mother.bird.weights[:slice_index]
            weights.extend(father.bird.weights[slice_index:])
            return Chromosome(NeuralBird(weights),
                              ancestor_generations=max(mother.ancestor_generations, father.ancestor_generations))
        return None

    def get_fitness(self):
        return self.fitness

    def to_dict(self):
        return {
            "score": self.fitness,
            "generations_alive": self.generations_alive,
            "ancestor_generations": self.ancestor_generations,
            "weights": self.bird.get_list_weights()
        }

    def complete_training(self, score):
        self.ancestor_generations += 1
        self.fitness = self.fitness * self.generations_alive + score
        self.generations_alive += 1
        self.fitness /= int(self.generations_alive)
        # self.fitness = max(self.fitness, score)

    def to_str(self):
        return str(self.bird.weights)

    def __str__(self):
        return str(self.bird.weights)

    def __lt__(self, other):
        return self.fitness < other.fitness

    @staticmethod
    def read_from_file(filename, population_size):
        data = read_dict_from_json(filename)
        if data is None:
            print("Json File {}: Error opening.".format(filename))
            return Chromosome.generate_new_random_population(population_size)
        population = [Chromosome(bird=NeuralBird(element["weights"]),
                                 fitness=element["score"],
                                 generations_alive=element["generations_alive"],
                                 ancestor_generations=element["ancestor_generations"])
                      for element in data]
        if len(population) < population_size:
            for _ in range(population_size - len(population)):
                population.append(Chromosome(NeuralBird()))
        if len(population) > population_size:
            population = population[:population_size]
        return population

    @staticmethod
    def generate_new_random_population(population_size):
        return [Chromosome(NeuralBird()) for _ in range(population_size)]
