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
        
        # Inicializar con el primer token (si existe)
        if self.tokens:
            self.token_actual = self.tokens[0]
        
        if self.debug:
            print("\n[DEBUG] Parser inicializado")
            print(f"[DEBUG] Tokens recibidos ({len(self.tokens)}):")
            for i, token in enumerate(self.tokens):
                print(f"  {i}: {token.type} ('{token.lexema}')")
    
    def avanzar(self):
        """
        Avanza al siguiente token en la secuencia, ignorando comentarios
        """
        self.posicion_actual += 1
        if self.posicion_actual < len(self.tokens):
            self.token_actual = self.tokens[self.posicion_actual]
            
            if self.debug:
                print(f"[DEBUG] Avanzando a token {self.posicion_actual}: {self.token_actual.type} ('{self.token_actual.lexema}')")
        else:
            # Crear un token ficticio para el fin de archivo
            self.token_actual = None
            if self.debug:
                print("[DEBUG] Avanzando a EOF")
    
    def obtener_tipo_token(self):
        """
        Obtiene el tipo del token actual y lo mapea al formato
        esperado por la gramática.
        
        Returns:
            El código numérico del terminal correspondiente al token actual
        """
        if self.token_actual is None:
            if self.debug:
                print("[DEBUG] Token actual: EOF")
            return Gramatica.MARCA_DERECHA  # Token de fin de archivo
        
        token_type = self.token_actual.type
        token_code = TokenMap.get_token_code(token_type)
        
        if self.debug:
            print(f"[DEBUG] Obteniendo tipo token: {token_type} -> {token_code}")
        
        if token_code == -1:
            self.reportar_error(f"Token desconocido: {token_type}")
        
        return token_code
    
    def match(self, terminal_esperado):
        """
        Verifica si el token actual coincide con el terminal esperado.
        Si coincide, avanza al siguiente token, si no, reporta un error.
        
        Args:
            terminal_esperado: Código del terminal que se espera encontrar
            
        Returns:
            True si hubo coincidencia, False en caso contrario
        """
        tipo_token_actual = self.obtener_tipo_token()
        
        try:
            nombre_esperado = Gramatica.getNombresTerminales(terminal_esperado)
        except:
            nombre_esperado = f"terminal#{terminal_esperado}"
        
        if self.debug:
            print(f"[DEBUG] Match: esperando {nombre_esperado} ({terminal_esperado}), encontrado {tipo_token_actual}")
        
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
        Reporta un error sintáctico
        
        Args:
            mensaje: Descripción del error
        """
        if self.token_actual:
            error = f"Error sintáctico en línea {self.token_actual.linea}, columna {self.token_actual.columna}: {mensaje}"
        else:
            error = f"Error sintáctico al final del archivo: {mensaje}"
        
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
        if self.debug:
            print(f"[DEBUG] Sincronizando para no terminal {simbolo_no_terminal}")
        
        try:
            # Ajustar el índice del no terminal para la tabla de follows
            indice_no_terminal = simbolo_no_terminal - Gramatica.NO_TERMINAL_INICIAL
            
            if indice_no_terminal < 0 or indice_no_terminal >= Gramatica.NUM_NO_TERMINALES:
                if self.debug:
                    print(f"[DEBUG] Índice de no terminal fuera de rango: {indice_no_terminal}")
                return False
            
            # Buscar en el conjunto Follow del no terminal
            for columna in range(Gramatica.MAX_FOLLOWS):
                try:
                    terminal_follow = Gramatica.getTablaFollows(indice_no_terminal, columna)
                    if terminal_follow == -1:  # Fin de la lista de Follow
                        break
                    
                    if self.debug:
                        print(f"[DEBUG] Buscando en Follow: {Gramatica.getNombresTerminales(terminal_follow)}")
                    
                    # Avanzar hasta encontrar un token en el conjunto Follow
                    tipo_token_actual = self.obtener_tipo_token()
                    while (tipo_token_actual != terminal_follow and 
                        tipo_token_actual != Gramatica.MARCA_DERECHA):
                        if self.debug:
                            print(f"[DEBUG] Saltando token {self.token_actual.type if self.token_actual else 'EOF'}")
                        self.avanzar()
                        tipo_token_actual = self.obtener_tipo_token()
                    
                    if tipo_token_actual == terminal_follow:
                        if self.debug:
                            print("[DEBUG] Sincronización exitosa")
                        return True
                except IndexError:
                    if self.debug:
                        print(f"[DEBUG] Error al acceder a Follows para columna {columna}")
                    break
            
            if self.debug:
                print("[DEBUG] No se pudo sincronizar")
            return False
        except Exception as e:
            if self.debug:
                print(f"[DEBUG] Excepción en sincronizar: {str(e)}")
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
        if self.debug:
            print(f"[DEBUG] Procesando no terminal: {simbolo_no_terminal}")
        
        # Calcular el índice del no terminal para la tabla de parsing
        indice_no_terminal = simbolo_no_terminal - Gramatica.NO_TERMINAL_INICIAL
        
        # Obtener el tipo del token actual
        tipo_token_actual = self.obtener_tipo_token()
        
        if self.debug:
            print(f"[DEBUG] Token actual para no terminal: {tipo_token_actual}")
        
        # Buscar la regla en la tabla de parsing
        numero_regla = Gramatica.getTablaParsing(indice_no_terminal, tipo_token_actual)
        
        if self.debug:
            print(f"[DEBUG] Regla encontrada: {numero_regla}")
        
        if numero_regla == -1:
            # Error: no hay regla aplicable
            nombre_no_terminal = f"<{indice_no_terminal}>"  # Representación básica
            if self.token_actual:
                self.reportar_error(f"Token inesperado '{self.token_actual.lexema}' para el no terminal {nombre_no_terminal}")
            else:
                self.reportar_error(f"Token inesperado (EOF) para el no terminal {nombre_no_terminal}")
            
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
        
        if self.debug:
            print(f"[DEBUG] Lado derecho de la regla {numero_regla}: {simbolos_lado_derecho}")
        
        # Apilar los símbolos en orden inverso
        for simbolo in reversed(simbolos_lado_derecho):
            self.stack.append(simbolo)
        
        if self.debug:
            print(f"[DEBUG] Pila después de apilar: {self.stack}")
        
        return True
    
    def parse(self):
        """
        Inicia el proceso de análisis sintáctico
        
        Returns:
            True si el análisis fue exitoso, False en caso contrario
        """
        if self.debug:
            print("\n[DEBUG] Iniciando análisis sintáctico")
        
        # Inicializar la pila con el símbolo de fin de archivo y el no terminal inicial
        self.stack = [Gramatica.MARCA_DERECHA, Gramatica.NO_TERMINAL_INICIAL]
        
        if self.debug:
            print(f"[DEBUG] Pila inicial: {self.stack}")
        
        try:
            # Mientras haya símbolos en la pila
            while self.stack:
                # Tomar el símbolo del tope de la pila
                simbolo = self.stack.pop()
                
                if self.debug:
                    print(f"\n[DEBUG] Procesando símbolo: {simbolo}")
                    print(f"[DEBUG] Pila actual: {self.stack}")
                    print(f"[DEBUG] Token actual: {self.token_actual.type if self.token_actual else 'EOF'}")
                
                # Si es un terminal, hacer match
                if Gramatica.esTerminal(simbolo):
                    if self.debug:
                        print("[DEBUG] Es terminal")
                    if not self.match(simbolo):
                        # Error de sintaxis al hacer match
                        # Intentar sincronizarse con algún símbolo de seguimiento
                        if not self.sincronizar(simbolo):
                            # No se pudo sincronizar, abortar
                            return False
                
                # Si es un no terminal, expandirlo según la tabla de parsing
                elif Gramatica.esNoTerminal(simbolo):
                    if self.debug:
                        print("[DEBUG] Es no terminal")
                    if not self.procesar_no_terminal(simbolo):
                        # Error al procesar el no terminal
                        return False
                
                # Si es un símbolo semántico, ejecutar la acción correspondiente
                elif Gramatica.esSimboloSemantico(simbolo):
                    if self.debug:
                        print("[DEBUG] Es símbolo semántico")
                    # En este caso no hay símbolos semánticos según la gramática
                    pass
            
            # Si hemos llegado aquí y no hay más tokens, el análisis fue exitoso
            if self.posicion_actual >= len(self.tokens):
                if self.debug:
                    print("[DEBUG] Análisis completado con éxito")
                return True
            else:
                self.reportar_error("Hay tokens de más al final del archivo")
                return False
        except Exception as e:
            self.reportar_error(f"Error fatal en el parser: {str(e)}")
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
def iniciar_parser(tokens, debug=False):
    """
    Función para ser llamada desde el main después del scanner
    
    Args:
        tokens: Lista de tokens generada por el scanner
        debug: Si es True, muestra información detallada del parsing
        
    Returns:
        True si el análisis fue exitoso, False en caso contrario
    """
    print("\n#################################################################")
    print("##                    INICIO PARSER                            ##")
    print("#################################################################")
    
    return parser(tokens, debug=debug)