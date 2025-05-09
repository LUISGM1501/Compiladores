# /Etapa1/codigo/contenidoBruto/mc_scan.py
"""
MC Scanner - Versión optimizada
"""

import sys
from pathlib import Path
from scanner.core import Scanner
from scanner.utils.cantidadComentarios import contar_comentarios_bloque, contar_comentarios_linea
from muroLadrillos.generarMuroLadrillos import generarLadrillos
from scanner.tokens import PALABRAS_RESERVADAS

def procesar_archivo(archivo_prueba):
    """Procesa un archivo y genera resultados"""
    # Contar líneas y caracteres
    with open(archivo_prueba, 'r', encoding='utf-8') as f:
        contenido = f.read()
        num_lineas = len(contenido.splitlines())
        num_caracteres = len(contenido)
        num_cometario_lineas = contar_comentarios_linea(contenido)
        num_comentario_bloque = contar_comentarios_bloque(contenido)
    
    # Procesar tokens
    manejador_errores = "ErrorHandler()"
    scanner = Scanner(str(archivo_prueba))
    scanner.inicializar_scanner()
    
    tokens = []
    lexemas = []
    estadisticas = {
        "Palabras reservadas": 0,
        "Identificadores": 0,
        "Literales numéricos": 0,
        "Literales de texto": 0,
        "Operadores": 0,
        "Errores léxicos": 0
    }
    
    while True:
        token = scanner.deme_token()
        tokens.append(token)
        
        # Procesar para estadísticas
        if token.tipo == 'EOF':
            break
        elif token.tipo == 'ERROR':
            estadisticas["Errores léxicos"] += 1
        elif token.tipo in PALABRAS_RESERVADAS.values():
            estadisticas["Palabras reservadas"] += 1
            lexemas.append(token.lexema)
        elif token.tipo == 'IDENTIFICADOR':
            estadisticas["Identificadores"] += 1
            lexemas.append(token.lexema)
        elif token.tipo in ['NUMERO_ENTERO', 'NUMERO_DECIMAL']:
            estadisticas["Literales numéricos"] += 1
            lexemas.append(token.lexema)
        elif token.tipo in ['CADENA', 'CARACTER']:
            estadisticas["Literales de texto"] += 1
            lexemas.append(token.lexema)
        elif token.tipo not in ['COMENTARIO']:  # Excluir comentarios
            estadisticas["Operadores"] += 1
            lexemas.append(token.lexema)
    
    scanner.finalizar_scanner()
    
    # Generar HTML con el muro de ladrillos
    generarLadrillos(
        contenido=lexemas,
        estadisticaToken=estadisticas,
        lineasPrograma=num_lineas,
        numeroCaracteresEntrada=num_caracteres,
        numeroComentariosLinea=num_cometario_lineas,
        numeroComentariosBloque=num_comentario_bloque,
        cantidadErrores=estadisticas["Errores léxicos"]
    )
    
    # Mover archivo generado
    resultados_dir = Path("resultados")
    resultados_dir.mkdir(exist_ok=True)
    nombre_resultado = f"{archivo_prueba.stem}_Resultado.html"
    ruta_resultado = resultados_dir / nombre_resultado
    
    try:
        Path("analisis_lexico.html").rename(ruta_resultado)
        print(f"\n✅ Resultado guardado en: {ruta_resultado}")
    except Exception as e:
        print(f"\n⚠️ Error al guardar resultados: {e}")
        print(f"El archivo temporal está en: analisis_lexico.html")
    
    # Retornar tokens para el parser
    return tokens

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
    
    # Procesar y obtener tokens
    tokens = procesar_archivo(archivo_prueba)
    
    # Debug: mostrar primeros 10 tokens
    print("\nPrimeros 10 tokens para el parser:")
    for token in tokens[:10]:
        print(token)
    
    print("="*50 + "\n")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Modo no interactivo
        archivo = Path(sys.argv[1])
        if archivo.exists():
            tokens = procesar_archivo(archivo)
            # Aquí podrías pasar los tokens al parser
        else:
            print(f"Error: Archivo {sys.argv[1]} no encontrado")
            sys.exit(1)
    else:
        # Modo interactivo
        ejecucion()