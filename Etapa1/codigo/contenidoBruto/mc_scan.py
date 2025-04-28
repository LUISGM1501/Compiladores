# /Etapa1/codigo/contenidoBruto/mc_scan.py
"""
MC Scanner - Interfaz de línea de comandos principal
"""

import sys
import os
from scanner.core import Scanner
from scanner.error_handling import ErrorHandler
from scanner.html_generator import HtmlGenerator

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
    
    # Crear generador HTML
    generador_html = HtmlGenerator()
    
    # Crear y inicializar el scanner
    scanner = Scanner(archivo_fuente, manejador_errores)
    scanner.inicializar_scanner()
    
    # Procesar todos los tokens
    print(f"Analizando archivo: {archivo_fuente}")
    print("-" * 50)
    
    # Contar líneas y caracteres del archivo
    with open(archivo_fuente, 'r', encoding='utf-8') as f:
        contenido = f.read()
        num_lineas = len(contenido.splitlines())
        num_caracteres = len(contenido)
    
    # Establecer estadísticas de archivo
    generador_html.establecer_estadisticas_archivo(num_lineas, num_caracteres)
    
    # Procesar todos los tokens
    while True:
        token = scanner.deme_token()
        print(f"Token: {token}")
        
        # Agregar token al generador HTML
        generador_html.agregar_token(token)
        
        if token.tipo == 'EOF':
            break
    
    # Finalizar el scanner
    scanner.finalizar_scanner()
    
    # Generar el archivo HTML con el muro de ladrillos
    nombre_archivo_html = os.path.splitext(archivo_fuente)[0] + "_ladrillos.html"
    generador_html.generar_html(nombre_archivo_html)
    
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