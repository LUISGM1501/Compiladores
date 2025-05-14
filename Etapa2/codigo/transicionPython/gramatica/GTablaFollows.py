"""
 * GTablaFollows.py
 *
 * 2025/05/11 13:08:11
 *
 * Archivo generado por GikGram 2.0
 *
 * Copyright © Olminsky 2011 Derechos reservados
 * Reproducción sin fines de lucro permitida
"""


# Parte del módulo Gramatica
from .Gramatica import Gramatica

class GTablaFollows:
    """
    Esta clase contiene la tabla de follows
    y los métodos necesarios para acceder a ella
    """

    # Tabla de follows
    # Contiene los números de los terminales
    # de los follows de cada no-terminal (filas)
    TablaFollows = [
        # <program>
        [Gramatica.MARCA_DERECHA, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        
    ]

    @staticmethod
    def getTablaFollows(numNoTerminal, numColumna):
        """
        Método getTablaFollows
            Obtiene el número de terminal del follow del no-terminal
        @param numNoTerminal
            Número de no-terminal
        @param numColumna
            Número de columna
        """
        return GTablaFollows.TablaFollows[numNoTerminal][numColumna]