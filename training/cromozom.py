from .neural_bird import NeuralBird
import random


def generate_random_int_range(max_range=1, min_range=0):
    return random.randint(min_range, max_range)


def select_parents(population: list, population_percent=0.5):
    parents_size = population_percent * len(population)
    return sorted(population, lambda x: x.fitness(), reverse=True)[:parents_size]


def generate_random_range(min_range=-1, max_range=1):
    return random.random() * (max_range - min_range) + min_range


def crossover(population: list, crossover_probability=0.9):
    children = []
    for mother in population:
        for father in population:
            child = Chromosome.reproduce(mother, father, crossover_probability)
            if child is not None:
                print("\nMother: {}".format(mother.to_str()))
                print("Father: {}".format(father.to_str()))
                print("Child: {}".format(child.to_str()))
                children.append(child)
    return children


class Chromosome:
    def __init__(self, bird: NeuralBird):
        self.bird = bird
        self.fitness = 0

    def mutate(self, mutation_probability=0.2):
        for index in range(len(self.bird.weights)):
            if random.random() < mutation_probability:
                self.bird.weights[index] = generate_random_range()

    @staticmethod
    def reproduce(father, mother, crossover_probability):
        if random.random() < crossover_probability:
            slice_index = generate_random_int_range(max_range=len(mother.weights) - 2,
                                                    min_range=1)
            weights = mother.weights[:slice_index]
            weights.extend(father.weights[slice_index:])
            return Chromosome(weights)
        return None

    def fitness(self):
        return self.fitness

    def to_dict(self):
        return {
            "score": self.fitness,
            "weights": self.bird.get_list_weights()
        }

    def to_str(self):
        return str(self.bird.weights)

    def __str__(self):
        return str(self.bird.weights)
