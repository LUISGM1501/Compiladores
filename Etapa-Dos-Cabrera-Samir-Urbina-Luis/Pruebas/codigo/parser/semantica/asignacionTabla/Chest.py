from ..Simbolo import Simbolo
from ..TablaSimbolos import TablaSimbolos
from ..diccionarioSemantico.CheckOperacion import chequear_tipos_expresion
from ..diccionarioSemantico.CheckShelfSize import checkShelfSize
from ..diccionarioSemantico.CheckVarInit import checkInicializacionVariable


def welcomeChest(actual, tipo, asignacion,):
    print(f"Verificación de asignación:")
    for elemento in asignacion:
        print(elemento)

    valores = []  # Aquí guardaremos todos los valores del array
    dentro_del_array = False  # Para saber si estamos dentro de {: ... :}

    for token in asignacion:
        # Si encontramos "{:" (DOS_PUNTOS después de un POLLO_CRUDO o similar)
        if token.type == "DOS_PUNTOS" and not dentro_del_array:
            dentro_del_array = True
            continue  # Saltamos el ":" de apertura
        
        # Si encontramos ":}" (DOS_PUNTOS antes de un POLLO_ASADO)
        elif token.type == "DOS_PUNTOS" and dentro_del_array:
            break  # Terminamos el procesamiento
        
        # Si estamos dentro del array y no es una coma ni delimitador
        if dentro_del_array and token.type not in ["COMA", "POLLO_CRUDO", "POLLO_ASADO", "DOS_PUNTOS"]:
            valores.append(token.lexema)  # Guardamos el valor tal cual (número, string, etc.)

    # Creamos el símbolo con la lista de valores
    mi_simbolo = Simbolo(
        nombre=actual.lexema,
        tipo=tipo.type,  # "CHEST"
        categoria="VARIABLE",
        linea=actual.linea,
        columna=actual.columna,
        valor=valores  
    )

    print(f"Verificación de símbolo:")
    print(mi_simbolo.__str__())
    
    tabla = TablaSimbolos.instancia()
    checkInicializacionVariable(mi_simbolo)
    tabla.insertar(mi_simbolo)
    
    print(f"\n\nVer info tabla:")
    tabla.imprimir_tabla()
    print(f"\n\n")


def welcomeShelf(categoria, cantidad, tipo, variable, items):
    print(f"Verificación de asignación:")
    for elemento in items:
        print(elemento)

    valores = []
    dentro_del_array = False

    for token in items:
        if token.type == "CORCHETE_ABRE" and not dentro_del_array:
            dentro_del_array = True
            continue
        elif token.type == "CORCHETE_CIERRA" and dentro_del_array:
            break
        if dentro_del_array and token.type not in ["COMA", "POLLO_CRUDO", "POLLO_ASADO", "DOS_PUNTOS"]:
            valores.append(token.lexema)

    # ✅ Aplicar regla semántica 005
    if not checkShelfSize(valores, cantidad):
        print("Error semántico: cantidad de elementos no coincide con lo declarado.")
        return  # Abortamos la inserción si la verificación falla

    # Crear símbolo si la verificación fue exitosa
    mi_simbolo = Simbolo(
        nombre=variable.lexema,
        tipo=categoria.type,  # SHELF
        categoria="VARIABLE",
        linea=variable.linea,
        columna=variable.columna,
        valor=chequear_tipos_expresion(tipo.type, valores)
    )

    print(f"Verificación de símbolo:")
    print(mi_simbolo.__str__())

    tabla = TablaSimbolos.instancia()
    checkInicializacionVariable(mi_simbolo)
    tabla.insertar(mi_simbolo)

    print(f"\n\nVer info tabla:")
    tabla.imprimir_tabla()
    print(f"\n\n")