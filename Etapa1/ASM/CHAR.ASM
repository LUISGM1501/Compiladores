; ********************************************
; * Programa: CHAR.ASM                      *
; * Descripcion: Conversiones desde caracter*
; * Autores: Luis Urbina, Samir Cabrera     *
; * Fecha de entrega: 10/04/2025            *
; ********************************************

; El segmento DATOS contiene todas las variables y constantes que usara el programa
DATOS SEGMENT
    ; Mensajes de entrada y salida
    prompt_in    DB 'Ingrese un caracter: $'                  ; Mensaje para solicitar entrada al usuario
    prompt_char  DB 'El caracter ingresado es: $'             ; Mensaje para mostrar el caracter original
    prompt_int   DB 'Convertido a entero (ASCII): $'          ; Mensaje para mostrar la conversión a entero
    prompt_float DB 'Convertido a flotante: $'                ; Mensaje para mostrar la conversión a flotante
    prompt_bool  DB 'Convertido a booleano: $'                ; Mensaje para mostrar la conversión a booleano
    prompt_str   DB 'Convertido a string: $'                  ; Mensaje para mostrar la conversión a string
    prompt_creativo DB 'Convertido a creativo (probabilidad): $' ; Mensaje para conversión a creativo
    
    ; Variables para almacenar valores
    caracter     DB ?           ; Variable para almacenar el caracter ingresado
    entero       DW ?           ; Variable para almacenar el valor convertido a entero
    bool_valor   DB ?           ; Variable para almacenar el valor booleano
    
    ; Variables para valor flotante
    float_entero DW ?           ; Parte entera del flotante
    float_decimal DW ?          ; Parte decimal del flotante
    dec_digitos  DB ?           ; Número de dígitos decimales
    
    ; Variable para valor string
    string_buffer DB 2 DUP(?), '$' ; Buffer para la conversión a string (caracter + terminador)
    
    ; Variables para valor creativo (probabilidad)
    prob_valor   DB ?           ; Valor de la probabilidad (0.0 o 1.0)
    
    ; Valores para mostrar booleanos
    valor_true   DB 'TRUE$'      ; Cadena de texto para mostrar cuando el valor es verdadero
    valor_false  DB 'FALSE$'     ; Cadena de texto para mostrar cuando el valor es falso
    
    ; Auxiliares
    nueva_lin    DB 0Dh, 0Ah, '$' ; Códigos para crear una nueva línea en pantalla
    punto        DB '.$'          ; Punto decimal para mostrar flotantes
    const_diez   DW 10            ; Constante 10 para cálculos
DATOS ENDS

; El segmento CODIGO contiene las instrucciones que ejecutara el programa
CODIGO SEGMENT
    ; Indicamos al ensamblador donde encontrar nuestros datos y codigo
    ASSUME CS:CODIGO, DS:DATOS
INICIO:
    ; Inicializacion: Preparamos el acceso al segmento de datos
    MOV AX, DATOS
    MOV DS, AX
    
    ; Mostramos el mensaje pidiendo al usuario que ingrese un caracter
    MOV AH, 09h       ; Funcion 9 de DOS: mostrar una cadena terminada en $
    LEA DX, prompt_in ; Cargamos la direccion del mensaje en DX
    INT 21h           ; Llamamos a la interrupcion 21h (servicios de DOS)
    
    ; Leemos un caracter del teclado
    MOV AH, 01h       ; Funcion 1 de DOS: leer un caracter (con eco en pantalla)
    INT 21h           ; Llamamos a la interrupcion 21h - El caracter leido queda en AL
    MOV [caracter], AL ; Guardamos el caracter en nuestra variable
    
    ; Realizar todas las conversiones desde el caracter
    CALL CHAR_A_ENTERO    ; Convertir a entero (código ASCII)
    CALL CHAR_A_FLOTANTE  ; Convertir a flotante
    CALL CHAR_A_BOOLEANO  ; Convertir a booleano
    CALL CHAR_A_STRING    ; Convertir a string
    CALL CHAR_A_CREATIVO  ; Convertir a creativo (probabilidad)
    
    ; Mostrar todas las conversiones
    CALL MOSTRAR_RESULTADOS
    
    ; Terminamos el programa y regresamos al sistema operativo
    MOV AX, 4C00h      ; Funcion 4Ch de DOS: terminar programa (con codigo de salida 0)
    INT 21h            ; Llamamos a la interrupcion 21h

;------------------------------------------------------------
; Procedimiento: CHAR_A_ENTERO
; Convierte el caracter a su valor ASCII (entero)
;------------------------------------------------------------
CHAR_A_ENTERO PROC
    ; Para caracter a entero, simplemente copiamos el valor ASCII
    XOR AX, AX                ; Limpiamos AX
    MOV AL, [caracter]        ; Cargamos el caracter en AL
    MOV [entero], AX          ; Guardamos el código ASCII como entero
    
    RET
CHAR_A_ENTERO ENDP

;------------------------------------------------------------
; Procedimiento: CHAR_A_FLOTANTE
; Convierte el caracter a flotante (valor ASCII.00)
;------------------------------------------------------------
CHAR_A_FLOTANTE PROC
    ; Para caracter a flotante, usamos el valor ASCII como parte entera
    ; y la parte decimal es siempre 0
    XOR AX, AX                ; Limpiamos AX
    MOV AL, [caracter]        ; Cargamos el caracter en AL
    MOV [float_entero], AX    ; Guardamos en la parte entera del flotante
    
    ; La parte decimal es siempre 0 para esta conversión
    MOV WORD PTR [float_decimal], 0
    MOV BYTE PTR [dec_digitos], 2     ; Dos dígitos decimales (00)
    
    RET
CHAR_A_FLOTANTE ENDP

;------------------------------------------------------------
; Procedimiento: CHAR_A_BOOLEANO
; Convierte el caracter a booleano (FALSE si ASCII=0, TRUE en caso contrario)
;------------------------------------------------------------
CHAR_A_BOOLEANO PROC
    ; Para caracter a booleano, es FALSE solo si el código ASCII es 0
    CMP BYTE PTR [caracter], 0
    JE ES_FALSO
    
    ; Si llegamos aquí, el caracter tiene código ASCII distinto de 0
    MOV [bool_valor], 1       ; TRUE
    JMP BOOL_FIN
    
ES_FALSO:
    MOV [bool_valor], 0       ; FALSE
    
BOOL_FIN:
    RET
CHAR_A_BOOLEANO ENDP

;------------------------------------------------------------
; Procedimiento: CHAR_A_STRING
; Convierte el caracter a un string de longitud 1
;------------------------------------------------------------
CHAR_A_STRING PROC
    ; Para caracter a string, simplemente copiamos el caracter
    ; y agregamos el terminador
    MOV AL, [caracter]
    MOV [string_buffer], AL   ; Primer y único caracter del string
    MOV BYTE PTR [string_buffer+1], '$' ; Terminador de string
    
    RET
CHAR_A_STRING ENDP

;------------------------------------------------------------
; Procedimiento: CHAR_A_CREATIVO
; Convierte el caracter a valor de probabilidad (0.0 o 1.0)
;------------------------------------------------------------
CHAR_A_CREATIVO PROC
    ; Para caracter a creativo (probabilidad):
    ; Si ASCII=0, entonces 0, en caso contrario 1
    CMP BYTE PTR [caracter], 0
    JE PROB_CERO
    
    ; Si llegamos aquí, el valor es distinto de 0
    MOV [prob_valor], 1      ; Probabilidad = 1.0
    JMP PROB_FIN
    
PROB_CERO:
    MOV [prob_valor], 0      ; Probabilidad = 0.0
    
PROB_FIN:
    RET
CHAR_A_CREATIVO ENDP

;------------------------------------------------------------
; Procedimiento: MOSTRAR_RESULTADOS
; Muestra el resultado original y todas las conversiones
;------------------------------------------------------------
MOSTRAR_RESULTADOS PROC
    ; Mostramos una nueva línea
    MOV AH, 09h
    LEA DX, nueva_lin
    INT 21h
    
    ; 1. Mostrar el caracter original
    MOV AH, 09h
    LEA DX, prompt_char
    INT 21h
    
    MOV DL, [caracter]      ; Caracter a mostrar
    MOV AH, 02h             ; Función 2: mostrar caracter
    INT 21h
    
    ; Nueva línea
    MOV AH, 09h
    LEA DX, nueva_lin
    INT 21h
    
    ; 2. Mostrar conversión a entero (ASCII)
    MOV AH, 09h
    LEA DX, prompt_int
    INT 21h
    
    MOV AX, [entero]
    CALL MOSTRAR_ENTERO
    
    ; Nueva línea
    MOV AH, 09h
    LEA DX, nueva_lin
    INT 21h
    
    ; 3. Mostrar conversión a flotante
    MOV AH, 09h
    LEA DX, prompt_float
    INT 21h
    
    CALL MOSTRAR_FLOTANTE
    
    ; Nueva línea
    MOV AH, 09h
    LEA DX, nueva_lin
    INT 21h
    
    ; 4. Mostrar conversión a booleano
    MOV AH, 09h
    LEA DX, prompt_bool
    INT 21h
    
    ; Decidir si mostrar "TRUE" o "FALSE"
    CMP [bool_valor], 0
    JE MOSTRAR_BOOL_FALSE
    
    MOV AH, 09h
    LEA DX, valor_true
    INT 21h
    JMP MOSTRAR_STR
    
MOSTRAR_BOOL_FALSE:
    MOV AH, 09h
    LEA DX, valor_false
    INT 21h
    
MOSTRAR_STR:
    ; Nueva línea
    MOV AH, 09h
    LEA DX, nueva_lin
    INT 21h
    
    ; 5. Mostrar conversión a string
    MOV AH, 09h
    LEA DX, prompt_str
    INT 21h
    
    MOV AH, 09h
    LEA DX, string_buffer
    INT 21h
    
    ; Nueva línea
    MOV AH, 09h
    LEA DX, nueva_lin
    INT 21h
    
    ; 6. Mostrar conversión a creativo (probabilidad)
    MOV AH, 09h
    LEA DX, prompt_creativo
    INT 21h
    
    ; Para el tipo creativo de probabilidad mostramos "0.00" o "1.00"
    MOV DL, [prob_valor]
    ADD DL, '0'         ; Convertir a carácter
    MOV AH, 02h         ; Función 2: mostrar carácter
    INT 21h
    
    ; Mostrar punto decimal
    MOV AH, 09h
    LEA DX, punto
    INT 21h
    
    ; Mostrar dos ceros para la parte decimal
    MOV DL, '0'
    MOV AH, 02h
    INT 21h
    
    MOV DL, '0'
    MOV AH, 02h
    INT 21h
    
    RET
MOSTRAR_RESULTADOS ENDP

;------------------------------------------------------------
; Procedimiento: MOSTRAR_ENTERO
; Muestra un número entero en pantalla
; Entrada: AX = número a mostrar
;------------------------------------------------------------
MOSTRAR_ENTERO PROC
    ; Guardamos los registros que vamos a modificar
    PUSH AX
    PUSH BX
    PUSH CX
    PUSH DX
    
    ; Verificamos si el número es cero
    CMP AX, 0
    JNE ENTERO_NO_CERO
    
    ; Si es cero, mostrar '0' y terminar
    MOV DL, '0'
    MOV AH, 02h
    INT 21h
    JMP FIN_MOSTRAR_ENTERO
    
ENTERO_NO_CERO:
    ; Verificamos si el número es negativo
    CMP AX, 0
    JGE ENTERO_POSITIVO
    
    ; Si es negativo, mostrar '-' y negar el número
    PUSH AX
    MOV DL, '-'
    MOV AH, 02h
    INT 21h
    POP AX
    NEG AX
    
ENTERO_POSITIVO:
    ; Convertir el número a dígitos usando división por 10
    MOV BX, 10          ; Divisor = 10
    XOR CX, CX          ; Contador de dígitos = 0
    
DIVISION_LOOP:
    XOR DX, DX          ; Limpiar DX para división
    DIV BX              ; AX = AX / 10, DX = resto (dígito)
    
    PUSH DX             ; Guardar dígito en la pila
    INC CX              ; Incrementar contador de dígitos
    
    CMP AX, 0           ; ¿Terminamos?
    JNE DIVISION_LOOP   ; Si no, continuar con la división
    
    ; Mostrar los dígitos en orden inverso (de la pila)
MOSTRAR_DIGITOS:
    POP DX              ; Obtener dígito de la pila
    ADD DL, '0'         ; Convertir a carácter ASCII
    MOV AH, 02h         ; Función 2: mostrar carácter
    INT 21h             ; Mostrar el dígito
    LOOP MOSTRAR_DIGITOS ; Repetir para cada dígito
    
FIN_MOSTRAR_ENTERO:
    ; Restaurar registros
    POP DX
    POP CX
    POP BX
    POP AX
    RET
MOSTRAR_ENTERO ENDP

;------------------------------------------------------------
; Procedimiento: MOSTRAR_FLOTANTE
; Muestra un número flotante en pantalla
;------------------------------------------------------------
MOSTRAR_FLOTANTE PROC
    ; Guardamos los registros que vamos a modificar
    PUSH AX
    PUSH BX
    PUSH CX
    PUSH DX
    
    ; Mostrar la parte entera
    MOV AX, [float_entero]
    CALL MOSTRAR_ENTERO
    
    ; Mostrar el punto decimal
    MOV AH, 09h
    LEA DX, punto
    INT 21h
    
    ; Verificar si hay dígitos decimales
    CMP BYTE PTR [dec_digitos], 0
    JE FLOTANTE_SIN_DECIMALES

    ; Mostrar la parte decimal
    XOR CH, CH                ; Limpiar la parte alta (CH)
    MOV CL, [dec_digitos]     ; Cargar el byte en la parte baja (CL)

    ; Si la parte decimal es 0, mostrar todos los dígitos como ceros
    CMP WORD PTR [float_decimal], 0
    JNE DECIMALES_NO_CERO
        
MOSTRAR_SOLO_CEROS:
    MOV DL, '0'
    MOV AH, 02h
    INT 21h
    
    LOOP MOSTRAR_SOLO_CEROS
    JMP FIN_MOSTRAR_FLOTANTE
    
DECIMALES_NO_CERO:
    ; Si llegamos aquí, tenemos decimales distintos de cero
    ; (pero para esta conversión siempre son ceros)
    JMP MOSTRAR_SOLO_CEROS
    
FLOTANTE_SIN_DECIMALES:
    ; Si no hay decimales, mostrar un 0
    MOV DL, '0'
    MOV AH, 02h
    INT 21h
    
FIN_MOSTRAR_FLOTANTE:
    ; Restaurar registros
    POP DX
    POP CX
    POP BX
    POP AX
    RET
MOSTRAR_FLOTANTE ENDP

CODIGO ENDS
END INICIO              ; Indicamos el punto de entrada del programa