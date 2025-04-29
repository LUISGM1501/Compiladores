#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de manejo de errores para el scanner de Notch Engine
"""

from typing import List, Dict, Optional, Tuple


class Error:
    """
    Clase que representa un error en el compilador
    """
    def __init__(self, codigo: str, tipo: str, mensaje: str, linea: int, columna: int, lexema: str = ""):
        """
        Inicializa un nuevo error
        
        Argumentos:
            codigo: Código de error (E1, E2, etc.)
            tipo: Tipo de error (LEXICO, SINTACTICO, SEMANTICO)
            mensaje: Descripción del error
            linea: Número de línea donde ocurrió el error
            columna: Número de columna donde ocurrió el error
            lexema: Lexema que causó el error (opcional)
        """
        self.codigo = codigo
        self.tipo = tipo
        self.mensaje = mensaje
        self.linea = linea
        self.columna = columna
        self.lexema = lexema
    
    def __str__(self):
        """
        Representación textual del error
        """
        if self.lexema:
            return f"Error {self.codigo}: {self.mensaje} en '{self.lexema}' (línea {self.linea}, columna {self.columna})"
        else:
            return f"Error {self.codigo}: {self.mensaje} (línea {self.linea}, columna {self.columna})"


class ErrorHandler:
    """
    Manejador de errores para recuperación de errores
    """
    def __init__(self):
        """
        Inicializa el manejador de errores
        """
        self.errores: List[Error] = []
        self.max_errores_por_linea = 5  # Límite para evitar cascada de errores
        self.errores_por_linea: Dict[int, int] = {}
        self.errores_consecutivos = 0
        self.limite_errores_consecutivos = 10
    
    def registrar_error(self, codigo: str, tipo: str, mensaje: str, linea: int, columna: int, lexema: str = ""):
        """
        Registra un nuevo error y maneja la recuperación
        
        Argumentos:
            codigo: Código de error (E1, E2, etc.)
            tipo: Tipo de error (LEXICO, SINTACTICO, SEMANTICO)
            mensaje: Descripción del error
            linea: Número de línea donde ocurrió el error
            columna: Número de columna donde ocurrió el error
            lexema: Lexema que causó el error (opcional)
        
        Retorna:
            bool: True si se debe continuar el análisis, False si se debe entrar en modo recuperación
        """
        # Verificar si debemos limitar errores en la misma línea
        if linea in self.errores_por_linea:
            self.errores_por_linea[linea] += 1
            if self.errores_por_linea[linea] > self.max_errores_por_linea:
                # Si hay demasiados errores en la misma línea, añadir solo un mensaje resumen
                if self.errores_por_linea[linea] == self.max_errores_por_linea + 1:
                    self.errores.append(Error(
                        "W1", "ADVERTENCIA", 
                        f"Demasiados errores en esta línea. Se omitirán errores adicionales.",
                        linea, columna
                    ))
                self.errores_consecutivos += 1
                return False
        else:
            self.errores_por_linea[linea] = 1
        
        # Verificar errores consecutivos para prevenir cascada
        if self.errores_consecutivos > self.limite_errores_consecutivos:
            # Entrar en modo de recuperación por pánico
            self.errores.append(Error(
                "W2", "ADVERTENCIA", 
                "Muchos errores consecutivos detectados. Entrando en modo de recuperación.",
                linea, columna
            ))
            self.errores_consecutivos = 0
            return False
        
        # Registrar el error normalmente
        error = Error(codigo, tipo, mensaje, linea, columna, lexema)
        self.errores.append(error)
        print(str(error))
        
        self.errores_consecutivos += 1
        return True
    
    def reset_errores_consecutivos(self):
        """
        Reinicia el contador de errores consecutivos
        """
        self.errores_consecutivos = 0
    
    def hay_errores(self) -> bool:
        """
        Verifica si hay errores registrados
        
        Retorna:
            bool: True si hay errores, False en caso contrario
        """
        return len(self.errores) > 0
    
    def contar_errores(self) -> int:
        """
        Cuenta el número total de errores registrados
        
        Retorna:
            int: Número total de errores
        """
        return len([e for e in self.errores if e.tipo != "ADVERTENCIA"])
    
    def obtener_errores_por_tipo(self) -> Dict[str, int]:
        """
        Agrupa los errores por tipo
        
        Retorna:
            Dict[str, int]: Diccionario con la cantidad de errores por tipo
        """
        resultado = {}
        for error in self.errores:
            if error.tipo not in resultado:
                resultado[error.tipo] = 0
            resultado[error.tipo] += 1
        return resultado
    
    def obtener_resumen(self) -> str:
        """
        Obtiene un resumen de los errores registrados
        
        Retorna:
            str: Resumen de errores
        """
        if not self.errores:
            return "No se encontraron errores."
        
        resumen = f"Total de errores: {self.contar_errores()}\n"
        
        # Contar errores por tipo
        errores_por_tipo = self.obtener_errores_por_tipo()
        
        # Agregar desglose por tipo
        for tipo, cantidad in errores_por_tipo.items():
            resumen += f"  {tipo}: {cantidad}\n"
        
        # Agregar detalle de errores
        resumen += "\nDetalle de errores:\n"
        for i, error in enumerate(self.errores):
            resumen += f"  {i+1}. {error}\n"
        
        return resumen