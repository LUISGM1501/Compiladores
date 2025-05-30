from ..TablaSimbolos import TablaSimbolos
from ..HistorialSemantico import historialSemantico  # Usa el alias ya creado

def checkObsidian(token, tokenpasado):
    tabla = TablaSimbolos.instancia()
    print(f"\n\n\n\n dentro del checkeo de variables para token: {token}")
    print(f"token: {token.lexema} ademas de ser tipo {tokenpasado.type}")

    if tabla.buscar(token.lexema) and tokenpasado.type == "OBSIDIAN":
        mensaje = f"REGLA SEMANTICA 002: El IDENTIFICADOR de nombre '{token.lexema}' ya existe y es un OBSIDIAN, ERROR al agregarlo"
        historialSemantico.agregar(mensaje)
        return False
    else:
        mensaje = f"REGLA SEMANTICA 002: El IDENTIFICADOR de nombre '{token.lexema}' NO existe, se procede a crear el OBSIDIAN"
        historialSemantico.agregar(mensaje)
        return True