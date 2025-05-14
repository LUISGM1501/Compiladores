"""
 * GLadosDerechos.py
 *
 * 2025/05/11 13:08:11
 *
 * Archivo generado por GikGram 2.0
 *
 * Copyright © Olminsky 2011 Derechos reservados
 * Reproducción sin fines de lucro permitida
"""

# Parte del módulo Gramatica

class GLadosDerechos:
    """
    Esta clase contiene la tabla de lados derechos
    y los métodos necesarios para acceder a ella
    """
    
    # Tabla de lados derechos
    # Contiene el lado derecho de las reglas de la gramática
    LadosDerechos = [
        [9,135,112,91,0,-1,-1,-1,-1],
        [135,136,-1,-1,-1,-1,-1,-1,-1],
        [-1,-1,-1,-1,-1,-1,-1,-1,-1],
        [137,1,-1,-1,-1,-1,-1,-1,-1],
        [140,2,-1,-1,-1,-1,-1,-1,-1],
        [142,3,-1,-1,-1,-1,-1,-1,-1],
    ]

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
        return GLadosDerechos.LadosDerechos[numRegla][numColumna]