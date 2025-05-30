"""
CheckPollo.py

Estudiantes: Cabrera Samir, Urbina Luis

Chequeo de emparejamiento correcto de delimitadores POLLOCRUDO y POLLOASADO.

Este chequeo verifica que cada POLLOCRUDO tenga su correspondiente POLLOASADO,
manteniendo un balance correcto en la estructura anidada de bloques.
"""

from ..HistorialSemantico import historialSemantico

class PolloBalanceChecker:
    """
    Clase para manejar el balance de bloques POLLOCRUDO/POLLOASADO
    """
    
    def __init__(self):
        self.pila_bloques = []  # Pila para rastrear bloques anidados
        self.contador_global = 0  # Contador global de balance
        self.bloques_abiertos = []  # Lista de posiciones de bloques abiertos
    
    def reset(self):
        """Reinicia el estado del checker"""
        self.pila_bloques.clear()
        self.contador_global = 0
        self.bloques_abiertos.clear()
    
    def abrir_bloque(self, linea, columna, contexto="desconocido"):
        """
        Registra la apertura de un bloque POLLOCRUDO
        
        Args:
            linea: Línea donde aparece POLLOCRUDO
            columna: Columna donde aparece POLLOCRUDO
            contexto: Contexto donde aparece (función, procedimiento, etc.)
        """
        bloque_info = {
            "linea": linea,
            "columna": columna,
            "contexto": contexto,
            "nivel": len(self.pila_bloques)
        }
        
        self.pila_bloques.append(bloque_info)
        self.contador_global += 1
        
        mensaje = f"REGLA SEMANTICA 030: POLLOCRUDO abierto en línea {linea}, columna {columna} (contexto: {contexto}, nivel: {len(self.pila_bloques)})"
        historialSemantico.agregar(mensaje)
        
        return True
    
    def cerrar_bloque(self, linea, columna):
        """
        Registra el cierre de un bloque POLLOASADO
        
        Args:
            linea: Línea donde aparece POLLOASADO
            columna: Columna donde aparece POLLOASADO
            
        Returns:
            tuple: (es_valido, bloque_cerrado, mensaje_error)
        """
        if not self.pila_bloques:
            mensaje_error = f"REGLA SEMANTICA 030: ERROR - POLLOASADO sin POLLOCRUDO correspondiente en línea {linea}, columna {columna}"
            historialSemantico.agregar(mensaje_error)
            return False, None, mensaje_error
        
        bloque_cerrado = self.pila_bloques.pop()
        self.contador_global -= 1
        
        mensaje = f"REGLA SEMANTICA 030: POLLOASADO cierra bloque de línea {bloque_cerrado['linea']} en línea {linea}, columna {columna} (contexto: {bloque_cerrado['contexto']})"
        historialSemantico.agregar(mensaje)
        
        return True, bloque_cerrado, None
    
    def verificar_balance_completo(self):
        """
        Verifica que todos los bloques estén cerrados al final del análisis
        
        Returns:
            tuple: (es_valido, lista_errores)
        """
        if self.contador_global == 0 and not self.pila_bloques:
            mensaje = "REGLA SEMANTICA 030: Todos los bloques POLLOCRUDO/POLLOASADO están correctamente balanceados"
            historialSemantico.agregar(mensaje)
            return True, []
        
        errores = []
        for bloque in self.pila_bloques:
            error = f"REGLA SEMANTICA 030: ERROR - POLLOCRUDO sin cerrar en línea {bloque['linea']}, columna {bloque['columna']} (contexto: {bloque['contexto']})"
            errores.append(error)
            historialSemantico.agregar(error)
        
        return False, errores
    
    def get_nivel_anidacion(self):
        """Retorna el nivel actual de anidación"""
        return len(self.pila_bloques)
    
    def get_contexto_actual(self):
        """Retorna el contexto del bloque más interno"""
        if self.pila_bloques:
            return self.pila_bloques[-1]["contexto"]
        return None

# Instancia global del checker
_pollo_checker = PolloBalanceChecker()

def get_pollo_checker():
    """Obtiene la instancia global del checker"""
    return _pollo_checker

def check_pollo_crudo_apertura(token, contexto="bloque_general"):
    """
    Verifica la apertura de un bloque POLLOCRUDO
    
    Args:
        token: Token POLLOCRUDO
        contexto: Contexto donde aparece (función, procedimiento, etc.)
        
    Returns:
        tuple: (es_valido, mensaje)
    """
    checker = get_pollo_checker()
    
    # Verificar que el token sea efectivamente POLLOCRUDO
    if not es_pollo_crudo_token(token):
        mensaje_error = f"REGLA SEMANTICA 030: ERROR - Token '{token.lexema}' no es un POLLOCRUDO válido"
        historialSemantico.agregar(mensaje_error)
        return False, mensaje_error
    
    # Registrar apertura del bloque
    checker.abrir_bloque(token.linea, token.columna, contexto)
    
    return True, None

def check_pollo_asado_cierre(token):
    """
    Verifica el cierre de un bloque POLLOASADO
    
    Args:
        token: Token POLLOASADO
        
    Returns:
        tuple: (es_valido, bloque_cerrado, mensaje_error)
    """
    checker = get_pollo_checker()
    
    # Verificar que el token sea efectivamente POLLOASADO
    if not es_pollo_asado_token(token):
        mensaje_error = f"REGLA SEMANTICA 030: ERROR - Token '{token.lexema}' no es un POLLOASADO válido"
        historialSemantico.agregar(mensaje_error)
        return False, None, mensaje_error
    
    # Registrar cierre del bloque
    return checker.cerrar_bloque(token.linea, token.columna)

def check_secuencia_pollo_tokens(tokens, inicio=0, fin=None):
    """
    Analiza una secuencia de tokens verificando el balance de POLLOCRUDO/POLLOASADO
    
    Args:
        tokens: Lista de tokens a analizar
        inicio: Índice de inicio (por defecto 0)
        fin: Índice de fin (por defecto hasta el final)
        
    Returns:
        tuple: (es_valido, errores_encontrados, estadisticas)
    """
    if fin is None:
        fin = len(tokens)
    
    checker = PolloBalanceChecker()  # Usar instancia local para análisis
    errores = []
    estadisticas = {
        "pollocrudo_encontrados": 0,
        "polloasado_encontrados": 0,
        "max_anidacion": 0,
        "bloques_correctos": 0
    }
    
    for i in range(inicio, min(fin, len(tokens))):
        token = tokens[i]
        
        if es_pollo_crudo_token(token):
            estadisticas["pollocrudo_encontrados"] += 1
            contexto = determinar_contexto_bloque(tokens, i)
            checker.abrir_bloque(token.linea, token.columna, contexto)
            
            # Actualizar máxima anidación
            nivel_actual = checker.get_nivel_anidacion()
            if nivel_actual > estadisticas["max_anidacion"]:
                estadisticas["max_anidacion"] = nivel_actual
                
        elif es_pollo_asado_token(token):
            estadisticas["polloasado_encontrados"] += 1
            es_valido, bloque_cerrado, error = checker.cerrar_bloque(token.linea, token.columna)
            
            if es_valido:
                estadisticas["bloques_correctos"] += 1
            else:
                errores.append(error)
    
    # Verificar balance final
    es_balance_valido, errores_balance = checker.verificar_balance_completo()
    errores.extend(errores_balance)
    
    return len(errores) == 0, errores, estadisticas

def es_pollo_crudo_token(token):
    """
    Verifica si un token es POLLOCRUDO (considerando variaciones)
    
    Args:
        token: Token a verificar
        
    Returns:
        bool: True si es POLLOCRUDO válido
    """
    if not hasattr(token, 'type') or not hasattr(token, 'lexema'):
        return False
    
    # Verificar tipo directo
    if token.type == "POLLO_CRUDO":
        return True
    
    # Verificar identificador que sea pollocrudo (case insensitive)
    if token.type == "IDENTIFICADOR" and token.lexema.lower() in ["pollocrudo", "pollo_crudo"]:
        return True
    
    return False

def es_pollo_asado_token(token):
    """
    Verifica si un token es POLLOASADO (considerando variaciones)
    
    Args:
        token: Token a verificar
        
    Returns:
        bool: True si es POLLOASADO válido
    """
    if not hasattr(token, 'type') or not hasattr(token, 'lexema'):
        return False
    
    # Verificar tipo directo
    if token.type == "POLLO_ASADO":
        return True
    
    # Verificar identificador que sea polloasado (case insensitive)
    if token.type == "IDENTIFICADOR" and token.lexema.lower() in ["polloasado", "pollo_asado"]:
        return True
    
    return False

def determinar_contexto_bloque(tokens, indice_pollo_crudo):
    """
    Determina el contexto donde aparece un POLLOCRUDO analizando tokens anteriores
    
    Args:
        tokens: Lista completa de tokens
        indice_pollo_crudo: Índice donde está el POLLOCRUDO
        
    Returns:
        str: Contexto determinado
    """
    # Analizar los últimos 10 tokens antes del POLLOCRUDO para determinar contexto
    inicio = max(0, indice_pollo_crudo - 10)
    
    contextos_detectados = []
    
    for i in range(inicio, indice_pollo_crudo):
        token = tokens[i]
        
        if hasattr(token, 'type'):
            if token.type == "SPELL":
                contextos_detectados.append("funcion")
            elif token.type == "RITUAL":
                contextos_detectados.append("procedimiento")
            elif token.type == "ENTITY":
                contextos_detectados.append("entidad")
            elif token.type in ["TARGET", "REPEATER", "SPAWNER", "WALK", "JUKEBOX", "WITHER"]:
                contextos_detectados.append("estructura_control")
    
    # Retornar el contexto más reciente o uno genérico
    if contextos_detectados:
        return contextos_detectados[-1]
    
    return "bloque_general"

def verificar_balance_archivo_completo(tokens):
    """
    Verifica el balance de POLLOCRUDO/POLLOASADO en un archivo completo
    
    Args:
        tokens: Lista completa de tokens del archivo
        
    Returns:
        tuple: (es_valido, reporte_completo)
    """
    es_valido, errores, estadisticas = check_secuencia_pollo_tokens(tokens)
    
    reporte = {
        "es_valido": es_valido,
        "errores": errores,
        "estadisticas": estadisticas,
        "resumen": f"Encontrados {estadisticas['pollocrudo_encontrados']} POLLOCRUDO y {estadisticas['polloasado_encontrados']} POLLOASADO. "
                  f"Bloques correctos: {estadisticas['bloques_correctos']}. Máxima anidación: {estadisticas['max_anidacion']}."
    }
    
    # Registrar en historial
    mensaje_resumen = f"REGLA SEMANTICA 030: {reporte['resumen']}"
    if es_valido:
        mensaje_resumen += " Balance CORRECTO."
    else:
        mensaje_resumen += f" Balance INCORRECTO ({len(errores)} errores)."
    
    historialSemantico.agregar(mensaje_resumen)
    
    return es_valido, reporte

def reset_pollo_checker():
    """Reinicia el estado global del checker"""
    get_pollo_checker().reset()

def get_estado_actual_pollo():
    """
    Obtiene el estado actual del balance de bloques
    
    Returns:
        dict: Estado actual con información de bloques abiertos
    """
    checker = get_pollo_checker()
    
    return {
        "nivel_anidacion": checker.get_nivel_anidacion(),
        "contexto_actual": checker.get_contexto_actual(),
        "bloques_abiertos": len(checker.pila_bloques),
        "balance_global": checker.contador_global,
        "info_bloques": [
            {
                "linea": bloque["linea"],
                "columna": bloque["columna"],
                "contexto": bloque["contexto"],
                "nivel": bloque["nivel"]
            }
            for bloque in checker.pila_bloques
        ]
    }