from ..TablaSimbolos import TablaSimbolos
from ..HistorialSemantico import historialSemantico  # Usa el alias ya creado

def checkVarExiste(token):
    tabla = TablaSimbolos.instancia()
    if tabla.buscar(token.lexema):
        mensaje = f"REGLA SEMANTICA 001: El IDENTIFICADOR de nombre '{token.lexema}' ya existe"
        historialSemantico.agregar(mensaje)
        return False
    else:
        mensaje = f"REGLA SEMANTICA 001: El IDENTIFICADOR de nombre '{token.lexema}' NO existe, se procede a crear"
        historialSemantico.agregar(mensaje)
        return True


