"""
Analizador Léxico (Scanner) para EnderLang
Autores: Samir Cabrera, Luis Urbina
Fecha de entrega: 10/04/2025

Este archivo implementa la funcionalidad principal del analizador léxico (scanner).
"""

from token import Token

class Scanner:
    """
    Implementación del analizador léxico (scanner) para EnderLang.
    
    El scanner lee un archivo fuente y lo convierte en una secuencia de tokens
    utilizando un autómata finito.
    """
    
    def __init__(self):
        """
        Constructor de la clase Scanner
        """
        # Configuración del buffer
        self.buffer_size = 1024      # Tamaño del buffer (podemos ajustarlo a 128 para pruebas)
        self.buffer = ""             # Buffer actual
        self.buffer_pos = 0          # Posición actual en el buffer
        
        # Información de posición
        self.linea = 1               # Línea actual
        self.columna = 1             # Columna actual
        
        # Estado del scanner
        self.archivo = None          # Archivo de entrada
        self.fin_archivo = False     # Indicador de fin de archivo
        self.token_actual = None     # Último token leído
        
        # Tablas de tokens (estas serían actualizadas con la definición completa del lenguaje)
        self.palabras_reservadas = set()  # Conjunto de palabras reservadas
        self.operadores = set()           # Conjunto de operadores
        self.simbolos = set()             # Conjunto de símbolos especiales
    
    def inicializar_scanner(self, nombre_archivo):
        """
        Inicializa el scanner con un archivo de entrada
        
        Parámetros:
            nombre_archivo (str): Ruta al archivo a analizar
            
        Retorna:
            bool: True si se pudo abrir el archivo, False en caso contrario
        """
        try:
            self.archivo = open(nombre_archivo, 'r', encoding='utf-8')
            self.buffer = self.archivo.read(self.buffer_size)
            self.buffer_pos = 0
            self.linea = 1
            self.columna = 1
            self.fin_archivo = False
            return True
        except Exception as e:
            print(f"Error al abrir el archivo: {e}")
            return False
    
    def finalizar_scanner(self):
        """
        Cierra el scanner y libera recursos
        """
        if self.archivo:
            self.archivo.close()
            self.archivo = None
    
    def dame_caracter(self):
        """
        Lee el siguiente carácter del buffer de entrada
        
        Retorna:
            str o None: El carácter leído o None si se llegó al final del archivo
        """
        # Si llegamos al final del buffer actual, intentamos leer más datos
        if self.buffer_pos >= len(self.buffer):
            if self.fin_archivo:
                return None  # Ya no hay más caracteres en el archivo
            
            # Cargar más datos en el buffer
            nuevo_buffer = self.archivo.read(self.buffer_size)
            if not nuevo_buffer:  # Si no hay más datos para leer
                self.fin_archivo = True
                return None
            
            self.buffer = nuevo_buffer
            self.buffer_pos = 0
        
        # Leer el carácter actual
        caracter = self.buffer[self.buffer_pos]
        self.buffer_pos += 1
        
        # Actualizar posición (línea y columna)
        if caracter == '\n':
            self.linea += 1
            self.columna = 1
        else:
            self.columna += 1
        
        return caracter
    
    def retroceder(self):
        """
        Retrocede un carácter en el buffer de entrada
        Actualiza las posiciones de línea y columna
        """
        if self.buffer_pos > 0:
            self.buffer_pos -= 1
            
            # Actualizar posición
            caracter = self.buffer[self.buffer_pos]
            if caracter == '\n':
                self.linea -= 1
                # Esto es una aproximación, idealmente deberíamos encontrar la longitud exacta
                # de la línea anterior, pero es complicado sin almacenar todo el contenido
                self.columna = 1  # Valor aproximado
            else:
                self.columna -= 1
    
    def dame_token(self):
        """
        Obtiene el siguiente token del archivo de entrada
        
        Retorna:
            Token: El siguiente token en el archivo
        """
        # Omitir espacios en blanco
        caracter = self.dame_caracter()
        while caracter is not None and caracter.isspace():
            caracter = self.dame_caracter()
        
        # Fin de archivo
        if caracter is None:
            return Token(Token.TK_EOF, "", self.linea, self.columna)
        
        # Registrar posición inicial del token
        linea_token = self.linea
        columna_token = self.columna - 1  # Ajuste por el incremento previo
        
        # --- Reconocimiento de tokens ---
        # Nota: Este es un esquema básico que se completará con la definición específica del lenguaje
        
        # 1. Identificadores y palabras reservadas
        if caracter.isalpha() or caracter == '_':
            return self._procesar_identificador(caracter, linea_token, columna_token)
        
        # 2. Números (enteros y flotantes)
        elif caracter.isdigit():
            return self._procesar_numero(caracter, linea_token, columna_token)
        
        # 3. Caracteres
        elif caracter == "'":
            return self._procesar_caracter(linea_token, columna_token)
        
        # 4. Strings
        elif caracter == '"':
            return self._procesar_string(linea_token, columna_token)
        
        # 5. Comentarios y operador de división
        elif caracter == '/':
            siguiente = self.dame_caracter()
            if siguiente == '/':
                return self._procesar_comentario_linea(linea_token, columna_token)
            elif siguiente == '*':
                return self._procesar_comentario_bloque(linea_token, columna_token)
            else:
                # Era un operador de división
                if siguiente is not None:
                    self.retroceder()
                return Token(Token.TK_OPERADOR, '/', linea_token, columna_token)
        
        # 6. Verificar si es un operador o símbolo
        # Esto se completará con la definición del lenguaje
        
        # Si llegamos aquí, es un carácter no reconocido (error)
        return Token(Token.TK_ERROR, caracter, linea_token, columna_token)
    
    def tomar_token(self):
        """
        Obtiene el siguiente token y lo almacena como token actual
        
        Retorna:
            Token: El token leído
        """
        self.token_actual = self.dame_token()
        return self.token_actual
    
    # --- Métodos auxiliares para procesar tipos específicos de tokens ---
    
    def _procesar_identificador(self, primer_caracter, linea, columna):
        """
        Procesa un identificador o palabra reservada
        """
        lexema = primer_caracter
        caracter = self.dame_caracter()
        
        # Acumular caracteres válidos para identificador
        while caracter is not None and (caracter.isalnum() or caracter == '_'):
            lexema += caracter
            caracter = self.dame_caracter()
        
        # Retroceder un carácter, ya que leímos uno de más
        if caracter is not None:
            self.retroceder()
        
        # Verificar si es una palabra reservada (se completará con la definición del lenguaje)
        if lexema in self.palabras_reservadas:
            return Token(Token.TK_PALABRA_RESERVADA, lexema, linea, columna)
        else:
            return Token(Token.TK_IDENTIFICADOR, lexema, linea, columna)
    
    def _procesar_numero(self, primer_caracter, linea, columna):
        """
        Procesa un número (entero o flotante)
        """
        lexema = primer_caracter
        es_flotante = False
        caracter = self.dame_caracter()
        
        # Leer parte entera
        while caracter is not None and caracter.isdigit():
            lexema += caracter
            caracter = self.dame_caracter()
        
        # Verificar si es un flotante
        if caracter == '.':
            es_flotante = True
            lexema += caracter
            caracter = self.dame_caracter()
            
            # Leer parte decimal
            while caracter is not None and caracter.isdigit():
                lexema += caracter
                caracter = self.dame_caracter()
        
        # Retroceder un carácter
        if caracter is not None:
            self.retroceder()
        
        # Crear token según el tipo de número
        if es_flotante:
            return Token(Token.TK_FLOTANTE, lexema, linea, columna)
        else:
            return Token(Token.TK_ENTERO, lexema, linea, columna)
    
    def _procesar_caracter(self, linea, columna):
        """
        Procesa un literal de carácter
        """
        lexema = "'"  # Comilla inicial
        caracter = self.dame_caracter()
        
        if caracter is None:
            return Token(Token.TK_ERROR, lexema, linea, columna)
        
        # Manejar secuencia de escape
        if caracter == '\\':
            lexema += caracter
            caracter = self.dame_caracter()
            if caracter is None:
                return Token(Token.TK_ERROR, lexema, linea, columna)
            lexema += caracter
        else:
            lexema += caracter
        
        # Leer comilla final
        caracter = self.dame_caracter()
        if caracter is None or caracter != "'":
            return Token(Token.TK_ERROR, lexema, linea, columna)
        
        lexema += caracter
        return Token(Token.TK_CARACTER, lexema, linea, columna)
    
    def _procesar_string(self, linea, columna):
        """
        Procesa un literal de string
        """
        lexema = '"'  # Comilla inicial
        caracter = self.dame_caracter()
        
        # Leer hasta encontrar la comilla final o fin de archivo
        while caracter is not None and caracter != '"':
            # Manejar secuencias de escape
            if caracter == '\\':
                lexema += caracter
                caracter = self.dame_caracter()
                if caracter is None:
                    break
                lexema += caracter
            else:
                lexema += caracter
            
            caracter = self.dame_caracter()
        
        # Verificar si terminó correctamente
        if caracter is None:
            return Token(Token.TK_ERROR, lexema, linea, columna)
        
        lexema += caracter  # Añadir comilla final
        return Token(Token.TK_STRING, lexema, linea, columna)
    
    def _procesar_comentario_linea(self, linea, columna):
        """
        Procesa un comentario de línea (// ...)
        """
        lexema = "//"
        caracter = self.dame_caracter()
        
        # Leer hasta el fin de línea o fin de archivo
        while caracter is not None and caracter != '\n':
            lexema += caracter
            caracter = self.dame_caracter()
        
        return Token(Token.TK_COMENTARIO, lexema, linea, columna)
    
    def _procesar_comentario_bloque(self, linea, columna):
        """
        Procesa un comentario de bloque (/* ... */)
        """
        lexema = "/*"
        caracter_previo = None
        caracter = self.dame_caracter()
        
        # Leer hasta encontrar */ o fin de archivo
        while caracter is not None and not (caracter_previo == '*' and caracter == '/'):
            lexema += caracter
            caracter_previo = caracter
            caracter = self.dame_caracter()
        
        # Verificar si terminó correctamente
        if caracter is None:
            return Token(Token.TK_ERROR, lexema, linea, columna)
        
        lexema += caracter  # Añadir '/' final
        return Token(Token.TK_COMENTARIO, lexema, linea, columna)