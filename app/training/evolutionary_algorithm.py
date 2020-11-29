from training.models.chromosome import Chromosome
from training.models.neural_bird import NeuralBird


def select_parents(population: list, population_percent=0.5):
    parents_size = int(population_percent * len(population))
    return sorted(population, reverse=True)[:parents_size]


def crossover(population: list, crossover_probability=0.9):
    children = []
    for mother in population:
        for father in population:
            child = Chromosome.reproduce(mother, father, crossover_probability)
            if child is not None:
                #print("\nMother: {}".format(mother.to_str()))
                #print("Father: {}".format(father.to_str()))
                #print("Child: {}".format(child.to_str()))
                children.append(child)
                if len(children) >= len(population):
                    #print("Generated new {} children".format(len(children)))
                    return children
    return children


def one_generation_evolution(population: list, crossover_probability, mutation_probability, finale_population_size, percentage_for_parenting):
    print("*******+One generation Evolution************")
    parents = select_parents(population, population_percent=percentage_for_parenting)

    children = crossover(parents, crossover_probability)

    for child in children:
        child.mutate(mutation_probability)

    population = parents.copy()
    population.extend(children)

    population = population[:finale_population_size]
    if len(population) < finale_population_size:
        for _ in range(finale_population_size - len(population)):
            population.append(Chromosome(NeuralBird()))
    print("New population size: {}".format(len(population)))
    return population


if __name__ == '__main__':
    population = [Chromosome(NeuralBird()) for _ in range(40)]

    print([str(individ) for individ in population])

    new_population = one_generation_evolution(population,
                                              crossover_probability=0.9,
                                              mutation_probability=0.2,
                                              finale_population_size=len(population),
                                              percentage_for_parenting=0.5)
    print([str(individ) for individ in new_population])

