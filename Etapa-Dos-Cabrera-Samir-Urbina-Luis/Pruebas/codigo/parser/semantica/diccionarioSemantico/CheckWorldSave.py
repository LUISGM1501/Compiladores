from ..HistorialSemantico import historialSemantico  # Usa el alias ya creado
from ..HistorialSemanticoNegativo import historialSemanticoNegativo

def checkWorldSave(token):
    print(f"IMPRESION DEL ultimo TOKEN type: {token.type}, lexema: {token.lexema}")
    if token.type == "WORLD_SAVE":
        mensaje = f"REGLA SEMANTICA 009: El ultimo Token del Programa es '{token.lexema}' con tipo '{token.type}', se PROCEDE con la ejecucion."
        historialSemantico.agregar(mensaje)
        return True  # Está bien
    else:
        mensaje = f"REGLA SEMANTICA 009: El ultimo Token del Programa es '{token.lexema}' con tipo '{token.type}', se DETIENE con la ejecucion."
        historialSemantico.agregar(mensaje)
        historialSemanticoNegativo.agregar(mensaje)
        return False  # Error
