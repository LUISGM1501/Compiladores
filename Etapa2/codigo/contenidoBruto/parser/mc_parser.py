"""
* Parser.py
*
* 2025/05/11
*
* Implementación del analizador sintáctico (parser) basado en la gramática generada
"""

from .gramatica.Gramatica import Gramatica
from .TokenMap import TokenMap

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
        nivel_detalle = 2  # Configura aquí el nivel de detalle (1-3)
        
        if nivel <= nivel_detalle:
            print(f"[DEBUG] {mensaje}")

    def imprimir_estado_pila(self, nivel=2):
        """Imprime una versión resumida del estado de la pila"""
        if not self.debug or nivel > 2:
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
        
        # Variables para manejo especial de tokens
        self._segundo_dos_puntos_procesado = False
        
        # Inicializar con el primer token (si existe)
        if self.tokens:
            self.token_actual = self.tokens[0]
        
        self.imprimir_debug("Parser inicializado", 1)
        self.imprimir_debug(f"Tokens recibidos ({len(self.tokens)}): {[f'{t.type} ({t.lexema})' for t in self.tokens]}", 3)
    
    def avanzar(self):
        """
        Avanza al siguiente token en la secuencia, ignorando comentarios
        """
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
        Si esperamos POLLO_CRUDO pero recibimos IDENTIFICADOR con lexema 'PolloCrudo',
        lo consideramos una coincidencia.
        """
        tipo_token_actual = self.obtener_tipo_token()
        
        # Manejo especial para PolloCrudo/PolloAsado
        if terminal_esperado == 22 and tipo_token_actual == 91:  # Si esperamos POLLO_CRUDO y encontramos IDENTIFICADOR
            if self.token_actual.lexema == "PolloCrudo":
                self.avanzar()
                return True
        
        if terminal_esperado == 23 and tipo_token_actual == 91:  # Si esperamos POLLO_ASADO y encontramos IDENTIFICADOR
            if self.token_actual.lexema == "PolloAsado":
                self.avanzar()
                return True
        
        # Manejo especial para worldSave
        if terminal_esperado == 9 and tipo_token_actual == 91:  # Si esperamos WORLD_SAVE y encontramos IDENTIFICADOR
            if self.token_actual.lexema == "worldSave":
                self.avanzar()
                return True
        
        # Manejo para DOBLE_DOS_PUNTOS
        if terminal_esperado == 112 and tipo_token_actual == 134:  # Si esperamos DOS_PUNTOS y encontramos DOBLE_DOS_PUNTOS
            # Consumir DOBLE_DOS_PUNTOS y configurar un estado para simular que ya se procesaron dos DOS_PUNTOS
            self.avanzar()
            self._segundo_dos_puntos_procesado = True
            return True
        
        # Si estamos esperando el segundo DOS_PUNTOS después de un DOBLE_DOS_PUNTOS
        if terminal_esperado == 112 and hasattr(self, '_segundo_dos_puntos_procesado') and self._segundo_dos_puntos_procesado:
            self._segundo_dos_puntos_procesado = False  # Limpiar el estado
            return True
        
        try:
            nombre_esperado = Gramatica.getNombresTerminales(terminal_esperado)
        except:
            nombre_esperado = f"terminal#{terminal_esperado}"
        
        try:
            nombre_actual = Gramatica.getNombresTerminales(tipo_token_actual) if tipo_token_actual < Gramatica.MARCA_DERECHA else "EOF"
        except:
            nombre_actual = f"terminal#{tipo_token_actual}"
        
        self.imprimir_debug(f"Match: esperando {nombre_esperado} ({terminal_esperado}), encontrado {nombre_actual} ({tipo_token_actual})", 2)
        
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
        Reporta un error sintáctico con mensajes específicos
        
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
        if "DOS_PUNTOS" in mensaje and "::" in mensaje:
            error = f"Error en {ubicacion}: En la definición de parámetros, se requiere '::' para separar el tipo de los parámetros."
        elif "PolloCrudo" in mensaje:
            error = f"Error en {ubicacion}: Se esperaba la palabra clave 'PolloCrudo' para abrir un bloque."
        elif "PolloAsado" in mensaje:
            error = f"Error en {ubicacion}: Se esperaba la palabra clave 'PolloAsado' para cerrar un bloque."
        elif "Se esperaba 'WORLD_SAVE'" in mensaje:
            error = f"Error en {ubicacion}: El programa debe terminar con 'worldSave'."
        elif "Token inesperado" in mensaje and "<25>" in mensaje:
            error = f"Error en {ubicacion}: Se esperaba un bloque 'PolloCrudo' después de la declaración de función."
        elif "Hay tokens de más" in mensaje:
            error = f"Error en {ubicacion}: Hay contenido después del 'worldSave' final."
        else:
            error = f"Error sintáctico en {ubicacion}: {mensaje}"
        
        print(error)
        self.errores.append(error)
    
    def sincronizar(self, simbolo_no_terminal):
        """
        Realiza la recuperación de errores avanzando hasta encontrar
        un token en el conjunto Follow del no terminal dado
        
        Args:
            simbolo_no_terminal: Número del no terminal para buscar su Follow
            
        Returns:
            True si se pudo sincronizar, False en caso contrario
        """
        self.imprimir_debug(f"Sincronizando para símbolo {simbolo_no_terminal}", 1)
        
        # Puntos seguros ampliados con tokens específicos de Notch-Engine
        puntos_seguros = [
            # Tokens de estructura
            9,    # WORLD_SAVE
            22,   # POLLO_CRUDO 
            23,   # POLLO_ASADO
            109,  # PUNTO_Y_COMA
            104,  # PARENTESIS_CIERRA
            106,  # CORCHETE_CIERRA
            1,    # BEDROCK
            2,    # RESOURCE_PACK
            3,    # INVENTORY
            4,    # RECIPE
            5,    # CRAFTING_TABLE 
            6,    # SPAWN_POINT
            
            # Tokens de delimitación
            109,  # PUNTO_Y_COMA
            23,   # POLLO_ASADO
            22,   # POLLO_CRUDO
            104,  # PARENTESIS_CIERRA
            106,  # CORCHETE_CIERRA
            112,  # DOS_PUNTOS
            115,  # FLECHA
        ]
        
        try:
            self.imprimir_debug(f"Buscando puntos seguros...", 2)
            
            # Avanzar en la entrada hasta encontrar un punto seguro
            tokens_saltados = 0
            while self.token_actual and self.obtener_tipo_token() not in puntos_seguros:
                tokens_saltados += 1
                self.avanzar()
            
            if self.token_actual:
                self.imprimir_debug(f"Sincronización exitosa en {self.token_actual.type} (saltados: {tokens_saltados})", 1)
                return True
            else:
                self.imprimir_debug("No se pudo sincronizar, fin de archivo", 1)
                return False
        except Exception as e:
            self.imprimir_debug(f"Excepción en sincronizar: {str(e)}", 1)
            return False
    
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
        
        # Buscar la regla en la tabla de parsing
        numero_regla = Gramatica.getTablaParsing(indice_no_terminal, tipo_token_actual)
        
        self.imprimir_debug(f"NT{indice_no_terminal} con token {tipo_token_actual} -> Regla {numero_regla}", 2)
        
        if numero_regla == -1:
            # Error: no hay regla aplicable
            nombre_no_terminal = f"<{indice_no_terminal}>"
            if self.token_actual:
                self.reportar_error(f"Token inesperado '{self.token_actual.lexema}' para el no terminal {nombre_no_terminal}")
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
        
        # Inicializar la pila con el símbolo de fin de archivo y el no terminal inicial
        self.stack = [Gramatica.MARCA_DERECHA, Gramatica.NO_TERMINAL_INICIAL]
        self.imprimir_estado_pila()
        
        try:
            # Mientras haya símbolos en la pila
            while self.stack:
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
                        if not self.sincronizar(simbolo):
                            # No se pudo sincronizar, abortar
                            return False
                
                # Si es un no terminal, expandirlo según la tabla de parsing
                elif Gramatica.esNoTerminal(simbolo):
                    self.imprimir_debug(f"Es no terminal: {simbolo}", 3)
                    if not self.procesar_no_terminal(simbolo):
                        # Error al procesar el no terminal
                        return False
                
                # Si es un símbolo semántico, ejecutar la acción correspondiente
                elif Gramatica.esSimboloSemantico(simbolo):
                    self.imprimir_debug(f"Es símbolo semántico: {simbolo}", 2)
                    # Acción del símbolo semántico...
            
            # Si hemos llegado aquí y no hay más tokens, el análisis fue exitoso
            if self.posicion_actual >= len(self.tokens):
                self.imprimir_debug("Análisis completado con éxito", 1)
                return True
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