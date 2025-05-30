from ..Simbolo import Simbolo
from ..TablaSimbolos import TablaSimbolos
from ..diccionarioSemantico.CheckOperacion import chequear_tipos_expresion
from ..diccionarioSemantico.CheckOverflow import check_overflow_by_type

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
        valor_inicial = asignacion[1].lexema
        
        # Chequeo de tipo
        valor_chequeado = chequear_tipos_expresion(tipo.type, valor_inicial)
        
        # CORRECCIÓN: Manejar tanto strings como floats del valor chequeado
        try:
            # Si valor_chequeado es un float, convertirlo a string primero
            if isinstance(valor_chequeado, float):
                valor_str = str(valor_chequeado)
            else:
                valor_str = str(valor_chequeado)
            
            # Parsear el flotante
            if '.' in valor_str:
                partes = valor_str.split('.')
                entero = int(float(partes[0]))  # Usar float() para manejar casos como "-0"
                # Tomar máximo 2 dígitos decimales y rellenar con ceros si es necesario
                decimal_str = partes[1][:2] if len(partes[1]) >= 2 else partes[1].ljust(2, '0')
                decimal = int(decimal_str)
            else:
                entero = int(float(valor_str))
                decimal = 0
                
            # *** CHEQUEO DE OVERFLOW PARA FLOTANTES ***
            from ..diccionarioSemantico.CheckOverflow import check_ghast_overflow
            es_valido, (entero_adj, decimal_adj), mensaje_error = check_ghast_overflow(
                entero, 
                decimal, 
                actual.lexema
            )
            
            if not es_valido:
                print(f"WARNING OVERFLOW: {mensaje_error}")
                print(f"Valor ajustado: {entero_adj}.{decimal_adj:02d}")
            
            valor_final = f"{entero_adj}.{decimal_adj:02d}"
            
        except (ValueError, IndexError) as e:
            print(f"ERROR: Valor flotante inválido: {valor_inicial} - {str(e)}")
            valor_final = "0.00"
        
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
        tabla.insertar(mi_simbolo)
        print(f" \n\n ver info tabla")
        tabla.imprimir_tabla()
        print(f"\n\n")
    except ValueError as e:
        print(f"ERROR SEMANTICO: {e}")