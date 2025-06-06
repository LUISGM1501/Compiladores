from ..Simbolo import Simbolo
from ..TablaSimbolos import TablaSimbolos
from ..diccionarioSemantico.CheckArchivoNombre import checkArchivoNombre
from ..diccionarioSemantico.CheckVarInit import checkInicializacionVariable


def welcomeBook(actual, tipo, contenido):
    print(f"\n\n\n\nactual: {actual}")
    print(f"tipo: {tipo} \n\n")
    for element in contenido:
        print(element)
    print(f"\n\n\n\n")

    tabla = TablaSimbolos.instancia()
    variable_existente = tabla.buscar(actual.lexema)

    if variable_existente is not None:
        print(f"La variable '{actual.lexema}' ya fue declarada.")
        return

    valores = []  # Lista para almacenar los valores ("datos.txt", 'E')
    barra_abierta = False

    for token in contenido:
        if token.type == "BARRA" and not barra_abierta:
            barra_abierta = True
            continue
        elif token.type == "BARRA" and barra_abierta:
            break  # Cerramos al encontrar la segunda barra

        # Recolectar valores útiles, excluyendo delimitadores
        if barra_abierta and token.type not in ["COMA", "POLLO_CRUDO", "POLLO_ASADO", "BARRA", "PUNTO_Y_COMA"]:
            valores.append(token.lexema)

    # ✔️ Validar la Regla Semántica 010: archivo debe terminar en .txt
    if not checkArchivoNombre(valores):
        print("Error semántico: archivo inválido. No se insertará la variable.")
        return

    # Crear símbolo e insertar
    mi_simbolo = Simbolo(
        nombre=actual.lexema,
        tipo=tipo.type,  # "BOOK"
        categoria="VARIABLE",
        linea=actual.linea,
        columna=actual.columna,
        valor=valores
    )

    print(f"Verificación de símbolo:")
    print(mi_simbolo.__str__())
    checkInicializacionVariable(mi_simbolo)
    tabla.insertar(mi_simbolo)

    print(f"\n\nVer info tabla:")
    tabla.imprimir_tabla()
    print(f"\n\n")
