"""
Compilador Notch Engine

Estudiantes: Cabrera Samir y Urbina Luis

Archivo: mc_generacion.py

Breve Descripcion: Generador de código ensamblador para Notch Engine
"""

import os
from datetime import datetime
from enum import Enum

class TipoSegmento(Enum):
    """Tipos de segmentos de memoria"""
    DATOS = "DATOS"
    CODIGO = "CODIGO"

# =====================================================
# CLASE BASE: GeneradorCodigo
# =====================================================

class GeneradorCodigo:
    """Generador de código ensamblador para el compilador Notch Engine"""
    
    def __init__(self, nombres_estudiantes=["Cabrera Samir", "Urbina Luis"]):
        self.nombres_estudiantes = nombres_estudiantes
        self.codigo_generado = []
        self.datos_generados = []
        
        # Control de segmentos (límites simplificados)
        self.limite_datos = 65536  # 64KB para datos
        self.limite_codigo = 65536  # 64KB para código
        self.tamaño_datos_actual = 0
        self.tamaño_codigo_actual = 0
        
        # Nuevo diccionario de símbolos semánticos para generación de código
        self.simbolos_generacion = {}
        
        # Contador para etiquetas únicas
        self.contador_etiquetas = 0
        
        # Lista de errores de generación
        self.errores_generacion = []
        
        # Inicializar estructura básica
        self.inicializar_estructura()
    
    def inicializar_estructura(self):
        """Inicializa la estructura básica del archivo ASM"""
        self.generar_portada()
        self.generar_configuracion_inicial()
    
    def generar_portada(self):
        """Genera la portada identificativa del programa"""
        fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M")
        
        portada = [
            ";===============================================",
            ";              NOTCH ENGINE COMPILER",
            ";===============================================",
            f"; Generado por: {', '.join(self.nombres_estudiantes)}",
            f"; Fecha: {fecha_actual}",
            "; Proyecto: Compilador para Notch Engine",
            "; Etapa 4: Generador de Código",
            ";===============================================",
            ""
        ]
        
        self.codigo_generado.extend(portada)
        self.tamaño_codigo_actual += len('\n'.join(portada))
    
    def generar_configuracion_inicial(self):
        """Genera la configuración inicial del programa ASM"""
        config = [
            "; Configuración inicial del programa",
            "ASSUME CS:CODE, DS:DATA, SS:STACK",
            "",
            "; Segmento de pila",
            "STACK SEGMENT STACK",
            "    DW 256 DUP(?)",
            "STACK ENDS",
            "",
            "; Segmento de datos",
            "DATA SEGMENT",
        ]
        
        self.codigo_generado.extend(config)
        self.tamaño_codigo_actual += len('\n'.join(config))
    
    def agregar_simbolo_generacion(self, nombre, tipo, direccion=None, tamaño=None):
        """Agrega un símbolo al diccionario de generación de código"""
        self.simbolos_generacion[nombre] = {
            'tipo': tipo,
            'direccion': direccion,
            'tamaño': tamaño,
            'declarado': True
        }
    
    def verificar_espacio_segmento(self, tipo_segmento, tamaño_requerido):
        """Verifica si hay espacio suficiente en el segmento"""
        if tipo_segmento == TipoSegmento.DATOS:
            if self.tamaño_datos_actual + tamaño_requerido > self.limite_datos:
                self.generar_error_generacion(
                    f"Segmento de datos lleno. Tamaño requerido: {tamaño_requerido}, "
                    f"Espacio disponible: {self.limite_datos - self.tamaño_datos_actual}"
                )
                return False
            self.tamaño_datos_actual += tamaño_requerido
        
        elif tipo_segmento == TipoSegmento.CODIGO:
            if self.tamaño_codigo_actual + tamaño_requerido > self.limite_codigo:
                self.generar_error_generacion(
                    f"Segmento de código lleno. Tamaño requerido: {tamaño_requerido}, "
                    f"Espacio disponible: {self.limite_codigo - self.tamaño_codigo_actual}"
                )
                return False
            self.tamaño_codigo_actual += tamaño_requerido
        
        return True
    
    def generar_etiqueta_unica(self, prefijo="L"):
        """Genera una etiqueta única"""
        self.contador_etiquetas += 1
        return f"{prefijo}{self.contador_etiquetas:04d}"
    
    def generar_error_generacion(self, mensaje):
        """Registra un error de generación de código"""
        error = {
            'numero': len(self.errores_generacion) + 4001,  # Errores de generación empiezan en 4001
            'tipo': 'Generación de Código',
            'mensaje': mensaje,
            'fatal': True  # Los errores de generación son no recuperables según el enunciado
        }
        self.errores_generacion.append(error)
        print(f"ERROR {error['numero']}: {mensaje}")
        
    def declarar_variable(self, nombre, tipo_notch, valor_inicial=None):
        """Declara una variable en el segmento de datos"""
        # Mapeo de tipos de Notch Engine a ASM
        tipos_asm = {
            'STACK': ('DW', 2),     # Entero
            'RUNE': ('DD', 4),      # Flotante
            'SPIDER': ('DB', 1),    # Carácter
            'TORCH': ('DB', 1),     # Booleano
            'BOOK': ('DB 255 DUP(?)', 255),  # String
            'CHEST': ('DW 100 DUP(?)', 200)  # Arreglo básico
        }
        
        if tipo_notch not in tipos_asm:
            self.generar_error_generacion(f"Tipo desconocido: {tipo_notch}")
            return
        
        tipo_asm, tamaño = tipos_asm[tipo_notch]
        
        # Verificar espacio en segmento de datos
        if not self.verificar_espacio_segmento(TipoSegmento.DATOS, tamaño):
            return
        
        # Generar declaración
        if valor_inicial:
            declaracion = f"    {nombre} {tipo_asm.split()[0]} {valor_inicial}"
        else:
            declaracion = f"    {nombre} {tipo_asm}"
        
        self.datos_generados.append(declaracion)
        self.agregar_simbolo_generacion(nombre, tipo_notch, len(self.datos_generados), tamaño)
        
        print(f"Variable declarada: {nombre} ({tipo_notch})")
    
    def generar_asignacion_simple(self, variable, valor):
        """Genera código para asignación simple: variable = valor"""
        if variable not in self.simbolos_generacion:
            self.generar_error_generacion(f"Variable no declarada: {variable}")
            return
        
        tipo_var = self.simbolos_generacion[variable]['tipo']
        
        # Código de asignación básica
        codigo_asignacion = [
            f"    ; Asignación: {variable} = {valor}",
            f"    MOV AX, {valor}",
            f"    MOV {variable}, AX",
            ""
        ]
        
        # Verificar espacio en segmento de código
        tamaño_codigo = len('\n'.join(codigo_asignacion))
        if not self.verificar_espacio_segmento(TipoSegmento.CODIGO, tamaño_codigo):
            return
        
        self.codigo_generado.extend(codigo_asignacion)
        print(f"Asignación generada: {variable} = {valor}")
    
    def finalizar_programa(self):
        """Finaliza la estructura del programa ASM"""
        finalizacion = [
            "",
            "DATA ENDS",
            "",
            "; Segmento de código",
            "CODE SEGMENT",
            "MAIN PROC",
            "    MOV AX, DATA",
            "    MOV DS, AX",
            "",
            "    ; Código principal generado",
        ]
        
        # Agregar el código generado
        finalizacion.extend(self.codigo_generado[len(self.codigo_generado):])
        
        finalizacion.extend([
            "",
            "    ; Terminar programa",
            "    MOV AH, 4Ch",
            "    INT 21h",
            "MAIN ENDP",
            "CODE ENDS",
            "END MAIN"
        ])
        
        self.codigo_generado.extend(finalizacion)
    
    def obtener_codigo_completo(self):
        """Retorna el código ASM completo"""
        codigo_completo = []
        
        # Portada y configuración inicial (ya incluida)
        inicio_datos = None
        for i, linea in enumerate(self.codigo_generado):
            if "DATA SEGMENT" in linea:
                inicio_datos = i + 1
                break
        
        if inicio_datos:
            # Insertar datos generados después de "DATA SEGMENT"
            codigo_completo = (
                self.codigo_generado[:inicio_datos] + 
                self.datos_generados + 
                self.codigo_generado[inicio_datos:]
            )
        else:
            codigo_completo = self.codigo_generado
        
        return '\n'.join(codigo_completo)
    
    def guardar_archivo(self, nombre_archivo):
        """Guarda el código generado en un archivo ASM"""
        try:
            with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
                archivo.write(self.obtener_codigo_completo())
            print(f"Archivo generado exitosamente: {nombre_archivo}")
            return True
        except Exception as e:
            self.generar_error_generacion(f"Error al guardar archivo: {str(e)}")
            return False
    
    def obtener_estadisticas(self):
        """Retorna estadísticas del generador"""
        return {
            'variables_declaradas': len(self.simbolos_generacion),
            'tamaño_datos': self.tamaño_datos_actual,
            'tamaño_codigo': self.tamaño_codigo_actual,
            'espacio_datos_disponible': self.limite_datos - self.tamaño_datos_actual,
            'espacio_codigo_disponible': self.limite_codigo - self.tamaño_codigo_actual,
            'errores_generacion': len(self.errores_generacion)
        }

# =====================================================
# CLASE EXTENDIDA: GeneradorConRuntime
# =====================================================

class GeneradorConRuntime(GeneradorCodigo):
    """Generador de código extendido con Runtime Library"""
    
    def __init__(self, nombres_estudiantes=["Cabrera Samir", "Urbina Luis"]):
        super().__init__(nombres_estudiantes)
        self.incluir_runtime = True
        self.runtime_incluida = False
    
    def generar_operacion_aritmetica(self, operador, var_resultado, operando1, operando2):
        """Genera código para operaciones aritméticas usando la Runtime Library"""
        
        # Mapeo de operadores a rutinas de la Runtime Library
        operaciones_runtime = {
            ':+': 'SUMAR_ENTEROS',
            ':-': 'RESTAR_ENTEROS', 
            ':*': 'MULTIPLICAR_ENTEROS',
            ':/': 'DIVIDIR_ENTEROS',
            ':%': 'MODULO_ENTEROS'
        }
        
        if operador not in operaciones_runtime:
            self.generar_error_generacion(f"Operador no soportado: {operador}")
            return
        
        rutina = operaciones_runtime[operador]
        
        codigo_operacion = [
            f"    ; Operación: {var_resultado} = {operando1} {operador} {operando2}",
            f"    PUSH {operando2}    ; Segundo operando",
            f"    PUSH {operando1}    ; Primer operando", 
            f"    CALL {rutina}       ; Llamar rutina de Runtime Library",
            f"    MOV {var_resultado}, AX  ; Guardar resultado",
            ""
        ]
        
        # Verificar espacio y agregar código
        tamaño_codigo = len('\n'.join(codigo_operacion))
        if self.verificar_espacio_segmento(TipoSegmento.CODIGO, tamaño_codigo):
            self.codigo_generado.extend(codigo_operacion)
            print(f"Operación generada: {var_resultado} = {operando1} {operador} {operando2}")
    
    def incluir_runtime_library(self):
        """Incluye la Runtime Library al final del código"""
        if self.runtime_incluida:
            return
        
        runtime_include = [
            "",
            ";===============================================",
            ";           INCLUSIÓN DE RUNTIME LIBRARY",
            ";===============================================",
            "",
            "; Incluir el archivo de Runtime Library",
            "INCLUDE runtime_library.asm",
            ""
        ]
        
        self.codigo_generado.extend(runtime_include)
        self.runtime_incluida = True
        print("Runtime Library incluida en el código generado")
    
    def crear_archivo_runtime(self, nombre_archivo_runtime="runtime_library.asm"):
        """Crea el archivo separado de Runtime Library COMPLETA"""
        try:
            # Contenido COMPLETO de la Runtime Library - Todas las operaciones unificadas
            runtime_content = """;===============================================
;           NOTCH ENGINE RUN TIME LIBRARY
;===============================================
; Generado por: Cabrera Samir, Urbina Luis
; Biblioteca de rutinas en tiempo de ejecución
; VERSIÓN COMPLETA - Etapa 4
;===============================================

;===============================================
; OPERACIONES ARITMÉTICAS ENTERAS (STACK)
;===============================================

; Rutina: Sumar dos enteros
SUMAR_ENTEROS PROC
    PUSH BP
    MOV BP, SP
    PUSH BX
    
    MOV AX, [BP+4]
    MOV BX, [BP+6]
    ADD AX, BX
    
    POP BX
    POP BP
    RET 4
SUMAR_ENTEROS ENDP

; Rutina: Restar dos enteros
RESTAR_ENTEROS PROC
    PUSH BP
    MOV BP, SP
    PUSH BX
    
    MOV AX, [BP+4]
    MOV BX, [BP+6]
    SUB AX, BX
    
    POP BX
    POP BP
    RET 4
RESTAR_ENTEROS ENDP

; Rutina: Multiplicar dos enteros
MULTIPLICAR_ENTEROS PROC
    PUSH BP
    MOV BP, SP
    PUSH BX
    PUSH DX
    
    MOV AX, [BP+4]
    MOV BX, [BP+6]
    IMUL BX
    
    POP DX
    POP BX
    POP BP
    RET 4
MULTIPLICAR_ENTEROS ENDP

; Rutina: Dividir dos enteros
DIVIDIR_ENTEROS PROC
    PUSH BP
    MOV BP, SP
    PUSH BX
    PUSH DX
    
    MOV AX, [BP+4]
    MOV BX, [BP+6]
    
    CMP BX, 0
    JE @DIV_ERROR
    
    CWD
    IDIV BX
    JMP @DIV_FIN
    
@DIV_ERROR:
    MOV AX, 0
    
@DIV_FIN:
    POP DX
    POP BX
    POP BP
    RET 4
DIVIDIR_ENTEROS ENDP

; Rutina: NUEVA - Módulo de dos enteros
MODULO_ENTEROS PROC
    PUSH BP
    MOV BP, SP
    PUSH BX
    PUSH DX
    
    MOV AX, [BP+4]
    MOV BX, [BP+6]
    
    CMP BX, 0
    JE @MOD_ERROR
    
    CWD
    IDIV BX
    MOV AX, DX    ; El resto está en DX
    JMP @MOD_FIN
    
@MOD_ERROR:
    MOV AX, 0
    
@MOD_FIN:
    POP DX
    POP BX
    POP BP
    RET 4
MODULO_ENTEROS ENDP

; Rutina: NUEVA - Incremento (soulsand)
INCREMENTAR_ENTERO PROC
    PUSH BP
    MOV BP, SP
    
    MOV AX, [BP+4]
    INC AX
    
    POP BP
    RET 2
INCREMENTAR_ENTERO ENDP

; Rutina: NUEVA - Decremento (magma)
DECREMENTAR_ENTERO PROC
    PUSH BP
    MOV BP, SP
    
    MOV AX, [BP+4]
    DEC AX
    
    POP BP
    RET 2
DECREMENTAR_ENTERO ENDP

;===============================================
; OPERACIONES DE COMPARACIÓN
;===============================================

; Rutina: Comparar si A == B
COMPARAR_IGUAL PROC
    PUSH BP
    MOV BP, SP
    PUSH BX
    
    MOV AX, [BP+4]
    MOV BX, [BP+6]
    CMP AX, BX
    
    MOV AX, 0
    JNE @COMP_IGUAL_FIN
    MOV AX, 1
    
@COMP_IGUAL_FIN:
    POP BX
    POP BP
    RET 4
COMPARAR_IGUAL ENDP

; Rutina: Comparar si A != B
COMPARAR_DIFERENTE PROC
    PUSH BP
    MOV BP, SP
    PUSH BX
    
    MOV AX, [BP+4]
    MOV BX, [BP+6]
    CMP AX, BX
    
    MOV AX, 0
    JE @COMP_DIF_FIN
    MOV AX, 1
    
@COMP_DIF_FIN:
    POP BX
    POP BP
    RET 4
COMPARAR_DIFERENTE ENDP

; Rutina: Comparar si A > B
COMPARAR_MAYOR PROC
    PUSH BP
    MOV BP, SP
    PUSH BX
    
    MOV AX, [BP+4]
    MOV BX, [BP+6]
    CMP AX, BX
    
    MOV AX, 0
    JLE @COMP_MAYOR_FIN
    MOV AX, 1
    
@COMP_MAYOR_FIN:
    POP BX
    POP BP
    RET 4
COMPARAR_MAYOR ENDP

; Rutina: NUEVA - Comparar si A < B
COMPARAR_MENOR PROC
    PUSH BP
    MOV BP, SP
    PUSH BX
    
    MOV AX, [BP+4]
    MOV BX, [BP+6]
    CMP AX, BX
    
    MOV AX, 0
    JGE @COMP_MENOR_FIN
    MOV AX, 1
    
@COMP_MENOR_FIN:
    POP BX
    POP BP
    RET 4
COMPARAR_MENOR ENDP

; Rutina: NUEVA - Comparar si A >= B
COMPARAR_MAYOR_IGUAL PROC
    PUSH BP
    MOV BP, SP
    PUSH BX
    
    MOV AX, [BP+4]
    MOV BX, [BP+6]
    CMP AX, BX
    
    MOV AX, 0
    JL @COMP_MAYOR_IG_FIN
    MOV AX, 1
    
@COMP_MAYOR_IG_FIN:
    POP BX
    POP BP
    RET 4
COMPARAR_MAYOR_IGUAL ENDP

; Rutina: NUEVA - Comparar si A <= B
COMPARAR_MENOR_IGUAL PROC
    PUSH BP
    MOV BP, SP
    PUSH BX
    
    MOV AX, [BP+4]
    MOV BX, [BP+6]
    CMP AX, BX
    
    MOV AX, 0
    JG @COMP_MENOR_IG_FIN
    MOV AX, 1
    
@COMP_MENOR_IG_FIN:
    POP BX
    POP BP
    RET 4
COMPARAR_MENOR_IGUAL ENDP

;===============================================
; OPERACIONES LÓGICAS (TORCH - BOOLEANOS)
;===============================================

; Rutina: NUEVA - AND lógico
AND_LOGICO PROC
    PUSH BP
    MOV BP, SP
    PUSH BX
    
    MOV AL, [BP+4]    ; Primer operando
    MOV BL, [BP+5]    ; Segundo operando
    AND AL, BL        ; Operación AND
    
    POP BX
    POP BP
    RET 2
AND_LOGICO ENDP

; Rutina: NUEVA - OR lógico
OR_LOGICO PROC
    PUSH BP
    MOV BP, SP
    PUSH BX
    
    MOV AL, [BP+4]    ; Primer operando
    MOV BL, [BP+5]    ; Segundo operando
    OR AL, BL         ; Operación OR
    
    POP BX
    POP BP
    RET 2
OR_LOGICO ENDP

; Rutina: NUEVA - NOT lógico
NOT_LOGICO PROC
    PUSH BP
    MOV BP, SP
    
    MOV AL, [BP+4]    ; Operando
    NOT AL            ; Inversión
    AND AL, 1         ; Mantener solo el bit menos significativo
    
    POP BP
    RET 1
NOT_LOGICO ENDP

; Rutina: NUEVA - XOR lógico
XOR_LOGICO PROC
    PUSH BP
    MOV BP, SP
    PUSH BX
    
    MOV AL, [BP+4]    ; Primer operando
    MOV BL, [BP+5]    ; Segundo operando
    XOR AL, BL        ; Operación XOR
    
    POP BX
    POP BP
    RET 2
XOR_LOGICO ENDP

;===============================================
; OPERACIONES DE ENTRADA/SALIDA (E/S)
;===============================================

; Rutina: Leer entero (HOPPER_STACK)
LEER_ENTERO PROC
    PUSH BX
    PUSH CX
    PUSH DX
    
    MOV AH, 01h
    MOV BX, 0
    
@LEER_ENT_LOOP:
    INT 21h
    CMP AL, 0Dh
    JE @LEER_ENT_FIN
    
    CMP AL, '0'
    JB @LEER_ENT_LOOP
    CMP AL, '9'
    JA @LEER_ENT_LOOP
    
    SUB AL, '0'
    MOV AH, 0
    
    PUSH AX
    MOV AX, BX
    MOV DX, 10
    MUL DX
    MOV BX, AX
    POP AX
    ADD BX, AX
    
    JMP @LEER_ENT_LOOP

@LEER_ENT_FIN:
    MOV AX, BX
    
    POP DX
    POP CX
    POP BX
    RET
LEER_ENTERO ENDP

; Rutina: Mostrar entero (DROPPER_STACK)
MOSTRAR_ENTERO PROC
    PUSH BP
    MOV BP, SP
    PUSH AX
    PUSH BX
    PUSH CX
    PUSH DX
    
    MOV AX, [BP+4]
    MOV BX, 10
    MOV CX, 0
    
@MOST_ENT_LOOP:
    MOV DX, 0
    DIV BX
    PUSH DX
    INC CX
    CMP AX, 0
    JNE @MOST_ENT_LOOP
    
@MOST_ENT_DISPLAY:
    POP DX
    ADD DL, '0'
    MOV AH, 02h
    INT 21h
    LOOP @MOST_ENT_DISPLAY
    
    POP DX
    POP CX
    POP BX
    POP AX
    POP BP
    RET 2
MOSTRAR_ENTERO ENDP

; Rutina: NUEVA - Leer carácter (HOPPER_RUNE)
LEER_CARACTER PROC
    MOV AH, 01h
    INT 21h
    ; El carácter queda en AL
    RET
LEER_CARACTER ENDP

; Rutina: NUEVA - Mostrar carácter (DROPPER_RUNE)
MOSTRAR_CARACTER PROC
    PUSH BP
    MOV BP, SP
    PUSH DX
    
    MOV DL, [BP+4]    ; Carácter a mostrar
    MOV AH, 02h
    INT 21h
    
    POP DX
    POP BP
    RET 2
MOSTRAR_CARACTER ENDP

; Rutina: NUEVA - Leer booleano (HOPPER_TORCH)
LEER_BOOLEANO PROC
    MOV AH, 01h
    INT 21h
    
    CMP AL, '1'
    JE @LEER_BOOL_TRUE
    CMP AL, 'T'
    JE @LEER_BOOL_TRUE
    CMP AL, 't'
    JE @LEER_BOOL_TRUE
    
    MOV AX, 0         ; False
    JMP @LEER_BOOL_FIN
    
@LEER_BOOL_TRUE:
    MOV AX, 1         ; True
    
@LEER_BOOL_FIN:
    RET
LEER_BOOLEANO ENDP

; Rutina: NUEVA - Mostrar booleano (DROPPER_TORCH)
MOSTRAR_BOOLEANO PROC
    PUSH BP
    MOV BP, SP
    PUSH DX
    
    MOV AX, [BP+4]
    CMP AX, 0
    JE @MOST_BOOL_FALSE
    
    MOV AH, 09h
    LEA DX, STR_TRUE
    INT 21h
    JMP @MOST_BOOL_FIN
    
@MOST_BOOL_FALSE:
    MOV AH, 09h
    LEA DX, STR_FALSE
    INT 21h
    
@MOST_BOOL_FIN:
    POP DX
    POP BP
    RET 2
MOSTRAR_BOOLEANO ENDP

;===============================================
; OPERACIONES DE STRINGS (SPIDER) - BÁSICAS
;===============================================

; Rutina: NUEVA - Concatenar strings (BIND)
CONCATENAR_STRINGS PROC
    PUSH BP
    MOV BP, SP
    PUSH SI
    PUSH DI
    PUSH CX
    
    MOV SI, [BP+4]    ; String fuente 1
    MOV DI, [BP+6]    ; String fuente 2
    MOV BX, [BP+8]    ; Buffer destino
    
    ; Copiar primer string
@CONCAT_LOOP1:
    MOV AL, [SI]
    CMP AL, '$'
    JE @CONCAT_SECOND
    MOV [BX], AL
    INC SI
    INC BX
    JMP @CONCAT_LOOP1
    
@CONCAT_SECOND:
    ; Copiar segundo string
@CONCAT_LOOP2:
    MOV AL, [DI]
    MOV [BX], AL
    CMP AL, '$'
    JE @CONCAT_FIN
    INC DI
    INC BX
    JMP @CONCAT_LOOP2
    
@CONCAT_FIN:
    POP CX
    POP DI
    POP SI
    POP BP
    RET 6
CONCATENAR_STRINGS ENDP

; Rutina: NUEVA - Longitud de string (#)
LONGITUD_STRING PROC
    PUSH BP
    MOV BP, SP
    PUSH SI
    
    MOV SI, [BP+4]    ; Dirección del string
    MOV AX, 0         ; Contador
    
@LEN_LOOP:
    MOV BL, [SI]
    CMP BL, '$'
    JE @LEN_FIN
    INC AX
    INC SI
    JMP @LEN_LOOP
    
@LEN_FIN:
    POP SI
    POP BP
    RET 2
LONGITUD_STRING ENDP

;===============================================
; DATOS PARA RUTINAS
;===============================================
STR_TRUE    DB "ON$"
STR_FALSE   DB "OFF$"
NEWLINE     DB 13, 10, '$'
SPACE       DB ' $'
"""
            
            with open(nombre_archivo_runtime, 'w', encoding='utf-8') as archivo:
                archivo.write(runtime_content)
            
            # Estadísticas de lo que se creó
            operaciones_incluidas = [
                "SUMAR_ENTEROS", "RESTAR_ENTEROS", "MULTIPLICAR_ENTEROS", 
                "DIVIDIR_ENTEROS", "MODULO_ENTEROS", "INCREMENTAR_ENTERO", "DECREMENTAR_ENTERO",
                "COMPARAR_IGUAL", "COMPARAR_DIFERENTE", "COMPARAR_MAYOR", "COMPARAR_MENOR",
                "COMPARAR_MAYOR_IGUAL", "COMPARAR_MENOR_IGUAL",
                "AND_LOGICO", "OR_LOGICO", "NOT_LOGICO", "XOR_LOGICO",
                "LEER_ENTERO", "MOSTRAR_ENTERO", "LEER_CARACTER", "MOSTRAR_CARACTER",
                "LEER_BOOLEANO", "MOSTRAR_BOOLEANO", "CONCATENAR_STRINGS", "LONGITUD_STRING"
            ]
            
            print(f"✅ Runtime Library COMPLETA creada: {nombre_archivo_runtime}")
            print(f"📊 Total de rutinas incluidas: {len(operaciones_incluidas)}")
            print("🔧 Operaciones unificadas de etapas anteriores:")
            print("   - Operaciones aritméticas enteras")
            print("   - Todas las comparaciones")
            print("   - Operaciones lógicas booleanas")
            print("   - E/S básica para tipos principales")
            print("   - Incremento/decremento")
            print("   - Operaciones básicas de strings")
            
            return True
            
        except Exception as e:
            self.generar_error_generacion(f"Error al crear Runtime Library: {str(e)}")
            return False

# =====================================================
# CLASE COMPLETA: GeneradorCompleto
# =====================================================

class GeneradorCompleto(GeneradorConRuntime):
    """Generador de código completo con control de flujo y estructuras"""
    
    def __init__(self, nombres_estudiantes=["Cabrera Samir", "Urbina Luis"]):
        super().__init__(nombres_estudiantes)
        self.etiquetas_usadas = set()
        self.pila_contextos = []  # Para manejar contextos anidados
    
    def generar_etiqueta_contexto(self, tipo_contexto):
        """Genera etiquetas únicas para contextos (if, while, etc.)"""
        prefijos = {
            'if': 'IF',
            'while': 'WHILE', 
            'for': 'FOR',
            'proc': 'PROC',
            'spell': 'SPELL'
        }
        
        prefijo = prefijos.get(tipo_contexto, 'LABEL')
        etiqueta = f"{prefijo}{self.contador_etiquetas:04d}"
        self.contador_etiquetas += 1
        
        return etiqueta
    
    def generar_if_inicio(self, condicion, var_condicion):
        """Genera código para inicio de estructura IF"""
        etiqueta_else = self.generar_etiqueta_contexto('if') + "_ELSE"
        etiqueta_fin = self.generar_etiqueta_contexto('if') + "_FIN"
        
        # Guardar contexto
        contexto = {
            'tipo': 'if',
            'etiqueta_else': etiqueta_else,
            'etiqueta_fin': etiqueta_fin,
            'condicion': condicion
        }
        self.pila_contextos.append(contexto)
        
        codigo_if = [
            f"    ; IF: {condicion}",
            f"    CMP {var_condicion}, 0    ; Evaluar condición",
            f"    JE {etiqueta_else}        ; Saltar si falso",
            f"    ; Inicio del bloque IF",
            ""
        ]
        
        tamaño_codigo = len('\n'.join(codigo_if))
        if self.verificar_espacio_segmento(TipoSegmento.CODIGO, tamaño_codigo):
            self.codigo_generado.extend(codigo_if)
            print(f"IF generado: {condicion}")
    
    def generar_else(self):
        """Genera código para ELSE"""
        if not self.pila_contextos or self.pila_contextos[-1]['tipo'] != 'if':
            self.generar_error_generacion("ELSE sin IF correspondiente")
            return
        
        contexto = self.pila_contextos[-1]
        
        codigo_else = [
            f"    JMP {contexto['etiqueta_fin']}  ; Saltar al final del IF",
            f"{contexto['etiqueta_else']}:",
            f"    ; Inicio del bloque ELSE",
            ""
        ]
        
        tamaño_codigo = len('\n'.join(codigo_else))
        if self.verificar_espacio_segmento(TipoSegmento.CODIGO, tamaño_codigo):
            self.codigo_generado.extend(codigo_else)
            print("ELSE generado")
    
    def generar_endif(self):
        """Genera código para fin de IF"""
        if not self.pila_contextos or self.pila_contextos[-1]['tipo'] != 'if':
            self.generar_error_generacion("ENDIF sin IF correspondiente")
            return
        
        contexto = self.pila_contextos.pop()
        
        codigo_endif = [
            f"{contexto['etiqueta_fin']}:",
            f"    ; Fin del IF: {contexto['condicion']}",
            ""
        ]
        
        tamaño_codigo = len('\n'.join(codigo_endif))
        if self.verificar_espacio_segmento(TipoSegmento.CODIGO, tamaño_codigo):
            self.codigo_generado.extend(codigo_endif)
            print(f"ENDIF generado para: {contexto['condicion']}")

# =====================================================
# FUNCIÓN PRINCIPAL: generar_codigo_asm
# =====================================================

def generar_codigo_asm(archivo_prueba):
    """
    Función principal para generar código ASM (compatible con main.py original)
    Args:
        archivo_prueba: Path del archivo de prueba
    """
    try:
        print(f"🔧 Generando código ASM para: {archivo_prueba.name}")
        
        # Crear directorio de resultados si no existe
        from pathlib import Path
        resultados_dir = Path("resultadosASM")
        resultados_dir.mkdir(exist_ok=True)

        # Crear generador
        generador = GeneradorCompleto()
        
        # Crear Runtime Library si no existe
        runtime_path = resultados_dir / "runtime_library.asm"
        if not runtime_path.exists():
            print("📚 Creando Runtime Library...")
            generador.crear_archivo_runtime(str(runtime_path))

        # Generar nombre del archivo de salida
        nombre_archivo = f"RSLT{archivo_prueba.stem}.ASM"
        ruta_archivo = resultados_dir / nombre_archivo

        # Generar algunas variables y operaciones de ejemplo
        print("📝 Generando variables de ejemplo...")
        generador.declarar_variable("numero1", "STACK", "10")
        generador.declarar_variable("numero2", "STACK", "5")
        generador.declarar_variable("resultado", "STACK", "0")
        generador.declarar_variable("booleano", "TORCH", "1")
        
        # Generar algunas operaciones de ejemplo
        print("⚙️ Generando operaciones de ejemplo...")
        generador.generar_operacion_aritmetica(":+", "resultado", "numero1", "numero2")
        
        # Si hay Runtime Library disponible, generar más operaciones
        if hasattr(generador, 'generar_operacion_comparacion'):
            generador.declarar_variable("comparacion", "TORCH", "0")
            generador.generar_operacion_comparacion(">", "comparacion", "numero1", "numero2")
        
        # Finalizar programa
        generador.finalizar_programa()
        
        # Guardar archivo
        resultado = generador.guardar_archivo(str(ruta_archivo))
        
        if resultado:
            print(f"✅ Archivo ASM generado exitosamente: {ruta_archivo}")
            
            # Mostrar estadísticas
            stats = generador.obtener_estadisticas()
            print(f"📊 Estadísticas de generación:")
            print(f"   Variables declaradas: {stats['variables_declaradas']}")
            print(f"   Tamaño de datos: {stats['tamaño_datos']} bytes")
            print(f"   Tamaño de código: {stats['tamaño_codigo']} bytes")
            print(f"   Errores de generación: {stats['errores_generacion']}")
            
            return ruta_archivo
        else:
            print("❌ Error al guardar el archivo ASM")
            return None

    except Exception as e:
        print(f"❌ Error en generación de código: {str(e)}")
        import traceback
        traceback.print_exc()
        return None