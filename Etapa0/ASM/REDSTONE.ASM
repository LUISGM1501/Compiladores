; ********************************************
; * Programa: REDSTONE.ASM                  *
; * Descripción: Manejo de booleanos        *
; * Autores: Luis Urbina, Samir Cabrera     *
; * Fecha: Viernes 07 de Marzo de 2025      *
; ********************************************

DATOS SEGMENT
    prompt_in  DB 'Ingrese 1 para TRUE o 0 para FALSE: $'
    prompt_out DB 'El valor booleano es: $'
    valor_true DB 'TRUE$'
    valor_false DB 'FALSE$'
    booleano   DB ?                 ; Variable para almacenar el booleano
    nueva_lin  DB 0Dh, 0Ah, '$'     ; Nueva línea
DATOS ENDS

CODIGO SEGMENT
    ASSUME CS:CODIGO, DS:DATOS
INICIO:
    MOV AX, DATOS
    MOV DS, AX
    
    ; Mostrar prompt de entrada
    MOV AH, 09h
    LEA DX, prompt_in
    INT 21h
    
    ; Leer caracter
    MOV AH, 01h       ; Función para leer caracter
    INT 21h
    
    ; Verificar si es '1' o '0'
    CMP AL, '1'
    JE ES_TRUE
    CMP AL, '0'
    JE ES_FALSE
    
    ; Si no es '1' ni '0', considera como FALSE
ES_FALSE:
    MOV [booleano], 0
    JMP MOSTRAR_RESULTADO
    
ES_TRUE:
    MOV [booleano], 1
    
MOSTRAR_RESULTADO:
    ; Mostrar nueva línea
    MOV AH, 09h
    LEA DX, nueva_lin
    INT 21h
    
    ; Mostrar prompt de salida
    MOV AH, 09h
    LEA DX, prompt_out
    INT 21h
    
    ; Mostrar valor booleano
    CMP [booleano], 0
    JE MOSTRAR_FALSE
    
    ; Mostrar TRUE
    MOV AH, 09h
    LEA DX, valor_true
    INT 21h
    JMP FIN_PROGRAMA
    
MOSTRAR_FALSE:
    ; Mostrar FALSE
    MOV AH, 09h
    LEA DX, valor_false
    INT 21h
    
FIN_PROGRAMA:
    ; Terminar programa
    MOV AX, 4C00h
    INT 21h
CODIGO ENDS
END INICIO