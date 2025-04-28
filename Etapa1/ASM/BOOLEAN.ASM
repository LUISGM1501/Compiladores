; ********************************************
; * Programa: BOOLEAN.ASM                   *
; * Descripcion: Conversiones desde booleano*
; * Autores: Luis Urbina, Samir Cabrera     *
; * Fecha de entrega: 28/04/2025            *
; ********************************************

; El segmento DATOS contiene todas las variables y constantes que usara el programa
DATOS SEGMENT
    ; Mensajes de entrada y salida
    prompt_in    DB 'Ingrese 1 para TRUE o 0 para FALSE: $'  ; Mensaje para solicitar entrada al usuario
    prompt_bool  DB 'El valor booleano es: $'                ; Mensaje para mostrar el valor booleano original
    prompt_int   DB 'Convertido a entero: $'                 ; Mensaje para mostrar la conversión a entero
    prompt_float DB 'Convertido a flotante: $'               ; Mensaje para mostrar la conversión a flotante
    prompt_char  DB 'Convertido a caracter: $'               ; Mensaje para mostrar la conversión a carácter
    prompt_str   DB 'Convertido a string: $'                 ; Mensaje para mostrar la conversión a string
    prompt_creativo DB 'Convertido a creativo (probabilidad): $' ; Mensaje para conversión a creativo

    ; Valores para mostrar booleanos
    valor_true   DB 'TRUE$'       ; Cadena de texto para mostrar cuando el valor es verdadero
    valor_false  DB 'FALSE$'      ; Cadena de texto para mostrar cuando el valor es falso
    
    ; Variables para almacenar valores
    booleano     DB ?             ; Variable para almacenar el valor booleano (1 = TRUE, 0 = FALSE)
    entero       DW ?             ; Variable para almacenar el valor convertido a entero
    
    ; Variables para valor flotante
    float_entero DW ?             ; Parte entera del flotante
    float_decimal DW ?            ; Parte decimal del flotante
    dec_digitos  DB ?             ; Número de dígitos decimales
    
    ; Variables para valor creativo (probabilidad)
    prob_valor   DB ?             ; Valor de la probabilidad (0.0 o 1.0)
    
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
    
    ; Mostramos el mensaje pidiendo al usuario que ingrese un 1 o un 0
    MOV AH, 09h       ; Funcion 9 de DOS: mostrar una cadena terminada en $
    LEA DX, prompt_in ; Cargamos la direccion del mensaje en DX
    INT 21h           ; Llamamos a la interrupcion 21h (servicios de DOS)
    
    ; Leemos un caracter del teclado
    MOV AH, 01h       ; Funcion 1 de DOS: leer un caracter (con eco en pantalla)
    INT 21h           ; Llamamos a la interrupcion 21h - El caracter leido queda en AL
    
    ; Verificamos si el caracter ingresado es '1' o '0'
    CMP AL, '1'       ; ¿El caracter es '1'?
    JE ES_TRUE        ; Si es '1', saltamos a ES_TRUE
    CMP AL, '0'       ; ¿El caracter es '0'?
    JE ES_FALSE       ; Si es '0', saltamos a ES_FALSE
    
    ; Si no es ni '1' ni '0', consideramos como FALSE por defecto
ES_FALSE:
    MOV [booleano], 0 ; Almacenamos 0 (FALSE) en la variable booleano
    JMP REALIZAR_CONVERSIONES
    
ES_TRUE:
    MOV [booleano], 1 ; Almacenamos 1 (TRUE) en la variable booleano
    
REALIZAR_CONVERSIONES:
    ; Convertir booleano a todos los demás tipos
    CALL BOOL_A_ENTERO    ; Convertir a entero
    CALL BOOL_A_FLOTANTE  ; Convertir a flotante
    CALL BOOL_A_CREATIVO  ; Convertir a creativo (probabilidad)
    
    ; Ahora mostramos todas las conversiones
    CALL MOSTRAR_RESULTADO
    
    ; Terminamos el programa y regresamos al sistema operativo
    MOV AX, 4C00h      ; Funcion 4Ch de DOS: terminar programa (con codigo de salida 0)
    INT 21h            ; Llamamos a la interrupcion 21h

;------------------------------------------------------------
; Procedimiento: BOOL_A_ENTERO
; Convierte el valor booleano a un entero (0 o 1)
;------------------------------------------------------------
BOOL_A_ENTERO PROC
    ; Para booleano a entero, simplemente copiamos el valor
    ; 0 (false) -> 0, 1 (true) -> 1
    XOR AX, AX                ; Limpiamos AX
    MOV AL, [booleano]        ; Cargamos el valor booleano en AL
    MOV [entero], AX          ; Guardamos en la variable entero
    
    RET
BOOL_A_ENTERO ENDP

;------------------------------------------------------------
; Procedimiento: BOOL_A_FLOTANTE 
; Convierte el valor booleano a un flotante (0.0 o 1.0)
;------------------------------------------------------------
BOOL_A_FLOTANTE PROC
    ; Para booleano a flotante, usamos 0.0 para false y 1.0 para true
    XOR AX, AX                ; Limpiamos AX
    MOV AL, [booleano]        ; Cargamos el valor booleano en AL
    MOV [float_entero], AX    ; Guardamos en la parte entera del flotante
    
    ; La parte decimal es siempre 0 para 0.0 y 1.0
    MOV WORD PTR [float_decimal], 0
    MOV BYTE PTR [dec_digitos], 1     ; Un dígito decimal (el cero)
    
    RET
BOOL_A_FLOTANTE ENDP

;------------------------------------------------------------
; Procedimiento: BOOL_A_CREATIVO
; Convierte el valor booleano a un valor de probabilidad (0.0 o 1.0)
;------------------------------------------------------------
BOOL_A_CREATIVO PROC
    ; Para la conversión a nuestro tipo creativo (probabilidad)
    ; usamos el mismo valor que el booleano (0 o 1)
    MOV AL, [booleano]
    MOV [prob_valor], AL
    
    RET
BOOL_A_CREATIVO ENDP

;------------------------------------------------------------
; Procedimiento: MOSTRAR_RESULTADO
; Muestra el resultado original y todas las conversiones
;------------------------------------------------------------
MOSTRAR_RESULTADO PROC
    ; Mostramos una nueva línea
    MOV AH, 09h
    LEA DX, nueva_lin
    INT 21h
    
    ; 1. Mostrar el valor booleano original
    MOV AH, 09h
    LEA DX, prompt_bool
    INT 21h
    
    ; Decidir si mostrar "TRUE" o "FALSE"
    CMP [booleano], 0
    JE MOSTRAR_BOOL_FALSE
    
    MOV AH, 09h
    LEA DX, valor_true
    INT 21h
    JMP MOSTRAR_SIGUIENTE
    
MOSTRAR_BOOL_FALSE:
    MOV AH, 09h
    LEA DX, valor_false
    INT 21h
    
MOSTRAR_SIGUIENTE:
    ; Nueva línea
    MOV AH, 09h
    LEA DX, nueva_lin
    INT 21h
    
    ; 2. Mostrar conversión a entero
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
    
    ; 4. Mostrar conversión a carácter
    MOV AH, 09h
    LEA DX, prompt_char
    INT 21h
    
    ; Para booleano a carácter usamos '0' o '1'
    MOV DL, '0'            ; Carácter base '0'
    ADD DL, [booleano]     ; Sumamos 0 o 1 para obtener '0' o '1'
    MOV AH, 02h            ; Función 2: mostrar carácter
    INT 21h
    
    ; Nueva línea
    MOV AH, 09h
    LEA DX, nueva_lin
    INT 21h
    
    ; 5. Mostrar conversión a string
    MOV AH, 09h
    LEA DX, prompt_str
    INT 21h
    
    ; Para booleano a string usamos "false" o "true"
    CMP [booleano], 0
    JE MOSTRAR_STR_FALSE
    
    MOV AH, 09h
    LEA DX, valor_true
    INT 21h
    JMP MOSTRAR_CREATIVO
    
MOSTRAR_STR_FALSE:
    MOV AH, 09h
    LEA DX, valor_false
    INT 21h
    
MOSTRAR_CREATIVO:
    ; Nueva línea
    MOV AH, 09h
    LEA DX, nueva_lin
    INT 21h
    
    ; 6. Mostrar conversión a creativo (probabilidad)
    MOV AH, 09h
    LEA DX, prompt_creativo
    INT 21h
    
    ; Para el tipo creativo de probabilidad mostramos "0.0" o "1.0"
    MOV DL, [prob_valor]
    ADD DL, '0'         ; Convertir a carácter
    MOV AH, 02h         ; Función 2: mostrar carácter
    INT 21h
    
    ; Mostrar punto decimal
    MOV AH, 09h
    LEA DX, punto
    INT 21h
    
    ; Mostrar el decimal (siempre es 0)
    MOV DL, '0'
    MOV AH, 02h
    INT 21h
    
    RET
MOSTRAR_RESULTADO ENDP

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
    MOV AX, [float_decimal]
    
    ; Si la parte decimal es 0, mostrar un solo 0
    CMP AX, 0
    JNE DECIMALES_NO_CERO
    
    MOV DL, '0'
    MOV AH, 02h
    INT 21h
    JMP FIN_MOSTRAR_FLOTANTE
    
DECIMALES_NO_CERO:
    ; Convertir la parte decimal a dígitos
    ; [Aquí iría la lógica para mostrar decimales distintos de cero]
    ; Para nuestro caso de booleano, siempre es 0.0 o 1.0, así que mostramos un cero
    MOV DL, '0'
    MOV AH, 02h
    INT 21h
    
    JMP FIN_MOSTRAR_FLOTANTE
    
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