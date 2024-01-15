import random
from sympy import symbols, sympify
import numpy as np

# Estos parametros dependerán del usuario
# equation = "sin(x)"  # se debe asegurar que la ecuación sea válida
# init_population_num = 4  # debe de ser un numero entero
# max_population_num = 10  # debe de ser un numero entero
# init_resolution = 0.05  # debe de ser un numero decimal, entre 0 y 1
# interval = [-10, 10]  # el primer digito debe de ser menor al segundo
# prob_crossover = 0.40  # debe de ser un numero decimal, entre 0 y 1
# prob_mutation = 0.75  # debe de ser un numero decimal, entre 0 y 1
# prob_mutation_per_gen = 0.51  # debe de ser un numero decimal, entre 0 y 1


# Utils
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


def calculate_values(binary, interval, equation, delta_x):
    i = convert_binary_to_int(binary)
    x = get_x(interval[0], i, delta_x)
    aptitude = solve_equation(equation, x)

    aptitude = float(f"{aptitude:.4f}")
    x = float(f"{x:.4f}")

    return {"binary": binary, "i": i, "x": x, "aptitude": aptitude}


def get_eligible_to_crossover(init_population, prob_crossover):
    eligible_to_crossover = []
    for individual in init_population:
        # TODO: Por cada individuo, se genera un numero aleatorio, si este es menor o igual al umbral de crossover, se agrega a la lista de elegibles
        if (get_random_int(0, 100) / 100) <= prob_crossover:
            eligible_to_crossover.append(individual)
    return eligible_to_crossover


def get_pairs_to_crossover(population):
    pairs = []
    for individual in population:
        # TODO: Teniendo los individuos a cruzar, se genera un numero aleatorio para seleccionar el segundo individuo, este numero sera el indice del individuo en la poblacion
        random_i = get_random_int(0, len(population) - 1)
        pairs.append((individual, population[random_i]))

    return pairs


def crossover(individual1, individual2):
    # Se obtiene el punto de cruce
    crossover_point = get_random_int(0, len(individual1["binary"]) - 1)

    # Se obtienen los numeros binarios de cada individuo
    individual1_binary = individual1["binary"]
    individual2_binary = individual2["binary"]

    # Se obtienen las partes de los numeros binarios de cada individuo
    individual1_binary_part1 = individual1_binary[:crossover_point]
    individual1_binary_part2 = individual1_binary[crossover_point:]
    individual2_binary_part1 = individual2_binary[:crossover_point]
    individual2_binary_part2 = individual2_binary[crossover_point:]

    # Se cruzan las partes de los numeros binarios de cada individuo
    individual1_binary = individual1_binary_part1 + individual2_binary_part2
    individual2_binary = individual2_binary_part1 + individual1_binary_part2

    return [individual1_binary, individual2_binary]


def mutate_gen(binary, prob_mutation_per_gen):
    mutation_mask = np.random.rand(len(binary)) <= prob_mutation_per_gen
    mutated_bits = np.logical_xor(
        np.array(list(map(int, binary))), mutation_mask
    ).astype(int)
    mutated_binary = "".join(map(str, mutated_bits))

    return mutated_binary


def get_statistics(population, is_using_min):
    # get best, worst and average
    best = population[0]
    worst = population[0]
    average = 0
    for individual in population:
        if is_using_min:
            if individual["aptitude"] < best["aptitude"]:
                best = individual
            if individual["aptitude"] > worst["aptitude"]:
                worst = individual
        else:
            if individual["aptitude"] > best["aptitude"]:
                best = individual
            if individual["aptitude"] < worst["aptitude"]:
                worst = individual

        average += individual["aptitude"]

    average = average / len(population)

    return {"best": best, "worst": worst, "average": average}


def deletion(population, best_individual, max_population_num):
    # Si hay individuos repetidos, DEBERÁN mantener sólo uno de estos en la población y enseguida si aplica, realizar la poda.
    # Remover los individuos repetidos
    temp_population = []
    for individual in population:
        if individual not in temp_population:
            temp_population.append(individual)

    # Implementa logica donde la eliminación sea aleatoria asegurando mantener al mejor individuo de la población.
    purged_population = []
    for individual in temp_population:
        if individual["aptitude"] == best_individual["aptitude"]:
            purged_population.append(individual)
            temp_population.remove(individual)
            break

    # Podar la población aleatoriamente
    while len(purged_population) < max_population_num and len(temp_population) > 0:
        random_i = get_random_int(0, len(temp_population) - 1)
        purged_population.append(temp_population[random_i])
        temp_population.remove(temp_population[random_i])

    return purged_population


def perform_genetic_algorithm(
    equation,
    init_population_num,
    max_population_num,
    init_resolution,
    interval,
    prob_crossover,
    prob_mutation,
    prob_mutation_per_gen,
    is_using_min,
    generations,
):
    # Calcular datos necesarios
    range_int = interval[1] - interval[0]
    points_num = int((range_int / init_resolution) + 1)

    bits_num = find_bits_num(points_num)
    delta_x = range_int / (2 ** (bits_num) - 1)

    # Generar población inicial de manera eficiente usando NumPy
    random_binaries = [get_random_binary(bits_num) for _ in range(init_population_num)]
    init_population = np.array([calculate_values(binary, interval, equation, delta_x) for binary in random_binaries])

    statistics_history = []
    prev_population = init_population

    for _ in range(generations):
        # Formacion de parejas
        selected_population = get_eligible_to_crossover(init_population, prob_crossover)
        pairs = get_pairs_to_crossover(selected_population)

        # Cruce y Mutación utilizando NumPy
        new_unmutated_population = np.array([crossover(pair[0], pair[1]) for pair in pairs]).flatten()
        mutation_mask = np.random.rand(len(new_unmutated_population)) <= prob_mutation
        new_unmutated_population = np.array([mutate_gen(ind, prob_mutation_per_gen) if should_mutate else ind for ind, should_mutate in zip(new_unmutated_population, mutation_mask)])

        new_population = np.array([calculate_values(ind, interval, equation, delta_x) for ind in new_unmutated_population])

        # Juntar poblaciones y recolección de estadísticas
        new_population = np.concatenate([prev_population, new_population])
        statistics = get_statistics(new_population, is_using_min)
        statistics_history.append(statistics)

        # Poda
        purged_population = deletion(new_population, statistics["best"], max_population_num)
        prev_population = purged_population

    return prev_population, statistics_history
