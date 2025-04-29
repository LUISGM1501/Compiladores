#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Autómata para reconocer símbolos básicos en Notch Engine
"""

from .base import Automaton


class BasicSymbolAutomaton(Automaton):
    """
    Autómata para reconocer símbolos básicos como puntuación, operadores, etc.
    """
    def __init__(self):
        """
        Inicializa el autómata para símbolos básicos
        """
        super().__init__()
        
        # Definir estados
        self.estado_inicial = "inicio"
        self.estado_actual = self.estado_inicial
        
        # Todos los símbolos que queremos reconocer
        self.simbolos = {
            ',': "COMA",
            ';': "PUNTO_Y_COMA",
            '.': "PUNTO",
            ':': "DOS_PUNTOS",
            '(': "PARENTESIS_ABRE",
            ')': "PARENTESIS_CIERRA",
            '[': "CORCHETE_ABRE",
            ']': "CORCHETE_CIERRA",
            '{': "LLAVE_ABRE",
            '}': "LLAVE_CIERRA",
            '+': "SUMA",
            '-': "RESTA",
            '*': "MULTIPLICACION",
            '/': "DIVISION",
            '%': "MODULO",
            '=': "IGUAL",
            '<': "MENOR_QUE",
            '>': "MAYOR_QUE",
            '@': "ARROBA",
            '$': "DOLAR",
            '#': "HASH",
            '&': "AMPERSAND",
            '|': "PIPE",
            '^': "CARET",
            '~': "TILDE",
            '"': "COMILLA_DOBLE",
            "'": "COMILLA_SIMPLE",
            '`': "BACKTICK",
            '\\': "BACKSLASH",
            '?': "INTERROGACION",
            '!': "EXCLAMACION",
            '_': "GUION_BAJO"
        }
        
        # Agregar cada símbolo a los estados finales
        self.estados_finales = set()
        for simbolo in self.simbolos:
            estado = f"simbolo_{simbolo}"
            self.estados_finales.add(estado)
            # Agregar la transición desde el estado inicial
            self.transiciones[(self.estado_inicial, simbolo)] = estado
    
    def iniciar(self, caracter: str) -> bool:
        """
        Inicia el autómata con el carácter dado
        
        Argumentos:
            caracter: Carácter inicial
        
        Retorna:
            bool: True si el autómata puede iniciar con el carácter, False en caso contrario
        """
        # Verificar si el carácter es uno de nuestros símbolos
        if caracter in self.simbolos:
            self.estado_actual = f"simbolo_{caracter}"
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
        # Extraer el símbolo del nombre del estado
        if estado.startswith("simbolo_") and len(estado) > 8:
            simbolo = estado[8:]  # Extraer el símbolo después de "simbolo_"
            if simbolo in self.simbolos:
                return self.simbolos[simbolo]
        
        return "ERROR"