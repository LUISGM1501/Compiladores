#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Definición de tokens para el lenguaje Notch Engine
"""

class Token:
    """
    Clase que representa un token del lenguaje
    """
    def __init__(self, tipo, lexema, linea, columna, valor=None, error=None):
        """
        Inicializa un nuevo token
        
        Argumentos:
            tipo: Tipo del token
            lexema: Representación textual del token
            linea: Número de línea donde aparece el token
            columna: Número de columna donde aparece el token
            valor: Valor semántico del token (opcional)
            error: Código de error si el token representa un error léxico
        """
        self.tipo = tipo
        self.lexema = lexema
        self.linea = linea
        self.columna = columna
        self.valor = valor
        self.error = error
    
    def __str__(self):
        """
        Representación textual del token
        """
        error_info = f", ERROR: {self.error}" if self.error else ""
        if self.valor is not None:
            return f"<{self.tipo}, '{self.lexema}', {self.linea}:{self.columna}, {self.valor}{error_info}>"
        else:
            return f"<{self.tipo}, '{self.lexema}', {self.linea}:{self.columna}{error_info}>"


# Definición de tipos de tokens
TIPOS_TOKEN = {
    # Palabras reservadas - Estructura del Programa
    'WORLDNAME': 'WorldName',
    'BEDROCK': 'Bedrock',
    'RESOURCEPACK': 'ResourcePack',
    'INVENTORY': 'Inventory',
    'RECIPE': 'Recipe',
    'CRAFTINGTABLE': 'CraftingTable',
    'SPAWNPOINT': 'SpawnPoint',
    'OBSIDIAN': 'Obsidian',
    'ANVIL': 'Anvil',
    'WORLDSAVE': 'worldSave',
    
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
    'POLLOCRUDO': 'PolloCrudo',
    'POLLOASADO': 'PolloAsado',
    
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
    'ENDERPEARL': 'enderPearl',
    'RAGEQUIT': 'ragequit',
    
    # Funciones y procedimientos
    'SPELL': 'Spell',
    'RITUAL': 'Ritual',
    'RESPAWN': 'respawn',
    
    # Operadores de caracteres
    'ISENGRAVED': 'isEngraved',
    'ISINSCRIBED': 'isInscribed',
    'ETCHUP': 'etchUp',
    'ETCHDOWN': 'etchDown',
    
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
    'TAG': 'tag',
    
    # Operadores de comparación
    'IS': 'is',
    'ISNOT': 'isNot',
    
    # Funciones de entrada/salida
    'HOPPERSTACK': 'hopperStack',
    'HOPPERRUNE': 'hopperRune',
    'HOPPERSPIDER': 'hopperSpider',
    'HOPPERTORCH': 'hopperTorch',
    'HOPPERCHEST': 'hopperChest',
    'HOPPERGHAST': 'hopperGhast',
    'DROPPERSTACK': 'dropperStack',
    'DROPPERRUNE': 'dropperRune',
    'DROPPERSPIDER': 'dropperSpider',
    'DROPPERTORCH': 'dropperTorch',
    'DROPPERCHEST': 'dropperChest',
    'DROPPERGHAST': 'dropperGhast',
    
    # Otros operadores
    'CHUNK': 'chunk',
    'SOULSAND': 'soulsand',
    'MAGMA': 'magma',
    
    # Tokens adicionales
    'IDENTIFICADOR': 'IDENTIFICADOR',
    'NUMERO_ENTERO': 'NUMERO_ENTERO',
    'NUMERO_DECIMAL': 'NUMERO_DECIMAL',
    'CADENA': 'CADENA',
    'CARACTER': 'CARACTER',
    'COMENTARIO': 'COMENTARIO',
    
    # Operadores y símbolos
    'SUMA': '+',
    'RESTA': '-',
    'MULTIPLICACION': '*',
    'DIVISION': '/',
    'DIVISION_ENTERA': '//',
    'MODULO': '%',
    'MAYOR_QUE': '>',
    'MENOR_QUE': '<',
    'MAYOR_IGUAL': '>=',
    'MENOR_IGUAL': '<=',
    'IGUAL': '=',
    'SUMA_IGUAL': '+=',
    'RESTA_IGUAL': '-=',
    'MULTIPLICACION_IGUAL': '*=',
    'DIVISION_IGUAL': '/=',
    'MODULO_IGUAL': '%=',
    'PUNTO_Y_COMA': ';',
    'COMA': ',',
    'PUNTO': '.',
    'DOS_PUNTOS': ':',
    'DOS_PUNTOS_DOBLE': '::',
    'PARENTESIS_ABRE': '(',
    'PARENTESIS_CIERRA': ')',
    'CORCHETE_ABRE': '[',
    'CORCHETE_CIERRA': ']',
    'LLAVE_ABRE': '{',
    'LLAVE_CIERRA': '}',
    'LLAVE_COLON_ABRE': '{:',
    'COLON_LLAVE_CIERRA': ':}',
    'LLAVE_SLASH_ABRE': '{/',
    'SLASH_LLAVE_CIERRA': '/}',
    'ARROBA': '@',
    'HASH_HASH': '##',
    'FLECHA': '->',
    'COERCION': '>>',
    'COLON_SUMA': ':+',
    'COLON_RESTA': ':-',
    'COLON_MULTI': ':*',
    'COLON_DIV': ':/',
    'COLON_DIV_ENTERA': '://',
    'COLON_MODULO': ':%',
    
    # Especiales
    'EOF': 'EOF',
    'ERROR': 'ERROR'
}

# Errores léxicos
ERRORES_LEXICOS = {
    'E1': 'Carácter no reconocido',
    'E2': 'Carácter Unicode no soportado',
    'E3': 'String sin cerrar',
    'E4': 'Carácter sin cerrar',
    'E5': 'Literal de carácter vacío',
    'E6': 'Secuencia de escape inválida',
    'E7': 'Múltiples caracteres en literal de carácter',
    'E8': 'Comentario de bloque sin cerrar',
    'E9': 'Múltiples puntos decimales',
    'E10': 'Número mal formado',
    'E11': 'Operador flotante incompleto',
    'E12': 'Literal de conjunto mal formado',
    'E13': 'Literal de archivo mal formado',
    'E14': 'Literal de registro mal formado',
    'E15': 'Literal de arreglo mal formado',
    'E16': 'Identificador mal formado',
    'E17': 'Identificador demasiado largo',
    'E18': 'Delimitador PolloCrudo sin cerrar',
    'E19': 'PolloAsado sin apertura',
    'E20': 'Delimitadores de estructuras de control incompletos',
    'E21': 'Palabra reservada mal escrita',
    'E22': 'Palabra reservada en contexto incorrecto',
    'E23': 'Operador de coerción incompleto',
    'E24': 'Operador de acceso incompleto',
    'E25': 'Error de lectura de archivo',
    'E26': 'Fin de archivo inesperado',
    'E27': 'Buffer overflow'
}

# Mapa inverso para buscar por lexema
PALABRAS_RESERVADAS = {}
for clave, valor in TIPOS_TOKEN.items():
    # Excluir símbolos y tipos genéricos de token
    if not (valor.startswith('+') or valor.startswith('-') or valor.startswith('*') or 
            valor.startswith('/') or valor.startswith('%') or valor.startswith('>') or 
            valor.startswith('<') or valor.startswith('=') or valor.startswith(';') or 
            valor.startswith(',') or valor.startswith('.') or valor.startswith(':') or 
            valor.startswith('(') or valor.startswith(')') or valor.startswith('[') or 
            valor.startswith(']') or valor.startswith('{') or valor.startswith('}') or 
            valor.startswith('@') or valor.startswith('#') or valor in 
            ['IDENTIFICADOR', 'NUMERO_ENTERO', 'NUMERO_DECIMAL', 'CADENA', 'CARACTER', 
             'COMENTARIO', 'EOF', 'ERROR']):
        PALABRAS_RESERVADAS[valor] = clave