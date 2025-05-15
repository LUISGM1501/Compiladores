"""
* special_tokens.py
*
* 2025/05/11
*
* Manejador de casos especiales de tokens para el parser de Notch-Engine
* Especialmente útil para manejar PolloCrudo/PolloAsado y otros identificadores especiales
"""

class SpecialTokens:
    """
    Esta clase proporciona utilidades para manejar casos especiales de tokens
    que requieren consideración especial en el parser.
    """
    
    # Mapeo de identificadores especiales a sus equivalentes en palabras clave
    SPECIAL_IDENTIFIERS = {
        "pollocrudo": "POLLO_CRUDO",
        "polloasado": "POLLO_ASADO",
        "worldsave": "WORLD_SAVE",
        "worldname": "WORLD_NAME",
        "resourcepack": "RESOURCE_PACK",
        "craftingtable": "CRAFTING_TABLE",
        "spawnpoint": "SPAWN_POINT"
    }
    
    # Códigos numéricos correspondientes a estos tokens especiales
    TOKEN_CODES = {
        "POLLO_CRUDO": 22,
        "POLLO_ASADO": 23,
        "WORLD_SAVE": 9,
        "WORLD_NAME": 0,
        "RESOURCE_PACK": 2,
        "CRAFTING_TABLE": 5,
        "SPAWN_POINT": 6
    }
    
    @staticmethod
    def is_special_identifier(token):
        """
        Verifica si un token es un identificador especial que debe ser
        tratado como un token específico en ciertos contextos.
        
        Args:
            token: El token a verificar
            
        Returns:
            True si es un identificador especial, False en caso contrario
        """
        if token.type != "IDENTIFICADOR":
            return False
        
        return token.lexema.lower() in SpecialTokens.SPECIAL_IDENTIFIERS
    
    @staticmethod
    def get_special_token_type(token):
        """
        Obtiene el tipo especial de token que correspondería a este identificador.
        
        Args:
            token: El token identificador a convertir
            
        Returns:
            El tipo de token especial correspondiente, o None si no es especial
        """
        if not SpecialTokens.is_special_identifier(token):
            return None
        
        return SpecialTokens.SPECIAL_IDENTIFIERS.get(token.lexema.lower())
    
    @staticmethod
    def get_special_token_code(token):
        """
        Obtiene el código numérico del token especial correspondiente a este identificador.
        
        Args:
            token: El token identificador a convertir
            
        Returns:
            El código numérico del token especial, o -1 si no es especial
        """
        special_type = SpecialTokens.get_special_token_type(token)
        if not special_type:
            return -1
        
        return SpecialTokens.TOKEN_CODES.get(special_type, -1)

    # Utilidades para manejo de DOBLE_DOS_PUNTOS
    @staticmethod
    def handle_double_colon(token, token_history=None):
        """
        Determina si un token DOBLE_DOS_PUNTOS debe ser manejado como uno o dos DOS_PUNTOS
        basado en el contexto (historial de tokens).
        
        Args:
            token: El token DOBLE_DOS_PUNTOS actual
            token_history: Lista de tokens anteriores para contexto (opcional)
            
        Returns:
            Un valor que indica cómo manejar el token:
            1 = Tratar como un solo DOS_PUNTOS
            2 = Tratar como dos DOS_PUNTOS consecutivos
        """
        # En nuestro caso, siempre lo manejamos como dos DOS_PUNTOS
        # Esto podría ser más sofisticado dependiendo del contexto
        return 2
    
    # Utilidades para manejo de literales en declaraciones
    @staticmethod
    def is_declaration_context(token_history):
        """
        Determina si estamos en un contexto de declaración de variable o constante
        basado en el historial de tokens.
        
        Args:
            token_history: Lista de tokens anteriores para contexto
            
        Returns:
            True si estamos en un contexto de declaración, False en caso contrario
        """
        if not token_history or len(token_history) < 3:
            return False
        
        # Verificar patrones comunes de declaración
        # Ejemplo: STACK contador = ...
        if token_history[-3].type in ["STACK", "SPIDER", "RUNE", "TORCH", "CHEST", "BOOK", "GHAST", "SHELF", "ENTITY"] and \
           token_history[-2].type == "IDENTIFICADOR" and \
           token_history[-1].type == "IGUAL":
            return True
            
        # Ejemplo: Obsidian Stack MAX_VALOR ...
        if token_history[-3].type == "OBSIDIAN" and \
           token_history[-2].type in ["STACK", "SPIDER", "RUNE", "TORCH", "CHEST", "BOOK", "GHAST", "SHELF", "ENTITY"] and \
           token_history[-1].type == "IDENTIFICADOR":
            return True
        
        return False
    @staticmethod
    def suggest_correction(token, mensaje_error):
        """
        Sugiere una corrección basada en un token y un mensaje de error.
        
        Args:
            token: El token actual
            mensaje_error: El mensaje de error actual
            
        Returns:
            Sugerencia de corrección o None si no hay sugerencia
        """
        if token.type == "IDENTIFICADOR":
            lexema_lower = token.lexema.lower()
            
            # Sugerencias para palabras clave comunes
            if lexema_lower == "pollocrudo":
                return "Sugerencia: Utilice 'PolloCrudo' como palabra clave, no como identificador."
            elif lexema_lower == "polloasado":
                return "Sugerencia: Utilice 'PolloAsado' como palabra clave, no como identificador."
            elif lexema_lower == "worldsave":
                return "Sugerencia: Utilice 'worldSave' para terminar el programa."
                
        # Sugerencias para errores comunes de sintaxis
        if "DOS_PUNTOS" in mensaje_error and "esperaba" in mensaje_error:
            return "Sugerencia: Verifique la sintaxis de declaración, puede faltar un símbolo de puntuación."
        
        return None