"""
CheckOverflow.py

Chequeo de desbordamiento (overflow) para los tipos de datos de Notch Engine.

Estudiante: Cabrera Samir, Urbina Luis

Basado en el análisis de los programas ASM:
- STACK (enteros): 16 bits con signo (-32,768 a 32,767) - usa DW (Word)
- GHAST (flotantes): 16 bits entero + 16 bits decimal
- SPIDER (strings): Máximo 80 caracteres por buffer
- RUNE (char): 8 bits (1 byte) - valores ASCII 0-255
- TORCH (bool): 8 bits (0 o 1)
- CHEST (conjuntos): Limitado por memoria y estructura
"""

from ..HistorialSemantico import historialSemantico

def check_stack_overflow(valor, nombre_variable=None):
    """
    Verifica overflow para tipo STACK (enteros de 16 bits con signo)
    Rango: -32,768 a 32,767
    
    Args:
        valor: Valor a verificar (int, str, o cualquier tipo convertible)
        nombre_variable: Nombre de la variable (opcional)
    
    Returns:
        tuple: (es_valido, valor_ajustado, mensaje_error)
    """
    try:
        # Convertir a entero si es string
        if isinstance(valor, str):
            # Manejar casos especiales de strings
            if valor.lower() in ['on', 'true']:
                valor_num = 1
            elif valor.lower() in ['off', 'false']:
                valor_num = 0
            else:
                valor_num = int(float(valor))  # Permitir decimales que se truncan
        elif isinstance(valor, float):
            valor_num = int(valor)  # Truncar parte decimal
        elif isinstance(valor, bool):
            valor_num = 1 if valor else 0
        else:
            valor_num = int(valor)
        
        # Verificar límites de 16 bits con signo
        MIN_STACK = -32768
        MAX_STACK = 32767
        
        if MIN_STACK <= valor_num <= MAX_STACK:
            nombre = f" para variable '{nombre_variable}'" if nombre_variable else ""
            mensaje = f"REGLA SEMANTICA 010: Valor {valor_num} está dentro del rango válido para STACK{nombre}"
            historialSemantico.agregar(mensaje)
            return True, valor_num, None
        else:
            # Hay overflow - aplicar wrap around (comportamiento típico de ASM)
            valor_ajustado = ((valor_num + 32768) % 65536) - 32768
            
            nombre = f" en variable '{nombre_variable}'" if nombre_variable else ""
            mensaje_error = f"REGLA SEMANTICA 010: OVERFLOW detectado{nombre}: valor {valor_num} excede rango STACK [-32768, 32767], ajustado a {valor_ajustado}"
            historialSemantico.agregar(mensaje_error)
            return False, valor_ajustado, mensaje_error
            
    except (ValueError, TypeError):
        nombre = f" para variable '{nombre_variable}'" if nombre_variable else ""
        mensaje_error = f"'{valor}' no convertible a STACK{nombre}"
        historialSemantico.agregar(mensaje_error)
        return False, 0, mensaje_error

def check_ghast_overflow(valor_entero, valor_decimal=0, nombre_variable=None):
    """
    Verifica overflow para tipo GHAST (flotantes)
    Basado en ASM: parte entera 16 bits + parte decimal 16 bits
    
    Args:
        valor_entero: Parte entera del flotante
        valor_decimal: Parte decimal del flotante
        nombre_variable: Nombre de la variable (opcional)
    
    Returns:
        tuple: (es_valido, (entero_ajustado, decimal_ajustado), mensaje_error)
    """
    try:
        # Verificar parte entera (16 bits con signo)
        MIN_ENTERO = -32768
        MAX_ENTERO = 32767
        
        # Verificar parte decimal (normalmente 0-99 para 2 dígitos)
        MAX_DECIMAL = 99
        
        entero_valido = MIN_ENTERO <= valor_entero <= MAX_ENTERO
        decimal_valido = 0 <= valor_decimal <= MAX_DECIMAL
        
        if entero_valido and decimal_valido:
            nombre = f" para variable '{nombre_variable}'" if nombre_variable else ""
            mensaje = f"REGLA SEMANTICA 011: Valor {valor_entero}.{valor_decimal:02d} está dentro del rango válido para GHAST{nombre}"
            historialSemantico.agregar(mensaje)
            return True, (valor_entero, valor_decimal), None
        else:
            # Ajustar valores con overflow
            entero_ajustado = valor_entero
            decimal_ajustado = valor_decimal
            
            if not entero_valido:
                entero_ajustado = ((valor_entero + 32768) % 65536) - 32768
            
            if not decimal_valido:
                decimal_ajustado = valor_decimal % 100
            
            nombre = f" en variable '{nombre_variable}'" if nombre_variable else ""
            mensaje_error = f"REGLA SEMANTICA 011: OVERFLOW detectado{nombre}: valor {valor_entero}.{valor_decimal} ajustado a {entero_ajustado}.{decimal_ajustado:02d}"
            historialSemantico.agregar(mensaje_error)
            return False, (entero_ajustado, decimal_ajustado), mensaje_error
            
    except (ValueError, TypeError):
        nombre = f" para variable '{nombre_variable}'" if nombre_variable else ""
        mensaje_error = f"Valores no válidos para GHAST{nombre}"
        historialSemantico.agregar(mensaje_error)
        return False, (0, 0), mensaje_error

def check_spider_overflow(cadena, nombre_variable=None):
    """
    Verifica overflow para tipo SPIDER (strings)
    Basado en ASM: buffer de 80 caracteres máximo
    
    Args:
        cadena: String a verificar
        nombre_variable: Nombre de la variable (opcional)
    
    Returns:
        tuple: (es_valido, cadena_ajustada, mensaje_error)
    """
    try:
        MAX_SPIDER_LENGTH = 80
        
        if len(cadena) <= MAX_SPIDER_LENGTH:
            nombre = f" para variable '{nombre_variable}'" if nombre_variable else ""
            mensaje = f"REGLA SEMANTICA 012: String de longitud {len(cadena)} está dentro del límite para SPIDER{nombre}"
            historialSemantico.agregar(mensaje)
            return True, cadena, None
        else:
            # Truncar string
            cadena_ajustada = cadena[:MAX_SPIDER_LENGTH]
            
            nombre = f" en variable '{nombre_variable}'" if nombre_variable else ""
            mensaje_error = f"REGLA SEMANTICA 012: OVERFLOW detectado{nombre}: String de {len(cadena)} caracteres truncado a {MAX_SPIDER_LENGTH}"
            historialSemantico.agregar(mensaje_error)
            return False, cadena_ajustada, mensaje_error
            
    except (AttributeError, TypeError):
        nombre = f" para variable '{nombre_variable}'" if nombre_variable else ""
        mensaje_error = f"Valor no es un string válido para SPIDER{nombre}"
        historialSemantico.agregar(mensaje_error)
        return False, "", mensaje_error

def check_rune_overflow(valor, nombre_variable=None):
    """
    Verifica overflow para tipo RUNE (char)
    Basado en ASM: 8 bits (0-255) valores ASCII
    
    Args:
        valor: Valor a verificar (char, int, str)
        nombre_variable: Nombre de la variable (opcional)
    
    Returns:
        tuple: (es_valido, char_ajustado, mensaje_error)
    """
    try:
        if isinstance(valor, str):
            if len(valor) == 0:
                char_code = 0  # NULL
            else:
                char_code = ord(valor[0])  # Tomar primer carácter
        elif isinstance(valor, int):
            char_code = valor
        else:
            char_code = ord(str(valor)[0])
        
        # Verificar rango ASCII extendido (8 bits)
        MIN_RUNE = 0
        MAX_RUNE = 255
        
        if MIN_RUNE <= char_code <= MAX_RUNE:
            nombre = f" para variable '{nombre_variable}'" if nombre_variable else ""
            mensaje = f"REGLA SEMANTICA 013: Código ASCII {char_code} ('{chr(char_code)}') válido para RUNE{nombre}"
            historialSemantico.agregar(mensaje)
            return True, chr(char_code), None
        else:
            # Ajustar con módulo 256
            char_ajustado = char_code % 256
            
            nombre = f" en variable '{nombre_variable}'" if nombre_variable else ""
            mensaje_error = f"REGLA SEMANTICA 013: OVERFLOW detectado{nombre}: código {char_code} ajustado a {char_ajustado} ('{chr(char_ajustado)}')"
            historialSemantico.agregar(mensaje_error)
            return False, chr(char_ajustado), mensaje_error
            
    except (ValueError, TypeError, OverflowError):
        nombre = f" para variable '{nombre_variable}'" if nombre_variable else ""
        mensaje_error = f"Valor '{valor}' no convertible a RUNE{nombre}"
        historialSemantico.agregar(mensaje_error)
        return False, '\0', mensaje_error

def check_torch_overflow(valor, nombre_variable=None):
    """
    Verifica overflow para tipo TORCH (boolean)
    Basado en ASM: 8 bits pero solo valores 0 y 1
    
    Args:
        valor: Valor a verificar
        nombre_variable: Nombre de la variable (opcional)
    
    Returns:
        tuple: (es_valido, bool_ajustado, mensaje_error)
    """
    try:
        # Convertir a booleano según las reglas de Notch Engine
        if isinstance(valor, str):
            valor_lower = valor.lower()
            if valor_lower in ['on', 'true', '1']:
                bool_val = True
            elif valor_lower in ['off', 'false', '0']:
                bool_val = False
            else:
                # Cualquier string no vacío es verdadero
                bool_val = len(valor) > 0
        elif isinstance(valor, (int, float)):
            bool_val = valor != 0
        else:
            bool_val = bool(valor)
        
        nombre = f" para variable '{nombre_variable}'" if nombre_variable else ""
        valor_str = "On" if bool_val else "Off"
        mensaje = f"REGLA SEMANTICA 014: Valor convertido a TORCH {valor_str}{nombre}"
        historialSemantico.agregar(mensaje)
        return True, bool_val, None
        
    except (ValueError, TypeError):
        nombre = f" para variable '{nombre_variable}'" if nombre_variable else ""
        mensaje_error = f"Valor '{valor}' no convertible a TORCH{nombre}"
        historialSemantico.agregar(mensaje_error)
        return False, False, mensaje_error

def check_chest_overflow(elementos, nombre_variable=None):
    """
    Verifica overflow para tipo CHEST (conjuntos)
    Límites razonables basados en memoria disponible
    
    Args:
        elementos: Lista de elementos del conjunto
        nombre_variable: Nombre de la variable (opcional)
    
    Returns:
        tuple: (es_valido, elementos_ajustados, mensaje_error)
    """
    try:
        MAX_CHEST_ELEMENTS = 100  # Límite razonable
        
        if len(elementos) <= MAX_CHEST_ELEMENTS:
            nombre = f" para variable '{nombre_variable}'" if nombre_variable else ""
            mensaje = f"REGLA SEMANTICA 015: Conjunto de {len(elementos)} elementos válido para CHEST{nombre}"
            historialSemantico.agregar(mensaje)
            return True, elementos, None
        else:
            # Truncar conjunto
            elementos_ajustados = elementos[:MAX_CHEST_ELEMENTS]
            
            nombre = f" en variable '{nombre_variable}'" if nombre_variable else ""
            mensaje_error = f"REGLA SEMANTICA 015: OVERFLOW detectado{nombre}: Conjunto de {len(elementos)} elementos truncado a {MAX_CHEST_ELEMENTS}"
            historialSemantico.agregar(mensaje_error)
            return False, elementos_ajustados, mensaje_error
            
    except (AttributeError, TypeError):
        nombre = f" para variable '{nombre_variable}'" if nombre_variable else ""
        mensaje_error = f"Valor no es un conjunto válido para CHEST{nombre}"
        historialSemantico.agregar(mensaje_error)
        return False, [], mensaje_error

def check_overflow_by_type(tipo, valor, nombre_variable=None):
    """
    Función unificada que verifica overflow según el tipo de dato
    
    Args:
        tipo: Tipo de dato ("STACK", "GHAST", "SPIDER", "RUNE", "TORCH", "CHEST")
        valor: Valor a verificar
        nombre_variable: Nombre de la variable (opcional)
    
    Returns:
        tuple: (es_valido, valor_ajustado, mensaje_error)
    """
    tipo_upper = tipo.upper()
    
    if tipo_upper == "STACK":
        return check_stack_overflow(valor, nombre_variable)
    elif tipo_upper == "GHAST":
        if isinstance(valor, tuple) and len(valor) == 2:
            return check_ghast_overflow(valor[0], valor[1], nombre_variable)
        else:
            # Asumir que es un solo valor para parte entera
            return check_ghast_overflow(valor, 0, nombre_variable)
    elif tipo_upper == "SPIDER":
        return check_spider_overflow(str(valor), nombre_variable)
    elif tipo_upper == "RUNE":
        return check_rune_overflow(valor, nombre_variable)
    elif tipo_upper == "TORCH":
        return check_torch_overflow(valor, nombre_variable)
    elif tipo_upper == "CHEST":
        if isinstance(valor, (list, tuple)):
            return check_chest_overflow(valor, nombre_variable)
        else:
            return check_chest_overflow([valor], nombre_variable)
    else:
        mensaje_error = f"Tipo '{tipo}' no reconocido para verificación de overflow"
        historialSemantico.agregar(mensaje_error)
        return False, valor, mensaje_error