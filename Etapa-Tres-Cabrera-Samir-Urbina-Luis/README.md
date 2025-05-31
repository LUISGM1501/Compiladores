# Compiladores e Intérpretes IC5701

## Etapa Tres: Analizador Contextual (Semántico) 
**Estudiantes:** Samir Cabrera y Luis Urbina

---

## Estructura del Proyecto

- **`ASM/`**  
  Contiene los archivos fuente en lenguaje ensamblador desarrollados utilizando TASM (Turbo Assembler).

- **`documentacion/`**  
  Incluye la documentación detallada del analisis contextual y de la documentacion completa de la gramatica.

- **`gramatica/`**  
  Contiene el archivo relacionado con la definición gramatical del lenguaje usado en el proyecto. En este archivo esta la gramatica del lenguaje y la gramatica del parser usada en GikGram a partir de la pagina 60.

- **`pruebas/`**  
  Carpeta principal para la ejecución y validación del scanner. Contiene:

  - El código fuente del compilador.
  - Un conjunto de archivos de prueba que permiten verificar el funcionamiento del programa.
  - El archivo ejecutable del scanner, nombrado como `main.OMITIDO` por razones de compatibilidad.

---

## Ejecución del Analisis Contextual

Para ejecutar el Analisis Contextual correctamente, sigue los siguientes pasos:

1. **Ubica la carpeta `pruebas/`** dentro del repositorio del proyecto.

2. **Identifica el archivo llamado `main.OMITIDO`**.  
   Este archivo es el ejecutable del scanner, pero debe ser renombrado para poder utilizarse.

3. **Renombra el archivo a mano**, eliminando la extensión `.OMITIDO`  
   El nombre final del archivo debe quedar como: **`main`**

4. **Ejecuta el archivo `main`** desde un entorno compatible.  
Al ejecutarlo, se generará automáticamente una carpeta llamada `resultados/`.

5. **Dentro de la carpeta `resultados/` encontrarás un archivo HTML** que muestra los resultados del análisis léxico realizado por el scanner.

6. **Visualización de resultados Scanner:**  Para visualizar el archivo HTML correctamente, se recomienda usar un navegador web o un entorno como **Live Server** en Visual Studio Code, que permite renderizar contenido HTML de forma local.

7. **Visualización de resultados Parser:** Para visualizar los resultados del parser se dejo activada la version de debug en el ejecutable, por lo que solo debe de hacer una lectura de los logs. 

8. **Visualización de resultados Analisis Contextual:** Para visualizar los resultados del analisis contextual se debe seleccionar el archivo a ejecutar, y seguidamente se debe de esperar a que termine la ejecucion del programa. Una vez hecho esto se debe de seleccionar la opcion de menu que se quiera. 

    1. Ver la Tabla de Simbolos
    2. Ver el Historial Semantico Completo
    3. Ver el Historial Semantico Negativo (Historial Semantico que contiene chequeos de posibles errores y tambien de aclaraciones en base a reglas de semantica)
    4. Salir

SE DEBEN DE IGNORAR LOS LOGS PREVIOS A ESTO, YA QUE SON PARTE DEL DEBUG DEL PROGRAMA Y PUEDEN PRESENTAR ERRORES INCONSISTENTES QUE SE ARREGLAN GRACIAS A LA GRAMATICA Y AL MANEJO SEMANTICO.

**Comando para ejecutar el archivo:** ./main


---

## Recomendaciones Finales

- El cambio de nombre del ejecutable **debe hacerse manualmente**. No se incluyen scripts ni instrucciones automatizadas.
- Asegúrate de que el archivo final se llame exactamente `main`, sin extensiones adicionales.

---
