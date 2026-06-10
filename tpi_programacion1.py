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


def obtener_simple_string(label, error_label):
    while True:
        pais = input(label).strip().capitalize()
        if pais.isalpha():
            return pais
        print(error_label)


def es_pais_asignado(paises=None, nombre_pais=""):
    if paises is None:
        paises = []
    for pais in paises:
        if pais["nombre"] == nombre_pais:
            return True
    return False


def obtener_integer(label, error_label):
    while True:
        try:
            entero = int(input(label).strip())
            if entero >= 0:
                return entero

            print(error_label)
        except Exception as e:
            print("Ocurrio un error al obtener el numero: ", e)


def convertir_entero(valor):
    try:
        return int(valor)
    except ValueError:
        return 0


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

            return {"paises": [], "nombre_archivo": nombre_archivo}

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
                for index, fila in enumerate(lector):
                    nombre_fila = (
                        fila["nombre"]
                        if fila["nombre"]
                        else f"Sin asignar {index_error }"
                    )

                    continente = (
                        fila["continente"].strip()
                        if fila["continente"].strip()
                        else "Sin asignar"
                    )

                    poblacion = convertir_entero(fila["poblacion"])

                    superficie = convertir_entero(fila["superficie"])

                    paises.append(
                        {
                            "nombre": nombre_fila,
                            "continente": continente,
                            "poblacion": poblacion,
                            "superficie": superficie,
                        }
                    )

                return {
                    "paises": paises,
                    "nombre_archivo": nombre_archivo,
                }

        except PermissionError:
            print("No se tienen permisos para acceder al archivo.")

        except Exception as error:
            print(f"Error al leer el archivo: {error}")


def agregar_pais(paises, nombre_archivo):
    with open(nombre_archivo, "a", newline="", encoding="utf-8") as archivo:

        while True:
            pais = obtener_simple_string(
                label="Ingrese el nombre del pais: ",
                error_label="Ingrese un pais valido",
            )
            if not es_pais_asignado(paises=paises, nombre_pais=pais):
                break
            print("Pais ya se encuentra asignado, ingrese otro.")
        continente = obtener_simple_string(
            label="Ingrese el continente: ", error_label="Ingrese un continente valido"
        )

        superficie = obtener_integer(
            label="Ingrese la superficie: ",
            error_label="Ingrese un superficie valida, igual o mayor que 0",
        )
        poblacion = obtener_integer(
            label="Ingrese la pobracion: ",
            error_label="Ingrese un pobracion valida, igual o mayor que 0",
        )

        escritor = csv.DictWriter(
            archivo, fieldnames=["nombre", "continente", "poblacion", "superficie"]
        )
        escritor.writerow(
            {
                "nombre": pais,
                "continente": continente,
                "poblacion": poblacion,
                "superficie": superficie,
            }
        )
        paises.append(
            {
                "nombre": pais,
                "continente": continente,
                "poblacion": poblacion,
                "superficie": superficie,
            }
        )


def init():
    is_active = True
    print("Bienvenido al sistema de gestion de paises.")
    data = get_countries_csv()
    paises = data["paises"]
    nombre_archivo = data["nombre_archivo"]
    while is_active:
        print_menu()
        opcion = input("Opcion: ").strip()
        if opcion == "1":
            agregar_pais(paises, nombre_archivo)

        exit()


init()
