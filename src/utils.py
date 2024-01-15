import random
import numpy as np
from sympy import sympify, symbols


def find_bits_num(points_num):
    n = 1
    while not 2 ** (n - 1) < points_num <= 2**n:
        n += 1
    return n


def get_random_int(min, max):
    return random.randint(min, max)


def get_x(interval_min, i, delta_x):
    return interval_min + i * delta_x


def get_random_binary(num_bits):
    if num_bits <= 0:
        raise ValueError("The number of bits must be greater than zero")

    random_bits = np.random.choice([0, 1], size=num_bits)
    binary = "".join(map(str, random_bits))

    return binary


def convert_binary_to_int(binary):
    return int(binary, 2)


def solve_equation(expression, x_value):
    x = symbols("x")

    equation = sympify(expression)

    solution = equation.subs(x, x_value)

    return solution
