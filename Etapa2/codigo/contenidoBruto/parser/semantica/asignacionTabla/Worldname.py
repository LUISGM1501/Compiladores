from ..Simbolo import Simbolo
from ..TablaSimbolos import TablaSimbolos

def welcomeWorldname(tipo, actual):

    print("\n\n\n\n")
    print(f"Bienvenido a ASIGNACION DE WORLDNAME")
    print(f"TOKEN ACTUAL: {actual} de TIPO: {tipo}")

    # Asignacion a la estructura de simbolo:
    mi_simbolo = Simbolo(
        nombre=actual.lexema,
        tipo=tipo.type,
        categoria=tipo.type,
        linea=actual.linea,
        columna=actual.columna,
        valor=actual.lexema
    ) 

    #insercion en la tabla de hash 
    tabla = TablaSimbolos.instancia()
    tabla.insertar(mi_simbolo)

