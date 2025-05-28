from ..Simbolo import Simbolo
from ..TablaSimbolos import TablaSimbolos
from ..simbolos.ChequeoOperacion import chequear_tipos_expresion

def welcomeGhast(actual, tipo, asignacion):
    print(f"verificacion de asignacion:")
    for elemento in asignacion:
        print(elemento)

    if len(asignacion) <=3:
        print(f"tipo: {tipo.type} y asignacion: {asignacion[1].lexema}")
        mi_simbolo = Simbolo(
            nombre=actual.lexema,
            tipo=tipo.type,
            categoria="VARIABLE",
            linea=actual.linea,
            columna=actual.columna,
            valor=chequear_tipos_expresion(tipo.type,asignacion[1].lexema)
        ) 
        print(f"verificacion de simbolo:")
        print(mi_simbolo.__str__())
        tabla = TablaSimbolos.instancia()
        tabla.insertar(mi_simbolo)
        print(f" \n\n ver info tabla")
        tabla.imprimir_tabla()
        print(f"\n\n")

    else: 
        print(f"CASO ESPECIAL")