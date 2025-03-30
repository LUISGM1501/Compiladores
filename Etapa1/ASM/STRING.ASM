; ********************************************
; * Programa: STRING.ASM                    *
; * Descripcion: Conversiones desde string  *
; * Autores: Luis Urbina, Samir Cabrera     *
; * Fecha de entrega: 10/04/2025            *
; ********************************************

; El segmento DATOS contiene todas las variables y constantes que usara el programa
DATOS SEGMENT
    ; Mensajes de entrada y salida
    prompt_in    DB 'Ingrese un texto (max 50 caracteres): $'  ; Mensaje para solicitar entrada
    prompt_str   DB 'El texto ingresado es: $'                 ; Mensaje para mostrar el texto original
    prompt_int   DB 'Convertido a entero (ASCII total): $'     ; Mensaje para conversión a entero
    prompt_float DB 'Convertido a flotante: $'                 ; Mensaje para conversión a flotante
    prompt_bool  DB 'Convertido a booleano: $'                 ; Mensaje para conversión a booleano
    prompt_char  DB 'Convertido a caracter: $'                 ; Mensaje para conversión a carácter
    prompt_creativo DB 'Convertido a creativo (probabilidad): $' ; Mensaje para conversión a creativo
    
    ; Valores para mostrar booleanos
    valor_true   DB 'TRUE$'       ; Cadena para mostrar cuando el valor es verdadero
    valor_false  DB 'FALSE$'      ; Cadena para mostrar cuando el valor es falso
    
    ; Buffer para la entrada del usuario
    buffer       DB 52, ?, 52 DUP(?)  ; Buffer para entrada
    
    ; Variables para almacenar conversiones
    texto_len    DW ?             ; Longitud del texto ingresado
    ascii_total  DW ?             ; Suma de todos los valores ASCII
    primer_char  DB ?             ; Primer carácter del texto
    es_booleano  DB ?             ; Resultado de la conversión a booleano (0=falso, 1=verdadero)
    
    ; Variables para flotante
    float_entero DW ?             ; Parte entera del flotante
    float_decimal DW ?            ; Parte decimal del flotante
    dec_digitos  DB ?             ; Número de dígitos decimales
    
    ; Variables para probabilidad (tipo creativo)
    prob_valor   DB ?             ; Valor de la probabilidad (0-9)
    
    ; Valores para comparación de strings
    str_true     DB 'TRUE', 0     ; String para comparar con "TRUE"
    str_false    DB 'FALSE', 0    ; String para comparar con "FALSE"
    
    ; Auxiliares
    nueva_lin    DB 0Dh, 0Ah, '$' ; Códigos para nueva línea
    punto        DB '.$'          ; Punto decimal para mostrar flotantes
    const_diez   DW 10            ; Constante 10 para cálculos
DATOS ENDS

; El segmento CODIGO contiene las instrucciones que ejecutara el programa
CODIGO SEGMENT
    ; Indicamos al ensamblador donde encontrar nuestros datos y codigo
    ASSUME CS:CODIGO, DS:DATOS
INICIO:
    ; Inicialización: Preparamos el acceso al segmento de datos
    MOV AX, DATOS
    MOV DS, AX
    
    ; Mostramos el mensaje pidiendo al usuario que ingrese un texto
    MOV AH, 09h       ; Función 9 de DOS: mostrar una cadena terminada en $
    LEA DX, prompt_in ; Cargamos la dirección del mensaje en DX
    INT 21h           ; Llamamos a la interrupción 21h (servicios de DOS)
    
    ; Leemos una cadena de texto del teclado
    MOV AH, 0Ah       ; Función 0Ah de DOS: leer una cadena (con buffer)
    LEA DX, buffer    ; Cargamos la dirección del buffer en DX
    INT 21h           ; Llamamos a la interrupción 21h
    
    ; Agregamos un terminador $ al final del texto ingresado para poder mostrarlo después
    MOV BL, [buffer+1]    ; En buffer+1 está la cantidad de caracteres leídos
    XOR BH, BH            ; Limpiamos BH (para que BX solo contenga el valor de BL)
    MOV BYTE PTR [buffer+BX+2], '$' ; Colocamos el terminador $ después del último carácter
    MOV [texto_len], BX   ; Guardamos la longitud del texto
    
    ; Realizar todas las conversiones
    CALL STRING_A_ENTERO      ; Convertir a entero (ASCII total)
    CALL STRING_A_FLOTANTE    ; Convertir a flotante
    CALL STRING_A_BOOLEANO    ; Convertir a booleano
    CALL STRING_A_CARACTER    ; Convertir a carácter
    CALL STRING_A_CREATIVO    ; Convertir a creativo (probabilidad)
    
    ; Mostrar todas las conversiones
    CALL MOSTRAR_RESULTADOS
    
    ; Terminamos el programa y regresamos al sistema operativo
    MOV AX, 4C00h      ; Función 4Ch de DOS: terminar programa (con código de salida 0)
    INT 21h            ; Llamamos a la interrupción 21h

;------------------------------------------------------------
; Procedimiento: STRING_A_ENTERO
; Convierte el string a un entero (suma de valores ASCII)
;------------------------------------------------------------
STRING_A_ENTERO PROC
    PUSH SI            ; Guardamos SI para restaurarlo después
    PUSH AX            ; Guardamos AX
    PUSH BX            ; Guardamos BX
    PUSH CX            ; Guardamos CX
    
    ; Inicializar contador ASCII total a 0
    MOV WORD PTR [ascii_total], 0
    
    ; Verificar si el string está vacío
    MOV CX, [texto_len]
    CMP CX, 0
    JE FIN_SUMA_ASCII
    
    ; Configurar índice para recorrer el string
    LEA SI, [buffer+2]     ; SI apunta al primer carácter
    
SUMA_ASCII_LOOP:
    XOR AX, AX            ; Limpiamos AX
    MOV AL, [SI]          ; Obtenemos el carácter actual
    ADD [ascii_total], AX ; Sumamos su valor ASCII al total
    
    INC SI                ; Avanzamos al siguiente carácter
    LOOP SUMA_ASCII_LOOP  ; Repetimos para cada carácter (CX veces)
    
FIN_SUMA_ASCII:
    POP CX                ; Restauramos CX
    POP BX                ; Restauramos BX
    POP AX                ; Restauramos AX
    POP SI                ; Restauramos SI
    RET
STRING_A_ENTERO ENDP

;------------------------------------------------------------
; Procedimiento: STRING_A_FLOTANTE
; Convierte el string a un flotante (ASCII total con .00)
;------------------------------------------------------------
STRING_A_FLOTANTE PROC
    PUSH AX            ; Guardamos AX
    
    ; Para este ejemplo, usamos el valor ASCII total como parte entera
    ; y agregamos .00 como parte decimal
    MOV AX, [ascii_total]
    MOV [float_entero], AX
    MOV WORD PTR [float_decimal], 0  ; Parte decimal es 00
    MOV BYTE PTR [dec_digitos], 2    ; Dos dígitos decimales
    
    POP AX             ; Restauramos AX
    RET
STRING_A_FLOTANTE ENDP

;------------------------------------------------------------
; Procedimiento: STRING_A_BOOLEANO
; Convierte el string a un booleano
; - "TRUE"/"true" o "1" -> verdadero
; - "FALSE"/"false" o "0" -> falso
; - Cualquier otro -> falso
;------------------------------------------------------------
STRING_A_BOOLEANO PROC
    PUSH SI            ; Guardamos SI
    PUSH DI            ; Guardamos DI
    PUSH AX            ; Guardamos AX
    PUSH BX            ; Guardamos BX
    PUSH CX            ; Guardamos CX
    
    ; Por defecto, el resultado es falso
    MOV BYTE PTR [es_booleano], 0
    
    ; Verificar si el string está vacío
    MOV CX, [texto_len]
    CMP CX, 0
    JE FIN_CONVERSION_BOOL
    
    ; Verificar si es "1" (un solo carácter y es '1')
    CMP CX, 1
    JNE VERIFICAR_CERO
    
    LEA SI, [buffer+2]         ; SI apunta al primer carácter
    CMP BYTE PTR [SI], '1'     ; ¿Es '1'?
    JNE VERIFICAR_CERO
    
    ; Es "1", por lo tanto es verdadero
    MOV BYTE PTR [es_booleano], 1
    JMP FIN_CONVERSION_BOOL
    
VERIFICAR_CERO:
    ; Verificar si es "0" (un solo carácter y es '0')
    CMP CX, 1
    JNE VERIFICAR_TRUE
    
    LEA SI, [buffer+2]         ; SI apunta al primer carácter
    CMP BYTE PTR [SI], '0'     ; ¿Es '0'?
    JNE VERIFICAR_TRUE
    
    ; Es "0", por lo tanto es falso (ya está inicializado a 0)
    JMP FIN_CONVERSION_BOOL
    
VERIFICAR_TRUE:
    ; Verificar si es "TRUE" (cualquier combinación de mayúsculas/minúsculas)
    ; Simplificación: solo verificamos exactamente "TRUE" o "true"
    CMP CX, 4
    JNE VERIFICAR_FALSE
    
    ; Verificar "TRUE"
    LEA SI, [buffer+2]         ; SI apunta al primer carácter
    LEA DI, [str_true]         ; DI apunta a "TRUE"
    
    ; Comparamos ignorando mayúsculas/minúsculas
    MOV BX, CX                 ; BX = longitud
    
COMP_TRUE_LOOP:
    MOV AL, [SI]               ; AL = carácter del string
    MOV AH, [DI]               ; AH = carácter de "TRUE"
    
    ; Convertir a mayúsculas si es minúscula
    CMP AL, 'a'
    JB NO_CONV_AL
    CMP AL, 'z'
    JA NO_CONV_AL
    SUB AL, 32                 ; Convertir a mayúscula
NO_CONV_AL:
    
    CMP AL, AH                 ; Comparar caracteres
    JNE VERIFICAR_FALSE       ; Si no son iguales, no es "TRUE"
    
    INC SI                     ; Siguiente carácter del string
    INC DI                     ; Siguiente carácter de "TRUE"
    DEC BX                     ; Decrementar contador
    
    CMP BX, 0                  ; ¿Terminamos?
    JNE COMP_TRUE_LOOP
    
    ; Si llegamos aquí, el string es "TRUE"
    MOV BYTE PTR [es_booleano], 1
    JMP FIN_CONVERSION_BOOL
    
VERIFICAR_FALSE:
    ; Verificar si es "FALSE" (cualquier combinación de mayúsculas/minúsculas)
    ; Simplificación: solo verificamos exactamente "FALSE" o "false"
    CMP CX, 5
    JNE FIN_CONVERSION_BOOL
    
    ; Verificar "FALSE"
    LEA SI, [buffer+2]         ; SI apunta al primer carácter
    LEA DI, [str_false]        ; DI apunta a "FALSE"
    
    ; Comparamos ignorando mayúsculas/minúsculas
    MOV BX, CX                 ; BX = longitud
    
COMP_FALSE_LOOP:
    MOV AL, [SI]               ; AL = carácter del string
    MOV AH, [DI]               ; AH = carácter de "FALSE"
    
    ; Convertir a mayúsculas si es minúscula
    CMP AL, 'a'
    JB NO_CONV_AL2
    CMP AL, 'z'
    JA NO_CONV_AL2
    SUB AL, 32                 ; Convertir a mayúscula
NO_CONV_AL2:
    
    CMP AL, AH                 ; Comparar caracteres
    JNE FIN_CONVERSION_BOOL    ; Si no son iguales, no es "FALSE"
    
    INC SI                     ; Siguiente carácter del string
    INC DI                     ; Siguiente carácter de "FALSE"
    DEC BX                     ; Decrementar contador
    
    CMP BX, 0                  ; ¿Terminamos?
    JNE COMP_FALSE_LOOP
    
    ; Si llegamos aquí, el string es "FALSE"
    ; (ya está inicializado a 0)
    
FIN_CONVERSION_BOOL:
    POP CX                     ; Restauramos CX
    POP BX                     ; Restauramos BX
    POP AX                     ; Restauramos AX
    POP DI                     ; Restauramos DI
    POP SI                     ; Restauramos SI
    RET
STRING_A_BOOLEANO ENDP

;------------------------------------------------------------
; Procedimiento: STRING_A_CARACTER
; Convierte el string a un carácter (toma el primer carácter)
;------------------------------------------------------------
STRING_A_CARACTER PROC
    PUSH SI            ; Guardamos SI
    PUSH AX            ; Guardamos AX
    
    ; Por defecto, si el string está vacío, usamos espacio
    MOV BYTE PTR [primer_char], ' '
    
    ; Verificar si el string está vacío
    MOV AX, [texto_len]
    CMP AX, 0
    JE FIN_CONVERSION_CHAR
    
    ; Tomar el primer carácter
    LEA SI, [buffer+2]        ; SI apunta al primer carácter
    MOV AL, [SI]              ; AL = primer carácter
    MOV [primer_char], AL     ; Guardamos el primer carácter
    
FIN_CONVERSION_CHAR:
    POP AX                    ; Restauramos AX
    POP SI                    ; Restauramos SI
    RET
STRING_A_CARACTER ENDP

;------------------------------------------------------------
; Procedimiento: STRING_A_CREATIVO
; Convierte el string a un valor de probabilidad (0.0-0.9)
; usando el primer dígito del ASCII total
;------------------------------------------------------------
STRING_A_CREATIVO PROC
    PUSH AX            ; Guardamos AX
    PUSH BX            ; Guardamos BX
    PUSH CX            ; Guardamos CX
    PUSH DX            ; Guardamos DX
    
    ; Utilizamos el ASCII total calculado previamente
    MOV AX, [ascii_total]
    
    ; Si el ASCII total es 0, usamos 0 como probabilidad
    CMP AX, 0
    JE PROB_CERO
    
    ; Encontrar el primer dígito dividiendo por 10 repetidamente
ENCONTRAR_PRIMER_DIGITO:
    CMP AX, 10
    JL USAR_DIGITO     ; Si AX < 10, ya tenemos un solo dígito
    
    XOR DX, DX         ; Limpiar DX para división
    MOV BX, 10         ; Divisor = 10
    DIV BX             ; AX = AX / 10, DX = resto
    
    CMP AX, 0          ; Si el cociente es 0, usar el resto (DX)
    JE USAR_RESTO
    
    JMP ENCONTRAR_PRIMER_DIGITO
    
USAR_RESTO:
    MOV AX, DX         ; Usar el resto como el dígito
    
USAR_DIGITO:
    ; AX contiene ahora el primer dígito (0-9)
    MOV [prob_valor], AL
    JMP FIN_CONVERSION_PROB
    
PROB_CERO:
    MOV BYTE PTR [prob_valor], 0
    
FIN_CONVERSION_PROB:
    POP DX             ; Restauramos DX
    POP CX             ; Restauramos CX
    POP BX             ; Restauramos BX
    POP AX             ; Restauramos AX
    RET
STRING_A_CREATIVO ENDP

;------------------------------------------------------------
; Procedimiento: MOSTRAR_RESULTADOS
; Muestra el resultado original y todas las conversiones
;------------------------------------------------------------
MOSTRAR_RESULTADOS PROC
    ; Nueva línea
    MOV AH, 09h
    LEA DX, nueva_lin
    INT 21h
    
    ; 1. Mostrar el texto original
    MOV AH, 09h
    LEA DX, prompt_str
    INT 21h
    
    MOV AH, 09h
    LEA DX, [buffer+2]     ; Mostrar el texto ingresado
    INT 21h
    
    ; Nueva línea
    MOV AH, 09h
    LEA DX, nueva_lin
    INT 21h
    
    ; 2. Mostrar conversión a entero (ASCII total)
    MOV AH, 09h
    LEA DX, prompt_int
    INT 21h
    
    MOV AX, [ascii_total]
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
    
    CMP BYTE PTR [es_booleano], 0
    JE MOSTRAR_BOOL_FALSE
    
    MOV AH, 09h
    LEA DX, valor_true
    INT 21h
    JMP MOSTRAR_SIGUIENTE1
    
MOSTRAR_BOOL_FALSE:
    MOV AH, 09h
    LEA DX, valor_false
    INT 21h
    
MOSTRAR_SIGUIENTE1:
    ; Nueva línea
    MOV AH, 09h
    LEA DX, nueva_lin
    INT 21h
    
    ; 5. Mostrar conversión a carácter
    MOV AH, 09h
    LEA DX, prompt_char
    INT 21h
    
    MOV DL, [primer_char]
    MOV AH, 02h            ; Función 2: mostrar carácter
    INT 21h
    
    ; Nueva línea
    MOV AH, 09h
    LEA DX, nueva_lin
    INT 21h
    
    ; 6. Mostrar conversión a creativo (probabilidad)
    MOV AH, 09h
    LEA DX, prompt_creativo
    INT 21h
    
    ; Mostrar el formato 0.X donde X es el valor de probabilidad
    MOV DL, '0'            ; Siempre comenzamos con 0.
    MOV AH, 02h
    INT 21h
    
    ; Mostrar punto decimal
    MOV AH, 09h
    LEA DX, punto
    INT 21h
    
    ; Mostrar el dígito de probabilidad
    MOV DL, [prob_valor]
    ADD DL, '0'            ; Convertir a carácter
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
    
    ; Para este ejemplo simplificado, siempre mostramos "00" como parte decimal
    MOV DL, '0'
    MOV AH, 02h
    INT 21h
    
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