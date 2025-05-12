import tkinter as tk
from tkinter import messagebox

class Pelicula:
    def __init__(self, titulo, duracion, clasificacion):
        self.titulo = titulo
        self.duracion = duracion
        self.clasificacion = clasificacion

class Sala:
    def __init__(self, numero):
        self.numero = numero
        self.asientos = [[True] * 5 for _ in range(5)]  # 5 filas y 5 columnas

    def reservar_asiento(self, fila, columna):
        if self.asientos[fila][columna]:
            self.asientos[fila][columna] = False
            return True
        return False

    def estado_asientos(self):
        return self.asientos

class Cine:
    def __init__(self):
        self.peliculas = []
        self.salas = []

    def agregar_pelicula(self, pelicula):
        self.peliculas.append(pelicula)

    def agregar_sala(self, sala):
        self.salas.append(sala)

class App:
    def __init__(self, root):
        self.cine = Cine()
        self.cine.agregar_pelicula(Pelicula("Avatar", 162, "PG-13"))
        self.cine.agregar_pelicula(Pelicula("Titanic", 195, "PG-13"))
        self.cine.agregar_sala(Sala(1))
        self.cine.agregar_sala(Sala(2))

        self.root = root
        self.root.title("Sistema de Venta de Tickets de Cine")

        self.pelicula_var = tk.StringVar()
        self.sala_var = tk.StringVar(value="1")
        self.fila_var = tk.StringVar()
        self.columna_var = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Seleccione una película:").pack()
        self.pelicula_menu = tk.OptionMenu(self.root, self.pelicula_var, *[p.titulo for p in self.cine.peliculas])
        self.pelicula_menu.pack()

        tk.Label(self.root, text="Seleccione una sala:").pack()
        self.sala_menu = tk.OptionMenu(self.root, self.sala_var, *[s.numero for s in self.cine.salas])
        self.sala_menu.pack()

        self.estado_frame = tk.Frame(self.root)
        self.estado_frame.pack()

        self.update_estado()

        tk.Label(self.root, text="Seleccione una fila (A-E):").pack()
        self.fila_entry = tk.Entry(self.root, textvariable=self.fila_var)
        self.fila_entry.pack()

        tk.Label(self.root, text="Seleccione una columna (1-5):").pack()
        self.columna_entry = tk.Entry(self.root, textvariable=self.columna_var)
        self.columna_entry.pack()

        self.reservar_button = tk.Button(self.root, text="Reservar Ticket", command=self.reservar_ticket)
        self.reservar_button.pack()

    def update_estado(self):
        for widget in self.estado_frame.winfo_children():
            widget.destroy()

        sala_index = int(self.sala_var.get()) - 1
        sala = self.cine.salas[sala_index]
        estado = sala.estado_asientos()

        for fila in range(5):
            for columna in range(5):
                estado_asiento = "Ocupado" if not estado[fila][columna] else "Disponible"
                color = "red" if not estado[fila][columna] else "green"
                btn = tk.Button(self.estado_frame, text=f"{chr(65 + fila)}{columna + 1}", bg=color, state="disabled")
                btn.grid(row=fila, column=columna)

        self.contador_asientos(sala)

    def contador_asientos(self, sala):
        ocupados = sum(not asiento for fila in sala.asientos for asiento in fila)
        disponibles = sala.capacidad - ocupados
        tk.Label(self.root, text=f"Asientos ocupados: {ocupados}").pack()
        tk.Label(self.root, text=f"Asientos disponibles: {disponibles}").pack()

    def reservar_ticket(self):
        fila = self.fila_var.get().upper()
        columna = self.columna_var.get()

        if not fila or not columna:
            messagebox.showerror("Error", "Por favor, complete todos los campos.")
            return

        fila_index = ord(fila) - 65