"""
Compilador Notch Engine

Estudiantes: Cabrera Samir y Urbina Luis

Archivo: mc_scanner.py

Breve Descripcion: orquestador scanner
"""

import sys
import os
from pathlib import Path

# Asegurarse de que el directorio actual está en el path para las importaciones
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .core import Scanner, ErrorHandler
from .utils.cantidadComentarios import contar_comentarios_bloque, contar_comentarios_linea
from .muroLadrillos.generarMuroLadrillos import generarLadrillos

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
    manejador_errores = ErrorHandler()
    scanner = Scanner(str(archivo_prueba), manejador_errores)
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
        if token.type == 'EOF':
            break
        elif token.type == 'ERROR':
            estadisticas["Errores léxicos"] += 1
        elif token.type in ['WORLD_NAME', 'BEDROCK', 'RESOURCE_PACK', 'INVENTORY', 'RECIPE', 
                           'CRAFTING_TABLE', 'SPAWN_POINT', 'OBSIDIAN', 'ANVIL', 'WORLD_SAVE',
                           'STACK', 'RUNE', 'SPIDER', 'TORCH', 'CHEST', 'BOOK', 'GHAST', 'SHELF',
                           'ENTITY', 'REF', 'ON', 'OFF', 'REPEATER', 'CRAFT', 'TARGET', 'HIT',
                           'MISS', 'JUKEBOX', 'DISC', 'SILENCE', 'SPAWNER', 'EXHAUSTED', 'WALK',
                           'SET', 'TO', 'STEP', 'WITHER', 'CREEPER', 'ENDER_PEARL', 'RAGEQUIT',
                           'SPELL', 'RITUAL', 'RESPAWN', 'IS_ENGRAVED', 'IS_INSCRIBED', 'ETCH_UP',
                           'ETCH_DOWN', 'AND', 'OR', 'NOT', 'XOR', 'BIND', 'HASH', 'FROM', 'EXCEPT',
                           'SEEK', 'ADD', 'DROP', 'FEED', 'MAP', 'BIOM', 'KILL', 'UNLOCK', 'LOCK',
                           'MAKE', 'GATHER', 'FORGE', 'EXPAND', 'IS', 'IS_NOT', 'HOPPER_STACK',
                           'HOPPER_RUNE', 'HOPPER_SPIDER', 'HOPPER_TORCH', 'HOPPER_CHEST',
                           'HOPPER_GHAST', 'DROPPER_STACK', 'DROPPER_RUNE', 'DROPPER_SPIDER',
                           'DROPPER_TORCH', 'DROPPER_CHEST', 'DROPPER_GHAST', 'CHUNK', 'SOULSAND',
                           'MAGMA', 'POLLO_CRUDO', 'POLLO_ASADO']:
            estadisticas["Palabras reservadas"] += 1
            lexemas.append(token.lexema)
        elif token.type == 'IDENTIFICADOR':
            estadisticas["Identificadores"] += 1
            lexemas.append(token.lexema)
        elif token.type in ['NUMERO_ENTERO', 'NUMERO_DECIMAL']:
            estadisticas["Literales numéricos"] += 1
            lexemas.append(token.lexema)
        elif token.type in ['CADENA', 'CARACTER']:
            estadisticas["Literales de texto"] += 1
            lexemas.append(token.lexema)
        elif token.type not in ['COMENTARIO']:
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
    resultados_dir = Path("resultadosScanner")
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