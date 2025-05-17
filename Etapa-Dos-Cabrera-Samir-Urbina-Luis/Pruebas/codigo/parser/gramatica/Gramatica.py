"""
Compilador Notch Engine

Estudiantes: Cabrera Samir y Urbina Luis

Archivo: Gramatica.py

Breve Descripcion: Archivo principal de gramatica generado por GikGram, traducido
por los estudiantes.
"""

# Módulo equivalente al paquete Java
# El equivalente a package Gramatica; en Python sería organizar los archivos
# en un directorio llamado Gramatica

from .GTablaParsing import GTablaParsing
from .GLadosDerechos import GLadosDerechos
from .GNombresTerminales import GNombresTerminales


class Gramatica:
    """
    Esta clase contiene:
    - Constantes necesarias para el driver de parsing
    - Constantes con las rutinas semánticas
    - Y los métodos necesarios para el driver de parsing
    """
    # Esta es la única clase que se accede fuera del paquete Gramatica

    # Constante que contiene el código de familia del terminal de fin de archivo
    MARCA_DERECHA = 133

    # Constante que contiene el número del no-terminal inicial
    # (el primer no-terminal que aparece en la gramática)
    NO_TERMINAL_INICIAL = 134

    # Constante que contiene el número máximo de columnas que tiene los lados derechos
    MAX_LADO_DER = 9

    # Constante que contiene el número máximo de follows
    MAX_FOLLOWS = 48

    # Constantes con las rutinas semánticas
    # NO SE DETECTARON SÍMBOLOS SEMÁNTICOS EN LA GRAMÁTICA

    @staticmethod
    def esTerminal(numSimbolo):
        """
        Método esTerminal
            Devuelve true si el símbolo es un terminal
            o false de lo contrario
        @param numSimbolo
            Número de símbolo
        """
        return (0 <= numSimbolo <= 133)

    @staticmethod
    def esNoTerminal(numSimbolo):
        """
        Método esNoTerminal
            Devuelve true si el símbolo es un no-terminal
            o false de lo contrario
        @param numSimbolo
            Número de símbolo
        """
        return (134 <= numSimbolo <= 211)

    @staticmethod
    def esSimboloSemantico(numSimbolo):
        """
        Método esSimboloSemantico
            Devuelve true si el símbolo es un símbolo semántico
            (incluyendo los símbolos de generación de código)
            o false de lo contrario
        @param numSimbolo
            Número de símbolo
        """
        return (212 <= numSimbolo <= 211)

    @staticmethod
    def getTablaParsing(numNoTerminal, numTerminal):
        """
        Método getTablaParsing
            Devuelve el número de regla contenida en la tabla de parsing
        @param numNoTerminal
            Número del no-terminal
        @param numTerminal
            Número del terminal
        """
        return GTablaParsing.getTablaParsing(numNoTerminal, numTerminal)

    @staticmethod
    def getLadosDerechos(numRegla, numColumna):
        """
        Método getLadosDerechos
            Obtiene un símbolo del lado derecho de la regla
        @param numRegla
            Número de regla
        @param numColumna
            Número de columna
        """
        return GLadosDerechos.getLadosDerechos(numRegla, numColumna)

    @staticmethod
    def getNombresTerminales(numTerminal):
        """
        Método getNombresTerminales
            Obtiene el nombre del terminal
        @param numTerminal
            Número del terminal
        """
        return GNombresTerminales.getNombresTerminales(numTerminal)

    @staticmethod
    def getTablaFollows(numNoTerminal, numColumna):

        from .GTablaFollows import GTablaFollows
        """
        Método getTablaFollows
            Obtiene el número de terminal del follow del no-terminal
        @param numNoTerminal
            Número de no-terminal
        @param numColumna
            Número de columna
        """
        return GTablaFollows.getTablaFollows(numNoTerminal, numColumna)

# Nota: Las clases referenciadas (GTablaParsing, GLadosDerechos, 
# GNombresTerminales, GTablaFollows) deberían definirse en 
# archivos separados dentro del mismo paquete/directorio.