from training.models.chromosome import Chromosome
from training.models.neural_bird import NeuralBird
from utils import generate_random_int_range, generate_random_range


def test_generate_random_int_range():
    result = generate_random_int_range(min_range=0, max_range=100)
    assert (0 <= result < 100)


def test_generate_random_range():
    result = generate_random_range()
    assert (-1 <= result < 1)


def test_generate_chromosome():
    chromosome = Chromosome(NeuralBird())
    for weight in chromosome.bird.weights:
        assert (-1 <= weight < 1)


if __name__ == '__main__':
    for _ in range(100):
        test_generate_random_int_range()
        test_generate_random_range()
        test_generate_chromosome()
