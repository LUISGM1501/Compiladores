from ..Simbolo import Simbolo
from ..TablaSimbolos import TablaSimbolos

def welcomeEntity(actual, tokens_temporales):
    """
    Maneja tanto definiciones de tipos Entity como declaraciones de variables Entity
    
    Args:
        actual: Token del identificador después de Entity
        tokens_temporales: Lista de tokens hasta encontrar PUNTO_Y_COMA
    """
    print(f"Procesando ENTITY: {actual.lexema}")
    print(f"Tokens recibidos: {len(tokens_temporales)}")
    
    # Debug: mostrar tokens recibidos
    for i, token in enumerate(tokens_temporales):
        print(f"  Token {i}: {token.type} -> {token.lexema}")
    
    # Determinar si es definición de tipo o declaración de variable
    es_definicion_tipo = False
    es_declaracion_variable = False
    
    if len(tokens_temporales) > 0:
        primer_token = tokens_temporales[0]
        if primer_token.type == "POLLO_CRUDO":
            es_definicion_tipo = True
        elif primer_token.type == "IDENTIFICADOR":
            # Es una declaración de variable: Entity TipoExistente nombreVariable = ...
            es_declaracion_variable = True
    
    if es_definicion_tipo:
        procesar_definicion_tipo(actual, tokens_temporales)
    elif es_declaracion_variable:
        procesar_declaracion_variable(actual, tokens_temporales)
    else:
        print(f"ERROR: No se pudo determinar el tipo de construcción Entity")

def procesar_definicion_tipo(nombre_tipo, tokens_temporales):
    """
    Procesa la definición de un nuevo tipo Entity
    Entity NombreTipo PolloCrudo campos... PolloAsado;
    """
    print(f"  -> Procesando DEFINICIÓN de tipo: {nombre_tipo.lexema}")
    
    # Verificar que el tipo no exista ya
    tabla = TablaSimbolos.instancia()
    tipo_existente = tabla.buscar(nombre_tipo.lexema)
    if tipo_existente is not None:
        print(f"ERROR SEMANTICO: El tipo '{nombre_tipo.lexema}' ya está definido en línea {tipo_existente.linea}")
        return
    
    # Extraer campos entre POLLO_CRUDO y POLLO_ASADO
    campos = []
    dentro_del_bloque = False
    
    i = 0
    while i < len(tokens_temporales):
        token = tokens_temporales[i]
        
        if token.type == "POLLO_CRUDO":
            dentro_del_bloque = True
            print("    Iniciando bloque de campos")
            i += 1
            continue
        elif token.type == "POLLO_ASADO":
            dentro_del_bloque = False
            print("    Finalizando bloque de campos")
            break
        
        if dentro_del_bloque:
            # Buscar patrón: TIPO IDENTIFICADOR PUNTO_Y_COMA
            if token.type in ["STACK", "SPIDER", "RUNE", "TORCH", "GHAST", "CHEST", "BOOK", "SHELF"]:
                tipo_campo = token.type
                print(f"    Tipo encontrado: {tipo_campo}")
                
                # El siguiente token debería ser el identificador del campo
                if i + 1 < len(tokens_temporales) and tokens_temporales[i + 1].type == "IDENTIFICADOR":
                    nombre_campo = tokens_temporales[i + 1].lexema
                    campo = {
                        "nombre": nombre_campo,
                        "tipo": tipo_campo,
                        "linea": tokens_temporales[i + 1].linea,
                        "columna": tokens_temporales[i + 1].columna
                    }
                    campos.append(campo)
                    print(f"    Campo encontrado: {nombre_campo} ({tipo_campo})")
                    
                    # Saltar el identificador y el punto y coma
                    i += 2  # Saltar IDENTIFICADOR y PUNTO_Y_COMA
                else:
                    print(f"    ERROR: Se esperaba identificador después del tipo {tipo_campo}")
                    i += 1
            elif token.type == "PUNTO_Y_COMA":
                print("    Separador de campo encontrado")
                i += 1
            else:
                print(f"    Token inesperado en bloque: {token.type}")
                i += 1
        else:
            i += 1
    
    # Crear el símbolo del tipo Entity
    simbolo_tipo = Simbolo(
        nombre=nombre_tipo.lexema,
        tipo="ENTITY_TYPE",  # Cambio: distinguir tipos de variables
        categoria="TIPO_DEFINIDO_USUARIO",
        linea=nombre_tipo.linea,
        columna=nombre_tipo.columna,
        valor=campos
    )
    
    print(f"  Simbolo ENTITY_TYPE creado:")
    print(f"    Nombre: {simbolo_tipo.nombre}")
    print(f"    Tipo: {simbolo_tipo.tipo}")
    print(f"    Categoria: {simbolo_tipo.categoria}")
    print(f"    Campos ({len(campos)}):")
    for j, campo in enumerate(campos):
        print(f"      Campo {j}: {campo['nombre']} ({campo['tipo']})")
    
    # Insertar en la tabla de símbolos
    try:
        tabla.insertar(simbolo_tipo)
        print(f"  ENTITY_TYPE '{nombre_tipo.lexema}' insertado correctamente")
    except ValueError as e:
        print(f"  ERROR SEMANTICO: {e}")

def procesar_declaracion_variable(tipo_entity, tokens_temporales):
    """
    Procesa la declaración de una variable de tipo Entity
    Entity TipoExistente nombreVariable = {campos...};
    """
    print(f"  -> Procesando DECLARACIÓN de variable tipo: {tipo_entity.lexema}")
    
    if len(tokens_temporales) < 1:
        print(f"  ERROR: Declaración incompleta")
        return
    
    nombre_variable = tokens_temporales[0]
    print(f"    Variable: {nombre_variable.lexema}")
    
    # Verificar que el tipo Entity exista
    tabla = TablaSimbolos.instancia()
    tipo_definido = tabla.buscar(tipo_entity.lexema)
    if tipo_definido is None:
        print(f"  ERROR SEMANTICO: El tipo '{tipo_entity.lexema}' no está definido")
        return
    
    if tipo_definido.tipo != "ENTITY_TYPE":
        print(f"  ERROR SEMANTICO: '{tipo_entity.lexema}' no es un tipo Entity")
        return
    
    # Verificar que la variable no exista ya
    variable_existente = tabla.buscar(nombre_variable.lexema)
    if variable_existente is not None:
        print(f"  ERROR SEMANTICO: La variable '{nombre_variable.lexema}' ya está declarada")
        return
    
    # Procesar inicialización si existe
    valores_iniciales = {}
    if len(tokens_temporales) >= 3 and tokens_temporales[1].type == "IGUAL":
        print(f"    Procesando inicialización...")
        valores_iniciales = procesar_inicializacion_entity(tokens_temporales[2:], tipo_definido.valor)
    
    # Crear el símbolo de la variable
    simbolo_variable = Simbolo(
        nombre=nombre_variable.lexema,
        tipo=tipo_entity.lexema,  # El tipo es el nombre del Entity definido
        categoria="VARIABLE",
        linea=nombre_variable.linea,
        columna=nombre_variable.columna,
        valor=valores_iniciales
    )
    
    print(f"  Simbolo ENTITY_VARIABLE creado:")
    print(f"    Nombre: {simbolo_variable.nombre}")
    print(f"    Tipo: {simbolo_variable.tipo}")
    print(f"    Categoria: {simbolo_variable.categoria}")
    print(f"    Valores: {simbolo_variable.valor}")
    
    # Insertar en la tabla de símbolos
    try:
        tabla.insertar(simbolo_variable)
        print(f"  ENTITY_VARIABLE '{nombre_variable.lexema}' insertada correctamente")
    except ValueError as e:
        print(f"  ERROR SEMANTICO: {e}")

def procesar_inicializacion_entity(tokens_inicializacion, campos_tipo):
    """
    Procesa la inicialización de una variable Entity: {campo1: valor1, campo2: valor2}
    """
    valores = {}
    dentro_del_bloque = False
    campo_actual = None
    
    i = 0
    while i < len(tokens_inicializacion):
        token = tokens_inicializacion[i]
        
        if token.type in ["POLLO_CRUDO", "LLAVE_ABRE"]:  # { o PolloCrudo
            dentro_del_bloque = True
            print(f"      Iniciando bloque de inicialización")
            i += 1
            continue
        elif token.type in ["POLLO_ASADO", "LLAVE_CIERRA"]:  # } o PolloAsado
            dentro_del_bloque = False
            print(f"      Finalizando bloque de inicialización")
            break
        
        if dentro_del_bloque:
            if token.type == "IDENTIFICADOR" and campo_actual is None:
                # Es el nombre de un campo
                campo_actual = token.lexema
                print(f"      Campo encontrado: {campo_actual}")
            elif token.type == "DOS_PUNTOS" and campo_actual is not None:
                # Siguiente token será el valor
                pass
            elif campo_actual is not None and token.type in ["NUMERO_ENTERO", "NUMERO_DECIMAL", "CADENA", "IDENTIFICADOR"]:
                # Es el valor del campo
                valores[campo_actual] = token.lexema
                print(f"        {campo_actual} = {token.lexema}")
                campo_actual = None
            elif token.type == "COMA":
                # Separador entre campos
                pass
            
        i += 1
    
    # Validar que los campos inicializados existan en el tipo
    for campo in valores.keys():
        if not any(c["nombre"] == campo for c in campos_tipo):
            print(f"      WARNING: Campo '{campo}' no existe en el tipo Entity")
    
    return valores