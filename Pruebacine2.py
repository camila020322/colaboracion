import tkinter as tk
from tkinter import messagebox

# Inicializar la disposición de asientos (10 filas x 8 columnas)
seating = {pelicula: {f"{row}{col}": "Disponible" for row in range(1, 11) for col in "ABCDEFGH"} for pelicula in ["Película 1", "Película 2", "Película 3", "Película 4"]}

# Lista de películas
peliculas = ["Película 1", "Película 2", "Película 3", "Película 4"]

# Variable global para la película seleccionada
pelicula_seleccionada = None
asientos_seleccionados = []  # Lista para almacenar los asientos seleccionados
costo_asiento = 12000  # Costo de cada asiento

def seleccionar_pelicula():
    def confirmar_seleccion():
        global pelicula_seleccionada
        seleccion = lista_peliculas.curselection()
        if seleccion:
            pelicula_seleccionada = peliculas[seleccion[0]]
            messagebox.showinfo("Película seleccionada", f"Has seleccionado: {pelicula_seleccionada}")
            ventana_peliculas.destroy()
            mostrar_asientos()
        else:
            messagebox.showerror("Error", "Por favor selecciona una película.")

    ventana_peliculas = tk.Toplevel(root)
    ventana_peliculas.title("Seleccionar Película")
    ventana_peliculas.geometry("1000x500")
    tk.Label(ventana_peliculas, text="Selecciona una película:", font=("Arial", 14)).pack(pady=10)
    lista_peliculas = tk.Listbox(ventana_peliculas, font=("Arial", 12), height=len(peliculas))
    for pelicula in peliculas:
        lista_peliculas.insert(tk.END, pelicula)
    lista_peliculas.pack(pady=10)
    tk.Button(ventana_peliculas, text="Confirmar", command=confirmar_seleccion).pack(pady=10)

def mostrar_asientos():
    def reservar_asiento(asiento):
        if asiento in asientos_seleccionados:
            asientos_seleccionados.remove(asiento)
            botones_asientos[asiento].config(relief=tk.RAISED)  # Cambiar el estilo del botón
        else:
            if seating[pelicula_seleccionada][asiento] == "Disponible":
                asientos_seleccionados.append(asiento)
                botones_asientos[asiento].config(relief=tk.SUNKEN)  # Cambiar el estilo del botón
            else:
                messagebox.showerror("Error", f"El asiento {asiento} ya está reservado.")

    def procesar_pago():
        if not asientos_seleccionados:
            messagebox.showwarning("Advertencia", "No has seleccionado ningún asiento.")
            return
        
        total_a_pagar = len(asientos_seleccionados) * costo_asiento  # Calcular el total a pagar
        metodo_pago = messagebox.askquestion("Método de Pago", f"Total a pagar: ${total_a_pagar}\n¿El pago es por tarjeta? (Sí para tarjeta, No para efectivo)")

        if metodo_pago == 'yes':  # Pago por tarjeta
            messagebox.showinfo("Esperando", "Esperando el procesamiento del pago...")
            root.after(5000, completar_reserva)  # Esperar 5 segundos antes de completar la reserva
        else:  # Pago en efectivo
            pagado = messagebox.askyesno("Pago en Efectivo", "¿El pago ha sido cancelado?")
            if pagado:
                completar_reserva()
            else:
                messagebox.showinfo("Pago no completado", "El pago no ha sido completado. Por favor, intenta nuevamente.")

    def completar_reserva():
        for asiento in asientos_seleccionados:
            seating[pelicula_seleccionada][asiento] = "Reservado"
            botones_asientos[asiento].config(text="🍿", state="disabled")
        messagebox.showinfo("Éxito", f"Has reservado los asientos: {', '.join(asientos_seleccionados)}")
        
        # Verificar si la sala está llena
        if all(seating[pelicula_seleccionada][asiento] == "Reservado" for asiento in seating[pelicula_seleccionada]):
            sala_llena()
        else:
            asientos_seleccionados.clear()  # Limpiar la lista de asientos seleccionados

    def sala_llena():
        messagebox.showinfo("Sala Llena", "La sala está llena. Todos los asientos han sido reservados.")
        # Reiniciar la sala después de 15 segundos
        root.after(15000, reiniciar_sala)

    def reiniciar_sala():
        for asiento in seating[pelicula_seleccionada]:
            seating[pelicula_seleccionada][asiento] = "Disponible"
            botones_asientos[asiento].config(text="⚪", state="normal")  # Reiniciar el botón
        messagebox.showinfo("Reinicio", "La sala ha sido reiniciada. Todos los asientos están disponibles nuevamente.")

    ventana_asientos = tk.Toplevel(root)
    ventana_asientos.title(f"Asientos - {pelicula_seleccionada}")
    ventana_asientos.geometry("900x700")
    tk.Label(ventana_asientos, text=f"Selecciona un asiento para {pelicula_seleccionada}", font=("Arial", 14)).pack(pady=10)

    frame_asientos = tk.Frame(ventana_asientos)
    frame_asientos.pack()

    global botones_asientos
    botones_asientos = {}
    for row in range(1, 11):
        fila = tk.Frame(frame_asientos)
        fila.pack()
        for col in "ABCDEFGH":
            asiento = f"{row}{col}"
            if seating[pelicula_seleccionada][asiento] == "Disponible":
                texto = "⚪"
            else:
                texto = "🍿"
            boton = tk.Button(fila, text=texto, width=4, height=2,
                              command=lambda a=asiento: reservar_asiento(a))
            boton.pack(side="left", padx=2, pady=2)
            botones_asientos[asiento] = boton

    # Botón para completar la reserva
    tk.Button(ventana_asientos, text="Completar Reserva", command=procesar_pago).pack(pady=20)

# Crear la ventana principal
root = tk.Tk()
root.title("Venta de Tickets de Cine")
root.geometry("1290x700")

# Botón para iniciar la selección de película
tk.Label(root, text="Bienvenido a la Venta de Tickets de Cine", font=("Arial", 16)).pack(pady=20)
tk.Button(root, text="Seleccionar Película", font=("Arial", 14), command=seleccionar_pelicula).pack(pady=20)

# Ejecutar la aplicación
root.mainloop()