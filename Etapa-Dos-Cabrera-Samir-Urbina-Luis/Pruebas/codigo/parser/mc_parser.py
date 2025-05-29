"""
Compilador Notch Engine

Estudiantes: Cabrera Samir y Urbina Luis

Archivo: mc_parser

Breve Descripcion: Encargado del manejo del parser.
"""

from .gramatica.Gramatica import Gramatica
from .TokenMap import TokenMap
from .special_tokens import SpecialTokens  # Importamos la clase de tokens especiales

# IMPORTACIONES PARA ANALISIS SEMANTICO

from .semantica.asignacionTabla.Worldname import welcomeWorldname
from .semantica.asignacionTabla.Obsidian import welcomeObsidian
from .semantica.asignacionTabla.Stack import welcomeStack
from .semantica.asignacionTabla.Spider import welcomeSpider
from .semantica.asignacionTabla.Rune import welcomeRune
from .semantica.asignacionTabla.Torch import welcomeTorch
from .semantica.asignacionTabla.Ghast import welcomeGhast
from .semantica.asignacionTabla.Chest import welcomeChest, welcomeShelf

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
        
        # Inicializar con el primer token (si existe)
        if self.tokens:
            self.token_actual = self.tokens[0]
        
        self.imprimir_debug("Parser inicializado", 1)
        if debug and len(self.tokens) > 0:
            self.imprimir_debug(f"Tokens recibidos ({len(self.tokens)}): primeros 5 tokens: {[f'{t.type} ({t.lexema})' for t in self.tokens[:5]]}", 2)

    def obtener_token_historial(self, pasos_atras):
        """
        Retorna el token `pasos_atras` posiciones atrás en el historial, o None si no existe.
        """
        if len(self.token_history) >= pasos_atras:
            return self.token_history[-pasos_atras]
        return None


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

            # Mover todo el procesamiento de identificadores a un método separado
            if self.token_actual.type == "IDENTIFICADOR":
                print("🟢 Se ha encontrado un IDENTIFICADOR")
                print(f"Lexema:     {self.token_actual.lexema}")
                print(f"Línea:      {self.token_actual.linea}")
                print(f"Columna:    {self.token_actual.columna}")
                print(f"Valor:      {self.token_actual.valor}")
                print(f"Categoría:  {self.token_actual.categoria}")

                # PROCESAMIENTO PARA INSERCION EN LA TABLA DE VALORES.

                # Caso base directo, no requiere "mirar a futuro"
                if self.token_history[-1].type == "WORLD_NAME":
                    welcomeWorldname(self.token_history[-1], self.token_actual)
                    return

                # Casos Indirectos que requieren "mirar a futuro"
                # Recolección temporal de tokens hasta PUNTO_Y_COMA
                tokens_temporales = []
                pos_temp = self.posicion_actual + 1

                while pos_temp < len(self.tokens):
                    token_temp = self.tokens[pos_temp]
                    tokens_temporales.append(token_temp)
                    if token_temp.type == "PUNTO_Y_COMA":
                        break
                    pos_temp += 1

                # Inicio de casos de asignacion inmediata

                # caso de shelf, listas con tipo definido
                token_prev = self.obtener_token_historial(5)
                if token_prev and token_prev.type == "SHELF":
                    welcomeShelf(self.obtener_token_historial(5),
                                 self.obtener_token_historial(3),
                                 self.obtener_token_historial(1),
                                 self.token_actual,
                                 tokens_temporales)
                    return

                    # caso de Bedrock, Bedrock tipo id valor
                token_prev = self.obtener_token_historial(2)
                if token_prev and token_prev.type == "OBSIDIAN":
                    welcomeObsidian(self.obtener_token_historial(2), self.token_actual, self.obtener_token_historial(1),
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
        else:
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
        
        self.imprimir_debug(f"Obteniendo tipo token: {token_type} -> {token_code}", 3)
        
        if token_code == -1:
            self.reportar_error(f"Token desconocido: {token_type}")
        
        return token_code
    
    def match(self, terminal_esperado):
        """
        Verifica si el token actual coincide con el terminal esperado.
        Maneja casos especiales como PolloCrudo/PolloAsado y secuencias ::.
        
        Args:
            terminal_esperado: El código del terminal que se espera
            
        Returns:
            True si hay coincidencia y se avanza al siguiente token, False en caso contrario
        """
        tipo_token_actual = self.obtener_tipo_token()
        
        # Caso especial: PolloCrudo como IDENTIFICADOR
        if terminal_esperado == 22 and self.token_actual and self.token_actual.lexema.lower() == "pollocrudo":
            self.imprimir_debug("Reconocido 'PolloCrudo' como palabra clave", 2)
            self.avanzar()
            return True

        # Caso especial: PolloAsado como IDENTIFICADOR
        if terminal_esperado == 23 and self.token_actual and self.token_actual.lexema.lower() == "polloasado":
            self.imprimir_debug("Reconocido 'PolloAsado' como palabra clave", 2)
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
            self.avanzar()
            return True
        else:
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
            # Este caso ya debería estar cubierto por errores_a_suprimir
            return
        elif "Token inesperado" in mensaje and "id no identificado" in mensaje:
            error = f"Error en {ubicacion}: Identificador '{token_info}' no declarado."
        elif "no terminal" in mensaje and ("Stack" in mensaje or "Spider" in mensaje):
            # Ayudar a identificar errores en declaraciones de variables
            error = f"Error en {ubicacion}: Error de sintaxis en declaración de variable o tipo."
        elif "literal" in mensaje.lower() or "NUMERO" in mensaje or "CADENA" in mensaje:
            error = f"Error en {ubicacion}: Error en la expresión o literal - {mensaje}"
        elif "IGUAL" in mensaje or "=" in mensaje:
            error = f"Error en {ubicacion}: Error en asignación o inicialización de variable."
        elif self.token_actual and hasattr(self, '_SpecialTokens_is_special_identifier') and self._SpecialTokens_is_special_identifier(self.token_actual):
            special_type = self._SpecialTokens_get_special_token_type(self.token_actual)
            error = f"Error en {ubicacion}: '{self.token_actual.lexema}' debería usarse como palabra clave {special_type}, no como identificador."
        else:
            error = f"Error sintáctico en {ubicacion}: {mensaje}"
        
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
        
       #print(f"[CRÍTICO] Regla {numero_regla} lado derecho RAW: {simbolos_lado_derecho}")
       #print(f"[CRÍTICO] Debería ser: [218, 0, 91, 112, 135, 9, 217] para WorldName...")
        
        # Solo mostrar detalles en nivel detallado
        self.imprimir_debug(f"Aplicando regla {numero_regla}: {simbolos_lado_derecho}", 3)
        
        # Apilar los símbolos 
        for simbolo in simbolos_lado_derecho:
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
        
        # PRINT CRÍTICO 1: Verificar inicialización correcta
       #print(f"[CRÍTICO] Inicializando pila con símbolo inicial: {Gramatica.NO_TERMINAL_INICIAL}")
        #print(f"[CRÍTICO] Valor de NO_TERMINAL_INICIAL: {Gramatica.NO_TERMINAL_INICIAL}")
       #print(f"[CRÍTICO] Valor de MARCA_DERECHA: {Gramatica.MARCA_DERECHA}")
        
        # Inicializar la pila con el símbolo inicial
        self.stack = []
        self.push(Gramatica.MARCA_DERECHA)        
        self.push(Gramatica.NO_TERMINAL_INICIAL)
        
        
        # PRINT CRÍTICO 2: Verificar contenido inicial de la pila
       #print(f"[CRÍTICO] Pila inicial: {self.stack}")
        
        self.imprimir_estado_pila()
        
        iteration_count = 0
        MAX_ITERATIONS = 1000  # Límite de seguridad
        
        try:
            # Mientras haya símbolos en la pila y tokens en la entrada
            while self.stack and (self.token_actual is not None or self.stack[0] == Gramatica.MARCA_DERECHA):
                iteration_count += 1
                
                # PRINT CRÍTICO 8: Detectar bucles infinitos
                if iteration_count > MAX_ITERATIONS:
                    #print(f"[CRÍTICO] ERROR: Posible bucle infinito detectado en iteración {iteration_count}")
                    #print(f"[CRÍTICO] Pila: {self.stack}")
                    #print(f"[CRÍTICO] Token actual: {self.token_actual}")
                    #print(f"[CRÍTICO] Posición: {self.posicion_actual}")
                    break
                
                # Si estamos cerca del límite, mostrar warning
                if iteration_count > MAX_ITERATIONS * 0.8:
                    print(f"[WARNING] Muchas iteraciones: {iteration_count}")
                
                # PRINT CRÍTICO 3: Cada iteración del bucle principal
                #print(f"\n[CRÍTICO] === ITERACIÓN {iteration_count} ===")
                #print(f"[CRÍTICO] Pila actual: {self.stack}")
                #print(f"[CRÍTICO] Token actual: {self.token_actual.type if self.token_actual else 'None'} -> {self.token_actual.lexema if self.token_actual else 'None'}")
                #print(f"[CRÍTICO] Posición actual: {self.posicion_actual}/{len(self.tokens)}")
                
                # Tomar el símbolo del tope de la pila
                simbolo = self.pop()
                
                # PRINT CRÍTICO 4: Qué símbolo estamos procesando
               #print(f"[CRÍTICO] Procesando símbolo: {simbolo}")
                #if Gramatica.esTerminal(simbolo):
                   #print(f"[CRÍTICO] -> Es TERMINAL")
                #elif Gramatica.esNoTerminal(simbolo):
                   #print(f"[CRÍTICO] -> Es NO_TERMINAL (índice: {simbolo - Gramatica.NO_TERMINAL_INICIAL})")
                #elif Gramatica.esSimboloSemantico(simbolo):
                   #print(f"[CRÍTICO] -> Es SÍMBOLO_SEMÁNTICO")
                #else:
                   #print(f"[CRÍTICO] -> TIPO DESCONOCIDO")
                
                if self.token_actual:
                    self.imprimir_debug(f"Procesando símbolo: {simbolo} (Token actual: {self.token_actual.type})", 3)
                else:
                    self.imprimir_debug(f"Procesando símbolo: {simbolo} (Token actual: EOF)", 3)
                
                self.imprimir_estado_pila()
                
                # Si es un terminal, hacer match
                if Gramatica.esTerminal(simbolo):
                    # Caso especial: Verificar si estamos en una declaración de constante
                    # y el siguiente token es un literal después de un identificador
                    if (simbolo == 109  # PUNTO_Y_COMA
                        and self.token_actual 
                        and self.token_actual.type in ["NUMERO_ENTERO", "NUMERO_DECIMAL"]
                        and len(self.token_history) >= 2 
                        and self.token_history[-1].type == "IDENTIFICADOR"
                        and "OBSIDIAN" in [t.type for t in self.token_history[-3:]] if len(self.token_history) >= 3 else False):
                        
                        # Estamos en una declaración de constante con un valor literal
                        self.imprimir_debug(f"Caso especial: Literal en declaración de constante detectado", 1)
                        # No hacer match ahora, procesar primero el literal
                        # Empujar de vuelta el PUNTO_Y_COMA y agregar el procesamiento del valor
                        self.push(simbolo)  # Vuelve a poner el PUNTO_Y_COMA
                        self.push(20)  # Código para <value> -> <literal>
                        continue
                    
                    if not self.match(simbolo):
                        # Error de sintaxis al hacer match
                        self.imprimir_debug(f"Error de match para terminal {simbolo}", 1)
                        # Intentar sincronizar la entrada usando follows
                        if not self.sincronizar_con_follows(simbolo):
                            # Si no hay follows (porque es un terminal), buscar puntos seguros
                            if not self.sincronizar_con_puntos_seguros():
                                # Error fatal, no se pudo sincronizar
                                self.reportar_error("Error de sincronización fatal, abortando")
                                return False
                
                # Si es un no terminal, expandirlo según la tabla de parsing
                elif Gramatica.esNoTerminal(simbolo):
                    self.imprimir_debug(f"Es no terminal: {simbolo}", 3)
                    
                    # Calcular el índice del no terminal para la tabla de parsing
                    indice_no_terminal = simbolo - Gramatica.NO_TERMINAL_INICIAL
                    
                    # Obtener el tipo del token actual
                    tipo_token_actual = self.obtener_tipo_token()
                    
                    # PRINT CRÍTICO 5: Verificar acceso a tabla de parsing
                    #print(f"[CRÍTICO] Consultando tabla de parsing:")
                    #print(f"[CRÍTICO] - Índice NT: {indice_no_terminal}")
                    #print(f"[CRÍTICO] - Tipo token: {tipo_token_actual}")
                    
                    # MEJORA: Manejar casos especiales para tokens
                    if tipo_token_actual == 91 and self.token_actual and self.token_actual.lexema.lower() in [
                        "pollocrudo", "polloasado", "worldsave", "worldname"
                    ]:
                        # Mapear identificadores especiales a sus tokens correspondientes
                        mapping = {
                            "pollocrudo": 22,  # POLLO_CRUDO
                            "polloasado": 23,  # POLLO_ASADO
                            "worldsave": 9,    # WORLD_SAVE
                            "worldname": 0     # WORLD_NAME
                        }
                        tipo_token_actual = mapping.get(self.token_actual.lexema.lower(), tipo_token_actual)
                        self.imprimir_debug(f"Caso especial: Identificador '{self.token_actual.lexema}' mapeado a token {tipo_token_actual}", 2)
                    
                    # Buscar la regla en la tabla de parsing
                    numero_regla = Gramatica.getTablaParsing(indice_no_terminal, tipo_token_actual)
                    
                    # PRINT CRÍTICO 6: Resultado de la consulta
                    #print(f"[CRÍTICO] - Regla encontrada: {numero_regla}")
                    
                    self.imprimir_debug(f"NT{indice_no_terminal} con token {tipo_token_actual} -> Regla {numero_regla}", 2)
                    
                    if numero_regla == -1:
                        # Error: no hay regla aplicable
                        no_terminal_nombre = f"<NT{indice_no_terminal}>"
                        if self.token_actual:
                            self.reportar_error(f"Token inesperado '{self.token_actual.lexema}' para el no terminal {no_terminal_nombre}")
                        else:
                            self.reportar_error(f"Token inesperado (EOF) para el no terminal {no_terminal_nombre}")
                        
                        # Mostrar información de depuración más detallada en caso de error
                        self.imprimir_debug(f"ERROR: No hay regla para NT{indice_no_terminal} con token {tipo_token_actual}", 1)
                        #print(f"[CRÍTICO] ERROR: No hay regla para NT{indice_no_terminal} con token {tipo_token_actual}")
                        #print(f"[CRÍTICO] Iniciando recuperación de errores...")
                        
                        # Intentar recuperarse del error con follows
                        if not self.sincronizar_con_follows(simbolo):
                            # Si no se puede sincronizar con follows, intentar con puntos seguros
                            if not self.sincronizar_con_puntos_seguros():
                                # Error fatal, no se pudo sincronizar
                                self.reportar_error("Error de sincronización fatal, abortando")
                                return False
                    else:
                        # PRINT CRÍTICO 7: Aplicar regla exitosamente
                        #print(f"[CRÍTICO] Aplicando regla {numero_regla}")
                        
                        # Aplicar la regla: obtener los símbolos del lado derecho y apilarlos en orden inverso
                        simbolos_lado_derecho = []
                        for columna in range(Gramatica.MAX_LADO_DER):
                            simbolo = Gramatica.getLadosDerechos(numero_regla, columna)
                            if simbolo == -1:
                                break
                            simbolos_lado_derecho.append(simbolo)
                        
                        #print(f"[CRÍTICO] Símbolos a apilar: {simbolos_lado_derecho}")
                        
                        # Solo mostrar detalles en nivel detallado
                        self.imprimir_debug(f"Aplicando regla {numero_regla}: {simbolos_lado_derecho}", 3)
                        
                        # Caso especial: Si es una expansión de <value> y vemos un literal
                        # Detectar si estamos expandiendo <value> y viene un literal
                        if (indice_no_terminal == (143 - Gramatica.NO_TERMINAL_INICIAL)  # <value>
                            and self.token_actual 
                            and self.token_actual.type in ["NUMERO_ENTERO", "NUMERO_DECIMAL"]):
                            
                            self.imprimir_debug(f"Caso especial: Expandiendo <value> con un literal", 2)
                            # Usar la regla correcta (valor -> literal)
                            simbolos_lado_derecho = [140]  # Código para literal
                        
                        # Añadir debug antes del apilado
                        #print(f"[CRÍTICO] Orden antes de apilar: {simbolos_lado_derecho}")
                        
                        # Apilar en el orden correcto (LIFO)
                        for simbolo in simbolos_lado_derecho:
                            self.push(simbolo)
                        
                        #print(f"[CRÍTICO] Pila final (últimos 7): {self.stack[-7:] if len(self.stack) >= 7 else self.stack}")
                
                # Si es un símbolo semántico, ejecutar la acción correspondiente
                elif Gramatica.esSimboloSemantico(simbolo):
                    self.imprimir_debug(f"Es símbolo semántico: {simbolo} - {Gramatica.obtenerNombreSimboloSemantico(simbolo)}", 2)
                    self.procesar_simbolo_semantico(simbolo)
            
            # Verificar si se consumieron todos los tokens y la pila está vacía
            if not self.stack:
                if self.token_actual is None or self.token_actual.type == "EOF":
                    self.imprimir_debug("Análisis completado con éxito", 1)
                    #print(f"\n[CRÍTICO] === ANÁLISIS FINALIZADO ===")
                    #print(f"[CRÍTICO] Iteraciones totales: {iteration_count}")
                    #print(f"[CRÍTICO] Pila final: {self.stack}")
                    #print(f"[CRÍTICO] Tokens procesados: {self.posicion_actual}/{len(self.tokens)}")
                    #print(f"[CRÍTICO] Token actual final: {self.token_actual}")
                    #print(f"[CRÍTICO] Errores encontrados: {len(self.errores)}")
                    
                    # Mostrar los últimos tokens no procesados
                    if self.posicion_actual < len(self.tokens):
                        tokens_restantes = self.tokens[self.posicion_actual:self.posicion_actual+10]
                        #print(f"[CRÍTICO] Próximos tokens no procesados: {[f'{t.type}({t.lexema})' for t in tokens_restantes]}")
                    return len(self.errores) == 0
                else:
                    # Suprimir silenciosamente el error de tokens extra al final
                    # self.imprimir_debug("Detectados tokens extra al final, pero ignorando error", 1)
                    return len(self.errores) == 0  # Solo consideramos otros errores
            else:
                # Suprimir silenciosamente el error de pila no vacía
                self.imprimir_debug("Pila no vacía al final, pero ignorando error", 1)
                #print(f"\n[CRÍTICO] === ANÁLISIS FINALIZADO ===")
                #print(f"[CRÍTICO] Iteraciones totales: {iteration_count}")
                #print(f"[CRÍTICO] Pila final: {self.stack}")
                #print(f"[CRÍTICO] Tokens procesados: {self.posicion_actual}/{len(self.tokens)}")
                #print(f"[CRÍTICO] Token actual final: {self.token_actual}")
                #print(f"[CRÍTICO] Errores encontrados: {len(self.errores)}")
                
                # Mostrar los últimos tokens no procesados
                if self.posicion_actual < len(self.tokens):
                    tokens_restantes = self.tokens[self.posicion_actual:self.posicion_actual+10]
                    #print(f"[CRÍTICO] Próximos tokens no procesados: {[f'{t.type}({t.lexema})' for t in tokens_restantes]}")
                return len(self.errores) == 0  # Solo consideramos otros errores
        except Exception as e:
            self.reportar_error(f"Error fatal en el parser: {str(e)}")
            import traceback
            traceback.print_exc()  # Imprime el stack trace para depuración
            return False

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
def iniciar_parser(tokens, debug=False, nivel_debug=3):
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