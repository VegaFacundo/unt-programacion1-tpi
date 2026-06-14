# Sistema de Gestión de Países - TPI Programación I

Este repositorio contiene el desarrollo del **Trabajo Práctico Integrador (TPI)** de la materia **Programación I**, correspondiente a la **Tecnicatura Universitaria en Programación** de la **Universidad Tecnológica Nacional (UTN)**.

La aplicación consiste en un sistema de consola interactivo desarrollado en Python que permite gestionar, almacenar, filtrar, ordenar y calcular estadísticas a partir de un conjunto de datos (*dataset*) de países almacenado en formato CSV. El desarrollo pone en práctica conceptos de programación estructurada, modularización, manipulación de estructuras de datos complejas (listas de diccionarios) y persistencia mediante archivos.

---

## Características Principales

El sistema ofrece una interfaz interactiva en consola que implementa las siguientes funciones de negocio:

* **Configuración Inicial Dinámica:** Permite al usuario cargar un archivo CSV por defecto (`paises.csv`) o indicar una ruta personalizada. Si el archivo no existe, el programa lo crea de forma automática con los encabezados correspondientes.
* **Manejo de Datos (CRUD básico):**
  * **Agregar País:** Permite dar de alta un país validando que no se duplique su nombre y que los campos no queden vacíos.
  * **Actualizar Datos:** Posibilita la modificación de la población y la superficie de un país específico guardando el cambio de forma persistente.
* **Búsquedas y Filtros:**
  * **Búsqueda por Nombre:** Búsqueda flexible con coincidencia parcial o exacta.
  * **Filtros Personalizados:** Filtrado de registros por continente, rango de población o rango de superficie.
* **Ordenamiento Dinámico:** Reordena la lista de países por nombre, población o superficie (con opción de orden ascendente o descendente).
* **Módulo de Estadísticas:** Genera indicadores mundiales clave como:
  * País con mayor y menor población.
  * Promedio de habitantes por país.
  * Promedio de superficie terrestre.
  * Conteo de cantidad de países agrupados por continente.

---

## Tecnologías y Conceptos Aplicados

* **Lenguaje:** Python 3.12.x (utilizando únicamente la biblioteca estándar).
* **Manejo de Archivos:** Lectura y escritura con el módulo nativo `csv` (`DictReader` y `DictWriter`) para asegurar la persistencia en tiempo real de los datos.
* **Estructuras de Datos:** Almacenamiento en memoria mediante listas de diccionarios, lo que facilita el acceso indexado por clave y la manipulación semántica de los datos.
* **Validación de Entradas:** Implementación de funciones auxiliares (*helpers*) para encapsular el ingreso y control de tipos numéricos y cadenas de caracteres, evitando colapsos (*crashes*) inesperados en tiempo de ejecución.

---

## Instalación y Uso

### Requisitos Previos
* Tener instalado Python 3.x en el sistema.

### Instrucciones de Ejecución
1. Clona este repositorio en tu máquina local:
   ```bash
   git clone <URL_DEL_REPOSITORIO>

2.  Accede al directorio del proyecto:
    cd <NOMBRE_DEL_REPOSITORIO>
3.  Ejecuta la aplicación principal:
    python index.py

 Ejemplo de Uso de la Interfaz

Al iniciar el sistema y tras seleccionar o crear un archivo CSV de datos, se
presentará un visual e interactivo menú para modificar o mostrar el csv.


## Integrantes y Participación

Este proyecto fue desarrollado en equipo de forma equitativa por los siguientes
integrantes:

  - Facundo Vega - Contribuciones: Lógica de modularización,
    funciones de ordenamiento, persistencia y mapeo con la librería CSV.
    
  - Luca Joel Ferreira - Contribuciones: Manejo de validaciones de
    entrada, diseño estético de interfaz de consola
    y documentación.
