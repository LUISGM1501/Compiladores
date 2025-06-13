;===============================================
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

; Rutina: NUEVA - Leer string (HOPPER_SPIDER)
LEER_STRING PROC
    PUSH BP
    MOV BP, SP
    PUSH BX
    PUSH CX
    PUSH DX
    PUSH SI
    
    MOV SI, [BP+4]    ; Dirección del buffer
    MOV CX, [BP+6]    ; Tamaño máximo
    MOV BX, 0         ; Contador de caracteres
    
@LEER_STR_LOOP:
    MOV AH, 01h
    INT 21h
    
    CMP AL, 0Dh       ; Enter
    JE @LEER_STR_FIN
    
    CMP BX, CX        ; Verificar límite
    JGE @LEER_STR_LOOP
    
    MOV [SI + BX], AL ; Guardar carácter
    INC BX
    JMP @LEER_STR_LOOP
    
@LEER_STR_FIN:
    MOV [SI + BX], '$' ; Terminador
    
    POP SI
    POP DX
    POP CX
    POP BX
    POP BP
    RET 4
LEER_STRING ENDP

; Rutina: NUEVA - Mostrar string (DROPPER_SPIDER)
MOSTRAR_STRING PROC
    PUSH BP
    MOV BP, SP
    PUSH DX
    
    MOV DX, [BP+4]    ; Dirección del string
    MOV AH, 09h
    INT 21h
    
    POP DX
    POP BP
    RET 2
MOSTRAR_STRING ENDP

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
; OPERACIONES DE STRINGS (SPIDER)
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
    CMP AL, '
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
    CMP AL, '
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
    CMP BL, '
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
; OPERACIONES FLOTANTES (GHAST)
;===============================================

; Rutina: NUEVA - Sumar flotantes (:+)
; Usa la lógica de SELECTED.ASM pero simplificada
SUMAR_FLOTANTES PROC
    PUSH BP
    MOV BP, SP
    PUSH BX
    PUSH CX
    PUSH DX
    
    ; Parámetros: [BP+4]=entero1, [BP+6]=decimal1, [BP+8]=entero2, [BP+10]=decimal2
    ; Resultado en AX (entero), DX (decimal)
    
    ; Sumar partes enteras
    MOV AX, [BP+4]
    ADD AX, [BP+8]
    
    ; Sumar partes decimales
    MOV BX, [BP+6]
    ADD BX, [BP+10]
    
    ; Verificar desbordamiento decimal
    CMP BX, 10000
    JL @SUMAR_FLOAT_FIN
    
    SUB BX, 10000
    INC AX
    
@SUMAR_FLOAT_FIN:
    MOV DX, BX
    
    POP DX
    POP CX
    POP BX
    POP BP
    RET 8
SUMAR_FLOTANTES ENDP

; Rutina: NUEVA - Restar flotantes (:-)
RESTAR_FLOTANTES PROC
    PUSH BP
    MOV BP, SP
    PUSH BX
    PUSH CX
    
    ; Parámetros similares a suma
    MOV AX, [BP+4]
    SUB AX, [BP+8]
    
    MOV BX, [BP+6]
    SUB BX, [BP+10]
    
    ; Verificar préstamo
    CMP BX, 0
    JGE @RESTAR_FLOAT_FIN
    
    ADD BX, 10000
    DEC AX
    
@RESTAR_FLOAT_FIN:
    MOV DX, BX
    
    POP CX
    POP BX
    POP BP
    RET 8
RESTAR_FLOTANTES ENDP

; Rutina: NUEVA - Multiplicar flotantes (:*)
MULTIPLICAR_FLOTANTES PROC
    PUSH BP
    MOV BP, SP
    ; Implementación básica - se puede expandir según SELECTED.ASM
    MOV AX, [BP+4]
    IMUL WORD PTR [BP+8]
    POP BP
    RET 8
MULTIPLICAR_FLOTANTES ENDP

; Rutina: NUEVA - Dividir flotantes (:/)
DIVIDIR_FLOTANTES PROC
    PUSH BP
    MOV BP, SP
    PUSH BX
    PUSH DX
    
    MOV AX, [BP+4]
    MOV BX, [BP+8]
    
    CMP BX, 0
    JE @DIV_FLOAT_ERROR
    
    CWD
    IDIV BX
    JMP @DIV_FLOAT_FIN
    
@DIV_FLOAT_ERROR:
    MOV AX, 0
    
@DIV_FLOAT_FIN:
    POP DX
    POP BX
    POP BP
    RET 8
DIVIDIR_FLOTANTES ENDP

;===============================================
; OPERACIONES ADICIONALES DE ENTEROS
;===============================================

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
; DATOS PARA RUTINAS
;===============================================
STR_TRUE    DB "ON$"
STR_FALSE   DB "OFF$"
NEWLINE     DB 13, 10, '
SPACE       DB '