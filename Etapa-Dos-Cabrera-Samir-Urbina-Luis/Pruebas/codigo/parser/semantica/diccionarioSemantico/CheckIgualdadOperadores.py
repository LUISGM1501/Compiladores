"""
CheckIgualdadOperadores.py

Estudiantes: Cabrera Samir, Urbina Luis

Chequeo de operadores de asignación compuesta (+=, -=, *=, /=, %=) 
y sus equivalentes flotantes (:+=, :-=, :*=, :/=, :%=).

Este módulo verifica que los operadores compuestos se apliquen correctamente:
- El identificador debe existir y ser modificable
- El tipo del valor debe ser compatible con el tipo del identificador
- La operación aritmética implícita debe ser válida
"""

from ..HistorialSemantico import historialSemantico
from ..TablaSimbolos import TablaSimbolos
from .CheckTipoOp import verificar_operacion_aritmetica, inferir_tipo_operando
from .CheckVarExiste import checkVarDeclared, getVarType
from .CheckDivZero import check_assignment_division_zero

class OperadorCompuestoChecker:
    """
    Clase para manejar la verificación de operadores de asignación compuesta
    """
    
    # Mapeo de operadores compuestos a sus operadores básicos equivalentes
    OPERADORES_COMPUESTOS = {
        "SUMA_IGUAL": "SUMA",
        "RESTA_IGUAL": "RESTA", 
        "MULTIPLICACION_IGUAL": "MULTIPLICACION",
        "DIVISION_IGUAL": "DIVISION",
        "MODULO_IGUAL": "MODULO",
        "SUMA_FLOTANTE_IGUAL": "SUMA_FLOTANTE",
        "RESTA_FLOTANTE_IGUAL": "RESTA_FLOTANTE",
        "MULTIPLICACION_FLOTANTE_IGUAL": "MULTIPLICACION_FLOTANTE",
        "DIVISION_FLOTANTE_IGUAL": "DIVISION_FLOTANTE",
        "MODULO_FLOTANTE_IGUAL": "MODULO_FLOTANTE"
    }
    
    # Operadores que requieren verificación de división por cero
    OPERADORES_DIVISION = {
        "DIVISION_IGUAL", "MODULO_IGUAL",
        "DIVISION_FLOTANTE_IGUAL", "MODULO_FLOTANTE_IGUAL"
    }
    
    # Tipos que pueden ser modificados
    CATEGORIAS_MODIFICABLES = {"VARIABLE"}
    
    # Tipos que NO pueden ser modificados
    CATEGORIAS_NO_MODIFICABLES = {"OBSIDIAN", "CONSTANTE", "FUNCION", "PROCEDIMIENTO", "TIPO_DEFINIDO_USUARIO"}

def verificar_operador_compuesto(identificador_token, operador_token, valor_token, linea=None):
    """
    Verifica que un operador compuesto se aplique correctamente
    
    Args:
        identificador_token: Token del identificador (lado izquierdo)
        operador_token: Token del operador compuesto (+=, -=, etc.)
        valor_token: Token del valor (lado derecho)
        linea: Línea donde ocurre la operación (opcional)
        
    Returns:
        tuple: (es_valido, tipo_resultado, mensaje_error)
    """
    ubicacion = f" en línea {linea}" if linea else ""
    
    # 1. Verificar que el identificador existe
    if not checkVarDeclared(identificador_token):
        mensaje_error = f"REGLA SEMANTICA 050: ERROR - Identificador '{identificador_token.lexema}' no declarado{ubicacion}"
        historialSemantico.agregar(mensaje_error)
        return False, "ERROR", mensaje_error
    
    # 2. Verificar que el identificador es modificable
    tabla = TablaSimbolos.instancia()
    simbolo = tabla.buscar(identificador_token.lexema)
    
    if simbolo.categoria in OperadorCompuestoChecker.CATEGORIAS_NO_MODIFICABLES:
        mensaje_error = f"REGLA SEMANTICA 050: ERROR - No se puede modificar '{identificador_token.lexema}' de categoría {simbolo.categoria}{ubicacion}"
        historialSemantico.agregar(mensaje_error)
        return False, "ERROR", mensaje_error
    
    # 3. Obtener tipos involucrados
    tipo_identificador = simbolo.tipo
    tipo_valor = inferir_tipo_operando(valor_token)
    
    if tipo_valor == "IDENTIFICADOR":
        # Si el valor es un identificador, obtener su tipo real
        tipo_valor = getVarType(valor_token)
        if tipo_valor is None:
            mensaje_error = f"REGLA SEMANTICA 050: ERROR - Variable '{valor_token.lexema}' no declarada{ubicacion}"
            historialSemantico.agregar(mensaje_error)
            return False, "ERROR", mensaje_error
    
    # 4. Verificar que el operador es válido
    operador_tipo = operador_token.type if hasattr(operador_token, 'type') else str(operador_token)
    
    if operador_tipo not in OperadorCompuestoChecker.OPERADORES_COMPUESTOS:
        mensaje_error = f"REGLA SEMANTICA 050: ERROR - Operador '{operador_tipo}' no es un operador compuesto válido{ubicacion}"
        historialSemantico.agregar(mensaje_error)
        return False, "ERROR", mensaje_error
    
    # 5. Verificar división por cero si aplica
    if operador_tipo in OperadorCompuestoChecker.OPERADORES_DIVISION:
        valor_divisor = valor_token.lexema if hasattr(valor_token, 'lexema') else str(valor_token)
        es_valido_div, error_div = check_assignment_division_zero(
            valor_divisor, 
            operador_tipo, 
            linea, 
            identificador_token.lexema
        )
        
        if not es_valido_div:
            historialSemantico.agregar(error_div)
            return False, "ERROR", error_div
    
    # 6. Verificar que la operación aritmética subyacente es válida
    operador_basico = OperadorCompuestoChecker.OPERADORES_COMPUESTOS[operador_tipo]
    
    es_valida, tipo_resultado, error_operacion = verificar_operacion_aritmetica(
        tipo_identificador, 
        operador_basico, 
        tipo_valor, 
        linea
    )
    
    if not es_valida:
        mensaje_error = f"REGLA SEMANTICA 050: ERROR - Operación {tipo_identificador} {operador_basico} {tipo_valor} inválida en asignación compuesta{ubicacion}: {error_operacion}"
        historialSemantico.agregar(mensaje_error)
        return False, "ERROR", mensaje_error
    
    # 7. Verificar compatibilidad del resultado con el tipo original
    compatibilidad = verificar_compatibilidad_asignacion_compuesta(
        tipo_identificador, 
        tipo_resultado, 
        operador_tipo
    )
    
    if not compatibilidad["es_compatible"]:
        mensaje_error = f"REGLA SEMANTICA 050: ERROR - Resultado de tipo {tipo_resultado} no compatible con variable {tipo_identificador}{ubicacion}: {compatibilidad['razon']}"
        historialSemantico.agregar(mensaje_error)
        return False, "ERROR", mensaje_error
    
    # 8. Operación válida
    if compatibilidad["requiere_conversion"]:
        mensaje = f"REGLA SEMANTICA 050: Operación compuesta '{identificador_token.lexema}' {operador_tipo} '{valor_token.lexema}' válida con conversión {tipo_resultado} -> {tipo_identificador}{ubicacion}"
    else:
        mensaje = f"REGLA SEMANTICA 050: Operación compuesta '{identificador_token.lexema}' {operador_tipo} '{valor_token.lexema}' válida{ubicacion}"
    
    historialSemantico.agregar(mensaje)
    return True, tipo_identificador, None

def verificar_compatibilidad_asignacion_compuesta(tipo_original, tipo_resultado, operador):
    """
    Verifica si el resultado de una operación compuesta es compatible con el tipo original
    
    Args:
        tipo_original: Tipo original de la variable
        tipo_resultado: Tipo resultado de la operación
        operador: Operador compuesto utilizado
        
    Returns:
        dict: Información sobre la compatibilidad
    """
    # Si los tipos son idénticos, siempre es compatible
    if tipo_original == tipo_resultado:
        return {
            "es_compatible": True,
            "requiere_conversion": False,
            "razon": None
        }
    
    # Definir conversiones permitidas en asignaciones compuestas
    conversiones_permitidas = {
        # De entero a flotante (común en operaciones mixtas)
        ("STACK", "GHAST"): {
            "permitida": True,
            "requiere_conversion": True,
            "razon": "Conversión de entero a flotante en resultado de operación"
        },
        
        # De flotante a entero (pérdida de precisión)
        ("GHAST", "STACK"): {
            "permitida": False,
            "requiere_conversion": False,
            "razon": "Pérdida de precisión al convertir flotante a entero"
        },
        
        # Booleano a entero
        ("TORCH", "STACK"): {
            "permitida": True,
            "requiere_conversion": True,
            "razon": "Conversión de booleano a entero (False=0, True=1)"
        },
        
        # Entero a booleano
        ("STACK", "TORCH"): {
            "permitida": True,
            "requiere_conversion": True,
            "razon": "Conversión de entero a booleano (0=False, !=0=True)"
        }
    }
    
    clave_conversion = (tipo_original, tipo_resultado)
    
    if clave_conversion in conversiones_permitidas:
        conv_info = conversiones_permitidas[clave_conversion]
        return {
            "es_compatible": conv_info["permitida"],
            "requiere_conversion": conv_info["requiere_conversion"],
            "razon": conv_info["razon"] if not conv_info["permitida"] else None
        }
    
    # Para operadores flotantes, ser más permisivo
    if "FLOTANTE" in operador:
        if tipo_original in ["STACK", "GHAST"] and tipo_resultado in ["STACK", "GHAST"]:
            return {
                "es_compatible": True,
                "requiere_conversion": True,
                "razon": None
            }
    
    # Casos no contemplados son incompatibles por defecto
    return {
        "es_compatible": False,
        "requiere_conversion": False,
        "razon": f"No hay conversión definida de {tipo_resultado} a {tipo_original}"
    }

def procesar_secuencia_asignacion_compuesta(tokens_secuencia, linea=None):
    """
    Procesa una secuencia completa de asignación compuesta: id op= expresión;
    
    Args:
        tokens_secuencia: Lista de tokens de la secuencia
        linea: Línea donde ocurre (opcional)
        
    Returns:
        tuple: (es_valida, errores_encontrados)
    """
    errores = []
    
    if len(tokens_secuencia) < 3:
        error = f"REGLA SEMANTICA 051: ERROR - Secuencia de asignación compuesta incompleta en línea {linea}"
        errores.append(error)
        historialSemantico.agregar(error)
        return False, errores
    
    identificador_token = tokens_secuencia[0]
    operador_token = tokens_secuencia[1]
    
    # El resto de tokens forman la expresión del lado derecho
    tokens_expresion = tokens_secuencia[2:]
    
    # Verificar que el primer token es un identificador
    if not hasattr(identificador_token, 'type') or identificador_token.type != "IDENTIFICADOR":
        error = f"REGLA SEMANTICA 051: ERROR - Se esperaba identificador al inicio de asignación compuesta en línea {linea}"
        errores.append(error)
        historialSemantico.agregar(error)
        return False, errores
    
    # Para simplificar, tomar solo el primer token de la expresión
    # (En una implementación más completa, se evaluaría toda la expresión)
    if tokens_expresion:
        valor_token = tokens_expresion[0]
        
        es_valida, tipo_resultado, error = verificar_operador_compuesto(
            identificador_token, 
            operador_token, 
            valor_token, 
            linea
        )
        
        if not es_valida:
            errores.append(error)
        
        return es_valida, errores
    else:
        error = f"REGLA SEMANTICA 051: ERROR - Falta expresión después del operador compuesto en línea {linea}"
        errores.append(error)
        historialSemantico.agregar(error)
        return False, errores

def verificar_multiples_operadores_compuestos(lista_secuencias):
    """
    Verifica múltiples operaciones de asignación compuesta
    
    Args:
        lista_secuencias: Lista de secuencias de tokens
        
    Returns:
        tuple: (todas_validas, resumen_errores)
    """
    todas_validas = True
    resumen_errores = []
    operaciones_procesadas = 0
    
    for i, secuencia in enumerate(lista_secuencias):
        linea = secuencia[0].linea if secuencia and hasattr(secuencia[0], 'linea') else i + 1
        
        es_valida, errores = procesar_secuencia_asignacion_compuesta(secuencia, linea)
        
        if not es_valida:
            todas_validas = False
            resumen_errores.extend(errores)
        
        operaciones_procesadas += 1
    
    # Registrar resumen en historial
    if todas_validas:
        mensaje_resumen = f"REGLA SEMANTICA 052: Procesadas {operaciones_procesadas} operaciones compuestas, todas válidas"
    else:
        mensaje_resumen = f"REGLA SEMANTICA 052: Procesadas {operaciones_procesadas} operaciones compuestas, {len(resumen_errores)} errores encontrados"
    
    historialSemantico.agregar(mensaje_resumen)
    
    return todas_validas, resumen_errores

def obtener_operadores_compuestos_soportados():
    """
    Retorna la lista de operadores compuestos soportados
    
    Returns:
        dict: Mapeo de operadores compuestos a sus equivalencias
    """
    return OperadorCompuestoChecker.OPERADORES_COMPUESTOS.copy()

def es_operador_compuesto(token_o_string):
    """
    Verifica si un token o string representa un operador compuesto
    
    Args:
        token_o_string: Token o string a verificar
        
    Returns:
        bool: True si es un operador compuesto
    """
    if hasattr(token_o_string, 'type'):
        return token_o_string.type in OperadorCompuestoChecker.OPERADORES_COMPUESTOS
    else:
        return str(token_o_string) in OperadorCompuestoChecker.OPERADORES_COMPUESTOS

def sugerir_correccion_operador_compuesto(identificador, operador, valor, error_tipo):
    """
    Sugiere correcciones para errores en operadores compuestos
    
    Args:
        identificador: Identificador involucrado
        operador: Operador compuesto
        valor: Valor involucrado
        error_tipo: Tipo de error detectado
        
    Returns:
        str: Sugerencia de corrección
    """
    if error_tipo == "IDENTIFICADOR_NO_DECLARADO":
        return f"Declare la variable '{identificador}' antes de usarla en operación compuesta"
    
    elif error_tipo == "IDENTIFICADOR_NO_MODIFICABLE":
        return f"Use una variable en lugar de '{identificador}' para operaciones compuestas"
    
    elif error_tipo == "TIPOS_INCOMPATIBLES":
        if "FLOTANTE" in operador:
            return f"Para operadores flotantes, asegúrese de que ambos operandos sean numéricos"
        else:
            return f"Verifique que los tipos de '{identificador}' y '{valor}' sean compatibles"
    
    elif error_tipo == "DIVISION_CERO":
        return f"Evite división o módulo por cero en operaciones compuestas"
    
    else:
        return f"Revise la sintaxis de la operación compuesta '{identificador} {operador} {valor}'"

# Función de conveniencia para uso externo
def check_operador_compuesto(identificador_token, operador_token, valor_token, linea=None):
    """
    Función de conveniencia que encapsula la verificación principal
    """
    return verificar_operador_compuesto(identificador_token, operador_token, valor_token, linea)