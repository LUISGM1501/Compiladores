# /Etapa1/codigo/scanner/core.py
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Núcleo del scanner para el lenguaje MC
"""

from .tokens import Token, TIPOS_TOKEN, PALABRAS_RESERVADAS
from .automata.base import Automaton
from .automata.identifiers import IdentifierAutomaton
from .automata.numbers import NumberAutomaton
from .automata.strings import StringAutomaton
from .automata.operators import OperatorAutomaton
from .automata.comments import CommentAutomaton
from .error_handling import ErrorHandler

class Scanner:
    """
    Clase principal del scanner
    """
    def __init__(self, nombre_archivo, manejador_errores):
        """
        Inicializa el scanner
        
        Argumentos:
            nombre_archivo: Nombre del archivo fuente a escanear
            manejador_errores: Manejador de errores para recuperación de errores
        """
        self.nombre_archivo = nombre_archivo
        self.manejador_errores = manejador_errores
        self.archivo = None
        self.contenido = ""
        self.posicion = 0
        self.linea = 1
        self.columna = 1
        self.buffer = ""
        self.automatas = []
        self.estado_actual = None
        self.token_actual = None
        self.token_siguiente = None
    
    def inicializar_scanner(self):
        """
        Inicializa el scanner, abre el archivo y prepara los autómatas
        """
        try:
            # Abrir archivo
            self.archivo = open(self.nombre_archivo, 'r', encoding='utf-8')
            self.contenido = self.archivo.read()
            
            # Inicializar autómatas
            self.automatas = [
                CommentAutomaton(),  # Primero comentarios
                StringAutomaton(),   # Luego strings
                NumberAutomaton(),   # Después números
                OperatorAutomaton(), # Operadores
                IdentifierAutomaton() # Finalmente identificadores
            ]
            
            # Cargar el primer token
            self.token_siguiente = self._siguiente_token()
            
        except Exception as e:
            self.manejador_errores.registrar_error("SCANNER", f"Error al inicializar scanner: {str(e)}", self.linea, self.columna)
            raise e
    
    def finalizar_scanner(self):
        """
        Finaliza el scanner y cierra el archivo
        """
        if self.archivo:
            self.archivo.close()
    
    def deme_token(self):
        """
        Retorna el token actual y avanza al siguiente token
        
        Retorna:
            Token: El token actual
        """
        self.token_actual = self.token_siguiente
        self.token_siguiente = self._siguiente_token()
        return self.token_actual
    
    def tome_token(self):
        """
        Retorna el token actual sin avanzar al siguiente token
        
        Retorna:
            Token: El token actual
        """
        return self.token_actual
    
    def _siguiente_token(self):
        self._ignorar_espacios()
        
        if self.posicion >= len(self.contenido):
            return Token("EOF", "", self.linea, self.columna)
        
        # Guardar posición inicial
        inicio_linea = self.linea
        inicio_col = self.columna
        
        # Probar cada autómata en orden
        for automata in self.automatas:
            # Configurar estado temporal
            temp_pos = self.posicion
            temp_linea = self.linea
            temp_col = self.columna
            lexema = ""
            
            if automata.iniciar(self.contenido[temp_pos]):
                estado = automata.estado_actual
                lexema += self.contenido[temp_pos]
                temp_pos += 1
                if self.contenido[temp_pos-1] == '\n':
                    temp_linea += 1
                    temp_col = 1
                else:
                    temp_col += 1
                
                while temp_pos < len(self.contenido):
                    next_char = self.contenido[temp_pos]
                    new_state = automata.transicion(estado, next_char)

                    if new_state == "error":
                        break
                    
                    estado = new_state
                    lexema += next_char
                    temp_pos += 1
                    
                    if next_char == '\n':
                        temp_linea += 1
                        temp_col = 1
                    else:
                        temp_col += 1

                # Después del while, fuera del bucle:
                if automata.es_estado_final(estado):
                    # Actualizar posición real
                    self.posicion = temp_pos
                    self.linea = temp_linea
                    self.columna = temp_col
                    
                    tipo = automata.obtener_tipo_token(estado, lexema)
                    if tipo == "IDENTIFICADOR" and lexema in PALABRAS_RESERVADAS:
                        tipo = PALABRAS_RESERVADAS[lexema]
                    
                    valor = automata.obtener_valor(estado, lexema)
                    return Token(tipo, lexema, inicio_linea, inicio_col, valor)

        
        # Manejo de error
        error_char = self.contenido[self.posicion]
        self.posicion += 1
        self.columna += 1
        
        self.manejador_errores.registrar_error(
            "LEXICO", 
            f"Carácter no reconocido: '{error_char}'", 
            inicio_linea, 
            inicio_col
        )
        return Token("ERROR", error_char, inicio_linea, inicio_col)

    def _ignorar_espacios(self):
        """
        Avanza la posición ignorando espacios en blanco y saltos de línea
        """
        while self.posicion < len(self.contenido):
            caracter = self.contenido[self.posicion]
            
            if caracter.isspace():
                if caracter == '\n':
                    self.linea += 1
                    self.columna = 1
                else:
                    self.columna += 1
                self.posicion += 1
            else:
                break
    
    def deme_caracter(self):
        """
        Devuelve el carácter actual y avanza a la siguiente posición
        
        Retorna:
            str: El carácter actual
        """
        if self.posicion >= len(self.contenido):
            return None
        
        caracter = self.contenido[self.posicion]
        self.posicion += 1
        
        if caracter == '\n':
            self.linea += 1
            self.columna = 1
        else:
            self.columna += 1
        
        return caracter
    
    def tome_caracter(self):
        """
        Devuelve el carácter actual sin avanzar la posición
        
        Retorna:
            str: El carácter actual
        """
        if self.posicion >= len(self.contenido):
            return None
        
        return self.contenido[self.posicion]