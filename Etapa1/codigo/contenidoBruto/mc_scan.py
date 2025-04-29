#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MC Scanner - Interfaz de línea de comandos principal para Notch Engine
"""

import sys
import os
import time
from pathlib import Path
from scanner.core import Scanner
from scanner.error_handling import ErrorHandler
from scanner.utils.cantidadComentarios import contar_comentarios_bloque, contar_comentarios_linea
from muroLadrillos.generarMuroLadrillos import generarLadrillos
from scanner.tokens import TIPOS_TOKEN

def main():
    """
    Función principal para ejecución desde línea de comandos
    
    Uso: python mc_scan.py <archivo_fuente>
    """
    # Verificar argumentos
    if len(sys.argv) != 2:
        print(f"Uso: python {sys.argv[0]} <archivo_fuente>")
        return 1
    
    archivo_fuente = sys.argv[1]
    
    # Verificar que el archivo existe
    if not os.path.isfile(archivo_fuente):
        print(f"Error: El archivo '{archivo_fuente}' no existe")
        return 1
    
    # Ejecutar el scanner
    return procesar_archivo(archivo_fuente)

def procesar_archivo(ruta_archivo):
    """
    Procesa un archivo con el scanner
    
    Argumentos:
        ruta_archivo (str): Ruta al archivo a procesar
    
    Retorna:
        int: Código de salida (0 si ok, 1 si error)
    """
    print(f"\n=== Analizando archivo: {ruta_archivo} ===")
    
    try:
        # Contar líneas y caracteres
        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            contenido = f.read()
            num_lineas = len(contenido.splitlines())
            num_caracteres = len(contenido)
            num_comentarios_linea = contar_comentarios_linea(contenido)
            num_comentarios_bloque = contar_comentarios_bloque(contenido)
        
        # Instanciar manejador de errores
        manejador_errores = ErrorHandler()
        
        # Instanciar y ejecutar scanner
        inicio = time.time()
        scanner = Scanner(ruta_archivo, manejador_errores)
        scanner.inicializar_scanner()
        
        # Recopilar todos los tokens
        tokens = []
        token = scanner.deme_token()
        tokens.append(token)
        
        while token.tipo != "EOF":
            token = scanner.deme_token()
            tokens.append(token)
        
        scanner.finalizar_scanner()
        fin = time.time()
        
        # Imprimir resumen
        print(f"\nAnalizado en {fin - inicio:.4f} segundos")
        print(f"Líneas de código: {num_lineas}")
        print(f"Caracteres: {num_caracteres}")
        print(f"Tokens encontrados: {len(tokens)}")
        print(f"Errores detectados: {manejador_errores.contar_errores()}")
        
        # Preparar datos para el muro de ladrillos
        lexemas = []
        for t in tokens:
            if t.tipo not in ['EOF', 'COMENTARIO']:
                lexemas.append(t.lexema)
        
        # Calcular estadísticas de tokens
        estadisticas = calcular_estadisticas_tokens(tokens)
        
        # Generar HTML con los resultados
        nombre_base = Path(ruta_archivo).stem
        nombre_resultado = f"{nombre_base}_Resultado.html"
        ruta_resultado = Path("resultados") / nombre_resultado
        
        # Asegurar que la carpeta resultados existe
        Path("resultados").mkdir(exist_ok=True)
        
        # Generar el HTML
        generarLadrillos(
            contenido=lexemas,
            estadisticaToken=estadisticas,
            lineasPrograma=num_lineas,
            numeroCaracteresEntrada=num_caracteres,
            numeroComentariosLinea=num_comentarios_linea,
            numeroComentariosBloque=num_comentarios_bloque,
            cantidadErrores=manejador_errores.contar_errores()
        )
        
        # Mover el archivo generado a la carpeta resultados
        try:
            Path("analisis_lexico.html").rename(ruta_resultado)
            print(f"\n✅ Resultado guardado en: {ruta_resultado}")
        except Exception as e:
            print(f"\n⚠️ Error al guardar resultados: {e}")
            print(f"El archivo temporal está en: analisis_lexico.html")
        
        # Si hay errores, mostrar resumen
        if manejador_errores.hay_errores():
            print("\n--- Resumen de errores ---")
            print(manejador_errores.obtener_resumen())
            return 1
        
        return 0
    
    except Exception as e:
        print(f"\n❌ Error durante el análisis: {e}")
        import traceback
        traceback.print_exc()
        return 1

def calcular_estadisticas_tokens(tokens):
    """
    Calcula estadísticas sobre los tokens encontrados
    
    Argumentos:
        tokens (list): Lista de tokens encontrados
    
    Retorna:
        dict: Diccionario con estadísticas de tokens
    """
    # Inicializar categorías
    estadisticas = {
        "Palabras reservadas": 0,
        "Identificadores": 0,
        "Literales numéricos": 0,
        "Literales de texto": 0,
        "Operadores": 0,
        "Comentarios": 0,
        "Errores léxicos": 0
    }
    
    # Clasificar tokens por categoría
    for token in tokens:
        if token.tipo == "IDENTIFICADOR":
            estadisticas["Identificadores"] += 1
        elif token.tipo in ["NUMERO_ENTERO", "NUMERO_DECIMAL"]:
            estadisticas["Literales numéricos"] += 1
        elif token.tipo in ["CADENA", "CARACTER"]:
            estadisticas["Literales de texto"] += 1
        elif token.tipo == "COMENTARIO":
            estadisticas["Comentarios"] += 1
        elif token.tipo == "ERROR":
            estadisticas["Errores léxicos"] += 1
        elif token.tipo in TIPOS_TOKEN:
            # Verificar si es un operador
            lexema = TIPOS_TOKEN.get(token.tipo, "")
            if any(c in lexema for c in "+-*/%<>=&|!~@#[]{}();:,."):
                estadisticas["Operadores"] += 1
            else:
                estadisticas["Palabras reservadas"] += 1
    
    return estadisticas

def ejecucion():
    """
    Función de ejecución interactiva
    """
    # Asegurar que la carpeta resultados existe
    resultados_dir = Path("resultados")
    resultados_dir.mkdir(exist_ok=True)
    
    # Obtener lista de pruebas disponibles
    pruebas_dir = Path("Pruebas")
    pruebas = sorted([p for p in pruebas_dir.glob("*.txt")])
    
    if not pruebas:
        print("No se encontraron archivos de prueba en la carpeta Pruebas/")
        return
    
    # Mostrar menú interactivo
    print("\n" + "="*50)
    print("MC Scanner - Menú de Pruebas".center(50))
    print("="*50)
    
    for i, prueba in enumerate(pruebas, 1):
        print(f"{i:2d}. {prueba.name}")
    print("\n0. Salir")
    
    # Selección de prueba
    while True:
        try:
            seleccion = int(input("\nSeleccione una prueba (número): "))
            if 0 <= seleccion <= len(pruebas):
                break
            print("Error: Selección fuera de rango")
        except ValueError:
            print("Error: Ingrese un número válido")
    
    if seleccion == 0:
        print("Saliendo...")
        return
    
    archivo_prueba = pruebas[seleccion-1]
    
    # Procesar el archivo
    procesar_archivo(str(archivo_prueba))

if __name__ == "__main__":
    if len(sys.argv) > 1:
        sys.exit(main())
    else:
        ejecucion()