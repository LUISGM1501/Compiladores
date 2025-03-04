; ********************************************
; * Programa: GOLDNUGG.ASM                  *
; * Descripción: Manejo de números flotantes*
; * Autores: Luis Urbina, Samir Cabrera     *
; * Fecha: Viernes 07 de Marzo de 2025      *
; ********************************************

DATOS SEGMENT
    prompt_in   DB 'Ingrese de probabilidad entre 0 y 1: $'
    prompt_out  DB 'El numero de probabilidad es: $'
    buffer      DB 15, ?, 15 DUP(?)  ; Buffer para entrada
    entero      DW ?                  ; Parte entera
    decimal     DW ?                  ; Parte decimal
    dec_digitos DB ?                  ; Número de dígitos decimales
    es_negativo DB 0                  ; Flag para números negativos
    nueva_lin   DB 0Dh, 0Ah, '$'      ; Nueva línea
    punto       DB '.$'               ; Punto decimal
    constante_diez DW 10              ; Constante para cálculos
    error_rango DB 'Error: El numero debe estar en el rango de 0 a 1$'  ; Mensaje de error para validación
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
    
    ; Procesar número flotante
    CALL PROCESAR_FLOTANTE
    
    ; Validar rango 0 a 1
    CALL VALIDAR_RANGO
    JC MOSTRAR_ERROR_RANGO  ; Si hay error de rango, mostrar mensaje
    
    ; Mostrar nueva línea
    MOV AH, 09h
    LEA DX, nueva_lin
    INT 21h
    
    ; Mostrar prompt de salida
    MOV AH, 09h
    LEA DX, prompt_out
    INT 21h
    
    ; Mostrar número flotante
    CALL MOSTRAR_FLOTANTE
    
    JMP FIN_PROGRAMA
    
MOSTRAR_ERROR_RANGO:
    ; Mostrar nueva línea
    MOV AH, 09h
    LEA DX, nueva_lin
    INT 21h
    
    ; Mostrar mensaje de error
    MOV AH, 09h
    LEA DX, error_rango
    INT 21h
    
FIN_PROGRAMA:
    ; Terminar programa
    MOV AX, 4C00h
    INT 21h

; Valida que el número esté en el rango de 0 a 1
; Si el número no es válido, CF=1, sino CF=0
VALIDAR_RANGO PROC
    PUSH AX
    
    ; Verificar si es negativo (debe ser mayor o igual a 0)
    CMP [es_negativo], 1
    JE FUERA_DE_RANGO
    
    ; Verificar que la parte entera sea 0 o 1
    MOV AX, [entero]
    CMP AX, 0
    JE RANGO_VALIDO      ; Si es 0, es válido
    CMP AX, 1
    JE VERIFICAR_DECIMAL ; Si es 1, hay que verificar que decimal sea 0
    JMP FUERA_DE_RANGO   ; Si es > 1, no es válido
    
VERIFICAR_DECIMAL:
    ; Si entero es 1, decimal debe ser 0 para estar en rango
    CMP WORD PTR [decimal], 0
    JNE FUERA_DE_RANGO
    
RANGO_VALIDO:
    CLC                  ; Limpiar carry flag (sin error)
    JMP FIN_VALIDACION
    
FUERA_DE_RANGO:
    STC                  ; Establecer carry flag (con error)
    
FIN_VALIDACION:
    POP AX
    RET
VALIDAR_RANGO ENDP

; Procesa la entrada y extrae parte entera y decimal
PROCESAR_FLOTANTE PROC
    PUSH AX
    PUSH BX
    PUSH CX
    PUSH DX
    PUSH SI
    
    XOR AX, AX            ; Inicializar resultado a 0
    MOV BL, [buffer+1]    ; Longitud de la cadena en BL
    XOR BH, BH
    LEA SI, [buffer+2]    ; Inicio de los caracteres en el buffer
    
    ; Inicializar variables
    MOV [entero], 0
    MOV [decimal], 0
    MOV [dec_digitos], 0
    MOV [es_negativo], 0  ; Resetear flag de negativo
    
    ; Verificar si empieza con signo negativo
    CMP BX, 0
    JE PROC_FIN           ; Si la cadena está vacía, terminar
    
    MOV CL, [SI]          ; Obtener primer carácter
    CMP CL, '-'           ; Verificar si es signo negativo
    JNE PROC_ENTERO       ; Si no es negativo, procesar parte entera
    
    ; Si es negativo, marcar flag y avanzar al siguiente carácter
    MOV [es_negativo], 1
    INC SI
    DEC BX
    
    ; Procesar parte entera hasta encontrar el punto
PROC_ENTERO:
    CMP BX, 0             ; ¿Terminamos?
    JE PROC_FIN
    
    MOV CL, [SI]          ; Obtener caracter
    INC SI
    DEC BX
    
    CMP CL, '.'           ; ¿Es el punto decimal?
    JE PROC_DECIMAL
    
    CMP CL, '0'           ; Verificar si es un dígito
    JL PROC_ENTERO
    CMP CL, '9'
    JG PROC_ENTERO
    
    SUB CL, '0'           ; Convertir ASCII a valor numérico
    XOR CH, CH
    
    ; Entero = Entero * 10 + Dígito
    MOV AX, [entero]
    MOV DX, 10
    MUL DX
    ADD AX, CX
    MOV [entero], AX
    
    JMP PROC_ENTERO
    
; Procesar parte decimal después del punto
PROC_DECIMAL:
    CMP BX, 0             ; ¿Terminamos?
    JE PROC_FIN
    
    MOV CL, [SI]          ; Obtener caracter
    INC SI
    DEC BX
    
    CMP CL, '0'           ; Verificar si es un dígito
    JL PROC_DECIMAL
    CMP CL, '9'
    JG PROC_DECIMAL
    
    SUB CL, '0'           ; Convertir ASCII a valor numérico
    XOR CH, CH
    
    ; Decimal = Decimal * 10 + Dígito
    MOV AX, [decimal]
    MOV DX, 10
    MUL DX
    ADD AX, CX
    MOV [decimal], AX
    
    ; Incrementar contador de dígitos decimales
    INC [dec_digitos]
    
    JMP PROC_DECIMAL
    
PROC_FIN:
    ; Si es negativo y la parte entera es diferente de cero, aplicar signo
    CMP [es_negativo], 1
    JNE PROC_NORMAL
    
    ; Sólo aplicamos el signo a la parte entera - la parte decimal siempre es positiva
    MOV AX, [entero]
    NEG AX
    MOV [entero], AX
    
PROC_NORMAL:
    POP SI
    POP DX
    POP CX
    POP BX
    POP AX
    RET
PROCESAR_FLOTANTE ENDP

; Muestra el número flotante
MOSTRAR_FLOTANTE PROC
    PUSH AX
    PUSH BX
    PUSH CX
    PUSH DX
    
    ; Mostrar parte entera
    MOV AX, [entero]
    CALL MOSTRAR_ENTERO
    
    ; Mostrar punto decimal
    MOV AH, 09h
    LEA DX, punto
    INT 21h
    
    ; Mostrar parte decimal
    CALL MOSTRAR_DECIMAL
    
    POP DX
    POP CX
    POP BX
    POP AX
    RET
MOSTRAR_FLOTANTE ENDP

; Muestra la parte decimal
MOSTRAR_DECIMAL PROC
    PUSH AX
    PUSH BX
    PUSH CX
    PUSH DX
    
    ; Verificar si hay dígitos decimales
    CMP BYTE PTR [dec_digitos], 0
    JNE TIENE_DECIMALES
    
    ; Si no hay decimales, mostrar 0
    MOV DL, '0'
    MOV AH, 02h
    INT 21h
    JMP FIN_DECIMAL
    
TIENE_DECIMALES:
    ; Inicializar contador para mantener dígitos originales
    MOV CL, [dec_digitos]
    XOR CH, CH
    MOV BX, CX  ; Guardar en BX para usar después
    
    ; Calcular potencia de 10
    MOV AX, 1
CALCULAR_POTENCIA:
    CMP CL, 0
    JE FIN_POTENCIA
    
    MUL WORD PTR [constante_diez]
    
    DEC CL
    JMP CALCULAR_POTENCIA
    
FIN_POTENCIA:
    MOV CX, AX  ; CX = potencia de 10
    
    ; Si el decimal es menor que la potencia, necesitamos ceros a la izquierda
    MOV AX, [decimal]
    
    ; Contar dígitos del decimal
    MOV DX, AX  ; Guardar decimal en DX
    XOR AX, AX  ; Contador de dígitos
    
    ; Si es 0, necesitamos todos los dígitos como ceros
    CMP DX, 0
    JNE CONTAR_DIGITOS
    
    ; Mostrar todos los ceros
    MOV CX, BX  ; Número de dígitos decimales
MOSTRAR_SOLO_CEROS:
    CMP CX, 0
    JE FIN_DECIMAL
    
    MOV DL, '0'
    MOV AH, 02h
    INT 21h
    
    DEC CX
    JMP MOSTRAR_SOLO_CEROS
    
CONTAR_DIGITOS:
    MOV AX, DX
    XOR CX, CX  ; Contador de dígitos
    
BUCLE_CONTAR:
    INC CX
    
    XOR DX, DX
    DIV WORD PTR [constante_diez]
    
    CMP AX, 0
    JNE BUCLE_CONTAR
    
    ; CX = número de dígitos del decimal
    MOV AX, BX  ; BX tiene el número original de dígitos necesarios
    SUB AX, CX  ; AX = ceros a agregar al inicio
    
    ; Mostrar ceros iniciales
    CMP AX, 0
    JLE MOSTRAR_DECIMAL_VALOR
    
    MOV CX, AX
MOSTRAR_CEROS_INICIALES:
    MOV DL, '0'
    MOV AH, 02h
    INT 21h
    
    LOOP MOSTRAR_CEROS_INICIALES
    
MOSTRAR_DECIMAL_VALOR:
    ; Mostrar el valor decimal
    MOV AX, [decimal]
    
    ; Procesar dígitos en orden
    CALL MOSTRAR_NUMERO_POSITIVO
    
FIN_DECIMAL:
    POP DX
    POP CX
    POP BX
    POP AX
    RET
MOSTRAR_DECIMAL ENDP

; Muestra un número entero (con signo)
MOSTRAR_ENTERO PROC
    PUSH AX
    PUSH BX
    PUSH CX
    PUSH DX
    
    ; Verificar si es negativo
    CMP AX, 0
    JGE ENTERO_POSITIVO
    
    ; Si es negativo, mostrar signo y negar
    PUSH AX
    MOV DL, '-'
    MOV AH, 02h
    INT 21h
    POP AX
    NEG AX
    
ENTERO_POSITIVO:
    CALL MOSTRAR_NUMERO_POSITIVO
    
    POP DX
    POP CX
    POP BX
    POP AX
    RET
MOSTRAR_ENTERO ENDP

; Muestra un número positivo
MOSTRAR_NUMERO_POSITIVO PROC
    PUSH AX
    PUSH BX
    PUSH CX
    PUSH DX
    
    ; Si es cero, tratar especial
    CMP AX, 0
    JNE CONVERTIR_DIGITOS
    
    MOV DL, '0'
    MOV AH, 02h
    INT 21h
    JMP FIN_POSITIVO
    
CONVERTIR_DIGITOS:
    ; Convertir número a dígitos en la pila
    XOR CX, CX  ; Contador de dígitos
    MOV BX, 10
    
BUCLE_DIVISION:
    XOR DX, DX
    DIV BX
    
    PUSH DX  ; Guardar dígito en la pila
    INC CX
    
    CMP AX, 0
    JNE BUCLE_DIVISION
    
    ; Mostrar dígitos en orden correcto
BUCLE_MOSTRAR:
    POP DX
    ADD DL, '0'
    
    MOV AH, 02h
    INT 21h
    
    LOOP BUCLE_MOSTRAR
    
FIN_POSITIVO:
    POP DX
    POP CX
    POP BX
    POP AX
    RET
MOSTRAR_NUMERO_POSITIVO ENDP

CODIGO ENDS
END INICIO