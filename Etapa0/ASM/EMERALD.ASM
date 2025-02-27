; ********************************************
; * Programa: EMERALD.ASM                   *
; * Descripción: Manejo de números enteros  *
; * Autores: Luis Urbina, Samir Cabrera     *
; * Fecha: Viernes 07 de Marzo de 2025      *
; ********************************************

DATOS SEGMENT
    prompt_in  DB 'Ingrese un numero entero: $'
    prompt_out DB 'El numero ingresado es: $'
    buffer     DB 10, ?, 10 DUP(?)  ; Buffer para entrada (max 10 chars)
    numero     DW ?                 ; Variable para almacenar el entero
    es_negativo DB 0                ; Flag para números negativos
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
    
    ; Convertir string a número
    CALL STR_A_NUM
    
    ; Mostrar nueva línea
    MOV AH, 09h
    LEA DX, nueva_lin
    INT 21h
    
    ; Mostrar prompt de salida
    MOV AH, 09h
    LEA DX, prompt_out
    INT 21h
    
    ; Convertir número a string y mostrar
    MOV AX, [numero]
    CALL NUM_A_STR
    
    ; Terminar programa
    MOV AX, 4C00h
    INT 21h

; Convierte string (buffer) a número (numero)
STR_A_NUM PROC
    PUSH AX
    PUSH BX
    PUSH CX
    PUSH DX
    PUSH SI
    
    XOR AX, AX        ; Inicializar resultado a 0
    MOV BL, [buffer+1] ; Longitud de la cadena en BL
    XOR BH, BH        ; BH = 0
    LEA SI, [buffer+2] ; Inicio de los caracteres en el buffer
    
    ; Resetear flag de negativo
    MOV [es_negativo], 0
    
    ; Verificar si empieza con signo negativo
    CMP BX, 0
    JE CONVERSION_FIN ; Si la cadena está vacía, terminar
    
    MOV CL, [SI]      ; Obtener primer carácter
    CMP CL, '-'       ; Verificar si es signo negativo
    JNE CONVERSION    ; Si no es negativo, continuar normal
    
    ; Si es negativo, marcar flag y avanzar al siguiente carácter
    MOV [es_negativo], 1
    INC SI
    DEC BX
    
CONVERSION:
    CMP BX, 0         ; ¿Terminamos la conversión?
    JE CONVERSION_PROCESAR
    
    MOV CL, [SI]      ; Obtener caracter
    INC SI            ; Avanzar al siguiente caracter
    
    CMP CL, '0'       ; Verificar si es un dígito
    JL NO_DIGITO
    CMP CL, '9'
    JG NO_DIGITO
    
    SUB CL, '0'       ; Convertir ASCII a valor numérico
    XOR CH, CH        ; CH = 0
    
    ; Resultado = Resultado * 10 + Dígito
    PUSH BX
    MOV BX, 10
    MUL BX            ; AX = AX * 10
    POP BX
    ADD AX, CX        ; AX = AX + Dígito
    
NO_DIGITO:
    DEC BX
    JMP CONVERSION
    
CONVERSION_PROCESAR:
    ; Si es negativo, negar el número
    CMP [es_negativo], 1
    JNE CONVERSION_FIN
    
    NEG AX            ; Convertir a negativo (complemento a 2)
    
CONVERSION_FIN:
    MOV [numero], AX
    
    POP SI
    POP DX
    POP CX
    POP BX
    POP AX
    RET
STR_A_NUM ENDP

; Convierte número (AX) a string y lo muestra
NUM_A_STR PROC
    PUSH AX
    PUSH BX
    PUSH CX
    PUSH DX
    
    ; Verificar si es negativo
    CMP AX, 0
    JGE NUM_POSITIVO
    
    ; Si es negativo, mostrar el signo "-" y negar el número
    PUSH AX
    MOV DL, '-'
    MOV AH, 02h
    INT 21h
    POP AX
    NEG AX            ; Convertir a positivo para procesarlo
    
NUM_POSITIVO:
    MOV BX, 10        ; Divisor
    XOR CX, CX        ; Contador de dígitos
    
    ; Si es cero, tratar especialmente
    CMP AX, 0
    JNE DIVIDIR
    
    MOV DL, '0'       ; Carácter '0'
    MOV AH, 02h       ; Función para mostrar carácter
    INT 21h
    JMP NUM_A_STR_FIN
    
DIVIDIR:
    XOR DX, DX        ; DX:AX / BX, DX = resto
    DIV BX            ; AX = cociente, DX = resto
    
    PUSH DX           ; Guardar el dígito
    INC CX            ; Incrementar contador
    
    CMP AX, 0         ; ¿Terminamos?
    JNE DIVIDIR
    
MOSTRAR_DIGITOS:
    POP DX            ; Recuperar dígito
    ADD DL, '0'       ; Convertir a ASCII
    MOV AH, 02h       ; Función para mostrar carácter
    INT 21h
    LOOP MOSTRAR_DIGITOS
    
NUM_A_STR_FIN:
    POP DX
    POP CX
    POP BX
    POP AX
    RET
NUM_A_STR ENDP

CODIGO ENDS
END INICIO