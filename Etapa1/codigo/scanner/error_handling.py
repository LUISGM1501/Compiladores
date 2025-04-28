"""
Sistema de manejo de errores para el scanner
"""

class Error:
    """
    Clase que representa un error en el compilador
    """
    def __init__(self, tipo, mensaje, linea, columna):
        """
        Inicializa un nuevo error
        
        Argumentos:
            tipo: Tipo de error (LEXICO, SINTACTICO, SEMANTICO)
            mensaje: Descripción del error
            linea: Número de línea donde ocurrió el error
            columna: Número de columna donde ocurrió el error
        """
        self.tipo = tipo
        self.mensaje = mensaje
        self.linea = linea
        self.columna = columna
    
    def __str__(self):
        """
        Representación textual del error
        """
        return f"[{self.tipo}] {self.mensaje} (línea {self.linea}, columna {self.columna})"

class ErrorHandler:
    """
    Manejador de errores para recuperación de errores
    """
    def __init__(self):
        """
        Inicializa el manejador de errores
        """
        self.errores = []
    
    def registrar_error(self, tipo, mensaje, linea, columna):
        """
        Registra un nuevo error
        
        Argumentos:
            tipo: Tipo de error (LEXICO, SINTACTICO, SEMANTICO)
            mensaje: Descripción del error
            linea: Número de línea donde ocurrió el error
            columna: Número de columna donde ocurrió el error
        """
        error = Error(tipo, mensaje, linea, columna)
        self.errores.append(error)
        print(str(error))
    
    def hay_errores(self):
        """
        Verifica si hay errores registrados
        
        Retorna:
            bool: True si hay errores, False en caso contrario
        """
        return len(self.errores) > 0
    
    def obtener_resumen(self):
        """
        Obtiene un resumen de los errores registrados
        
        Retorna:
            str: Resumen de errores
        """
        if not self.errores:
            return "No se encontraron errores."
        
        resumen = f"Total de errores: {len(self.errores)}\n"
        
        # Contar errores por tipo
        errores_por_tipo = {}
        for error in self.errores:
            if error.tipo not in errores_por_tipo:
                errores_por_tipo[error.tipo] = 0
            errores_por_tipo[error.tipo] += 1
        
        # Agregar desglose por tipo
        for tipo, cantidad in errores_por_tipo.items():
            resumen += f"  {tipo}: {cantidad}\n"
        
        # Agregar detalle de errores
        resumen += "\nDetalle de errores:\n"
        for i, error in enumerate(self.errores):
            resumen += f"  {i+1}. {error}\n"
        
        return resumen