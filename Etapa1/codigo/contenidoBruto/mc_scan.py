#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MC Scanner - Interfaz de línea de comandos principal
"""

import sys
import os
from scanner.core import Scanner
from scanner.error_handling import ErrorHandler

def main():
    """
    Función principal que inicia el proceso de escaneo
    """
    # Verificar que se proporcione un nombre de archivo
    if len(sys.argv) != 2:
        print("Uso: python mc_scan.py <archivo_fuente>")
        sys.exit(1)
    
    # Obtener el nombre del archivo a compilar
    archivo_fuente = sys.argv[1]
    
    # Verificar que el archivo exista
    if not os.path.exists(archivo_fuente):
        print(f"Error: El archivo '{archivo_fuente}' no existe.")
        sys.exit(1)
    
    # Crear manejador de errores
    manejador_errores = ErrorHandler()
    
    # Crear y inicializar el scanner
    scanner = Scanner(archivo_fuente, manejador_errores)
    scanner.inicializar_scanner()
    
    # Procesar todos los tokens
    print(f"Analizando archivo: {archivo_fuente}")
    print("-" * 50)
    
    while True:
        token = scanner.deme_token()
        if token.tipo == 'EOF':
            break
        print(f"Token: {token}")
    
    # Finalizar el scanner
    scanner.finalizar_scanner()
    
    # Mostrar resumen de errores
    if manejador_errores.hay_errores():
        print("\nResumen de errores:")
        print(manejador_errores.obtener_resumen())
        return 1
    else:
        print("\nAnálisis léxico completado sin errores.")
        return 0

if __name__ == "__main__":
    sys.exit(main())