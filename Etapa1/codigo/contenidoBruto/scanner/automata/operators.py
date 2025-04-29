#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Autómata para reconocer operadores y símbolos en Notch Engine
"""

from .base import Automaton


class OperatorAutomaton(Automaton):
    """
    Autómata para reconocer operadores y símbolos
    """
    def __init__(self):
        """
        Inicializa el autómata para operadores
        """
        super().__init__()
        
        # Definir estados
        self.estado_inicial = "inicio"
        self.estado_actual = self.estado_inicial
        self.estados_finales = {
            # Operadores aritméticos
            "suma", "resta", "multiplicacion", "division", "division_entera", "modulo",
            
            # Operadores compuestos de asignación
            "suma_igual", "resta_igual", "multiplicacion_igual", "division_igual", "modulo_igual",
            
            # Operadores de comparación
            "mayor_que", "menor_que", "mayor_igual", "menor_igual",
            
            # Operadores especiales
            "igual", "flecha", "doble_mayor", "arroba", "hash", "hash_hash",
            
            # Operadores flotantes
            "dos_puntos", "colon_suma", "colon_resta", "colon_multiplicacion", 
            "colon_division", "colon_division_entera", "colon_modulo",
            
            # Delimitadores
            "punto_y_coma", "coma", "punto", "dos_puntos_doble",
            "parentesis_abre", "parentesis_cierra",
            "corchete_abre", "corchete_cierra",
            "llave_abre", "llave_cierra",
            
            # Literales especiales
            "llave_colon_abre", "colon_llave_cierra",
            "llave_slash_abre", "slash_llave_cierra"
        }
        
        # Definir transiciones
        self.transiciones = {
            # Operadores aritméticos y de asignación
            (self.estado_inicial, '+'): "suma",
            (self.estado_inicial, '-'): "resta",
            (self.estado_inicial, '*'): "multiplicacion",
            (self.estado_inicial, '/'): "division",
            (self.estado_inicial, '%'): "modulo",
            
            # Operadores compuestos
            ("suma", '='): "suma_igual",
            ("resta", '='): "resta_igual",
            ("multiplicacion", '='): "multiplicacion_igual",
            ("division", '='): "division_igual",
            ("modulo", '='): "modulo_igual",
            ("division", '/'): "division_entera",
            
            # Operadores especiales
            (self.estado_inicial, '='): "igual",
            ("resta", '>'): "flecha",
            (self.estado_inicial, '>'): "mayor_que",
            (self.estado_inicial, '<'): "menor_que",
            ("mayor_que", '='): "mayor_igual",
            ("menor_que", '='): "menor_igual",
            ("mayor_que", '>'): "doble_mayor",
            
            # Operadores de acceso
            (self.estado_inicial, '@'): "arroba",
            (self.estado_inicial, '#'): "hash",
            ("hash", '#'): "hash_hash",
            
            # Operadores para flotantes
            (self.estado_inicial, ':'): "dos_puntos",
            ("dos_puntos", '+'): "colon_suma",
            ("dos_puntos", '-'): "colon_resta",
            ("dos_puntos", '*'): "colon_multiplicacion",
            ("dos_puntos", '/'): "colon_division",
            ("colon_division", '/'): "colon_division_entera",
            ("dos_puntos", '%'): "colon_modulo",
            ("dos_puntos", ':'): "dos_puntos_doble",
            
            # Delimitadores básicos
            (self.estado_inicial, ';'): "punto_y_coma",
            (self.estado_inicial, ','): "coma",
            (self.estado_inicial, '.'): "punto",
            
            # Delimitadores de agrupación
            (self.estado_inicial, '('): "parentesis_abre",
            (self.estado_inicial, ')'): "parentesis_cierra",
            (self.estado_inicial, '['): "corchete_abre",
            (self.estado_inicial, ']'): "corchete_cierra",
            (self.estado_inicial, '{'): "llave_abre",
            (self.estado_inicial, '}'): "llave_cierra",
            
            # Literales especiales (conjuntos, archivos)
            ("llave_abre", ':'): "llave_colon_abre",
            ("dos_puntos", '}'): "colon_llave_cierra",
            ("llave_abre", '/'): "llave_slash_abre",
            ("division", '}'): "slash_llave_cierra"
        }
        
        # Definir manejadores de error (CORREGIDO)
        self.error_handlers = {
            # Error de operador flotante incompleto
            "dos_puntos": {
                lambda c: c not in ['+', '-', '*', '/', '%', ':'] and not c.isspace() and c != '}': 
                    ("error", ("E11", "Operador flotante incompleto"))
            },
            # Error de operador de coerción incompleto
            "doble_mayor": {
                lambda c: not (c.isalpha() or c == '_') and not c.isspace(): 
                    ("error", ("E23", "Operador de coerción incompleto: debe seguir un tipo"))
            },
            # Error de operador de acceso incompleto
            "arroba": {
                lambda c: not (c.isalpha() or c == '_') and not c.isspace(): 
                    ("error", ("E24", "Operador de acceso incompleto: debe seguir un identificador"))
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
        # Ampliamos la lista de caracteres que pueden iniciar un operador
        operadores_inicio = '+-*/%=><@#:;,.()[]{}"\'$_0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        
        if caracter in operadores_inicio:
            # Actualizar estado según el carácter inicial
            for (estado, car), nuevo_estado in self.transiciones.items():
                if estado == self.estado_inicial and car == caracter:
                    self.estado_actual = nuevo_estado
                    return True
            
            # Si no hay una transición específica pero el carácter es válido como inicio
            # de operador, podemos intentar buscarlo como un símbolo simple
            if caracter in '+-*/%=><@#:;,.()[]{}"\'$':
                # Crear un estado temporal para este símbolo
                temp_estado = f"simple_{caracter}"
                if temp_estado not in self.estados_finales:
                    self.estados_finales.add(temp_estado)
                self.estado_actual = temp_estado
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
        # Mapeo de estados a tipos de token
        mapa_tipos = {
            # Operadores aritméticos
            "suma": "SUMA",
            "resta": "RESTA",
            "multiplicacion": "MULTIPLICACION",
            "division": "DIVISION",
            "division_entera": "DIVISION_ENTERA",
            "modulo": "MODULO",
            
            # Operadores compuestos
            "suma_igual": "SUMA_IGUAL",
            "resta_igual": "RESTA_IGUAL",
            "multiplicacion_igual": "MULTIPLICACION_IGUAL",
            "division_igual": "DIVISION_IGUAL",
            "modulo_igual": "MODULO_IGUAL",
            
            # Operadores especiales
            "igual": "IGUAL",
            "flecha": "FLECHA",
            "mayor_que": "MAYOR_QUE",
            "menor_que": "MENOR_QUE",
            "mayor_igual": "MAYOR_IGUAL",
            "menor_igual": "MENOR_IGUAL",
            "doble_mayor": "COERCION",
            
            # Operadores de acceso
            "arroba": "ARROBA",
            "hash": "HASH",
            "hash_hash": "HASH_HASH",
            
            # Operadores para flotantes
            "dos_puntos": "DOS_PUNTOS",
            "colon_suma": "COLON_SUMA",
            "colon_resta": "COLON_RESTA",
            "colon_multiplicacion": "COLON_MULTI",
            "colon_division": "COLON_DIV",
            "colon_division_entera": "COLON_DIV_ENTERA",
            "colon_modulo": "COLON_MODULO",
            "dos_puntos_doble": "DOS_PUNTOS_DOBLE",
            
            # Delimitadores básicos
            "punto_y_coma": "PUNTO_Y_COMA",
            "coma": "COMA",
            "punto": "PUNTO",
            
            # Delimitadores de agrupación
            "parentesis_abre": "PARENTESIS_ABRE",
            "parentesis_cierra": "PARENTESIS_CIERRA",
            "corchete_abre": "CORCHETE_ABRE",
            "corchete_cierra": "CORCHETE_CIERRA",
            "llave_abre": "LLAVE_ABRE",
            "llave_cierra": "LLAVE_CIERRA",
            
            # Literales especiales
            "llave_colon_abre": "LLAVE_COLON_ABRE",
            "colon_llave_cierra": "COLON_LLAVE_CIERRA",
            "llave_slash_abre": "LLAVE_SLASH_ABRE",
            "slash_llave_cierra": "SLASH_LLAVE_CIERRA",
            
            # Agregar mapeos para símbolos simples
            "simple_+": "SUMA",
            "simple_-": "RESTA",
            "simple_*": "MULTIPLICACION",
            "simple_/": "DIVISION",
            "simple_%": "MODULO",
            "simple_=": "IGUAL",
            "simple_>": "MAYOR_QUE",
            "simple_<": "MENOR_QUE",
            "simple_@": "ARROBA",
            "simple_#": "HASH",
            "simple_:": "DOS_PUNTOS",
            "simple_;": "PUNTO_Y_COMA",
            "simple_,": "COMA",
            "simple_.": "PUNTO",
            "simple_(": "PARENTESIS_ABRE",
            "simple_)": "PARENTESIS_CIERRA",
            "simple_[": "CORCHETE_ABRE",
            "simple_]": "CORCHETE_CIERRA",
            "simple_{": "LLAVE_ABRE",
            "simple_}": "LLAVE_CIERRA",
            "simple_\"": "COMILLA_DOBLE",
            "simple_'": "COMILLA_SIMPLE",
            "simple_$": "DOLAR"
        }
        
        return mapa_tipos.get(estado, "ERROR")