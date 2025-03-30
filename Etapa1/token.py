"""
Clase Token para el Analizador Léxico de EnderLang
Autores: Samir Cabrera, Luis Urbina
Fecha de entrega: 10/04/2025

Este archivo define la clase Token que representa una unidad léxica del lenguaje.
"""

class Token:
    """
    Representa un token del lenguaje.
    Cada token contiene información sobre su tipo, lexema, línea y columna donde aparece.
    """
    
    # Definición de tipos de token (estos serán actualizados cuando se tenga la definición completa del lenguaje)
    # Tokens básicos que no dependen del lenguaje específico
    TK_IDENTIFICADOR = 'IDENTIFICADOR'
    TK_ENTERO = 'ENTERO'
    TK_FLOTANTE = 'FLOTANTE'
    TK_CARACTER = 'CARACTER'
    TK_STRING = 'STRING'
    TK_COMENTARIO = 'COMENTARIO'
    TK_ERROR = 'ERROR'
    TK_EOF = 'EOF'  # Fin de archivo
    
    # Familias de tokens que requerirán detalles del lenguaje específico
    TK_PALABRA_RESERVADA = 'PALABRA_RESERVADA'
    TK_OPERADOR = 'OPERADOR'
    TK_SIMBOLO = 'SIMBOLO'
    
    def __init__(self, tipo, lexema, linea, columna):
        """
        Constructor de la clase Token
        
        Parámetros:
            tipo (str): El tipo de token (uno de los valores TK_*)
            lexema (str): La secuencia de caracteres que forma el token
            linea (int): Número de línea donde aparece el token
            columna (int): Número de columna donde comienza el token
        """
        self.tipo = tipo
        self.lexema = lexema
        self.linea = linea
        self.columna = columna
    
    def __str__(self):
        """
        Representación en cadena de texto del token
        """
        return f"Token({self.tipo}, '{self.lexema}', línea={self.linea}, columna={self.columna})"
    
    def __repr__(self):
        """
        Representación oficial del token (para depuración)
        """
        return self.__str__()