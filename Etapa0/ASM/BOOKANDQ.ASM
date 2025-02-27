; ********************************************
; * Programa: BOOKANDQ.ASM                  *
; * Descripción: Manejo de strings          *
; * Autores: Luis Urbina, Samir Cabrera     *
; * Fecha: Viernes 07 de Marzo de 2025      *
; ********************************************

DATOS SEGMENT
    prompt_in  DB 'Ingrese un texto (max 50 caracteres): $'
    prompt_out DB 'El texto ingresado es: $'
    buffer     DB 52, ?, 52 DUP(?)  ; Buffer para entrada (max 50 chars + CR + LF)
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
    
    ; Leer entrada
    MOV AH, 0Ah
    LEA DX, buffer
    INT 21h
    
    ; Agregar terminador $ al final del texto
    MOV BL, [buffer+1]    ; Longitud del texto
    XOR BH, BH
    MOV BYTE PTR [buffer+BX+2], '$' ; Agregar terminador
    
    ; Mostrar nueva línea
    MOV AH, 09h
    LEA DX, nueva_lin
    INT 21h
    
    ; Mostrar prompt de salida
    MOV AH, 09h
    LEA DX, prompt_out
    INT 21h
    
    ; Mostrar texto
    MOV AH, 09h
    LEA DX, [buffer+2]
    INT 21h
    
    ; Terminar programa
    MOV AX, 4C00h
    INT 21h
CODIGO ENDS
END INICIO