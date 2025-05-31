from ..HistorialSemantico import historialSemantico
from ..HistorialSemanticoNegativo import historialSemanticoNegativo

def checkShelfSize(valores, cantidad):
    """
    Regla Semántica 005: Verifica que el número de valores en un SHELF
    coincida con la cantidad declarada.
    """
    cantidad_esperada = int(cantidad.lexema)
    cantidad_real = len(valores)

    if cantidad_real == cantidad_esperada:
        mensaje = (
            f"REGLA SEMANTICA 005: La cantidad declarada en el SHELF es {cantidad_esperada} "
            f"y se asignaron correctamente {cantidad_real} elementos."
        )
        historialSemantico.agregar(mensaje)
        return True
    else:
        mensaje = (
            f"REGLA SEMANTICA 005: ERROR - Se declararon {cantidad_esperada} espacios en el SHELF, "
            f"pero se asignaron {cantidad_real} elementos. Desajuste en tamaño."
        )
        historialSemanticoNegativo.agregar(mensaje)
        historialSemantico.agregar(mensaje)
        return False
