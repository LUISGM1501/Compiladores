# Compiladores e Intérpretes IC5701

## Etapa Dos: Parser

**Estudiantes:** Samir Cabrera y Luis Urbina

---

## Estructura del Proyecto

- **`ASM/`**  
  Contiene los archivos fuente en lenguaje ensamblador desarrollados utilizando TASM (Turbo Assembler).

- **`documentacion/`**  
  Incluye la documentación detallada del parser y de la documentacion completa de la gramatica.

- **`gramatica/`**  
  Contiene el archivo relacionado con la definición gramatical del lenguaje usado en el proyecto. En este archivo esta la gramatica del lenguaje y la gramatica del parser usada en GikGram a partir de la pagina 59.

- **`pruebas/`**  
  Carpeta principal para la ejecución y validación del scanner. Contiene:

  - El código fuente del compilador.
  - Un conjunto de archivos de prueba que permiten verificar el funcionamiento del programa.
  - El archivo ejecutable del scanner, nombrado como `main.OMITIDO` por razones de compatibilidad.

---

## Ejecución del Scanner

Para ejecutar el scanner correctamente, sigue los siguientes pasos:

1. **Ubica la carpeta `pruebas/`** dentro del repositorio del proyecto.

2. **Identifica el archivo llamado `MC_Scanner.OMITIDO`**.  
   Este archivo es el ejecutable del scanner, pero debe ser renombrado para poder utilizarse.

3. **Renombra el archivo a mano**, eliminando la extensión `.OMITIDO` y agregando la extension '.exe'.  
   El nombre final del archivo debe quedar como: **`main.exe`**


4. **Ejecuta el archivo `main.exex`** desde un entorno compatible.  
Al ejecutarlo, se generará automáticamente una carpeta llamada `resultados/`.

5. **Dentro de la carpeta `resultados/` encontrarás un archivo HTML** que muestra los resultados del análisis léxico realizado por el scanner.

6. **Visualización de resultados Scanner:**  Para visualizar el archivo HTML correctamente, se recomienda usar un navegador web o un entorno como **Live Server** en Visual Studio Code, que permite renderizar contenido HTML de forma local.

7. **Visualización de resultados Parser:** Para visualizar los resultados del parser se dejo activada la version de debug en el ejecutable, por lo que solo debe de hacer una lectura de los logs. 

---

## Recomendaciones Finales

- El cambio de nombre del ejecutable **debe hacerse manualmente**. No se incluyen scripts ni instrucciones automatizadas.
- Asegúrate de que el archivo final se llame exactamente `main.exe`, sin extensiones adicionales.

---