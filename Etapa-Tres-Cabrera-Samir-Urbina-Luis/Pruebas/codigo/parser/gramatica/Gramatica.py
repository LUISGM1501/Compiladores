"""
Compilador Notch Engine

Estudiantes: Cabrera Samir y Urbina Luis

Archivo: Gramatica.py

Breve Descripcion: Archivo principal de gramatica generado por GikGram, traducido
por los estudiantes.
"""

from .GTablaParsing import GTablaParsing
from .GLadosDerechos import GLadosDerechos
from .GNombresTerminales import GNombresTerminales


class Gramatica:
    """
    Esta clase contiene:
    - Constantes necesarias para el driver de parsing
    - Constantes con las rutinas semánticas
    - Y los métodos necesarios para el driver de parsing
    """
    
    # Constante que contiene el código de familia del terminal de fin de archivo
    MARCA_DERECHA = 133

    # Constante que contiene el número del no-terminal inicial
    NO_TERMINAL_INICIAL = 134

    # Constante que contiene el número máximo de columnas que tiene los lados derechos
    MAX_LADO_DER = 9

    # Constante que contiene el número máximo de follows
    MAX_FOLLOWS = 48

    # 🔧 CORRECCIÓN: Definir correctamente los rangos de símbolos semánticos
    # Basado en los símbolos que aparecen en los logs (220, 222, 224, etc.)
    SIMBOLO_SEMANTICO_INICIAL = 212
    SIMBOLO_SEMANTICO_FINAL = 350  # Ajustar según sea necesario

    # Constantes con las rutinas semánticas
    # Mapeo de símbolos semánticos identificados en los logs
    INIT_TSG = 220           # #init_tsg - Inicializar tabla de símbolos global
    FREE_TSG = 221           # #free_tsg - Liberar tabla de símbolos global
    CHECK_EXISTENCE = 222    # #chkExistencia - Verificar existencia de identificador
    CHECK_FUNC_START = 223   # #chk_func_start - Verificar inicio de función
    CHECK_FUNC_RETURN = 224  # #chk_func_return - Verificar retorno de función
    VAR_LIST_MORE = 228      # Manejo de más variables en lista
    VAR_INIT = 229           # Inicialización de variables
    LITERAL_INIT = 230       # Inicialización con literal
    PARAM_MORE = 231         # Más parámetros
    # ... Agregar más según aparezcan en los logs

    @staticmethod
    def esTerminal(numSimbolo):
        """
        Método esTerminal
            Devuelve true si el símbolo es un terminal
            o false de lo contrario
        @param numSimbolo: Número de símbolo
        """
        return (0 <= numSimbolo <= 133)

    @staticmethod
    def esNoTerminal(numSimbolo):
        """
        Método esNoTerminal
            Devuelve true si el símbolo es un no-terminal
            o false de lo contrario
        @param numSimbolo: Número de símbolo
        """
        return (134 <= numSimbolo <= 211)

    @staticmethod
    def esSimboloSemantico(numSimbolo):
        """
        🔧 MÉTODO CORREGIDO
        Método esSimboloSemantico
            Devuelve true si el símbolo es un símbolo semántico
            (incluyendo los símbolos de generación de código)
            o false de lo contrario
        @param numSimbolo: Número de símbolo
        """
        # CORRECCIÓN: Rango válido para símbolos semánticos
        return (212 <= numSimbolo <= 350)  # ✅ Rango matemáticamente válido

    @staticmethod
    def obtenerNombreSimboloSemantico(numSimbolo):
        """
        🆕 NUEVO MÉTODO
        Obtiene el nombre descriptivo de un símbolo semántico
        @param numSimbolo: Número del símbolo semántico
        @return: Nombre del símbolo semántico o "DESCONOCIDO"
        """
        simbolos_semanticos = {
            220: "init_tsg",
            221: "free_tsg", 
            222: "chkExistencia",
            223: "chk_func_start",
            224: "chk_func_return",
            225: "literal_init",
            226: "var_more",
            227: "param_more",
            228: "var_list_more",
            229: "var_init",
            230: "literal_proc",
            231: "param_proc",
            # Agregar más según se identifiquen
        }
        
        return simbolos_semanticos.get(numSimbolo, f"SEMANTICO_{numSimbolo}")

    @staticmethod
    def diagnosticarSimbolo(numSimbolo):
        """
        🆕 NUEVO MÉTODO DE DIAGNÓSTICO
        Diagnostica qué tipo de símbolo es y proporciona información útil
        @param numSimbolo: Número de símbolo a diagnosticar
        @return: String con información del símbolo
        """
        if Gramatica.esTerminal(numSimbolo):
            try:
                nombre = Gramatica.getNombresTerminales(numSimbolo)
                return f"TERMINAL: {nombre} ({numSimbolo})"
            except:
                return f"TERMINAL: T{numSimbolo} ({numSimbolo})"
        
        elif Gramatica.esNoTerminal(numSimbolo):
            indice = numSimbolo - Gramatica.NO_TERMINAL_INICIAL
            return f"NO_TERMINAL: NT{indice} ({numSimbolo})"
        
        elif Gramatica.esSimboloSemantico(numSimbolo):
            nombre = Gramatica.obtenerNombreSimboloSemantico(numSimbolo)
            return f"SIMBOLO_SEMANTICO: #{nombre} ({numSimbolo})"
        
        else:
            return f"DESCONOCIDO: {numSimbolo} - ¡REVISAR RANGOS!"

    @staticmethod
    def getTablaParsing(numNoTerminal, numTerminal):
        """
        Método getTablaParsing
            Devuelve el número de regla contenida en la tabla de parsing
        @param numNoTerminal: Número del no-terminal
        @param numTerminal: Número del terminal
        """
        return GTablaParsing.getTablaParsing(numNoTerminal, numTerminal)

    @staticmethod
    def getLadosDerechos(numRegla, numColumna):
        """
        Método getLadosDerechos
            Obtiene un símbolo del lado derecho de la regla
        @param numRegla: Número de regla
        @param numColumna: Número de columna
        """
        return GLadosDerechos.getLadosDerechos(numRegla, numColumna)

    @staticmethod
    def getNombresTerminales(numTerminal):
        """
        Método getNombresTerminales
            Obtiene el nombre del terminal
        @param numTerminal: Número del terminal
        """
        return GNombresTerminales.getNombresTerminales(numTerminal)

    @staticmethod
    def getTablaFollows(numNoTerminal, numColumna):
        """
        Método getTablaFollows
            Obtiene el número de terminal del follow del no-terminal
        @param numNoTerminal: Número de no-terminal
        @param numColumna: Número de columna
        """
        from .GTablaFollows import GTablaFollows
        return GTablaFollows.getTablaFollows(numNoTerminal, numColumna)

    @staticmethod
    def verificarIntegridadRangos():
        """
        🆕 MÉTODO DE VERIFICACIÓN
        Verifica que los rangos de símbolos estén correctamente definidos
        """
        print("=== VERIFICACIÓN DE INTEGRIDAD DE RANGOS ===")
        print(f"Terminales: 0-{Gramatica.MARCA_DERECHA}")
        print(f"No-terminales: {Gramatica.NO_TERMINAL_INICIAL}-211")
        print(f"Símbolos semánticos: 212-{Gramatica.SIMBOLO_SEMANTICO_FINAL}")
        
        # Verificar que no hay solapamiento
        if Gramatica.MARCA_DERECHA >= Gramatica.NO_TERMINAL_INICIAL:
            print("⚠️  ADVERTENCIA: Solapamiento entre terminales y no-terminales")
        
        if 211 >= 212:
            print("✅ Sin solapamiento entre no-terminales y símbolos semánticos")
        else:
            print("⚠️  ADVERTENCIA: Gap entre no-terminales y símbolos semánticos")
        
        print("===============================================")