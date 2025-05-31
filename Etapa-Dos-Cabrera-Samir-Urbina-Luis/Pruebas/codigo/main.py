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
from parser.semantica.HistorialSemantico import HistorialSemanticoSingleton

from token_cleaner import limpiar_tokens_para_parser, debug_tokens_para_parser

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
    
    #################################################################
    #################################################################
    ##                 LIMPIEZA DE TOKENS                          ##
    #################################################################
    print("\n" + "="*60)
    print("              APLICANDO LIMPIEZA DE TOKENS")
    print("="*60)
    
    # *** NUEVA FUNCIONALIDAD: Limpiar tokens ***
    tokens_limpios = limpiar_tokens_para_parser(tokens)
    
    # Debug de la limpieza (opcional, comentar si no quieres tanto detalle)
    debug_tokens_para_parser(tokens, tokens_limpios)
    
    #################################################################
    #################################################################
    ##                    INICIO ANALISIS                          ##
    ##                  SINTACTICO Y SEMANTICO                     ##
    #################################################################
    # Funcionamiento del parser con tokens limpios
    iniciar_parser(tokens_limpios, debug=False, nivel_debug=1) 

    tabla = TablaSimbolos.instancia()
    print(f" \n\n Ver informacion de la tablas semantica:")
    tabla.imprimir_tabla()

    historialSemantico = HistorialSemanticoSingleton()
    print(f"\n\n Ver informacion del historial semantico:")
    historialSemantico.imprimir_historial()
    
    # NUEVO: Mostrar resultados de operadores compuestos
    mostrar_resultados_operadores_compuestos()
    
    #################################################################
    #################################################################

def mostrar_resultados_operadores_compuestos():
    """Muestra los resultados de las operaciones compuestas"""
    tabla = TablaSimbolos.instancia()
    
    print("\n" + "="*50)
    print("RESULTADOS DE OPERADORES COMPUESTOS")
    print("="*50)
    
    variables_interes = ["numero1", "numero2", "flotante1", "flotante2", "cadena1", "cadena2"]
    
    for var_nombre in variables_interes:
        simbolo = tabla.buscar(var_nombre)
        if simbolo:
            print(f"{var_nombre} ({simbolo.tipo}): {simbolo.valor}")
        else:
            print(f"{var_nombre}: No encontrado")
    
    print("="*50)

if __name__ == "__main__":
    ejecucion()
