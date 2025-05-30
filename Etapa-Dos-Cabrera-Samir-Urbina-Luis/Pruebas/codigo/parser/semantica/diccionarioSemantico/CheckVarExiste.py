from ..TablaSimbolos import TablaSimbolos
from ..HistorialSemantico import historialSemantico

def checkVarExiste(token):
    """
    Verifica si un identificador ya existe en la tabla de símbolos.
    
    Args:
        token: Token con el identificador a verificar
        
    Returns:
        True si NO existe (puede ser creado), False si ya existe
    """
    tabla = TablaSimbolos.instancia()
    simbolo_existente = tabla.buscar(token.lexema)
    
    if simbolo_existente:
        mensaje = f"REGLA SEMANTICA 001: El IDENTIFICADOR de nombre '{token.lexema}' ya existe"
        historialSemantico.agregar(mensaje)
        return False
    else:
        mensaje = f"REGLA SEMANTICA 001: El IDENTIFICADOR de nombre '{token.lexema}' NO existe, se procede a crear"
        historialSemantico.agregar(mensaje)
        return True

def checkVarDeclared(token):
    """
    Verifica si un identificador está declarado (para uso en expresiones).
    
    Args:
        token: Token con el identificador a verificar
        
    Returns:
        True si existe y puede ser usado, False si no está declarado
    """
    tabla = TablaSimbolos.instancia()
    simbolo_existente = tabla.buscar(token.lexema)
    
    if simbolo_existente:
        mensaje = f"REGLA SEMANTICA 003: El IDENTIFICADOR '{token.lexema}' está declarado y puede ser usado"
        historialSemantico.agregar(mensaje)
        return True
    else:
        mensaje = f"REGLA SEMANTICA 003: ERROR - El IDENTIFICADOR '{token.lexema}' NO está declarado"
        historialSemantico.agregar(mensaje)
        return False

def checkVarInitialized(token):
    """
    Verifica si una variable está inicializada antes de ser usada.
    
    Args:
        token: Token con el identificador a verificar
        
    Returns:
        True si está inicializada, False si no
    """
    tabla = TablaSimbolos.instancia()
    simbolo_existente = tabla.buscar(token.lexema)
    
    if simbolo_existente:
        if simbolo_existente.categoria in ["VARIABLE"] and simbolo_existente.valor is None:
            mensaje = f"REGLA SEMANTICA 004: WARNING - Variable '{token.lexema}' usada sin inicializar"
            historialSemantico.agregar(mensaje)
            return False
        else:
            mensaje = f"REGLA SEMANTICA 004: Variable '{token.lexema}' está inicializada"
            historialSemantico.agregar(mensaje)
            return True
    
    return False

def getVarType(token):
    """
    Obtiene el tipo de una variable declarada.
    
    Args:
        token: Token con el identificador
        
    Returns:
        Tipo de la variable o None si no existe
    """
    tabla = TablaSimbolos.instancia()
    simbolo_existente = tabla.buscar(token.lexema)
    
    if simbolo_existente:
        return simbolo_existente.tipo
    return None
