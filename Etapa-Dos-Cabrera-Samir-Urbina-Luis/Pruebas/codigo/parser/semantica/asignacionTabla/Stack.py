from ..Simbolo import Simbolo
from ..TablaSimbolos import TablaSimbolos
from ..diccionarioSemantico.CheckOperacion import chequear_tipos_expresion
from ..diccionarioSemantico.CheckOverflow import check_overflow_by_type
from ..diccionarioSemantico.CheckUsoVar import verificador_uso_variables
from ..diccionarioSemantico.CheckVarInit import checkInicializacionVariable

def welcomeStack(actual, tipo, asignacion):
    print(f"verificacion de asignacion:")
    for elemento in asignacion:
        print(elemento)

    # Verificar que la variable no esté ya declarada
    tabla = TablaSimbolos.instancia()
    variable_existente = tabla.buscar(actual.lexema)
    if variable_existente is not None:
        print(f"ERROR SEMANTICO: La variable '{actual.lexema}' ya está declarada en línea {variable_existente.linea}")
        return

    # Determinar el valor a verificar
    valor_a_verificar = None
    
    if len(asignacion) == 1 and asignacion[0].type == "PUNTO_Y_COMA":
        # Declaración sin inicialización: Stack variable;
        print(f"Declaración sin inicialización de variable Stack: {actual.lexema}")
        # No hay valor que verificar para overflow
        mi_simbolo = Simbolo(
            nombre=actual.lexema,
            tipo=tipo.type,
            categoria="VARIABLE",
            linea=actual.linea,
            columna=actual.columna,
            valor=None
        )
    elif len(asignacion) >= 3 and asignacion[0].type == "IGUAL":
        # Declaración con inicialización: Stack variable = valor;
        if len(asignacion) >= 4 and asignacion[1].type == "RESTA":
            # Es un número negativo: = - 40000
            valor_inicial = "-" + asignacion[2].lexema
        else:
            # Es un número normal: = 40000
            valor_inicial = asignacion[1].lexema
        
        print(f"tipo: {tipo.type} y asignacion: {valor_inicial}")
        
        # Chequeo de tipo
        valor_chequeado = chequear_tipos_expresion(tipo.type, valor_inicial)
        
        # *** AQUÍ SE INTEGRA EL CHEQUEO DE OVERFLOW ***
        es_valido, valor_ajustado, mensaje_error = check_overflow_by_type(
            tipo.type, 
            valor_chequeado, 
            actual.lexema
        )
        
        if not es_valido and mensaje_error:
            print(f"WARNING OVERFLOW: {mensaje_error}")
            # Usar valor ajustado pero continuar procesamiento
            valor_final = valor_ajustado
        else:
            valor_final = valor_ajustado
        
        mi_simbolo = Simbolo(
            nombre=actual.lexema,
            tipo=tipo.type,
            categoria="VARIABLE",
            linea=actual.linea,
            columna=actual.columna,
            valor=valor_final
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
        verificador_uso_variables.registrar_declaracion(mi_simbolo.nombre)
        tabla.insertar(mi_simbolo)
        print(f" \n\n ver info tabla")
        tabla.imprimir_tabla()
        print(f"\n\n")
    except ValueError as e:
        print(f"ERROR SEMANTICO: {e}")