"""
* TokenMap.py
*
* 2025/05/11
*
* Mapeo de tokens a códigos numéricos para el parser
* Contiene mejoras para manejar casos especiales como DOBLE_DOS_PUNTOS
"""

class TokenMap:
    # Mapeo de tipos de token a códigos numéricos de terminal
    MAP = {
        "WORLD_NAME": 0,
        "BEDROCK": 1,
        "RESOURCE_PACK": 2,
        "INVENTORY": 3,
        "RECIPE": 4,
        "CRAFTING_TABLE": 5,
        "SPAWN_POINT": 6,
        "OBSIDIAN": 7,
        "ANVIL": 8,
        "WORLD_SAVE": 9,
        "STACK": 10,
        "RUNE": 11,
        "SPIDER": 12,
        "TORCH": 13,
        "CHEST": 14,
        "BOOK": 15,
        "GHAST": 16,
        "SHELF": 17,
        "ENTITY": 18,
        "REF": 19,
        "ON": 20,
        "OFF": 21,
        "POLLO_CRUDO": 22,
        "POLLO_ASADO": 23,
        "REPEATER": 24,
        "CRAFT": 25,
        "TARGET": 26,
        "HIT": 27,
        "MISS": 28,
        "JUKEBOX": 29,
        "DISC": 30,
        "SILENCE": 31,
        "SPAWNER": 32,
        "EXHAUSTED": 33,
        "WALK": 34,
        "SET": 35,
        "TO": 36,
        "STEP": 37,
        "WITHER": 38,
        "CREEPER": 39,
        "ENDER_PEARL": 40,
        "RAGEQUIT": 41,
        "SPELL": 42,
        "RITUAL": 43,
        "RESPAWN": 44,
        "IS_ENGRAVED": 45,
        "IS_INSCRIBED": 46,
        "ETCH_UP": 47,
        "ETCH_DOWN": 48,
        "AND": 49,
        "OR": 50,
        "NOT": 51,
        "XOR": 52,
        "BIND": 53,
        "HASH": 54,
        "FROM": 55,
        "EXCEPT": 56,
        "SEEK": 57,
        "ADD": 58,
        "DROP": 59,
        "FEED": 60,
        "MAP": 61,
        "BIOM": 62,
        "VOID": 63,
        "UNLOCK": 64,
        "LOCK": 65,
        "MAKE": 66,
        "GATHER": 67,
        "FORGE": 68,
        "TAG": 69,
        "IS": 70,
        "IS_NOT": 71,
        "HOPPER_STACK": 72,
        "HOPPER_RUNE": 73,
        "HOPPER_SPIDER": 74,
        "HOPPER_TORCH": 75,
        "HOPPER_CHEST": 76,
        "HOPPER_GHAST": 77,
        "DROPPER_STACK": 78,
        "DROPPER_RUNE": 79,
        "DROPPER_SPIDER": 80,
        "DROPPER_TORCH": 81,
        "DROPPER_CHEST": 82,
        "DROPPER_GHAST": 83,
        "CHUNK": 84,
        "SOULSAND": 85,
        "MAGMA": 86,
        "NUMERO_ENTERO": 87,
        "NUMERO_DECIMAL": 88,
        "CADENA": 89,
        "CARACTER": 90,
        "IDENTIFICADOR": 91,
        "DOBLE_IGUAL": 92,
        "MENOR_QUE": 93,
        "MAYOR_QUE": 94,
        "MENOR_IGUAL": 95,
        "MAYOR_IGUAL": 96,
        "IGUAL": 97,
        "SUMA": 98,
        "RESTA": 99,
        "MULTIPLICACION": 100,
        "DIVISION": 101,
        "MODULO": 102,
        "PARENTESIS_ABRE": 103,
        "PARENTESIS_CIERRA": 104,
        "CORCHETE_ABRE": 105,
        "CORCHETE_CIERRA": 106,
        "LLAVE_ABRE": 107,
        "LLAVE_CIERRA": 108,
        "PUNTO_Y_COMA": 109,
        "COMA": 110,
        "PUNTO": 111,
        "DOS_PUNTOS": 112,
        "ARROBA": 113,
        "BARRA": 114,
        "FLECHA": 115,
        "SUMA_IGUAL": 116,
        "RESTA_IGUAL": 117,
        "MULTIPLICACION_IGUAL": 118,
        "DIVISION_IGUAL": 119,
        "MODULO_IGUAL": 120,
        "RETURN": 121,
        "SUMA_FLOTANTE": 122,
        "RESTA_FLOTANTE": 123,
        "MULTIPLICACION_FLOTANTE": 124,
        "DIVISION_FLOTANTE": 125,
        "MODULO_FLOTANTE": 126,
        "SUMA_FLOTANTE_IGUAL": 127,
        "RESTA_FLOTANTE_IGUAL": 128,
        "MULTIPLICACION_FLOTANTE_IGUAL": 129,
        "DIVISION_FLOTANTE_IGUAL": 130,
        "MODULO_FLOTANTE_IGUAL": 131,
        "COERCION": 132,
        "EOF": 133,
        "COMENTARIO": -1  # Token ignorado
    }

    # Manejo inverso para facilitar la depuración y algunos casos especiales
    REVERSE_MAP = None

    @staticmethod
    def init_reverse_map():
        """Inicializa el mapeo inverso para facilitar la consulta por código"""
        if TokenMap.REVERSE_MAP is None:
            TokenMap.REVERSE_MAP = {}
            for token_type, code in TokenMap.MAP.items():
                if code != -1:  # No incluir tokens ignorados
                    TokenMap.REVERSE_MAP[code] = token_type

    @staticmethod
    def get_token_code(token_type):
        """
        Obtiene el código numérico para un tipo de token
        
        Args:
            token_type: Tipo de token a buscar
            
        Returns:
            Código numérico del token o -1 si no se encuentra
        """
        # Caso especial: manejo de aliases para casos clave
        if isinstance(token_type, str) and token_type.upper() == "IDENTIFICADOR":
            # Este chequeo es redundante pero seguro
            return TokenMap.MAP.get("IDENTIFICADOR", -1)
        
        if hasattr(token_type, 'type') and token_type.type == "IDENTIFICADOR":
            lex = token_type.lexema.lower()
            if lex == "pollocrudo":
                return TokenMap.MAP["POLLO_CRUDO"]
            elif lex == "polloasado":
                return TokenMap.MAP["POLLO_ASADO"]
            elif lex == "worldsave":
                return TokenMap.MAP["WORLD_SAVE"]
        
        return TokenMap.MAP.get(token_type, -1)

    @staticmethod
    def get_token_name(token_code):
        """
        Obtiene el nombre del tipo de token a partir de su código
        
        Args:
            token_code: Código numérico del token
            
        Returns:
            Nombre del tipo de token o None si no se encuentra
        """
        TokenMap.init_reverse_map()
        return TokenMap.REVERSE_MAP.get(token_code)