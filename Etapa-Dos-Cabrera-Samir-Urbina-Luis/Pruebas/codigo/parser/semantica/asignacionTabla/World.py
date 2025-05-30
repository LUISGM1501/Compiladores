from ..Simbolo import Simbolo
from ..TablaSimbolos import TablaSimbolos
from ..diccionarioSemantico.CheckVarInit import checkInicializacionVariable


def welcomeWorld(tipo, actual):
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
    checkInicializacionVariable(mi_simbolo)
    tabla = TablaSimbolos.instancia()
    tabla.insertar(mi_simbolo)

    print(f" \n\n ver info tabla")
    tabla.imprimir_tabla()
    print(f"\n\n")

