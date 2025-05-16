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
    
    # Lista de tokens que pueden ser valores en declaraciones de constantes
    LITERAL_TOKENS = ["NUMERO_ENTERO", "NUMERO_DECIMAL", "CADENA", "CARACTER", "ON", "OFF"]
    
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
    
    @staticmethod
    def is_in_constant_declaration_context(token_history):
        """
        Determina si estamos en un contexto de declaración de constante
        basado en el historial de tokens.
        """
        if not token_history or len(token_history) < 3:
            return False
        
        # Buscar patrones como "Obsidian Stack id"
        for i in range(len(token_history) - 2):
            if (token_history[i].type == "OBSIDIAN" and 
                token_history[i+1].type in ["STACK", "SPIDER", "RUNE", "TORCH", "CHEST", "BOOK", "GHAST", "SHELF", "ENTITY"] and
                token_history[i+2].type == "IDENTIFICADOR"):
                return True
        
        return False
    
    @staticmethod
    def is_literal_token(token_type):
        """
        Verifica si un tipo de token es un literal.
        """
        return token_type in SpecialTokens.LITERAL_TOKENS
    
    @staticmethod
    def suggest_correction(token, error_msg):
        """
        Sugiere correcciones basadas en errores comunes.
        """
        if "PolloCrudo" in error_msg or "POLLO_CRUDO" in error_msg:
            return "Usa 'PolloCrudo' (con mayúsculas/minúsculas correctas) como palabra clave para abrir un bloque."
        
        if "PolloAsado" in error_msg or "POLLO_ASADO" in error_msg:
            return "Usa 'PolloAsado' (con mayúsculas/minúsculas correctas) como palabra clave para cerrar un bloque."
        
        if token and token.type == "IDENTIFICADOR" and token.lexema.lower() in SpecialTokens.SPECIAL_IDENTIFIERS:
            correct_form = token.lexema.lower()
            if correct_form == "pollocrudo":
                correct_form = "PolloCrudo"
            elif correct_form == "polloasado":
                correct_form = "PolloAsado"
            elif correct_form == "worldsave":
                correct_form = "WorldSave"
            elif correct_form == "worldname":
                correct_form = "WorldName"
            
            return f"¿Querías usar '{correct_form}' como palabra clave?"
        
        return None