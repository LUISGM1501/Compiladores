class Simbolo:
    def __init__(self, nombre, tipo, categoria, linea, columna, valor=None, otros_atributos=None):
        self.nombre = nombre
        self.tipo = tipo  # 'int', 'float', 'string', 'bool', o tipos personalizados
        self.categoria = categoria  # 'variable', 'funcion', 'procedimiento', 'constante', 'tipo'
        self.linea = linea  # Línea de declaración
        self.columna = columna  # Columna de declaración
        self.valor = valor  # Para constantes o inicializaciones
        self.otros_atributos = otros_atributos  # Diccionario u otros datos adicionales
    
    def __str__(self):
        return (
            f"Nombre: {self.nombre}, "
            f"Tipo: {self.tipo}, "
            f"Categoría: {self.categoria}, "
            f"Línea: {self.linea}, "
            f"Columna: {self.columna}, "
            f"Valor: {self.valor}, "
            f"Otros atributos: {self.otros_atributos}"
        )
