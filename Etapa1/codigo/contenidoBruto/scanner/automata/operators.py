# /Etapa1/codigo/scanner/automata/operators.py
"""
Autómata para operadores
"""

from .base import Automaton

class OperatorAutomaton(Automaton):
    """
    Autómata para reconocer operadores y símbolos
    """
    def __init__(self):
        """
        Inicializa el autómata para operadores
        """
        super().__init__()
        
        # Definir estados
        self.estado_inicial = "inicio"
        self.estado_actual = self.estado_inicial
        self.estados_finales = {
            # Operadores aritméticos básicos
            "suma", "resta", "multiplicacion", "division", "modulo", "doble_slash",
            
            # Operadores para flotantes (Ghast)
            "colon_plus", "colon_minus", "colon_mult", "colon_div", "colon_mod",
            
            # Operadores de comparación
            "mayor_que", "menor_que", "mayor_igual", "menor_igual",
            
            # Asignaciones
            "igual", "suma_igual", "resta_igual", "mult_igual", "div_igual", "mod_igual",
            
            # Delimitadores y símbolos especiales
            "parentesis_abre", "parentesis_cierra",
            "corchete_abre", "corchete_cierra",
            "llave_abre", "llave_cierra",
            "punto_y_coma", "coma", "punto", "dos_puntos",
            "arroba", "hash", "hash_doble", "flecha"
        }
        
        # Definir transiciones
        self.transiciones = {
            # Operadores aritméticos básicos
            (self.estado_inicial, '+'): "suma",
            (self.estado_inicial, '-'): "resta",
            (self.estado_inicial, '*'): "multiplicacion",
            (self.estado_inicial, '/'): "division",
            ("division", '/'): "doble_slash",
            (self.estado_inicial, '%'): "modulo",
            
            # Operadores flotantes (precedidos por :)
            (self.estado_inicial, ':'): "colon",
            ("colon", '+'): "colon_plus",
            ("colon", '-'): "colon_minus",
            ("colon", '*'): "colon_mult",
            ("colon", '/'): "colon_div_inicio",
            ("colon_div_inicio", '/'): "colon_div",
            ("colon", '%'): "colon_mod",
            
            # Operadores de comparación
            (self.estado_inicial, '>'): "mayor_que",
            (self.estado_inicial, '<'): "menor_que",
            ("mayor_que", '='): "mayor_igual",
            ("menor_que", '='): "menor_igual",
            
            # Asignaciones combinadas
            (self.estado_inicial, '='): "igual",
            ("suma", '='): "suma_igual",
            ("resta", '='): "resta_igual",
            ("multiplicacion", '='): "mult_igual",
            ("division", '='): "div_igual",
            ("modulo", '='): "mod_igual",
            
            # Delimitadores
            (self.estado_inicial, '('): "parentesis_abre",
            (self.estado_inicial, ')'): "parentesis_cierra",
            (self.estado_inicial, '['): "corchete_abre",
            (self.estado_inicial, ']'): "corchete_cierra",
            (self.estado_inicial, '{'): "llave_abre",
            (self.estado_inicial, '}'): "llave_cierra",
            (self.estado_inicial, ';'): "punto_y_coma",
            (self.estado_inicial, ','): "coma",
            (self.estado_inicial, '.'): "punto",
            (self.estado_inicial, ':'): "dos_puntos",
            
            # Símbolos especiales
            (self.estado_inicial, '@'): "arroba",
            (self.estado_inicial, '#'): "hash",
            ("hash", '#'): "hash_doble",
            
            # Flecha para definiciones de tipos y funciones
            ("resta", '>'): "flecha",
        }
    
    def iniciar(self, caracter):
        """
        Inicia el autómata con el carácter dado
        
        Argumentos:
            caracter: Carácter inicial
        
        Retorna:
            bool: True si el autómata puede iniciar con el carácter, False en caso contrario
        """
        # Caracteres que pueden iniciar un operador
        operadores_inicio = '+-*/:%><=[]{()}.,;:#@'
        
        if caracter in operadores_inicio:
            # Actualizar estado según el carácter inicial
            for (estado, cond), nuevo_estado in self.transiciones.items():
                if estado == self.estado_inicial and (cond == caracter or (callable(cond) and cond(caracter))):
                    self.estado_actual = nuevo_estado
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
        # Mapeo de estados a tipos de token
        mapa_tipos = {
            # Operadores aritméticos básicos
            "suma": "SUMA",
            "resta": "RESTA",
            "multiplicacion": "MULTIPLICACION",
            "division": "DIVISION",
            "doble_slash": "DIVISION_ENTERA",
            "modulo": "MODULO",
            
            # Operadores flotantes
            "colon_plus": "SUMA_FLOTANTE",
            "colon_minus": "RESTA_FLOTANTE",
            "colon_mult": "MULTIPLICACION_FLOTANTE",
            "colon_div": "DIVISION_FLOTANTE",
            "colon_mod": "MODULO_FLOTANTE",
            
            # Operadores de comparación
            "mayor_que": "MAYOR_QUE",
            "menor_que": "MENOR_QUE",
            "mayor_igual": "MAYOR_IGUAL",
            "menor_igual": "MENOR_IGUAL",
            
            # Asignaciones
            "igual": "IGUAL",
            "suma_igual": "SUMA_IGUAL",
            "resta_igual": "RESTA_IGUAL",
            "mult_igual": "MULTIPLICACION_IGUAL",
            "div_igual": "DIVISION_IGUAL",
            "mod_igual": "MODULO_IGUAL",
            
            # Delimitadores
            "parentesis_abre": "PARENTESIS_ABRE",
            "parentesis_cierra": "PARENTESIS_CIERRA",
            "corchete_abre": "CORCHETE_ABRE",
            "corchete_cierra": "CORCHETE_CIERRA",
            "llave_abre": "LLAVE_ABRE",
            "llave_cierra": "LLAVE_CIERRA",
            "punto_y_coma": "PUNTO_Y_COMA",
            "coma": "COMA",
            "punto": "PUNTO",
            "dos_puntos": "DOS_PUNTOS",
            
            # Símbolos especiales
            "arroba": "ARROBA",
            "hash": "HASH",
            "hash_doble": "HASH_DOBLE",
            "flecha": "FLECHA"
        }
        
        return mapa_tipos.get(estado, "ERROR")