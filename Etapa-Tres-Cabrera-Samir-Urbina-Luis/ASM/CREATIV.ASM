; ********************************************
; * Programa: CREATIV.ASM (SPYDEREYE)       *
; * Descripcion: Operaciones con probabilidades*
; * Autores: Luis Urbina, Samir Cabrera     *
; * Fecha: 30/05/2025                       *
; * Version: 2.0 - Menu Completo            *
; * Curso: Compiladores e Interpretes       *
; * Proyecto: Notch Engine - Etapa 3        *
; ********************************************

DATOS SEGMENT
    ; Mensajes de entrada y salida
    titulo       DB "DEMOSTRACION DE OPERACIONES CON SPYDEREYE (PROBABILIDADES)", 0Dh, 0Ah, '$'
    separador    DB "-------------------------------------------", 0Dh, 0Ah, '$'
    
    menu         DB "MENU DE OPERACIONES:", 0Dh, 0Ah
                 DB "1. Suma de probabilidades (:+)", 0Dh, 0Ah
                 DB "2. Resta de probabilidades (:-)", 0Dh, 0Ah
                 DB "3. Multiplicacion de probabilidades (:*)", 0Dh, 0Ah
                 DB "4. Division de probabilidades (://)", 0Dh, 0Ah
                 DB "5. Modulo de probabilidades (:%)", 0Dh, 0Ah
                 DB "6. Asignaciones (:+=, :-=, :*=, ://=, :%=)", 0Dh, 0Ah
                 DB "7. Comparaciones (<, >, <=, >=, is, isNot)", 0Dh, 0Ah
                 DB "8. Convertir a otros tipos", 0Dh, 0Ah
                 DB "0. Salir", 0Dh, 0Ah
                 DB "Seleccione una opcion: $"

    submenu_asig DB 0Dh, 0Ah, "OPERACIONES DE ASIGNACION:", 0Dh, 0Ah
                 DB "1. Suma y asigna (:+=)", 0Dh, 0Ah
                 DB "2. Resta y asigna (:-=)", 0Dh, 0Ah
                 DB "3. Multiplica y asigna (:*=)", 0Dh, 0Ah
                 DB "4. Divide y asigna (://=)", 0Dh, 0Ah
                 DB "5. Modulo y asigna (:%=)", 0Dh, 0Ah
                 DB "Seleccione: $"
    
    ; Prompts específicos para probabilidades
    prompt_prob1 DB "Ingrese primera probabilidad (0.0 - 1.0): $"
    prompt_prob2 DB "Ingrese segunda probabilidad (0.0 - 1.0): $"
    result_msg   DB "Resultado: $"
    
    ; Mensajes de error específicos para probabilidades
    error_div    DB "Error: Division por cero", 0Dh, 0Ah, '$'
    error_rango  DB "Error: La probabilidad debe estar entre 0.0 y 1.0", 0Dh, 0Ah, '$'
    warn_clamp   DB "Aviso: Resultado ajustado al rango [0.0, 1.0]", 0Dh, 0Ah, '$'

    ; Variables para primera probabilidad
    buffer1      DB 15, ?, 15 DUP(?)  ; Buffer para primera probabilidad
    entero1      DW ?                  ; Parte entera de la primera probabilidad
    decimal1     DW ?                  ; Parte decimal de la primera probabilidad
    dec_digitos1 DB ?                  ; Dígitos decimales de la primera probabilidad
    es_negativo1 DB 0                  ; Bandera de signo de la primera probabilidad
    
    ; Variables para segunda probabilidad
    buffer2      DB 15, ?, 15 DUP(?)  ; Buffer para segunda probabilidad
    entero2      DW ?                  ; Parte entera de la segunda probabilidad
    decimal2     DW ?                  ; Parte decimal de la segunda probabilidad
    dec_digitos2 DB ?                  ; Dígitos decimales de la segunda probabilidad
    es_negativo2 DB 0                  ; Bandera de signo de la segunda probabilidad
    
    ; Variables para el resultado
    resultado_entero   DW ?            ; Parte entera del resultado
    resultado_decimal  DW ?            ; Parte decimal del resultado
    resultado_digitos  DB ?            ; Dígitos decimales del resultado
    resultado_negativo DB 0            ; Bandera de signo del resultado
    resultado_clamped  DB 0            ; Indica si el resultado fue ajustado al rango
    
    ; Variables para conversiones
    int_valor    DW ?                  ; Conversión a entero (Stack)
    bool_valor   DB ?                  ; Conversión a booleano (Torch)
    char_valor   DB ?                  ; Conversión a caracter (Rune)
    string_buffer DB 50 DUP(?),'$'    ; Conversión a string (Spider)
    float_valor_ent  DW ?              ; Conversión a flotante - parte entera
    float_valor_dec  DW ?              ; Conversión a flotante - parte decimal
    
    ; Mensajes para conversiones
    prompt_conversiones_orig DB "La probabilidad original es: $"
    prompt_conv_int     DB "Convertido a Stack (entero): $"
    prompt_conv_bool    DB "Convertido a Torch (booleano): $"
    prompt_conv_char    DB "Convertido a Rune (caracter): $"
    prompt_conv_str     DB "Convertido a Spider (string): $"
    prompt_conv_float   DB "Convertido a Ghast (flotante): $"
    
    ; Mensajes para comparaciones
    msg_menor    DB "MENOR QUE (<): $"
    msg_mayor    DB "MAYOR QUE (>): $"
    msg_menig    DB "MENOR O IGUAL QUE (<=): $"
    msg_mayig    DB "MAYOR O IGUAL QUE (>=): $"
    msg_igual    DB "IGUAL A (is): $"
    msg_nig      DB "DISTINTO DE (isNot): $"
    
    ; Valores para mostrar booleanos
    valor_true   DB 'TRUE$'
    valor_false  DB 'FALSE$'
    
    ; Auxiliares
    nueva_lin    DB 0Dh, 0Ah, '$'
    punto        DB '.$'
    const_diez   DW 10
    const_cien   DW 100
    const_10000  DW 10000
DATOS ENDS

CODIGO SEGMENT
    ASSUME CS:CODIGO, DS:DATOS
INICIO:
    ; Inicialización: Preparamos el acceso al segmento de datos
    MOV AX, DATOS
    MOV DS, AX
    
    ; Mostrar título
    MOV AH, 09h
    LEA DX, titulo
    INT 21h
    
    LEA DX, separador
    INT 21h

MENU_PRINCIPAL:
    ; Mostrar menú de opciones
    MOV AH, 09h
    LEA DX, menu
    INT 21h
    
    ; Leer opción del usuario
    MOV AH, 01h
    INT 21h
    
    ; Comparar con las opciones disponibles - usando saltos largos
    CMP AL, '1'
    JNE @CREATIV_NOT1
    JMP OPCION_SUMA
@CREATIV_NOT1:
    CMP AL, '2'
    JNE @CREATIV_NOT2
    JMP OPCION_RESTA
@CREATIV_NOT2:
    CMP AL, '3'
    JNE @CREATIV_NOT3
    JMP OPCION_MULTIPLICACION
@CREATIV_NOT3:
    CMP AL, '4'
    JNE @CREATIV_NOT4
    JMP OPCION_DIVISION
@CREATIV_NOT4:
    CMP AL, '5'
    JNE @CREATIV_NOT5
    JMP OPCION_MODULO
@CREATIV_NOT5:
    CMP AL, '6'
    JNE @CREATIV_NOT6
    JMP OPCION_ASIGNACIONES
@CREATIV_NOT6:
    CMP AL, '7'
    JNE @CREATIV_NOT7
    JMP OPCION_COMPARACIONES
@CREATIV_NOT7:
    CMP AL, '8'
    JNE @CREATIV_NOT8
    JMP OPCION_CONVERSIONES
@CREATIV_NOT8:
    CMP AL, '0'
    JNE @CREATIV_NOT0
    JMP SALIR
@CREATIV_NOT0:
    
    ; Si llegamos aquí, la opción no es válida, volver al menú
    JMP MENU_PRINCIPAL

SALIR:
    ; Terminamos el programa y regresamos al sistema operativo
    MOV AX, 4C00h
    INT 21h

OPCION_SUMA:
    CALL NUEVA_LINEA
    CALL LEER_DOS_PROBABILIDADES
    
    ; Realizar la suma de probabilidades (:+)
    CALL SUMAR_PROBABILIDADES
    
    ; Mostrar resultado
    CALL MOSTRAR_RESULTADO_PROBABILIDAD
    JMP MENU_PRINCIPAL

OPCION_RESTA:
    CALL NUEVA_LINEA
    CALL LEER_DOS_PROBABILIDADES
    
    ; Realizar la resta de probabilidades (:-)
    CALL RESTAR_PROBABILIDADES
    
    ; Mostrar resultado
    CALL MOSTRAR_RESULTADO_PROBABILIDAD
    JMP MENU_PRINCIPAL

OPCION_MULTIPLICACION:
    CALL NUEVA_LINEA
    CALL LEER_DOS_PROBABILIDADES
    
    ; Realizar la multiplicación de probabilidades (:*)
    CALL MULTIPLICAR_PROBABILIDADES
    
    ; Mostrar resultado
    CALL MOSTRAR_RESULTADO_PROBABILIDAD
    JMP MENU_PRINCIPAL

;------------------------------------------------------------
; Procedimiento: LEER_DOS_PROBABILIDADES
; Lee dos probabilidades desde la entrada estándar y valida rangos
;------------------------------------------------------------
LEER_DOS_PROBABILIDADES PROC
    ; Leer primera probabilidad
    MOV AH, 09h
    LEA DX, prompt_prob1
    INT 21h
    
    MOV AH, 0Ah
    LEA DX, buffer1
    INT 21h
    
    ; Procesar primera probabilidad
    CALL PROCESAR_PRIMERA_PROBABILIDAD
    
    ; Validar rango de la primera probabilidad
    CALL VALIDAR_RANGO_PRIMERA
    JC @CREATIV_ERROR_RANGO1
    
    CALL NUEVA_LINEA
    
    ; Leer segunda probabilidad
    MOV AH, 09h
    LEA DX, prompt_prob2
    INT 21h
    
    MOV AH, 0Ah
    LEA DX, buffer2
    INT 21h
    
    ; Procesar segunda probabilidad
    CALL PROCESAR_SEGUNDA_PROBABILIDAD
    
    ; Validar rango de la segunda probabilidad
    CALL VALIDAR_RANGO_SEGUNDA
    JC @CREATIV_ERROR_RANGO2
    
    CALL NUEVA_LINEA
    JMP @CREATIV_LECTURA_OK
    
@CREATIV_ERROR_RANGO1:
@CREATIV_ERROR_RANGO2:
    MOV AH, 09h
    LEA DX, error_rango
    INT 21h
    JMP MENU_PRINCIPAL
    
@CREATIV_LECTURA_OK:
    RET
LEER_DOS_PROBABILIDADES ENDP

;------------------------------------------------------------
; Procedimiento: SUMAR_PROBABILIDADES
; Realiza la suma de dos probabilidades (:+)
; El resultado se mantiene en rango [0.0, 1.0]
;------------------------------------------------------------
SUMAR_PROBABILIDADES PROC
    PUSH AX
    PUSH BX
    PUSH CX
    PUSH DX
    
    ; Normalizar decimales para operación
    CALL NORMALIZAR_DECIMALES_PARA_OPERACION
    
    ; Sumar valores absolutos (probabilidades son siempre positivas)
    CALL SUMAR_VALORES_ABSOLUTOS
    
    ; El resultado es siempre positivo para probabilidades
    MOV [resultado_negativo], 0
    
    ; Verificar si el resultado excede 1.0 y ajustar si es necesario
    CALL VERIFICAR_Y_AJUSTAR_RESULTADO
    
    POP DX
    POP CX
    POP BX
    POP AX
    RET
SUMAR_PROBABILIDADES ENDP

;------------------------------------------------------------
; Procedimiento: RESTAR_PROBABILIDADES
; Realiza la resta de dos probabilidades (:-)
; El resultado se mantiene en rango [0.0, 1.0]
;------------------------------------------------------------
RESTAR_PROBABILIDADES PROC
    PUSH AX
    PUSH BX
    PUSH CX
    PUSH DX
    
    ; Normalizar decimales para operación
    CALL NORMALIZAR_DECIMALES_PARA_OPERACION
    
    ; Comparar cuál probabilidad es mayor
    CALL COMPARAR_PROBABILIDADES_ABSOLUTO
    JC @CREATIV_RESTA_SEGUNDA_MAYOR
    
    ; Primera >= Segunda: resultado = primera - segunda
    CALL RESTAR_PRIMERA_MENOS_SEGUNDA
    MOV [resultado_negativo], 0
    JMP @CREATIV_RESTA_FIN
    
@CREATIV_RESTA_SEGUNDA_MAYOR:
    ; Segunda > Primera: resultado = 0 (no puede ser negativo)
    MOV [resultado_entero], 0
    MOV [resultado_decimal], 0
    MOV [resultado_negativo], 0
    MOV [resultado_clamped], 1  ; Indicar que fue ajustado
    
@CREATIV_RESTA_FIN:
    ; Verificar y ajustar resultado final
    CALL VERIFICAR_Y_AJUSTAR_RESULTADO
    
    POP DX
    POP CX
    POP BX
    POP AX
    RET
RESTAR_PROBABILIDADES ENDP

;------------------------------------------------------------
; Procedimiento: MULTIPLICAR_PROBABILIDADES
; Realiza la multiplicación de dos probabilidades (:*)
; P(A ∩ B) = P(A) * P(B) para eventos independientes
;------------------------------------------------------------
MULTIPLICAR_PROBABILIDADES PROC
    PUSH AX
    PUSH BX
    PUSH CX
    PUSH DX
    
    ; Para probabilidades: 0 ≤ P(A) * P(B) ≤ 1 siempre se cumple
    ; si 0 ≤ P(A) ≤ 1 y 0 ≤ P(B) ≤ 1
    
    ; Multiplicar usando método simplificado para probabilidades
    CALL MULTIPLICAR_VALORES_PROBABILIDAD
    
    ; El resultado es siempre positivo y ≤ 1.0 para probabilidades válidas
    MOV [resultado_negativo], 0
    
    ; Verificar resultado (debería estar en rango, pero por seguridad)
    CALL VERIFICAR_Y_AJUSTAR_RESULTADO
    
    POP DX
    POP CX
    POP BX
    POP AX
    RET
MULTIPLICAR_PROBABILIDADES ENDP

OPCION_DIVISION:
    CALL NUEVA_LINEA
    CALL LEER_DOS_PROBABILIDADES
    
    ; Verificar división por cero
    CALL VERIFICAR_CERO_SEGUNDA_PROBABILIDAD
    JC @CREATIV_ERROR_DIV
    
    ; Realizar la división de probabilidades (://)
    CALL DIVIDIR_PROBABILIDADES
    
    ; Mostrar resultado
    CALL MOSTRAR_RESULTADO_PROBABILIDAD
    JMP MENU_PRINCIPAL

@CREATIV_ERROR_DIV:
    MOV AH, 09h
    LEA DX, error_div
    INT 21h
    JMP MENU_PRINCIPAL

OPCION_MODULO:
    CALL NUEVA_LINEA
    CALL LEER_DOS_PROBABILIDADES
    
    ; Verificar división por cero para módulo
    CALL VERIFICAR_CERO_SEGUNDA_PROBABILIDAD
    JC @CREATIV_ERROR_MOD
    
    ; Realizar el módulo de probabilidades (:%)
    CALL MODULO_PROBABILIDADES
    
    ; Mostrar resultado
    CALL MOSTRAR_RESULTADO_PROBABILIDAD
    JMP MENU_PRINCIPAL

@CREATIV_ERROR_MOD:
    MOV AH, 09h
    LEA DX, error_div
    INT 21h
    JMP MENU_PRINCIPAL

OPCION_ASIGNACIONES:
    CALL NUEVA_LINEA
    
    ; Submenu para operaciones de asignación
    MOV AH, 09h
    LEA DX, submenu_asig
    INT 21h
    
    ; Leer subopción
    MOV AH, 01h
    INT 21h
    
    CMP AL, '1'
    JNE @CREATIV_ASIG_NOT1
    JMP ASIGNACION_SUMA
@CREATIV_ASIG_NOT1:
    CMP AL, '2'
    JNE @CREATIV_ASIG_NOT2
    JMP ASIGNACION_RESTA
@CREATIV_ASIG_NOT2:
    CMP AL, '3'
    JNE @CREATIV_ASIG_NOT3
    JMP ASIGNACION_MULT
@CREATIV_ASIG_NOT3:
    CMP AL, '4'
    JNE @CREATIV_ASIG_NOT4
    JMP ASIGNACION_DIV
@CREATIV_ASIG_NOT4:
    CMP AL, '5'
    JNE @CREATIV_ASIG_VOLVER
    JMP ASIGNACION_MOD
@CREATIV_ASIG_VOLVER:
    JMP MENU_PRINCIPAL

ASIGNACION_SUMA:
    ; Implementar A :+= B (equivale a A = A :+ B)
    CALL NUEVA_LINEA
    CALL LEER_DOS_PROBABILIDADES
    CALL SUMAR_PROBABILIDADES
    CALL MOSTRAR_RESULTADO_PROBABILIDAD
    JMP MENU_PRINCIPAL

ASIGNACION_RESTA:
    ; Implementar A :-= B (equivale a A = A :- B)
    CALL NUEVA_LINEA
    CALL LEER_DOS_PROBABILIDADES
    CALL RESTAR_PROBABILIDADES
    CALL MOSTRAR_RESULTADO_PROBABILIDAD
    JMP MENU_PRINCIPAL

ASIGNACION_MULT:
    ; Implementar A :*= B (equivale a A = A :* B)
    CALL NUEVA_LINEA
    CALL LEER_DOS_PROBABILIDADES
    CALL MULTIPLICAR_PROBABILIDADES
    CALL MOSTRAR_RESULTADO_PROBABILIDAD
    JMP MENU_PRINCIPAL

ASIGNACION_DIV:
    CALL NUEVA_LINEA
    CALL LEER_DOS_PROBABILIDADES
    
    CALL VERIFICAR_CERO_SEGUNDA_PROBABILIDAD
    JC @CREATIV_ASIG_ERROR_DIV
    
    CALL DIVIDIR_PROBABILIDADES
    CALL MOSTRAR_RESULTADO_PROBABILIDAD
    JMP MENU_PRINCIPAL

@CREATIV_ASIG_ERROR_DIV:
    MOV AH, 09h
    LEA DX, error_div
    INT 21h
    JMP MENU_PRINCIPAL

ASIGNACION_MOD:
    ; Implementar A :%= B (equivale a A = A :% B)
    CALL NUEVA_LINEA
    CALL LEER_DOS_PROBABILIDADES
    CALL VERIFICAR_CERO_SEGUNDA_PROBABILIDAD
    JC @CREATIV_ASIG_ERROR_MOD
    CALL MODULO_PROBABILIDADES
    CALL MOSTRAR_RESULTADO_PROBABILIDAD
    JMP MENU_PRINCIPAL

@CREATIV_ASIG_ERROR_MOD:
    MOV AH, 09h
    LEA DX, error_div
    INT 21h
    JMP MENU_PRINCIPAL

;------------------------------------------------------------
; Procedimiento: DIVIDIR_PROBABILIDADES
; Realiza la división de dos probabilidades (://)
; Para probabilidades: P(A)/P(B) puede exceder 1.0, así que se ajusta
;------------------------------------------------------------
DIVIDIR_PROBABILIDADES PROC
    PUSH AX
    PUSH BX
    PUSH CX
    PUSH DX
    
    ; División básica adaptada para probabilidades
    ; Usar solo las partes enteras y decimales normalizadas
    
    ; Convertir probabilidades a valores enteros para división
    CALL CONVERTIR_PROBABILIDADES_A_ENTEROS
    
    ; Realizar división entera
    MOV AX, BX              ; BX contiene valor1 * 1000
    MOV CX, DX              ; DX contiene valor2 * 1000
    
    XOR DX, DX              ; Limpiar DX
    DIV CX                  ; AX = resultado * 1000
    
    ; Convertir resultado de vuelta a formato probabilidad
    CALL CONVERTIR_ENTERO_A_PROBABILIDAD
    
    ; El resultado es siempre positivo
    MOV [resultado_negativo], 0
    
    ; Verificar y ajustar si excede 1.0
    CALL VERIFICAR_Y_AJUSTAR_RESULTADO
    
    POP DX
    POP CX
    POP BX
    POP AX
    RET
DIVIDIR_PROBABILIDADES ENDP

;------------------------------------------------------------
; Procedimiento: MODULO_PROBABILIDADES
; Realiza el módulo de dos probabilidades (:%)
; Para probabilidades: A % B donde resultado siempre < B
;------------------------------------------------------------
MODULO_PROBABILIDADES PROC
    PUSH AX
    PUSH BX
    PUSH CX
    PUSH DX
    
    ; El módulo para probabilidades usa el mismo algoritmo
    ; pero garantiza que el resultado esté en [0.0, 1.0]
    
    ; Convertir a enteros para módulo
    CALL CONVERTIR_PROBABILIDADES_A_ENTEROS
    
    ; Realizar módulo entero
    MOV AX, BX              ; BX = valor1 * 1000
    MOV CX, DX              ; DX = valor2 * 1000
    
    XOR DX, DX
    DIV CX                  ; AX = cociente, DX = resto
    
    ; El resto (DX) es nuestro resultado
    MOV AX, DX
    CALL CONVERTIR_ENTERO_A_PROBABILIDAD
    
    ; El resultado es siempre positivo y < divisor
    MOV [resultado_negativo], 0
    
    ; Por definición del módulo, debería estar en rango, pero verificamos
    CALL VERIFICAR_Y_AJUSTAR_RESULTADO
    
    POP DX
    POP CX
    POP BX
    POP AX
    RET
MODULO_PROBABILIDADES ENDP

OPCION_COMPARACIONES:
    CALL NUEVA_LINEA
    CALL LEER_DOS_PROBABILIDADES
    
    ; Comparar MENOR QUE (<)
    CALL NUEVA_LINEA
    MOV AH, 09h
    LEA DX, msg_menor
    INT 21h
    
    CALL COMPARAR_PROBABILIDADES_MENOR
    MOV AH, 09h
    JZ @CREATIV_COMP_MENOR_TRUE
    LEA DX, valor_false
    JMP @CREATIV_SHOW_MENOR
@CREATIV_COMP_MENOR_TRUE:
    LEA DX, valor_true
@CREATIV_SHOW_MENOR:
    INT 21h
    CALL NUEVA_LINEA
    
    ; Comparar MAYOR QUE (>)
    MOV AH, 09h
    LEA DX, msg_mayor
    INT 21h
    
    CALL COMPARAR_PROBABILIDADES_MAYOR
    MOV AH, 09h
    JZ @CREATIV_COMP_MAYOR_TRUE
    LEA DX, valor_false
    JMP @CREATIV_SHOW_MAYOR
@CREATIV_COMP_MAYOR_TRUE:
    LEA DX, valor_true
@CREATIV_SHOW_MAYOR:
    INT 21h
    CALL NUEVA_LINEA
    
    ; Comparar MENOR O IGUAL QUE (<=)
    MOV AH, 09h
    LEA DX, msg_menig
    INT 21h
    
    CALL COMPARAR_PROBABILIDADES_MENOR_IGUAL
    MOV AH, 09h
    JZ @CREATIV_COMP_MENIG_TRUE
    LEA DX, valor_false
    JMP @CREATIV_SHOW_MENIG
@CREATIV_COMP_MENIG_TRUE:
    LEA DX, valor_true
@CREATIV_SHOW_MENIG:
    INT 21h
    CALL NUEVA_LINEA
    
    ; Comparar MAYOR O IGUAL QUE (>=)
    MOV AH, 09h
    LEA DX, msg_mayig
    INT 21h
    
    CALL COMPARAR_PROBABILIDADES_MAYOR_IGUAL
    MOV AH, 09h
    JZ @CREATIV_COMP_MAYIG_TRUE
    LEA DX, valor_false
    JMP @CREATIV_SHOW_MAYIG
@CREATIV_COMP_MAYIG_TRUE:
    LEA DX, valor_true
@CREATIV_SHOW_MAYIG:
    INT 21h
    CALL NUEVA_LINEA
    
    ; Comparar IGUAL A (is)
    MOV AH, 09h
    LEA DX, msg_igual
    INT 21h
    
    CALL COMPARAR_PROBABILIDADES_IGUAL
    MOV AH, 09h
    JZ @CREATIV_COMP_IGUAL_TRUE
    LEA DX, valor_false
    JMP @CREATIV_SHOW_IGUAL
@CREATIV_COMP_IGUAL_TRUE:
    LEA DX, valor_true
@CREATIV_SHOW_IGUAL:
    INT 21h
    CALL NUEVA_LINEA
    
    ; Comparar DISTINTO DE (isNot)
    MOV AH, 09h
    LEA DX, msg_nig
    INT 21h
    
    CALL COMPARAR_PROBABILIDADES_DISTINTO
    MOV AH, 09h
    JZ @CREATIV_COMP_DISTINTO_TRUE
    LEA DX, valor_false
    JMP @CREATIV_SHOW_DISTINTO
@CREATIV_COMP_DISTINTO_TRUE:
    LEA DX, valor_true
@CREATIV_SHOW_DISTINTO:
    INT 21h
    
    CALL NUEVA_LINEA
    JMP MENU_PRINCIPAL

OPCION_CONVERSIONES:
    CALL NUEVA_LINEA
    
    ; Leer una probabilidad para convertir
    MOV AH, 09h
    LEA DX, prompt_prob1
    INT 21h
    
    MOV AH, 0Ah
    LEA DX, buffer1
    INT 21h
    
    ; Procesar la probabilidad
    CALL PROCESAR_PRIMERA_PROBABILIDAD
    
    ; Validar rango
    CALL VALIDAR_RANGO_PRIMERA
    JC @CREATIV_CONV_ERROR_RANGO
    
    ; Realizar todas las conversiones
    CALL PROBABILIDAD_A_INTEGER     ; A Stack (entero)
    CALL PROBABILIDAD_A_BOOLEAN     ; A Torch (booleano)
    CALL PROBABILIDAD_A_CHAR        ; A Rune (caracter)
    CALL PROBABILIDAD_A_STRING      ; A Spider (string)
    CALL PROBABILIDAD_A_FLOAT       ; A Ghast (flotante)
    
    ; Mostrar todas las conversiones
    CALL MOSTRAR_CONVERSIONES_PROBABILIDAD
    
    JMP MENU_PRINCIPAL

@CREATIV_CONV_ERROR_RANGO:
    MOV AH, 09h
    LEA DX, error_rango
    INT 21h
    JMP MENU_PRINCIPAL

;------------------------------------------------------------
; Procedimiento: PROCESAR_PRIMERA_PROBABILIDAD
; Procesa la primera probabilidad del buffer1
;------------------------------------------------------------
PROCESAR_PRIMERA_PROBABILIDAD PROC
    PUSH AX
    PUSH BX
    PUSH CX
    PUSH DX
    PUSH SI
    
    ; Inicializar variables de la primera probabilidad
    MOV [entero1], 0
    MOV [decimal1], 0
    MOV [dec_digitos1], 0
    MOV [es_negativo1], 0
    
    ; Obtener longitud y puntero
    MOV BL, [buffer1+1]
    XOR BH, BH
    LEA SI, [buffer1+2]
    
    ; Verificar si está vacío
    CMP BX, 0
    JE @CREATIV_PROC1_FIN
    
    ; Verificar signo negativo
    MOV CL, [SI]
    CMP CL, '-'
    JNE @CREATIV_PROC1_ENTERO
    
    MOV [es_negativo1], 1
    INC SI
    DEC BX
    
@CREATIV_PROC1_ENTERO:
    CMP BX, 0
    JE @CREATIV_PROC1_FIN
    
    MOV CL, [SI]
    INC SI
    DEC BX
    
    CMP CL, '.'
    JE @CREATIV_PROC1_DECIMAL
    
    ; Verificar si es dígito
    CMP CL, '0'
    JL @CREATIV_PROC1_ENTERO
    CMP CL, '9'
    JG @CREATIV_PROC1_ENTERO
    
    SUB CL, '0'
    XOR CH, CH
    
    ; entero1 = entero1 * 10 + dígito
    MOV AX, [entero1]
    MOV DX, 10
    MUL DX
    ADD AX, CX
    MOV [entero1], AX
    
    JMP @CREATIV_PROC1_ENTERO
    
@CREATIV_PROC1_DECIMAL:
    CMP BX, 0
    JE @CREATIV_PROC1_FIN
    
    MOV CL, [SI]
    INC SI
    DEC BX
    
    ; Verificar si es dígito
    CMP CL, '0'
    JL @CREATIV_PROC1_DECIMAL
    CMP CL, '9'
    JG @CREATIV_PROC1_DECIMAL
    
    SUB CL, '0'
    XOR CH, CH
    
    ; decimal1 = decimal1 * 10 + dígito
    MOV AX, [decimal1]
    MOV DX, 10
    MUL DX
    ADD AX, CX
    MOV [decimal1], AX
    
    ; Incrementar contador de dígitos decimales
    INC [dec_digitos1]
    
    JMP @CREATIV_PROC1_DECIMAL
    
@CREATIV_PROC1_FIN:
    POP SI
    POP DX
    POP CX
    POP BX
    POP AX
    RET
PROCESAR_PRIMERA_PROBABILIDAD ENDP

;------------------------------------------------------------
; Procedimiento: PROCESAR_SEGUNDA_PROBABILIDAD
; Procesa la segunda probabilidad del buffer2 (similar al primero)
;------------------------------------------------------------
PROCESAR_SEGUNDA_PROBABILIDAD PROC
    PUSH AX
    PUSH BX
    PUSH CX
    PUSH DX
    PUSH SI
    
    ; Inicializar variables de la segunda probabilidad
    MOV [entero2], 0
    MOV [decimal2], 0
    MOV [dec_digitos2], 0
    MOV [es_negativo2], 0
    
    ; Obtener longitud y puntero
    MOV BL, [buffer2+1]
    XOR BH, BH
    LEA SI, [buffer2+2]
    
    ; Verificar si está vacío
    CMP BX, 0
    JE @CREATIV_PROC2_FIN
    
    ; Verificar signo negativo
    MOV CL, [SI]
    CMP CL, '-'
    JNE @CREATIV_PROC2_ENTERO
    
    MOV [es_negativo2], 1
    INC SI
    DEC BX
    
@CREATIV_PROC2_ENTERO:
    CMP BX, 0
    JE @CREATIV_PROC2_FIN
    
    MOV CL, [SI]
    INC SI
    DEC BX
    
    CMP CL, '.'
    JE @CREATIV_PROC2_DECIMAL
    
    ; Verificar si es dígito
    CMP CL, '0'
    JL @CREATIV_PROC2_ENTERO
    CMP CL, '9'
    JG @CREATIV_PROC2_ENTERO
    
    SUB CL, '0'
    XOR CH, CH
    
    ; entero2 = entero2 * 10 + dígito
    MOV AX, [entero2]
    MOV DX, 10
    MUL DX
    ADD AX, CX
    MOV [entero2], AX
    
    JMP @CREATIV_PROC2_ENTERO
    
@CREATIV_PROC2_DECIMAL:
    CMP BX, 0
    JE @CREATIV_PROC2_FIN
    
    MOV CL, [SI]
    INC SI
    DEC BX
    
    ; Verificar si es dígito
    CMP CL, '0'
    JL @CREATIV_PROC2_DECIMAL
    CMP CL, '9'
    JG @CREATIV_PROC2_DECIMAL
    
    SUB CL, '0'
    XOR CH, CH
    
    ; decimal2 = decimal2 * 10 + dígito
    MOV AX, [decimal2]
    MOV DX, 10
    MUL DX
    ADD AX, CX
    MOV [decimal2], AX
    
    ; Incrementar contador de dígitos decimales
    INC [dec_digitos2]
    
    JMP @CREATIV_PROC2_DECIMAL
    
@CREATIV_PROC2_FIN:
    POP SI
    POP DX
    POP CX
    POP BX
    POP AX
    RET
PROCESAR_SEGUNDA_PROBABILIDAD ENDP

;------------------------------------------------------------
; Procedimiento: VALIDAR_RANGO_PRIMERA
; Valida que la primera probabilidad esté entre 0.0 y 1.0
; Salida: CF=1 si está fuera de rango, CF=0 si está en rango
;------------------------------------------------------------
VALIDAR_RANGO_PRIMERA PROC
    PUSH AX
    
    ; Verificar si es negativo
    CMP [es_negativo1], 1
    JE @CREATIV_VAL1_FUERA_RANGO
    
    ; Verificar parte entera
    MOV AX, [entero1]
    CMP AX, 0
    JE @CREATIV_VAL1_RANGO_OK       ; Si es 0.x, está en rango
    CMP AX, 1
    JE @CREATIV_VAL1_VERIFICAR_DEC  ; Si es 1.x, verificar que sea 1.0
    JMP @CREATIV_VAL1_FUERA_RANGO   ; Si es > 1, fuera de rango
    
@CREATIV_VAL1_VERIFICAR_DEC:
    ; Si es 1.x, la parte decimal debe ser 0
    CMP WORD PTR [decimal1], 0
    JNE @CREATIV_VAL1_FUERA_RANGO
    
@CREATIV_VAL1_RANGO_OK:
    CLC                             ; CF=0, en rango
    JMP @CREATIV_VAL1_FIN
    
@CREATIV_VAL1_FUERA_RANGO:
    STC                             ; CF=1, fuera de rango
    
@CREATIV_VAL1_FIN:
    POP AX
    RET
VALIDAR_RANGO_PRIMERA ENDP

;------------------------------------------------------------
; Procedimiento: VALIDAR_RANGO_SEGUNDA
; Valida que la segunda probabilidad esté entre 0.0 y 1.0
; Salida: CF=1 si está fuera de rango, CF=0 si está en rango
;------------------------------------------------------------
VALIDAR_RANGO_SEGUNDA PROC
    PUSH AX
    
    ; Verificar si es negativo
    CMP [es_negativo2], 1
    JE @CREATIV_VAL2_FUERA_RANGO
    
    ; Verificar parte entera
    MOV AX, [entero2]
    CMP AX, 0
    JE @CREATIV_VAL2_RANGO_OK       ; Si es 0.x, está en rango
    CMP AX, 1
    JE @CREATIV_VAL2_VERIFICAR_DEC  ; Si es 1.x, verificar que sea 1.0
    JMP @CREATIV_VAL2_FUERA_RANGO   ; Si es > 1, fuera de rango
    
@CREATIV_VAL2_VERIFICAR_DEC:
    ; Si es 1.x, la parte decimal debe ser 0
    CMP WORD PTR [decimal2], 0
    JNE @CREATIV_VAL2_FUERA_RANGO
    
@CREATIV_VAL2_RANGO_OK:
    CLC                             ; CF=0, en rango
    JMP @CREATIV_VAL2_FIN
    
@CREATIV_VAL2_FUERA_RANGO:
    STC                             ; CF=1, fuera de rango
    
@CREATIV_VAL2_FIN:
    POP AX
    RET
VALIDAR_RANGO_SEGUNDA ENDP

;------------------------------------------------------------
; Procedimiento: VERIFICAR_CERO_SEGUNDA_PROBABILIDAD
; Verifica si la segunda probabilidad es cero
; Salida: CF=1 si es cero, CF=0 si no es cero
;------------------------------------------------------------
VERIFICAR_CERO_SEGUNDA_PROBABILIDAD PROC
    PUSH AX
    
    ; Verificar si entero2 es cero Y decimal2 es cero
    CMP WORD PTR [entero2], 0
    JNE @CREATIV_VERIF_NO_CERO
    CMP WORD PTR [decimal2], 0
    JNE @CREATIV_VERIF_NO_CERO
    
    STC  ; Es cero - establecer Carry Flag
    JMP @CREATIV_VERIF_FIN
    
@CREATIV_VERIF_NO_CERO:
    CLC  ; No es cero - limpiar Carry Flag
    
@CREATIV_VERIF_FIN:
    POP AX
    RET
VERIFICAR_CERO_SEGUNDA_PROBABILIDAD ENDP

;------------------------------------------------------------
; Procedimiento: VERIFICAR_Y_AJUSTAR_RESULTADO
; Verifica que el resultado esté en [0.0, 1.0] y ajusta si es necesario
;------------------------------------------------------------
VERIFICAR_Y_AJUSTAR_RESULTADO PROC
    PUSH AX
    
    ; Inicializar bandera de ajuste
    MOV [resultado_clamped], 0
    
    ; Verificar si es negativo (no válido para probabilidades)
    CMP [resultado_negativo], 1
    JE @CREATIV_AJUSTAR_A_CERO
    
    ; Verificar si excede 1.0
    MOV AX, [resultado_entero]
    CMP AX, 1
    JL @CREATIV_RESULTADO_OK        ; Si < 1, está en rango
    JE @CREATIV_VERIFICAR_DECIMAL   ; Si = 1, verificar decimal
    JMP @CREATIV_AJUSTAR_A_UNO      ; Si > 1, ajustar a 1.0
    
@CREATIV_VERIFICAR_DECIMAL:
    ; Si entero = 1, verificar que decimal = 0
    CMP WORD PTR [resultado_decimal], 0
    JE @CREATIV_RESULTADO_OK        ; 1.0 es válido
    JMP @CREATIV_AJUSTAR_A_UNO      ; 1.x > 1.0, ajustar
    
@CREATIV_AJUSTAR_A_CERO:
    ; Ajustar a 0.0
    MOV [resultado_entero], 0
    MOV [resultado_decimal], 0
    MOV [resultado_negativo], 0
    MOV [resultado_clamped], 1
    JMP @CREATIV_VERIFICAR_FIN
    
@CREATIV_AJUSTAR_A_UNO:
    ; Ajustar a 1.0
    MOV [resultado_entero], 1
    MOV [resultado_decimal], 0
    MOV [resultado_negativo], 0
    MOV [resultado_clamped], 1
    JMP @CREATIV_VERIFICAR_FIN
    
@CREATIV_RESULTADO_OK:
    ; El resultado está en rango válido
    
@CREATIV_VERIFICAR_FIN:
    POP AX
    RET
VERIFICAR_Y_AJUSTAR_RESULTADO ENDP

;------------------------------------------------------------
; Procedimiento: NORMALIZAR_DECIMALES_PARA_OPERACION
; Normaliza ambos decimales al mayor número de dígitos
;------------------------------------------------------------
NORMALIZAR_DECIMALES_PARA_OPERACION PROC
    PUSH AX
    PUSH BX
    PUSH CX
    PUSH DX
    
    ; Determinar el máximo número de dígitos decimales
    MOV AL, [dec_digitos1]
    MOV BL, [dec_digitos2]
    CMP AL, BL
    JAE @CREATIV_NORM_MAX_ES_DIG1
    MOV AL, BL
    
@CREATIV_NORM_MAX_ES_DIG1:
    MOV [resultado_digitos], AL
    
    ; Normalizar primer número
    MOV CL, [dec_digitos1]
    MOV CH, AL
    SUB CH, CL
    JZ @CREATIV_NORM_NUM2  ; Ya tiene los dígitos necesarios
    
    MOV AX, [decimal1]
    MOV BX, 10
@CREATIV_NORM_LOOP1:
    MUL BX
    DEC CH
    JNZ @CREATIV_NORM_LOOP1
    MOV [decimal1], AX
    MOV AL, [resultado_digitos]
    MOV [dec_digitos1], AL
    
@CREATIV_NORM_NUM2:
    ; Normalizar segundo número
    MOV CL, [dec_digitos2]
    MOV CH, [resultado_digitos]
    SUB CH, CL
    JZ @CREATIV_NORM_FIN
    
    MOV AX, [decimal2]
    MOV BX, 10
@CREATIV_NORM_LOOP2:
    MUL BX
    DEC CH
    JNZ @CREATIV_NORM_LOOP2
    MOV [decimal2], AX
    MOV AL, [resultado_digitos]
    MOV [dec_digitos2], AL
    
@CREATIV_NORM_FIN:
    POP DX
    POP CX
    POP BX
    POP AX
    RET
NORMALIZAR_DECIMALES_PARA_OPERACION ENDP

;------------------------------------------------------------
; Procedimiento: SUMAR_VALORES_ABSOLUTOS
; Suma los valores absolutos de dos probabilidades
;------------------------------------------------------------
SUMAR_VALORES_ABSOLUTOS PROC
    PUSH AX
    PUSH BX
    PUSH CX
    PUSH DX
    
    ; Para probabilidades, siempre son positivas, así que sumamos directamente
    
    ; Sumar partes decimales
    MOV AX, [decimal1]
    ADD AX, [decimal2]
    
    ; Calcular la base para verificar acarreo
    MOV DL, [resultado_digitos]
    CALL CALCULAR_POTENCIA_10_DL
    ; BX contiene 10^digitos (base decimal)
    
    MOV DX, BX              ; DX = base decimal
    
    ; Verificar acarreo en decimales
    XOR DI, DI              ; DI = acarreo (0 inicialmente)
    CMP AX, DX
    JL @CREATIV_SUMA_SIN_ACARREO
    
    SUB AX, DX              ; Ajustar decimal
    MOV DI, 1               ; Hay acarreo
    
@CREATIV_SUMA_SIN_ACARREO:
    MOV [resultado_decimal], AX
    
    ; Sumar partes enteras + acarreo
    MOV AX, [entero1]
    ADD AX, [entero2]
    ADD AX, DI              ; AX = suma + acarreo
    MOV [resultado_entero], AX
    
    POP DX
    POP CX
    POP BX
    POP AX
    RET
SUMAR_VALORES_ABSOLUTOS ENDP

;------------------------------------------------------------
; Procedimiento: COMPARAR_PROBABILIDADES_ABSOLUTO
; Compara cuál probabilidad es mayor en valor absoluto
; Salida: CF=1 si segunda > primera, CF=0 si primera >= segunda
;------------------------------------------------------------
COMPARAR_PROBABILIDADES_ABSOLUTO PROC
    PUSH AX
    PUSH BX
    
    ; Normalizar decimales para comparación justa
    CALL NORMALIZAR_DECIMALES_PARA_OPERACION
    
    ; Comparar partes enteras
    MOV AX, [entero1]
    MOV BX, [entero2]
    
    CMP AX, BX
    JG @CREATIV_COMP_ABS_PRIMERA_MAYOR  ; primera > segunda
    JL @CREATIV_COMP_ABS_SEGUNDA_MAYOR  ; primera < segunda
    
    ; Partes enteras iguales, comparar decimales
    MOV AX, [decimal1]
    MOV BX, [decimal2]
    CMP AX, BX
    JGE @CREATIV_COMP_ABS_PRIMERA_MAYOR ; primera >= segunda
    
@CREATIV_COMP_ABS_SEGUNDA_MAYOR:
    STC  ; CF=1, segunda es mayor
    JMP @CREATIV_COMP_ABS_FIN
    
@CREATIV_COMP_ABS_PRIMERA_MAYOR:
    CLC  ; CF=0, primera es mayor o igual
    
@CREATIV_COMP_ABS_FIN:
    POP BX
    POP AX
    RET
COMPARAR_PROBABILIDADES_ABSOLUTO ENDP

;------------------------------------------------------------
; Procedimiento: RESTAR_PRIMERA_MENOS_SEGUNDA
; Resta primera - segunda (asume primera >= segunda)
;------------------------------------------------------------
RESTAR_PRIMERA_MENOS_SEGUNDA PROC
    PUSH AX
    PUSH BX
    PUSH CX
    PUSH DX
    
    ; Restar partes decimales
    MOV AX, [decimal1]
    SUB AX, [decimal2]
    
    ; Verificar si necesitamos pedir prestado
    CMP AX, 0
    JGE @CREATIV_RESTA_DEC_OK
    
    ; Pedir prestado de la parte entera
    DEC WORD PTR [entero1]
    
    ; Calcular base decimal para ajustar
    MOV BL, [resultado_digitos]
    CALL CALCULAR_POTENCIA_10_BL
    ADD AX, BX
    
@CREATIV_RESTA_DEC_OK:
    MOV [resultado_decimal], AX
    
    ; Restar partes enteras
    MOV AX, [entero1]
    SUB AX, [entero2]
    MOV [resultado_entero], AX
    
    ; Restaurar valor original de entero1 si fue modificado
    ; (para futuras operaciones en la misma sesión)
    MOV AX, [resultado_decimal]
    CMP AX, [decimal1]
    JGE @CREATIV_RESTA_NO_PRESTAMO
    INC WORD PTR [entero1]  ; Restaurar si hubo préstamo
    
@CREATIV_RESTA_NO_PRESTAMO:
    
    POP DX
    POP CX
    POP BX
    POP AX
    RET
RESTAR_PRIMERA_MENOS_SEGUNDA ENDP

;------------------------------------------------------------
; Procedimiento: MULTIPLICAR_VALORES_PROBABILIDAD
; Multiplica dos valores de probabilidad
;------------------------------------------------------------
MULTIPLICAR_VALORES_PROBABILIDAD PROC
    PUSH AX
    PUSH BX
    PUSH CX
    PUSH DX
    
    ; Para probabilidades, usamos método simplificado
    ; (a.bc) * (d.ef) ≈ (a*100 + bc) * (d*100 + ef) / 10000
    
    ; Convertir primera probabilidad a entero
    MOV AX, [entero1]
    MOV BX, 100
    MUL BX              ; AX = entero1 * 100
    ADD AX, [decimal1]  ; AX = entero1*100 + decimal1
    MOV BX, AX          ; BX = primera probabilidad como entero
    
    ; Convertir segunda probabilidad a entero
    MOV AX, [entero2]
    MOV CX, 100
    MUL CX              ; AX = entero2 * 100
    ADD AX, [decimal2]  ; AX = entero2*100 + decimal2
    MOV CX, AX          ; CX = segunda probabilidad como entero
    
    ; Multiplicar
    MOV AX, BX
    MUL CX              ; DX:AX = resultado * 10000
    
    ; Dividir por 10000 para obtener el resultado correcto
    MOV BX, 10000
    DIV BX              ; AX = parte entera, DX = resto
    
    MOV [resultado_entero], AX
    
    ; Convertir resto a parte decimal
    MOV AX, DX
    MOV BX, 100
    MUL BX              ; AX = resto * 100
    MOV BX, 10000
    DIV BX              ; AX = parte decimal
    MOV [resultado_decimal], AX
    
    MOV [resultado_digitos], 2  ; Usar 2 dígitos decimales
    
    POP DX
    POP CX
    POP BX
    POP AX
    RET
MULTIPLICAR_VALORES_PROBABILIDAD ENDP

;------------------------------------------------------------
; Procedimiento: CALCULAR_POTENCIA_10_DL
; Calcula 10^DL y retorna en BX
;------------------------------------------------------------
CALCULAR_POTENCIA_10_DL PROC
    PUSH AX
    PUSH CX
    
    MOV BX, 1               ; Resultado inicial
    XOR DH, DH              ; Limpiar DH
    MOV CL, DL              ; CL = exponente
    
    CMP CL, 0
    JE @CREATIV_POT_DL_FIN
    
@CREATIV_POT_DL_LOOP:
    PUSH CX
    MOV AX, BX
    MOV CX, 10
    MUL CX                  ; AX = BX * 10
    MOV BX, AX              ; BX = resultado
    POP CX
    DEC CL
    JNZ @CREATIV_POT_DL_LOOP
    
@CREATIV_POT_DL_FIN:
    ; BX contiene 10^DL
    POP CX
    POP AX
    RET
CALCULAR_POTENCIA_10_DL ENDP

;------------------------------------------------------------
; Procedimiento: CALCULAR_POTENCIA_10_BL
; Calcula 10^BL y retorna en BX
;------------------------------------------------------------
CALCULAR_POTENCIA_10_BL PROC
    PUSH AX
    PUSH CX
    
    MOV CX, BX              ; Guardar BX original
    MOV BX, 1
    MOV CL, BL
    XOR CH, CH
    CMP CL, 0
    JE @CREATIV_POT_BL_FIN
    
@CREATIV_POT_BL_LOOP:
    MOV AX, BX
    MOV BX, 10
    MUL BX
    MOV BX, AX
    LOOP @CREATIV_POT_BL_LOOP
    
@CREATIV_POT_BL_FIN:
    POP CX
    POP AX
    RET
CALCULAR_POTENCIA_10_BL ENDP

;------------------------------------------------------------
; PROCEDIMIENTOS DE COMPARACIÓN PARA PROBABILIDADES
; Todos los procedimientos comparan probabilidad1 con probabilidad2
; y devuelven el resultado en ZF (Zero Flag)
;------------------------------------------------------------

;------------------------------------------------------------
; Procedimiento: COMPARAR_PROBABILIDADES_MENOR
; Compara si probabilidad1 < probabilidad2
; Salida: ZF=1 si es verdadero, ZF=0 si es falso
;------------------------------------------------------------
COMPARAR_PROBABILIDADES_MENOR PROC
    PUSH AX
    PUSH BX
    
    ; Normalizar decimales para comparación justa
    CALL NORMALIZAR_DECIMALES_PARA_OPERACION
    
    ; Comparar partes enteras primero
    MOV AX, [entero1]
    MOV BX, [entero2]
    
    CMP AX, BX
    JL @CREATIV_MENOR_VERDADERO     ; entero1 < entero2
    JG @CREATIV_MENOR_FALSO         ; entero1 > entero2
    
    ; Partes enteras iguales, comparar decimales
    MOV AX, [decimal1]
    MOV BX, [decimal2]
    CMP AX, BX
    JL @CREATIV_MENOR_VERDADERO     ; decimal1 < decimal2
    JMP @CREATIV_MENOR_FALSO        ; decimal1 >= decimal2
    
@CREATIV_MENOR_VERDADERO:
    XOR AX, AX
    CMP AX, AX  ; ZF=1 (verdadero)
    JMP @CREATIV_MENOR_FIN
    
@CREATIV_MENOR_FALSO:
    MOV AX, 1
    CMP AX, 0   ; ZF=0 (falso)
    
@CREATIV_MENOR_FIN:
    POP BX
    POP AX
    RET
COMPARAR_PROBABILIDADES_MENOR ENDP

;------------------------------------------------------------
; Procedimiento: COMPARAR_PROBABILIDADES_MAYOR
; Compara si probabilidad1 > probabilidad2
; Salida: ZF=1 si es verdadero, ZF=0 si es falso
;------------------------------------------------------------
COMPARAR_PROBABILIDADES_MAYOR PROC
    PUSH AX
    PUSH BX
    
    ; Normalizar decimales para comparación justa
    CALL NORMALIZAR_DECIMALES_PARA_OPERACION
    
    ; Comparar partes enteras primero
    MOV AX, [entero1]
    MOV BX, [entero2]
    
    CMP AX, BX
    JG @CREATIV_MAYOR_VERDADERO     ; entero1 > entero2
    JL @CREATIV_MAYOR_FALSO         ; entero1 < entero2
    
    ; Partes enteras iguales, comparar decimales
    MOV AX, [decimal1]
    MOV BX, [decimal2]
    CMP AX, BX
    JG @CREATIV_MAYOR_VERDADERO     ; decimal1 > decimal2
    JMP @CREATIV_MAYOR_FALSO        ; decimal1 <= decimal2
    
@CREATIV_MAYOR_VERDADERO:
    XOR AX, AX
    CMP AX, AX  ; ZF=1 (verdadero)
    JMP @CREATIV_MAYOR_FIN
    
@CREATIV_MAYOR_FALSO:
    MOV AX, 1
    CMP AX, 0   ; ZF=0 (falso)
    
@CREATIV_MAYOR_FIN:
    POP BX
    POP AX
    RET
COMPARAR_PROBABILIDADES_MAYOR ENDP

;------------------------------------------------------------
; Procedimiento: COMPARAR_PROBABILIDADES_IGUAL
; Compara si probabilidad1 == probabilidad2
; Salida: ZF=1 si son iguales, ZF=0 si son diferentes
;------------------------------------------------------------
COMPARAR_PROBABILIDADES_IGUAL PROC
    PUSH AX
    PUSH BX
    
    ; Normalizar decimales para comparación justa
    CALL NORMALIZAR_DECIMALES_PARA_OPERACION
    
    ; Comparar partes enteras
    MOV AX, [entero1]
    MOV BX, [entero2]
    CMP AX, BX
    JNE @CREATIV_IGUAL_FALSO
    
    ; Partes enteras iguales, comparar decimales
    MOV AX, [decimal1]
    MOV BX, [decimal2]
    CMP AX, BX
    JE @CREATIV_IGUAL_VERDADERO
    
@CREATIV_IGUAL_FALSO:
    MOV AX, 0
    CMP AX, 1  ; ZF=0 (diferentes)
    JMP @CREATIV_IGUAL_FIN
    
@CREATIV_IGUAL_VERDADERO:
    MOV AX, 1
    CMP AX, 1  ; ZF=1 (iguales)
    
@CREATIV_IGUAL_FIN:
    POP BX
    POP AX
    RET
COMPARAR_PROBABILIDADES_IGUAL ENDP

;------------------------------------------------------------
; Procedimiento: COMPARAR_PROBABILIDADES_DISTINTO
; Compara si probabilidad1 != probabilidad2
; Salida: ZF=1 si son diferentes, ZF=0 si son iguales
;------------------------------------------------------------
COMPARAR_PROBABILIDADES_DISTINTO PROC
    CALL COMPARAR_PROBABILIDADES_IGUAL
    
    ; Invertir el resultado
    JZ @CREATIV_DIST_ERAN_IGUALES
    
    ; Eran diferentes, devolver verdadero
    MOV AX, 1
    CMP AX, 1  ; ZF=1 (verdadero - son diferentes)
    JMP @CREATIV_DIST_FIN
    
@CREATIV_DIST_ERAN_IGUALES:
    ; Eran iguales, devolver falso
    MOV AX, 0
    CMP AX, 1  ; ZF=0 (falso - no son diferentes)
    
@CREATIV_DIST_FIN:
    RET
COMPARAR_PROBABILIDADES_DISTINTO ENDP

;------------------------------------------------------------
; Procedimiento: COMPARAR_PROBABILIDADES_MENOR_IGUAL
; Compara si probabilidad1 <= probabilidad2
; Salida: ZF=1 si es verdadero, ZF=0 si es falso
;------------------------------------------------------------
COMPARAR_PROBABILIDADES_MENOR_IGUAL PROC
    ; A <= B es equivalente a (A < B) OR (A == B)
    
    CALL COMPARAR_PROBABILIDADES_MENOR
    JZ @CREATIV_MENIG_ES_MENOR  ; Si ZF=1, es menor
    
    ; No es menor, verificar si es igual
    CALL COMPARAR_PROBABILIDADES_IGUAL
    JMP @CREATIV_MENIG_FIN
    
@CREATIV_MENIG_ES_MENOR:
    ; Es menor, por tanto es menor o igual (ZF ya está en 1)
    
@CREATIV_MENIG_FIN:
    RET
COMPARAR_PROBABILIDADES_MENOR_IGUAL ENDP

;------------------------------------------------------------
; Procedimiento: COMPARAR_PROBABILIDADES_MAYOR_IGUAL
; Compara si probabilidad1 >= probabilidad2
; Salida: ZF=1 si es verdadero, ZF=0 si es falso
;------------------------------------------------------------
COMPARAR_PROBABILIDADES_MAYOR_IGUAL PROC
    ; A >= B es equivalente a (A > B) OR (A == B)
    
    CALL COMPARAR_PROBABILIDADES_MAYOR
    JZ @CREATIV_MAYIG_ES_MAYOR  ; Si ZF=1, es mayor
    
    ; No es mayor, verificar si es igual
    CALL COMPARAR_PROBABILIDADES_IGUAL
    JMP @CREATIV_MAYIG_FIN
    
@CREATIV_MAYIG_ES_MAYOR:
    ; Es mayor, por tanto es mayor o igual (ZF ya está en 1)
    
@CREATIV_MAYIG_FIN:
    RET
COMPARAR_PROBABILIDADES_MAYOR_IGUAL ENDP

;------------------------------------------------------------
; Procedimiento: CONVERTIR_PROBABILIDADES_A_ENTEROS
; Convierte ambas probabilidades a enteros para operaciones
; Salida: BX = probabilidad1 * 1000, DX = probabilidad2 * 1000
;------------------------------------------------------------
CONVERTIR_PROBABILIDADES_A_ENTEROS PROC
    PUSH AX
    PUSH CX
    
    ; Convertir primera probabilidad: (entero1 * 1000) + (decimal1 * factor)
    MOV AX, [entero1]
    MOV CX, 1000
    MUL CX              ; AX = entero1 * 1000
    MOV BX, AX          ; BX = resultado parcial
    
    ; Normalizar decimal1 a 3 dígitos (para * 1000)
    MOV AX, [decimal1]
    MOV CL, [dec_digitos1]
    CMP CL, 3
    JE @CREATIV_CONV_DEC1_OK
    JL @CREATIV_CONV_DEC1_MULT
    
    ; Más de 3 dígitos, dividir para ajustar
    SUB CL, 3
@CREATIV_CONV_DEC1_DIV:
    MOV CX, 10
    XOR DX, DX
    DIV CX
    DEC BYTE PTR [dec_digitos1]
    MOV CL, [dec_digitos1]
    CMP CL, 3
    JG @CREATIV_CONV_DEC1_DIV
    JMP @CREATIV_CONV_DEC1_OK
    
@CREATIV_CONV_DEC1_MULT:
    ; Menos de 3 dígitos, multiplicar
    MOV CX, 10
    MUL CX
    INC BYTE PTR [dec_digitos1]
    MOV CL, [dec_digitos1]
    CMP CL, 3
    JL @CREATIV_CONV_DEC1_MULT
    
@CREATIV_CONV_DEC1_OK:
    ADD BX, AX          ; BX = (entero1 * 1000) + decimal1
    
    ; Convertir segunda probabilidad
    MOV AX, [entero2]
    MOV CX, 1000
    MUL CX              ; AX = entero2 * 1000
    MOV DX, AX          ; DX = resultado parcial
    
    ; Normalizar decimal2 de forma similar
    MOV AX, [decimal2]
    MOV CL, [dec_digitos2]
    CMP CL, 3
    JE @CREATIV_CONV_DEC2_OK
    JL @CREATIV_CONV_DEC2_MULT
    
    ; Más de 3 dígitos, dividir
    SUB CL, 3
@CREATIV_CONV_DEC2_DIV:
    PUSH DX
    MOV CX, 10
    XOR DX, DX
    DIV CX
    POP DX
    DEC BYTE PTR [dec_digitos2]
    MOV CL, [dec_digitos2]
    CMP CL, 3
    JG @CREATIV_CONV_DEC2_DIV
    JMP @CREATIV_CONV_DEC2_OK
    
@CREATIV_CONV_DEC2_MULT:
    ; Menos de 3 dígitos, multiplicar
    MOV CX, 10
    MUL CX
    INC BYTE PTR [dec_digitos2]
    MOV CL, [dec_digitos2]
    CMP CL, 3
    JL @CREATIV_CONV_DEC2_MULT
    
@CREATIV_CONV_DEC2_OK:
    ADD DX, AX          ; DX = (entero2 * 1000) + decimal2
    
    POP CX
    POP AX
    RET
CONVERTIR_PROBABILIDADES_A_ENTEROS ENDP

;------------------------------------------------------------
; Procedimiento: CONVERTIR_ENTERO_A_PROBABILIDAD
; Convierte un entero de vuelta a formato probabilidad
; Entrada: AX = valor entero (ej: 750 para 0.750)
;------------------------------------------------------------
CONVERTIR_ENTERO_A_PROBABILIDAD PROC
    PUSH BX
    PUSH DX
    
    ; Dividir AX por 1000 para obtener parte entera y decimal
    MOV BX, 1000
    XOR DX, DX
    DIV BX              ; AX = parte entera, DX = parte decimal
    
    MOV [resultado_entero], AX
    MOV [resultado_decimal], DX
    MOV [resultado_digitos], 3  ; 3 dígitos decimales
    
    POP DX
    POP BX
    RET
CONVERTIR_ENTERO_A_PROBABILIDAD ENDP

;------------------------------------------------------------
; Procedimiento: MOSTRAR_RESULTADO_PROBABILIDAD
; Muestra el resultado de una operación con probabilidades
;------------------------------------------------------------
MOSTRAR_RESULTADO_PROBABILIDAD PROC
    CALL NUEVA_LINEA
    
    ; Mostrar mensaje de advertencia si el resultado fue ajustado
    CMP [resultado_clamped], 1
    JNE @CREATIV_MOSTRAR_SIN_ADVERTENCIA
    
    MOV AH, 09h
    LEA DX, warn_clamp
    INT 21h
    
@CREATIV_MOSTRAR_SIN_ADVERTENCIA:
    MOV AH, 09h
    LEA DX, result_msg
    INT 21h
    
    ; Mostrar la probabilidad resultado
    CALL MOSTRAR_PROBABILIDAD_RESULTADO
    
    CALL NUEVA_LINEA
    CALL NUEVA_LINEA
    
    RET
MOSTRAR_RESULTADO_PROBABILIDAD ENDP

;------------------------------------------------------------
; Procedimiento: MOSTRAR_PROBABILIDAD_RESULTADO
; Muestra una probabilidad desde las variables de resultado
;------------------------------------------------------------
MOSTRAR_PROBABILIDAD_RESULTADO PROC
    PUSH AX
    PUSH BX
    PUSH CX
    PUSH DX
    
    ; Mostrar parte entera (siempre 0 o 1 para probabilidades)
    MOV AX, [resultado_entero]
    CALL MOSTRAR_NUMERO_POSITIVO
    
    ; Mostrar punto decimal
    MOV AH, 09h
    LEA DX, punto
    INT 21h
    
    ; Mostrar parte decimal
    CALL MOSTRAR_DECIMAL_RESULTADO_PROBABILIDAD
    
    POP DX
    POP CX
    POP BX
    POP AX
    RET
MOSTRAR_PROBABILIDAD_RESULTADO ENDP

;------------------------------------------------------------
; Procedimiento: MOSTRAR_DECIMAL_RESULTADO_PROBABILIDAD
; Muestra la parte decimal del resultado de probabilidad
;------------------------------------------------------------
MOSTRAR_DECIMAL_RESULTADO_PROBABILIDAD PROC
    PUSH AX
    PUSH BX
    PUSH CX
    PUSH DX
    
    ; Verificar si hay dígitos decimales
    CMP BYTE PTR [resultado_digitos], 0
    JNE @CREATIV_MOSTRAR_DEC_HAY
    
    ; No hay decimales, mostrar 0
    MOV DL, '0'
    MOV AH, 02h
    INT 21h
    JMP @CREATIV_MOSTRAR_DEC_FIN
    
@CREATIV_MOSTRAR_DEC_HAY:
    ; Para probabilidades, asegurar al menos 2 dígitos decimales
    XOR CH, CH
    MOV CL, [resultado_digitos]
    CMP CL, 2
    JGE @CREATIV_DEC_DIGITOS_OK
    MOV CL, 2  ; Mínimo 2 dígitos para probabilidades
    
@CREATIV_DEC_DIGITOS_OK:
    MOV BX, CX  ; BX = total de dígitos necesarios
    
    ; Si resultado_decimal es 0, mostrar todos ceros
    CMP WORD PTR [resultado_decimal], 0
    JNE @CREATIV_MOSTRAR_DEC_NO_CERO
    
    MOV CX, BX
@CREATIV_MOSTRAR_DEC_SOLO_CEROS:
    MOV DL, '0'
    MOV AH, 02h
    INT 21h
    LOOP @CREATIV_MOSTRAR_DEC_SOLO_CEROS
    JMP @CREATIV_MOSTRAR_DEC_FIN
    
@CREATIV_MOSTRAR_DEC_NO_CERO:
    ; Contar dígitos reales en resultado_decimal
    MOV AX, [resultado_decimal]
    XOR CX, CX  ; Contador de dígitos reales
    PUSH BX     ; Guardar total de dígitos necesarios
    MOV BX, 10
    
@CREATIV_MOSTRAR_DEC_CONTAR:
    XOR DX, DX
    DIV BX
    INC CX
    CMP AX, 0
    JNE @CREATIV_MOSTRAR_DEC_CONTAR
    
    POP BX      ; Recuperar total de dígitos necesarios
    
    ; BX = dígitos necesarios, CX = dígitos reales
    ; Calcular ceros iniciales
    MOV AX, BX
    SUB AX, CX
    CMP AX, 0
    JLE @CREATIV_MOSTRAR_DEC_SIN_CEROS
    
    ; Mostrar ceros iniciales
    MOV CX, AX
@CREATIV_MOSTRAR_DEC_CEROS_INIT:
    MOV DL, '0'
    MOV AH, 02h
    INT 21h
    LOOP @CREATIV_MOSTRAR_DEC_CEROS_INIT
    
@CREATIV_MOSTRAR_DEC_SIN_CEROS:
    ; Mostrar dígitos reales
    MOV AX, [resultado_decimal]
    CALL MOSTRAR_NUMERO_POSITIVO
    
@CREATIV_MOSTRAR_DEC_FIN:
    POP DX
    POP CX
    POP BX
    POP AX
    RET
MOSTRAR_DECIMAL_RESULTADO_PROBABILIDAD ENDP

;------------------------------------------------------------
; Procedimiento: MOSTRAR_CONVERSIONES_PROBABILIDAD
; Muestra todas las conversiones de la probabilidad
;------------------------------------------------------------
MOSTRAR_CONVERSIONES_PROBABILIDAD PROC
    CALL NUEVA_LINEA
    
    ; Mostrar probabilidad original
    MOV AH, 09h
    LEA DX, prompt_conversiones_orig
    INT 21h
    
    ; Mostrar la probabilidad original usando entero1, decimal1, etc.
    CALL MOSTRAR_PROBABILIDAD_ORIGINAL
    
    CALL NUEVA_LINEA
    
    ; Mostrar conversión a entero (Stack)
    MOV AH, 09h
    LEA DX, prompt_conv_int
    INT 21h
    
    MOV AX, [int_valor]
    CALL MOSTRAR_NUMERO_POSITIVO
    
    CALL NUEVA_LINEA
    
    ; Mostrar conversión a booleano (Torch)
    MOV AH, 09h
    LEA DX, prompt_conv_bool
    INT 21h
    
    CMP [bool_valor], 0
    JE @CREATIV_CONV_BOOL_FALSE
    
    LEA DX, valor_true
    JMP @CREATIV_CONV_BOOL_MOSTRAR
    
@CREATIV_CONV_BOOL_FALSE:
    LEA DX, valor_false
    
@CREATIV_CONV_BOOL_MOSTRAR:
    MOV AH, 09h
    INT 21h
    
    CALL NUEVA_LINEA
    
    ; Mostrar conversión a caracter (Rune)
    MOV AH, 09h
    LEA DX, prompt_conv_char
    INT 21h
    
    MOV DL, [char_valor]
    MOV AH, 02h
    INT 21h
    
    CALL NUEVA_LINEA
    
    ; Mostrar conversión a string (Spider)
    MOV AH, 09h
    LEA DX, prompt_conv_str
    INT 21h
    
    LEA DX, string_buffer
    INT 21h
    
    CALL NUEVA_LINEA
    
    ; Mostrar conversión a flotante (Ghast)
    MOV AH, 09h
    LEA DX, prompt_conv_float
    INT 21h
    
    CALL MOSTRAR_PROBABILIDAD_COMO_FLOTANTE
    
    CALL NUEVA_LINEA
    
    RET
MOSTRAR_CONVERSIONES_PROBABILIDAD ENDP

;------------------------------------------------------------
; Procedimiento: MOSTRAR_PROBABILIDAD_ORIGINAL
; Muestra la probabilidad original usando las variables 1
;------------------------------------------------------------
MOSTRAR_PROBABILIDAD_ORIGINAL PROC
    PUSH AX
    PUSH BX
    PUSH CX
    PUSH DX
    
    ; Mostrar parte entera
    MOV AX, [entero1]
    CALL MOSTRAR_NUMERO_POSITIVO
    
    ; Mostrar punto decimal
    MOV AH, 09h
    LEA DX, punto
    INT 21h
    
    ; Mostrar parte decimal
    CMP BYTE PTR [dec_digitos1], 0
    JNE @CREATIV_ORIG_HAY_DECIMALES
    
    ; No hay decimales, mostrar 0
    MOV DL, '0'
    MOV AH, 02h
    INT 21h
    JMP @CREATIV_ORIG_FIN
    
@CREATIV_ORIG_HAY_DECIMALES:
    ; Mostrar decimales de la probabilidad original
    XOR CH, CH
    MOV CL, [dec_digitos1]
    
    CMP WORD PTR [decimal1], 0
    JNE @CREATIV_ORIG_DEC_NO_CERO
    
    ; decimal1 es 0, mostrar ceros
@CREATIV_ORIG_CEROS_LOOP:
    MOV DL, '0'
    MOV AH, 02h
    INT 21h
    LOOP @CREATIV_ORIG_CEROS_LOOP
    JMP @CREATIV_ORIG_FIN
    
@CREATIV_ORIG_DEC_NO_CERO:
    ; Mostrar valor real de decimal1 con ceros iniciales si es necesario
    MOV AX, [decimal1]
    CALL MOSTRAR_NUMERO_POSITIVO
    
@CREATIV_ORIG_FIN:
    POP DX
    POP CX
    POP BX
    POP AX
    RET
MOSTRAR_PROBABILIDAD_ORIGINAL ENDP

;------------------------------------------------------------
; Procedimiento: MOSTRAR_PROBABILIDAD_COMO_FLOTANTE
; Muestra la probabilidad convertida como flotante
;------------------------------------------------------------
MOSTRAR_PROBABILIDAD_COMO_FLOTANTE PROC
    PUSH AX
    
    ; Para mostrar como flotante, usar los valores convertidos
    MOV AX, [float_valor_ent]
    CALL MOSTRAR_NUMERO_POSITIVO
    
    MOV AH, 09h
    LEA DX, punto
    INT 21h
    
    MOV AX, [float_valor_dec]
    CALL MOSTRAR_NUMERO_POSITIVO
    
    POP AX
    RET
MOSTRAR_PROBABILIDAD_COMO_FLOTANTE ENDP

;------------------------------------------------------------
; Procedimiento: MOSTRAR_NUMERO_POSITIVO
; Muestra un número positivo en pantalla
; Entrada: AX = número a mostrar (debe ser positivo)
;------------------------------------------------------------
MOSTRAR_NUMERO_POSITIVO PROC
    PUSH AX
    PUSH BX
    PUSH CX
    PUSH DX
    
    ; Caso especial: cero
    CMP AX, 0
    JNE @CREATIV_POS_NO_CERO
    
    MOV DL, '0'
    MOV AH, 02h
    INT 21h
    JMP @CREATIV_POS_FIN
    
@CREATIV_POS_NO_CERO:
    ; Convertir a dígitos usando pila
    XOR CX, CX  ; Contador de dígitos
    MOV BX, 10  ; Divisor
    
@CREATIV_POS_DIV_LOOP:
    XOR DX, DX
    DIV BX      ; AX = AX / 10, DX = resto (dígito)
    PUSH DX     ; Guardar dígito en pila
    INC CX      ; Incrementar contador
    
    CMP AX, 0
    JNE @CREATIV_POS_DIV_LOOP
    
    ; Mostrar dígitos en orden correcto
@CREATIV_POS_MOSTRAR_LOOP:
    POP DX
    ADD DL, '0'
    MOV AH, 02h
    INT 21h
    LOOP @CREATIV_POS_MOSTRAR_LOOP
    
@CREATIV_POS_FIN:
    POP DX
    POP CX
    POP BX
    POP AX
    RET
MOSTRAR_NUMERO_POSITIVO ENDP

;------------------------------------------------------------
; PROCEDIMIENTOS DE CONVERSIÓN FALTANTES
; Estos procedimientos convierten probabilidades a otros tipos
;------------------------------------------------------------

;------------------------------------------------------------
; Procedimiento: PROBABILIDAD_A_INTEGER
; Convierte la probabilidad a entero (Stack)
; Multiplica por 100: 0.75 -> 75
;------------------------------------------------------------
PROBABILIDAD_A_INTEGER PROC
    PUSH AX
    PUSH BX
    
    ; Convertir probabilidad a entero multiplicando por 100
    ; (entero1 * 100) + decimal1 (asumiendo 2 dígitos decimales)
    MOV AX, [entero1]
    MOV BX, 100
    MUL BX              ; AX = entero1 * 100
    
    ; Normalizar decimal1 a 2 dígitos
    MOV BX, [decimal1]
    CMP [dec_digitos1], 2
    JE @CREATIV_INT_DEC_OK
    JL @CREATIV_INT_DEC_MENOS
    
    ; Más de 2 dígitos, tomar solo los primeros 2
    MOV CL, [dec_digitos1]
    SUB CL, 2
    XOR CH, CH
@CREATIV_INT_DEC_REDUCE:
    PUSH AX
    MOV AX, BX
    XOR DX, DX
    MOV BX, 10
    DIV BX
    MOV BX, AX
    POP AX
    LOOP @CREATIV_INT_DEC_REDUCE
    JMP @CREATIV_INT_DEC_OK
    
@CREATIV_INT_DEC_MENOS:
    ; Menos de 2 dígitos, multiplicar por 10
    PUSH AX
    MOV AX, BX
    MOV BX, 10
    MUL BX
    MOV BX, AX
    POP AX
    
@CREATIV_INT_DEC_OK:
    ; Sumar parte decimal normalizada
    ADD AX, BX
    MOV [int_valor], AX
    
    POP BX
    POP AX
    RET
PROBABILIDAD_A_INTEGER ENDP

;------------------------------------------------------------
; Procedimiento: PROBABILIDAD_A_BOOLEAN
; Convierte la probabilidad a booleano (Torch)
; FALSE si es 0.0, TRUE si es > 0.0
;------------------------------------------------------------
PROBABILIDAD_A_BOOLEAN PROC
    ; Una probabilidad es FALSE solo si es exactamente 0.0
    CMP WORD PTR [entero1], 0
    JNE @CREATIV_BOOL_TRUE
    CMP WORD PTR [decimal1], 0
    JNE @CREATIV_BOOL_TRUE
    
    ; Es 0.0, por tanto FALSE
    MOV [bool_valor], 0
    JMP @CREATIV_BOOL_FIN
    
@CREATIV_BOOL_TRUE:
    ; No es 0.0, por tanto TRUE
    MOV [bool_valor], 1
    
@CREATIV_BOOL_FIN:
    RET
PROBABILIDAD_A_BOOLEAN ENDP

;------------------------------------------------------------
; Procedimiento: PROBABILIDAD_A_CHAR
; Convierte la probabilidad a caracter (Rune)
; Usa el primer dígito decimal: 0.75 -> '7'
;------------------------------------------------------------
PROBABILIDAD_A_CHAR PROC
    PUSH AX
    PUSH BX
    PUSH DX
    
    ; Si la probabilidad es 1.0, usar '1'
    CMP WORD PTR [entero1], 1
    JNE @CREATIV_CHAR_NO_UNO
    CMP WORD PTR [decimal1], 0
    JNE @CREATIV_CHAR_NO_UNO
    
    MOV [char_valor], '1'
    JMP @CREATIV_CHAR_FIN
    
@CREATIV_CHAR_NO_UNO:
    ; Si la parte entera es 0, extraer primer dígito decimal
    CMP WORD PTR [entero1], 0
    JNE @CREATIV_CHAR_ENTERO
    
    ; Extraer primer dígito de la parte decimal
    MOV AX, [decimal1]
    CMP AX, 0
    JNE @CREATIV_CHAR_EXTRAER_DEC
    
    ; Decimal es 0, usar '0'
    MOV [char_valor], '0'
    JMP @CREATIV_CHAR_FIN
    
@CREATIV_CHAR_EXTRAER_DEC:
    ; Extraer el primer dígito de decimal1
    MOV BL, [dec_digitos1]
    CMP BL, 1
    JE @CREATIV_CHAR_UN_DIGITO
    
    ; Más de un dígito, extraer el primero
    DEC BL
@CREATIV_CHAR_EXTRAER_LOOP:
    CMP BL, 0
    JE @CREATIV_CHAR_UN_DIGITO
    
    XOR DX, DX
    MOV BX, 10
    DIV BX                  ; AX = AX / 10
    DEC BL
    JMP @CREATIV_CHAR_EXTRAER_LOOP
    
@CREATIV_CHAR_UN_DIGITO:
    ; AX contiene el primer dígito
    ADD AL, '0'
    MOV [char_valor], AL
    JMP @CREATIV_CHAR_FIN
    
@CREATIV_CHAR_ENTERO:
    ; La parte entera no es 0 ni 1 (no debería ocurrir en probabilidades válidas)
    MOV [char_valor], '?'
    
@CREATIV_CHAR_FIN:
    POP DX
    POP BX
    POP AX
    RET
PROBABILIDAD_A_CHAR ENDP

;------------------------------------------------------------
; Procedimiento: PROBABILIDAD_A_STRING
; Convierte la probabilidad a string (Spider)
;------------------------------------------------------------
PROBABILIDAD_A_STRING PROC
    PUSH AX
    PUSH BX
    PUSH CX
    PUSH DX
    PUSH SI
    PUSH DI
    
    ; Limpiar buffer de string
    LEA DI, string_buffer
    
    ; Convertir parte entera a string
    MOV AX, [entero1]
    
    ; Caso especial: cero
    CMP AX, 0
    JNE @CREATIV_STR_ENT_NO_CERO
    
    MOV BYTE PTR [DI], '0'
    INC DI
    JMP @CREATIV_STR_PUNTO
    
@CREATIV_STR_ENT_NO_CERO:
    ; Convertir dígitos de la parte entera
    XOR CX, CX  ; Contador de dígitos
    MOV BX, 10  ; Divisor
    
@CREATIV_STR_DIV_LOOP:
    XOR DX, DX
    DIV BX      ; AX = AX / 10, DX = resto (dígito)
    PUSH DX     ; Guardar dígito en pila
    INC CX      ; Incrementar contador
    
    CMP AX, 0
    JNE @CREATIV_STR_DIV_LOOP
    
    ; Sacar dígitos de la pila en orden correcto
@CREATIV_STR_POP_LOOP:
    POP DX
    ADD DL, '0'
    MOV [DI], DL
    INC DI
    LOOP @CREATIV_STR_POP_LOOP
    
@CREATIV_STR_PUNTO:
    ; Agregar punto decimal
    MOV BYTE PTR [DI], '.'
    INC DI
    
    ; Convertir parte decimal
    CMP BYTE PTR [dec_digitos1], 0
    JNE @CREATIV_STR_HAY_DECIMALES
    
    ; No hay decimales, agregar 0
    MOV BYTE PTR [DI], '0'
    INC DI
    JMP @CREATIV_STR_TERMINAR
    
@CREATIV_STR_HAY_DECIMALES:
    ; Si decimal1 es 0, mostrar ceros según dígitos
    CMP WORD PTR [decimal1], 0
    JNE @CREATIV_STR_CONTAR_DEC
    
    XOR CH, CH
    MOV CL, [dec_digitos1]
@CREATIV_STR_CEROS_LOOP:
    MOV BYTE PTR [DI], '0'
    INC DI
    LOOP @CREATIV_STR_CEROS_LOOP
    JMP @CREATIV_STR_TERMINAR
    
@CREATIV_STR_CONTAR_DEC:
    ; Agregar dígitos decimales reales
    MOV AX, [decimal1]
    XOR CX, CX
    MOV BX, 10
    
@CREATIV_STR_DEC_DIV_LOOP:
    XOR DX, DX
    DIV BX
    PUSH DX
    INC CX
    CMP AX, 0
    JNE @CREATIV_STR_DEC_DIV_LOOP
    
@CREATIV_STR_DEC_POP_LOOP:
    POP DX
    ADD DL, '0'
    MOV [DI], DL
    INC DI
    LOOP @CREATIV_STR_DEC_POP_LOOP
    
@CREATIV_STR_TERMINAR:
    ; Agregar terminador
    MOV BYTE PTR [DI], '$'
    
    POP DI
    POP SI
    POP DX
    POP CX
    POP BX
    POP AX
    RET
PROBABILIDAD_A_STRING ENDP

;------------------------------------------------------------
; Procedimiento: PROBABILIDAD_A_FLOAT
; Convierte la probabilidad a flotante (Ghast)
; Básicamente copia los valores (probabilidad ya es un flotante)
;------------------------------------------------------------
PROBABILIDAD_A_FLOAT PROC
    ; Para convertir a flotante, simplemente copiamos los valores
    ; ya que una probabilidad es esencialmente un flotante en [0,1]
    
    MOV AX, [entero1]
    MOV [float_valor_ent], AX
    
    MOV AX, [decimal1]
    MOV [float_valor_dec], AX
    
    RET
PROBABILIDAD_A_FLOAT ENDP

;------------------------------------------------------------
; Procedimiento: NUEVA_LINEA
; Muestra un salto de línea
;------------------------------------------------------------
NUEVA_LINEA PROC
    PUSH AX
    PUSH DX
    
    MOV AH, 09h
    LEA DX, nueva_lin
    INT 21h
    
    POP DX
    POP AX
    RET
NUEVA_LINEA ENDP

CODIGO ENDS
END INICIO