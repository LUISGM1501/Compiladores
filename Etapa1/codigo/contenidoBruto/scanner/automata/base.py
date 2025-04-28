# /Etapa1/codigo/scanner/automata/base.py
"""
Clase base para los autómatas del scanner
"""

class Automaton:
    """
    Clase base para los autómatas
    """
    def __init__(self):
        """
        Inicializa un nuevo autómata
        """
        self.estado_actual = None
        self.estados_finales = set()
        self.transiciones = {}
    
    def iniciar(self, caracter):
        """
        Inicia el autómata con el carácter dado
        
        Argumentos:
            caracter: Carácter inicial
        
        Retorna:
            bool: True si el autómata puede iniciar con el carácter, False en caso contrario
        """
        # Método a ser implementado por las subclases
        raise NotImplementedError("El método 'iniciar' debe ser implementado por las subclases")
    
    def transicion(self, estado, caracter):
        """
        Realiza una transición desde el estado actual con el carácter dado
        
        Argumentos:
            estado: Estado actual
            caracter: Carácter para la transición
        
        Retorna:
            str: Nuevo estado después de la transición
        """
        # Buscar transición específica para el carácter
        if (estado, caracter) in self.transiciones:
            return self.transiciones[(estado, caracter)]
        
        # Buscar transición para rangos de caracteres
        for (estado_origen, condicion), estado_destino in self.transiciones.items():
            if estado_origen == estado and callable(condicion) and condicion(caracter):
                return estado_destino
        
        # Si no hay transición, error
        return "error"
    
    def es_estado_final(self, estado):
        """
        Verifica si el estado dado es un estado final
        
        Argumentos:
            estado: Estado a verificar
        
        Retorna:
            bool: True si es estado final, False en caso contrario
        """
        return estado in self.estados_finales
    
    def obtener_tipo_token(self, estado, lexema):
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
    
    def obtener_valor(self, estado, lexema):
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