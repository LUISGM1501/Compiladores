;===============================================
;              NOTCH ENGINE COMPILER
;===============================================
; Generado por: Cabrera Samir, Urbina Luis
; Fecha: 12/06/2025 19:39
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
    numero DW 0
    resultado DW 0
    es_positivo DB 0
    ; HOPPER_STACK: Leer STACK en numero
    CALL LEER_ENTERO
    MOV numero, AX

    ; MAYOR_QUE (>): es_positivo = numero > 0
    PUSH 0    ; Segundo operando
    PUSH numero    ; Primer operando
    CALL COMPARAR_MAYOR       ; Rutina: COMPARAR_MAYOR
    MOV es_positivo, AX  ; Resultado (0=falso, 1=verdadero)

    ; TARGET (if): numero > 0
    CMP es_positivo, 0    ; Evaluar condición
    JE IF0000_MISS        ; MISS si falso
    ; HIT - bloque verdadero

    ; Asignación: resultado = 1
    MOV AX, 1
    MOV resultado, AX

    ; DROPPER_STACK: Mostrar STACK de resultado
    PUSH resultado
    CALL MOSTRAR_ENTERO

    JMP IF0001_FIN  ; Saltar al final del TARGET
IF0000_MISS:
    ; MISS - bloque falso

    ; Asignación: resultado = -1
    MOV AX, -1
    MOV resultado, AX

    ; DROPPER_STACK: Mostrar STACK de resultado
    PUSH resultado
    CALL MOSTRAR_ENTERO

IF0001_FIN:
    ; Fin del TARGET: numero > 0


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