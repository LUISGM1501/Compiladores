; ********************************************
; * Programa: BOOK.ASM                      *
; * Descripción: Manejo de caracteres       *
; * Autores: Luis Urbina, Samir Cabrera     *
; * Fecha: Viernes 07 de Marzo de 2025      *
; ********************************************

DATOS SEGMENT
    prompt_in  DB 'Ingrese un caracter: $'
    prompt_out DB 'El caracter ingresado es: $'
    caracter   DB ?                 ; Variable para almacenar el carácter
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
    MOV [caracter], AL ; Guardar caracter
    
    ; Mostrar nueva línea
    MOV AH, 09h
    LEA DX, nueva_lin
    INT 21h
    
    ; Mostrar prompt de salida
    MOV AH, 09h
    LEA DX, prompt_out
    INT 21h
    
    ; Mostrar caracter
    MOV DL, [caracter]
    MOV AH, 02h       ; Función para mostrar caracter
    INT 21h
    
    ; Terminar programa
    MOV AX, 4C00h
    INT 21h
CODIGO ENDS
END INICIO