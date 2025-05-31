from ..Simbolo import Simbolo
from ..TablaSimbolos import TablaSimbolos
from ..diccionarioSemantico.CheckOperacion import chequear_tipos_expresion
from ..diccionarioSemantico.CheckVarInit import checkInicializacionVariable


def welcomeObsidian(categoria, actual, tipo, asignacion):
    print(f"verificacion de asignacion:")
    for elemento in asignacion:
        print(elemento)
    if len(asignacion) <=2:
        mi_simbolo = Simbolo(
            nombre=actual.lexema,
            tipo=tipo.type,
            categoria=categoria.type,
            linea=actual.linea,
            columna=actual.columna,
            valor= chequear_tipos_expresion(tipo.type, asignacion[0].lexema)
        ) 
        print(f"verificacion de simbolo:")
        print(mi_simbolo.__str__())
        
        tabla = TablaSimbolos.instancia()
        checkInicializacionVariable(mi_simbolo)
        tabla.insertar(mi_simbolo)
        print(f" \n\n ver info tabla")
        tabla.imprimir_tabla()
        print(f"\n\n")

    else: 
        print(f"CASO ESPECIAL")