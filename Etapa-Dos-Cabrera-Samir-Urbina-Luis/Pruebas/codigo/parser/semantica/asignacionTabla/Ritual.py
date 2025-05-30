# Crear este archivo como: semantica/asignacionTabla/Ritual.py

from ..Simbolo import Simbolo
from ..TablaSimbolos import TablaSimbolos

def welcomeRitual(actual, tokens_temporales, es_prototipo=False):
    """
    Maneja tanto prototipos como implementaciones de procedimientos Ritual
    """
    print(f"Procesando RITUAL: {actual.lexema}")
    print(f"Tokens recibidos: {len(tokens_temporales)}")
    print(f"Es prototipo: {es_prototipo}")
    
    # Debug: mostrar tokens recibidos
    for i, token in enumerate(tokens_temporales):
        print(f"  Token {i}: {token.type} -> {token.lexema}")
    
    # VERIFICACIÓN CRÍTICA: Los procedimientos NO deben tener tipo de retorno
    if tiene_tipo_retorno(tokens_temporales):
        print(f"ERROR SEMANTICO: El procedimiento '{actual.lexema}' no puede tener tipo de retorno. Los procedimientos no retornan valores.")
        return
    
    # Verificar que el procedimiento no exista ya
    tabla = TablaSimbolos.instancia()
    procedimiento_existente = tabla.buscar(actual.lexema)
    
    if procedimiento_existente is not None:
        if es_prototipo and procedimiento_existente.categoria == "PROTOTIPO_PROC":
            print(f"ERROR SEMANTICO: El prototipo de procedimiento '{actual.lexema}' ya está declarado en línea {procedimiento_existente.linea}")
            return
        elif not es_prototipo and procedimiento_existente.categoria == "PROCEDIMIENTO":
            print(f"ERROR SEMANTICO: El procedimiento '{actual.lexema}' ya está implementado en línea {procedimiento_existente.linea}")
            return
        elif not es_prototipo and procedimiento_existente.categoria == "PROTOTIPO_PROC":
            print(f"  -> Implementando procedimiento previamente prototipado")
            if not validar_signatura_proc_coincide(procedimiento_existente, tokens_temporales):
                print(f"ERROR SEMANTICO: La implementación de '{actual.lexema}' no coincide con su prototipo")
                return
    
    # Extraer parámetros
    parametros = extraer_parametros_procedimiento(tokens_temporales)
    tiene_implementacion = tiene_bloque_implementacion(tokens_temporales)
    
    print(f"  Parámetros extraídos: {len(parametros)}")
    for i, param in enumerate(parametros):
        print(f"    Param {i}: {param['nombre']} ({param['tipo']})")
    print(f"  Tiene implementación: {tiene_implementacion}")
    
    # Determinar categoría
    if es_prototipo or not tiene_implementacion:
        categoria = "PROTOTIPO_PROC"
    else:
        categoria = "PROCEDIMIENTO"
    
    # Crear el símbolo
    simbolo_procedimiento = Simbolo(
        nombre=actual.lexema,
        tipo="VOID",
        categoria=categoria,
        linea=actual.linea,
        columna=actual.columna,
        valor={
            "parametros": parametros,
            "tipo_retorno": "VOID",
            "tiene_implementacion": tiene_implementacion
        }
    )
    
    print(f"  Simbolo RITUAL creado:")
    print(f"    Nombre: {simbolo_procedimiento.nombre}")
    print(f"    Tipo: {simbolo_procedimiento.tipo}")
    print(f"    Categoria: {simbolo_procedimiento.categoria}")
    print(f"    Parámetros: {len(parametros)}")
    
    # Insertar o actualizar en la tabla de símbolos
    try:
        if procedimiento_existente and procedimiento_existente.categoria == "PROTOTIPO_PROC" and categoria == "PROCEDIMIENTO":
            tabla.eliminar(actual.lexema)
            tabla.insertar(simbolo_procedimiento)
            print(f"  RITUAL '{actual.lexema}' actualizado de prototipo a procedimiento implementado")
        else:
            tabla.insertar(simbolo_procedimiento)
            print(f"  RITUAL '{actual.lexema}' insertado correctamente como {categoria}")
    except ValueError as e:
        print(f"  ERROR SEMANTICO: {e}")

def extraer_parametros_procedimiento(tokens_temporales):
    """Extrae los parámetros de la declaración de procedimiento"""
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

def tiene_tipo_retorno(tokens_temporales):
    """Verifica si hay un tipo de retorno (FLECHA) en la declaración"""
    for token in tokens_temporales:
        if token.type == "FLECHA":
            return True
    return False

def tiene_bloque_implementacion(tokens_temporales):
    """Verifica si el procedimiento tiene un bloque de implementación"""
    for token in tokens_temporales:
        if token.type == "POLLO_CRUDO":
            return True
    return False

def validar_signatura_proc_coincide(prototipo_existente, tokens_nuevos):
    """Valida que la signatura de la implementación coincida con el prototipo"""
    nuevos_parametros = extraer_parametros_procedimiento(tokens_nuevos)
    parametros_prototipo = prototipo_existente.valor.get("parametros", [])
    
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
    
    print(f"    Signatura del procedimiento coincide correctamente")
    return True

def verificar_llamada_procedimiento(nombre_procedimiento, argumentos):
    """Verifica que una llamada a procedimiento sea válida"""
    tabla = TablaSimbolos.instancia()
    procedimiento = tabla.buscar(nombre_procedimiento)
    
    if procedimiento is None:
        print(f"ERROR SEMANTICO: El procedimiento '{nombre_procedimiento}' no está declarado")
        return False
    
    if procedimiento.categoria not in ["PROCEDIMIENTO", "PROTOTIPO_PROC"]:
        print(f"ERROR SEMANTICO: '{nombre_procedimiento}' no es un procedimiento")
        return False
    
    parametros_esperados = procedimiento.valor.get("parametros", [])
    
    # Verificar cantidad de argumentos
    if len(argumentos) != len(parametros_esperados):
        print(f"ERROR SEMANTICO: El procedimiento '{nombre_procedimiento}' espera {len(parametros_esperados)} argumentos, pero se pasaron {len(argumentos)}")
        return False
    
    # Verificar tipos de argumentos
    for i, (param_esperado, tipo_argumento) in enumerate(zip(parametros_esperados, argumentos)):
        if param_esperado["tipo"] != tipo_argumento:
            print(f"ERROR SEMANTICO: El argumento {i} de '{nombre_procedimiento}' debe ser de tipo {param_esperado['tipo']}, pero se pasó {tipo_argumento}")
            return False
    
    # Filtro para argumentos desconocidos
    for i, tipo in enumerate(argumentos):
        if tipo == "UNKNOWN":
            print(f"ERROR SEMANTICO: El tipo del argumento {i} no se pudo determinar.")
            return False
    
    print(f"Llamada a procedimiento '{nombre_procedimiento}' es válida")
    return True

def extraer_tipos_argumentos_llamada_proc(tokens_temporales):
    """Extrae los tipos de los argumentos en una llamada a procedimiento"""
    tipos_argumentos = []
    dentro_parentesis = False
    i = 0
    
    print(f"    Extrayendo tipos de argumentos de llamada a procedimiento:")
    
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
            if token.type != "COMA":
                tipo_argumento = inferir_tipo_argumento(token)
                if tipo_argumento and tipo_argumento != "UNKNOWN":
                    tipos_argumentos.append(tipo_argumento)
                    print(f"      Argumento: {token.lexema} -> {tipo_argumento}")
                
        i += 1
    
    print(f"    Total argumentos encontrados: {len(tipos_argumentos)}")
    return tipos_argumentos

def inferir_tipo_argumento(token):
    """Infiere el tipo de un argumento basado en su token"""
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
        tabla = TablaSimbolos.instancia()
        simbolo = tabla.buscar(token.lexema)
        if simbolo:
            return simbolo.tipo
        else:
            print(f"      ERROR: Variable '{token.lexema}' no declarada.")
            return "UNKNOWN"  # CAMBIO CLAVE: antes decía STACK
    elif token.type == "LLAVE_ABRE":
        return "CHEST"
    
    token_to_type_map = {
        "STACK": "STACK", "SPIDER": "SPIDER", "RUNE": "RUNE",
        "TORCH": "TORCH", "GHAST": "GHAST", "CHEST": "CHEST",
        "BOOK": "BOOK", "SHELF": "SHELF", "ENTITY": "ENTITY"
    }
    
    return token_to_type_map.get(token.type, "UNKNOWN")

def procesar_llamada_procedimiento_en_statement(nombre_procedimiento, argumentos_tokens):
    """Procesa una llamada a procedimiento dentro de un statement"""
    tabla = TablaSimbolos.instancia()
    procedimiento = tabla.buscar(nombre_procedimiento)
    
    if procedimiento is None:
        print(f"ERROR SEMANTICO: El procedimiento '{nombre_procedimiento}' no está declarado")
        return False
    
    if procedimiento.categoria not in ["PROCEDIMIENTO", "PROTOTIPO_PROC"]:
        print(f"ERROR SEMANTICO: '{nombre_procedimiento}' no es un procedimiento")
        return False
    
    # Extraer tipos de argumentos
    tipos_argumentos = extraer_tipos_argumentos_llamada_proc(argumentos_tokens)
    
    # Verificar la llamada
    if verificar_llamada_procedimiento(nombre_procedimiento, tipos_argumentos):
        print(f"    Procedimiento '{nombre_procedimiento}' llamado correctamente")
        return True
    
    return False

def detectar_llamada_con_asignacion(tokens_history):
    """Detecta si se está intentando asignar el resultado de un procedimiento"""
    if len(tokens_history) >= 2:
        for i in range(len(tokens_history) - 1):
            if (tokens_history[i].type == "IDENTIFICADOR" and 
                tokens_history[i + 1].type == "IGUAL"):
                return True
    return False