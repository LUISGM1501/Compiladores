#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Autómata para reconocer comentarios en Notch Engine
"""

from .base import Automaton


class CommentAutomaton(Automaton):
    """
    Autómata para reconocer comentarios de línea ($$) y de bloque ($* ... *$)
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
            (self.estado_inicial, '$'): "dolar",
            
            # Comentarios de línea ($$)
            ("dolar", '$'): "comentario_linea_inicio",
            ("comentario_linea_inicio", lambda c: c != '\n'): "comentario_linea_contenido",
            ("comentario_linea_contenido", lambda c: c != '\n'): "comentario_linea_contenido",
            ("comentario_linea_contenido", '\n'): "comentario_linea",
            
            # Comentarios de bloque ($* ... *$)
            ("dolar", '*'): "comentario_bloque_inicio",
            ("comentario_bloque_inicio", lambda c: c != '*'): "comentario_bloque_contenido",
            ("comentario_bloque_contenido", lambda c: c != '*'): "comentario_bloque_contenido",
            ("comentario_bloque_contenido", '*'): "comentario_bloque_asterisco",
            ("comentario_bloque_asterisco", lambda c: c != '$' and c != '*'): "comentario_bloque_contenido",
            ("comentario_bloque_asterisco", '*'): "comentario_bloque_asterisco",
            ("comentario_bloque_asterisco", '$'): "comentario_bloque"
        }
        
        # Definir manejadores de error (CORREGIDO)
        self.error_handlers = {
            # Error para símbolos no reconocidos después de $
            "dolar": {
                # Usamos una condición simple sin f-string
                lambda c: c != '$' and c != '*': ("error", ("E1", "Carácter no reconocido después de '$'"))
            }
        }
    
    def iniciar(self, caracter: str) -> bool:
        """
        Inicia el autómata con el carácter dado
        
        Argumentos:
            caracter: Carácter inicial
        
        Retorna:
            bool: True si el autómata puede iniciar con el carácter, False en caso contrario
        """
        # Un comentario siempre comienza con el carácter $
        if caracter == '$':
            self.estado_actual = "dolar"
            return True
        
        return False
    
    def obtener_tipo_token(self, estado: str, lexema: str) -> str:
        """
        Obtiene el tipo de token para el estado final y lexema dados
        
        Argumentos:
            estado: Estado final
            lexema: Lexema reconocido
        
        Retorna:
            str: Tipo de token
        """
        return "COMENTARIO"
    
    def obtener_valor(self, estado: str, lexema: str):
        """
        Obtiene el valor semántico del token
        
        Argumentos:
            estado: Estado final
            lexema: Lexema reconocido
        
        Retorna:
            str: El contenido del comentario sin los delimitadores
        """
        if estado == "comentario_linea":
            # Eliminar los $$ al inicio
            return lexema[2:].strip()
        
        elif estado == "comentario_bloque":
            # Eliminar los $* al inicio y *$ al final
            return lexema[2:-2].strip()
        
        return None
    
    def validar_final_archivo(self, estado: str) -> tuple:
        """
        Valida si un comentario puede terminar correctamente al final del archivo
        
        Argumentos:
            estado: Estado actual
        
        Retorna:
            tuple: (bool, str, str) donde el primer elemento indica si es válido,
                  y los otros dos elementos son el código y mensaje de error si no es válido
        """
        # Comentario de línea puede terminar con el fin de archivo
        if estado in ["comentario_linea_contenido"]:
            return (True, None, None)
        
        # Comentario de bloque no puede terminar con el fin de archivo
        elif estado in ["comentario_bloque_inicio", "comentario_bloque_contenido", "comentario_bloque_asterisco"]:
            return (False, "E8", "Comentario de bloque sin cerrar")
        
        return (True, None, None)