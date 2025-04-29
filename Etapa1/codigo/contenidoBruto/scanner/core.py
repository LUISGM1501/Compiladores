#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Núcleo del scanner para el lenguaje Notch Engine
"""

from typing import List, Optional, Dict, Set, Tuple
import os

from .tokens import Token, TIPOS_TOKEN, PALABRAS_RESERVADAS, ERRORES_LEXICOS
from .automata.base import Automaton
from .automata.identifiers import IdentifierAutomaton
from .automata.numbers import NumberAutomaton
from .automata.strings import StringAutomaton
from .automata.operators import OperatorAutomaton
from .automata.comments import CommentAutomaton
from .automata.basic_symbols import BasicSymbolAutomaton
from .error_handling import ErrorHandler


class Scanner:
    """
    Clase principal del scanner para Notch Engine
    """
    def __init__(self, nombre_archivo: str, manejador_errores: ErrorHandler):
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
        self.buffer = []
        self.automatas = []
        self.estado_actual = None
        self.token_actual = None
        self.token_siguiente = None
        self.tokens = []
        
        # Control del modo de pánico para recuperación de errores
        self.modo_panico = False
        self.delimitadores_recuperacion = {';', '\n', '}', ')', ']'}
        
        # Control de bloques PolloCrudo-PolloAsado para detección de errores
        self.pollo_crudo_count = 0
        
        # Control de contexto de palabras reservadas
        self.secciones_validas = []
        self.seccion_actual = None
        
        # Límites para detección de buffer overflow
        self.max_buffer_size = 4096
    
    def inicializar_scanner(self):
        """
        Inicializa el scanner, abre el archivo y prepara los autómatas
        """
        try:
            # Abrir archivo
            with open(self.nombre_archivo, 'r', encoding='utf-8') as f:
                self.contenido = f.read()
            
            # Inicializar autómatas
            self.automatas = [
                BasicSymbolAutomaton(),  # Primero los símbolos básicos
                CommentAutomaton(),      # Luego comentarios
                StringAutomaton(),       # Strings
                NumberAutomaton(),       # Números
                OperatorAutomaton(),     # Operadores complejos
                IdentifierAutomaton()    # Finalmente identificadores
            ]
            
            # Escanear todos los tokens
            self._escanear_tokens()
            
            # Verificar errores de estructura al final del archivo
            self._verificar_estructura_final()
            
        except Exception as e:
            self.manejador_errores.registrar_error(
                "E25", "SCANNER", 
                f"Error al inicializar scanner: {str(e)}", 
                self.linea, self.columna
            )
            raise e
    
    def finalizar_scanner(self):
        """
        Finaliza el scanner y libera recursos
        """
        pass  # No hay recursos que liberar ya que el archivo se cierra automáticamente
    
    def deme_token(self):
        """
        Retorna el siguiente token disponible
        
        Retorna:
            Token: El siguiente token
        """
        if not self.tokens:
            return Token("EOF", "", self.linea, self.columna)
        
        return self.tokens.pop(0)
    
    def tome_token(self):
        """
        Observa el siguiente token sin consumirlo
        
        Retorna:
            Token: El siguiente token sin consumirlo
        """
        if not self.tokens:
            return Token("EOF", "", self.linea, self.columna)
        
        return self.tokens[0]
    
    def _escanear_tokens(self):
        """
        Escanea todos los tokens del archivo fuente con manejo especial para símbolos básicos
        """
        while self.posicion < len(self.contenido):
            # Ignorar espacios en blanco
            if self._ignorar_espacios():
                continue
            
            # Posición inicial del token para reportar errores
            linea_inicio = self.linea
            columna_inicio = self.columna
            
            # Caracteres especiales que deberían ser reconocidos directamente
            caracter_actual = self.contenido[self.posicion]
            simbolos_especiales = {
                '.': "PUNTO",
                ',': "COMA",
                ';': "PUNTO_Y_COMA",
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
            
            # Si es un comentario (empieza con $)
            if caracter_actual == '$':
                # Intentar procesar como comentario primero
                token_reconocido = False
                for automata in self.automatas:
                    if isinstance(automata, CommentAutomaton) and automata.iniciar(caracter_actual):
                        # Procesar con el autómata de comentarios
                        temp_pos = self.posicion
                        temp_linea = self.linea
                        temp_columna = self.columna
                        
                        automata.reset()
                        lexema = self.contenido[temp_pos]
                        estado_actual = automata.estado_actual
                        temp_pos += 1
                        
                        # Actualizar posición temporal
                        if lexema == '\n':
                            temp_linea += 1
                            temp_columna = 1
                        else:
                            temp_columna += 1
                        
                        # Continuar mientras podamos avanzar
                        while temp_pos < len(self.contenido):
                            car = self.contenido[temp_pos]
                            nuevo_estado = automata.transicion(estado_actual, car)
                            if nuevo_estado == "error":
                                break
                            
                            estado_actual = nuevo_estado
                            lexema += car
                            temp_pos += 1
                            
                            # Actualizar posición
                            if car == '\n':
                                temp_linea += 1
                                temp_columna = 1
                            else:
                                temp_columna += 1
                        
                        # Verificar si estamos en un estado final
                        if automata.es_estado_final(estado_actual):
                            token_reconocido = True
                            
                            # Obtener tipo y valor del token
                            tipo_token = automata.obtener_tipo_token(estado_actual, lexema)
                            valor_token = automata.obtener_valor(estado_actual, lexema)
                            
                            # Actualizar posición real
                            self.posicion = temp_pos
                            self.linea = temp_linea
                            self.columna = temp_columna
                            
                            # No agregamos los comentarios a la lista de tokens
                            break
                
                # Si no se reconoció como comentario, procesarlo como símbolo simple
                if not token_reconocido:
                    token = Token("DOLAR", caracter_actual, linea_inicio, columna_inicio)
                    self.tokens.append(token)
                    self.posicion += 1
                    self.columna += 1
            
            # Si es un carácter especial reconocido, procesarlo directamente
            elif caracter_actual in simbolos_especiales:
                tipo_token = simbolos_especiales[caracter_actual]
                token = Token(tipo_token, caracter_actual, linea_inicio, columna_inicio)
                self.tokens.append(token)
                self.posicion += 1
                self.columna += 1
            
            # Si es un dígito, procesarlo como número
            elif caracter_actual.isdigit() or (caracter_actual == '-' and self.posicion + 1 < len(self.contenido) and self.contenido[self.posicion + 1].isdigit()):
                # Procesar número
                lexema = caracter_actual
                self.posicion += 1
                self.columna += 1
                
                # Leer dígitos para la parte entera
                while self.posicion < len(self.contenido) and self.contenido[self.posicion].isdigit():
                    lexema += self.contenido[self.posicion]
                    self.posicion += 1
                    self.columna += 1
                
                # Verificar si hay parte decimal
                if self.posicion < len(self.contenido) and self.contenido[self.posicion] == '.':
                    lexema += self.contenido[self.posicion]
                    self.posicion += 1
                    self.columna += 1
                    
                    # Leer dígitos para la parte decimal
                    tiene_decimal = False
                    while self.posicion < len(self.contenido) and self.contenido[self.posicion].isdigit():
                        lexema += self.contenido[self.posicion]
                        self.posicion += 1
                        self.columna += 1
                        tiene_decimal = True
                    
                    if tiene_decimal:
                        # Es un número decimal
                        token = Token("NUMERO_DECIMAL", lexema, linea_inicio, columna_inicio, float(lexema))
                    else:
                        # Es un número entero con punto (incorrecto)
                        token = Token("ERROR", lexema, linea_inicio, columna_inicio, None, "E10")
                        self.manejador_errores.registrar_error(
                            "E10", "LEXICO", 
                            "Número mal formado: después del punto decimal debe haber dígitos", 
                            linea_inicio, columna_inicio, lexema
                        )
                else:
                    # Es un número entero
                    token = Token("NUMERO_ENTERO", lexema, linea_inicio, columna_inicio, int(lexema))
                
                self.tokens.append(token)
            
            # Si es una comilla doble, procesarlo como string
            elif caracter_actual == '"':
                # Procesar string
                lexema = caracter_actual
                self.posicion += 1
                self.columna += 1
                
                token_valido = True
                # Leer hasta encontrar otra comilla doble o fin de línea
                while self.posicion < len(self.contenido) and self.contenido[self.posicion] != '"' and self.contenido[self.posicion] != '\n':
                    lexema += self.contenido[self.posicion]
                    self.posicion += 1
                    self.columna += 1
                
                # Verificar si terminó correctamente
                if self.posicion < len(self.contenido) and self.contenido[self.posicion] == '"':
                    lexema += self.contenido[self.posicion]
                    self.posicion += 1
                    self.columna += 1
                    token = Token("CADENA", lexema, linea_inicio, columna_inicio, lexema[1:-1])
                else:
                    # String sin cerrar
                    token = Token("ERROR", lexema, linea_inicio, columna_inicio, None, "E3")
                    self.manejador_errores.registrar_error(
                        "E3", "LEXICO", 
                        "String sin cerrar", 
                        linea_inicio, columna_inicio, lexema
                    )
                    token_valido = False
                
                self.tokens.append(token)
            
            # Si es una letra o guión bajo, procesarlo como identificador o palabra reservada
            elif caracter_actual.isalpha() or caracter_actual == '_':
                # Procesar identificador o palabra reservada
                lexema = caracter_actual
                self.posicion += 1
                self.columna += 1
                
                # Leer hasta encontrar un carácter que no sea letra, dígito o guión bajo
                while self.posicion < len(self.contenido) and (self.contenido[self.posicion].isalnum() or self.contenido[self.posicion] == '_'):
                    lexema += self.contenido[self.posicion]
                    self.posicion += 1
                    self.columna += 1
                
                # Verificar si es una palabra reservada
                if lexema in PALABRAS_RESERVADAS:
                    tipo_token = PALABRAS_RESERVADAS[lexema]
                    token = Token(tipo_token, lexema, linea_inicio, columna_inicio)
                else:
                    # Es un identificador
                    token = Token("IDENTIFICADOR", lexema, linea_inicio, columna_inicio, lexema)
                
                self.tokens.append(token)
            
            # Si no se reconoce, reportar error y avanzar
            else:
                # Carácter no reconocido
                self.manejador_errores.registrar_error(
                    "E1", "LEXICO", 
                    f"Carácter no reconocido: '{caracter_actual}'", 
                    linea_inicio, columna_inicio, caracter_actual
                )
                
                # Crear token de error
                token = Token("ERROR", caracter_actual, linea_inicio, columna_inicio, None, "E1")
                self.tokens.append(token)
                
                # Avanzar al siguiente carácter
                self.posicion += 1
                self.columna += 1
        
        # Agregar token EOF al final
        self.tokens.append(Token("EOF", "", self.linea, self.columna))
    def _procesar_token_especial(self, tipo_token, lexema, linea, columna, valor, error):
        """
        Procesa tokens que requieren manejo especial (PolloCrudo, PolloAsado, etc.)
        
        Retorna:
            Token: El token procesado
        """
        # Crear el token base
        token = Token(tipo_token, lexema, linea, columna, valor)
        
        # Si hay error de validación, registrarlo
        if error:
            codigo, mensaje = error
            self.manejador_errores.registrar_error(
                codigo, "LEXICO", 
                mensaje, 
                linea, columna, lexema
            )
            token.error = codigo
        
        # Procesar tokens especiales
        if tipo_token == "POLLOCRUDO":
            self.pollo_crudo_count += 1
        elif tipo_token == "POLLOASADO":
            if self.pollo_crudo_count > 0:
                self.pollo_crudo_count -= 1
            else:
                # Error: PolloAsado sin PolloCrudo
                self.manejador_errores.registrar_error(
                    "E19", "LEXICO", 
                    "PolloAsado sin apertura correspondiente", 
                    linea, columna, lexema
                )
                token.error = "E19"
        
        # Procesar palabras reservadas en contexto
        self._verificar_palabra_reservada_contexto(tipo_token, lexema, linea, columna)
        
        return token
    
    def _verificar_palabra_reservada_contexto(self, tipo_token, lexema, linea, columna):
        """
        Verifica que las palabras reservadas se usen en el contexto correcto
        """
        # Secciones principales del programa
        secciones_programa = {
            "WORLDNAME": "programa",
            "BEDROCK": "constantes",
            "RESOURCEPACK": "tipos",
            "INVENTORY": "variables",
            "RECIPE": "prototipos",
            "CRAFTINGTABLE": "rutinas",
            "SPAWNPOINT": "main",
            "WORLDSAVE": "fin"
        }
        
        # Actualizar sección actual
        if tipo_token in secciones_programa:
            self.seccion_actual = secciones_programa[tipo_token]
            self.secciones_validas.append(self.seccion_actual)
        
        # Verificar que las palabras reservadas específicas estén en la sección correcta
        # Esto es simplemente un ejemplo y se puede expandir según las reglas del lenguaje
        if tipo_token == "OBSIDIAN" and self.seccion_actual != "constantes":
            self.manejador_errores.registrar_error(
                "E22", "LEXICO", 
                "Obsidian solo puede utilizarse en la sección Bedrock", 
                linea, columna, lexema
            )
        elif tipo_token == "ANVIL" and self.seccion_actual != "tipos":
            self.manejador_errores.registrar_error(
                "E22", "LEXICO", 
                "Anvil solo puede utilizarse en la sección ResourcePack", 
                linea, columna, lexema
            )
    
    def _verificar_estructura_final(self):
        """
        Verifica errores de estructura al final del archivo
        """
        # Verificar PolloCrudo sin cerrar
        if self.pollo_crudo_count > 0:
            self.manejador_errores.registrar_error(
                "E18", "LEXICO", 
                f"Hay {self.pollo_crudo_count} PolloCrudo sin cerrar al final del archivo", 
                self.linea, self.columna
            )
    
    def _ignorar_espacios(self) -> bool:
        """
        Ignora espacios en blanco y devuelve True si avanzó la posición
        
        Retorna:
            bool: True si se ignoraron espacios, False en caso contrario
        """
        if self.posicion >= len(self.contenido):
            return False
        
        if self.contenido[self.posicion].isspace():
            char = self.contenido[self.posicion]
            # Avanzar posición
            self.posicion += 1
            
            # Actualizar línea y columna
            if char == '\n':
                self.linea += 1
                self.columna = 1
            else:
                self.columna += 1
            
            return True
        
        return False