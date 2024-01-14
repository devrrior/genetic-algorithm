import random
from sympy import symbols, sympify

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

    binary = ""
    for _ in range(num_bits):
        random_bit = random.choice(["0", "1"])
        binary += random_bit

    return binary


def convert_binary_to_int(binary):
    integer_value = int(binary, 2)
    return integer_value


def solve_equation(expression, x_value):
    x = symbols("x")

    equation = sympify(expression)

    solution = equation.subs(x, x_value)

    return solution


def calculate_values(binary, interval, equation, delta_x):
    i = convert_binary_to_int(binary)
    x = get_x(interval[0], i, delta_x)
    aptitude = solve_equation(equation, x)

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
    for i in range(len(binary)):
        if (get_random_int(0, 100) / 100) <= prob_mutation_per_gen:
            # Negar el bit
            binary = binary[:i] + str(int(not int(binary[i]))) + binary[i + 1 :]

    return binary


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
    points_num = (range_int / init_resolution) + 1

    bits_num = find_bits_num(points_num)
    delta_x = range_int / (2 ** (bits_num) - 1)

    # Generar población inicial
    init_population = []
    statistics_history = []

    for _ in range(init_population_num):
        binary = get_random_binary(bits_num)
        new_individual = calculate_values(binary, interval, equation, delta_x)

        init_population.append(new_individual)

    statistics = get_statistics(init_population, is_using_min)
    statistics_history.append(statistics)
    prev_population = init_population

    for _ in range(generations):
        # Formacion de parejas
        selected_population = get_eligible_to_crossover(init_population, prob_crossover)
        pairs = get_pairs_to_crossover(selected_population)

        # Cruce
        new_unmutated_population = []
        for pair in pairs:
            new_individuals = crossover(pair[0], pair[1])

            new_unmutated_population.extend(new_individuals)

        # Mutacion
        new_mutated_population = []
        for i in range(len(new_unmutated_population)):
            # TODO: Por cada individuo, se genera un numero aleatorio, si este es menor o igual al umbral de mutacion, se muta
            if (get_random_int(0, 100) / 100) <= prob_mutation:
                new_unmutated_population[i] = mutate_gen(
                    new_unmutated_population[i], prob_mutation_per_gen
                )

            new_mutated_population.append(new_unmutated_population[i])

        new_population = []
        for individual in new_mutated_population:
            individual_with_data = calculate_values(
                individual, interval, equation, delta_x
            )
            new_population.append(individual_with_data)

        # Juntar poblaciones
        new_population.extend(prev_population)

        # Recoleccion de estadisticas
        statistics = get_statistics(new_population, is_using_min)
        statistics_history.append(statistics)

        # Poda
        purged_population = deletion(
            new_population, statistics["best"], max_population_num
        )

        prev_population = purged_population

    return prev_population, statistics_history
