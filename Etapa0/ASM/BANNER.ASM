; ********************************************
; * Programa: BANNER.ASM                    *
; * Descripción: Manejo de conjuntos        *
; * Autores: Luis Urbina, Samir Cabrera     *
; * Fecha: Viernes 07 de Marzo de 2025      *
; ********************************************

DATOS SEGMENT
    prompt_in  DB 'Ingrese elementos del conjunto separados por comas (max 30 caracteres): $'
    prompt_out DB 'Elementos del conjunto: $'
    buffer     DB 32, ?, 32 DUP(?)  ; Buffer para entrada (max 30 chars + CR + LF)
    conjunto   DB 30 DUP(0)         ; Buffer para almacenar elementos del conjunto
    num_elems  DB 0                 ; Número de elementos en el conjunto
    nueva_lin  DB 0Dh, 0Ah, '$'     ; Nueva línea
    separador  DB ', $'             ; Separador para mostrar elementos
    valor_empty DB '{conjunto vacio}$'
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
    
    ; Procesar elementos del conjunto
    CALL PROCESAR_CONJUNTO
    
    ; Mostrar nueva línea
    MOV AH, 09h
    LEA DX, nueva_lin
    INT 21h
    
    ; Mostrar prompt de salida
    MOV AH, 09h
    LEA DX, prompt_out
    INT 21h
    
    ; Mostrar elementos del conjunto
    CALL MOSTRAR_CONJUNTO
    
    ; Terminar programa
    MOV AX, 4C00h
    INT 21h

; Procesa la entrada y extrae elementos del conjunto
PROCESAR_CONJUNTO PROC
    PUSH AX
    PUSH BX
    PUSH CX
    PUSH DX
    PUSH SI
    PUSH DI
    
    MOV BL, [buffer+1]    ; Longitud del texto
    XOR BH, BH
    LEA SI, [buffer+2]    ; Puntero al texto de entrada
    LEA DI, conjunto      ; Puntero al buffer del conjunto
    XOR CX, CX            ; Contador de elementos
    
    ; Si no hay entrada, terminar
    CMP BX, 0
    JE PROCESAR_FIN
    
PROCESAR_LOOP:
    CMP BX, 0
    JE PROCESAR_FIN
    
    MOV AL, [SI]          ; Obtener caracter
    INC SI
    DEC BX
    
    ; Si es una coma, ignorar
    CMP AL, ','
    JE PROCESAR_LOOP
    
    ; Si es un espacio, ignorar
    CMP AL, ' '
    JE PROCESAR_LOOP
    
    ; Si es un caracter válido, agregarlo al conjunto
    MOV [DI], AL
    INC DI
    INC CX
    
    JMP PROCESAR_LOOP
    
PROCESAR_FIN:
    MOV [num_elems], CL    ; Guardar número de elementos
    
    POP DI
    POP SI
    POP DX
    POP CX
    POP BX
    POP AX
    RET
PROCESAR_CONJUNTO ENDP

; Muestra los elementos del conjunto
MOSTRAR_CONJUNTO PROC
    PUSH AX
    PUSH BX
    PUSH CX
    PUSH DX
    PUSH SI
    
    XOR CX, CX
    MOV CL, [num_elems]    ; Número de elementos
    LEA SI, conjunto      ; Puntero a los elementos
    
    CMP CL, 0
    JE MOSTRAR_VACIO
    
MOSTRAR_LOOP:
    ; Mostrar elemento
    MOV DL, [SI]
    MOV AH, 02h
    INT 21h
    
    INC SI
    DEC CX
    
    ; Si no es el último elemento, mostrar separador
    CMP CX, 0
    JE MOSTRAR_FIN
    
    MOV AH, 09h
    LEA DX, separador
    INT 21h
    
    JMP MOSTRAR_LOOP
    
MOSTRAR_VACIO:
    MOV AH, 09h
    LEA DX, valor_empty
    INT 21h
    JMP MOSTRAR_FIN
    
MOSTRAR_FIN:
    POP SI
    POP DX
    POP CX
    POP BX
    POP AX
    RET
MOSTRAR_CONJUNTO ENDP

CODIGO ENDS
END INICIO