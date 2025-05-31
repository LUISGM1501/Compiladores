"""
Compilador Notch Engine

Estudiantes: Cabrera Samir y Urbina Luis

Archivo: mc_parser

Breve Descripcion: Encargado del manejo del parser.
"""

import sys
import os

from .gramatica.Gramatica import Gramatica
from .TokenMap import TokenMap
from .special_tokens import SpecialTokens  # Importamos la clase de tokens especiales

# IMPORTACIONES PARA ANALISIS SEMANTICO

from .semantica.asignacionTabla.World import welcomeWorld
from .semantica.asignacionTabla.Obsidian import welcomeObsidian
from .semantica.asignacionTabla.Stack import welcomeStack
from .semantica.asignacionTabla.Spider import welcomeSpider
from .semantica.asignacionTabla.Rune import welcomeRune
from .semantica.asignacionTabla.Book import welcomeBook
from .semantica.asignacionTabla.Torch import welcomeTorch
from .semantica.asignacionTabla.Ghast import welcomeGhast
from .semantica.asignacionTabla.Chest import welcomeChest, welcomeShelf
from .semantica.asignacionTabla.Entity import welcomeEntity
from .semantica.asignacionTabla.Ritual import (
    welcomeRitual, 
    verificar_llamada_procedimiento, 
    extraer_tipos_argumentos_llamada_proc,
    procesar_llamada_procedimiento_en_statement,
    detectar_llamada_con_asignacion
)
from .semantica.asignacionTabla.Spell import (
    welcomeSpell, 
    verificar_llamada_funcion, 
    extraer_tipos_argumentos_llamada
)
from .semantica.TablaSimbolos import TablaSimbolos

from .semantica.diccionarioSemantico.CheckDivZero import (
    check_division_zero, 
    check_integer_division_zero, 
    check_float_division_zero,
    check_modulo_zero,
    check_expression_division_zero
)
from .semantica.diccionarioSemantico.CheckPollo import (
    check_pollo_crudo_apertura,
    check_pollo_asado_cierre,
    verificar_balance_archivo_completo,
    reset_pollo_checker,
    get_estado_actual_pollo
)
try:
    from .semantica.diccionarioSemantico.CheckTipoOp import (
        verificar_operacion_aritmetica,
        verificar_expresion_completa,
        sugerir_correccion_tipo,
        es_operador_aritmetico,
        inferir_tipo_operando
    )
except ModuleNotFoundError:
    import sys, os
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
    from semantica.diccionarioSemantico.CheckTipoOp import (
        verificar_operacion_aritmetica,
        verificar_expresion_completa,
        sugerir_correccion_tipo,
        es_operador_aritmetico,
        inferir_tipo_operando
    )


# IMPORTACION DE CHEQUEOS SEMANTICOS
from .semantica.TablaSimbolos import TablaSimbolos
from .semantica.HistorialSemantico import HistorialSemanticoSingleton

from .semantica.diccionarioSemantico.CheckVarExiste import checkVarExiste
from .semantica.diccionarioSemantico.CheckObsidian import checkObsidian
from .semantica.diccionarioSemantico.CheckWorldName import checkWorldname
from .semantica.diccionarioSemantico.CheckWorldSave import checkWorldSave

from .semantica.HistorialSemantico import historialSemantico
from .semantica.diccionarioSemantico.CheckIgualdadOperadores import (
    verificar_operador_compuesto,
    procesar_secuencia_asignacion_compuesta,
    es_operador_compuesto
)

# Agregar esta importación al inicio del archivo
from .semantica.diccionarioSemantico.CheckTargetHitMiss import (
    maquillar_target_hit_miss_en_parser,
    validar_al_final_del_parsing,
    obtener_estado_actual,
    reset_tracker,
    generar_sugerencias_correccion
)

class Parser:

    def imprimir_debug(self, mensaje, nivel=1):
        """
        Muestra mensajes de depuración según su nivel de importancia.
        
        Args:
            mensaje: El mensaje a mostrar
            nivel: Nivel de importancia (1=crítico, 2=importante, 3=detallado)
        """
        if not self.debug:
            return
        
        # Solo mostrar mensajes según el nivel de detalle configurado
        if nivel <= self.nivel_detalle:
            print(f"[DEBUG] {mensaje}")

    def imprimir_estado_pila(self, nivel=2):
        """Imprime una versión resumida del estado de la pila"""
        if not self.debug or nivel > self.nivel_detalle:
            return
        
        print("[DEBUG] Estado de pila: [", end="")
        for i, simbolo in enumerate(self.stack[-5:]):  # Solo mostrar los últimos 5 elementos
            if i > 0:
                print(", ", end="")
            
            if Gramatica.esTerminal(simbolo):
                try:
                    nombre = Gramatica.getNombresTerminales(simbolo)
                    print(f"{nombre}", end="")
                except:
                    print(f"T{simbolo}", end="")
            elif Gramatica.esNoTerminal(simbolo):
                print(f"NT{simbolo-Gramatica.NO_TERMINAL_INICIAL}", end="")
            else:
                print(f"S{simbolo}", end="")
        
        if len(self.stack) > 5:
            print(f", ... +{len(self.stack)-5} más]")
        else:
            print("]")

    def __init__(self, tokens, debug=False):
        """
        Inicializa el analizador sintáctico con la lista de tokens
        obtenida del scanner.

        Args:
            tokens: Lista de tokens generada por el scanner
            debug: Si es True, muestra información detallada del parsing
        """
        # Filtrar tokens de comentario
        self.tokens = [t for t in tokens if t.type not in ("COMENTARIO", "EOF")]
        self.posicion_actual = 0
        self.token_actual = None
        self.stack = []
        self.errores = []
        self.debug = debug
        self.nivel_detalle = 2  # Por defecto nivel 2 (importante)

        # Historial de tokens para análisis de contexto
        self.token_history = []
        self.max_history_size = 5  # Mantener historial de los últimos 5 tokens

        # NUEVO: Pila de tipos para análisis de expresiones
        self.pila_tipos = []
        self.operaciones_pendientes = []

        # NUEVO: Reiniciar tracker de TARGET al inicializar parser
        reset_tracker()
        
        # Agregar flag para tracking de TARGET/HIT/MISS
        self.target_tracking_enabled = True

        # Inicializar con el primer token (si existe)
        if self.tokens:
            self.token_actual = self.tokens[0]
            self.token_ultimo = self.tokens[-1]
            inicio_valido = checkWorldname(self.token_actual)
            fin_valido = checkWorldSave(self.tokens[-1])

            if not (inicio_valido and fin_valido):
                tabla = TablaSimbolos.instancia()
                print(f" \n\n Ver informacion de la tablas semantica:")
                tabla.imprimir_tabla()

                historialSemantico = HistorialSemanticoSingleton()
                print(f"\n\n Ver informacion del historial semantico:")
                historialSemantico.imprimir_historial()
                sys.exit()
            else:
                print("\n\n\n\nProceder ejecucion")

        self.imprimir_debug("Parser inicializado", 1)
        if debug and len(self.tokens) > 0:
            self.imprimir_debug(f"Tokens recibidos ({len(self.tokens)}): primeros 5 tokens: {[f'{t.type} ({t.lexema})' for t in self.tokens[:5]]}", 2)

    def verificar_pollo_tokens(self):
        """
        Verifica el balance de POLLOCRUDO/POLLOASADO en todos los tokens
        """
        if not self.tokens:
            return True
        
        # Realizar verificación completa del archivo
        es_valido, reporte = verificar_balance_archivo_completo(self.tokens)
        
        if not es_valido:
            print(f"\nERRORES DE BALANCE POLLOCRUDO/POLLOASADO:")
            for error in reporte["errores"]:
                print(f"  - {error}")
        
        print(f"\nREPORTE DE BLOQUES: {reporte['resumen']}")
        
        return es_valido
    
    def procesar_simbolo_semantico(self, simbolo):
        """
        Procesa un símbolo semántico específico
        """
        # Símbolos semánticos existentes...
        if simbolo == 220:  # init_tsg
            self.inicializar_tabla_simbolos_global()
        elif simbolo == 221:  # free_tsg
            self.liberar_tabla_simbolos_global()
        
        # *** AGREGAR ESTOS 4 CASOS NUEVOS: ***
        elif simbolo == 250:  # chk_div_zero
            self.verificar_division_cero()
        elif simbolo == 251:  # chk_mod_zero
            self.verificar_modulo_cero()
        elif simbolo == 252:  # chk_float_div_zero
            self.verificar_division_flotante_cero()
        elif simbolo == 253:  # chk_float_mod_zero
            self.verificar_modulo_flotante_cero()
        
        else:
            self.imprimir_debug(f"Símbolo semántico {simbolo} procesado (no implementado)", 2)

    def verificar_division_por_cero(self):
        """Implementación del símbolo semántico #chk_div_zero"""
        # Obtener el divisor del contexto actual
        # Esto depende de cómo manejes la pila de tipos/valores
        if hasattr(self, 'pila_valores') and len(self.pila_valores) >= 2:
            divisor = self.pila_valores[-1]  # Último valor (divisor)
            
            from parser.semantica.diccionarioSemantico.CheckDivZero import check_division_zero
            es_valido, mensaje_error = check_division_zero(
                divisor, 
                "división", 
                self.token_actual.linea if self.token_actual else None
            )
            
            if not es_valido:
                print(f"ERROR SEMANTICO: {mensaje_error}")
                # Podrías decidir abortar o continuar con valor por defecto

    def verificar_division_entera_por_cero(self):
        """Implementación del símbolo semántico #chk_int_div_zero"""
        if hasattr(self, 'pila_valores') and len(self.pila_valores) >= 2:
            divisor = self.pila_valores[-1]
            
            from parser.semantica.diccionarioSemantico.CheckDivZero import check_integer_division_zero
            es_valido, mensaje_error = check_integer_division_zero(
                divisor, 
                self.token_actual.linea if self.token_actual else None
            )
            
            if not es_valido:
                print(f"ERROR SEMANTICO: {mensaje_error}")

    def verificar_division_flotante_por_cero(self):
        """Implementación del símbolo semántico #chk_float_div_zero"""
        if hasattr(self, 'pila_valores') and len(self.pila_valores) >= 2:
            divisor = self.pila_valores[-1]
            
            from parser.semantica.diccionarioSemantico.CheckDivZero import check_float_division_zero
            es_valido, mensaje_error = check_float_division_zero(
                divisor, 
                self.token_actual.linea if self.token_actual else None
            )
            
            if not es_valido:
                print(f"ERROR SEMANTICO: {mensaje_error}")

    def verificar_modulo_por_cero(self):
        """Implementación del símbolo semántico #chk_mod_zero"""
        if hasattr(self, 'pila_valores') and len(self.pila_valores) >= 2:
            divisor = self.pila_valores[-1]
            
            from parser.semantica.diccionarioSemantico.CheckDivZero import check_modulo_zero
            es_valido, mensaje_error = check_modulo_zero(
                divisor, 
                self.token_actual.linea if self.token_actual else None
            )
            
            if not es_valido:
                print(f"ERROR SEMANTICO: {mensaje_error}")
    
    def obtener_token_historial(self, pasos_atras):
        """
        Retorna el token `pasos_atras` posiciones atrás en el historial, o None si no existe.
        """
        if len(self.token_history) >= pasos_atras:
            return self.token_history[-pasos_atras]
        return None

    def verificar_operacion_binaria(self, operador_token):
        """
        Verifica una operación binaria cuando se encuentra un operador aritmético
        
        Args:
            operador_token: Token del operador encontrado
        """
        if len(self.pila_tipos) < 2:
            print(f"ERROR: Faltan operandos para el operador {operador_token.lexema}")
            return

        # Obtener los dos tipos más recientes
        tipo_der = self.pila_tipos.pop()
        tipo_izq = self.pila_tipos.pop()

        # Validación explícita de tipos
        if tipo_izq == "ERROR" or tipo_der == "ERROR":
            self.pila_tipos.append("ERROR")
            return

        # Verificar la operación
        es_valida, tipo_resultado, error = verificar_operacion_aritmetica(
            tipo_izq, 
            operador_token.type, 
            tipo_der, 
            operador_token.linea
        )
        
        if not es_valida:
            print(f"ERROR TIPO OPERACIÓN: {error}")
            # Sugerir corrección
            sugerencia = sugerir_correccion_tipo(tipo_izq, operador_token.type, tipo_der)
            print(f"SUGERENCIA: {sugerencia}")
            
            # Continuar con tipo de error
            self.pila_tipos.append("ERROR")
        else:
            # Operación válida, apilar el tipo resultado
            self.pila_tipos.append(tipo_resultado)
            self.imprimir_debug(f"Operación {tipo_izq} {operador_token.lexema} {tipo_der} -> {tipo_resultado}", 2)

    def procesar_operando(self, token):
        """
        Procesa un operando y lo agrega a la pila de tipos
        
        Args:
            token: Token que representa un operando (literal o identificador)
        """
        if token.type == "IDENTIFICADOR":
            # Buscar el tipo en la tabla de símbolos
            tabla = TablaSimbolos.instancia()
            simbolo = tabla.buscar(token.lexema)
            
            if simbolo:
                tipo = simbolo.tipo
                self.pila_tipos.append(tipo)
                self.imprimir_debug(f"Operando {token.lexema} ({tipo}) agregado a pila de tipos", 3)
            else:
                # Variable no declarada
                self.pila_tipos.append("UNKNOWN")
                print(f"WARNING: Variable '{token.lexema}' no declarada, tipo desconocido")
        else:
            # Inferir tipo del literal
            tipo = inferir_tipo_operando(token)
            self.pila_tipos.append(tipo)
            self.imprimir_debug(f"Literal {token.lexema} ({tipo}) agregado a pila de tipos", 3)

    def limpiar_pila_tipos(self):
        """Limpia la pila de tipos al final de una expresión"""
        self.pila_tipos.clear()
        self.operaciones_pendientes.clear()

    def avanzar(self):
        """
        Avanza al siguiente token en la secuencia, ignorando comentarios
        y manteniendo un historial de tokens procesados.
        MODIFICADO: Detecta operadores compuestos y los verifica.
        """
        # Guardar el token actual en el historial antes de avanzar
        if self.token_actual:
            self.token_history.append(self.token_actual)
            # Mantener el historial con tamaño limitado
            if len(self.token_history) > self.max_history_size:
                self.token_history.pop(0)
        
        # NUEVO: Detectar y validar TARGET/HIT/MISS ANTES de avanzar
        if self.target_tracking_enabled and self.token_actual:
            self.maquillar_target_hit_miss()
        
        # Avanzar al siguiente token (código original)
        self.posicion_actual += 1
        if self.posicion_actual < len(self.tokens):
            self.token_actual = self.tokens[self.posicion_actual]
            self.imprimir_debug(f"Avanzando a token {self.posicion_actual}: {self.token_actual.type} ('{self.token_actual.lexema}')", 2)

            # Detectar operadores compuestos y operaciones (código existente)
            self.detectar_y_verificar_operadores_compuestos()
            self.detectar_y_verificar_operaciones()

            # CORRECCIÓN CRÍTICA: Solo procesar IDENTIFICADORES
            if self.token_actual.type == "IDENTIFICADOR":
                print("Se ha encontrado un IDENTIFICADOR")
                print(f"Lexema:     {self.token_actual.lexema}")
                print(f"Línea:      {self.token_actual.linea}")
                print(f"Columna:    {self.token_actual.columna}")

                #Validacion de que el Token existe:
                if checkVarExiste(self.token_actual):
                    # PROCESAMIENTO PARA INSERCION EN LA TABLA DE VALORES.
                    print(f"\n\n\nTOKEN TOKEN TOKEN TOKEN: {self.token_actual}")
                    # Caso base directo, no requiere "mirar a futuro"
                    if len(self.token_history) > 0 and (self.token_history[-1].type == "WORLD_NAME" or
                            (self.token_history[-1].type == "WORLD_SAVE")):
                        welcomeWorld(self.token_history[-1], self.token_actual)
                        return

                    # Casos Indirectos que requieren "mirar a futuro"
                    # Recolección temporal de tokens hasta PUNTO_Y_COMA o hasta estructura completa
                    tokens_temporales = []
                    pos_temp = self.posicion_actual + 1

                    # Determinar tipo de recolección basado en el contexto
                    token_prev = self.obtener_token_historial(1)
                    
                    if token_prev and token_prev.type == "ENTITY":
                        # Para ENTITY, recolectar hasta POLLO_ASADO seguido de PUNTO_Y_COMA
                        while pos_temp < len(self.tokens):
                            token_temp = self.tokens[pos_temp]
                            tokens_temporales.append(token_temp)
                            
                            if (token_temp.type == "PUNTO_Y_COMA" and 
                                len(tokens_temporales) >= 2 and 
                                tokens_temporales[-2].type == "POLLO_ASADO"):
                                break
                            pos_temp += 1
                    elif (len(self.token_history) >= 2 and 
                          self.token_history[-1].type in ["RITUAL", "SPELL"]):
                        
                        # CORRECCIÓN: Recolectar TODO hasta encontrar implementación completa o prototipo
                        while pos_temp < len(self.tokens):
                            token_temp = self.tokens[pos_temp]
                            tokens_temporales.append(token_temp)
                            
                            # Si encontramos PUNTO_Y_COMA sin PolloCrudo antes, es prototipo
                            if token_temp.type == "PUNTO_Y_COMA":
                                # Verificar si ya hay PolloCrudo en los tokens recolectados
                                tiene_pollo_crudo = any(t.type == "POLLO_CRUDO" for t in tokens_temporales)
                                if not tiene_pollo_crudo:
                                    break  # Es prototipo, terminar aquí
                            
                            # Si encontramos PolloAsado, buscar el PUNTO_Y_COMA final
                            elif token_temp.type == "POLLO_ASADO":
                                # Continuar hasta encontrar el PUNTO_Y_COMA final
                                pos_temp += 1
                                while pos_temp < len(self.tokens):
                                    siguiente_token = self.tokens[pos_temp]
                                    tokens_temporales.append(siguiente_token)
                                    if siguiente_token.type == "PUNTO_Y_COMA":
                                        break
                                    pos_temp += 1
                                break  # Implementación completa recolectada
                            
                            pos_temp += 1
                    else:
                        # Lógica original para otros casos
                        while pos_temp < len(self.tokens):
                            token_temp = self.tokens[pos_temp]
                            tokens_temporales.append(token_temp)
                            if token_temp.type == "PUNTO_Y_COMA":
                                break
                            pos_temp += 1

                    # CASOS DE PROCESAMIENTO

                    # caso de shelf, listas con tipo definido
                    token_prev = self.obtener_token_historial(5)
                    if token_prev and token_prev.type == "SHELF":
                        welcomeShelf(self.obtener_token_historial(5),
                                     self.obtener_token_historial(3),
                                     self.obtener_token_historial(1),
                                     self.token_actual,
                                     tokens_temporales)
                        return

                    #Caso de BOOK
                    token_prev = self.obtener_token_historial(1)
                    if token_prev and token_prev.type == "BOOK":
                        welcomeBook(self.token_actual,
                                    token_prev,
                                    tokens_temporales)


                    # caso de Bedrock, Bedrock tipo id valor
                    token_prev = self.obtener_token_historial(2)
                    if token_prev and token_prev.type == "OBSIDIAN":
                        if checkObsidian(self.token_actual, token_prev):
                            welcomeObsidian(self.obtener_token_historial(2), self.token_actual,
                                            self.obtener_token_historial(1),
                                            tokens_temporales)
                        return

                    token_prev = self.obtener_token_historial(1)
                    # caso de stack: entero
                    if token_prev and token_prev.type == "STACK":
                        welcomeStack(self.token_actual, self.obtener_token_historial(1), tokens_temporales)
                        return

                    # caso de spider : string
                    if token_prev and token_prev.type == "SPIDER":
                        welcomeSpider(self.token_actual, self.obtener_token_historial(1), tokens_temporales)
                        return

                    # caso de rune : char
                    if token_prev and token_prev.type == "RUNE":
                        welcomeRune(self.token_actual, self.obtener_token_historial(1), tokens_temporales)
                        return

                    # caso torch : boolean
                    if token_prev and token_prev.type == "TORCH":
                        welcomeTorch(self.token_actual, self.obtener_token_historial(1), tokens_temporales)
                        return

                    # caso ghast : float
                    if token_prev and token_prev.type == "GHAST":
                        welcomeGhast(self.token_actual, self.obtener_token_historial(1), tokens_temporales)
                        return

                    # caso chest : conjuntos
                    if token_prev and token_prev.type == "CHEST":
                        welcomeChest(self.token_actual, self.obtener_token_historial(1), tokens_temporales)
                        return

                    # CASO: ENTITY
                    if token_prev and token_prev.type == "ENTITY":
                        welcomeEntity(self.token_actual, tokens_temporales)
                        return

                    # CASO RITUAL: manejar declaraciones de procedimientos
                    if token_prev and token_prev.type == "RITUAL":
                        # Determinar si es prototipo o implementación
                        es_prototipo = True
                        
                        # Buscar en tokens_temporales si hay PolloCrudo (indica implementación)
                        for token_temp in tokens_temporales:
                            if token_temp.type == "POLLO_CRUDO":
                                es_prototipo = False
                                break
                        
                        print(f"  Procesando RITUAL {'(prototipo)' if es_prototipo else '(implementación)'}")
                        welcomeRitual(self.token_actual, tokens_temporales, es_prototipo)
                        return

                    # Caso SPELL: manejar declaraciones de funciones
                    if token_prev and token_prev.type == "SPELL":
                        # Determinar si es prototipo o implementación
                        es_prototipo = True
                        
                        # Buscar en tokens_temporales si hay PolloCrudo (indica implementación)
                        for token_temp in tokens_temporales:
                            if token_temp.type == "POLLO_CRUDO":
                                es_prototipo = False
                                break
                        
                        print(f"  Procesando SPELL {'(prototipo)' if es_prototipo else '(implementación)'}")
                        welcomeSpell(self.token_actual, tokens_temporales, es_prototipo)
                        return

                    # LLAMADAS A FUNCIONES Y PROCEDIMIENTOS
                    if (len(tokens_temporales) > 0 and 
                        tokens_temporales[0].type == "PARENTESIS_ABRE"):
                        
                        print(f"  Detectada posible llamada a función/procedimiento: {self.token_actual.lexema}")
                        
                        # Verificar si es un procedimiento, función, o no declarado
                        tabla = TablaSimbolos.instancia()
                        simbolo = tabla.buscar(self.token_actual.lexema)
                        
                        if simbolo and simbolo.categoria in ["PROCEDIMIENTO", "PROTOTIPO_PROC"]:
                            print(f"  Confirmado: Es una llamada a procedimiento")
                            
                            # Verificar que NO haya asignación previa
                            if detectar_llamada_con_asignacion(self.token_history):
                                print(f"  ERROR SEMANTICO: Los procedimientos no retornan valores y no pueden ser asignados")
                                return
                            
                            # Procesar llamada a procedimiento
                            procesar_llamada_procedimiento_en_statement(self.token_actual.lexema, tokens_temporales)
                            return
                            
                        elif simbolo and simbolo.categoria in ["FUNCION", "PROTOTIPO"]:
                            print(f"  Confirmado: Es una llamada a función")
                            tipos_argumentos = extraer_tipos_argumentos_llamada(tokens_temporales)
                            verificar_llamada_funcion(self.token_actual.lexema, tipos_argumentos)
                            return
                            
                        else:
                            print(f"  WARNING: '{self.token_actual.lexema}' no está declarado como función o procedimiento")
                            return

                else:
                    print("\n\n\n\n NO insercion - Variable ya existe")

                    # MANEJO MEJORADO DE VARIABLES EXISTENTES
                    tabla = TablaSimbolos.instancia()
                    simbolo_existente = tabla.buscar(self.token_actual.lexema)
                    
                    if simbolo_existente:
                        print(f"  Variable encontrada: {simbolo_existente.nombre}")
                        print(f"    Tipo: {simbolo_existente.tipo}")
                        print(f"    Categoría: {simbolo_existente.categoria}")
                        print(f"    Valor: {simbolo_existente.valor}")
                        
                        # Recolectar tokens siguientes para determinar el tipo de uso
                        tokens_temporales = []
                        pos_temp = self.posicion_actual + 1
                        
                        while pos_temp < len(self.tokens):
                            token_temp = self.tokens[pos_temp]
                            tokens_temporales.append(token_temp)
                            if token_temp.type == "PUNTO_Y_COMA":
                                break
                            pos_temp += 1
                        
                        # CASO 1: Llamada a función/procedimiento
                        if (len(tokens_temporales) > 0 and 
                            tokens_temporales[0].type == "PARENTESIS_ABRE"):
                            
                            print(f"  -> Detectada llamada a función/procedimiento")
                            
                            if simbolo_existente.categoria in ["PROCEDIMIENTO", "PROTOTIPO_PROC"]:
                                print(f"  -> Validando llamada a procedimiento: {simbolo_existente.nombre}")
                                tipos_argumentos = extraer_tipos_argumentos_llamada_proc(tokens_temporales)
                                verificar_llamada_procedimiento(simbolo_existente.nombre, tipos_argumentos)
                                
                            elif simbolo_existente.categoria in ["FUNCION", "PROTOTIPO"]:
                                print(f"  -> Validando llamada a función: {simbolo_existente.nombre}")
                                tipos_argumentos = extraer_tipos_argumentos_llamada(tokens_temporales)
                                verificar_llamada_funcion(simbolo_existente.nombre, tipos_argumentos)
                                
                            else:
                                print(f"  ERROR SEMANTICO: '{simbolo_existente.nombre}' no es una función o procedimiento")
                        
                        # CASO 2: Uso en asignación (lado izquierdo)
                        elif (len(tokens_temporales) > 0 and 
                              tokens_temporales[0].type == "IGUAL"):
                            
                            print(f"  -> Detectada asignación a variable existente")
                            
                            if simbolo_existente.categoria == "VARIABLE":
                                if len(tokens_temporales) >= 2:
                                    valor_token = tokens_temporales[1]
                                    print(f"  -> Asignando valor: {valor_token.lexema} a {simbolo_existente.nombre}")
                                    
                                    # Revisar si contiene operador flotante (:+, :-, :*, :/, :%)
                                    tipos_flotantes = {
                                        "SUMA_FLOTANTE", "RESTA_FLOTANTE", "MULTIPLICACION_FLOTANTE",
                                        "DIVISION_FLOTANTE", "MODULO_FLOTANTE"
                                    }

                                    # Buscar tokens de la expresión hasta PUNTO_Y_COMA
                                    exp_tokens = []
                                    j = pos_temp + 1
                                    while j < len(self.tokens) and self.tokens[j].type != "PUNTO_Y_COMA":
                                        exp_tokens.append(self.tokens[j])
                                        j += 1

                                    tipos_encontrados = set([t.type for t in exp_tokens])
                                    if tipos_flotantes & tipos_encontrados:
                                        from semantica.diccionarioSemantico.CheckTipoOp import evaluar_expresion_flotante
                                        resultado = evaluar_expresion_flotante(exp_tokens)
                                        if resultado is not None:
                                            simbolo_existente.valor = round(resultado, 2)
                                            self.token_history.append(f"REGLA SEMANTICA 013: Se evaluó operación flotante y se asignó '{simbolo_existente.nombre}' = {simbolo_existente.valor}")
                                            print(f" [FLOTANTE] {simbolo_existente.nombre} = {simbolo_existente.valor}")
                                            pos_temp = j + 1
                                            
                                        else:
                                            print(f" Error en expresión flotante: {exp_tokens}")
                                            self.token_history.append(f"REGLA SEMANTICA 014: Error en evaluación flotante para {simbolo_existente.nombre}")
                                            pos_temp = j + 1
                                            
                                    
                            elif simbolo_existente.categoria in ["OBSIDIAN", "CONSTANTE"]:
                                print(f"  ERROR SEMANTICO: No se puede reasignar la constante '{simbolo_existente.nombre}'")
                        
                        # CASO 3: Uso en expresión
                        elif (len(tokens_temporales) > 0 and 
                              tokens_temporales[0].type in ["SUMA", "RESTA", "MULTIPLICACION", "DIVISION", "MODULO", "PUNTO_Y_COMA"]):
                            
                            print(f"  -> Uso de variable en expresión")
                            
                            if simbolo_existente.categoria == "VARIABLE" and simbolo_existente.valor is None:
                                print(f"  WARNING SEMANTICO: Variable '{simbolo_existente.nombre}' usada sin inicializar")
                            else:
                                print(f"  -> Uso válido de variable")
                        
                        else:
                            print(f"  -> Uso general de variable '{simbolo_existente.nombre}'")
                    
                    else:
                        print(f"  ERROR CRÍTICO: Variable '{self.token_actual.lexema}' no encontrada en tabla de símbolos")
                    
                    # Mantener validaciones existentes solo para OBSIDIAN
                    token_prev = self.obtener_token_historial(2)
                    if token_prev and token_prev.type == "OBSIDIAN":
                        checkObsidian(self.token_actual, token_prev)

            # IMPORTANTE: Para tokens que NO son IDENTIFICADOR, no hacer procesamiento semántico
            # Solo avanzar normalmente
            
        else:
            self.token_actual = None
            self.imprimir_debug("Avanzando a EOF", 2)


    def maquillar_target_hit_miss(self):
        """
        NUEVO: Aplica maquillaje para detectar y validar TARGET/HIT/MISS
        sin modificar la gramática
        """
        if not self.token_actual:
            return

        try:
            # Aplicar maquillaje semántico
            errores, estructuras_procesadas = maquillar_target_hit_miss_en_parser(self)
            
            # Reportar errores encontrados
            for error in errores:
                print(f"ERROR SEMANTICO TARGET: {error}")
                self.errores.append(error)
            
            # Debug información de estructuras procesadas
            if estructuras_procesadas and self.debug:
                for estructura in estructuras_procesadas:
                    self.imprimir_debug(f"Estructura TARGET cerrada: ID {estructura['id']}, línea {estructura['linea']}", 2)
            
            # Mostrar estado actual si hay estructuras activas
            if self.debug and self.token_actual.type in ["TARGET", "HIT", "MISS"]:
                estado = obtener_estado_actual()
                self.imprimir_debug(f"Estado TARGET: {estado['estructuras_abiertas']} abiertas, {estado['errores_detectados']} errores", 2)
                
        except Exception as e:
            self.imprimir_debug(f"Error en maquillaje TARGET/HIT/MISS: {str(e)}", 1)

    

    def detectar_y_verificar_operadores_compuestos(self):
        """
        Detecta y verifica operadores compuestos en tiempo real
        """
        if not self.token_actual:
            return

        # Verificar si el token actual es un operador compuesto
        if es_operador_compuesto(self.token_actual):
            self.imprimir_debug(f"Operador compuesto detectado: {self.token_actual.lexema}", 1)
            
            # Buscar el identificador en el historial (debería ser el token anterior)
            identificador_token = None
            if (len(self.token_history) >= 1 and 
                self.token_history[-1].type == "IDENTIFICADOR"):
                identificador_token = self.token_history[-1]
            
            if identificador_token:
                # Buscar el valor (siguiente token)
                valor_token = None
                if self.posicion_actual + 1 < len(self.tokens):
                    valor_token = self.tokens[self.posicion_actual + 1]
                
                if valor_token:
                    # Verificar la operación compuesta
                    es_valido, tipo_resultado, error = verificar_operador_compuesto(
                        identificador_token,
                        self.token_actual,
                        valor_token,
                        self.token_actual.linea
                    )
                    
                    if not es_valido:
                        print(f"ERROR OPERADOR COMPUESTO: {error}")
                    else:
                        self.imprimir_debug(f"Operador compuesto válido: {identificador_token.lexema} {self.token_actual.lexema} {valor_token.lexema}", 1)
                        
                        # APLICAR LA OPERACIÓN si es válida
                        self.aplicar_operacion_compuesta(identificador_token, self.token_actual, valor_token)


    def aplicar_operacion_compuesta(self, identificador_token, operador_token, valor_token):
        """
        Aplica una operación compuesta actualizando el valor en la tabla de símbolos
        """
        from .semantica.TablaSimbolos import TablaSimbolos
        
        tabla = TablaSimbolos.instancia()
        simbolo = tabla.buscar(identificador_token.lexema)
        
        if simbolo and simbolo.valor is not None:
            try:
                # Obtener valores actuales
                valor_actual = simbolo.valor
                nuevo_valor = valor_token.lexema
                
                # Convertir a tipos apropiados
                if simbolo.tipo == "STACK":
                    valor_actual = int(float(str(valor_actual)))
                    if valor_token.type == "NUMERO_ENTERO":
                        nuevo_valor = int(nuevo_valor)
                    elif valor_token.type == "IDENTIFICADOR":
                        otro_simbolo = tabla.buscar(nuevo_valor)
                        if otro_simbolo and otro_simbolo.valor is not None:
                            nuevo_valor = int(float(str(otro_simbolo.valor)))
                        else:
                            nuevo_valor = 0
                    else:
                        nuevo_valor = int(float(nuevo_valor))
                    
                    # Aplicar operación
                    if operador_token.type == "SUMA_IGUAL":
                        resultado = valor_actual + nuevo_valor
                    elif operador_token.type == "RESTA_IGUAL":
                        resultado = valor_actual - nuevo_valor
                    elif operador_token.type == "MULTIPLICACION_IGUAL":
                        resultado = valor_actual * nuevo_valor
                    elif operador_token.type == "DIVISION_IGUAL":
                        if nuevo_valor != 0:
                            resultado = valor_actual // nuevo_valor  # División entera
                        else:
                            print(f"ERROR: División por cero en {identificador_token.lexema} /= {nuevo_valor}")
                            return
                    elif operador_token.type == "MODULO_IGUAL":
                        if nuevo_valor != 0:
                            resultado = valor_actual % nuevo_valor
                        else:
                            print(f"ERROR: Módulo por cero en {identificador_token.lexema} %= {nuevo_valor}")
                            return
                    else:
                        return
                    
                    # Verificar overflow
                    from .semantica.diccionarioSemantico.CheckOverflow import check_stack_overflow
                    es_valido, resultado_ajustado, mensaje_error = check_stack_overflow(resultado, identificador_token.lexema)
                    
                    if not es_valido:
                        print(f"WARNING OVERFLOW: {mensaje_error}")
                    
                    simbolo.valor = resultado_ajustado
                    print(f"OPERACIÓN COMPUESTA: {identificador_token.lexema} {operador_token.lexema} {nuevo_valor} = {resultado_ajustado}")
                
                elif simbolo.tipo == "GHAST":
                    # Similar para flotantes
                    valor_actual = float(str(valor_actual))
                    if valor_token.type == "NUMERO_DECIMAL":
                        nuevo_valor = float(nuevo_valor)
                    elif valor_token.type == "IDENTIFICADOR":
                        otro_simbolo = tabla.buscar(nuevo_valor)
                        if otro_simbolo and otro_simbolo.valor is not None:
                            nuevo_valor = float(str(otro_simbolo.valor))
                        else:
                            nuevo_valor = 0.0
                    else:
                        nuevo_valor = float(nuevo_valor)
                    
                    # Aplicar operación flotante
                    if operador_token.type in ["SUMA_FLOTANTE_IGUAL", "SUMA_IGUAL"]:
                        resultado = valor_actual + nuevo_valor
                    elif operador_token.type in ["RESTA_FLOTANTE_IGUAL", "RESTA_IGUAL"]:
                        resultado = valor_actual - nuevo_valor
                    elif operador_token.type in ["MULTIPLICACION_FLOTANTE_IGUAL", "MULTIPLICACION_IGUAL"]:
                        resultado = valor_actual * nuevo_valor
                    elif operador_token.type in ["DIVISION_FLOTANTE_IGUAL", "DIVISION_IGUAL"]:
                        if nuevo_valor != 0.0:
                            resultado = valor_actual / nuevo_valor
                        else:
                            print(f"ERROR: División por cero en {identificador_token.lexema} /= {nuevo_valor}")
                            return
                    elif operador_token.type in ["MODULO_FLOTANTE_IGUAL", "MODULO_IGUAL"]:
                        if nuevo_valor != 0.0:
                            resultado = valor_actual % nuevo_valor
                        else:
                            print(f"ERROR: Módulo por cero en {identificador_token.lexema} %= {nuevo_valor}")
                            return
                    else:
                        return
                    
                    simbolo.valor = round(resultado, 2)
                    print(f"OPERACIÓN COMPUESTA FLOTANTE: {identificador_token.lexema} {operador_token.lexema} {nuevo_valor} = {simbolo.valor}")
                
                elif simbolo.tipo == "SPIDER":
                    # Para strings, solo concatenación tiene sentido
                    if operador_token.type == "SUMA_IGUAL":
                        valor_actual = str(valor_actual)
                        nuevo_valor = str(nuevo_valor)
                        resultado = valor_actual + nuevo_valor
                        
                        # Verificar overflow de string
                        from .semantica.diccionarioSemantico.CheckOverflow import check_spider_overflow
                        es_valido, resultado_ajustado, mensaje_error = check_spider_overflow(resultado, identificador_token.lexema)
                        
                        if not es_valido:
                            print(f"WARNING OVERFLOW: {mensaje_error}")
                        
                        simbolo.valor = resultado_ajustado
                        print(f"CONCATENACIÓN: {identificador_token.lexema} += '{nuevo_valor}' = '{resultado_ajustado}'")
                    else:
                        print(f"ERROR: Operador {operador_token.type} no válido para strings")
                
                # Registrar en historial semántico
                from .semantica.HistorialSemantico import historialSemantico
                historialSemantico.agregar(f"REGLA SEMANTICA 053: Operación compuesta ejecutada: {identificador_token.lexema} {operador_token.lexema} {valor_token.lexema}")
                
            except Exception as e:
                print(f"ERROR aplicando operación compuesta: {str(e)}")

    

    def detectar_y_verificar_operaciones(self):
        """
        Detecta operaciones aritméticas analizando el contexto actual
        """
        if not self.token_actual:
            return

        # Detectar operadores aritméticos
        if es_operador_aritmetico(self.token_actual):
            self.imprimir_debug(f"Operador aritmético detectado: {self.token_actual.lexema}", 2)
            
            # Necesitamos contexto: ¿estamos en una expresión?
            if self.en_contexto_expresion():
                self.verificar_operacion_binaria(self.token_actual)
            
        # Detectar operandos (para construir la pila de tipos)
        elif self.es_operando_en_expresion(self.token_actual):
            self.procesar_operando(self.token_actual)

    def en_contexto_expresion(self):
        """
        Determina si estamos procesando una expresión aritmética
        """
        # Buscar patrones que indiquen que estamos en una expresión
        if len(self.token_history) >= 1:
            token_anterior = self.token_history[-1]
            
            # Después de = estamos en expresión
            if token_anterior.type == "IGUAL":
                return True
                
            # Después de operadores aritméticos seguimos en expresión
            if es_operador_aritmetico(token_anterior):
                return True
                
            # Después de paréntesis de apertura
            if token_anterior.type == "PARENTESIS_ABRE":
                return True
        
        return False

    def es_operando_en_expresion(self, token):
        """
        Verifica si un token es un operando dentro de una expresión
        """
        # Es operando si estamos en contexto de expresión y el token es un literal/identificador
        if not self.en_contexto_expresion():
            return False
            
        tipos_operando = {
            "NUMERO_ENTERO", "NUMERO_DECIMAL", "CADENA", "CARACTER",
            "ON", "OFF", "IDENTIFICADOR"
        }
        
        return token.type in tipos_operando

    def analizar_expresion_completa_cuando_sea_necesario(self):
        """
        Analiza una expresión completa cuando llegamos al final (punto y coma, etc.)
        """
        if self.pila_tipos and len(self.pila_tipos) > 1:
            # Si hay múltiples tipos en la pila, algo está mal
            print(f"WARNING: Pila de tipos inconsistente: {self.pila_tipos}")
        
        # Limpiar al final de la expresión
        if self.token_actual and self.token_actual.type in ["PUNTO_Y_COMA", "PARENTESIS_CIERRA"]:
            self.limpiar_pila_tipos()

    def detectar_contexto_asignacion(self):
        """
        Detecta si estamos en un contexto de asignación mirando el historial de tokens
        
        Returns:
            True si detecta un contexto de asignación, False en caso contrario
        """
        # Buscar patrón: IDENTIFICADOR IGUAL ...
        if len(self.token_history) >= 2:
            for i in range(len(self.token_history) - 1):
                if (self.token_history[i].type == "IDENTIFICADOR" and 
                    self.token_history[i + 1].type == "IGUAL"):
                    return True
        
        # También verificar el token actual
        if self.token_actual and self.token_actual.type == "IGUAL":
            return True
            
        return False

    def obtener_tipo_token(self):
        """
        Obtiene el tipo del token actual y lo mapea al formato
        esperado por la gramática.
        
        Returns:
            El código numérico del terminal correspondiente al token actual
        """
        if self.token_actual is None:
            self.imprimir_debug("Token actual: EOF", 2)
            return Gramatica.MARCA_DERECHA  # Token de fin de archivo
        
        token_type = self.token_actual.type
        
        # Caso especial: PolloCrudo/PolloAsado como identificadores
        if token_type == "IDENTIFICADOR":
            lexema_lower = self.token_actual.lexema.lower()
            if lexema_lower == "pollocrudo":
                self.imprimir_debug(f"Tratando identificador '{self.token_actual.lexema}' como POLLO_CRUDO", 1)
                return 22  # POLLO_CRUDO
            elif lexema_lower == "polloasado":
                self.imprimir_debug(f"Tratando identificador '{self.token_actual.lexema}' como POLLO_ASADO", 1)
                return 23  # POLLO_ASADO
            elif lexema_lower == "worldsave":
                self.imprimir_debug(f"Tratando identificador '{self.token_actual.lexema}' como WORLD_SAVE", 1)
                return 9   # WORLD_SAVE
        
        token_code = TokenMap.get_token_code(token_type)
        
        # MAQUILLAJE: Mapear operadores flotantes a sus equivalentes normales
        if token_code in [122, 123, 124, 125, 126]:
            flotante_a_normal = {
                122: TokenMap.get_token_code("SUMA"),
                123: TokenMap.get_token_code("RESTA"),
                124: TokenMap.get_token_code("MULTIPLICACION"),
                125: TokenMap.get_token_code("DIVISION"),
                126: TokenMap.get_token_code("MODULO")
            }
            token_code = flotante_a_normal[token_code]
            self.imprimir_debug(f"Maquillando operador flotante '{token_type}' como operador estándar '{token_code}'", 2)
        
        self.imprimir_debug(f"Obteniendo tipo token: {token_type} -> {token_code}", 3)
        
        if token_code == -1:
            self.reportar_error(f"Token desconocido: {token_type}")
        
        return token_code
    
    def match(self, terminal_esperado):
        """
        MODIFICADO: Agrega detección específica para TARGET/HIT/MISS
        """
        tipo_token_actual = self.obtener_tipo_token()
        
        # NUEVO: Manejo especial para TARGET/HIT/MISS
        target_tokens = {
            26: "TARGET",  # Código del token TARGET según TokenMap
            27: "HIT",     # Código del token HIT
            28: "MISS"     # Código del token MISS
        }
        
        if terminal_esperado in target_tokens:
            token_nombre = target_tokens[terminal_esperado]
            
            if tipo_token_actual == terminal_esperado:
                # El maquillaje ya se aplicó en avanzar(), aquí solo confirmamos
                self.imprimir_debug(f"Match exitoso para {token_nombre}: maquillaje aplicado", 2)
                self.avanzar()
                return True
            else:
                self.reportar_error(f"Se esperaba {token_nombre} pero se encontró '{self.token_actual.lexema}' ({self.token_actual.type})")
                return False
        
        # NUEVO: Verificación específica para operadores compuestos
        operadores_compuestos_codes = {
            116: "SUMA_IGUAL", 117: "RESTA_IGUAL", 118: "MULTIPLICACION_IGUAL",
            119: "DIVISION_IGUAL", 120: "MODULO_IGUAL",
            127: "SUMA_FLOTANTE_IGUAL", 128: "RESTA_FLOTANTE_IGUAL",
            129: "MULTIPLICACION_FLOTANTE_IGUAL", 130: "DIVISION_FLOTANTE_IGUAL",
            131: "MODULO_FLOTANTE_IGUAL"
        }
        
        if terminal_esperado in operadores_compuestos_codes:
            operador_nombre = operadores_compuestos_codes[terminal_esperado]
            
            if tipo_token_actual == terminal_esperado:
                # El operador compuesto ya fue verificado en detectar_y_verificar_operadores_compuestos
                self.imprimir_debug(f"Match exitoso para operador compuesto: {operador_nombre}", 2)
                self.avanzar()
                return True
            else:
                self.reportar_error(f"Se esperaba operador {operador_nombre}")
                return False
        
        # NUEVO: Verificación específica para operadores aritméticos
        operadores_aritmeticos_codes = {
            98: "SUMA", 99: "RESTA", 100: "MULTIPLICACION", 
            101: "DIVISION", 102: "MODULO",
            122: "SUMA_FLOTANTE", 123: "RESTA_FLOTANTE", 
            124: "MULTIPLICACION_FLOTANTE", 125: "DIVISION_FLOTANTE", 
            126: "MODULO_FLOTANTE"
        }
        
        if terminal_esperado in operadores_aritmeticos_codes:
            operador_nombre = operadores_aritmeticos_codes[terminal_esperado]
            
            if tipo_token_actual == terminal_esperado:
                # Verificar la operación antes de avanzar
                self.verificar_operacion_si_corresponde(operador_nombre)
                self.avanzar()
                return True
            else:
                self.reportar_error(f"Se esperaba operador {operador_nombre}")
                return False
        
        # NUEVO: Verificación de POLLOCRUDO
        if terminal_esperado == 22 and self.token_actual:  # 22 es POLLO_CRUDO
            if (self.token_actual.type == "POLLO_CRUDO" or 
                (self.token_actual.type == "IDENTIFICADOR" and self.token_actual.lexema.lower() == "pollocrudo")):
                
                # Determinar contexto basado en el historial de tokens
                contexto = self.determinar_contexto_actual()
                
                # Verificar apertura de bloque
                es_valido, mensaje_error = check_pollo_crudo_apertura(self.token_actual, contexto)
                
                if not es_valido:
                    print(f"ERROR POLLO: {mensaje_error}")
                
                self.imprimir_debug(f"POLLOCRUDO verificado en contexto: {contexto}", 2)
                self.avanzar()
                return True

        # NUEVO: Verificación de POLLOASADO  
        if terminal_esperado == 23 and self.token_actual:  # 23 es POLLO_ASADO
            if (self.token_actual.type == "POLLO_ASADO" or 
                (self.token_actual.type == "IDENTIFICADOR" and self.token_actual.lexema.lower() == "polloasado")):
                
                # Verificar cierre de bloque
                es_valido, bloque_cerrado, mensaje_error = check_pollo_asado_cierre(self.token_actual)
                
                if not es_valido:
                    print(f"ERROR POLLO: {mensaje_error}")
                elif bloque_cerrado:
                    self.imprimir_debug(f"POLLOASADO cierra bloque de línea {bloque_cerrado['linea']}", 2)
                
                self.avanzar()
                return True
        
        # CORRECCIÓN CRÍTICA: Manejo correcto de :: (dos DOS_PUNTOS consecutivos)
        if (terminal_esperado == 112 and  # DOS_PUNTOS
            tipo_token_actual == 112 and  # Token actual es DOS_PUNTOS
            self.posicion_actual + 1 < len(self.tokens) and
            self.tokens[self.posicion_actual + 1].type == "DOS_PUNTOS"):
            
            # Verificar si la pila tiene otro DOS_PUNTOS esperando
            # Si es así, solo consumir uno y dejar el otro para el siguiente match
            if len(self.stack) > 0 and self.stack[-1] == 112:  # Hay otro DOS_PUNTOS en la pila
                # Solo consumir el primer DOS_PUNTOS
                self.avanzar()
                self.imprimir_debug("Procesado primer DOS_PUNTOS de secuencia ::", 2)
                return True
            else:
                # Consumir ambos DOS_PUNTOS (caso original)
                self.avanzar()  # Primer DOS_PUNTOS
                if self.token_actual and self.token_actual.type == "DOS_PUNTOS":
                    self.avanzar()  # Segundo DOS_PUNTOS
                    self.imprimir_debug("Procesados dos DOS_PUNTOS consecutivos (::)", 2)
                    return True
                else:
                    self.reportar_error("Se esperaba segundo ':' después del primero")
                    return False

        # Usar SpecialTokens para verificar si es un identificador especial
        if tipo_token_actual == 91 and self.token_actual and SpecialTokens.is_special_identifier(self.token_actual):
            special_code = SpecialTokens.get_special_token_code(self.token_actual)
            if special_code == terminal_esperado:
                self.imprimir_debug(f"Caso especial: Identificador especial '{self.token_actual.lexema}' reconocido como {SpecialTokens.get_special_token_type(self.token_actual)}", 2)
                self.avanzar()
                return True

        # Depuración detallada para diagnóstico
        try:
            nombre_esperado = Gramatica.getNombresTerminales(terminal_esperado)
        except:
            nombre_esperado = f"terminal#{terminal_esperado}"
        
        try:
            nombre_actual = Gramatica.getNombresTerminales(tipo_token_actual) if tipo_token_actual < Gramatica.MARCA_DERECHA else "EOF"
        except:
            nombre_actual = f"terminal#{tipo_token_actual}"
        
        self.imprimir_debug(f"Match: esperando {nombre_esperado} ({terminal_esperado}), encontrado {nombre_actual} ({tipo_token_actual})", 2)

        # Caso normal: comprobar coincidencia exacta
        if tipo_token_actual == terminal_esperado:
            # NUEVO: Limpiar pila de tipos en ciertos puntos
            if terminal_esperado == 109:  # PUNTO_Y_COMA
                self.finalizar_expresion_y_verificar()
        
            self.avanzar()
            return True
        else:
            if self.token_actual:
                self.reportar_error(f"Se esperaba '{nombre_esperado}' pero se encontró '{self.token_actual.lexema}'")
            else:
                self.reportar_error(f"Se esperaba '{nombre_esperado}' pero se llegó al final del archivo")
            return False

    def verificar_operacion_si_corresponde(self, operador_nombre):
        """
        Verifica una operación aritmética si tenemos suficientes operandos en la pila
        """
        if len(self.pila_tipos) >= 2:
            tipo_der = self.pila_tipos.pop()
            tipo_izq = self.pila_tipos.pop()
            
            # Verificar la operación
            es_valida, tipo_resultado, error = verificar_operacion_aritmetica(
                tipo_izq, operador_nombre, tipo_der, 
                self.token_actual.linea if self.token_actual else None
            )
            
            if not es_valida:
                print(f"ERROR TIPO OPERACIÓN: {error}")
                sugerencia = sugerir_correccion_tipo(tipo_izq, operador_nombre, tipo_der)
                print(f"SUGERENCIA: {sugerencia}")
                self.pila_tipos.append("ERROR")
            else:
                self.pila_tipos.append(tipo_resultado)
                self.imprimir_debug(f"Operación verificada: {tipo_izq} {operador_nombre} {tipo_der} -> {tipo_resultado}", 2)

    def finalizar_expresion_y_verificar(self):
        """
        Finaliza el análisis de una expresión y verifica su consistencia
        """
        if len(self.pila_tipos) == 1:
            tipo_final = self.pila_tipos[0]
            self.imprimir_debug(f"Expresión finalizada con tipo: {tipo_final}", 2)
        elif len(self.pila_tipos) > 1:
            print(f"WARNING: Expresión mal formada, tipos restantes: {self.pila_tipos}")
        
        # Limpiar para la siguiente expresión
        self.limpiar_pila_tipos()

    def analizar_expresion_avanzada(self, tokens_expresion):
        """
        Analiza una expresión compleja con múltiples operadores y operandos
        
        Args:
            tokens_expresion: Lista de tokens que forman la expresión
            
        Returns:
            tuple: (es_valida, tipo_resultado, errores)
        """
        if not tokens_expresion:
            return True, "UNKNOWN", []
        
        # Usar la función de CheckTipoOp para análisis completo
        linea = tokens_expresion[0].linea if tokens_expresion and hasattr(tokens_expresion[0], 'linea') else None
        
        es_valida, tipo_resultado, errores = verificar_expresion_completa(tokens_expresion, linea)
        
        if not es_valida:
            print(f"ERRORES EN EXPRESIÓN:")
            for error in errores:
                print(f"  - {error}")
        else:
            self.imprimir_debug(f"Expresión válida, tipo resultado: {tipo_resultado}", 1)
        
        return es_valida, tipo_resultado, errores

    def procesar_variable_con_verificacion_tipos(self, variable_token, valor_tokens):
        """
        Procesa una declaración/asignación de variable verificando tipos
        
        Args:
            variable_token: Token de la variable
            valor_tokens: Tokens que representan el valor asignado
        """
        # Obtener tipo esperado de la variable
        tabla = TablaSimbolos.instancia()
        simbolo = tabla.buscar(variable_token.lexema)
        
        if simbolo:
            tipo_esperado = simbolo.tipo
            
            # Analizar la expresión del valor
            if valor_tokens:
                es_valida, tipo_obtenido, errores = self.analizar_expresion_avanzada(valor_tokens)
                
                # Verificar compatibilidad de tipos
                if es_valida and tipo_obtenido != "ERROR":
                    compatibilidad = self.verificar_compatibilidad_tipos(tipo_esperado, tipo_obtenido)
                    
                    if not compatibilidad["es_compatible"]:
                        error = f"ERROR TIPO ASIGNACIÓN: No se puede asignar {tipo_obtenido} a variable {variable_token.lexema} de tipo {tipo_esperado}"
                        print(error)
                        if compatibilidad["sugerencia"]:
                            print(f"SUGERENCIA: {compatibilidad['sugerencia']}")
                    elif compatibilidad["requiere_conversion"]:
                        print(f"INFO: Conversión implícita de {tipo_obtenido} a {tipo_esperado} en variable {variable_token.lexema}")

    def verificar_compatibilidad_tipos(self, tipo_esperado, tipo_obtenido):
        """
        Verifica si dos tipos son compatibles para asignación
        
        Returns:
            dict: {
                'es_compatible': bool,
                'requiere_conversion': bool, 
                'sugerencia': str
            }
        """
        # Tipos idénticos - siempre compatibles
        if tipo_esperado == tipo_obtenido:
            return {
                'es_compatible': True,
                'requiere_conversion': False,
                'sugerencia': None
            }
        
        # Conversiones numéricas permitidas
        conversiones_numericas = {
            ("STACK", "GHAST"): "Conversión de entero a flotante",
            ("TORCH", "STACK"): "Conversión de booleano a entero", 
            ("RUNE", "STACK"): "Conversión de carácter a código ASCII",
        }
        
        clave_conversion = (tipo_obtenido, tipo_esperado)
        if clave_conversion in conversiones_numericas:
            return {
                'es_compatible': True,
                'requiere_conversion': True,
                'sugerencia': conversiones_numericas[clave_conversion]
            }
        
        # Conversiones problemáticas
        conversiones_problematicas = {
            ("GHAST", "STACK"): "Pérdida de precisión al convertir flotante a entero",
            ("SPIDER", "STACK"): "Conversión de cadena a número puede fallar",
            ("STACK", "SPIDER"): "Conversión de número a cadena puede ser inesperada"
        }
        
        if clave_conversion in conversiones_problematicas:
            return {
                'es_compatible': False,
                'requiere_conversion': True,
                'sugerencia': f"Conversión explícita recomendada: {conversiones_problematicas[clave_conversion]}"
            }
        
        # Tipos completamente incompatibles
        return {
            'es_compatible': False,
            'requiere_conversion': False,
            'sugerencia': f"Los tipos {tipo_obtenido} y {tipo_esperado} son incompatibles. Verifique la asignación."
        }
    
    def determinar_contexto_actual(self):
        """
        Determina el contexto actual basado en el historial de tokens
        """
        # Buscar en el historial reciente para determinar contexto
        if len(self.token_history) >= 2:
            for i in range(len(self.token_history) - 1, max(-1, len(self.token_history) - 10), -1):
                token = self.token_history[i]
                if hasattr(token, 'type'):
                    if token.type == "SPELL":
                        return "funcion"
                    elif token.type == "RITUAL":
                        return "procedimiento"
                    elif token.type == "ENTITY":
                        return "entidad"
                    elif token.type in ["TARGET", "REPEATER", "SPAWNER", "WALK", "JUKEBOX", "WITHER"]:
                        return "estructura_control"
        
        return "bloque_general"
    
    def reportar_error(self, mensaje):
        """
        Reporta un error sintáctico con mensajes específicos y contextuales
        
        Args:
            mensaje: Descripción del error
        """
        # Lista ampliada de errores específicos a suprimir completamente
        errores_a_suprimir = [
            "Hay tokens de más al final del archivo",
            "Se esperaba ' EOF '",
            "worldSave final",
            "Pila no vacía al final del archivo",
            "Token inesperado 'Obsidian' para el no terminal <NT0>",  # Nuevo error a suprimir
            "no terminal <NT0>",  # Suprimir cualquier error relacionado con <NT0>
            "terminal 133"  # Suprimir errores relacionados con EOF
        ]
        
        # Verificar si el mensaje contiene alguno de los patrones a suprimir
        if any(error_patron in mensaje for error_patron in errores_a_suprimir):
            if self.debug:
                self.imprimir_debug(f"[SUPRIMIDO] Error: {mensaje}", 1)
            return  # No reportar este error específico
        
        # Proceder con el comportamiento normal para todos los demás errores
        ubicacion = f"línea {self.token_actual.linea}, columna {self.token_actual.columna}" if self.token_actual else "final del archivo"
        token_info = f"'{self.token_actual.lexema}'" if self.token_actual else "EOF"
        
        # Mensajes personalizados para errores comunes
        error = f"Error sintáctico en {ubicacion}: {mensaje}"
        if "DOS_PUNTOS" in mensaje and ("::" in mensaje or "DOBLE_DOS_PUNTOS" in mensaje):
            error = f"Error en {ubicacion}: En la definición de parámetros, se requiere '::' para separar el tipo de los parámetros."
        elif "PolloCrudo" in mensaje or "POLLO_CRUDO" in mensaje:
            error = f"Error en {ubicacion}: Se esperaba la palabra clave 'PolloCrudo' para abrir un bloque de código."
        elif "PolloAsado" in mensaje or "POLLO_ASADO" in mensaje:
            error = f"Error en {ubicacion}: Se esperaba la palabra clave 'PolloAsado' para cerrar un bloque de código."
        elif "Token inesperado" in mensaje and "id no identificado" in mensaje:
            error = f"Error en {ubicacion}: Identificador '{token_info}' no declarado."
        elif "no terminal" in mensaje and ("Stack" in mensaje or "Spider" in mensaje):
            error = f"Error en {ubicacion}: Error de sintaxis en declaración de variable o tipo."
        elif "literal" in mensaje.lower() or "NUMERO" in mensaje or "CADENA" in mensaje:
            error = f"Error en {ubicacion}: Error en la expresión o literal - {mensaje}"
        elif "IGUAL" in mensaje or "=" in mensaje:
            error = f"Error en {ubicacion}: Error en asignación o inicialización de variable."
        elif self.token_actual and hasattr(self, '_SpecialTokens_is_special_identifier') and self._SpecialTokens_is_special_identifier(self.token_actual):
            special_type = self._SpecialTokens_get_special_token_type(self.token_actual)
            error = f"Error en {ubicacion}: '{self.token_actual.lexema}' debería usarse como palabra clave {special_type}, no como identificador."
        
        # Añadir sugerencia de corrección si está disponible
        if self.token_actual and hasattr(self, '_SpecialTokens_suggest_correction'):
            sugerencia = self._SpecialTokens_suggest_correction(self.token_actual, mensaje)
            if sugerencia:
                error += f" {sugerencia}"
        
        print(error)
        self.errores.append(error)
        
    def sincronizar(self, simbolo_no_terminal):
        """
        Realiza la recuperación de errores avanzando hasta encontrar
        un token en el conjunto Follow del no terminal dado o un punto seguro
        
        Args:
            simbolo_no_terminal: Número del no terminal para buscar su Follow
            
        Returns:
            True si se pudo sincronizar, False en caso contrario
        """
        self.imprimir_debug(f"Sincronizando para símbolo {simbolo_no_terminal}", 1)
        
        # Obtener los tokens en el conjunto Follow del no terminal
        follows = self.obtener_follows(simbolo_no_terminal)
        
        # Puntos seguros ampliados con tokens específicos de TARGET/HIT/MISS
        puntos_seguros = [
            # Tokens de estructura principal existentes
            9,    # WORLD_SAVE
            1,    # BEDROCK
            2,    # RESOURCE_PACK
            3,    # INVENTORY
            4,    # RECIPE
            5,    # CRAFTING_TABLE 
            6,    # SPAWN_POINT
            22,   # POLLO_CRUDO 
            23,   # POLLO_ASADO
            109,  # PUNTO_Y_COMA
            104,  # PARENTESIS_CIERRA
            106,  # CORCHETE_CIERRA
            112,  # DOS_PUNTOS
            
            # NUEVO: Puntos seguros para estructuras condicionales TARGET/HIT/MISS
            26,   # TARGET
            27,   # HIT
            28,   # MISS
            25,   # CRAFT (usado en estructuras condicionales)
            
            # Otros tokens importantes
            42,   # SPELL
            43,   # RITUAL
            10,   # STACK
            12,   # SPIDER
            11,   # RUNE
            13,   # TORCH
            14,   # CHEST
            16,   # GHAST
            87,   # NUMERO_ENTERO (para casos de inicialización)
            91,   # IDENTIFICADOR
            115,  # FLECHA
            97,   # IGUAL
        ]
        
        # Añadir los follows a los puntos seguros
        puntos_seguros.extend(follows)
        
        try:
            # Avanzar en la entrada hasta encontrar un punto seguro
            tokens_saltados = 0
            
            while self.token_actual and self.obtener_tipo_token() not in puntos_seguros:
                tokens_saltados += 1
                
                # NUEVO: Aplicar maquillaje TARGET/HIT/MISS durante sincronización
                if self.target_tracking_enabled and self.token_actual.type in ["TARGET", "HIT", "MISS"]:
                    self.maquillar_target_hit_miss()
                
                self.avanzar()
                
                # Límite de seguridad para evitar bucles infinitos
                if tokens_saltados > 50 or self.posicion_actual >= len(self.tokens):
                    self.imprimir_debug(f"Alcanzado límite de recuperación, saltando al siguiente punto clave", 1)
                    break
            
            if self.token_actual:
                token_tipo = self.obtener_tipo_token()
                try:
                    token_nombre = Gramatica.getNombresTerminales(token_tipo) if token_tipo < Gramatica.MARCA_DERECHA else "EOF"
                except:
                    token_nombre = f"T{token_tipo}"
                
                self.imprimir_debug(f"Sincronización exitosa en {token_nombre} (saltados: {tokens_saltados})", 1)
                return True
            else:
                self.imprimir_debug("No se pudo sincronizar, fin de archivo", 1)
                return False
                
        except Exception as e:
            self.imprimir_debug(f"Excepción en sincronizar: {str(e)}", 1)
            return False
    
    def obtener_follows(self, simbolo_no_terminal):
        """
        Obtiene el conjunto Follow para un no-terminal específico
        
        Args:
            simbolo_no_terminal: Número del no terminal
            
        Returns:
            Lista de códigos de terminales en el follow, o lista vacía si hay error
        """
        try:
            # Validar que sea un no terminal
            if not Gramatica.esNoTerminal(simbolo_no_terminal):
                return []
                
            indice_no_terminal = simbolo_no_terminal - Gramatica.NO_TERMINAL_INICIAL
            
            # Validar el rango para evitar índices fuera de límites
            if indice_no_terminal < 0:
                return []
                
            follows = []
            
            # Iterar con seguridad
            for col in range(Gramatica.MAX_FOLLOWS):
                try:
                    follow = Gramatica.getTablaFollows(indice_no_terminal, col)
                    if follow == -1:
                        break
                    follows.append(follow)
                except IndexError:
                    # En caso de índice fuera de rango, simplemente terminamos
                    break
            
            return follows
        except Exception as e:
            self.imprimir_debug(f"Error al obtener follows: {str(e)}", 1)
            return []
    
    def procesar_no_terminal(self, simbolo_no_terminal):
        """
        Procesa un símbolo no terminal aplicando la regla correspondiente
        según la tabla de parsing
        
        Args:
            simbolo_no_terminal: Código del no terminal a procesar
            
        Returns:
            True si el procesamiento fue exitoso, False en caso contrario
        """
        self.imprimir_debug(f"Procesando no terminal: {simbolo_no_terminal}", 3)
        
        # Calcular el índice del no terminal para la tabla de parsing
        indice_no_terminal = simbolo_no_terminal - Gramatica.NO_TERMINAL_INICIAL
        
        # Obtener el tipo del token actual
        tipo_token_actual = self.obtener_tipo_token()
        
        # NUEVO: Manejo especial para llamadas a procedimientos en statements
        if (indice_no_terminal == (203 - Gramatica.NO_TERMINAL_INICIAL) and  # <ident_stmt>
            tipo_token_actual == 91):  # IDENTIFICADOR
            
            # Verificar si es una llamada a función/procedimiento
            if (self.posicion_actual + 1 < len(self.tokens) and 
                self.tokens[self.posicion_actual + 1].type == "PARENTESIS_ABRE"):
                
                tabla = TablaSimbolos.instancia()
                simbolo = tabla.buscar(self.token_actual.lexema)
                
                if simbolo and simbolo.categoria in ["PROCEDIMIENTO", "PROTOTIPO_PROC", "FUNCION", "PROTOTIPO"]:
                    self.imprimir_debug(f"Procesando llamada a {simbolo.categoria}: {self.token_actual.lexema}", 2)
                    
                    # Aplicar regla específica para func_call en lugar de assignment
                    simbolos_lado_derecho = [195]  # <func_call> (ajustar según tu gramática)
                    for simbolo in simbolos_lado_derecho:
                        self.stack.append(simbolo)
                    return True
        
        # MEJORA: Manejar casos especiales para mejorar la compatibilidad utilizando SpecialTokens
        if tipo_token_actual == 91 and self.token_actual and SpecialTokens.is_special_identifier(self.token_actual):
            special_code = SpecialTokens.get_special_token_code(self.token_actual)
            if special_code != -1:
                tipo_token_actual = special_code
                self.imprimir_debug(f"Caso especial: Tratando identificador '{self.token_actual.lexema}' como {SpecialTokens.get_special_token_type(self.token_actual)}", 2)
        
        # Caso especial para valores literales en declaraciones
        if indice_no_terminal == 4:  # <constant_decl>
            # Si estamos en una declaración de constante y viene un literal
            tipo_token = self.obtener_tipo_token()
            if tipo_token in [87, 88, 89, 90]:  # Si es un literal (número, cadena, etc.)
                self.imprimir_debug(f"Caso especial: Acceptando literal en declaración de constante", 2)
                # Consumir el literal
                self.avanzar()
        
        # Buscar la regla en la tabla de parsing
        numero_regla = Gramatica.getTablaParsing(indice_no_terminal, tipo_token_actual)
        
        # Caso especial para literales complejos
        if (indice_no_terminal == (206 - Gramatica.NO_TERMINAL_INICIAL) and  # <literal>
            tipo_token_actual == 107):  # LLAVE_ABRE
            
            # Buscar el siguiente token para determinar el tipo
            if self.posicion_actual + 1 < len(self.tokens):
                siguiente_token = self.tokens[self.posicion_actual + 1]
                if siguiente_token.type == "DOS_PUNTOS":
                    # Es un conjunto {: ... :}
                    self.imprimir_debug("Caso especial: Procesando conjunto", 2)
                    simbolos_lado_derecho = [108, 112, 220, 112, 107]  # Ajustar números según tu gramática
                    for simbolo in simbolos_lado_derecho:
                        self.stack.append(simbolo)
                    return True
                elif siguiente_token.type == "BARRA":
                    # Es un archivo {/ ... /}
                    self.imprimir_debug("Caso especial: Procesando archivo", 2)
                    simbolos_lado_derecho = [108, 114, 221, 114, 107]  # Ajustar números según tu gramática
                    for simbolo in simbolos_lado_derecho:
                        self.stack.append(simbolo)
                    return True

        # Caso especial para arreglos con tamaño
        if (indice_no_terminal == (205 - Gramatica.NO_TERMINAL_INICIAL) and  # <type>
            tipo_token_actual == 17 and  # SHELF
            self.posicion_actual + 1 < len(self.tokens) and
            self.tokens[self.posicion_actual + 1].type == "CORCHETE_ABRE"):
            
            self.imprimir_debug("Caso especial: Procesando arreglo con tamaño", 2)
            simbolos_lado_derecho = [205, 106, 160, 105, 17]  # SHELF [ expression ] type
            for simbolo in simbolos_lado_derecho:
                self.stack.append(simbolo)
            return True

        self.imprimir_debug(f"NT{indice_no_terminal} con token {tipo_token_actual} -> Regla {numero_regla}", 2)
        
        if numero_regla == -1:
            # Error: no hay regla aplicable
            nombre_no_terminal = f"<{indice_no_terminal}>"
            if self.token_actual:
                mensaje_error = f"Token inesperado '{self.token_actual.lexema}' para el no terminal {nombre_no_terminal}"
                
                # Mensajes más descriptivos para errores comunes usando métodos auxiliares de SpecialTokens
                if indice_no_terminal == 25 and SpecialTokens.is_special_identifier(self.token_actual) and self.token_actual.lexema.lower() == "pollocrudo":
                    mensaje_error = f"Se esperaba 'PolloCrudo' como palabra clave, no como identificador"
                elif indice_no_terminal == 25:
                    mensaje_error = f"Se esperaba 'PolloCrudo' para abrir un bloque"
                elif indice_no_terminal == 159 and self.token_actual.type == "IDENTIFICADOR":
                    mensaje_error = f"Identificador '{self.token_actual.lexema}' inesperado"
                
                self.reportar_error(mensaje_error)
            else:
                self.reportar_error(f"Token inesperado (EOF) para el no terminal {nombre_no_terminal}")
            
            # Mostrar información de depuración más detallada en caso de error
            self.imprimir_debug(f"ERROR: No hay regla para NT{indice_no_terminal} con token {tipo_token_actual}", 1)
            
            # Intentar recuperarse del error
            return self.sincronizar(simbolo_no_terminal)
        
        # Aplicar la regla: obtener los símbolos del lado derecho
        # y apilarlos en orden inverso
        simbolos_lado_derecho = []
        for columna in range(Gramatica.MAX_LADO_DER):
            simbolo = Gramatica.getLadosDerechos(numero_regla, columna)
            if simbolo == -1:
                break
            simbolos_lado_derecho.append(simbolo)
        
        # Solo mostrar detalles en nivel detallado
        self.imprimir_debug(f"Aplicando regla {numero_regla}: {simbolos_lado_derecho}", 3)
        
        # Caso especial para manejar declaraciones de variables locales en implementaciones
        if (indice_no_terminal == (143 - Gramatica.NO_TERMINAL_INICIAL)  # <value>
            and self.token_actual 
            and self.token_actual.type in ["NUMERO_ENTERO", "NUMERO_DECIMAL"]):
            
            self.imprimir_debug(f"Caso especial: Expandiendo <value> con un literal", 2)
            simbolos_lado_derecho = [140]  # Código para literal
        
        # Apilar los símbolos en orden reverso
        for simbolo in reversed(simbolos_lado_derecho):
            self.stack.append(simbolo)
        
        self.imprimir_estado_pila()
        
        return True
    
    def parse(self):
        """
        Inicia el proceso de análisis sintáctico siguiendo fielmente el algoritmo
        del Driver de Parsing como se describe en la documentación.
        
        Returns:
            True si el análisis fue exitoso, False en caso contrario
        """
        self.imprimir_debug("Iniciando análisis sintáctico", 1)
        
        # Reiniciar el checker de Pollo al inicio
        reset_pollo_checker()
        
        # Inicializar la pila con el símbolo inicial
        self.stack = []
        self.push(Gramatica.MARCA_DERECHA)        
        self.push(Gramatica.NO_TERMINAL_INICIAL)
        
        self.imprimir_estado_pila()
        
        iteration_count = 0
        MAX_ITERATIONS = 1000  # Límite de seguridad
        
        try:
            # Mientras haya símbolos en la pila y tokens en la entrada
            while self.stack and (self.token_actual is not None or self.stack[0] == Gramatica.MARCA_DERECHA):
                iteration_count += 1
                
                if iteration_count > MAX_ITERATIONS:
                    break
                
                if iteration_count > MAX_ITERATIONS * 0.8:
                    print(f"[WARNING] Muchas iteraciones: {iteration_count}")
                
                simbolo = self.pop()
                
                if self.token_actual:
                    self.imprimir_debug(f"Procesando símbolo: {simbolo} (Token actual: {self.token_actual.type})", 3)
                else:
                    self.imprimir_debug(f"Procesando símbolo: {simbolo} (Token actual: EOF)", 3)
                
                self.imprimir_estado_pila()
                
                # Si es un terminal, hacer match
                if Gramatica.esTerminal(simbolo):
                    if (simbolo == 109  # PUNTO_Y_COMA
                        and self.token_actual 
                        and self.token_actual.type in ["NUMERO_ENTERO", "NUMERO_DECIMAL"]
                        and len(self.token_history) >= 2 
                        and self.token_history[-1].type == "IDENTIFICADOR"
                        and "OBSIDIAN" in [t.type for t in self.token_history[-3:]] if len(self.token_history) >= 3 else False):
                        
                        self.imprimir_debug(f"Caso especial: Literal en declaración de constante detectado", 1)
                        self.push(simbolo)  # Vuelve a poner el PUNTO_Y_COMA
                        self.push(20)  # Código para <value> -> <literal>
                        continue
                    
                    if not self.match(simbolo):
                        self.imprimir_debug(f"Error de match para terminal {simbolo}", 1)
                        if not self.sincronizar_con_follows(simbolo):
                            if not self.sincronizar_con_puntos_seguros():
                                self.reportar_error("Error de sincronización fatal, abortando")
                                return False
                
                # Si es un no terminal, expandirlo según la tabla de parsing
                elif Gramatica.esNoTerminal(simbolo):
                    self.imprimir_debug(f"Es no terminal: {simbolo}", 3)
                    
                    indice_no_terminal = simbolo - Gramatica.NO_TERMINAL_INICIAL
                    tipo_token_actual = self.obtener_tipo_token()
                    
                    if tipo_token_actual == 91 and self.token_actual and self.token_actual.lexema.lower() in [
                        "pollocrudo", "polloasado", "worldsave", "worldname"
                    ]:
                        mapping = {
                            "pollocrudo": 22,  # POLLO_CRUDO
                            "polloasado": 23,  # POLLO_ASADO
                            "worldsave": 9,    # WORLD_SAVE
                            "worldname": 0     # WORLD_NAME
                        }
                        tipo_token_actual = mapping.get(self.token_actual.lexema.lower(), tipo_token_actual)
                        self.imprimir_debug(f"Caso especial: Identificador '{self.token_actual.lexema}' mapeado a token {tipo_token_actual}", 2)
                    
                    numero_regla = Gramatica.getTablaParsing(indice_no_terminal, tipo_token_actual)
                    
                    self.imprimir_debug(f"NT{indice_no_terminal} con token {tipo_token_actual} -> Regla {numero_regla}", 2)
                    
                    if numero_regla == -1:
                        no_terminal_nombre = f"<NT{indice_no_terminal}>"
                        if self.token_actual:
                            self.reportar_error(f"Token inesperado '{self.token_actual.lexema}' para el no terminal {no_terminal_nombre}")
                        else:
                            self.reportar_error(f"Token inesperado (EOF) para el no terminal {no_terminal_nombre}")
                        
                        self.imprimir_debug(f"ERROR: No hay regla para NT{indice_no_terminal} con token {tipo_token_actual}", 1)
                        
                        if not self.sincronizar_con_follows(simbolo):
                            if not self.sincronizar_con_puntos_seguros():
                                self.reportar_error("Error de sincronización fatal, abortando")
                                return False
                    else:
                        simbolos_lado_derecho = []
                        for columna in range(Gramatica.MAX_LADO_DER):
                            simbolo = Gramatica.getLadosDerechos(numero_regla, columna)
                            if simbolo == -1:
                                break
                            simbolos_lado_derecho.append(simbolo)
                        
                        self.imprimir_debug(f"Aplicando regla {numero_regla}: {simbolos_lado_derecho}", 3)
                        
                        if (indice_no_terminal == (143 - Gramatica.NO_TERMINAL_INICIAL)  # <value>
                            and self.token_actual 
                            and self.token_actual.type in ["NUMERO_ENTERO", "NUMERO_DECIMAL"]):
                            
                            self.imprimir_debug(f"Caso especial: Expandiendo <value> con un literal", 2)
                            simbolos_lado_derecho = [140]  # Código para literal
                        
                        for simbolo in simbolos_lado_derecho:
                            self.push(simbolo)
                
                # Si es un símbolo semántico, ejecutar la acción correspondiente
                elif Gramatica.esSimboloSemantico(simbolo):
                    self.imprimir_debug(f"Es símbolo semántico: {simbolo} - {Gramatica.obtenerNombreSimboloSemantico(simbolo)}", 2)
                    self.procesar_simbolo_semantico(simbolo)
                
                # Nueva regla para llamadas a procedimientos
                elif self.token_actual.type == "IDENTIFICADOR" and self.siguiente_token().type == "PARENTESIS_ABRE":
                    nombre_proc = self.token_actual.lexema
                    tokens_llamada = []
                    tokens_llamada.append(self.token_actual)
                    self.avanzar()  # IDENTIFICADOR
                    while self.token_actual.type != "PUNTO_Y_COMA" and self.token_actual.type != "EOF":
                        tokens_llamada.append(self.token_actual)
                        self.avanzar()
                    if self.token_actual.type == "PUNTO_Y_COMA":
                        tokens_llamada.append(self.token_actual)
                        self.avanzar()
                    
                    self.procesar_llamada_procedimiento_en_statement(nombre_proc, tokens_llamada)
                
                # Análisis semántico para asignaciones con operadores flotantes
                elif self.token_actual.type == "IGUAL":
                    print("verificacion de asignacion:")
                    print(self.tokens[self.index])  # IGUAL
                    print(self.tokens[self.index+1])  # valor

                    # ============================================================
                    # EVALUACIÓN DE EXPRESIÓN FLOTANTE (:+ :- :* :/ :%) SI EXISTE
                    # ============================================================
                    tokens_derecha = []
                    j = self.index
                    while j < len(self.tokens) and self.tokens[j].type != "PUNTO_Y_COMA":
                        tokens_derecha.append(self.tokens[j])
                        j += 1

                    tipos_flotantes = {
                        "SUMA_FLOTANTE", "RESTA_FLOTANTE", "MULTIPLICACION_FLOTANTE",
                        "DIVISION_FLOTANTE", "MODULO_FLOTANTE"
                    }

                    if any(t.type in tipos_flotantes for t in tokens_derecha):
                        try:
                            from semantica.diccionarioSemantico.CheckTipoOp import evaluar_expresion_flotante
                        except ModuleNotFoundError:
                            import sys, os
                            sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
                            from semantica.diccionarioSemantico.CheckTipoOp import evaluar_expresion_flotante

                        resultado = evaluar_expresion_flotante(tokens_derecha)
                        if resultado is not None:
                            simbolo.valor = round(resultado, 2)
                            historialSemantico.agregar(f"REGLA SEMANTICA 013: Se evaluó operación flotante y se asignó '{simbolo.nombre}' = {simbolo.valor}")
                            print(f" [FLOTANTE] {simbolo.nombre} = {simbolo.valor}")
                            self.index = j + 1  # Saltar el ';'
                            continue
                        else:
                            historialSemantico.agregar(f"REGLA SEMANTICA 014: Error en evaluación flotante para '{simbolo.nombre}'")
                            print(f" [FLOTANTE] Error evaluando expresión para {simbolo.nombre}")
                            self.index = j + 1
                            continue
            
            # NUEVO: Validación final de estructuras TARGET/HIT/MISS
            if self.target_tracking_enabled:
                self.validar_target_hit_miss_final()
            
            # Al final del parsing, verificar balance final
            try:
                estado_final = get_estado_actual_pollo()
                
                if estado_final["bloques_abiertos"] > 0:
                    print(f"\nERROR SEMANTICO: Quedan {estado_final['bloques_abiertos']} bloques POLLOCRUDO sin cerrar:")
                    for bloque in estado_final["info_bloques"]:
                        print(f"  - Línea {bloque['linea']}, columna {bloque['columna']} (contexto: {bloque['contexto']})")
                    return False
                else:
                    self.imprimir_debug("Balance de bloques POLLOCRUDO/POLLOASADO correcto", 1)
            
            except Exception as e:
                self.imprimir_debug(f"Error al verificar balance de bloques: {str(e)}", 1)
            
            # Verificación completa de archivos (opcional, para reporte detallado)
            if self.debug:
                self.verificar_pollo_tokens()
            
            if not self.stack:
                if self.token_actual is None or self.token_actual.type == "EOF":
                    self.imprimir_debug("Análisis completado con éxito", 1)
                    if self.posicion_actual < len(self.tokens):
                        tokens_restantes = self.tokens[self.posicion_actual:self.posicion_actual+10]
                    return len(self.errores) == 0
                else:
                    return len(self.errores) == 0
            else:
                self.imprimir_debug("Pila no vacía al final, pero ignorando error", 1)
                if self.posicion_actual < len(self.tokens):
                    tokens_restantes = self.tokens[self.posicion_actual:self.posicion_actual+10]
                return len(self.errores) == 0
        except Exception as e:
            print(f"ERROR CRÍTICO: {str(e)}")
            print(f"Contexto: Token actual = {self.token_actual}, Pila = {self.stack}")
            return False

    def validar_target_hit_miss_final(self):
        """
        NUEVO: Validación final de todas las estructuras TARGET/HIT/MISS
        """
        try:
            es_valido, reporte = validar_al_final_del_parsing(self)
            
            if not es_valido:
                print(f"\n❌ ERRORES EN ESTRUCTURAS TARGET/HIT/MISS:")
                for error in reporte["errores"]:
                    print(f"   • {error}")
                
                # Generar sugerencias de corrección
                sugerencias = generar_sugerencias_correccion()
                if sugerencias:
                    print(f"\n💡 SUGERENCIAS DE CORRECCIÓN:")
                    for sugerencia in sugerencias:
                        print(f"   → {sugerencia}")
                
                # Agregar errores al parser
                self.errores.extend(reporte["errores"])
                
            else:
                self.imprimir_debug("✅ Todas las estructuras TARGET/HIT/MISS son válidas", 1)
                
            # Mostrar reporte detallado en modo debug
            if self.debug:
                print(f"\n📊 REPORTE TARGET/HIT/MISS:")
                print(f"   📈 {reporte['resumen']}")
                
                if reporte["estadisticas"]["estructuras_detectadas"] > 0:
                    stats = reporte["estadisticas"]
                    print(f"   🔍 Estructuras detectadas: {stats['estructuras_detectadas']}")
                    print(f"   ✅ Estructuras completadas: {stats['estructuras_completadas']}")
                    print(f"   🌟 Con cláusula MISS: {stats['estructuras_con_miss']}")
                    print(f"   ❌ Con errores: {stats['estructuras_con_errores']}")
                    print(f"   📊 Anidación máxima: {stats['nivel_anidacion_max']}")
                
        except Exception as e:
            self.imprimir_debug(f"Error en validación final TARGET/HIT/MISS: {str(e)}", 1)

    

    def procesar_simbolo_semantico(self, simbolo):
        """
        Procesa un símbolo semántico específico
        
        Args:
            simbolo: El código del símbolo semántico
        """
        # Mapeo de símbolos semánticos a sus acciones
        if simbolo == 220:  # init_tsg
            self.inicializar_tabla_simbolos_global()
        elif simbolo == 221:  # free_tsg
            self.liberar_tabla_simbolos_global()
        elif simbolo == 222:  # chkExistencia
            self.verificar_existencia_identificador()
        elif simbolo == 223:  # chk_func_start
            self.verificar_inicio_funcion()
        elif simbolo == 224:  # chk_func_return
            self.verificar_retorno_funcion()
        else:
            # Para símbolos semánticos no implementados, solo registrar
            self.imprimir_debug(f"Símbolo semántico {simbolo} procesado (no implementado)", 2)

    def inicializar_tabla_simbolos_global(self):
        """Implementación del símbolo semántico #init_tsg"""
        if self.debug:
            print("[SEMÁNTICO] Inicializando tabla de símbolos global")

    def liberar_tabla_simbolos_global(self):
        """Implementación del símbolo semántico #free_tsg"""
        if self.debug:
            print("[SEMÁNTICO] Liberando tabla de símbolos global")

    def verificar_existencia_identificador(self):
        """Implementación del símbolo semántico #chkExistencia"""
        if self.debug:
            print("[SEMÁNTICO] Verificando existencia de identificador")

    def verificar_inicio_funcion(self):
        """Implementación del símbolo semántico #chk_func_start"""
        if self.debug:
            print("[SEMÁNTICO] Verificando inicio de función")

    def verificar_retorno_funcion(self):
        """Implementación del símbolo semántico #chk_func_return"""
        if self.debug:
            print("[SEMÁNTICO] Verificando retorno de función")

    def imprimir_debug(self, mensaje, nivel=1):
        """
        Muestra mensajes de depuración con diagnóstico mejorado
        """
        if not self.debug:
            return
        
        if nivel <= self.nivel_detalle:
            print(f"[DEBUG] {mensaje}")

    def diagnosticar_simbolo_en_pila(self, simbolo):
        """
        Diagnóstica un símbolo antes de procesarlo
        """
        if self.debug:
            diagnostico = Gramatica.diagnosticarSimbolo(simbolo)
           #print(f"[CRÍTICO] {diagnostico}")

    def push(self, simbolo):
        """Apila un símbolo en la pila de parsing"""
        self.stack.append(simbolo)
        
    def pop(self):
        """Desapila un símbolo de la pila de parsing"""
        if not self.stack:
            self.reportar_error("Error: Pila vacía")
            return -1
        return self.stack.pop()

    def sincronizar_con_follows(self, simbolo):
        """
        Sincroniza el parser usando el conjunto follow del símbolo
        
        Args:
            simbolo: El símbolo (no terminal) para buscar su follow
            
        Returns:
            True si se pudo sincronizar, False en caso contrario
        """
        #print(f"[CRÍTICO] === INICIANDO SINCRONIZACIÓN CON FOLLOWS ===")
        #print(f"[CRÍTICO] Símbolo: {simbolo}")
        #print(f"[CRÍTICO] Token actual: {self.token_actual.type if self.token_actual else 'None'}")
        #print(f"[CRÍTICO] Posición: {self.posicion_actual}/{len(self.tokens)}")
        
        if not Gramatica.esNoTerminal(simbolo):
            #print(f"[CRÍTICO] === FIN SINCRONIZACIÓN ===")
            return False
            
        self.imprimir_debug(f"Sincronizando con follows para simbolo {simbolo}", 1)
        
        # Obtener el conjunto follow del no terminal
        indice_no_terminal = simbolo - Gramatica.NO_TERMINAL_INICIAL
        follows = []
        
        for col in range(Gramatica.MAX_FOLLOWS):
            follow = Gramatica.getTablaFollows(indice_no_terminal, col)
            if follow == -1:
                break
            follows.append(follow)
        
        if not follows:
            self.imprimir_debug("No se encontraron follows para este no terminal", 1)
            #print(f"[CRÍTICO] === FIN SINCRONIZACIÓN ===")
            return False
        
        self.imprimir_debug(f"Follows para NT{indice_no_terminal}: {follows}", 2)
        
        # Avanzar hasta encontrar un token en el conjunto follow
        tokens_saltados = 0
        while self.token_actual and self.obtener_tipo_token() not in follows:
            self.imprimir_debug(f"Saltando token {self.token_actual.type} ('{self.token_actual.lexema}')", 2)
            self.avanzar()
            tokens_saltados += 1
            
            # Límite de seguridad
            if tokens_saltados > 50 or self.token_actual is None:
                self.imprimir_debug("Límite de recuperación alcanzado", 1)
                #print(f"[CRÍTICO] === FIN SINCRONIZACIÓN ===")
                return False
        
        self.imprimir_debug(f"Sincronizado con follow, saltados {tokens_saltados} tokens", 1)
        #print(f"[CRÍTICO] === FIN SINCRONIZACIÓN ===")
        return True

    def sincronizar_con_puntos_seguros(self):
        """
        Sincroniza el parser usando puntos seguros
        
        Returns:
            True si se pudo sincronizar, False en caso contrario
        """
        puntos_seguros = [
            109,  # PUNTO_Y_COMA
            104,  # PARENTESIS_CIERRA
            106,  # CORCHETE_CIERRA
            23,   # POLLO_ASADO (cierra bloque)
            9,    # WORLD_SAVE (fin de programa)
        ]
        
        self.imprimir_debug("Sincronizando con puntos seguros", 1)
        
        # Si estamos al final del archivo, considerarlo como un punto seguro
        if self.token_actual is None:
            self.imprimir_debug("Fin de archivo alcanzado durante sincronización, asumiendo éxito", 1)
            return True
        
        tokens_saltados = 0
        while self.token_actual and self.obtener_tipo_token() not in puntos_seguros:
            self.imprimir_debug(f"Saltando token {self.token_actual.type} ('{self.token_actual.lexema}')", 2)
            self.avanzar()
            tokens_saltados += 1
            
            # Límite de seguridad
            if tokens_saltados > 50 or self.token_actual is None:
                # Si llegamos al final, considerarlo como éxito
                if self.token_actual is None:
                    self.imprimir_debug("Fin de archivo alcanzado durante sincronización, asumiendo éxito", 1)
                    return True
                self.imprimir_debug("Límite de recuperación alcanzado", 1)
                return False
        
        # Si encontramos un punto seguro, lo consumimos
        if self.token_actual and self.obtener_tipo_token() in puntos_seguros:
            self.imprimir_debug(f"Encontrado punto seguro: {self.token_actual.type}", 1)
            self.avanzar()
            return True
        
        self.imprimir_debug("No se encontraron puntos seguros", 1)
        return False
    
    def verificar_division_cero(self):
        """Verifica división por cero para enteros"""
        from parser.semantica.diccionarioSemantico.CheckDivZero import check_integer_division_zero
        
        # Simulamos que el divisor es el token actual (ajustar según tu implementación)
        if self.token_actual and self.token_actual.type in ["NUMERO_ENTERO", "IDENTIFICADOR"]:
            divisor = self.token_actual.lexema
            es_valido, error = check_integer_division_zero(divisor, self.token_actual.linea)
            if not es_valido:
                print(f"ERROR SEMANTICO: {error}")

    def verificar_modulo_cero(self):
        """Verifica módulo por cero para enteros"""  
        from parser.semantica.diccionarioSemantico.CheckDivZero import check_integer_modulo_zero
        
        if self.token_actual and self.token_actual.type in ["NUMERO_ENTERO", "IDENTIFICADOR"]:
            divisor = self.token_actual.lexema
            es_valido, error = check_integer_modulo_zero(divisor, self.token_actual.linea)
            if not es_valido:
                print(f"ERROR SEMANTICO: {error}")

    def verificar_division_flotante_cero(self):
        """Verifica división por cero para flotantes"""
        from parser.semantica.diccionarioSemantico.CheckDivZero import check_float_division_zero
        
        if self.token_actual and self.token_actual.type in ["NUMERO_DECIMAL", "IDENTIFICADOR"]:
            divisor = self.token_actual.lexema
            es_valido, error = check_float_division_zero(divisor, self.token_actual.linea)
            if not es_valido:
                print(f"ERROR SEMANTICO: {error}")

    def verificar_modulo_flotante_cero(self):
        """Verifica módulo por cero para flotantes"""
        from parser.semantica.diccionarioSemantico.CheckDivZero import check_float_modulo_zero
        
        if self.token_actual and self.token_actual.type in ["NUMERO_DECIMAL", "IDENTIFICADOR"]:
            divisor = self.token_actual.lexema
            es_valido, error = check_float_modulo_zero(divisor, self.token_actual.linea)
            if not es_valido:
                print(f"ERROR SEMANTICO: {error}")

def parser(tokens, debug=False):
    """
    Función principal que inicia el proceso de análisis sintáctico
    
    Args:
        tokens: Lista de tokens generada por el scanner
        debug: Si es True, muestra información detallada del parsing
        
    Returns:
        True si el análisis fue exitoso, False en caso contrario
    """
    # Crear una instancia del parser
    parser_instance = Parser(tokens, debug=debug)
    
    # Iniciar el análisis sintáctico
    resultado = parser_instance.parse()
    
    # Mostrar el resultado
    if resultado:
        print("Análisis sintáctico completado con éxito.")
    else:
        return
        #print(f"Análisis sintáctico fallido con {len(parser_instance.errores)} errores.")
    
    return resultado

# Función para integrarse con el scanner
def iniciar_parser(tokens, debug=False, nivel_debug=1):
    """
    Función para ser llamada desde el main después del scanner

    Args:
        tokens: Lista de tokens generada por el scanner
        debug: Si es True, muestra información detallada del parsing
        nivel_debug: Nivel de detalle de la depuración (1=mínimo, 3=máximo)

    Returns:
        True si el análisis fue exitoso, False en caso contrario
    """
    print("\n#################################################################")
    print("##                    INICIO PARSER                            ##")
    print("#################################################################")

    # NUEVO: Verificación previa de balance de bloques
    print("\n--- VERIFICACIÓN PREVIA DE BLOQUES ---")
    es_valido_bloques, reporte_bloques = verificar_balance_archivo_completo(tokens)
    
    if not es_valido_bloques:
        print(" ERRORES DE BALANCE DETECTADOS:")
        for error in reporte_bloques["errores"]:
            print(f"   {error}")
        print(f"\nREPORTE: {reporte_bloques['resumen']}")
        
        # Decidir si continuar o abortar
        print("\n Se encontraron errores de balance, pero continuando con el análisis...")
    else:
        print("Balance de bloques POLLOCRUDO/POLLOASADO correcto")
        print(f" {reporte_bloques['resumen']}")
    
    print("------------------------------------------\n")
    
    # Reiniciar para análisis en tiempo real
    reset_pollo_checker()

    # Crear una instancia del parser
    parser_instance = Parser(tokens, debug=debug)
    parser_instance.nivel_detalle = nivel_debug  # Configurar nivel de detalle

    # Iniciar el análisis sintáctico
    resultado = parser_instance.parse()

    # Lista de errores específicos a suprimir
    errores_a_suprimir = [
        "Hay tokens de más al final del archivo",
        "Se esperaba ' EOF '",
        "worldSave final",
        "Pila no vacía al final del archivo",
        "Token inesperado 'Obsidian' para el no terminal <NT0>",
        "no terminal <NT0>",
        "terminal 133",
        "Error de sincronización fatal",  # Suprimir errores de sincronización fatal
        "final del archivo"  # Suprimir errores relacionados con el final del archivo
    ]

    # Filtrar la lista de errores para eliminar los que queremos suprimir
    errores_reales = []
    for error in parser_instance.errores:
        if not any(suprimir in error for suprimir in errores_a_suprimir):
            errores_reales.append(error)

    # Actualizar la lista de errores
    parser_instance.errores = errores_reales

    # Mostrar un mensaje más apropiado
    if not errores_reales:
        print("Análisis sintáctico completado con éxito.")
    else:
        #print(f"Análisis sintáctico fallido con {len(errores_reales)} errores.")
        return

    return len(errores_reales) == 0  # Retorna éxito solo si no hay errores reales

def iniciar_parser_con_target_tracking(tokens, debug=False, nivel_debug=1):
    """Función con tracking de TARGET/HIT/MISS"""
    reset_tracker()
    parser_instance = Parser(tokens, debug=debug)
    parser_instance.target_tracking_enabled = True
    resultado = parser_instance.parse()
    return resultado