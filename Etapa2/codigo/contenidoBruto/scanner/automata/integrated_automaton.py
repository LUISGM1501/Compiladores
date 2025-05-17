"""
Autómata integrado para el scanner MC
"""

class AutomatonResult:
    """Resultado del procesamiento del autómata"""
    def __init__(self, exito, tipo=None, lexema=None, valor=None, 
                 final_pos=None, final_linea=None, final_columna=None):
        self.exito = exito
        self.tipo = tipo
        self.lexema = lexema
        self.valor = valor
        self.final_pos = final_pos
        self.final_linea = final_linea
        self.final_columna = final_columna

class IntegratedAutomaton:
    """Autómata que integra todos los patrones léxicos"""
    
    def __init__(self):
        # Inicialización básica del autómata
        pass
    
    def procesar(self, contenido, posicion, linea, columna):
        """Procesa el contenido desde la posición actual"""
        if posicion >= len(contenido):
            return AutomatonResult(False)
        
        char_inicial = contenido[posicion]
        
        # Determinar qué tipo de token podría empezar aquí
        if char_inicial == '$':
            return self._procesar_comentario(contenido, posicion, linea, columna)
        elif char_inicial == '"' or char_inicial == "'":
            return self._procesar_string(contenido, posicion, linea, columna)
        elif char_inicial.isdigit():
            return self._procesar_numero(contenido, posicion, linea, columna)
        elif char_inicial.isalpha() or char_inicial == '_':
            return self._procesar_identificador(contenido, posicion, linea, columna)
        elif char_inicial in '{':
            return AutomatonResult(
                True,
                "POLLO_CRUDO",
                char_inicial,
                None,
                posicion + 1,
                linea,
                columna + 1
            )
        elif char_inicial in '}':
            return AutomatonResult(
                True,
                "POLLO_ASADO",
                char_inicial,
                None,
                posicion + 1,
                linea,
                columna + 1
            )
        elif char_inicial in '+-*/%<>=!&|^~:,;()[].#@':
            return self._procesar_operador(contenido, posicion, linea, columna)
        else:
            # Caracter no reconocido, lo trataremos como error
            return AutomatonResult(
                True,
                "ERROR",
                char_inicial,
                None,
                posicion + 1,
                linea,
                columna + 1
            )
    
    def _procesar_comentario(self, contenido, pos, linea, columna):
        """Procesa comentarios ($$ o $* ... *$)"""
        if pos + 1 < len(contenido) and contenido[pos + 1] == '$':
            # Comentario de línea
            final_pos = contenido.find('\n', pos + 2)
            if final_pos == -1:
                final_pos = len(contenido)
            lexema = contenido[pos:final_pos]
            
            # Contar saltos de línea en el comentario
            num_saltos = lexema.count('\n')
            if num_saltos > 0:
                final_linea = linea + num_saltos
                # Calcula la columna final correctamente
                ultima_linea = lexema.split('\n')[-1]
                final_columna = len(ultima_linea) + 1
            else:
                final_linea = linea
                final_columna = columna + len(lexema)
            
            return AutomatonResult(
                True,
                "COMENTARIO",
                lexema,
                None,
                final_pos,
                final_linea,
                final_columna
            )
        
        elif pos + 1 < len(contenido) and contenido[pos + 1] == '*':
            # Comentario de bloque
            final_pos = contenido.find('*$', pos + 2)
            if final_pos == -1:
                # Comentario no cerrado, lo tratamos como error
                final_pos = len(contenido)
                lexema = contenido[pos:final_pos]
                return AutomatonResult(
                    True,
                    "ERROR",
                    lexema,
                    None,
                    final_pos,
                    linea + lexema.count('\n'),
                    columna + len(lexema)
                )
            
            lexema = contenido[pos:final_pos + 2]
            lineas_extras = lexema.count('\n')
            
            if lineas_extras > 0:
                final_linea = linea + lineas_extras
                # Encuentra la posición de la columna en la última línea
                ultima_linea = lexema.split('\n')[-1]
                final_columna = len(ultima_linea) + 1
            else:
                final_linea = linea
                final_columna = columna + len(lexema)
            
            return AutomatonResult(
                True,
                "COMENTARIO",
                lexema,
                None,
                final_pos + 2,
                final_linea,
                final_columna
            )
        else:
            # $ sin seguir de $ o *, lo tratamos como error
            return AutomatonResult(
                True,
                "ERROR",
                contenido[pos],
                None,
                pos + 1,
                linea,
                columna + 1
            )
    
    def _procesar_string(self, contenido, pos, linea, columna):
        """Procesa strings y caracteres"""
        comilla = contenido[pos]
        escape = False
        lexema = comilla
        current_pos = pos + 1
        current_linea = linea
        current_col = columna + 1
        
        while current_pos < len(contenido):
            c = contenido[current_pos]
            lexema += c
            
            if c == '\n':
                current_linea += 1
                current_col = 1
            else:
                current_col += 1
            
            if not escape and c == comilla:
                # Fin del string/caracter
                return AutomatonResult(
                    True,
                    "CADENA" if comilla == '"' else "CARACTER",
                    lexema,
                    lexema[1:-1],  # Valor sin comillas
                    current_pos + 1,
                    current_linea,
                    current_col
                )
            elif not escape and c == '\\':
                escape = True
            else:
                escape = False
            
            current_pos += 1
        
        # String no cerrado, lo tratamos como error
        return AutomatonResult(
            True,
            "ERROR",
            lexema,
            None,
            len(contenido),
            current_linea,
            current_col
        )
    
    def _procesar_numero(self, contenido, pos, linea, columna):
        """Procesa números enteros y decimales"""
        lexema = ""
        tiene_punto = False
        current_pos = pos
        current_col = columna
        
        while current_pos < len(contenido):
            c = contenido[current_pos]
            
            if c.isdigit():
                lexema += c
                current_col += 1
                current_pos += 1
            elif c == '.' and not tiene_punto and current_pos + 1 < len(contenido) and contenido[current_pos + 1].isdigit():
                lexema += c
                tiene_punto = True
                current_col += 1
                current_pos += 1
            else:
                break
        
        if not lexema:
            return AutomatonResult(
                True,
                "ERROR",
                contenido[pos],
                None,
                pos + 1,
                linea,
                columna + 1
            )
        
        # Determinar tipo y valor
        tipo = "NUMERO_DECIMAL" if tiene_punto else "NUMERO_ENTERO"
        try:
            valor = float(lexema) if tiene_punto else int(lexema)
        except ValueError:
            # Nunca debería llegar aquí debido a nuestra lógica
            return AutomatonResult(
                True,
                "ERROR",
                lexema,
                None,
                current_pos,
                linea,
                current_col
            )
        
        return AutomatonResult(
            True,
            tipo,
            lexema,
            valor,
            current_pos,
            linea,
            current_col
        )
    
    def _procesar_identificador(self, contenido, pos, linea, columna):
        """Procesa identificadores y detecta palabras reservadas"""
        from ..tokens import PALABRAS_RESERVADAS
        
        lexema = ""
        current_pos = pos
        current_col = columna
        
        # Extraer el lexema completo
        while current_pos < len(contenido):
            c = contenido[current_pos]
            if c.isalnum() or c == '_':
                lexema += c
                current_pos += 1
                current_col += 1
            else:
                break
        
        if not lexema:
            return AutomatonResult(
                True,
                "ERROR",
                contenido[pos],
                None,
                pos + 1,
                linea,
                columna + 1
            )
        
        # Verificar si es palabra reservada
        if lexema.lower() in PALABRAS_RESERVADAS:
            tipo = PALABRAS_RESERVADAS[lexema.lower()]
            return AutomatonResult(
                True,
                tipo,
                lexema,
                None,
                current_pos,
                linea,
                current_col
            )
        else:
            return AutomatonResult(
                True,
                "IDENTIFICADOR",
                lexema,
                None,
                current_pos,
                linea,
                current_col
            )
    
    def _procesar_operador(self, contenido, pos, linea, columna):
        """Procesa operadores y símbolos"""
        # Mapeo de operadores simples
        operadores_simples = {
            '+': 'SUMA',
            '-': 'RESTA',
            '*': 'MULTIPLICACION',
            '//': 'DIVISION',
            '%': 'MODULO',
            '(': 'PARENTESIS_ABRE',
            ')': 'PARENTESIS_CIERRA',
            '[': 'CORCHETE_ABRE',
            ']': 'CORCHETE_CIERRA',
            ';': 'PUNTO_Y_COMA',
            ',': 'COMA',
            '.': 'PUNTO',
            ':': 'DOS_PUNTOS',
            '#': 'HASH',
            '@': 'ARROBA',
            '<': 'MENOR_QUE',
            '>': 'MAYOR_QUE',
            '=': 'IGUAL', 
            '/': 'BARRA',
            ':+': 'SUMA_FLOTANTE',
            ':-': 'RESTA_FLOTANTE',
            ':*': 'MULTIPLICACION_FLOTANTE',
            '://': 'DIVISION_FLOTANTE',
            ':%': 'MODULO_FLOTANTE',
        }
        
        # Mapeo de operadores compuestos
        operadores_compuestos = {
            '==': 'DOBLE_IGUAL',
            '!=': 'DIFERENTE',
            '>=': 'MAYOR_IGUAL',
            '<=': 'MENOR_IGUAL',
            '->': 'FLECHA',
            '++': 'INCREMENTO',
            '--': 'DECREMENTO'
        }
        
        # Verificar operadores compuestos primero
        if pos + 1 < len(contenido):
            if contenido[pos] == ':' and contenido[pos + 1] == ':':
                # Devolver solo el primer ':', el siguiente será escaneado en el próximo llamado
                return AutomatonResult(
                    True,
                    "DOS_PUNTOS",
                    ":",
                    None,
                    pos + 1,
                    linea,
                    columna + 1
                )
            dos_caracteres = contenido[pos] + contenido[pos + 1]
            if dos_caracteres in operadores_compuestos:
                return AutomatonResult(
                    True,
                    operadores_compuestos[dos_caracteres],
                    dos_caracteres,
                    None,
                    pos + 2,
                    linea,
                    columna + 2
                )
        
        # Verificar operadores simples
        if contenido[pos] in operadores_simples:
            return AutomatonResult(
                True,
                operadores_simples[contenido[pos]],
                contenido[pos],
                None,
                pos + 1,
                linea,
                columna + 1
            )
        
        # Si no es un operador reconocido
        return AutomatonResult(
            True,
            "ERROR",
            contenido[pos],
            None,
            pos + 1,
            linea,
            columna + 1
        )