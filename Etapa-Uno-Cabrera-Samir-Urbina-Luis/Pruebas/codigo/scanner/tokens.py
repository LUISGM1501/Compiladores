# /Etapa1/codigo/scanner/tokens.py
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Definición de tokens para el lenguaje MC
"""

class Token:
    """
    Clase que representa un token del lenguaje
    """
    def __init__(self, tipo, lexema, linea, columna, valor=None):
        """
        Inicializa un nuevo token
        
        Argumentos:
            tipo: Tipo del token
            lexema: Representación textual del token
            linea: Número de línea donde aparece el token
            columna: Número de columna donde aparece el token
            valor: Valor semántico del token (opcional)
        """
        self.tipo = tipo
        self.lexema = lexema
        self.linea = linea
        self.columna = columna
        self.valor = valor
    
    def __str__(self):
        """
        Representación textual del token
        """
        if self.valor is not None:
            return f"<{self.tipo}, '{self.lexema}', {self.linea}:{self.columna}, {self.valor}>"
        else:
            return f"<{self.tipo}, '{self.lexema}', {self.linea}:{self.columna}>"


# Definición de tipos de tokens
TIPOS_TOKEN = {
    # Palabras reservadas - Estructura del Programa
    'WORLD_NAME': 'WorldName',
    'BEDROCK': 'Bedrock',
    'RESOURCE_PACK': 'ResourcePack',
    'INVENTORY': 'Inventory',
    'RECIPE': 'Recipe',
    'CRAFTING_TABLE': 'CraftingTable',
    'SPAWN_POINT': 'SpawnPoint',
    'OBSIDIAN': 'Obsidian',
    'ANVIL': 'Anvil',
    'WORLD_SAVE': 'worldSave',
    
    # Tipos de datos
    'STACK': 'Stack',
    'RUNE': 'Rune',
    'SPIDER': 'Spider',
    'TORCH': 'Torch',
    'CHEST': 'Chest',
    'BOOK': 'Book',
    'GHAST': 'Ghast',
    'SHELF': 'Shelf',
    'ENTITY': 'Entity',
    'REF': 'ref',
    
    # Literales booleanas
    'ON': 'On',
    'OFF': 'Off',
    
    # Delimitadores de bloques
    'POLLO_CRUDO': 'PolloCrudo',
    'POLLO_ASADO': 'PolloAsado',
    
    # Control de flujo
    'REPEATER': 'repeater',
    'CRAFT': 'craft',
    'TARGET': 'target',
    'HIT': 'hit',
    'MISS': 'miss',
    'JUKEBOX': 'jukebox',
    'DISC': 'disc',
    'SILENCE': 'silence',
    'SPAWNER': 'spawner',
    'EXHAUSTED': 'exhausted',
    'WALK': 'walk',
    'SET': 'set',
    'TO': 'to',
    'STEP': 'step',
    'WITHER': 'wither',
    'CREEPER': 'creeper',
    'ENDER_PEARL': 'enderPearl',
    'RAGEQUIT': 'ragequit',
    
    # Funciones y procedimientos
    'SPELL': 'Spell',
    'RITUAL': 'Ritual',
    'RESPAWN': 'respawn',
    
    # Operadores de caracteres
    'IS_ENGRAVED': 'isEngraved',
    'IS_INSCRIBED': 'isInscribed',
    'ETCH_UP': 'etchUp',
    'ETCH_DOWN': 'etchDown',
    
    # Operadores lógicos
    'AND': 'and',
    'OR': 'or',
    'NOT': 'not',
    'XOR': 'xor',
    
    # Operadores de strings
    'BIND': 'bind',
    'HASH': '#',
    'FROM': 'from',
    'EXCEPT': 'except',
    'SEEK': 'seek',
    
    # Operadores de conjuntos
    'ADD': 'add',
    'DROP': 'drop',
    'FEED': 'feed',
    'MAP': 'map',
    'BIOM': 'biom',
    'KILL': 'kill',
    
    # Operadores de archivos
    'UNLOCK': 'unlock',
    'LOCK': 'lock',
    'MAKE': 'make',
    'GATHER': 'gather',
    'FORGE': 'forge',
    'EXPAND': 'expand',
    
    # Operadores de comparación
    'IS': 'is',
    'IS_NOT': 'isNot',
    
    # Funciones de entrada/salida
    'HOPPER_STACK': 'hopperStack',
    'HOPPER_RUNE': 'hopperRune',
    'HOPPER_SPIDER': 'hopperSpider',
    'HOPPER_TORCH': 'hopperTorch',
    'HOPPER_CHEST': 'hopperChest',
    'HOPPER_GHAST': 'hopperGhast',
    'DROPPER_STACK': 'dropperStack',
    'DROPPER_RUNE': 'dropperRune',
    'DROPPER_SPIDER': 'dropperSpider',
    'DROPPER_TORCH': 'dropperTorch',
    'DROPPER_CHEST': 'dropperChest',
    'DROPPER_GHAST': 'dropperGhast',
    
    # Otros operadores
    'CHUNK': 'chunk',
    'SOULSAND': 'soulsand',
    'MAGMA': 'magma',
    
    # Tokens adicionales
    'IDENTIFICADOR': 'IDENTIFICADOR',
    'NUMERO_ENTERO': 'NUMERO_ENTERO',
    'NUMERO_DECIMAL': 'NUMERO_DECIMAL',
    'CADENA': 'CADENA',
    'COMENTARIO': 'COMENTARIO',
    
    # Operadores y símbolos
    'SUMA': '+',
    'RESTA': '-',
    'MULTIPLICACION': '*',
    'DIVISION': '/',
    'MODULO': '%',
    'MAYOR_QUE': '>',
    'MENOR_QUE': '<',
    'MAYOR_IGUAL': '>=',
    'MENOR_IGUAL': '<=',
    'IGUAL': '=',
    'DOBLE_IGUAL': '==',
    'DIFERENTE': '!=',
    'PUNTO_Y_COMA': ';',
    'COMA': ',',
    'PUNTO': '.',
    'DOS_PUNTOS': ':',
    'PARENTESIS_ABRE': '(',
    'PARENTESIS_CIERRA': ')',
    'CORCHETE_ABRE': '[',
    'CORCHETE_CIERRA': ']',
    'LLAVE_ABRE': '{',
    'LLAVE_CIERRA': '}',
    
    # Especiales
    'EOF': 'EOF',
    'ERROR': 'ERROR'
}

# Mapa inverso para buscar por lexema
PALABRAS_RESERVADAS = {}
for clave, valor in TIPOS_TOKEN.items():
    if valor not in ['+', '-', '*', '/', '%', '>', '<', '>=', '<=', '=', '==', '!=', ';', ',', '.', ':', '(', ')', '[', ']', '{', '}', 'IDENTIFICADOR', 'NUMERO_ENTERO', 'NUMERO_DECIMAL', 'CADENA', 'COMENTARIO', 'EOF', 'ERROR']:
        PALABRAS_RESERVADAS[valor] = clave