;===============================================
;              NOTCH ENGINE COMPILER
;===============================================
; Generado por: Cabrera Samir, Urbina Luis
; Fecha: 12/06/2025 21:47
; Proyecto: Compilador para Notch Engine
; Etapa 4: Generador de Código
;===============================================

; Configuración inicial del programa
ASSUME CS:CODE, DS:DATA, SS:STACK

; Segmento de pila
STACK SEGMENT STACK
    DW 256 DUP(?)
STACK ENDS

; Segmento de datos
DATA SEGMENT
    numero DW 10
    ; Operación: resultado = numero :+ 5
    PUSH 5    ; Segundo operando
    PUSH numero    ; Primer operando
    CALL SUMAR_ENTEROS       ; Llamar rutina de Runtime Library
    MOV resultado, AX  ; Guardar resultado


DATA ENDS

; Segmento de código
CODE SEGMENT
MAIN PROC
    MOV AX, DATA
    MOV DS, AX

    ; Código principal generado

    ; Terminar programa
    MOV AH, 4Ch
    INT 21h
MAIN ENDP
CODE ENDS
END MAIN