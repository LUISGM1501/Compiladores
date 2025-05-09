"""
Definición de tokens y palabras reservadas para el lenguaje MC - Versión optimizada
"""

from enum import Enum, auto

class TokenCategory(Enum):
    """Categorías para organizar los tokens"""
    PROGRAM_STRUCTURE = "Estructura del Programa"
    DATA_TYPES = "Tipos de datos"
    BOOLEAN_LITERALS = "Literales booleanas"
    BLOCK_DELIMITERS = "Delimitadores de bloques"
    FLOW_CONTROL = "Control de flujo"
    FUNCTIONS = "Funciones y procedimientos"
    CHAR_OPERATORS = "Operadores de caracteres"
    LOGIC_OPERATORS = "Operadores lógicos"
    STRING_OPERATORS = "Operadores de strings"
    SET_OPERATORS = "Operadores de conjuntos"
    FILE_OPERATORS = "Operadores de archivos"
    COMPARISON_OPERATORS = "Operadores de comparación"
    IO_FUNCTIONS = "Funciones de entrada/salida"
    OTHER_OPERATORS = "Otros operadores"
    OPERATORS = "Operadores"
    IDENTIFIERS = "Identificadores"
    LITERALS = "Literales"
    SPECIAL = "Especiales"

class Token:
    """Clase Token mejorada con categorización"""
    def __init__(self, type, lexema, linea, columna, valor=None, categoria=None):
        self.type = type
        self.lexema = lexema
        self.linea = linea
        self.columna = columna
        self.valor = valor
        self.categoria = categoria if categoria is not None else TokenCategory.SPECIAL
    
    def __str__(self):
        """Representación en cadena del token"""
        return f"Token(type={self.type}, lexema='{self.lexema}', linea={self.linea}, columna={self.columna})"

# Diccionario simplificado de palabras reservadas
PALABRAS_RESERVADAS = {
    'worldname': 'WORLD_NAME',
    'bedrock': 'BEDROCK',
    'resourcepack': 'RESOURCE_PACK',
    'inventory': 'INVENTORY',
    'recipe': 'RECIPE',
    'craftingtable': 'CRAFTING_TABLE',
    'spawnpoint': 'SPAWN_POINT',
    'obsidian': 'OBSIDIAN',
    'anvil': 'ANVIL',
    'worldsave': 'WORLD_SAVE',
    'stack': 'STACK',
    'rune': 'RUNE',
    'spider': 'SPIDER',
    'torch': 'TORCH',
    'chest': 'CHEST',
    'book': 'BOOK',
    'ghast': 'GHAST',
    'shelf': 'SHELF',
    'entity': 'ENTITY',
    'ref': 'REF',
    'on': 'ON',
    'off': 'OFF',
    'repeater': 'REPEATER',
    'craft': 'CRAFT',
    'target': 'TARGET',
    'hit': 'HIT',
    'miss': 'MISS',
    'jukebox': 'JUKEBOX',
    'disc': 'DISC',
    'silence': 'SILENCE',
    'spawner': 'SPAWNER',
    'exhausted': 'EXHAUSTED',
    'walk': 'WALK',
    'set': 'SET',
    'to': 'TO',
    'step': 'STEP',
    'wither': 'WITHER',
    'creeper': 'CREEPER',
    'enderpearl': 'ENDER_PEARL',
    'ragequit': 'RAGEQUIT',
    'spell': 'SPELL',
    'ritual': 'RITUAL',
    'respawn': 'RESPAWN',
    'isengraved': 'IS_ENGRAVED',
    'isinscribed': 'IS_INSCRIBED',
    'etchup': 'ETCH_UP',
    'etchdown': 'ETCH_DOWN',
    'and': 'AND',
    'or': 'OR',
    'not': 'NOT',
    'xor': 'XOR',
    'bind': 'BIND',
    'hash': 'HASH',
    'from': 'FROM',
    'except': 'EXCEPT',
    'seek': 'SEEK',
    'add': 'ADD',
    'drop': 'DROP',
    'feed': 'FEED',
    'map': 'MAP',
    'biom': 'BIOM',
    'kill': 'KILL',
    'unlock': 'UNLOCK',
    'lock': 'LOCK',
    'make': 'MAKE',
    'gather': 'GATHER',
    'forge': 'FORGE',
    'expand': 'EXPAND',
    'is': 'IS',
    'isnot': 'IS_NOT',
    'hopperstack': 'HOPPER_STACK',
    'hopperrune': 'HOPPER_RUNE',
    'hopperspider': 'HOPPER_SPIDER',
    'hoppertorch': 'HOPPER_TORCH',
    'hopperchest': 'HOPPER_CHEST',
    'hopperghast': 'HOPPER_GHAST',
    'dropperstack': 'DROPPER_STACK',
    'dropperrune': 'DROPPER_RUNE',
    'dropperspider': 'DROPPER_SPIDER',
    'droppertorch': 'DROPPER_TORCH',
    'dropperchest': 'DROPPER_CHEST',
    'dropperghast': 'DROPPER_GHAST',
    'chunk': 'CHUNK',
    'soulsand': 'SOULSAND',
    'magma': 'MAGMA'
}

# Operadores especiales
OPERADORES_ESPECIALES = {
    '{': 'POLLO_CRUDO',
    '}': 'POLLO_ASADO'
}