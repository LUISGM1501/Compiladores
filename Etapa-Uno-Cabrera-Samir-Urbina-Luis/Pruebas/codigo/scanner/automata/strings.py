# /Etapa1/codigo/scanner/automata/strings.py
"""
Autómata para strings y caracteres
"""

from .base import Automaton

class StringAutomaton(Automaton):
    """
    Autómata para reconocer strings (Spider) y caracteres (Rune)
    """
    def __init__(self):
        """
        Inicializa el autómata para strings y caracteres
        """
        super().__init__()
        
        # Definir estados
        self.estado_inicial = "inicio"
        self.estado_actual = self.estado_inicial
        self.estados_finales = {"string", "caracter"}
        
        # Definir transiciones
        self.transiciones = {
            # Strings
            (self.estado_inicial, '"'): "string_inicio",
            ("string_inicio", lambda c: c != '"' and c != '\n'): "string_contenido",
            ("string_inicio", '"'): "string",  # String vacío
            ("string_contenido", lambda c: c != '"' and c != '\n'): "string_contenido",
            ("string_contenido", '"'): "string",
            
            # Caracteres
            (self.estado_inicial, "'"): "caracter_inicio",
            ("caracter_inicio", lambda c: c != "'" and c != '\n'): "caracter_contenido",
            ("caracter_contenido", "'"): "caracter",
            
            # Secuencias de escape
            ("string_contenido", '\\'): "string_escape",
            ("string_escape", lambda c: c in 'ntr"\\\''): "string_contenido",
            
            ("caracter_inicio", '\\'): "caracter_escape",
            ("caracter_escape", lambda c: c in 'ntr"\\\''): "caracter_contenido",
        }
    
    def iniciar(self, caracter):
        """
        Inicia el autómata con el carácter dado
        
        Argumentos:
            caracter: Carácter inicial
        
        Retorna:
            bool: True si el autómata puede iniciar con el carácter, False en caso contrario
        """
        if caracter == '"':
            self.estado_actual = "string_inicio"
            return True
        elif caracter == "'":
            self.estado_actual = "caracter_inicio"
            return True
        
        return False
    
    def obtener_tipo_token(self, estado, lexema):
        """
        Obtiene el tipo de token para el estado final y lexema dados
        
        Argumentos:
            estado: Estado final
            lexema: Lexema reconocido
        
        Retorna:
            str: Tipo de token
        """
        if estado == "string":
            return "CADENA"
        elif estado == "caracter":
            return "CARACTER"
        else:
            return "ERROR"
    
    def obtener_valor(self, estado, lexema):
        """
        Obtiene el valor semántico para el estado final y lexema dados
        
        Argumentos:
            estado: Estado final
            lexema: Lexema reconocido
        
        Retorna:
            any: Valor semántico del token
        """
        if estado == "string":
            # Eliminar las comillas dobles y procesar secuencias de escape
            return lexema[1:-1].replace('\\n', '\n').replace('\\t', '\t').replace('\\"', '"').replace('\\\\', '\\')
        elif estado == "caracter":
            # Eliminar las comillas simples y procesar secuencias de escape
            valor = lexema[1:-1].replace('\\n', '\n').replace('\\t', '\t').replace("\\'", "'").replace('\\\\', '\\')
            return valor
        else:
            return None