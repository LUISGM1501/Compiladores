# /Etapa1/codigo/scanner/automata/comments.py
"""
Autómata para comentarios
"""

from .base import Automaton

class CommentAutomaton(Automaton):
    """
    Autómata para reconocer comentarios
    """
    def __init__(self):
        """
        Inicializa el autómata para comentarios
        """
        super().__init__()
        
        # Definir estados
        self.estado_inicial = "inicio"
        self.estado_actual = self.estado_inicial
        self.estados_finales = {"comentario_linea", "comentario_bloque"}
        
        # Definir transiciones
        self.transiciones = {
            # Inicio de comentarios
            (self.estado_inicial, '$'): "dollar",
            
            # Comentario de línea ($$)
            ("dollar", '$'): "comentario_linea_inicio",
            ("comentario_linea_inicio", lambda c: c != '\n'): "comentario_linea_contenido",
            ("comentario_linea_contenido", lambda c: c != '\n'): "comentario_linea_contenido",
            ("comentario_linea_contenido", '\n'): "comentario_linea",
            
            # Comentario de bloque ($* ... *$)
            ("dollar", '*'): "comentario_bloque_inicio",
            ("comentario_bloque_inicio", lambda c: c != '*'): "comentario_bloque_contenido",
            ("comentario_bloque_contenido", lambda c: c != '*'): "comentario_bloque_contenido",
            ("comentario_bloque_contenido", '*'): "comentario_bloque_asterisco",
            ("comentario_bloque_asterisco", lambda c: c != '$' and c != '*'): "comentario_bloque_contenido",
            ("comentario_bloque_asterisco", '*'): "comentario_bloque_asterisco",
            ("comentario_bloque_asterisco", '$'): "comentario_bloque",
        }
    
    def iniciar(self, caracter):
        """
        Inicia el autómata con el carácter dado
        
        Argumentos:
            caracter: Carácter inicial
        
        Retorna:
            bool: True si el autómata puede iniciar con el carácter, False en caso contrario
        """
        if caracter == '$':
            self.estado_actual = "dollar"
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
        return "COMENTARIO"