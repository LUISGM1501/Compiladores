from ..Simbolo import Simbolo
from ..TablaSimbolos import TablaSimbolos
from ..diccionarioSemantico.CheckOperacion import chequear_tipos_expresion
from ..diccionarioSemantico.CheckVarInit import checkInicializacionVariable


def welcomeGhast(actual, tipo, asignacion):
    print(f"verificacion de asignacion:")
    for elemento in asignacion:
        print(elemento)

    # Verificar que la variable no esté ya declarada
    tabla = TablaSimbolos.instancia()
    variable_existente = tabla.buscar(actual.lexema)
    if variable_existente is not None:
        print(f"ERROR SEMANTICO: La variable '{actual.lexema}' ya está declarada en línea {variable_existente.linea}")
        return

    # Manejar diferentes casos de asignación
    if len(asignacion) == 1 and asignacion[0].type == "PUNTO_Y_COMA":
        # Declaración sin inicialización: Ghast variable;
        print(f"Declaración sin inicialización de variable Ghast: {actual.lexema}")
        mi_simbolo = Simbolo(
            nombre=actual.lexema,
            tipo=tipo.type,
            categoria="VARIABLE",
            linea=actual.linea,
            columna=actual.columna,
            valor=None  # Sin valor inicial
        )
    elif len(asignacion) >= 3 and asignacion[0].type == "IGUAL":
        # Declaración con inicialización: Ghast variable = valor;
        print(f"tipo: {tipo.type} y asignacion: {asignacion[1].lexema}")
        mi_simbolo = Simbolo(
            nombre=actual.lexema,
            tipo=tipo.type,
            categoria="VARIABLE",
            linea=actual.linea,
            columna=actual.columna,
            valor=chequear_tipos_expresion(tipo.type, asignacion[1].lexema)
        )
    else:
        # Caso especial o error
        print(f"CASO ESPECIAL: formato de asignación no reconocido")
        print(f"Longitud de asignación: {len(asignacion)}")
        mi_simbolo = Simbolo(
            nombre=actual.lexema,
            tipo=tipo.type,
            categoria="VARIABLE",
            linea=actual.linea,
            columna=actual.columna,
            valor=None
        )

    print(f"verificacion de simbolo:")
    print(mi_simbolo.__str__())
    
    try:
        checkInicializacionVariable(mi_simbolo)
        tabla.insertar(mi_simbolo)
        print(f" \n\n ver info tabla")
        tabla.imprimir_tabla()
        print(f"\n\n")
    except ValueError as e:
        print(f"ERROR SEMANTICO: {e}")