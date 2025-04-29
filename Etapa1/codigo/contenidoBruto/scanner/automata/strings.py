#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Autómata para reconocer strings (Spider) y caracteres (Rune) en Notch Engine
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
        
        # Secuencias de escape válidas
        self.valid_escapes = {'n', 't', 'r', '\\', '"', "'"}
        
        # Definir transiciones
        self.transiciones = {
            # Strings (delimitados por comillas dobles)
            (self.estado_inicial, '"'): "string_inicio",
            ("string_inicio", '"'): "string",  # String vacío
            ("string_inicio", lambda c: c != '"' and c != '\n'): "string_contenido",
            ("string_contenido", lambda c: c != '"' and c != '\n' and c != '\\'): "string_contenido",
            ("string_contenido", '"'): "string",
            ("string_contenido", '\\'): "string_escape",
            ("string_escape", lambda c: c in self.valid_escapes): "string_contenido",
            
            # Caracteres (delimitados por comillas simples)
            (self.estado_inicial, "'"): "caracter_inicio",
            ("caracter_inicio", lambda c: c != "'" and c != '\n' and c != '\\'): "caracter_contenido",
            ("caracter_contenido", "'"): "caracter",
            ("caracter_inicio", '\\'): "caracter_escape",
            ("caracter_escape", lambda c: c in self.valid_escapes): "caracter_contenido"
        }
        
        # Definir manejadores de error - CORREGIDO para evitar usar variables en f-strings
        self.error_handlers = {
            # Errores de strings
            "string_inicio": {
                '\n': ("error", ("E3", "String sin cerrar: salto de línea no permitido dentro de un string"))
            },
            "string_contenido": {
                '\n': ("error", ("E3", "String sin cerrar: salto de línea no permitido dentro de un string"))
            },
            "string_escape": {
                lambda c: c not in self.valid_escapes: ("error", ("E6", "Secuencia de escape inválida"))
            },
            
            # Errores de caracteres
            "caracter_inicio": {
                '\n': ("error", ("E4", "Carácter sin cerrar: salto de línea no permitido dentro de un carácter")),
                "'": ("error", ("E5", "Literal de carácter vacío"))
            },
            "caracter_contenido": {
                '\n': ("error", ("E4", "Carácter sin cerrar: salto de línea no permitido dentro de un carácter"))
            },
            "caracter_escape": {
                lambda c: c not in self.valid_escapes: ("error", ("E6", "Secuencia de escape inválida"))
            }
        }
        
        # Definir validaciones adicionales para tokens
        self.token_validations = {
            "caracter": self._validar_caracter
        }
    
    def iniciar(self, caracter: str) -> bool:
        """
        Inicia el autómata con el carácter dado
        
        Argumentos:
            caracter: Carácter inicial
        
        Retorna:
            bool: True si el autómata puede iniciar con el carácter, False en caso contrario
        """
        # Un string comienza con comillas dobles
        if caracter == '"':
            self.estado_actual = "string_inicio"
            return True
        
        # Un carácter comienza con comillas simples
        elif caracter == "'":
            self.estado_actual = "caracter_inicio"
            return True
        
        return False
    
    def _validar_caracter(self, lexema: str):
        """
        Valida que un literal de carácter contenga exactamente un carácter
        
        Argumentos:
            lexema: Lexema a validar
        
        Retorna:
            Optional[Tuple[str, str]]: Tupla (código, mensaje) si hay error, None si es válido
        """
        # Eliminar las comillas y procesar secuencias de escape
        contenido = lexema[1:-1]
        
        # Reemplazar secuencias de escape por un solo carácter
        contenido = contenido.replace('\\n', '\n').replace('\\t', '\t').replace('\\r', '\r')
        contenido = contenido.replace('\\"', '"').replace("\\'", "'").replace('\\\\', '\\')
        
        # Verificar que solo hay un carácter
        if len(contenido) > 1:
            return ("E7", "Múltiples caracteres en literal de carácter")
        
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
        if estado == "string":
            return "CADENA"
        elif estado == "caracter":
            return "CARACTER"
        else:
            return "ERROR"
    
    def obtener_valor(self, estado: str, lexema: str):
        """
        Obtiene el valor semántico del token
        
        Argumentos:
            estado: Estado final
            lexema: Lexema reconocido
        
        Retorna:
            str o char: El valor del string o carácter, con secuencias de escape procesadas
        """
        if estado == "string":
            # Eliminar las comillas y procesar secuencias de escape
            valor = lexema[1:-1]
            valor = valor.replace('\\n', '\n').replace('\\t', '\t').replace('\\r', '\r')
            valor = valor.replace('\\"', '"').replace("\\'", "'").replace('\\\\', '\\')
            return valor
        
        elif estado == "caracter":
            # Eliminar las comillas y procesar secuencias de escape
            valor = lexema[1:-1]
            valor = valor.replace('\\n', '\n').replace('\\t', '\t').replace('\\r', '\r')
            valor = valor.replace('\\"', '"').replace("\\'", "'").replace('\\\\', '\\')
            return valor
        
        return None