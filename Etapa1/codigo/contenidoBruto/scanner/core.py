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
                IdentifierAutomaton(),
                NumberAutomaton(),
                StringAutomaton(),
                OperatorAutomaton(),
                CommentAutomaton()
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
        """
        Encuentra el siguiente token en el archivo
        
        Retorna:
            Token: El siguiente token
        """
        # Ignorar espacios en blanco, tabulaciones y saltos de línea
        self._ignorar_espacios()
        
        # Si llegamos al final del archivo, devolver EOF
        if self.posicion >= len(self.contenido):
            return Token("EOF", "", self.linea, self.columna)
        
        # Obtener el carácter actual
        caracter = self.contenido[self.posicion]
        
        # Inicializar el buffer y posición inicial
        self.buffer = caracter
        linea_inicial = self.linea
        columna_inicial = self.columna
        
        # Intentar reconocer con cada autómata
        for automata in self.automatas:
            self.posicion += 1
            self.columna += 1
            
            if automata.iniciar(caracter):
                estado = automata.estado_actual
                
                # Procesar caracteres según el autómata
                while self.posicion < len(self.contenido) and estado != "error" and not automata.es_estado_final(estado):
                    caracter = self.contenido[self.posicion]
                    self.buffer += caracter
                    estado = automata.transicion(estado, caracter)
                    
                    self.posicion += 1
                    self.columna += 1
                    
                    # Manejo especial para saltos de línea
                    if caracter == '\n':
                        self.linea += 1
                        self.columna = 1
                
                # Si terminamos en estado de aceptación
                if automata.es_estado_final(estado):
                    lexema = self.buffer
                    tipo = automata.obtener_tipo_token(estado, lexema)
                    
                    # Verificar si es una palabra reservada
                    if tipo == "IDENTIFICADOR" and lexema in PALABRAS_RESERVADAS:
                        tipo = PALABRAS_RESERVADAS[lexema]
                    
                    # Crear y devolver el token
                    valor = automata.obtener_valor(estado, lexema)
                    return Token(tipo, lexema, linea_inicial, columna_inicial, valor)
                
                # Si no se reconoció, restaurar posición
                self.posicion -= len(self.buffer)
                self.columna = columna_inicial
                
        # Si ningún autómata reconoció el token, es un error
        caracter = self.contenido[self.posicion]
        self.posicion += 1
        self.columna += 1
        
        # Registrar error y continuar con recuperación
        mensaje = f"Carácter no reconocido: '{caracter}'"
        self.manejador_errores.registrar_error("LEXICO", mensaje, self.linea, self.columna)
        
        # Recuperación de error: devolver un token de error
        return Token("ERROR", caracter, linea_inicial, columna_inicial)
    
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