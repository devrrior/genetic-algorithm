from tkinter import *
from tkinter import messagebox
from algo import perform_genetic_algorithm
import matplotlib.pyplot as plt
import numpy as np

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

# Crear interfaz para aplicar el algoritmo genetico
# Se necesitara los siguientes parametros en un form:
# Estos parametros dependerán del usuario
# equation = "sin(x)" # se debe asegurar que la ecuación sea válida
# init_population_num = 4 # debe de ser un numero entero
# max_population_num = 10 # debe de ser un numero entero
# init_resolution = 0.05 # debe de ser un numero decimal, entre 0 y 1
# interval = [-10, 10]  # el primer digito debe de ser menor al segundo
# prob_crossover = 0.40 # debe de ser un numero decimal, entre 0 y 1
# prob_mutation = 0.75 # debe de ser un numero decimal, entre 0 y 1
# prob_mutation_per_gen = 0.51 # debe de ser un numero decimal, entre 0 y 1
# is_using_minimum = True # booleano para saber si se quiere encontrar el minimo o el maximo


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

    # Validar que los datos sean correctos
    if equation == "":
        messagebox.showerror("Error", "Por favor, ingrese una ecuación.")
        return
    # Validar que los datos contienen valores
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
        messagebox.showerror("Error", "Por favor, ingrese el número de generaciones.")
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
        messagebox.showerror("Error", "Por favor, ingrese una población máxima válida.")
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
            "Error", "Por favor, ingrese una probabilidad de mutación por gen válida."
        )
        return

    # Ejecutar el algoritmo
    final_population, list_statistics = perform_genetic_algorithm(
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

    # Mostrar los resultados en una nueva ventana
    # messagebox.showinfo("Resultados", f"Resultados:\nMejor: {list_statistics["best"]}\n Peor: {list_statistics["worst"]}\n Promedio: {list_statistics["average"]}\n Poblacion final: {final_population}")

    # Crear ventana donde se mostrara una grafica del historial de los datos estadisticos
    tmp_win = Tk()
    tmp_win.title("Historial de datos estadisticos")
    tmp_win.geometry("550x700")
    tmp_win.resizable(False, False)

    tmp_frame = Frame(tmp_win)
    tmp_frame.pack(fill=BOTH, expand=True)

    # Crear grafica donde se muestre a traves de las generaciones el mejor, peor y promedio
    # Colocar la grafica en la ventana de tkinter

    # Crear grafica
    figure = Figure(figsize=(5, 5), dpi=100)
    plot = figure.add_subplot(111)
    plot.set_title(f"Historial de datos estadisticos (Generaciones: {generations})")
    plot.set_xlabel("Generaciones")
    plot.set_ylabel("Valores")
    plot.grid()

    # Obtener los datos de la grafica
    generations = []
    best = []
    worst = []
    average = []
    for i in range(len(list_statistics)):
        generations.append(i)
        best.append(list_statistics[i]["best"]["aptitude"])
        worst.append(list_statistics[i]["worst"]["aptitude"])
        average.append(list_statistics[i]["average"])

    plot.set_xticks(np.arange(0, generations[-1] + 1, 1))
    plot.set_yticks(np.arange(0, max(best) + 1, 1))

    # Colocar los datos en la grafica
    plot.plot(generations, best, label="Mejor")
    plot.plot(generations, worst, label="Peor")
    plot.plot(generations, average, label="Promedio")
    plot.legend()

    # Colocar la grafica en la ventana de tkinter
    canvas = FigureCanvasTkAgg(figure, tmp_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=True)

    print("Historial de datos estadisticos:")

    for i in range(len(list_statistics)):
        print(
            f"Generacion {i}: Mejor: {list_statistics[i]['best']['aptitude']}, Peor: {list_statistics[i]['worst']['aptitude']}, Promedio: {list_statistics[i]['average']}"
        )

    tmp_win.mainloop()


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

technique_to_use_label = Label(general_frame, text="Tecnica a usar")
technique_to_use_label.grid(row=3, column=0, sticky="w")
# 2 opciones: minimo o maximo
technique_to_use = StringVar()
technique_to_use.set("Minimo")
technique_to_use_menu = OptionMenu(general_frame, technique_to_use, "Minimo", "Maximo")
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
    population_frame, validate="key", validatecommand=(validate_positive_int_cmd, "%P")
)
init_population_entry.grid(row=0, column=1)

max_population_label = Label(population_frame, text="Poblacion maxima")
max_population_label.grid(row=1, column=0, sticky="w")
max_population_entry = Entry(
    population_frame, validate="key", validatecommand=(validate_positive_int_cmd, "%P")
)
max_population_entry.grid(row=1, column=1)

for child in population_frame.winfo_children():
    child.grid_configure(padx=10, pady=5)

# Probabilidades
probabilities_frame = LabelFrame(frame, text="Probabilidades")
probabilities_frame.grid(row=3, column=0, padx=20, pady=10, sticky="ew")

prob_crossover_label = Label(probabilities_frame, text="Probabilidad de crossover")
prob_crossover_label.grid(row=0, column=0, sticky="w")
prob_crossover_entry = Entry(
    probabilities_frame,
    validate="key",
    validatecommand=(validate_probability_cmd, "%P"),
)
prob_crossover_entry.grid(row=0, column=1)

prob_mutation_label = Label(probabilities_frame, text="Probabilidad de mutacion")
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