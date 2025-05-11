from .base import Automaton

class IdentifierAutomaton(Automaton):
    """
    Autómata para reconocer identificadores y palabras reservadas
    Versión corregida que no divide los lexemas
    """
    def __init__(self):
        super().__init__()
        self.estado_inicial = "inicio"
        self.estado_actual = self.estado_inicial
        self.estados_finales = {"identificador"}
        
        # Transiciones más flexibles
        self.transiciones = {
            ("inicio", lambda c: c.isalpha() or c == '_'): "identificador",
            ("identificador", lambda c: c.isalnum() or c == '_'): "identificador"
        }
    
    def iniciar(self, caracter):
        """Inicia el reconocimiento con el primer carácter"""
        if caracter.isalpha() or caracter == '_':
            self.estado_actual = "identificador"
            return True
        return False
    
    def transicion(self, estado, caracter):
        """Transición extendida para capturar lexemas completos"""
        for (estado_orig, condicion), estado_dest in self.transiciones.items():
            if estado_orig == estado and condicion(caracter):
                return estado_dest
        return "error"
    
    def obtener_tipo_token(self, estado, lexema):
        """Determina si es palabra reservada o identificador"""
        return "IDENTIFICADOR"
    
    def obtener_valor(self, estado, lexema):
        """Devuelve el lexema completo"""
        return lexema