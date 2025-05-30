"""
CheckTipoOp.py

Estudiantes: Cabrera Samir, Urbina Luis

Chequeo de tipos de operación para garantizar que los operadores aritméticos
se utilicen exclusivamente con tipos de datos compatibles.

VERSIÓN CORREGIDA: Arreglado el mapeo de operadores para reconocer tanto símbolos como nombres
"""

from ..HistorialSemantico import historialSemantico
from ..TablaSimbolos import TablaSimbolos

class TipoOperacionChecker:
    """
    Clase para manejar la verificación de tipos en operaciones aritméticas
    """
    
    # Definición de tipos de datos del lenguaje Notch Engine
    TIPOS_NUMERICOS = {"STACK", "GHAST"}  # Enteros y flotantes
    TIPOS_CADENA = {"SPIDER"}  # Strings
    TIPOS_BOOLEANOS = {"TORCH"}  # Booleanos
    TIPOS_CARACTER = {"RUNE"}  # Caracteres
    TIPOS_CONJUNTO = {"CHEST"}  # Conjuntos
    TIPOS_ARCHIVO = {"BOOK"}  # Archivos
    TIPOS_PERSONALIZADOS = {"ENTITY"}  # Tipos definidos por usuario
    
    # CORREGIDO: Mapeo bidireccional de operadores (símbolo <-> nombre)
    OPERADORES_SIMBOLOS_A_NOMBRES = {
        "+": "SUMA",
        "-": "RESTA", 
        "*": "MULTIPLICACION",
        "/": "DIVISION",
        "%": "MODULO",
        ":+": "SUMA_FLOTANTE",
        ":-": "RESTA_FLOTANTE",
        ":*": "MULTIPLICACION_FLOTANTE",
        ":/": "DIVISION_FLOTANTE",
        ":%": "MODULO_FLOTANTE"
    }
    
    # NUEVO: Mapeo inverso (nombre -> símbolo) para validación
    OPERADORES_NOMBRES_A_SIMBOLOS = {v: k for k, v in OPERADORES_SIMBOLOS_A_NOMBRES.items()}
    
    # NUEVO: Conjunto unificado de operadores válidos (nombres)
    OPERADORES_VALIDOS = set(OPERADORES_SIMBOLOS_A_NOMBRES.values())
    
    # Operadores de comparación que también requieren tipos compatibles
    OPERADORES_COMPARACION = {
        "DOBLE_IGUAL": "==",
        "MENOR_QUE": "<", 
        "MAYOR_QUE": ">",
        "MENOR_IGUAL": "<=",
        "MAYOR_IGUAL": ">=",
        "IS": "is",
        "IS_NOT": "is_not"
    }

def evaluar_expresion_flotante(tokens):
    """Evalúa expresiones flotantes complejas"""
    if not tokens:
        print("ERROR: Expresión vacía")
        return None

    tabla = TablaSimbolos.instancia()
    pila = []

    for token in tokens:
        if token.type == "IDENTIFICADOR":
            simbolo = tabla.buscar(token.lexema)
            if not simbolo:
                print(f"ERROR: Identificador '{token.lexema}' no declarado")
                return None
            if simbolo.tipo != "GHAST":
                print(f"ERROR: '{token.lexema}' no es un flotante")
                return None
            pila.append((simbolo.tipo, float(simbolo.valor)))
        elif token.type == "NUMERO_DECIMAL":
            pila.append(("GHAST", float(token.lexema)))
        elif token.type in [
            "SUMA_FLOTANTE", "RESTA_FLOTANTE",
            "MULTIPLICACION_FLOTANTE", "DIVISION_FLOTANTE", "MODULO_FLOTANTE"
        ]:
            pila.append(token)
        else:
            print(f"ERROR: Token no válido en expresión: {token.lexema}")
            return None

    while len(pila) >= 3:
        (tipo1, val1) = pila.pop(0)
        operador = pila.pop(0)
        (tipo2, val2) = pila.pop(0)

        if tipo1 != tipo2:
            print(f"ERROR: No se puede operar {tipo1} con {tipo2}")
            return None

        if operador.type == "SUMA_FLOTANTE":
            resultado = val1 + val2
        elif operador.type == "RESTA_FLOTANTE":
            resultado = val1 - val2
        elif operador.type == "MULTIPLICACION_FLOTANTE":
            resultado = val1 * val2
        elif operador.type == "DIVISION_FLOTANTE":
            if val2 == 0:
                print("ERROR: División por cero.")
                return None
            resultado = val1 / val2
        elif operador.type == "MODULO_FLOTANTE":
            resultado = val1 % val2
        else:
            print(f"ERROR: Operador no reconocido: {operador.lexema}")
            return None

        pila.insert(0, (tipo1, resultado))

    if len(pila) == 1:
        return pila[0][1]  # Solo el valor
    else:
        print("ERROR: Expresión mal formada.")
        return None

def verificar_operacion_aritmetica(operando_izq, operador, operando_der, linea=None):
    """
    Verifica que una operación aritmética sea válida según los tipos de los operandos
    
    Args:
        operando_izq: Tipo del operando izquierdo ("STACK", "GHAST", etc.)
        operador: Tipo de operador ("SUMA", "RESTA", etc.) o símbolo ("+", "-", etc.)
        operando_der: Tipo del operando derecho
        linea: Línea donde ocurre la operación (opcional)
        
    Returns:
        tuple: (es_valida, tipo_resultado, mensaje_error)
    """
    # Normalizar tipos si vienen como strings
    tipo_izq = str(operando_izq).upper()
    tipo_der = str(operando_der).upper()
    op = str(operador).upper()
    
    ubicacion = f" en línea {linea}" if linea else ""
    
    # CORREGIDO: Normalizar operador a nombre si viene como símbolo
    if op in TipoOperacionChecker.OPERADORES_SIMBOLOS_A_NOMBRES:
        op = TipoOperacionChecker.OPERADORES_SIMBOLOS_A_NOMBRES[op]
    
    # CORREGIDO: Verificar si el operador es válido
    if op not in TipoOperacionChecker.OPERADORES_VALIDOS:
        # Verificar también en operadores de comparación
        if op not in TipoOperacionChecker.OPERADORES_COMPARACION:
            mensaje_error = f"REGLA SEMANTICA 040: ERROR - Operador '{operador}' no reconocido{ubicacion}"
            historialSemantico.agregar(mensaje_error)
            return False, "UNKNOWN", mensaje_error
    
    # Caso 1: Operadores flotantes específicos (:+, :-, :*, :/, :%)
    if op.endswith("_FLOTANTE"):
        return verificar_operacion_flotante(tipo_izq, op, tipo_der, linea)
    
    # Caso 2: Operadores aritméticos estándar
    elif op in ["SUMA", "RESTA", "MULTIPLICACION", "DIVISION", "MODULO"]:
        return verificar_operacion_entera(tipo_izq, op, tipo_der, linea)
    
    # Caso 3: Operadores de comparación
    elif op in TipoOperacionChecker.OPERADORES_COMPARACION:
        return verificar_operacion_comparacion(tipo_izq, op, tipo_der, linea)
    
    # Operador no reconocido
    mensaje_error = f"REGLA SEMANTICA 040: ERROR - Operador '{operador}' no reconocido{ubicacion}"
    historialSemantico.agregar(mensaje_error)
    return False, "UNKNOWN", mensaje_error

def verificar_operacion_entera(tipo_izq, operador, tipo_der, linea=None):
    """
    Verifica operaciones aritméticas estándar que trabajan principalmente con enteros
    """
    ubicacion = f" en línea {linea}" if linea else ""
    
    # CORREGIDO: Obtener símbolo del operador para display
    op_simbolo = TipoOperacionChecker.OPERADORES_NOMBRES_A_SIMBOLOS.get(operador, operador)
    
    # Caso 1: Ambos operandos son STACK (enteros) - IDEAL
    if tipo_izq == "STACK" and tipo_der == "STACK":
        mensaje = f"REGLA SEMANTICA 040: Operación {tipo_izq} {op_simbolo} {tipo_der} válida{ubicacion}"
        historialSemantico.agregar(mensaje)
        return True, "STACK", None
    
    # Caso 2: Uno es STACK y otro es GHAST - CONVERSIÓN IMPLÍCITA PERMITIDA
    if (tipo_izq == "STACK" and tipo_der == "GHAST") or (tipo_izq == "GHAST" and tipo_der == "STACK"):
        mensaje = f"REGLA SEMANTICA 040: Operación {tipo_izq} {op_simbolo} {tipo_der} válida con conversión implícita a GHAST{ubicacion}"
        historialSemantico.agregar(mensaje)
        return True, "GHAST", None
    
    # Caso 3: Ambos operandos son GHAST - VÁLIDO pero debería usar operadores flotantes
    if tipo_izq == "GHAST" and tipo_der == "GHAST":
        mensaje = f"REGLA SEMANTICA 040: WARNING - Operación {tipo_izq} {op_simbolo} {tipo_der} válida, pero se recomienda usar operadores flotantes (:+, :-, etc.){ubicacion}"
        historialSemantico.agregar(mensaje)
        return True, "GHAST", None
    
    # Caso especial: Concatenación de strings con SUMA
    if operador == "SUMA" and tipo_izq == "SPIDER" and tipo_der == "SPIDER":
        mensaje = f"REGLA SEMANTICA 040: Concatenación de strings {tipo_izq} {op_simbolo} {tipo_der} válida{ubicacion}"
        historialSemantico.agregar(mensaje)
        return True, "SPIDER", None
    
    # Caso 4: TIPOS INCOMPATIBLES - ERROR
    tipos_incompatibles = verificar_tipos_incompatibles(tipo_izq, tipo_der, operador)
    if tipos_incompatibles:
        mensaje_error = f"REGLA SEMANTICA 040: ERROR - Operación {tipo_izq} {op_simbolo} {tipo_der} inválida: {tipos_incompatibles}{ubicacion}"
        historialSemantico.agregar(mensaje_error)
        return False, "ERROR", mensaje_error
    
    # Caso 5: Otros tipos no soportados
    mensaje_error = f"REGLA SEMANTICA 040: ERROR - Operación {tipo_izq} {op_simbolo} {tipo_der} no soportada{ubicacion}"
    historialSemantico.agregar(mensaje_error)
    return False, "ERROR", mensaje_error

def verificar_operacion_flotante(tipo_izq, operador, tipo_der, linea=None):
    """
    Verifica operaciones flotantes específicas (:+, :-, :*, :/, :%)
    """
    ubicacion = f" en línea {linea}" if linea else ""
    op_simbolo = TipoOperacionChecker.OPERADORES_NOMBRES_A_SIMBOLOS.get(operador, operador)
    
    # Caso 1: Ambos operandos son GHAST (flotantes) - IDEAL
    if tipo_izq == "GHAST" and tipo_der == "GHAST":
        mensaje = f"REGLA SEMANTICA 041: Operación flotante {tipo_izq} {op_simbolo} {tipo_der} válida{ubicacion}"
        historialSemantico.agregar(mensaje)
        return True, "GHAST", None
    
    # Caso 2: Uno es GHAST y otro es STACK - CONVERSIÓN PERMITIDA
    if (tipo_izq == "GHAST" and tipo_der == "STACK") or (tipo_izq == "STACK" and tipo_der == "GHAST"):
        mensaje = f"REGLA SEMANTICA 041: Operación flotante {tipo_izq} {op_simbolo} {tipo_der} válida con conversión implícita{ubicacion}"
        historialSemantico.agregar(mensaje)
        return True, "GHAST", None
    
    # Caso 3: Ambos son STACK - VÁLIDO pero se convierte a flotante
    if tipo_izq == "STACK" and tipo_der == "STACK":
        mensaje = f"REGLA SEMANTICA 041: Operación flotante {tipo_izq} {op_simbolo} {tipo_der} válida, convertida a GHAST{ubicacion}"
        historialSemantico.agregar(mensaje)
        return True, "GHAST", None
    
    # Caso 4: TIPOS INCOMPATIBLES
    tipos_incompatibles = verificar_tipos_incompatibles(tipo_izq, tipo_der, operador)
    if tipos_incompatibles:
        mensaje_error = f"REGLA SEMANTICA 041: ERROR - Operación flotante {tipo_izq} {op_simbolo} {tipo_der} inválida: {tipos_incompatibles}{ubicacion}"
        historialSemantico.agregar(mensaje_error)
        return False, "ERROR", mensaje_error
    
    # Otros casos no soportados
    mensaje_error = f"REGLA SEMANTICA 041: ERROR - Operación flotante {tipo_izq} {op_simbolo} {tipo_der} no soportada{ubicacion}"
    historialSemantico.agregar(mensaje_error)
    return False, "ERROR", mensaje_error

def verificar_operacion_comparacion(tipo_izq, operador, tipo_der, linea=None):
    """
    Verifica operaciones de comparación entre tipos compatibles
    """
    ubicacion = f" en línea {linea}" if linea else ""
    op_simbolo = TipoOperacionChecker.OPERADORES_COMPARACION.get(operador, operador)
    
    # Caso 1: Ambos tipos son idénticos - SIEMPRE VÁLIDO
    if tipo_izq == tipo_der:
        mensaje = f"REGLA SEMANTICA 042: Comparación {tipo_izq} {op_simbolo} {tipo_der} válida{ubicacion}"
        historialSemantico.agregar(mensaje)
        return True, "TORCH", None  # Las comparaciones retornan booleano
    
    # Caso 2: Tipos numéricos compatibles (STACK y GHAST)
    if (tipo_izq in TipoOperacionChecker.TIPOS_NUMERICOS and 
        tipo_der in TipoOperacionChecker.TIPOS_NUMERICOS):
        mensaje = f"REGLA SEMANTICA 042: Comparación numérica {tipo_izq} {op_simbolo} {tipo_der} válida{ubicacion}"
        historialSemantico.agregar(mensaje)
        return True, "TORCH", None
    
    # Caso 3: Comparaciones especiales IS/IS_NOT - Más permisivas
    if operador in ["IS", "IS_NOT"]:
        mensaje = f"REGLA SEMANTICA 042: Comparación de identidad {tipo_izq} {op_simbolo} {tipo_der} válida{ubicacion}"
        historialSemantico.agregar(mensaje)
        return True, "TORCH", None
    
    # Caso 4: TIPOS INCOMPATIBLES PARA COMPARACIÓN
    mensaje_error = f"REGLA SEMANTICA 042: ERROR - Comparación {tipo_izq} {op_simbolo} {tipo_der} inválida: tipos incompatibles{ubicacion}"
    historialSemantico.agregar(mensaje_error)
    return False, "ERROR", mensaje_error

def verificar_tipos_incompatibles(tipo_izq, tipo_der, operador=None):
    """
    Verifica si dos tipos son fundamentalmente incompatibles
    
    Returns:
        str: Descripción del problema de incompatibilidad, o None si son compatibles
    """
    # CASO ESPECIAL: Para strings, solo permitir SUMA (concatenación)
    if tipo_izq == "SPIDER" or tipo_der == "SPIDER":
        if operador == "SUMA" and tipo_izq == "SPIDER" and tipo_der == "SPIDER":
            return None  # Concatenación válida
        elif operador != "SUMA":
            return f"solo se permite concatenación (+) con strings, no {operador}"
        elif tipo_izq != tipo_der:
            return "no se puede concatenar string con otro tipo"
    
    # Definir grupos de tipos incompatibles
    incompatibilidades = [
        # Números vs Cadenas (excepto suma/concatenación ya manejada arriba)
        (TipoOperacionChecker.TIPOS_NUMERICOS, TipoOperacionChecker.TIPOS_CADENA,
         "no se pueden realizar operaciones aritméticas entre números y cadenas"),
        
        # Números vs Booleanos (para aritmética)
        (TipoOperacionChecker.TIPOS_NUMERICOS, TipoOperacionChecker.TIPOS_BOOLEANOS,
         "operaciones aritméticas entre números y booleanos requieren conversión explícita"),
        
        # Cadenas vs Booleanos  
        (TipoOperacionChecker.TIPOS_CADENA, TipoOperacionChecker.TIPOS_BOOLEANOS,
         "no se pueden realizar operaciones aritméticas entre cadenas y booleanos"),
        
        # Cualquier tipo vs Conjuntos
        ({"STACK", "GHAST", "SPIDER", "TORCH", "RUNE"}, TipoOperacionChecker.TIPOS_CONJUNTO,
         "los conjuntos requieren operadores especializados"),
        
        # Cualquier tipo vs Archivos
        ({"STACK", "GHAST", "SPIDER", "TORCH", "RUNE"}, TipoOperacionChecker.TIPOS_ARCHIVO,
         "los archivos requieren operadores especializados"),
        
        # Cualquier tipo vs Tipos personalizados
        ({"STACK", "GHAST", "SPIDER", "TORCH", "RUNE"}, TipoOperacionChecker.TIPOS_PERSONALIZADOS,
         "los tipos personalizados requieren operadores definidos específicamente")
    ]
    
    # Verificar cada incompatibilidad
    for grupo1, grupo2, razon in incompatibilidades:
        if ((tipo_izq in grupo1 and tipo_der in grupo2) or 
            (tipo_izq in grupo2 and tipo_der in grupo1)):
            return razon
    
    return None

def verificar_expresion_completa(tokens_expresion, linea=None):
    """
    Verifica los tipos de una expresión completa con múltiples operaciones
    
    Args:
        tokens_expresion: Lista de tokens que forman la expresión
        linea: Línea donde ocurre la expresión
        
    Returns:
        tuple: (es_valida, tipo_resultado_final, lista_errores)
    """
    if not tokens_expresion:
        return True, "UNKNOWN", []
    
    errores = []
    pila_tipos = []  # Pila para manejar precedencia de operadores
    ubicacion = f" en línea {linea}" if linea else ""
    
    try:
        i = 0
        while i < len(tokens_expresion):
            token = tokens_expresion[i]
            
            # Si es un operando (literal o identificador)
            if es_operando(token):
                tipo_operando = inferir_tipo_operando(token)
                pila_tipos.append(tipo_operando)
                
            # Si es un operador
            elif es_operador_aritmetico(token):
                if len(pila_tipos) >= 2:
                    # Sacar los dos operandos más recientes
                    tipo_der = pila_tipos.pop()
                    tipo_izq = pila_tipos.pop()
                    
                    # Verificar la operación
                    es_valida, tipo_resultado, error = verificar_operacion_aritmetica(
                        tipo_izq, token.type, tipo_der, linea
                    )
                    
                    if not es_valida:
                        errores.append(error)
                        # Continuar con tipo de error para no romper el análisis
                        pila_tipos.append("ERROR")
                    else:
                        pila_tipos.append(tipo_resultado)
                        
                else:
                    error = f"REGLA SEMANTICA 043: ERROR - Operador '{token.lexema}' sin suficientes operandos{ubicacion}"
                    errores.append(error)
                    historialSemantico.agregar(error)
            
            i += 1
        
        # El resultado final es el tipo que queda en la pila
        if pila_tipos:
            tipo_final = pila_tipos[-1] if pila_tipos[-1] != "ERROR" else "UNKNOWN"
            
            if not errores:
                mensaje = f"REGLA SEMANTICA 043: Expresión analizada correctamente, tipo resultado: {tipo_final}{ubicacion}"
                historialSemantico.agregar(mensaje)
            
            return len(errores) == 0, tipo_final, errores
        else:
            return True, "UNKNOWN", errores
            
    except Exception as e:
        error = f"REGLA SEMANTICA 043: ERROR al analizar expresión: {str(e)}{ubicacion}"
        errores.append(error)
        historialSemantico.agregar(error)
        return False, "ERROR", errores

def es_operando(token):
    """Verifica si un token es un operando (literal o identificador)"""
    if not hasattr(token, 'type'):
        return False
    
    tipos_operando = {
        "NUMERO_ENTERO", "NUMERO_DECIMAL", "CADENA", "CARACTER", 
        "ON", "OFF", "IDENTIFICADOR"
    }
    
    return token.type in tipos_operando

def es_operador_aritmetico(token):
    """Verifica si un token es un operador aritmético"""
    if not hasattr(token, 'type'):
        return False
    
    # CORREGIDO: Verificar tanto contra nombres como valores
    return token.type in TipoOperacionChecker.OPERADORES_VALIDOS

def inferir_tipo_operando(token):
    """Infiere el tipo de un operando basado en su token"""
    if not hasattr(token, 'type'):
        return "UNKNOWN"
    
    mapeo_tipos = {
        "NUMERO_ENTERO": "STACK",
        "NUMERO_DECIMAL": "GHAST", 
        "CADENA": "SPIDER",
        "CARACTER": "RUNE",
        "ON": "TORCH",
        "OFF": "TORCH"
    }
    
    if token.type in mapeo_tipos:
        return mapeo_tipos[token.type]
    elif token.type == "IDENTIFICADOR":
        # Para identificadores, necesitaríamos consultar la tabla de símbolos
        # Por ahora retornamos un tipo genérico
        return "IDENTIFICADOR"  # Se debe resolver con tabla de símbolos
    else:
        return "UNKNOWN"

def obtener_conversiones_permitidas():
    """
    Retorna un diccionario con las conversiones de tipos permitidas
    
    Returns:
        dict: Mapeo de (tipo_origen, tipo_destino) -> es_permitida
    """
    return {
        ("STACK", "GHAST"): True,   # Entero a flotante
        ("GHAST", "STACK"): False,  # Flotante a entero (pérdida de precisión)
        ("STACK", "TORCH"): True,   # Entero a booleano (0=False, !=0=True)
        ("TORCH", "STACK"): True,   # Booleano a entero (False=0, True=1)
        ("RUNE", "STACK"): True,    # Carácter a entero (código ASCII)
        ("STACK", "RUNE"): True,    # Entero a carácter (si está en rango ASCII)
        ("SPIDER", "TORCH"): True,  # String a booleano (vacío=False, no vacío=True)
        ("TORCH", "SPIDER"): True,  # Booleano a string ("On"/"Off")
    }

def sugerir_correccion_tipo(tipo_izq, operador, tipo_der):
    """
    Sugiere una corrección cuando hay un error de tipos
    
    Args:
        tipo_izq: Tipo del operando izquierdo
        operador: Operador utilizado
        tipo_der: Tipo del operando derecho
        
    Returns:
        str: Sugerencia de corrección
    """
    conversiones = obtener_conversiones_permitidas()
    
    # Sugerir conversión explícita si está permitida
    if (tipo_izq, tipo_der) in conversiones and conversiones[(tipo_izq, tipo_der)]:
        return f"Considere convertir {tipo_izq} a {tipo_der} explícitamente"
    elif (tipo_der, tipo_izq) in conversiones and conversiones[(tipo_der, tipo_izq)]:
        return f"Considere convertir {tipo_der} a {tipo_izq} explícitamente"
    
    # Sugerir operadores específicos
    if tipo_izq == "GHAST" or tipo_der == "GHAST":
        op_flotante = {
            "SUMA": ":+", "RESTA": ":-", "MULTIPLICACION": ":*", 
            "DIVISION": ":/", "MODULO": ":%" 
        }.get(operador)
        if op_flotante:
            return f"Para operaciones con flotantes, use '{op_flotante}' en lugar de '{operador}'"
    
    # Casos especiales para strings
    if tipo_izq == "SPIDER" or tipo_der == "SPIDER":
        if operador != "SUMA":
            return f"Para strings, solo use '+' para concatenación, no '{operador}'"
    
    # Sugerir verificar tipos
    return f"Verifique que ambos operandos sean del mismo tipo o tipos compatibles"