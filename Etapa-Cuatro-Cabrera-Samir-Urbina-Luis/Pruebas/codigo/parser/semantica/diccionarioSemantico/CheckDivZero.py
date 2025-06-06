"""
CheckDivZero.py

Estudiante: Cabrera Samir, Urbina Luis

Chequeo de división por cero para las operaciones aritméticas de Notch Engine.

Basado en el análisis de los programas ASM que muestran verificaciones explícitas
de división por cero antes de ejecutar operaciones DIV y MOD.
"""

from ..HistorialSemantico import historialSemantico

def check_division_zero(divisor, operacion="división", linea=None, nombre_variable=None):
    """
    Verifica si el divisor es cero antes de una operación de división
    
    Args:
        divisor: Valor del divisor a verificar
        operacion: Tipo de operación ("división", "modulo", "div-asignacion", etc.)
        linea: Línea donde ocurre la operación (opcional)
        nombre_variable: Nombre de la variable involucrada (opcional)
    
    Returns:
        tuple: (es_valido, mensaje_error)
    """
    try:
        # Convertir divisor a número si es string
        if isinstance(divisor, str):
            if divisor.lower() in ['off', 'false']:
                divisor_num = 0
            elif divisor.lower() in ['on', 'true']:
                divisor_num = 1
            else:
                divisor_num = float(divisor)
        elif isinstance(divisor, bool):
            divisor_num = 1 if divisor else 0
        else:
            divisor_num = float(divisor)
        
        # Verificar si es cero (considerando tolerancia para flotantes)
        if abs(divisor_num) < 1e-10:  # Prácticamente cero
            ubicacion = f" en línea {linea}" if linea else ""
            variable = f" (variable: {nombre_variable})" if nombre_variable else ""
            mensaje_error = f"REGLA SEMANTICA 020: ERROR - División por cero detectada en {operacion}{ubicacion}{variable}"
            historialSemantico.agregar(mensaje_error)
            return False, mensaje_error
        else:
            ubicacion = f" en línea {linea}" if linea else ""
            variable = f" (variable: {nombre_variable})" if nombre_variable else ""
            mensaje = f"REGLA SEMANTICA 020: Divisor {divisor_num} válido para {operacion}{ubicacion}{variable}"
            historialSemantico.agregar(mensaje)
            return True, None
            
    except (ValueError, TypeError):
        ubicacion = f" en línea {linea}" if linea else ""
        variable = f" (variable: {nombre_variable})" if nombre_variable else ""
        mensaje_error = f"REGLA SEMANTICA 020: ERROR - Divisor '{divisor}' no es un valor numérico válido{ubicacion}{variable}"
        historialSemantico.agregar(mensaje_error)
        return False, mensaje_error

def check_integer_division_zero(divisor, linea=None, nombre_variable=None):
    """
    Verifica división por cero específicamente para enteros (STACK)
    
    Args:
        divisor: Valor del divisor entero
        linea: Línea donde ocurre la operación (opcional)
        nombre_variable: Nombre de la variable (opcional)
    
    Returns:
        tuple: (es_valido, mensaje_error)
    """
    return check_division_zero(divisor, "división entera", linea, nombre_variable)

def check_float_division_zero(divisor, linea=None, nombre_variable=None):
    """
    Verifica división por cero específicamente para flotantes (GHAST)
    
    Args:
        divisor: Valor del divisor flotante (puede ser tuple (entero, decimal))
        linea: Línea donde ocurre la operación (opcional)
        nombre_variable: Nombre de la variable (opcional)
    
    Returns:
        tuple: (es_valido, mensaje_error)
    """
    try:
        # Si es un flotante representado como tupla (entero, decimal)
        if isinstance(divisor, tuple) and len(divisor) == 2:
            entero, decimal = divisor
            # Convertir a flotante: entero.decimal
            divisor_val = float(f"{entero}.{decimal:02d}")
        else:
            divisor_val = divisor
        
        return check_division_zero(divisor_val, "división flotante", linea, nombre_variable)
        
    except (ValueError, TypeError):
        ubicacion = f" en línea {linea}" if linea else ""
        variable = f" (variable: {nombre_variable})" if nombre_variable else ""
        mensaje_error = f"REGLA SEMANTICA 021: ERROR - Divisor flotante '{divisor}' no válido{ubicacion}{variable}"
        historialSemantico.agregar(mensaje_error)
        return False, mensaje_error

def check_modulo_zero(divisor, linea=None, nombre_variable=None):
    """
    Verifica división por cero específicamente para operación módulo
    
    Args:
        divisor: Valor del divisor para la operación módulo
        linea: Línea donde ocurre la operación (opcional)
        nombre_variable: Nombre de la variable (opcional)
    
    Returns:
        tuple: (es_valido, mensaje_error)
    """
    return check_division_zero(divisor, "operación módulo", linea, nombre_variable)

def check_integer_modulo_zero(divisor, linea=None, nombre_variable=None):
    """
    Verifica división por cero para módulo de enteros (STACK % STACK)
    
    Args:
        divisor: Valor del divisor entero
        linea: Línea donde ocurre la operación (opcional)
        nombre_variable: Nombre de la variable (opcional)
    
    Returns:
        tuple: (es_valido, mensaje_error)
    """
    return check_division_zero(divisor, "módulo entero", linea, nombre_variable)

def check_float_modulo_zero(divisor, linea=None, nombre_variable=None):
    """
    Verifica división por cero para módulo de flotantes (GHAST :% GHAST)
    
    Args:
        divisor: Valor del divisor flotante
        linea: Línea donde ocurre la operación (opcional)
        nombre_variable: Nombre de la variable (opcional)
    
    Returns:
        tuple: (es_valido, mensaje_error)
    """
    try:
        # Si es un flotante representado como tupla (entero, decimal)
        if isinstance(divisor, tuple) and len(divisor) == 2:
            entero, decimal = divisor
            # Convertir a flotante: entero.decimal
            divisor_val = float(f"{entero}.{decimal:02d}")
        else:
            divisor_val = divisor
        
        return check_division_zero(divisor_val, "módulo flotante", linea, nombre_variable)
        
    except (ValueError, TypeError):
        ubicacion = f" en línea {linea}" if linea else ""
        variable = f" (variable: {nombre_variable})" if nombre_variable else ""
        mensaje_error = f"REGLA SEMANTICA 022: ERROR - Divisor para módulo flotante '{divisor}' no válido{ubicacion}{variable}"
        historialSemantico.agregar(mensaje_error)
        return False, mensaje_error

def check_assignment_division_zero(divisor, operador, linea=None, nombre_variable=None):
    """
    Verifica división por cero en operaciones de asignación (//=, %=, ://=, :%=)
    
    Args:
        divisor: Valor del divisor
        operador: Tipo de operador ("//=", "%=", "://=", ":%=")
        linea: Línea donde ocurre la operación (opcional)
        nombre_variable: Nombre de la variable que se modifica (opcional)
    
    Returns:
        tuple: (es_valido, mensaje_error)
    """
    operacion_map = {
        "//=": "asignación con división entera",
        "%=": "asignación con módulo entero", 
        "://=": "asignación con división flotante",
        ":%=": "asignación con módulo flotante"
    }
    
    operacion = operacion_map.get(operador, f"asignación con {operador}")
    return check_division_zero(divisor, operacion, linea, nombre_variable)

def check_expression_division_zero(expresion_tokens, linea=None):
    """
    Analiza una expresión completa buscando divisiones por cero
    
    Args:
        expresion_tokens: Lista de tokens que representan la expresión
        linea: Línea donde ocurre la expresión (opcional)
    
    Returns:
        tuple: (es_valido, lista_errores)
    """
    errores = []
    es_valido = True
    
    try:
        # Buscar operadores de división y módulo
        operadores_division = ["/", "//", "%", ":/", "://", ":%"]
        
        for i, token in enumerate(expresion_tokens):
            if hasattr(token, 'type') and hasattr(token, 'lexema'):
                # Es un token del scanner
                token_value = token.lexema
            else:
                # Es un string simple
                token_value = str(token)
            
            if token_value in operadores_division:
                # Verificar el siguiente token (divisor)
                if i + 1 < len(expresion_tokens):
                    siguiente_token = expresion_tokens[i + 1]
                    
                    if hasattr(siguiente_token, 'lexema'):
                        divisor_value = siguiente_token.lexema
                    else:
                        divisor_value = str(siguiente_token)
                    
                    # Determinar tipo de operación
                    if token_value in [":/", "://", ":%"]:
                        operacion = f"{token_value} (flotante)"
                    else:
                        operacion = f"{token_value} (entero)"
                    
                    # Verificar división por cero
                    valido, error = check_division_zero(divisor_value, operacion, linea)
                    
                    if not valido:
                        es_valido = False
                        errores.append(error)
        
        if es_valido:
            mensaje = f"REGLA SEMANTICA 023: Expresión verificada sin divisiones por cero"
            if linea:
                mensaje += f" en línea {linea}"
            historialSemantico.agregar(mensaje)
        
        return es_valido, errores
        
    except Exception as e:
        mensaje_error = f"REGLA SEMANTICA 023: ERROR al analizar expresión para división por cero: {str(e)}"
        if linea:
            mensaje_error += f" en línea {linea}"
        historialSemantico.agregar(mensaje_error)
        return False, [mensaje_error]

def check_function_call_division_zero(nombre_funcion, argumentos, linea=None):
    """
    Verifica división por cero en llamadas a funciones que podrían realizar divisiones
    
    Args:
        nombre_funcion: Nombre de la función llamada
        argumentos: Lista de argumentos pasados a la función
        linea: Línea donde ocurre la llamada (opcional)
    
    Returns:
        tuple: (es_valido, lista_errores)
    """
    errores = []
    es_valido = True
    
    # Funciones que sabemos que realizan divisiones
    funciones_division = {
        'dividir': [1],  # Índice del argumento que es divisor
        'modulo': [1],
        'division_flotante': [1],
        'promedio': [],  # Divide por cantidad de elementos
    }
    
    if nombre_funcion.lower() in funciones_division:
        indices_divisor = funciones_division[nombre_funcion.lower()]
        
        for indice in indices_divisor:
            if indice < len(argumentos):
                divisor = argumentos[indice]
                valido, error = check_division_zero(
                    divisor, 
                    f"función {nombre_funcion}", 
                    linea
                )
                
                if not valido:
                    es_valido = False
                    errores.append(error)
        
        # Caso especial para funciones como 'promedio' que dividen por cantidad
        if nombre_funcion.lower() == 'promedio' and len(argumentos) == 0:
            mensaje_error = f"REGLA SEMANTICA 024: ERROR - Función 'promedio' llamada sin argumentos (división por cero implícita)"
            if linea:
                mensaje_error += f" en línea {linea}"
            historialSemantico.agregar(mensaje_error)
            errores.append(mensaje_error)
            es_valido = False
    
    return es_valido, errores

def get_division_safe_value(tipo_dato):
    """
    Obtiene un valor seguro (no cero) para usar como divisor por defecto
    
    Args:
        tipo_dato: Tipo de dato ("STACK", "GHAST", etc.)
    
    Returns:
        Valor seguro para usar como divisor
    """
    tipo_upper = tipo_dato.upper()
    
    if tipo_upper == "STACK":
        return 1  # Entero 1
    elif tipo_upper == "GHAST":
        return (1, 0)  # Flotante 1.00
    elif tipo_upper == "TORCH":
        return True  # Booleano verdadero (1)
    else:
        return 1  # Por defecto