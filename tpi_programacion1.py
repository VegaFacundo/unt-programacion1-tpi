# Importar módulos necesarios
import csv  # Para leer y escribir archivos CSV
import os   # Para verificar la existencia de archivos


# Función puramente estética para imprimir un país formateado
def imprimir_pais_bonito(pais):
    print(f"  ┌{'─'*30}┐")
    print(f"  │ País:       {pais['nombre']}")
    print(f"  │ Continente: {pais['continente']}")
    print(f"  │ Población:  {pais['poblacion']:,}")
    print(f"  │ Superficie: {pais['superficie']:,} km²")
    print(f"  └{'─'*30}┘")


# Función que imprime una línea separadora para mejorar la legibilidad del menú
def print_separador():
    print(f"┠{'─' * 45}┨")


# Función que muestra el menú principal de opciones disponibles
def print_menu():
    print(f"\n┏{'━' * 45}┓")
    print(f"┃{'SISTEMA DE GESTIÓN DE PAÍSES'.center(45)}┃")
    print(f"┣{'━' * 45}┫")
    print(f"┃{'  [1]  Agregar nuevo País'.ljust(45)}┃")
    print(f"┃{'  [2]  Actualizar Población/Superficie'.ljust(45)}┃")
    print(f"┃{'  [3]  Buscar país'.ljust(45)}┃")
    print(f"┃{'  [4]  Filtrar países'.ljust(45)}┃")
    print(f"┃{'  [5]  Ordenar países'.ljust(45)}┃")
    print(f"┃{'  [6]  Mostrar estadísticas'.ljust(45)}┃")
    print(f"┃{'  [7]  Salir del programa'.ljust(45)}┃")


# Función que obtiene una cadena de texto del usuario con validación
def obtener_simple_string(
    label, error_label, convert="capitalize", permitir_vacio=False
):
    while True:
        pais = input(f"> {label}").strip()
        if convert == "capitalize":
            pais = pais.capitalize()
        if convert == "lower":
            pais = pais.lower()
        if pais.replace(" ", "").isalpha() or permitir_vacio:
            return pais
        print(f"[Error] {error_label}")


# Función que verifica si un país ya existe en la lista
def es_pais_asignado(paises=None, nombre_pais=""):
    if paises is None:
        paises = []
    for pais in paises:
        if pais["nombre"] == nombre_pais:
            return True
    return False


# Función que obtiene un número entero del usuario con validación
def obtener_integer(label, error_label):
    while True:
        try:
            entero = int(input(f"> {label}").strip())
            if entero >= 0:
                return entero

            print(f"[Error] {error_label}")
        except Exception as e:
            print(f"[Error] Ocurrió un error al obtener el número: {e}")


# Función auxiliar que convierte una cadena a entero, retorna 0 si falla
def convertir_entero(valor):
    try:
        return int(valor)
    except ValueError:
        return 0


# Función que carga los países desde un archivo CSV
def get_countries_csv():
    columnas_requeridas = {
        "nombre",
        "continente",
        "poblacion",
        "superficie",
    }
    
    print(f"\n╭{'─'*40}╮")
    print(f"│{'CONFIGURACIÓN DE ARCHIVO INICIAL'.center(40)}│")
    print(f"╰{'─'*40}╯")

    while True:
        usar_defecto = (
            input("> ¿Usar archivo por defecto 'paises.csv'? (S/n): ").strip().lower()
        )

        if usar_defecto != "n":
            nombre_archivo = "paises.csv"
        else:
            while True:
                nombre_archivo = input("> Ingrese el nombre del archivo CSV: ").strip()

                if nombre_archivo.endswith(".csv") and len(nombre_archivo) > 4:
                    break
                print("[Error] Debe ingresar un nombre válido terminado en .csv")

        if not os.path.exists(nombre_archivo):
            print(f"[Info] Creando nuevo archivo: {nombre_archivo}...")
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
                            "[Advertencia] El archivo está vacío. ¿Desea utilizarlo igualmente? (S/n): "
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
                    print(f"[Error] El archivo no posee las columnas: {', '.join(faltantes)}")
                    print("Seleccione otro archivo.")
                    continue

                paises = []
                for index, fila in enumerate(lector):
                    nombre_fila = (
                        fila["nombre"]
                        if fila["nombre"]
                        else f"Sin asignar {index}"
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
                print(f"[Éxito] Archivo cargado exitosamente ({len(paises)} países).")
                return {
                    "paises": paises,
                    "nombre_archivo": nombre_archivo,
                }

        except PermissionError:
            print("[Error] No se tienen permisos para acceder al archivo.")

        except Exception as error:
            print(f"[Error] Error al leer el archivo: {error}")


# Función que agrega un nuevo país al archivo CSV
def agregar_pais(paises, nombre_archivo):
    print("\n=== AGREGAR NUEVO PAÍS ===")
    with open(nombre_archivo, "a", newline="", encoding="utf-8") as archivo:
        while True:
            pais = obtener_simple_string(
                label="Ingrese el nombre del país: ",
                error_label="Ingrese un país válido",
            )
            if not es_pais_asignado(paises=paises, nombre_pais=pais):
                break
            print("[Advertencia] El país ya se encuentra asignado, ingrese otro.")
            
        continente = obtener_simple_string(
            label="Ingrese el continente: ", error_label="Ingrese un continente válido"
        )
        superficie = obtener_integer(
            label="Ingrese la superficie (km²): ",
            error_label="Ingrese una superficie válida, igual o mayor que 0",
        )
        poblacion = obtener_integer(
            label="Ingrese la población: ",
            error_label="Ingrese una población válida, igual o mayor que 0",
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
        print(f"\n[Éxito] ¡País '{pais}' agregado correctamente!")


# Función que guarda todos los países en el archivo CSV
def guardar_nuevo_paises(paises, nombre_archivo):
    with open(nombre_archivo, "w", newline="", encoding="utf-8") as archivo:
        escritor = csv.DictWriter(
            archivo, fieldnames=["nombre", "continente", "poblacion", "superficie"]
        )
        escritor.writeheader()
        escritor.writerows(paises)


# Función que busca un país por nombre en la lista
def buscar_pais(paises):
    print("\n=== BUSCAR PAÍS ===")
    while True:
        pais_nombre = obtener_simple_string(
            label="Ingrese el nombre del país a buscar: ",
            error_label="Ingrese un país válido",
        )

        resultado = next(
            (pais for pais in paises if pais_nombre.lower() in pais["nombre"].lower()),
            None,
        )

        if not resultado:
            print(f"[Error] No se encontró un país con el nombre: {pais_nombre}")
            opcion = obtener_simple_string(
                label="¿Intentar de nuevo? (Y/n): ",
                error_label="Ingrese una opción válida",
                convert="lower",
            )
            if opcion == "n":
                break
            continue

        print("\n[Éxito] ¡País Encontrado!")
        imprimir_pais_bonito(resultado)
        break


# Función que permite modificar la población o superficie de un país
def modificar_pais(paises, nombre_archivo):
    print("\n=== ACTUALIZAR PAÍS ===")
    es_pais = False
    while not es_pais:
        pais_nombre = obtener_simple_string(
            label="Ingrese el nombre del país a modificar: ",
            error_label="Ingrese un país válido",
        )
        resultado = next(
            (pais for pais in paises if pais_nombre.lower() in pais["nombre"].lower()),
            None,
        )

        if not resultado:
            print(f"[Error] No se encontró un país con el nombre: {pais_nombre}")
            opcion = obtener_simple_string(
                label="¿Intentar de nuevo? (Y/n): ",
                error_label="Ingrese una opción válida",
                convert="lower",
            )
            if opcion == "n":
                break
            continue

        imprimir_pais_bonito(resultado)

        pais_index = paises.index(resultado)

        opcion_pais = obtener_simple_string(
            label=f"¿Modificar datos de {resultado['nombre']}? (Y/n): ",
            error_label="Opción inválida",
            convert="lower",
            permitir_vacio=True,
        )
        if opcion_pais == "n":
            continue
        es_pais = True

    es_editando = True
    while es_editando:
        print("\nOpciones de edición:")
        print("  [p] Población")
        print("  [x] Superficie")
        print("  [s] Salir al menú")
        opcion_editar = obtener_simple_string(
            label="Elija una opción (p/x/s): ",
            error_label="Opción inválida",
            convert="lower",
        )
        if opcion_editar == "p":
            poblacion = obtener_integer(
                label="Ingrese la nueva población: ",
                error_label="Ingrese una población válida, igual o mayor que 0",
            )
            paises[pais_index]["poblacion"] = poblacion
            guardar_nuevo_paises(paises, nombre_archivo)
            print("[Éxito] Población actualizada.")
            continue
        elif opcion_editar == "x":
            superficie = obtener_integer(
                label="Ingrese la nueva superficie: ",
                error_label="Ingrese una superficie válida, igual o mayor que 0",
            )
            paises[pais_index]["superficie"] = superficie
            guardar_nuevo_paises(paises, nombre_archivo)
            print("[Éxito] Superficie actualizada.")
            continue
        elif opcion_editar == "s":
            print("Volviendo al menú principal...")
            es_editando = False
            continue
        else:
            print("[Error] Opción inválida")


# Función simple que imprime todos los países en la lista
def mostrar_paises(paises):
    print("\n=== LISTADO DE TODOS LOS PAÍSES ===")
    for pais in paises:
        imprimir_pais_bonito(pais)


# Función que filtra países según criterios
def filtrar_paises(paises, nombre_archivo):
    print("\n=== FILTRAR PAÍSES ===")
    print("  [c] Continente")
    print("  [p] Población")
    print("  [s] Superficie")
    
    filtrar_opcion = obtener_simple_string(
        label="Elija un criterio (c/p/s): ",
        error_label="Opción incorrecta",
        convert="lower",
    )

    paises_filtrados = []

    if filtrar_opcion == "c":
        continentes = {pais["continente"] for pais in paises}
        print("\nContinentes disponibles:")
        for continente in continentes:
            print(f"  - {continente}")
        
        continente = obtener_simple_string(
            label="Ingrese el continente a filtrar: ",
            error_label="Continente inválido",
        )
        paises_filtrados = [
            pais for pais in paises if continente.lower() in pais["continente"].lower()
        ]

    elif filtrar_opcion == "p":
        minimo = obtener_integer(label="Población mínima: ", error_label="Valor inválido")
        maximo = obtener_integer(label="Población máxima: ", error_label="Valor inválido")
        paises_filtrados = [pais for pais in paises if minimo <= pais["poblacion"] <= maximo]

    elif filtrar_opcion == "s":
        minimo = obtener_integer(label="Superficie mínima: ", error_label="Valor inválido")
        maximo = obtener_integer(label="Superficie máxima: ", error_label="Valor inválido")
        paises_filtrados = [pais for pais in paises if minimo <= pais["superficie"] <= maximo]

    else:
        print("[Error] Opción inválida.")
        return

    if len(paises_filtrados) == 0:
        print("\n[Advertencia] No se encontraron países con esos criterios.")
    else:
        print(f"\n[Info] Se encontraron {len(paises_filtrados)} países:")
        for pais in paises_filtrados:
            imprimir_pais_bonito(pais)


# Función que ordena la lista de países por criterio
def ordenar_paises(paises, nombre_archivo):
    print("\n=== ORDENAR PAÍSES ===")
    print("  [n] Nombre")
    print("  [p] Población")
    print("  [s] Superficie")
    
    ordenar_opcion = obtener_simple_string(
        label="Elija un criterio de orden (n/p/s): ",
        error_label="Opción incorrecta",
        convert="lower",
    )

    if ordenar_opcion == "n":
        paises.sort(key=lambda pais: pais["nombre"].lower())
    elif ordenar_opcion == "p":
        paises.sort(key=lambda pais: pais["poblacion"])
    elif ordenar_opcion == "s":
        print("\n=== ¿Ascendente o descendente? ===")
        print("  [A] Ascendente")
        print("  [D] Descendente")

        direccion = obtener_simple_string(
            label="Elija una dirección (A/D): ",
            error_label="Opción incorrecta",
            convert="lower",
        )

        if direccion == "a":
            paises.sort(key=lambda pais: pais["superficie"])
        elif direccion == "d":
            paises.sort(key=lambda pais: pais["superficie"], reverse=True)
        else:
            print("[Error] Opción inválida.")
    else:
        print("[Error] Opción inválida.")
        return

    guardar_nuevo_paises(paises, nombre_archivo)
    print("\n[Éxito] Países ordenados y archivo actualizado.")


# Función que calcula y muestra estadísticas de los países
def mostrar_stadisticas(paises):
    print("\n[Info] Calculando estadísticas...")
    if len(paises) < 1:
        print("[Advertencia] Países insuficientes para calcular estadísticas")
        return

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
            prom_superficie = prom_superficie + pais["superficie"]

        paises_por_continente[pais["continente"]] = (
            paises_por_continente.get(pais["continente"], 0) + 1
        )

    if poblacion_cantidad > 0:
        prom_poblacion /= poblacion_cantidad

    if superficie_cantidad > 0:
        prom_superficie /= superficie_cantidad

    print(f"\n┏{'━'*40}┓")
    print(f"┃{'RESUMEN ESTADÍSTICO GLOBAL'.center(40)}┃")
    print(f"┣{'━'*40}┫")
    
    print("┃  Mayor Población:")
    print(f"┃      - {pais_mayor_poblacion['nombre']} ({pais_mayor_poblacion['poblacion']:,} hab.)")
    print(f"┠{'─'*40}┨")
    
    print("┃  Menor Población:")
    print(f"┃      - {pais_menor_poblacion['nombre']} ({pais_menor_poblacion['poblacion']:,} hab.)")
    print(f"┠{'─'*40}┨")
    
    print("┃  Promedios Mundiales:")
    print(f"┃      - Población : {prom_poblacion:,.2f} hab.")
    print(f"┃      - Superficie: {prom_superficie:,.2f} km²")
    print(f"┠{'─'*40}┨")
    
    print("┃  Países por Continente:")
    for continente, cantidad in paises_por_continente.items():
        print(f"┃      - {continente.ljust(15)} : {cantidad} países")
        
    print(f"┗{'━'*40}┛\n")


# Función principal que controla el flujo de la aplicación
def init():
    is_active = True
    print(f"\n════════════════════════════════════════════")
    print(f"{'¡BIENVENIDO AL GESTOR DE PAÍSES!'.center(44)}")
    print(f"════════════════════════════════════════════")
    
    data = get_countries_csv()
    paises = data["paises"]
    nombre_archivo = data["nombre_archivo"]
    
    while is_active:
        print_menu()
        print_separador()
        opcion = input("> Ingrese su opción: ").strip()
        
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
            print("\n¡Saliendo del programa. Que tengas un buen día!\n")
        elif opcion == "x":
            mostrar_paises(paises)
        else:
            print("[Error] Opción inválida, por favor intente de nuevo.")


# Punto de entrada del programa
if __name__ == "__main__":
    try:
        init()
    except KeyboardInterrupt:
        print("\n\n[Cancelado] Programa cancelado por el usuario. ¡Adiós!\n")
    except Exception as e:
        print(f"\n[Error] Ocurrió un error inesperado: {e}")
        print("¡Adiós!\n")