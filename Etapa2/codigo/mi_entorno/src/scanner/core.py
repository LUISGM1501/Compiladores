# Archivo: /scanner/core.py
"""
Núcleo optimizado del scanner para el lenguaje MC
"""

from .tokens import Token, PALABRAS_RESERVADAS, TokenCategory
from .automata.integrated_automaton import IntegratedAutomaton

class ErrorHandler:
    """Manejador de errores simplificado"""
    
    def __init__(self):
        self.errores = []
    
    def registrar_error(self, tipo, mensaje, linea, columna):
        """Registra un error"""
        self.errores.append({
            'tipo': tipo,
            'mensaje': mensaje,
            'linea': linea,
            'columna': columna
        })
        print(f"[ERROR {tipo}] (Línea {linea}, Columna {columna}): {mensaje}")

    def hay_errores(self):
        """Verifica si hay errores registrados"""
        return len(self.errores) > 0

class Scanner:
    """
    Clase principal del scanner optimizado
    """
    def __init__(self, nombre_archivo, manejador_errores=None):
        self.nombre_archivo = nombre_archivo
        self.manejador_errores = manejador_errores or ErrorHandler()
        self.archivo = None
        self.contenido = ""
        self.posicion = 0
        self.linea = 1
        self.columna = 1
        self.automata = IntegratedAutomaton()
        self.token_actual = None
        self.token_siguiente = None
    
    def inicializar_scanner(self):
        """Inicializa el scanner con el archivo fuente"""
        try:
            self.archivo = open(self.nombre_archivo, 'r', encoding='utf-8')
            self.contenido = self.archivo.read()
            self._cargar_primer_token()
        except Exception as e:
            if hasattr(self.manejador_errores, 'registrar_error'):
                self.manejador_errores.registrar_error(
                    "SCANNER", 
                    f"Error al inicializar scanner: {str(e)}", 
                    self.linea, 
                    self.columna
                )
            else:
                # Si manejador_errores es un string u otro objeto sin método registrar_error
                print(f"Error al inicializar scanner: {str(e)}")
            raise
    
    def finalizar_scanner(self):
        """Cierra el archivo fuente"""
        if self.archivo:
            self.archivo.close()
    
    def deme_token(self):
        """Retorna el token actual y avanza al siguiente"""
        self.token_actual = self.token_siguiente
        self.token_siguiente = self._siguiente_token()
        return self.token_actual
    
    def tome_token(self):
        """Retorna el token actual sin avanzar"""
        return self.token_actual
    
    def _cargar_primer_token(self):
        """Carga el primer token del archivo"""
        self.token_siguiente = self._siguiente_token()
    
    def _siguiente_token(self):
        """Obtiene el siguiente token del contenido"""
        self._ignorar_espacios()
        
        if self.posicion >= len(self.contenido):
            return Token("EOF", "", self.linea, self.columna)
        
        inicio_linea = self.linea
        inicio_col = self.columna
        
        # Usar el autómata integrado
        resultado = self.automata.procesar(
            self.contenido, 
            self.posicion, 
            self.linea, 
            self.columna
        )
        
        if resultado.exito:
            self.posicion = resultado.final_pos
            self.linea = resultado.final_linea
            self.columna = resultado.final_columna
            
            # Creamos directamente el token con la información adecuada
            return Token(
                resultado.tipo,
                resultado.lexema,
                inicio_linea,
                inicio_col,
                resultado.valor
            )
        else:
            # Manejo de error léxico
            error_char = self.contenido[self.posicion]
            self.posicion += 1
            self.columna += 1
            
            return Token("ERROR", error_char, inicio_linea, inicio_col)
    
    def _ignorar_espacios(self):
        """Avanza la posición ignorando espacios en blanco"""
        while self.posicion < len(self.contenido):
            c = self.contenido[self.posicion]
            if not c.isspace():
                break
                
            if c == '\n':
                self.linea += 1
                self.columna = 1
            else:
                self.columna += 1
            self.posicion += 1
