import random


def generate_random_int_range(max_range=1, min_range=0):
    return random.randint(min_range, max_range)


def generate_random_range(min_range=-1, max_range=1):
    return random.random() * (max_range - min_range) + min_range