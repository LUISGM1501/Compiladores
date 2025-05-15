"""
* mc_parser.py
*
* 2025/05/11
*
* Implementación del analizador sintáctico (parser) basado en la gramática generada
* con mejoras para manejar casos especiales y recuperación de errores
"""

from .gramatica.Gramatica import Gramatica
from .TokenMap import TokenMap
from .special_tokens import SpecialTokens  # Importamos la clase de tokens especiales

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
        
        # Variables para manejo especial de tokens
        self._segundo_dos_puntos_procesado = False
        
        # Historial de tokens para análisis de contexto
        self.token_history = []
        self.max_history_size = 5  # Mantener historial de los últimos 5 tokens
        
        # Inicializar con el primer token (si existe)
        if self.tokens:
            self.token_actual = self.tokens[0]
        
        self.imprimir_debug("Parser inicializado", 1)
        if debug and len(self.tokens) > 0:
            self.imprimir_debug(f"Tokens recibidos ({len(self.tokens)}): primeros 5 tokens: {[f'{t.type} ({t.lexema})' for t in self.tokens[:5]]}", 2)
    
    def avanzar(self):
        """
        Avanza al siguiente token en la secuencia, ignorando comentarios
        y manteniendo un historial de tokens procesados.
        """
        # Guardar el token actual en el historial antes de avanzar
        if self.token_actual:
            self.token_history.append(self.token_actual)
            # Mantener el historial con tamaño limitado
            if len(self.token_history) > self.max_history_size:
                self.token_history.pop(0)
        
        # Avanzar al siguiente token
        self.posicion_actual += 1
        if self.posicion_actual < len(self.tokens):
            self.token_actual = self.tokens[self.posicion_actual]
            self.imprimir_debug(f"Avanzando a token {self.posicion_actual}: {self.token_actual.type} ('{self.token_actual.lexema}')", 2)
        else:
            # Crear un token ficticio para el fin de archivo
            self.token_actual = None
            self.imprimir_debug("Avanzando a EOF", 2)
    
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
        token_code = TokenMap.get_token_code(token_type)
        
        self.imprimir_debug(f"Obteniendo tipo token: {token_type} -> {token_code}", 3)
        
        if token_code == -1:
            self.reportar_error(f"Token desconocido: {token_type}")
        
        return token_code
    
    def match(self, terminal_esperado):
        """
        Verifica si el token actual coincide con el terminal esperado.
        Maneja casos especiales como PolloCrudo/PolloAsado y otros escenarios específicos.
        
        Args:
            terminal_esperado: El código del terminal que se espera
            
        Returns:
            True si hay coincidencia y se avanza al siguiente token, False en caso contrario
        """
        tipo_token_actual = self.obtener_tipo_token()
        
        # Usar SpecialTokens para verificar si es un identificador especial
        if tipo_token_actual == 91 and self.token_actual and SpecialTokens.is_special_identifier(self.token_actual):
            special_code = SpecialTokens.get_special_token_code(self.token_actual)
            if special_code == terminal_esperado:
                self.imprimir_debug(f"Caso especial: Identificador especial '{self.token_actual.lexema}' reconocido como {SpecialTokens.get_special_token_type(self.token_actual)}", 2)
                self.avanzar()
                return True
        
        # CASO ESPECIAL 4: Manejo para DOBLE_DOS_PUNTOS -> DOS_PUNTOS DOS_PUNTOS
        if terminal_esperado == 112 and tipo_token_actual == 134:  # Si esperamos DOS_PUNTOS y encontramos DOBLE_DOS_PUNTOS
            # Consultar a SpecialTokens para determinar cómo procesar este token
            modo_procesamiento = SpecialTokens.handle_double_colon(self.token_actual)
            
            # Consumir DOBLE_DOS_PUNTOS y configurar un estado para simular que ya se procesaron DOS_PUNTOS
            self.imprimir_debug(f"Caso especial: DOBLE_DOS_PUNTOS reconocido como DOS_PUNTOS", 2)
            self.avanzar()
            
            if modo_procesamiento == 2:  # Si debe tratarse como dos DOS_PUNTOS
                self._segundo_dos_puntos_procesado = True
            
            return True
        
        # Si estamos esperando el segundo DOS_PUNTOS después de un DOBLE_DOS_PUNTOS
        if terminal_esperado == 112 and self._segundo_dos_puntos_procesado:
            self.imprimir_debug(f"Caso especial: Segundo DOS_PUNTOS simulado de DOBLE_DOS_PUNTOS", 2)
            self._segundo_dos_puntos_procesado = False  # Limpiar el estado
            return True
        
        # Manejo para literales en inicialización de variables
        # Usar SpecialTokens para determinar el contexto de declaración
        if (terminal_esperado == 140 or terminal_esperado == 199) and (tipo_token_actual in [87, 88, 89, 90]):
            # Construir un historial de tokens para determinar el contexto
            token_history = self.tokens[max(0, self.posicion_actual-3):self.posicion_actual]
            
            if SpecialTokens.is_declaration_context(token_history):
                self.imprimir_debug(f"Caso especial: Literal en inicialización reconocido", 2)
                return True  # No avanzamos aquí, solo permitimos continuar
        
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
            # Coincidencia encontrada, avanzar al siguiente token
            self.avanzar()
            return True
        else:
            # Error de sintaxis: token inesperado
            if self.token_actual:
                self.reportar_error(f"Se esperaba '{nombre_esperado}' pero se encontró '{self.token_actual.lexema}'")
            else:
                self.reportar_error(f"Se esperaba '{nombre_esperado}' pero se llegó al final del archivo")
            return False
    
    def reportar_error(self, mensaje):
        """
        Reporta un error sintáctico con mensajes específicos y contextuales
        
        Args:
            mensaje: Descripción del error
        """
        if self.token_actual:
            ubicacion = f"línea {self.token_actual.linea}, columna {self.token_actual.columna}"
            token_info = f"'{self.token_actual.lexema}'"
        else:
            ubicacion = "final del archivo"
            token_info = "EOF"
        
        # Mensajes personalizados para errores comunes
        if "DOS_PUNTOS" in mensaje and ("::" in mensaje or "DOBLE_DOS_PUNTOS" in mensaje):
            error = f"Error en {ubicacion}: En la definición de parámetros, se requiere '::' para separar el tipo de los parámetros."
        elif "PolloCrudo" in mensaje or "POLLO_CRUDO" in mensaje:
            error = f"Error en {ubicacion}: Se esperaba la palabra clave 'PolloCrudo' para abrir un bloque de código."
        elif "PolloAsado" in mensaje or "POLLO_ASADO" in mensaje:
            error = f"Error en {ubicacion}: Se esperaba la palabra clave 'PolloAsado' para cerrar un bloque de código."
        elif "Se esperaba 'WORLD_SAVE'" in mensaje or "worldSave" in mensaje:
            error = f"Error en {ubicacion}: El programa debe terminar con 'worldSave'."
        elif "Hay tokens de más" in mensaje:
            error = f"Error en {ubicacion}: Hay contenido después del 'worldSave' final."
        elif "Token inesperado" in mensaje and "id no identificado" in mensaje:
            error = f"Error en {ubicacion}: Identificador '{token_info}' no declarado."
        elif "no terminal" in mensaje and ("Stack" in mensaje or "Spider" in mensaje):
            # Ayudar a identificar errores en declaraciones de variables
            error = f"Error en {ubicacion}: Error de sintaxis en declaración de variable o tipo."
        elif "literal" in mensaje.lower() or "NUMERO" in mensaje or "CADENA" in mensaje:
            error = f"Error en {ubicacion}: Error en la expresión o literal - {mensaje}"
        elif "IGUAL" in mensaje or "=" in mensaje:
            error = f"Error en {ubicacion}: Error en asignación o inicialización de variable."
        # Usar SpecialTokens para detectar si un identificador es un token especial mal usado
        elif self.token_actual and SpecialTokens.is_special_identifier(self.token_actual):
            special_type = SpecialTokens.get_special_token_type(self.token_actual)
            error = f"Error en {ubicacion}: '{self.token_actual.lexema}' debería usarse como palabra clave {special_type}, no como identificador."
        else:
            error = f"Error sintáctico en {ubicacion}: {mensaje}"
        
        # Añadir sugerencia de corrección si está disponible
        if self.token_actual:
            sugerencia = SpecialTokens.suggest_correction(self.token_actual, mensaje)
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
        
        # Puntos seguros ampliados con tokens específicos de Notch-Engine
        puntos_seguros = [
            # Tokens de estructura principal
            9,    # WORLD_SAVE
            1,    # BEDROCK
            2,    # RESOURCE_PACK
            3,    # INVENTORY
            4,    # RECIPE
            5,    # CRAFTING_TABLE 
            6,    # SPAWN_POINT
            
            # Delimitadores de bloques y sentencias
            22,   # POLLO_CRUDO 
            23,   # POLLO_ASADO
            109,  # PUNTO_Y_COMA
            104,  # PARENTESIS_CIERRA
            106,  # CORCHETE_CIERRA
            112,  # DOS_PUNTOS
            
            # Palabras clave importantes
            42,   # SPELL
            43,   # RITUAL
            10,   # STACK
            12,   # SPIDER
            11,   # RUNE
            13,   # TORCH
            14,   # CHEST
            16,   # GHAST
            87,   # NUMERO_ENTERO (para casos de inicialización)
            91,   # IDENTIFICADOR (importante para nombres de variables)
            
            # Operadores significativos
            115,  # FLECHA
            97,   # IGUAL
        ]
        
        # Añadir los follows a los puntos seguros
        puntos_seguros.extend(follows)
        
        # Si estamos cerca del final, sincronizar con el EOF
        if self.posicion_actual >= len(self.tokens) - 5:
            puntos_seguros.append(Gramatica.MARCA_DERECHA)
        
        try:
            self.imprimir_debug(f"Buscando puntos seguros...", 2)
            
            # Obtener follows del no-terminal para mejor recuperación
            follows = self.obtener_follows(simbolo_no_terminal)
            if follows:
                self.imprimir_debug(f"Follows para NT{simbolo_no_terminal - Gramatica.NO_TERMINAL_INICIAL}: {follows}", 3)
                puntos_seguros.extend(follows)
            
            # Avanzar en la entrada hasta encontrar un punto seguro
            tokens_saltados = 0
            inicio_pos = self.posicion_actual
            
            while self.token_actual and self.obtener_tipo_token() not in puntos_seguros:
                tokens_saltados += 1
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
            
            while self.token_actual and self.obtener_tipo_token() not in puntos_seguros:
                tokens_saltados += 1
                self.avanzar()
                
                # Límite de seguridad para evitar bucles infinitos
                if tokens_saltados > 100 or self.posicion_actual >= len(self.tokens):
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
            indice_no_terminal = simbolo_no_terminal - Gramatica.NO_TERMINAL_INICIAL
            follows = []
            
            for col in range(Gramatica.MAX_FOLLOWS):
                follow = Gramatica.getTablaFollows(indice_no_terminal, col)
                if follow == -1:
                    break
                follows.append(follow)
            
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
        
        # MEJORA: Manejar casos especiales para mejorar la compatibilidad utilizando SpecialTokens
        if tipo_token_actual == 91 and self.token_actual and SpecialTokens.is_special_identifier(self.token_actual):
            special_code = SpecialTokens.get_special_token_code(self.token_actual)
            if special_code != -1:
                tipo_token_actual = special_code
                self.imprimir_debug(f"Caso especial: Tratando identificador '{self.token_actual.lexema}' como {SpecialTokens.get_special_token_type(self.token_actual)}", 2)
        
        # Buscar la regla en la tabla de parsing
        numero_regla = Gramatica.getTablaParsing(indice_no_terminal, tipo_token_actual)
        
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
        
        # Apilar los símbolos 
        for simbolo in simbolos_lado_derecho:
            self.stack.append(simbolo)
        
        self.imprimir_estado_pila()
        
        return True
    
    def parse(self):
        """
        Inicia el proceso de análisis sintáctico
        
        Returns:
            True si el análisis fue exitoso, False en caso contrario
        """
        self.imprimir_debug("Iniciando análisis sintáctico", 1)
        
        # Inicializar la pila con el símbolo inicial
        self.stack = [Gramatica.NO_TERMINAL_INICIAL]
        self.imprimir_estado_pila()
        
        try:
            # Mientras haya símbolos en la pila y tokens en la entrada
            while self.stack and (self.token_actual is not None or self.stack[0] == Gramatica.MARCA_DERECHA):
                # Tomar el símbolo del tope de la pila
                simbolo = self.stack.pop()
                
                if self.token_actual:
                    self.imprimir_debug(f"Procesando símbolo: {simbolo} (Token actual: {self.token_actual.type})", 3)
                else:
                    self.imprimir_debug(f"Procesando símbolo: {simbolo} (Token actual: EOF)", 3)
                
                self.imprimir_estado_pila()
                
                # Si es un terminal, hacer match
                if Gramatica.esTerminal(simbolo):
                    self.imprimir_debug(f"Es terminal: {simbolo}", 3)
                    
                    if not self.match(simbolo):
                        # Error de sintaxis al hacer match
                        self.imprimir_debug(f"Error de match para terminal {simbolo}", 1)
                        # Si hay error en el match, sincronizar la entrada
                        if not self.sincronizar(simbolo):
                            # No se pudo sincronizar, continuar con el siguiente símbolo
                            continue
                
                # Si es un no terminal, expandirlo según la tabla de parsing
                elif Gramatica.esNoTerminal(simbolo):
                    self.imprimir_debug(f"Es no terminal: {simbolo}", 3)
                    if not self.procesar_no_terminal(simbolo):
                        # Error al procesar el no terminal, continuar con el siguiente símbolo
                        continue
                
                # Si es un símbolo semántico, ejecutar la acción correspondiente
                elif Gramatica.esSimboloSemantico(simbolo):
                    self.imprimir_debug(f"Es símbolo semántico: {simbolo}", 2)
                    # Implementar acciones semánticas según sea necesario
                    # self.ejecutar_accion_semantica(simbolo)
                    pass
            
            # Si hemos llegado aquí y no hay más tokens, el análisis fue exitoso
            if self.posicion_actual >= len(self.tokens):
                self.imprimir_debug("Análisis completado con éxito", 1)
                return len(self.errores) == 0
            else:
                self.reportar_error("Hay tokens de más al final del archivo")
                return False
        except Exception as e:
            self.reportar_error(f"Error fatal en el parser: {str(e)}")
            import traceback
            traceback.print_exc()  # Imprime el stack trace para depuración
            return False

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
        print(f"Análisis sintáctico fallido con {len(parser_instance.errores)} errores.")
    
    return resultado

# Función para integrarse con el scanner
def iniciar_parser(tokens, debug=False, nivel_debug=2):
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
    
    # Crear una instancia del parser
    parser_instance = Parser(tokens, debug=debug)
    parser_instance.nivel_detalle = nivel_debug  # Configurar nivel de detalle
    
    # Iniciar el análisis sintáctico
    resultado = parser_instance.parse()
    
    # Mostrar el resultado
    if resultado:
        print("Análisis sintáctico completado con éxito.")
    else:
        print(f"Análisis sintáctico fallido con {len(parser_instance.errores)} errores.")
    
    return resultado