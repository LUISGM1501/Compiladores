#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Autómata para reconocer identificadores y palabras reservadas en Notch Engine
"""

from .base import Automaton
from ..tokens import PALABRAS_RESERVADAS


class IdentifierAutomaton(Automaton):
    """
    Autómata para reconocer identificadores y palabras reservadas en Notch Engine
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
        
        # Máxima longitud de identificadores
        self.max_identifier_length = 64
        
        # Definir transiciones
        self.transiciones = {
            # Un identificador empieza con letra o guion bajo
            (self.estado_inicial, lambda c: c.isalpha() or c == '_'): "identificador",
            
            # Un identificador puede contener letras, dígitos o guiones bajos
            ("identificador", lambda c: c.isalnum() or c == '_'): "identificador",
        }
        
        # Definir manejadores de error (CORREGIDO)
        self.error_handlers = {
            # Error si un identificador comienza con número
            ("inicio", lambda c: c.isdigit()): 
                ("error", ("E16", "Identificador mal formado: no puede comenzar con dígito")),
        }
        
        # Definir validaciones adicionales para tokens
        self.token_validations = {
            "identificador": self._validar_identificador
        }
    
    def iniciar(self, caracter: str) -> bool:
        """
        Inicia el autómata con el carácter dado
        
        Argumentos:
            caracter: Carácter inicial
        
        Retorna:
            bool: True si el autómata puede iniciar con el carácter, False en caso contrario
        """
        # Un identificador debe comenzar con una letra o guion bajo
        if caracter.isalpha() or caracter == '_':
            self.estado_actual = "identificador"
            return True
        
        return False
    
    def _validar_identificador(self, lexema: str):
        """
        Valida que un identificador cumpla con las reglas del lenguaje
        
        Argumentos:
            lexema: Lexema a validar
        
        Retorna:
            Optional[Tuple[str, str]]: Tupla (código, mensaje) si hay error, None si es válido
        """
        # Verificar longitud máxima
        if len(lexema) > self.max_identifier_length:
            return ("E17", f"Identificador demasiado largo (máximo {self.max_identifier_length} caracteres)")
        
        # Verificar que comienza con letra o guion bajo
        if not (lexema[0].isalpha() or lexema[0] == '_'):
            return ("E16", "Identificador mal formado: debe comenzar con letra o guion bajo")
        
        # Verificar que solo contiene caracteres válidos
        if not all(c.isalnum() or c == '_' for c in lexema):
            return ("E16", "Identificador mal formado: contiene caracteres no válidos")
        
        return None
    
    def obtener_tipo_token(self, estado: str, lexema: str) -> str:
        """
        Obtiene el tipo de token para el estado final y lexema dados
        
        Argumentos:
            estado: Estado final
            lexema: Lexema reconocido
        
        Retorna:
            str: Tipo de token
        """
        # Verificar si es una palabra reservada
        if lexema in PALABRAS_RESERVADAS:
            return PALABRAS_RESERVADAS[lexema]
        
        # Si no es una palabra reservada, es un identificador
        return "IDENTIFICADOR"
    
    def obtener_valor(self, estado: str, lexema: str):
        """
        Obtiene el valor semántico del token
        
        Argumentos:
            estado: Estado final
            lexema: Lexema reconocido
        
        Retorna:
            str: El lexema como valor
        """
        return lexema