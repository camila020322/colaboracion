# Definimos el tamaño de la sala de cine
filas = 5
columnas = 5

# Creamos una matriz para representar los asientos
# 'O' representa un asiento disponible, 'X' representa un asiento reservado
sala_cine = [['O' for _ in range(columnas)] for _ in range(filas)]

def mostrar_sala(sala):
    print("Sala de Cine:")
    # Imprimir las letras de las columnas
    print("  " + " ".join(chr(i + 65) for i in range(columnas)))  # A, B, C, D, E
    for idx, fila in enumerate(sala):
        print(chr(idx + 65) + " " + " ".join(fila))  # Imprimir la letra de la fila (A, B, C, D, E)

def reservar_asiento(sala, fila, columna):
    if sala[fila][columna] == 'O':
        sala[fila][columna] = 'X'
        print(f"Asiento en fila {chr(fila + 65)}, columna {chr(columna + 65)} reservado con éxito.")
    else:
        print("Lo siento, ese asiento ya está reservado.")

def remover_asiento(sala, fila, columna):
    if sala[fila][columna] == 'X':
        sala[fila][columna] = 'O'
        print(f"Asiento en fila {chr(fila + 65)}, columna {chr(columna + 65)} ha sido liberado.")
    else:
        print("Lo siento, ese asiento no está reservado.")

def main():
    while True:
        mostrar_sala(sala_cine)  # Mostrar la sala al inicio de cada ciclo
        accion = input("¿Desea reservar (s) o remover (r) un asiento? (s/r): ").lower()
        
        if accion == 's':
            try:
                fila = int(input("Ingrese el número de fila (1-5) para reservar: ")) - 1
                columna = input("Seleccione la columna entre la A y la E para reservar: ").upper()
                
                # Convertir la letra de la columna a un índice numérico
                if columna in ['A', 'B', 'C', 'D', 'E']:
                    columna = ord(columna) - 65  # 'A' es 65 en ASCII
                else:
                    print("Por favor, ingrese una letra de columna válida (A-E).")
                    continue
                
                if 0 <= fila < filas and 0 <= columna < columnas:
                    reservar_asiento(sala_cine, fila, columna)
                else:
                    print("Por favor, ingrese un número de fila y columna válido.")
            except ValueError:
                print("Entrada no válida. Por favor, ingrese números enteros.")
        
        elif accion == 'r':
            try:
                fila = int(input("Ingrese el número de fila (1-5) para remover: ")) - 1
                columna = input("Seleccione la columna entre la A y la E para remover: ").upper()
                
                # Convertir la letra de la columna a un índice numérico
                if columna in ['A', 'B', 'C', 'D', 'E']:
                    columna = ord(columna) - 65  # 'A' es 65 en ASCII
                else:
                    print("Por favor, ingrese una letra de columna válida (A-E).")
                    continue
                
                if 0 <= fila < filas and 0 <= columna < columnas:
                    remover_asiento(sala_cine, fila, columna)
                else:
                    print("Por favor, ingrese un número de fila y columna válido.")
            except ValueError:
                print("Entrada no válida. Por favor, ingrese números enteros.")
        
        else:
            print("Opción no válida. Por favor, elija 'r' para reservar o 'm' para remover.")
        
        mostrar_sala(sala_cine)  # Mostrar la sala después de cada acción
        continuar = input("¿Desea realizar otra acción? (s/n): ").lower()
        if continuar != 's':
            break

if __name__ == "__main__":
    main()