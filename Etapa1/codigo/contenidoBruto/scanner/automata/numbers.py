#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Autómata para reconocer números (enteros y decimales) en Notch Engine
"""

from .base import Automaton


class NumberAutomaton(Automaton):
    """
    Autómata para reconocer números enteros (Stack) y decimales (Ghast)
    """
    def __init__(self):
        """
        Inicializa el autómata para números
        """
        super().__init__()
        
        # Definir estados
        self.estado_inicial = "inicio"
        self.estado_actual = self.estado_inicial
        self.estados_finales = {"entero", "decimal"}
        
        # Definir transiciones
        self.transiciones = {
            # Manejo del signo negativo
            (self.estado_inicial, '-'): "signo_negativo",
            ("signo_negativo", lambda c: c.isdigit()): "entero",
            
            # Enteros
            (self.estado_inicial, lambda c: c.isdigit()): "entero",
            ("entero", lambda c: c.isdigit()): "entero",
            
            # Punto decimal
            ("entero", '.'): "punto_decimal",
            
            # Parte decimal
            ("punto_decimal", lambda c: c.isdigit()): "decimal",
            ("decimal", lambda c: c.isdigit()): "decimal"
        }
        
        # Definir manejadores de error
        self.error_handlers = {
            # Error si después del punto no hay dígito
            "punto_decimal": {
                lambda c: not c.isdigit(): ("error", ("E10", "Número mal formado: después del punto decimal debe haber dígitos"))
            },
            # Error si después del signo negativo no hay dígito
            "signo_negativo": {
                lambda c: not c.isdigit(): ("error", ("E10", "Número mal formado: después del signo debe haber dígitos"))
            },
            # Error si hay múltiples puntos decimales
            "decimal": {
                '.': ("error", ("E9", "Múltiples puntos decimales"))
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
        # Un número puede comenzar con un dígito o un signo negativo
        if caracter.isdigit():
            self.estado_actual = "entero"
            return True
        elif caracter == '-':
            self.estado_actual = "signo_negativo"
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
        if estado == "entero":
            return "NUMERO_ENTERO"
        elif estado == "decimal":
            return "NUMERO_DECIMAL"
        else:
            return "ERROR"
    
    def obtener_valor(self, estado: str, lexema: str):
        """
        Obtiene el valor semántico del token
        
        Argumentos:
            estado: Estado final
            lexema: Lexema reconocido
        
        Retorna:
            int o float: El valor numérico del lexema
        """
        if estado == "entero":
            return int(lexema)
        elif estado == "decimal":
            return float(lexema)
        else:
            return None