import csv
import os


def print_menu():
    print("1. Agregar nuevo Pais")
    print("2. Actualizar Poblacion/Superficie de pais")
    print("3. Buscar pais")
    print("4. Filtrar paises")
    print("5. Ordenar paisese")
    print("6. Mostrar estadisticas")
    print("7. Salir del programa")


def get_countries_csv():
    columnas_requeridas = {
        "nombre",
        "continente",
        "poblacion",
        "superficie",
    }

    while True:

        usar_defecto = (
            input("¿Usar archivo por defecto 'paises.csv'? (S/n): ").strip().lower()
        )

        if usar_defecto != "n":
            nombre_archivo = "paises.csv"
        else:

            while True:
                nombre_archivo = input("Ingrese el nombre del archivo CSV: ").strip()

                if nombre_archivo.endswith(".csv") and len(nombre_archivo) > 4:
                    break

                print("Debe ingresar un nombre válido terminado en .csv")

        if not os.path.exists(nombre_archivo):

            with open(nombre_archivo, "w", newline="", encoding="utf-8") as archivo:
                escritor = csv.writer(archivo)
                escritor.writerow(["nombre", "continente", "poblacion", "superficie"])

            return {"paises": [], "archivo": archivo, "nombre_archivo": nombre_archivo}

        try:
            with open(nombre_archivo, "r", encoding="utf-8") as archivo:

                lector = csv.DictReader(archivo)

                if lector.fieldnames is None:

                    opcion = (
                        input(
                            "El archivo está vacío. ¿Desea utilizarlo igualmente? (S/n): "
                        )
                        .strip()
                        .lower()
                    )

                    if opcion != "n":
                        with open(
                            nombre_archivo, "w", newline="", encoding="utf-8"
                        ) as archivo:
                            escritor = csv.writer(archivo)
                            escritor.writerow(
                                ["nombre", "continente", "poblacion", "superficie"]
                            )

                    return {
                        "paises": [],
                        "archivo": archivo,
                        "nombre_archivo": nombre_archivo,
                    }

                columnas_actuales = set(lector.fieldnames)
                faltantes = columnas_requeridas - columnas_actuales

                if faltantes:
                    print(
                        "El archivo no posee las columnas:",
                        ", ".join(faltantes),
                    )
                    print("Seleccione otro archivo.")
                    continue

                paises = []

                for fila in lector:
                    try:
                        paises.append(
                            {
                                "nombre": fila["nombre"],
                                "continente": fila["continente"],
                                "poblacion": int(fila["poblacion"]),
                                "superficie": int(fila["superficie"]),
                            }
                        )

                    except ValueError:
                        print("Se ignoró una fila con datos numéricos inválidos.")

                return {
                    "paises": paises,
                    "archivo": archivo,
                    "nombre_archivo": nombre_archivo,
                }

        except PermissionError:
            print("No se tienen permisos para acceder al archivo.")

        except Exception as error:
            print(f"Error al leer el archivo: {error}")


def init():
    is_active = True
    print("Bienvenido al sistema de gestion de paises.")
    countries_csv = get_countries_csv()
    while is_active:
        print_menu()
        exit()


init()
