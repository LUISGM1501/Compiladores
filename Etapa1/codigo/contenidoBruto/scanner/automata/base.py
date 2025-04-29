#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Clase base para los autómatas del scanner de Notch Engine
"""

from typing import Dict, Set, Callable, Union, Any, Tuple, Optional


class Automaton:
    """
    Clase base para los autómatas del scanner
    Cada tipo de token (identificadores, números, strings, etc.) tendrá su propio autómata
    """
    def __init__(self):
        """
        Inicializa un nuevo autómata
        """
        self.estado_inicial = "inicio"
        self.estado_actual = self.estado_inicial
        self.estados_finales: Set[str] = set()
        self.transiciones: Dict[Union[Tuple[str, str], Tuple[str, Callable]], str] = {}
        self.error_handlers: Dict[str, Dict[str, Tuple[str, str]]] = {}
        self.token_validations: Dict[str, Callable] = {}
    
    def iniciar(self, caracter: str) -> bool:
        """
        Inicia el autómata con el carácter dado
        
        Argumentos:
            caracter: Carácter inicial
        
        Retorna:
            bool: True si el autómata puede iniciar con el carácter, False en caso contrario
        """
        # Método a ser implementado por las subclases
        raise NotImplementedError("El método 'iniciar' debe ser implementado por las subclases")
    
    def transicion(self, estado: str, caracter: str) -> str:
        """
        Realiza una transición desde el estado actual con el carácter dado
        
        Argumentos:
            estado: Estado actual
            caracter: Carácter para la transición
        
        Retorna:
            str: Nuevo estado después de la transición, o "error" si no hay transición válida
        """
        # Buscar transición específica para el carácter exacto
        if (estado, caracter) in self.transiciones:
            return self.transiciones[(estado, caracter)]
        
        # Buscar transición para rangos de caracteres (usando funciones de condición)
        for (estado_origen, condicion), estado_destino in self.transiciones.items():
            if estado_origen == estado and callable(condicion) and condicion(caracter):
                return estado_destino
        
        # Si no hay transición válida, verificar si hay un manejador de error para este estado
        if estado in self.error_handlers:
            for cond, (nuevo_estado, _) in self.error_handlers[estado].items():
                if cond == caracter or (callable(cond) and cond(caracter)):
                    return nuevo_estado
        
        # Si no hay transición ni manejador de error, retornamos "error"
        return "error"
    
    def obtener_error(self, estado: str, caracter: str) -> Optional[Tuple[str, str]]:
        """
        Obtiene el código y mensaje de error para un estado y carácter que causó error
        
        Argumentos:
            estado: Estado actual
            caracter: Carácter que causó el error
        
        Retorna:
            Optional[Tuple[str, str]]: Tupla (código, mensaje) o None si no hay error definido
        """
        if estado in self.error_handlers:
            for cond, (_, error_info) in self.error_handlers[estado].items():
                if cond == caracter or (callable(cond) and cond(caracter)):
                    return error_info
        return None
    
    def es_estado_final(self, estado: str) -> bool:
        """
        Verifica si el estado dado es un estado final
        
        Argumentos:
            estado: Estado a verificar
        
        Retorna:
            bool: True si es estado final, False en caso contrario
        """
        return estado in self.estados_finales
    
    def obtener_tipo_token(self, estado: str, lexema: str) -> str:
        """
        Obtiene el tipo de token para el estado final y lexema dados
        
        Argumentos:
            estado: Estado final
            lexema: Lexema reconocido
        
        Retorna:
            str: Tipo de token
        """
        # Método a ser implementado por las subclases
        raise NotImplementedError("El método 'obtener_tipo_token' debe ser implementado por las subclases")
    
    def validar_token(self, estado: str, lexema: str) -> Optional[Tuple[str, str]]:
        """
        Realiza validaciones adicionales sobre el token reconocido
        
        Argumentos:
            estado: Estado final
            lexema: Lexema reconocido
        
        Retorna:
            Optional[Tuple[str, str]]: Tupla (código, mensaje) si hay error, None si es válido
        """
        if estado in self.token_validations:
            return self.token_validations[estado](lexema)
        return None
    
    def obtener_valor(self, estado: str, lexema: str) -> Any:
        """
        Obtiene el valor semántico para el estado final y lexema dados
        
        Argumentos:
            estado: Estado final
            lexema: Lexema reconocido
        
        Retorna:
            any: Valor semántico del token
        """
        # Por defecto, no hay valor semántico
        return None
    
    def reset(self) -> None:
        """
        Reinicia el autómata a su estado inicial
        """
        self.estado_actual = self.estado_inicial