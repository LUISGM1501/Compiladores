# /Etapa1/codigo/scanner/automata/identifiers.py
"""
Autómata para identificadores
"""

from .base import Automaton

class IdentifierAutomaton(Automaton):
    """
    Autómata para reconocer identificadores
    """
    def __init__(self):
        """
        Inicializa el autómata para identificadores
        """
        super().__init__()
        
        # Definir estados
        self.estado_inicial = "inicio"
        self.estado_actual = self.estado_inicial
        self.estados_finales = {"identificador"}
        
        # Definir transiciones
        self.transiciones = {
            # Inicio -> Identificador: Letras o guión bajo
            (self.estado_inicial, lambda c: c.isalpha() or c == '_'): "identificador",
            
            # Identificador -> Identificador: Letras, números o guión bajo
            ("identificador", lambda c: c.isalpha() or c.isdigit() or c == '_'): "identificador",
        }
    
    def iniciar(self, caracter):
        """
        Inicia el autómata con el carácter dado
        
        Argumentos:
            caracter: Carácter inicial
        
        Retorna:
            bool: True si el autómata puede iniciar con el carácter, False en caso contrario
        """
        # Verificar si el carácter puede iniciar un identificador (letras o guión bajo)
        if caracter.isalpha() or caracter == '_':
            self.estado_actual = "identificador"
            return True
        
        self.estado_actual = self.estado_inicial
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
        return "IDENTIFICADOR"