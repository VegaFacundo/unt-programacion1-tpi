import csv
import os


def print_separador():
    print("-" * 40)


def print_menu():
    print("1. Agregar nuevo Pais")
    print("2. Actualizar Poblacion/Superficie de pais")
    print("3. Buscar pais")
    print("4. Filtrar paises")
    print("5. Ordenar paisese")
    print("6. Mostrar estadisticas")
    print("7. Salir del programa")


def obtener_simple_string(
    label, error_label, convert="capitalize", permitir_vacio=False
):
    while True:
        pais = input(label).strip()
        if convert == "capitalize":
            pais = pais.capitalize()
        if convert == "lower":
            pais = pais.lower()
        if pais.isalpha() or permitir_vacio:
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
            label="Ingrese la poblacion: ",
            error_label="Ingrese un poblacion valida, igual o mayor que 0",
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


def guardar_nuevo_paises(paises, nombre_archivo):
    with open(nombre_archivo, "w", newline="", encoding="utf-8") as archivo:
        escritor = csv.DictWriter(
            archivo, fieldnames=["nombre", "continente", "poblacion", "superficie"]
        )

        escritor.writeheader()
        escritor.writerows(paises)


def buscar_pais(paises):
    while True:
        pais_nombre = obtener_simple_string(
            label="Ingrese el nombre del pais: ",
            error_label="Ingrese un pais valido",
        )

        resultado = next(
            (pais for pais in paises if pais_nombre.lower() in pais["nombre"].lower()),
            None,
        )

        if not resultado:
            print("No se encontro un pais con el nombre: ", obtener_simple_string)
            opcion = obtener_simple_string(
                label="intentar de nuevo? Y/n: ",
                error_label="Ingrese una opcion valida",
                convert="lower",
            )
            if opcion == "n":
                break
            continue

        print(resultado)
        break


def modificar_pais(paises, nombre_archivo):
    es_pais = False
    while not es_pais:
        pais_nombre = obtener_simple_string(
            label="Ingrese el nombre del pais: ",
            error_label="Ingrese un pais valido",
        )
        resultado = next(
            (pais for pais in paises if pais_nombre.lower() in pais["nombre"].lower()),
            None,
        )

        if not resultado:
            print("No se encontro un pais con el nombre: ", obtener_simple_string)
            opcion = obtener_simple_string(
                label="intentar de nuevo? Y/n: ",
                error_label="Ingrese una opcion valida",
                convert="lower",
            )
            if opcion == "n":
                break
            continue

        print(resultado)

        pais_index = paises.index(
            resultado,
        )

        opcion_pais = obtener_simple_string(
            label=f"Usar el pais: {resultado["nombre"]}? Y/n ",
            error_label="Opcion invalida",
            convert="lower",
            permitir_vacio=True,
        )
        if opcion_pais == "n":
            continue
        es_pais = True

    es_editando = True
    while es_editando:
        opcion_editar = obtener_simple_string(
            label="editar poblacion(p) o superficie(x) o salir(s): ",
            error_label="Opcion invalida",
            convert="lower",
        )
        if opcion_editar == "p":

            poblacion = obtener_integer(
                label="Ingrese la poblacion: ",
                error_label="Ingrese un poblacion valida, igual o mayor que 0",
            )
            paises[pais_index]["poblacion"] = poblacion
            guardar_nuevo_paises(paises, nombre_archivo)
            continue
        elif opcion_editar == "x":
            superficie = obtener_integer(
                label="Ingrese la superficie: ",
                error_label="Ingrese un superficie valida, igual o mayor que 0",
            )
            paises[pais_index]["superficie"] = superficie
            guardar_nuevo_paises(paises, nombre_archivo)
            continue
        elif opcion_editar == "s":
            print("Volviendo al menu...")
            es_editando = False
            continue
        else:
            print("Opcion invalida")


def mostrar_paises(paises):
    for pais in paises:
        print(pais)


def filtrar_paises(paises, nombre_archivo):
    filtrar_opcion = obtener_simple_string(
        label="Filtrar países por Continente(c), Población(p), Superficie(s): ",
        error_label="Opción incorrecta",
        convert="lower",
    )

    paises_filtrados = []

    if filtrar_opcion == "c":
        continentes = {pais["continente"] for pais in paises}
        print("Continentes disponibles:")
        for continente in continentes:
            print("-", continente)
        continente = obtener_simple_string(
            label="Ingrese el continente: ",
            error_label="Continente inválido",
        )

        paises_filtrados = [
            pais for pais in paises if continente.lower() in pais["continente"].lower()
        ]

    elif filtrar_opcion == "p":
        minimo = obtener_integer(
            label="Población mínima: ",
            error_label="Valor inválido",
        )

        maximo = obtener_integer(
            label="Población máxima: ",
            error_label="Valor inválido",
        )

        paises_filtrados = [
            pais for pais in paises if minimo <= pais["poblacion"] <= maximo
        ]

    elif filtrar_opcion == "s":
        minimo = obtener_integer(
            label="Superficie mínima: ",
            error_label="Valor inválido",
        )

        maximo = obtener_integer(
            label="Superficie máxima: ",
            error_label="Valor inválido",
        )

        paises_filtrados = [
            pais for pais in paises if minimo <= pais["superficie"] <= maximo
        ]

    else:
        print("Opción inválida.")
        return

    if len(paises_filtrados) == 0:
        print("No se encontraron países.")
    else:
        for pais in paises_filtrados:
            print(pais)


def ordenar_paises(paises, nombre_archivo):
    ordenar_opcion = obtener_simple_string(
        label="Ordenar países por Nombre(n), Población(p), Superficie(s): ",
        error_label="Opción incorrecta",
        convert="lower",
    )

    if ordenar_opcion == "n":
        paises.sort(key=lambda pais: pais["nombre"].lower())

    elif ordenar_opcion == "p":
        paises.sort(key=lambda pais: pais["poblacion"])

    elif ordenar_opcion == "s":
        paises.sort(key=lambda pais: pais["superficie"])

    else:
        print("Opción inválida.")
        return

    guardar_nuevo_paises(paises, nombre_archivo)
    print("Países ordenados y archivo actualizado.")


def mostrar_stadisticas(paises):
    print("Calculando estadisticas...")
    if len(paises) < 1:
        print("Paises insuficiente para calcular estadisticas")

    pais_mayor_poblacion = paises[0]
    pais_menor_poblacion = paises[0]
    prom_poblacion = 0
    poblacion_cantidad = 0
    prom_superficie = 0
    superficie_cantidad = 0
    paises_por_continente = {}

    for pais in paises:
        if pais["poblacion"] > pais_mayor_poblacion["poblacion"]:
            pais_mayor_poblacion = pais

        if pais["poblacion"] < pais_menor_poblacion["poblacion"]:
            pais_menor_poblacion = pais

        if pais["poblacion"] > 0:
            poblacion_cantidad = poblacion_cantidad + 1
            prom_poblacion = prom_poblacion + pais["poblacion"]

        if pais["superficie"] > 0:
            superficie_cantidad = superficie_cantidad + 1
            prom_superficie = prom_poblacion + pais["superficie"]

        paises_por_continente[pais["continente"]] = (
            paises_por_continente.get(pais["continente"], 0) + 1
        )

    if poblacion_cantidad > 0:
        prom_poblacion /= poblacion_cantidad

    if superficie_cantidad > 0:
        prom_superficie /= superficie_cantidad

    print("Pais con Mayor poblacion: ")
    print(pais_mayor_poblacion)
    print("---")

    print("Pais con Menor poblacion: ")
    print(pais_menor_poblacion)
    print("---")

    print("Promedio de poblacion: ")
    print(prom_poblacion)
    print("---")

    print("Promedio de supervicion: ")
    print(prom_superficie)
    print("---")

    print("Paises por continente: ")
    for continente, cantidad in paises_por_continente.items():
        print(f"{continente}: {cantidad}")
    print("---")


def init():
    is_active = True
    print("Bienvenido al sistema de gestion de paises.")
    data = get_countries_csv()
    paises = data["paises"]
    nombre_archivo = data["nombre_archivo"]
    while is_active:
        print_menu()
        print_separador()
        opcion = input("Opcion: ").strip()
        if opcion == "1":
            agregar_pais(paises, nombre_archivo)
        elif opcion == "2":
            modificar_pais(paises, nombre_archivo)
        elif opcion == "3":
            buscar_pais(paises)
        elif opcion == "4":
            filtrar_paises(paises, nombre_archivo)
        elif opcion == "5":
            ordenar_paises(paises, nombre_archivo)
        elif opcion == "6":
            mostrar_stadisticas(paises)
        elif opcion == "7":
            is_active = False
            print("saliendo del programa. Adios!")
        elif opcion == "x":
            mostrar_paises(
                paises,
            )
        else:
            print("Opcion invalida")
        print_separador()


if __name__ == "__main__":
    try:
        init()
    except KeyboardInterrupt:
        print("\nPrograma cancelado por el usuario. Adios!")
    except Exception as e:
        print(f"Ocurrió un error: {e}")
        print("Adios!")
