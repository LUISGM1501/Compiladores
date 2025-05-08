# Compiladores e Intérpretes IC5701

## Etapa 1: Scanner

**Estudiantes:** Samir Cabrera y Luis Urbina

---

## Estructura del Proyecto

- **`ASM/`**  
  Contiene los archivos fuente en lenguaje ensamblador desarrollados utilizando TASM (Turbo Assembler).

- **`documentacion/`**  
  Incluye la documentación detallada del autómata finito diseñado para el análisis léxico del lenguaje.

- **`gramatica/`**  
  Contiene los archivos relacionados con la definición gramatical del lenguaje usado en el proyecto.

- **`pruebas/`**  
  Carpeta principal para la ejecución y validación del scanner. Contiene:

  - El código fuente del scanner.
  - Un conjunto de archivos de prueba que permiten verificar el funcionamiento del programa.
  - El archivo ejecutable del scanner, nombrado como `MC_Scanner.OMITIDO` por razones de compatibilidad.

---

## Ejecución del Scanner

Para ejecutar el scanner correctamente, sigue los siguientes pasos:

1. **Ubica la carpeta `pruebas/`** dentro del repositorio del proyecto.

2. **Identifica el archivo llamado `MC_Scanner.OMITIDO`**.  
   Este archivo es el ejecutable del scanner, pero debe ser renombrado para poder utilizarse.

3. **Renombra el archivo a mano**, eliminando la extensión `.OMITIDO`.  
   El nombre final del archivo debe quedar como: **`MC_Scanner`**


4. **Ejecuta el archivo `MC_Scanner`** desde un entorno compatible.  
Al ejecutarlo, se generará automáticamente una carpeta llamada `resultados/`.

5. **Dentro de la carpeta `resultados/` encontrarás un archivo HTML** que muestra los resultados del análisis léxico realizado por el scanner.

6. **Visualización de resultados:**  Para visualizar el archivo HTML correctamente, se recomienda usar un navegador web o un entorno como **Live Server** en Visual Studio Code, que permite renderizar contenido HTML de forma local.

---

## Recomendaciones Finales

- El cambio de nombre del ejecutable **debe hacerse manualmente**. No se incluyen scripts ni instrucciones automatizadas.
- Asegúrate de que el archivo final se llame exactamente `MC_Scanner`, sin extensiones adicionales.
- La visualización del archivo HTML es esencial para una correcta interpretación de los resultados del análisis.

---
