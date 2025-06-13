;===============================================
;         PROGRAMA DE PRUEBA RUNTIME LIBRARY
;===============================================
; Generado por: Cabrera Samir, Urbina Luis
; Prueba básica de la Runtime Library
;===============================================

ASSUME CS:CODE, DS:DATA, SS:STACK

; Segmento de pila
STACK SEGMENT STACK
    DW 256 DUP(?)
STACK ENDS

; Segmento de datos
DATA SEGMENT
    titulo DB "PRUEBA DE RUNTIME LIBRARY - NOTCH ENGINE", 13, 10, '$'
    separador DB "==========================================", 13, 10, '$'
    
    ; Variables de prueba
    num1 DW 15
    num2 DW 7
    resultado DW ?
    
    bool1 DB 1
    bool2 DB 0
    resultado_bool DB ?
    
    ; Mensajes
    msg_suma DB "Suma 15 + 7 = $"
    msg_resta DB "Resta 15 - 7 = $"
    msg_mult DB "Multiplicacion 15 * 7 = $"
    msg_div DB "Division 15 / 7 = $"
    msg_mod DB "Modulo 15 % 7 = $"
    msg_and DB "AND 1 AND 0 = $"
    msg_or DB "OR 1 OR 0 = $"
    newline DB 13, 10, '$'
    
DATA ENDS

; Segmento de código
CODE SEGMENT
START:
    ; Inicializar segmentos
    MOV AX, DATA
    MOV DS, AX
    
    ; Mostrar título
    MOV AH, 09h
    LEA DX, titulo
    INT 21h
    
    LEA DX, separador
    INT 21h
    
    ; PRUEBA 1: Suma de enteros
    MOV AH, 09h
    LEA DX, msg_suma
    INT 21h
    
    PUSH [num2]
    PUSH [num1]
    CALL SUMAR_ENTEROS
    MOV [resultado], AX
    
    PUSH [resultado]
    CALL MOSTRAR_ENTERO
    
    MOV AH, 09h
    LEA DX, newline
    INT 21h
    
    ; PRUEBA 2: Resta de enteros
    MOV AH, 09h
    LEA DX, msg_resta
    INT 21h
    
    PUSH [num2]
    PUSH [num1]
    CALL RESTAR_ENTEROS
    MOV [resultado], AX
    
    PUSH [resultado]
    CALL MOSTRAR_ENTERO
    
    MOV AH, 09h
    LEA DX, newline
    INT 21h
    
    ; PRUEBA 3: Multiplicación
    MOV AH, 09h
    LEA DX, msg_mult
    INT 21h
    
    PUSH [num2]
    PUSH [num1]
    CALL MULTIPLICAR_ENTEROS
    MOV [resultado], AX
    
    PUSH [resultado]
    CALL MOSTRAR_ENTERO
    
    MOV AH, 09h
    LEA DX, newline
    INT 21h
    
    ; PRUEBA 4: División
    MOV AH, 09h
    LEA DX, msg_div
    INT 21h
    
    PUSH [num2]
    PUSH [num1]
    CALL DIVIDIR_ENTEROS
    MOV [resultado], AX
    
    PUSH [resultado]
    CALL MOSTRAR_ENTERO
    
    MOV AH, 09h
    LEA DX, newline
    INT 21h
    
    ; PRUEBA 5: Módulo
    MOV AH, 09h
    LEA DX, msg_mod
    INT 21h
    
    PUSH [num2]
    PUSH [num1]
    CALL MODULO_ENTEROS
    MOV [resultado], AX
    
    PUSH [resultado]
    CALL MOSTRAR_ENTERO
    
    MOV AH, 09h
    LEA DX, newline
    INT 21h
    
    ; PRUEBA 6: AND lógico
    MOV AH, 09h
    LEA DX, msg_and
    INT 21h
    
    MOV AL, [bool2]
    PUSH AX
    MOV AL, [bool1]
    PUSH AX
    CALL AND_LOGICO
    MOV [resultado_bool], AL
    
    CMP AL, 0
    JE @MOSTRAR_FALSE_AND
    
    MOV AH, 09h
    LEA DX, STR_TRUE
    INT 21h
    JMP @AND_FIN
    
@MOSTRAR_FALSE_AND:
    MOV AH, 09h
    LEA DX, STR_FALSE
    INT 21h
    
@AND_FIN:
    MOV AH, 09h
    LEA DX, newline
    INT 21h
    
    ; PRUEBA 7: OR lógico
    MOV AH, 09h
    LEA DX, msg_or
    INT 21h
    
    MOV AL, [bool2]
    PUSH AX
    MOV AL, [bool1]
    PUSH AX
    CALL OR_LOGICO
    MOV [resultado_bool], AL
    
    CMP AL, 0
    JE @MOSTRAR_FALSE_OR
    
    MOV AH, 09h
    LEA DX, STR_TRUE
    INT 21h
    JMP @OR_FIN
    
@MOSTRAR_FALSE_OR:
    MOV AH, 09h
    LEA DX, STR_FALSE
    INT 21h
    
@OR_FIN:
    MOV AH, 09h
    LEA DX, newline
    INT 21h
    
    ; Finalizar programa
    MOV AH, 4Ch
    INT 21h

CODE ENDS

; Incluir la Runtime Library
INCLUDE runtime_library.asm

END START