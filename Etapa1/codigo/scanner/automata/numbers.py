"""
Autómata para números
"""

from .base import Automaton

class NumberAutomaton(Automaton):
    """
    Autómata para reconocer números (enteros y decimales)
    """
    def __init__(self):
        """
        Inicializa el autómata para números
        """
        super().__init__()
        
        # Definir estados
        self.estado_inicial = "inicio"
        self.estado_actual = self.estado_inicial
        self.estados_finales = {"entero", "decimal"}
        
        # Definir transiciones
        self.transiciones = {
            # Inicio -> Entero: Dígitos
            (self.estado_inicial, lambda c: c.isdigit()): "entero",
            
            # Entero -> Entero: Dígitos
            ("entero", lambda c: c.isdigit()): "entero",
            
            # Entero -> Punto: Punto decimal
            ("entero", lambda c: c == '.'): "punto",
            
            # Punto -> Decimal: Dígitos
            ("punto", lambda c: c.isdigit()): "decimal",
            
            # Decimal -> Decimal: Dígitos
            ("decimal", lambda c: c.isdigit()): "decimal",
        }
    
    def iniciar(self, caracter):
        """
        Inicia el autómata con el carácter dado
        
        Argumentos:
            caracter: Carácter inicial
        
        Retorna:
            bool: True si el autómata puede iniciar con el carácter, False en caso contrario
        """
        # Verificar si el carácter puede iniciar un número
        if caracter.isdigit():
            self.estado_actual = "entero"
            return True
        
        return False
    
    def obtener_tipo_token(self, estado, lexema):
        """
        Obtiene el tipo de token para el estado final y lexema dados
        
        Argumentos:
            estado: Estado final
            lexema: Lexema reconocido
        
        Retorna:
            str: Tipo de token
        """
        if estado == "entero":
            return "NUMERO_ENTERO"
        elif estado == "decimal":
            return "NUMERO_DECIMAL"
        else:
            return "ERROR"
    
    def obtener_valor(self, estado, lexema):
        """
        Obtiene el valor semántico para el estado final y lexema dados
        
        Argumentos:
            estado: Estado final
            lexema: Lexema reconocido
        
        Retorna:
            any: Valor semántico del token
        """
        if estado == "entero":
            return int(lexema)
        elif estado == "decimal":
            return float(lexema)
        else:
            return None