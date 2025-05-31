from ..Simbolo import Simbolo
from ..TablaSimbolos import TablaSimbolos
from ..diccionarioSemantico.CheckVarInit import checkInicializacionVariable


def welcomeSpell(actual, tokens_temporales, es_prototipo=False):
    """
    Maneja tanto prototipos como implementaciones de funciones Spell
    
    Args:
        actual: Token del identificador de la función (nombre)
        tokens_temporales: Lista de tokens hasta encontrar PUNTO_Y_COMA o final de bloque
        es_prototipo: True si es solo un prototipo, False si es implementación completa
    """
    print(f"Procesando SPELL: {actual.lexema}")
    print(f"Tokens recibidos: {len(tokens_temporales)}")
    print(f"Es prototipo: {es_prototipo}")
    
    # Debug: mostrar tokens recibidos
    for i, token in enumerate(tokens_temporales):
        print(f"  Token {i}: {token.type} -> {token.lexema}")
    
    # Verificar que la función no exista ya
    tabla = TablaSimbolos.instancia()
    funcion_existente = tabla.buscar(actual.lexema)
    
    if funcion_existente is not None:
        if es_prototipo and funcion_existente.categoria == "PROTOTIPO":
            print(f"ERROR SEMANTICO: El prototipo '{actual.lexema}' ya está declarado en línea {funcion_existente.linea}")
            return
        elif not es_prototipo and funcion_existente.categoria == "FUNCION":
            print(f"ERROR SEMANTICO: La función '{actual.lexema}' ya está implementada en línea {funcion_existente.linea}")
            return
        elif not es_prototipo and funcion_existente.categoria == "PROTOTIPO":
            print(f"  -> Implementando función previamente prototipada")
            # Validar que la signatura coincida
            if not validar_signatura_coincide(funcion_existente, tokens_temporales):
                print(f"ERROR SEMANTICO: La implementación de '{actual.lexema}' no coincide con su prototipo")
                return
    
    # Extraer parámetros y tipo de retorno
    parametros = extraer_parametros(tokens_temporales)
    tipo_retorno = extraer_tipo_retorno(tokens_temporales)
    tiene_implementacion = tiene_bloque_implementacion(tokens_temporales)
    
    print(f"  Parámetros extraídos: {len(parametros)}")
    for i, param in enumerate(parametros):
        print(f"    Param {i}: {param['nombre']} ({param['tipo']})")
    print(f"  Tipo de retorno: {tipo_retorno}")
    print(f"  Tiene implementación: {tiene_implementacion}")
    
    # Determinar categoría
    if es_prototipo or not tiene_implementacion:
        categoria = "PROTOTIPO"
    else:
        categoria = "FUNCION"
    
    # Crear el símbolo
    simbolo_funcion = Simbolo(
        nombre=actual.lexema,
        tipo=tipo_retorno,
        categoria=categoria,
        linea=actual.linea,
        columna=actual.columna,
        valor={
            "parametros": parametros,
            "tipo_retorno": tipo_retorno,
            "tiene_implementacion": tiene_implementacion
        }
    )
    
    print(f"  Simbolo SPELL creado:")
    print(f"    Nombre: {simbolo_funcion.nombre}")
    print(f"    Tipo: {simbolo_funcion.tipo}")
    print(f"    Categoria: {simbolo_funcion.categoria}")
    print(f"    Parámetros: {len(parametros)}")
    
    # Insertar o actualizar en la tabla de símbolos
    try:
        if funcion_existente and funcion_existente.categoria == "PROTOTIPO" and categoria == "FUNCION":
            # Actualizar prototipo a función implementada
            tabla.eliminar(actual.lexema)
            checkInicializacionVariable(simbolo_funcion)
            tabla.insertar(simbolo_funcion)
            print(f"  SPELL '{actual.lexema}' actualizado de prototipo a función implementada")
        else:
            checkInicializacionVariable(simbolo_funcion)
            tabla.insertar(simbolo_funcion)
            print(f"  SPELL '{actual.lexema}' insertado correctamente como {categoria}")
    except ValueError as e:
        print(f"  ERROR SEMANTICO: {e}")

def extraer_parametros(tokens_temporales):
    """
    Extrae los parámetros de la declaración de función
    Formato: ( tipo :: id, id, ... , tipo :: id, ... )
    """
    parametros = []
    dentro_parentesis = False
    tipo_actual = None
    i = 0
    
    while i < len(tokens_temporales):
        token = tokens_temporales[i]
        
        if token.type == "PARENTESIS_ABRE":
            dentro_parentesis = True
            i += 1
            continue
        elif token.type == "PARENTESIS_CIERRA":
            dentro_parentesis = False
            break
        
        if dentro_parentesis:
            # Buscar tipo :: identificadores
            if token.type in ["STACK", "SPIDER", "RUNE", "TORCH", "GHAST", "CHEST", "BOOK", "SHELF", "ENTITY"]:
                tipo_actual = token.type
                print(f"    Tipo de parámetro encontrado: {tipo_actual}")
                
                # Verificar :: después del tipo
                if (i + 2 < len(tokens_temporales) and 
                    tokens_temporales[i + 1].type == "DOS_PUNTOS" and 
                    tokens_temporales[i + 2].type == "DOS_PUNTOS"):
                    
                    i += 3  # Saltar tipo y ::
                    
                    # Recoger identificadores hasta la coma o fin
                    while i < len(tokens_temporales):
                        if tokens_temporales[i].type == "IDENTIFICADOR":
                            parametro = {
                                "nombre": tokens_temporales[i].lexema,
                                "tipo": tipo_actual,
                                "linea": tokens_temporales[i].linea,
                                "columna": tokens_temporales[i].columna
                            }
                            parametros.append(parametro)
                            print(f"      Parámetro: {parametro['nombre']} ({parametro['tipo']})")
                            i += 1
                            
                            # Saltar coma si existe
                            if (i < len(tokens_temporales) and 
                                tokens_temporales[i].type == "COMA"):
                                i += 1
                                
                                # Si después de la coma viene otro tipo, salir del bucle
                                if (i < len(tokens_temporales) and 
                                    tokens_temporales[i].type in ["STACK", "SPIDER", "RUNE", "TORCH", "GHAST", "CHEST", "BOOK", "SHELF", "ENTITY"]):
                                    break
                        else:
                            break
                else:
                    i += 1
            else:
                i += 1
        else:
            i += 1
    
    return parametros

def extraer_tipo_retorno(tokens_temporales):
    """
    Extrae el tipo de retorno después de FLECHA
    """
    for i, token in enumerate(tokens_temporales):
        if token.type == "FLECHA" and i + 1 < len(tokens_temporales):
            siguiente = tokens_temporales[i + 1]
            if siguiente.type in ["STACK", "SPIDER", "RUNE", "TORCH", "GHAST", "CHEST", "BOOK", "SHELF", "ENTITY"]:
                print(f"    Tipo de retorno encontrado: {siguiente.type}")
                return siguiente.type
    
    print(f"    WARNING: No se encontró tipo de retorno válido")
    return "VOID"

def tiene_bloque_implementacion(tokens_temporales):
    """
    Verifica si la función tiene un bloque de implementación (PolloCrudo...PolloAsado)
    """
    for token in tokens_temporales:
        if token.type == "POLLO_CRUDO":
            return True
    return False

def validar_signatura_coincide(prototipo_existente, tokens_nuevos):
    """
    Valida que la signatura de la implementación coincida con el prototipo
    """
    nuevos_parametros = extraer_parametros(tokens_nuevos)
    nuevo_tipo_retorno = extraer_tipo_retorno(tokens_nuevos)
    
    parametros_prototipo = prototipo_existente.valor.get("parametros", [])
    tipo_retorno_prototipo = prototipo_existente.valor.get("tipo_retorno", "VOID")
    
    # Verificar tipo de retorno
    if nuevo_tipo_retorno != tipo_retorno_prototipo:
        print(f"    ERROR: Tipo de retorno no coincide. Prototipo: {tipo_retorno_prototipo}, Implementación: {nuevo_tipo_retorno}")
        return False
    
    # Verificar cantidad de parámetros
    if len(nuevos_parametros) != len(parametros_prototipo):
        print(f"    ERROR: Cantidad de parámetros no coincide. Prototipo: {len(parametros_prototipo)}, Implementación: {len(nuevos_parametros)}")
        return False
    
    # Verificar cada parámetro
    for i, (param_proto, param_nuevo) in enumerate(zip(parametros_prototipo, nuevos_parametros)):
        if param_proto["tipo"] != param_nuevo["tipo"]:
            print(f"    ERROR: Tipo del parámetro {i} no coincide. Prototipo: {param_proto['tipo']}, Implementación: {param_nuevo['tipo']}")
            return False
        if param_proto["nombre"] != param_nuevo["nombre"]:
            print(f"    ERROR: Nombre del parámetro {i} no coincide. Prototipo: {param_proto['nombre']}, Implementación: {param_nuevo['nombre']}")
            return False
    
    print(f"    Signatura coincide correctamente")
    return True

def verificar_llamada_funcion(nombre_funcion, argumentos):
    """
    Verifica que una llamada a función sea válida
    
    Args:
        nombre_funcion: Nombre de la función a llamar
        argumentos: Lista de tipos de los argumentos pasados
    """
    tabla = TablaSimbolos.instancia()
    funcion = tabla.buscar(nombre_funcion)
    
    if funcion is None:
        print(f"ERROR SEMANTICO: La función '{nombre_funcion}' no está declarada")
        return False
    
    if funcion.categoria not in ["FUNCION", "PROTOTIPO"]:
        print(f"ERROR SEMANTICO: '{nombre_funcion}' no es una función")
        return False
    
    parametros_esperados = funcion.valor.get("parametros", [])
    
    # Verificar cantidad de argumentos
    if len(argumentos) != len(parametros_esperados):
        print(f"ERROR SEMANTICO: La función '{nombre_funcion}' espera {len(parametros_esperados)} argumentos, pero se pasaron {len(argumentos)}")
        return False
    
    # Verificar tipos de argumentos
    for i, (param_esperado, tipo_argumento) in enumerate(zip(parametros_esperados, argumentos)):
        if param_esperado["tipo"] != tipo_argumento:
            print(f"ERROR SEMANTICO: El argumento {i} de '{nombre_funcion}' debe ser de tipo {param_esperado['tipo']}, pero se pasó {tipo_argumento}")
            return False
    
    print(f"Llamada a función '{nombre_funcion}' es válida")
    return True

def extraer_tipos_argumentos_llamada(tokens_temporales):
    """
    Extrae los tipos de los argumentos en una llamada a función
    Formato: ( arg1, arg2, arg3, ... )
    
    Args:
        tokens_temporales: Lista de tokens de la llamada
        
    Returns:
        Lista de tipos inferidos de los argumentos
    """
    tipos_argumentos = []
    dentro_parentesis = False
    i = 0
    
    print(f"    Extrayendo tipos de argumentos de llamada:")
    
    while i < len(tokens_temporales):
        token = tokens_temporales[i]
        
        if token.type == "PARENTESIS_ABRE":
            dentro_parentesis = True
            i += 1
            continue
        elif token.type == "PARENTESIS_CIERRA":
            dentro_parentesis = False
            break
        
        if dentro_parentesis:
            # CORRECCIÓN: Solo procesar tokens que NO sean comas
            if token.type != "COMA":
                tipo_argumento = inferir_tipo_argumento(token)
                if tipo_argumento and tipo_argumento != "UNKNOWN":
                    tipos_argumentos.append(tipo_argumento)
                    print(f"      Argumento: {token.lexema} -> {tipo_argumento}")
                
        i += 1
    
    print(f"    Total argumentos encontrados: {len(tipos_argumentos)}")
    return tipos_argumentos

def inferir_tipo_argumento(token):
    """
    Infiere el tipo de un argumento basado en su token
    
    Args:
        token: Token del argumento
        
    Returns:
        Tipo inferido del argumento
    """
    if token.type == "NUMERO_ENTERO":
        return "STACK"
    elif token.type == "NUMERO_DECIMAL":
        return "GHAST"
    elif token.type == "CADENA":
        return "SPIDER"
    elif token.type == "CARACTER":
        return "RUNE"
    elif token.type in ["ON", "OFF"]:
        return "TORCH"
    elif token.type == "IDENTIFICADOR":
        # Para identificadores, necesitamos buscar en la tabla de símbolos
        tabla = TablaSimbolos.instancia()
        simbolo = tabla.buscar(token.lexema)
        if simbolo:
            return simbolo.tipo
        else:
            print(f"      WARNING: Variable '{token.lexema}' no declarada, asumiendo tipo STACK")
            return "STACK"
    elif token.type == "LLAVE_ABRE":
        # Podría ser un conjunto, archivo, o estructura
        return "CHEST"  # Por defecto, asumimos conjunto
    
    # Para otros casos, intentar mapear tokens a tipos
    token_to_type_map = {
        "STACK": "STACK",
        "SPIDER": "SPIDER", 
        "RUNE": "RUNE",
        "TORCH": "TORCH",
        "GHAST": "GHAST",
        "CHEST": "CHEST",
        "BOOK": "BOOK",
        "SHELF": "SHELF",
        "ENTITY": "ENTITY"
    }
    
    return token_to_type_map.get(token.type, "UNKNOWN")

def procesar_llamada_funcion_en_expresion(nombre_funcion, argumentos_tokens):
    """
    Procesa una llamada a función dentro de una expresión
    
    Args:
        nombre_funcion: Nombre de la función llamada
        argumentos_tokens: Tokens de los argumentos
        
    Returns:
        Tipo de retorno de la función si es válida, None si hay error
    """
    tabla = TablaSimbolos.instancia()
    funcion = tabla.buscar(nombre_funcion)
    
    if funcion is None:
        print(f"ERROR SEMANTICO: La función '{nombre_funcion}' no está declarada")
        return None
    
    if funcion.categoria not in ["FUNCION", "PROTOTIPO"]:
        print(f"ERROR SEMANTICO: '{nombre_funcion}' no es una función")
        return None
    
    # Extraer tipos de argumentos
    tipos_argumentos = extraer_tipos_argumentos_llamada(argumentos_tokens)
    
    # Verificar la llamada
    if verificar_llamada_funcion(nombre_funcion, tipos_argumentos):
        tipo_retorno = funcion.valor.get("tipo_retorno", "VOID")
        print(f"    Función '{nombre_funcion}' retorna tipo: {tipo_retorno}")
        return tipo_retorno
    
    return None