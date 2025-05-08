# /Etapa1/codigo/contenidoBruto/mc_scan.py  
"""
MC Scanner - Interfaz de línea de comandos principal
"""

import sys
import os
from pathlib import Path
from scanner.core import Scanner
from scanner.error_handling import ErrorHandler
from scanner.utils.cantidadComentarios import contar_comentarios_bloque, contar_comentarios_linea
from muroLadrillos.generarMuroLadrillos import generarLadrillos
from scanner.tokens import PALABRAS_RESERVADAS

def main():
    """Función principal original (se mantiene intacta)"""
    # ... (código original de main permanece igual)
    # Solo añadimos el return al final para evitar código inalcanzable
    return 0

def ejecucion():
    """
    Función de ejecución interactiva con gestión correcta de resultados
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
    print(f"\nEjecutando prueba: {archivo_prueba.name}")
    
    # Contar líneas y caracteres
    with open(archivo_prueba, 'r', encoding='utf-8') as f:
        contenido = f.read()
        num_lineas = len(contenido.splitlines())
        num_caracteres = len(contenido)
        num_cometario_lineas = contar_comentarios_linea(contenido)
        num_comentario_bloque = contar_comentarios_bloque(contenido)
    
    # Procesar tokens
    manejador_errores = ErrorHandler()
    scanner = Scanner(str(archivo_prueba), manejador_errores)
    scanner.inicializar_scanner()
    
    tokens = []
    while True:
        token = scanner.deme_token()
        tokens.append(token)
        if token.tipo == 'EOF':
            break
    
    scanner.finalizar_scanner()
    
    # Preparar datos para el HTML - Solución corregida
    lexemas = []
    for t in tokens:
        if t.tipo not in ['EOF', 'COMENTARIO']:
            # Añadir el lexema completo directamente
            lexemas.append(t.lexema)
    
    # Filtrar espacios y elementos vacíos, asegurándose de no descomponer los lexemas
    lexemas = [lex for lex in lexemas if lex.strip() and len(lex) > 0]
    
    # Después de recolectar todos los tokens
    print("\nDebug - Tokens recolectados:")
    for i, token in enumerate(tokens[:20]):  # Mostrar primeros 20 tokens para debug
        print(f"Token {i+1}: Tipo='{token.tipo}' | Lexema='{token.lexema}' | Pos={token.linea}:{token.columna}")

    # Verificar si los lexemas ya vienen divididos del scanner
    print("\nLexemas antes de cualquier procesamiento:")
    print([t.lexema for t in tokens[:20]])
    
    # Debug - imprimir los primeros 5 lexemas para verificar
    print("Primeros 5 lexemas:")
    for i, lex in enumerate(lexemas[:5]):
        print(f"{i+1}. '{lex}'")
    
    
    # Calcular estadísticas de tokens (ejemplo)
    estadisticas = {
        "Palabras reservadas": sum(1 for t in tokens if t.tipo in PALABRAS_RESERVADAS.values()),
        "Identificadores": sum(1 for t in tokens if t.tipo == 'IDENTIFICADOR'),
        "Literales numéricos": sum(1 for t in tokens if t.tipo in ['NUMERO_ENTERO', 'NUMERO_DECIMAL']),
        "Literales de texto": sum(1 for t in tokens if t.tipo == 'CADENA'),
        "Operadores": sum(1 for t in tokens if t.tipo in [
            'SUMA', 'RESTA', 'MULTIPLICACION', 'DIVISION', 'MODULO',
            'MAYOR_QUE', 'MENOR_QUE', 'MAYOR_IGUAL', 'MENOR_IGUAL',
            'IGUAL', 'DOBLE_IGUAL', 'DIFERENTE', 'PUNTO_Y_COMA',
            'COMA', 'PUNTO', 'DOS_PUNTOS', 'PARENTESIS_ABRE',
            'PARENTESIS_CIERRA', 'CORCHETE_ABRE', 'CORCHETE_CIERRA',
            'LLAVE_ABRE', 'LLAVE_CIERRA', 'HASH'
        ]),
        "Errores léxicos": sum(1 for t in tokens if t.tipo == 'ERROR')
    }
    
    # Manejo de errores robusto
    cantidad_errores = 0
    if hasattr(manejador_errores, 'contar_errores'):
        cantidad_errores = manejador_errores.contar_errores()
    elif manejador_errores.hay_errores():
        cantidad_errores = 1  # Valor por defecto si no podemos contar
    
    # Generar nombre del archivo de resultado exacto como se solicita
    nombre_base = archivo_prueba.stem  # Elimina la extensión .txt
    nombre_resultado = f"{nombre_base}_Resultado.html"
    ruta_resultado = resultados_dir / nombre_resultado
    
    # Generar el HTML
    generarLadrillos(
        contenido=lexemas,
        estadisticaToken=estadisticas,
        lineasPrograma=num_lineas,
        numeroCaracteresEntrada=num_caracteres,
        numeroComentariosLinea=num_cometario_lineas,
        numeroComentariosBloque=num_comentario_bloque,
        cantidadErrores=cantidad_errores
    )
    
    # Mover el archivo generado a la carpeta resultados
    try:
        Path("analisis_lexico.html").rename(ruta_resultado)
        print(f"\n✅ Resultado guardado en: {ruta_resultado}")
    except Exception as e:
        print(f"\n⚠️ Error al guardar resultados: {e}")
        print(f"El archivo temporal está en: analisis_lexico.html")
    
    print("="*50 + "\n")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        sys.exit(main())
    else:
        ejecucion()