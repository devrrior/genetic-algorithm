from tkinter import *
from tkinter import messagebox
from gentic_algorithm import perform_genetic_algorithm
import matplotlib.pyplot as plt
import numpy as np
import moviepy.editor as mpy
from natsort import natsorted


import os
import shutil
import numpy as np
import matplotlib.pyplot as plt
from tkinter import Tk, Frame, BOTH
from utils import solve_equation


def validate_probability(input_text):
    if input_text == "":
        return True  # Permite campo vacío
    try:
        value = float(input_text)
        if 0 <= value <= 1:
            return True

        messagebox.showerror("Error", "Por favor, ingrese un número entre 0 y 1.")
        return False

    except ValueError:
        messagebox.showerror("Error", "Por favor, ingrese un número válido.")
        return False


def validate_numbers(input_num):
    if input_num == "" or input_num == "-":
        return True  # Permite campo vacío
    try:
        float(input_num)
        return True
    except ValueError:
        messagebox.showerror("Error", "Por favor, ingrese un número válido.")
        return False


def validate_positive_int(input):
    if input == "":
        return True

    try:
        float(input)
        return True
    except ValueError:
        messagebox.showerror("Error", "Por favor, ingrese un número positivo válido.")
        return False


def show_main_window():
    def perform_algorithm():
        # Obtener los datos del form
        equation = equation_entry.get()
        init_resolution = float(init_resolution_entry.get())
        interval = [float(interval_min_entry.get()), float(interval_max_entry.get())]
        init_population_num = int(init_population_entry.get())
        max_population_num = int(max_population_entry.get())
        prob_crossover = float(prob_crossover_entry.get())
        prob_mutation = float(prob_mutation_entry.get())
        prob_mutation_per_gen = float(prob_mutation_per_gen_entry.get())
        is_using_minimum = technique_to_use.get() == "Minimo"
        generations = int(generations_entry.get())

        if equation == "":
            messagebox.showerror("Error", "Por favor, ingrese una ecuación.")
            return
        if interval[0] == "" or interval[1] == "":
            messagebox.showerror("Error", "Por favor, ingrese un intervalo.")
            return
        if init_population_num == "":
            messagebox.showerror("Error", "Por favor, ingrese una población inicial.")
            return
        if max_population_num == "":
            messagebox.showerror("Error", "Por favor, ingrese una población máxima.")
            return
        if init_resolution == "":
            messagebox.showerror("Error", "Por favor, ingrese una resolución inicial.")
            return
        if prob_crossover == "":
            messagebox.showerror(
                "Error", "Por favor, ingrese una probabilidad de crossover."
            )
            return
        if prob_mutation == "":
            messagebox.showerror(
                "Error", "Por favor, ingrese una probabilidad de mutación."
            )
            return
        if prob_mutation_per_gen == "":
            messagebox.showerror(
                "Error", "Por favor, ingrese una probabilidad de mutación por gen."
            )
            return
        if generations == "":
            messagebox.showerror(
                "Error", "Por favor, ingrese el número de generaciones."
            )
            return
        if interval[0] >= interval[1]:
            messagebox.showerror("Error", "Por favor, ingrese un intervalo válido.")
            return
        if init_population_num <= 0:
            messagebox.showerror(
                "Error", "Por favor, ingrese una población inicial válida."
            )
            return
        if max_population_num <= 0:
            messagebox.showerror(
                "Error", "Por favor, ingrese una población máxima válida."
            )
            return
        if init_resolution <= 0 or init_resolution >= 1:
            messagebox.showerror(
                "Error", "Por favor, ingrese una resolución inicial válida."
            )
            return
        if prob_crossover < 0 or prob_crossover > 1:
            messagebox.showerror(
                "Error", "Por favor, ingrese una probabilidad de crossover válida."
            )
            return
        if prob_mutation < 0 or prob_mutation > 1:
            messagebox.showerror(
                "Error", "Por favor, ingrese una probabilidad de mutación válida."
            )
            return
        if prob_mutation_per_gen < 0 or prob_mutation_per_gen > 1:
            messagebox.showerror(
                "Error",
                "Por favor, ingrese una probabilidad de mutación por gen válida.",
            )
            return

        # Ejecutar el algoritmo
        population_history, statistics_history = perform_genetic_algorithm(
            equation,
            init_population_num,
            max_population_num,
            init_resolution,
            interval,
            prob_crossover,
            prob_mutation,
            prob_mutation_per_gen,
            is_using_minimum,
            generations,
        )

        generations = np.arange(0, generations, 1)
        best = np.array([])
        worst = np.array([])
        average = np.array([])
        for i in range(len(statistics_history)):
            best = np.append(best, statistics_history[i]["best"]["aptitude"])
            worst = np.append(worst, statistics_history[i]["worst"]["aptitude"])
            average = np.append(average, statistics_history[i]["average"])

        stats_figure = plt.figure(1)
        plt.plot(generations, best, label="Mejor")
        plt.plot(generations, worst, label="Peor")
        plt.plot(generations, average, label="Promedio")
        plt.xlabel("Generaciones")
        plt.xlim(0, generations[-1])
        plt.ylabel("Aptitud")
        plt.title(f"Historial de datos estadisticos (Generaciones: {len(generations)})")
        plt.legend(loc="upper right")
        plt.grid()
        stats_figure.show()

        last_population = population_history[-1]
        best = last_population[0]
        worst = last_population[0]
        x = np.array([])
        y = np.array([])

        for individual in last_population:
            x = np.append(x, individual["x"])
            y = np.append(y, individual["aptitude"])
            if individual["aptitude"] < best["aptitude"] and is_using_minimum:
                best = individual
            elif individual["aptitude"] > best["aptitude"] and not is_using_minimum:
                best = individual

            if individual["aptitude"] > worst["aptitude"] and is_using_minimum:
                worst = individual
            elif individual["aptitude"] < worst["aptitude"] and not is_using_minimum:
                worst = individual

        last_population_figure = plt.figure(2)
        x_values = np.arange(interval[0], interval[1], 0.01)
        y_values = np.array([solve_equation(equation, x) for x in x_values])
        plt.plot(x_values, y_values, label="Funcion", color="#A0A0A0", zorder=1)
        plt.scatter(x, y, label="Poblacion", color="#0900FF", zorder=2)
        plt.plot(best["x"], best["aptitude"], "o", label="Mejor", color="#FF00FF", zorder=2)
        plt.plot(worst["x"], worst["aptitude"], "o", label="Peor", color="red", zorder=2)
        plt.xlabel("X")
        plt.ylabel("f(x)")
        plt.title(f"Ultima generacion (Generacion: {len(generations)})")
        plt.legend(loc="upper right")
        plt.xlim(interval[0], interval[1])
        plt.grid()
        last_population_figure.show()

        # Nueva ventana para decir cual fue el mejor, el peor y el promedio
        tmp_win2 = Tk()
        tmp_win2.title("Mejor, peor y promedio, de la última generación")
        tmp_win2.geometry("310x100")

        tmp_frame2 = Frame(tmp_win2)
        tmp_frame2.pack(fill=BOTH, expand=True)

        label_info = Label(
            tmp_frame2, text="Mejor, peor y promedio, de la última generación"
        )
        label_info.grid(row=0, column=0, sticky="w")

        label_best = Label(
            tmp_frame2, text=f"Mejor: {statistics_history[-1]['best']['aptitude']}"
        )
        label_best.grid(row=1, column=0, sticky="w")

        label_worst = Label(
            tmp_frame2, text=f"Peor: {statistics_history[-1]['worst']['aptitude']}"
        )
        label_worst.grid(row=2, column=0, sticky="w")

        label_average = Label(
            tmp_frame2, text=f"Promedio: {statistics_history[-1]['average']}"
        )
        label_average.grid(row=3, column=0, sticky="w")

        for child in tmp_frame2.winfo_children():
            child.grid_configure(padx=10, pady=5)

        # end: Nueva ventana para decir cual fue el mejor, el peor y el promedio

        # Crear carpeta temporal
        if os.path.exists("tmp"):
            shutil.rmtree("tmp")
        os.mkdir("tmp")

        # Generar las graficas
        x_values = np.arange(interval[0], interval[1], 0.01)
        y_values = np.array([solve_equation(equation, x) for x in x_values])

        for individual, i in zip(population_history, range(len(population_history))):
            x = np.array([])
            y = np.array([])
            best = individual[0]
            worst = individual[0]

            for individual in individual:
                x = np.append(x, individual["x"])
                y = np.append(y, individual["aptitude"])

                if individual["aptitude"] < best["aptitude"] and is_using_minimum:
                    best = individual
                elif individual["aptitude"] > best["aptitude"] and not is_using_minimum:
                    best = individual

                if individual["aptitude"] > worst["aptitude"] and is_using_minimum:
                    worst = individual
                elif individual["aptitude"] < worst["aptitude"] and not is_using_minimum:
                    worst = individual

            # Colocar los datos en la grafica
            plt.figure()

            plt.plot(x_values, y_values, label="Funcion", color="#A0A0A0", zorder=1)

            plt.scatter(x, y, label="Poblacion", color="#0900FF", zorder=2)
            plt.plot(best["x"], best["aptitude"], "o", label="Mejor", color="#FF00FF", zorder=2)
            plt.plot(worst["x"], worst["aptitude"], "o", label="Peor", color="red", zorder=2)
            plt.xlabel("X")
            plt.ylabel("f(x)")
            plt.title(f"Generacion {i}")
            plt.legend(loc="upper right")
            plt.xlim(interval[0], interval[1])
            plt.grid()

            # Guardar la grafica en la carpeta temporal
            plt.savefig(f"tmp/{i}.png")
            plt.close()

        # Generar video mp4 con las graficas

        # Obtener lista de imagenes, hacer un sort para que se ordenen
        images = natsorted(
            [os.path.join("tmp", fn) for fn in os.listdir("tmp") if fn.endswith(".png")]
        )

        clip = mpy.ImageSequenceClip(images, fps=1)

        # Guardar el video
        clip.write_videofile("evolution_gens.mp4")

        tmp_win2.mainloop()

    window = Tk()
    window.title("Algoritmo Genetico")
    window.geometry("550x700")
    window.resizable(False, False)

    frame = Frame(window)
    frame.pack(fill=BOTH, expand=True)

    # Datos generales
    validate_positive_int_cmd = window.register(validate_positive_int)
    validate_probability_cmd = window.register(validate_probability)
    validate_interval_cmd = window.register(validate_numbers)

    general_frame = LabelFrame(frame, text="Datos generales")
    general_frame.grid(row=0, column=0, padx=20, pady=10, sticky="ew")

    equation_label = Label(general_frame, text="Ecuacion")
    equation_label.grid(row=0, column=0, sticky="w")
    equation_entry = Entry(general_frame)
    equation_entry.grid(row=0, column=1)

    init_resolution_label = Label(general_frame, text="Resolucion inicial")
    init_resolution_label.grid(row=1, column=0, sticky="w")
    init_resolution_entry = Entry(
        general_frame, validate="key", validatecommand=(validate_probability_cmd, "%P")
    )
    init_resolution_entry.grid(row=1, column=1)

    generations_label = Label(general_frame, text="Generaciones")
    generations_label.grid(row=2, column=0, sticky="w")
    generations_entry = Entry(
        general_frame, validate="key", validatecommand=(validate_positive_int_cmd, "%P")
    )
    generations_entry.grid(row=2, column=1)

    technique_to_use_label = Label(general_frame, text="Técnica a usar")
    technique_to_use_label.grid(row=3, column=0, sticky="w")
    # 2 opciones: minimo o maximo
    technique_to_use = StringVar()
    technique_to_use.set("Minimo")
    technique_to_use_menu = OptionMenu(
        general_frame, technique_to_use, "Minimo", "Máximo"
    )
    technique_to_use_menu.grid(row=3, column=1)

    for child in general_frame.winfo_children():
        child.grid_configure(padx=10, pady=5)

    # Intervalos
    interval_frame = LabelFrame(frame, text="Intervalo")
    interval_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

    interval_min_label = Label(interval_frame, text="Minimo")
    interval_min_label.grid(row=0, column=0, sticky="w")
    interval_min_entry = Entry(
        interval_frame, validate="key", validatecommand=(validate_interval_cmd, "%P")
    )
    interval_min_entry.grid(row=0, column=1)

    interval_max_label = Label(interval_frame, text="Maximo")
    interval_max_label.grid(row=1, column=0, sticky="w")
    interval_max_entry = Entry(
        interval_frame, validate="key", validatecommand=(validate_interval_cmd, "%P")
    )
    interval_max_entry.grid(row=1, column=1)

    for child in interval_frame.winfo_children():
        child.grid_configure(padx=10, pady=5)

    # Datos de poblacion
    population_frame = LabelFrame(frame, text="Datos de población")
    population_frame.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

    init_population_label = Label(population_frame, text="Poblacion inicial")
    init_population_label.grid(row=0, column=0, sticky="w")
    init_population_entry = Entry(
        population_frame,
        validate="key",
        validatecommand=(validate_positive_int_cmd, "%P"),
    )
    init_population_entry.grid(row=0, column=1)

    max_population_label = Label(population_frame, text="Poblacion maxima")
    max_population_label.grid(row=1, column=0, sticky="w")
    max_population_entry = Entry(
        population_frame,
        validate="key",
        validatecommand=(validate_positive_int_cmd, "%P"),
    )
    max_population_entry.grid(row=1, column=1)

    for child in population_frame.winfo_children():
        child.grid_configure(padx=10, pady=5)

    # Probabilidades
    probabilities_frame = LabelFrame(frame, text="Probabilidades")
    probabilities_frame.grid(row=3, column=0, padx=20, pady=10, sticky="ew")

    prob_crossover_label = Label(probabilities_frame, text="Probabilidad de cruce")
    prob_crossover_label.grid(row=0, column=0, sticky="w")
    prob_crossover_entry = Entry(
        probabilities_frame,
        validate="key",
        validatecommand=(validate_probability_cmd, "%P"),
    )
    prob_crossover_entry.grid(row=0, column=1)

    prob_mutation_label = Label(
        probabilities_frame, text="Probabilidad de mutacion por individuo"
    )
    prob_mutation_label.grid(row=1, column=0, sticky="w")
    prob_mutation_entry = Entry(
        probabilities_frame,
        validate="key",
        validatecommand=(validate_probability_cmd, "%P"),
    )
    prob_mutation_entry.grid(row=1, column=1)

    prob_mutation_per_gen_label = Label(
        probabilities_frame, text="Probabilidad de mutacion por gen"
    )
    prob_mutation_per_gen_label.grid(row=2, column=0, sticky="w")
    prob_mutation_per_gen_entry = Entry(probabilities_frame)
    prob_mutation_per_gen_entry.grid(row=2, column=1)

    for child in probabilities_frame.winfo_children():
        child.grid_configure(padx=10, pady=5)

    # Colocar 2 botones en una misma linea
    buttons_frame = Frame(frame)
    buttons_frame.grid(row=4, column=0, padx=20, pady=10, sticky="ew")

    # Boton para iniciar el algoritmo
    execute_button = Button(buttons_frame, text="Ejecutar", command=perform_algorithm)
    execute_button.pack(side=RIGHT, padx=10)

    # Boton para mostrar la grafica
    exit_button = Button(buttons_frame, text="Salir", command=window.quit)
    exit_button.pack(side=LEFT, padx=10)

    window.columnconfigure(0, weight=1)

    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)

    window.mainloop()
