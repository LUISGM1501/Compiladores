from ..Simbolo import Simbolo
from ..TablaSimbolos import TablaSimbolos
from ..diccionarioSemantico.CheckOperacion import chequear_tipos_expresion
from ..diccionarioSemantico.CheckOverflow import check_overflow_by_type

def welcomeSpider(actual, tipo, asignacion):
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
        # Declaración sin inicialización: Spider variable;
        print(f"Declaración sin inicialización de variable Spider: {actual.lexema}")
        mi_simbolo = Simbolo(
            nombre=actual.lexema,
            tipo=tipo.type,
            categoria="VARIABLE",
            linea=actual.linea,
            columna=actual.columna,
            valor=None  # Sin valor inicial
        )
    elif len(asignacion) >= 3 and asignacion[0].type == "IGUAL":
        # Declaración con inicialización: Spider variable = valor;
        valor_inicial = asignacion[1].lexema
        print(f"tipo: {tipo.type} y asignacion: {valor_inicial}")
        
        # Chequeo de tipo
        valor_chequeado = chequear_tipos_expresion(tipo.type, valor_inicial)
        
        # *** CHEQUEO DE OVERFLOW PARA STRINGS ***
        from ..diccionarioSemantico.CheckOverflow import check_spider_overflow
        es_valido, cadena_ajustada, mensaje_error = check_spider_overflow(
            valor_chequeado, 
            actual.lexema
        )
        
        if not es_valido:
            print(f"WARNING OVERFLOW: {mensaje_error}")
            print(f"Cadena truncada de {len(valor_inicial)} a {len(cadena_ajustada)} caracteres")
        
        mi_simbolo = Simbolo(
            nombre=actual.lexema,
            tipo=tipo.type,
            categoria="VARIABLE",
            linea=actual.linea,
            columna=actual.columna,
            valor=cadena_ajustada  # Usar valor ajustado
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
        tabla.insertar(mi_simbolo)
        print(f" \n\n ver info tabla")
        tabla.imprimir_tabla()
        print(f"\n\n")
    except ValueError as e:
        print(f"ERROR SEMANTICO: {e}")