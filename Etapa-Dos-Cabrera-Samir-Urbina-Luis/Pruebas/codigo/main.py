"""
Compilador Notch Engine

Estudiantes: Cabrera Samir y Urbina Luis

Archivo: main.py

Breve Descripcion: Archivo de gestion principal
"""

import sys
import os
from pathlib import Path

# Asegurarse de que el directorio actual está en el path para las importaciones
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scanner.mc_scanner import procesar_archivo
from parser.mc_parser import iniciar_parser
from parser.gramatica.Gramatica import Gramatica
from parser.semantica.TablaSimbolos import TablaSimbolos

# Verificar integridad
Gramatica.verificarIntegridadRangos()

# Diagnosticar símbolos problemáticos
for simbolo in [220, 222, 224, 225, 226, 227, 228, 229, 230, 231]:
    print(Gramatica.diagnosticarSimbolo(simbolo))


def ejecucion():
    """Modo interactivo"""
    pruebas_dir = Path("Pruebas")
    pruebas = sorted([p for p in pruebas_dir.glob("*.txt")])
    
    if not pruebas:
        print("No se encontraron archivos de prueba en la carpeta Pruebas/")
        return
    
    # Mostrar menú
    print("\n" + "="*50)
    print("MC Scanner - Menú de Pruebas".center(50))
    print("="*50)
    for i, prueba in enumerate(pruebas, 1):
        print(f"{i:2d}. {prueba.name}")
    print("\n0. Salir")
    
    # Selección
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
    print(f"\nEjecutando prueba: {archivo_prueba.name}")
    
    #################################################################
    #################################################################
    ##                    INICIO SCANER                            ##
    #################################################################
    # Procesar y obtener tokens
    tokens = procesar_archivo(archivo_prueba)
    print("\nTokens generados (primeros 10):")
    for i, token in enumerate(tokens[:10]):
        print(f"{i}: {token}")
    
    # Debug: mostrar primeros 100 tokens
    print("\nPrimeros 100 tokens para el parser:")
    for token in tokens[:100]:
        print(token)

    
    #################################################################
    #################################################################
    ##                    INICIO ANALISIS                          ##
    ##                  SINTACTICO Y SEMANTICO                     ##
    #################################################################
    # Funcionamiento del parser 
    iniciar_parser(tokens, debug=True)

    tabla = TablaSimbolos.instancia()
    print(f" \n\n Ver informacion de la tablas semantica:")
    tabla.imprimir_tabla()
    
    #################################################################
    #################################################################

if __name__ == "__main__":
    ejecucion()
