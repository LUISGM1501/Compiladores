"""
CheckTargetHitMiss.py

Estudiantes: Cabrera Samir, Urbina Luis

Chequeo de estructura condicional TARGET/HIT/MISS mediante maquillaje semántico.
No modifica la gramática existente, sino que detecta y valida estas estructuras
en tiempo real durante el proceso de parsing.

Este módulo verifica que:
- TARGET siempre preceda a HIT/MISS
- No haya duplicación de TARGET sin cierre
- Las estructuras estén correctamente anidadas
- MISS solo aparezca después de HIT correspondiente
"""

from ..HistorialSemantico import historialSemantico

class TargetHitMissTracker:
    """
    Rastreador de estructuras TARGET/HIT/MISS que funciona como maquillaje
    durante el proceso de parsing sin modificar la gramática
    """
    
    def __init__(self):
        self.pila_target = []  # Pila para rastrear TARGET activos
        self.contador_estructuras = 0  # Contador global de estructuras
        self.estructuras_completadas = []  # Estructuras finalizadas
        self.errores_encontrados = []  # Lista de errores detectados
        
        # Estados posibles de una estructura TARGET
        self.ESTADOS = {
            "ESPERANDO_HIT": "esperando_hit",         # TARGET declarado, necesita HIT
            "HIT_ENCONTRADO": "hit_encontrado",       # HIT procesado, puede venir MISS
            "MISS_ENCONTRADO": "miss_encontrado",     # MISS procesado, estructura completa
            "ESTRUCTURA_COMPLETA": "estructura_completa"  # Estructura cerrada
        }
        
        # Patrones de tokens que indican cierre de estructura
        self.TOKENS_CIERRE = {
            "PUNTO_Y_COMA", "POLLO_ASADO", "TARGET", "REPEATER", 
            "SPAWNER", "WALK", "JUKEBOX", "WORLD_SAVE"
        }
    
    def reset(self):
        """Reinicia el estado del tracker"""
        self.pila_target.clear()
        self.contador_estructuras = 0
        self.estructuras_completadas.clear()
        self.errores_encontrados.clear()
    
    def procesar_target(self, token, contexto="desconocido"):
        """
        Procesa un token TARGET detectado durante el parsing
        
        Args:
            token: Token TARGET encontrado
            contexto: Contexto donde aparece
            
        Returns:
            tuple: (es_valido, mensaje)
        """
        # Crear nueva estructura TARGET
        estructura = {
            "id": self.contador_estructuras,
            "tipo": "TARGET",
            "token": token,
            "linea": token.linea,
            "columna": token.columna,
            "contexto": contexto,
            "estado": self.ESTADOS["ESPERANDO_HIT"],
            "nivel": len(self.pila_target),
            "tiene_hit": False,
            "tiene_miss": False,
            "tokens_procesados": [token]
        }
        
        self.pila_target.append(estructura)
        self.contador_estructuras += 1
        
        mensaje = f"REGLA SEMANTICA 035: TARGET detectado en línea {token.linea}, columna {token.columna} (ID: {estructura['id']}, contexto: {contexto}, nivel: {len(self.pila_target)})"
        historialSemantico.agregar(mensaje)
        
        return True, mensaje
    
    def procesar_hit(self, token):
        """
        Procesa un token HIT detectado durante el parsing
        
        Args:
            token: Token HIT encontrado
            
        Returns:
            tuple: (es_valido, target_asociado, mensaje_error)
        """
        if not self.pila_target:
            error = f"REGLA SEMANTICA 035: ERROR - HIT sin TARGET correspondiente en línea {token.linea}, columna {token.columna}"
            self.errores_encontrados.append(error)
            historialSemantico.agregar(error)
            return False, None, error
        
        # Buscar TARGET que esté esperando HIT
        target_encontrado = None
        for i in range(len(self.pila_target) - 1, -1, -1):
            if self.pila_target[i]["estado"] == self.ESTADOS["ESPERANDO_HIT"]:
                target_encontrado = self.pila_target[i]
                break
        
        if not target_encontrado:
            error = f"REGLA SEMANTICA 035: ERROR - HIT en línea {token.linea} sin TARGET válido (todos los TARGET ya tienen HIT)"
            self.errores_encontrados.append(error)
            historialSemantico.agregar(error)
            return False, None, error
        
        # Actualizar TARGET con HIT
        target_encontrado["estado"] = self.ESTADOS["HIT_ENCONTRADO"]
        target_encontrado["tiene_hit"] = True
        target_encontrado["token_hit"] = token
        target_encontrado["tokens_procesados"].append(token)
        
        mensaje = f"REGLA SEMANTICA 035: HIT procesado en línea {token.linea}, columna {token.columna} para TARGET (ID: {target_encontrado['id']}, línea {target_encontrado['linea']})"
        historialSemantico.agregar(mensaje)
        
        return True, target_encontrado, None
    
    def procesar_miss(self, token):
        """
        Procesa un token MISS detectado durante el parsing
        
        Args:
            token: Token MISS encontrado
            
        Returns:
            tuple: (es_valido, target_asociado, mensaje_error)
        """
        if not self.pila_target:
            error = f"REGLA SEMANTICA 035: ERROR - MISS sin TARGET correspondiente en línea {token.linea}, columna {token.columna}"
            self.errores_encontrados.append(error)
            historialSemantico.agregar(error)
            return False, None, error
        
        # Buscar TARGET que tenga HIT y pueda aceptar MISS
        target_encontrado = None
        for i in range(len(self.pila_target) - 1, -1, -1):
            if self.pila_target[i]["estado"] == self.ESTADOS["HIT_ENCONTRADO"]:
                target_encontrado = self.pila_target[i]
                break
        
        if not target_encontrado:
            # Verificar si hay TARGET esperando HIT
            target_sin_hit = None
            for target in reversed(self.pila_target):
                if target["estado"] == self.ESTADOS["ESPERANDO_HIT"]:
                    target_sin_hit = target
                    break
            
            if target_sin_hit:
                error = f"REGLA SEMANTICA 035: ERROR - MISS sin HIT correspondiente en línea {token.linea}, TARGET (ID: {target_sin_hit['id']}) requiere HIT primero"
            else:
                error = f"REGLA SEMANTICA 035: ERROR - MISS en línea {token.linea} sin estructura TARGET-HIT válida"
            
            self.errores_encontrados.append(error)
            historialSemantico.agregar(error)
            return False, None, error
        
        # Actualizar TARGET con MISS
        target_encontrado["estado"] = self.ESTADOS["MISS_ENCONTRADO"]
        target_encontrado["tiene_miss"] = True
        target_encontrado["token_miss"] = token
        target_encontrado["tokens_procesados"].append(token)
        
        mensaje = f"REGLA SEMANTICA 035: MISS procesado en línea {token.linea}, columna {token.columna} para TARGET (ID: {target_encontrado['id']}, línea {target_encontrado['linea']})"
        historialSemantico.agregar(mensaje)
        
        return True, target_encontrado, None
    
    def detectar_cierre_estructura(self, token):
        """
        Detecta si un token indica el cierre de una estructura TARGET
        
        Args:
            token: Token actual del parser
            
        Returns:
            list: Lista de estructuras que se cerraron
        """
        if not token or not self.pila_target:
            return []
        
        estructuras_cerradas = []
        
        # Detectar tokens que fuerzan cierre de estructura
        if token.type in self.TOKENS_CIERRE:
            # Cerrar estructura más reciente si está completa
            if self.pila_target:
                ultima_estructura = self.pila_target[-1]
                
                # Solo cerrar si tiene HIT (estructura mínima válida)
                if ultima_estructura["estado"] in [self.ESTADOS["HIT_ENCONTRADO"], self.ESTADOS["MISS_ENCONTRADO"]]:
                    estructura_cerrada = self.pila_target.pop()
                    estructura_cerrada["estado"] = self.ESTADOS["ESTRUCTURA_COMPLETA"]
                    estructura_cerrada["token_cierre"] = token
                    self.estructuras_completadas.append(estructura_cerrada)
                    estructuras_cerradas.append(estructura_cerrada)
                    
                    mensaje = f"REGLA SEMANTICA 035: Estructura TARGET (ID: {estructura_cerrada['id']}) cerrada implícitamente por {token.type} en línea {token.linea}"
                    historialSemantico.agregar(mensaje)
        
        # Detectar nuevo TARGET (cierra estructuras anteriores)
        elif token.type == "TARGET":
            # Cerrar todas las estructuras que puedan cerrarse
            while self.pila_target:
                ultima_estructura = self.pila_target[-1]
                if ultima_estructura["estado"] in [self.ESTADOS["HIT_ENCONTRADO"], self.ESTADOS["MISS_ENCONTRADO"]]:
                    estructura_cerrada = self.pila_target.pop()
                    estructura_cerrada["estado"] = self.ESTADOS["ESTRUCTURA_COMPLETA"]
                    estructura_cerrada["token_cierre"] = token
                    self.estructuras_completadas.append(estructura_cerrada)
                    estructuras_cerradas.append(estructura_cerrada)
                    
                    mensaje = f"REGLA SEMANTICA 035: Estructura TARGET (ID: {estructura_cerrada['id']}) cerrada por nuevo TARGET en línea {token.linea}"
                    historialSemantico.agregar(mensaje)
                else:
                    break
        
        return estructuras_cerradas
    
    def forzar_cierre_todas_estructuras(self, token_final=None):
        """
        Fuerza el cierre de todas las estructuras al final del archivo
        
        Args:
            token_final: Token final del archivo (opcional)
            
        Returns:
            tuple: (estructuras_cerradas, errores_generados)
        """
        estructuras_cerradas = []
        errores_generados = []
        
        while self.pila_target:
            estructura = self.pila_target.pop()
            
            if estructura["estado"] == self.ESTADOS["ESPERANDO_HIT"]:
                # ERROR: TARGET sin HIT
                error = f"REGLA SEMANTICA 035: ERROR - TARGET (ID: {estructura['id']}) en línea {estructura['linea']} sin HIT correspondiente"
                errores_generados.append(error)
                self.errores_encontrados.append(error)
                historialSemantico.agregar(error)
                
                estructura["tiene_error"] = True
            
            # Marcar como cerrada (aunque tenga errores)
            estructura["estado"] = self.ESTADOS["ESTRUCTURA_COMPLETA"]
            if token_final:
                estructura["token_cierre"] = token_final
            
            self.estructuras_completadas.append(estructura)
            estructuras_cerradas.append(estructura)
        
        return estructuras_cerradas, errores_generados
    
    def obtener_estadisticas(self):
        """
        Obtiene estadísticas del análisis realizado
        
        Returns:
            dict: Estadísticas completas
        """
        return {
            "estructuras_detectadas": self.contador_estructuras,
            "estructuras_abiertas": len(self.pila_target),
            "estructuras_completadas": len(self.estructuras_completadas),
            "estructuras_con_miss": sum(1 for e in self.estructuras_completadas if e.get("tiene_miss", False)),
            "estructuras_con_errores": sum(1 for e in self.estructuras_completadas if e.get("tiene_error", False)),
            "errores_totales": len(self.errores_encontrados),
            "nivel_anidacion_max": max([e["nivel"] for e in self.estructuras_completadas], default=0)
        }

# Instancia global del tracker
_target_tracker = TargetHitMissTracker()

def get_target_tracker():
    """Obtiene la instancia global del tracker"""
    return _target_tracker

def maquillar_target_hit_miss_en_parser(parser_instance):
    """
    Función principal que se integra con el parser para detectar
    y validar estructuras TARGET/HIT/MISS durante el parsing
    
    Args:
        parser_instance: Instancia del parser en ejecución
        
    Returns:
        tuple: (errores_detectados, estructuras_procesadas)
    """
    tracker = get_target_tracker()
    token_actual = parser_instance.token_actual
    
    if not token_actual:
        return [], []
    
    errores = []
    estructuras_procesadas = []
    
    # PASO 1: Detectar cierre implícito de estructuras
    estructuras_cerradas = tracker.detectar_cierre_estructura(token_actual)
    estructuras_procesadas.extend(estructuras_cerradas)
    
    # PASO 2: Procesar token actual si es TARGET/HIT/MISS
    if token_actual.type == "TARGET":
        contexto = determinar_contexto_parsing(parser_instance)
        es_valido, mensaje = tracker.procesar_target(token_actual, contexto)
        if not es_valido:
            errores.append(mensaje)
            
    elif token_actual.type == "HIT":
        es_valido, target_asociado, error = tracker.procesar_hit(token_actual)
        if not es_valido:
            errores.append(error)
            
    elif token_actual.type == "MISS":
        es_valido, target_asociado, error = tracker.procesar_miss(token_actual)
        if not es_valido:
            errores.append(error)
    
    return errores, estructuras_procesadas

def determinar_contexto_parsing(parser_instance):
    """
    Determina el contexto actual del parsing para ubicar el TARGET
    
    Args:
        parser_instance: Instancia del parser
        
    Returns:
        str: Contexto determinado
    """
    if not hasattr(parser_instance, 'token_history'):
        return "contexto_desconocido"
    
    # Analizar historial reciente para determinar contexto
    contextos = []
    
    for token in parser_instance.token_history[-15:]:  # Últimos 15 tokens
        if hasattr(token, 'type'):
            if token.type == "SPELL":
                contextos.append("funcion")
            elif token.type == "RITUAL":
                contextos.append("procedimiento")
            elif token.type == "REPEATER":
                contextos.append("bucle_while")
            elif token.type == "SPAWNER":
                contextos.append("bucle_repeat")
            elif token.type == "WALK":
                contextos.append("bucle_for")
            elif token.type == "TARGET":
                contextos.append("target_anidado")
            elif token.type == "POLLO_CRUDO":
                contextos.append("bloque_abierto")
    
    # Determinar contexto más específico
    if "target_anidado" in contextos:
        return "target_anidado"
    elif "funcion" in contextos:
        return "dentro_funcion"
    elif "procedimiento" in contextos:
        return "dentro_procedimiento"
    elif any(bucle in contextos for bucle in ["bucle_while", "bucle_repeat", "bucle_for"]):
        return "dentro_bucle"
    elif "bloque_abierto" in contextos:
        return "dentro_bloque"
    else:
        return "bloque_principal"

def validar_al_final_del_parsing(parser_instance):
    """
    Valida todas las estructuras TARGET al final del parsing
    
    Args:
        parser_instance: Instancia del parser
        
    Returns:
        tuple: (es_valido, reporte_completo)
    """
    tracker = get_target_tracker()
    
    # Forzar cierre de estructuras pendientes
    estructuras_cerradas, errores_finales = tracker.forzar_cierre_todas_estructuras(
        parser_instance.token_actual
    )
    
    # Obtener estadísticas
    estadisticas = tracker.obtener_estadisticas()
    
    # Generar reporte
    es_valido = len(tracker.errores_encontrados) == 0
    
    reporte = {
        "es_valido": es_valido,
        "errores": tracker.errores_encontrados.copy(),
        "estructuras_cerradas_final": estructuras_cerradas,
        "estadisticas": estadisticas,
        "resumen": f"TARGET detectados: {estadisticas['estructuras_detectadas']}, "
                  f"Completados: {estadisticas['estructuras_completadas']}, "
                  f"Con MISS: {estadisticas['estructuras_con_miss']}, "
                  f"Con errores: {estadisticas['estructuras_con_errores']}, "
                  f"Anidación máxima: {estadisticas['nivel_anidacion_max']}"
    }
    
    # Registrar en historial
    mensaje_final = f"REGLA SEMANTICA 035: Validación final TARGET/HIT/MISS - {reporte['resumen']}"
    if es_valido:
        mensaje_final += " - VALIDACIÓN EXITOSA"
    else:
        mensaje_final += f" - {len(tracker.errores_encontrados)} ERRORES DETECTADOS"
    
    historialSemantico.agregar(mensaje_final)
    
    return es_valido, reporte

def obtener_estado_actual():
    """
    Obtiene el estado actual del tracker para debugging
    
    Returns:
        dict: Estado actual detallado
    """
    tracker = get_target_tracker()
    
    return {
        "estructuras_abiertas": len(tracker.pila_target),
        "estructuras_completadas": len(tracker.estructuras_completadas),
        "errores_detectados": len(tracker.errores_encontrados),
        "info_estructuras_abiertas": [
            {
                "id": e["id"],
                "linea": e["linea"],
                "estado": e["estado"],
                "tiene_hit": e["tiene_hit"],
                "tiene_miss": e["tiene_miss"],
                "contexto": e["contexto"]
            }
            for e in tracker.pila_target
        ],
        "ultimo_error": tracker.errores_encontrados[-1] if tracker.errores_encontrados else None
    }

def reset_tracker():
    """Reinicia el tracker global"""
    get_target_tracker().reset()

def generar_sugerencias_correccion():
    """
    Genera sugerencias de corrección basadas en los errores detectados
    
    Returns:
        list: Lista de sugerencias
    """
    tracker = get_target_tracker()
    sugerencias = []
    
    for error in tracker.errores_encontrados:
        if "HIT sin TARGET" in error:
            sugerencias.append("Agregue un TARGET antes del HIT correspondiente")
        elif "MISS sin HIT" in error:
            sugerencias.append("Agregue un HIT antes del MISS, o elimine el MISS")
        elif "TARGET sin HIT" in error:
            sugerencias.append("Complete la estructura TARGET con su HIT correspondiente")
        elif "MISS sin estructura TARGET-HIT" in error:
            sugerencias.append("Agregue una estructura TARGET-HIT completa antes del MISS")
    
    # Sugerencias generales
    if tracker.pila_target:
        sugerencias.append(f"Hay {len(tracker.pila_target)} estructura(s) TARGET sin cerrar")
    
    return sugerencias

# Función de conveniencia para testing
def test_secuencia_tokens(tokens):
    """
    Función de testing que valida una secuencia de tokens
    
    Args:
        tokens: Lista de tokens a validar
        
    Returns:
        dict: Resultado de la validación
    """
    reset_tracker()
    tracker = get_target_tracker()
    
    errores = []
    
    for token in tokens:
        if token.type == "TARGET":
            es_valido, mensaje = tracker.procesar_target(token, "test")
            if not es_valido:
                errores.append(mensaje)
        elif token.type == "HIT":
            es_valido, _, error = tracker.procesar_hit(token)
            if not es_valido:
                errores.append(error)
        elif token.type == "MISS":
            es_valido, _, error = tracker.procesar_miss(token)
            if not es_valido:
                errores.append(error)
        
        # Simular cierre implícito en ciertos tokens
        tracker.detectar_cierre_estructura(token)
    
    # Forzar cierre final
    _, errores_finales = tracker.forzar_cierre_todas_estructuras()
    errores.extend(errores_finales)
    
    estadisticas = tracker.obtener_estadisticas()
    
    return {
        "es_valido": len(errores) == 0,
        "errores": errores,
        "estadisticas": estadisticas,
        "sugerencias": generar_sugerencias_correccion()
    }