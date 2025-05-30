from ..HistorialSemantico import historialSemantico  # Usa el alias ya creado

def checkWorldname(token):
    print(f"IMPRESION DEL primer TOKEN type: {token.type}, lexema: {token.lexema}")
    if token.type == "WORLD_NAME":
        mensaje = f"REGLA SEMANTICA 008: El primer Token del Programa es '{token.lexema}' con tipo '{token.type}', se PROCEDE con la ejecucion."
        historialSemantico.agregar(mensaje)
        return True  # Está bien
    else:
        mensaje = f"REGLA SEMANTICA 008: El primer Token del Programa es '{token.lexema}' con tipo '{token.type}', se DETIENE con la ejecucion."
        historialSemantico.agregar(mensaje)
        return False  # Error
