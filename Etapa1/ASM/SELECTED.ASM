; ********************************************
; * Programa: SELECTED.ASM                   *
; * Descripcion: Conversiones desde flotante *
; * Autores: Luis Urbina, Samir Cabrera      *
; * Fecha de entrega: 10/04/2025            *
; ********************************************

; El segmento DATOS contiene todas las variables y constantes que usara el programa
DATOS SEGMENT
    ; Mensajes de entrada y salida
    prompt_in    DB 'Ingrese un numero flotante (Ej: 3.14): $'  ; Mensaje para solicitar entrada
    prompt_float DB 'El numero flotante ingresado es: $'        ; Mensaje para mostrar el flotante original
    prompt_int   DB 'Convertido a entero: $'                    ; Mensaje para mostrar la conversión a entero
    prompt_char  DB 'Convertido a caracter: $'                  ; Mensaje para mostrar la conversión a carácter
    prompt_bool  DB 'Convertido a booleano: $'                  ; Mensaje para mostrar la conversión a booleano
    prompt_str   DB 'Convertido a string: $'                    ; Mensaje para mostrar la conversión a string
    prompt_creativo DB 'Convertido a creativo (probabilidad): $' ; Mensaje para conversión a creativo
    
    ; Variables para almacenar valores
    buffer      DB 15, ?, 15 DUP(?)  ; Buffer para entrada (maximo 15 caracteres)
    
    ; Variables para valor flotante original
    entero      DW ?                  ; Variable para almacenar la parte entera del numero
    decimal     DW ?                  ; Variable para almacenar la parte decimal del numero
    dec_digitos DB ?                  ; Contador de digitos en la parte decimal
    es_negativo DB 0                  ; Bandera para indicar si el numero es negativo
    
    ; Variables para las conversiones
    int_valor   DW ?                  ; Valor entero (para conversión a INTEGER)
    bool_valor  DB ?                  ; Valor booleano (para conversión a BOOLEAN)
    char_valor  DB ?                  ; Valor carácter (para conversión a CHAR)
    prob_valor  DB ?                  ; Valor de probabilidad (para conversión a CREATIVO)
    
    ; Variable para valor string
    string_buffer DB 30 DUP(?),'$'   ; Buffer para la conversión a string
    
    ; Valores para mostrar booleanos
    valor_true   DB 'TRUE$'          ; Cadena de texto para mostrar cuando el valor es verdadero
    valor_false  DB 'FALSE$'         ; Cadena de texto para mostrar cuando el valor es falso
    
    ; Auxiliares
    nueva_lin    DB 0Dh, 0Ah, '$'    ; Códigos para crear una nueva línea en pantalla
    punto        DB '.$'             ; Punto decimal para mostrar flotantes
    const_diez   DW 10               ; Constante 10 para cálculos
DATOS ENDS

; El segmento CODIGO contiene las instrucciones que ejecutara el programa
CODIGO SEGMENT
    ; Indicamos al ensamblador donde encontrar nuestros datos y codigo
    ASSUME CS:CODIGO, DS:DATOS
INICIO:
    ; Inicializacion: Preparamos el acceso al segmento de datos
    MOV AX, DATOS
    MOV DS, AX
    
    ; Mostramos el mensaje pidiendo al usuario que ingrese un numero flotante
    MOV AH, 09h       ; Funcion 9 de DOS: mostrar una cadena terminada en $
    LEA DX, prompt_in ; Cargamos la direccion del mensaje en DX
    INT 21h           ; Llamamos a la interrupcion 21h (servicios de DOS)
    
    ; Leemos la entrada del usuario como texto
    MOV AH, 0Ah       ; Funcion 0Ah de DOS: leer una cadena (con buffer)
    LEA DX, buffer    ; Cargamos la direccion del buffer en DX
    INT 21h           ; Llamamos a la interrupcion 21h
    
    ; Procesamos el numero flotante (separando parte entera y decimal)
    CALL PROCESAR_FLOTANTE  ; Llamamos al procedimiento que separa las partes
    
    ; Realizar todas las conversiones desde el flotante
    CALL FLOAT_A_INTEGER    ; Convertir a entero
    CALL FLOAT_A_CHAR       ; Convertir a caracter
    CALL FLOAT_A_BOOLEAN    ; Convertir a booleano
    CALL FLOAT_A_STRING     ; Convertir a string
    CALL FLOAT_A_CREATIVO   ; Convertir a creativo (probabilidad)
    
    ; Mostrar todas las conversiones
    CALL MOSTRAR_RESULTADOS
    
    ; Terminamos el programa y regresamos al sistema operativo
    MOV AX, 4C00h      ; Funcion 4Ch de DOS: terminar programa (con codigo de salida 0)
    INT 21h            ; Llamamos a la interrupcion 21h

;------------------------------------------------------------
; Procedimiento: PROCESAR_FLOTANTE
; Analiza la entrada del usuario y extrae la parte entera y decimal del numero
;------------------------------------------------------------
PROCESAR_FLOTANTE PROC
    ; Guardamos los registros que vamos a modificar
    PUSH AX
    PUSH BX
    PUSH CX
    PUSH DX
    PUSH SI
    
    XOR AX, AX            ; Inicializamos AX a 0
    MOV BL, [buffer+1]    ; En buffer+1 esta la cantidad de caracteres leidos
    XOR BH, BH            ; Limpiamos BH (para que BX solo contenga el valor de BL)
    LEA SI, [buffer+2]    ; SI apunta al primer caracter ingresado
    
    ; Inicializamos todas las variables relacionadas con el numero
    MOV [entero], 0       ; Parte entera a 0
    MOV [decimal], 0      ; Parte decimal a 0
    MOV [dec_digitos], 0  ; Contador de digitos decimales a 0
    MOV [es_negativo], 0  ; Bandera de negativo a 0 (positivo)
    
    ; Verificamos si la cadena esta vacia
    CMP BX, 0
    JE PROC_FIN           ; Si esta vacia, terminamos
    
    ; Verificamos si comienza con signo negativo
    MOV CL, [SI]          ; Obtenemos el primer caracter
    CMP CL, '-'           ; ¿Es un signo negativo?
    JNE PROC_ENTERO       ; Si no es negativo, procesamos parte entera
    
    ; Si es negativo, marcamos la bandera y avanzamos al siguiente caracter
    MOV [es_negativo], 1
    INC SI                ; Avanzamos al siguiente caracter
    DEC BX                ; Reducimos el contador de caracteres
    
    ; Procesamos la parte entera hasta encontrar el punto decimal
PROC_ENTERO:
    CMP BX, 0             ; ¿Terminamos todos los caracteres?
    JE PROC_FIN
    
    MOV CL, [SI]          ; Obtenemos el caracter actual
    INC SI                ; Avanzamos al siguiente caracter
    DEC BX                ; Reducimos el contador de caracteres
    
    CMP CL, '.'           ; ¿Es el punto decimal?
    JE PROC_DECIMAL       ; Si es el punto, pasamos a procesar la parte decimal
    
    ; Verificamos si es un digito valido
    CMP CL, '0'
    JL PROC_ENTERO        ; Si es menor que '0', no es un digito (lo ignoramos)
    CMP CL, '9'
    JG PROC_ENTERO        ; Si es mayor que '9', no es un digito (lo ignoramos)
    
    SUB CL, '0'           ; Convertimos el caracter ASCII a valor numerico
    XOR CH, CH            ; Limpiamos CH (para que CX solo contenga el valor de CL)
    
    ; Formula para construir la parte entera: entero = entero * 10 + digito
    MOV AX, [entero]
    MOV DX, 10
    MUL DX                ; AX = AX * 10
    ADD AX, CX            ; AX = AX + digito
    MOV [entero], AX
    
    JMP PROC_ENTERO       ; Continuamos con el siguiente caracter
    
; Procesamos la parte decimal despues del punto
PROC_DECIMAL:
    CMP BX, 0             ; ¿Terminamos todos los caracteres?
    JE PROC_FIN
    
    MOV CL, [SI]          ; Obtenemos el caracter actual
    INC SI                ; Avanzamos al siguiente caracter
    DEC BX                ; Reducimos el contador de caracteres
    
    ; Verificamos si es un digito valido
    CMP CL, '0'
    JL PROC_DECIMAL       ; Si es menor que '0', no es un digito (lo ignoramos)
    CMP CL, '9'
    JG PROC_DECIMAL       ; Si es mayor que '9', no es un digito (lo ignoramos)
    
    SUB CL, '0'           ; Convertimos el caracter ASCII a valor numerico
    XOR CH, CH            ; Limpiamos CH (para que CX solo contenga el valor de CL)
    
    ; Formula para construir la parte decimal: decimal = decimal * 10 + digito
    MOV AX, [decimal]
    MOV DX, 10
    MUL DX                ; AX = AX * 10
    ADD AX, CX            ; AX = AX + digito
    MOV [decimal], AX
    
    ; Incrementamos el contador de digitos decimales
    INC [dec_digitos]
    
    JMP PROC_DECIMAL      ; Continuamos con el siguiente caracter
    
PROC_FIN:
    ; Si el numero es negativo, aplicamos el signo solo a la parte entera
    CMP [es_negativo], 1
    JNE PROC_NORMAL
    
    ; La parte decimal siempre es positiva, solo negamos la parte entera
    MOV AX, [entero]
    NEG AX                ; Negamos AX (complemento a 2)
    MOV [entero], AX
    
PROC_NORMAL:
    ; Restauramos los registros que modificamos
    POP SI
    POP DX
    POP CX
    POP BX
    POP AX
    RET                   ; Retornamos al punto de llamada
PROCESAR_FLOTANTE ENDP

;------------------------------------------------------------
; Procedimiento: FLOAT_A_INTEGER
; Convierte el valor flotante a entero (truncando la parte decimal)
;------------------------------------------------------------
FLOAT_A_INTEGER PROC
    ; Para float a entero, simplemente tomamos la parte entera y descartamos la decimal
    MOV AX, [entero]
    MOV [int_valor], AX   ; Guardar el valor en la variable de entero
    
    RET
FLOAT_A_INTEGER ENDP

;------------------------------------------------------------
; Procedimiento: FLOAT_A_CHAR
; Convierte el valor flotante a caracter (primer dígito de la parte entera)
;------------------------------------------------------------
FLOAT_A_CHAR PROC
    PUSH AX
    PUSH BX
    PUSH DX
    
    ; Primero obtenemos el valor absoluto de la parte entera
    MOV AX, [entero]
    CMP AX, 0
    JGE POSITIVO_CHAR
    NEG AX                ; Si es negativo, lo hacemos positivo
    
POSITIVO_CHAR:
    ; Ahora extraemos el primer dígito significativo
    ; Si es un número de un solo dígito, ya lo tenemos
    CMP AX, 10
    JL DIGITO_UNICO_CHAR
    
    ; Si tiene más de un dígito, extraemos el primero
    MOV BX, 10

EXTRAER_PRIMER_DIGITO_CHAR:
    CMP AX, 10
    JL DIGITO_UNICO_CHAR  ; Si es menor que 10, ya tenemos un solo dígito
    
    XOR DX, DX
    DIV BX                ; AX = AX / 10, DX = resto
    JMP EXTRAER_PRIMER_DIGITO_CHAR
    
DIGITO_UNICO_CHAR:
    ; Ahora AX contiene el primer dígito
    ADD AL, '0'           ; Convertir a ASCII
    MOV [char_valor], AL  ; Guardar como caracter
    
    POP DX
    POP BX
    POP AX
    RET
FLOAT_A_CHAR ENDP

;------------------------------------------------------------
; Procedimiento: FLOAT_A_BOOLEAN
; Convierte el valor flotante a booleano (FALSE si 0.0, TRUE en caso contrario)
;------------------------------------------------------------
FLOAT_A_BOOLEAN PROC
    ; Un flotante es FALSE solo si tanto la parte entera como la decimal son 0
    CMP WORD PTR [entero], 0
    JNE ES_TRUE           ; Si la parte entera no es 0, es TRUE
    
    CMP WORD PTR [decimal], 0
    JNE ES_TRUE           ; Si la parte decimal no es 0, es TRUE
    
    ; Si llegamos aquí, es 0.0
    MOV [bool_valor], 0   ; FALSE
    JMP BOOL_FIN_FLOAT
    
ES_TRUE:
    MOV [bool_valor], 1   ; TRUE
    
BOOL_FIN_FLOAT:
    RET
FLOAT_A_BOOLEAN ENDP

;------------------------------------------------------------
; Procedimiento: FLOAT_A_STRING
; Convierte el valor flotante a su representación textual
;------------------------------------------------------------
FLOAT_A_STRING PROC
    PUSH AX
    PUSH BX
    PUSH CX
    PUSH DX
    PUSH SI
    PUSH DI
    
    ; Empezamos con el buffer vacío
    LEA DI, string_buffer
    
    ; Verificamos si el número es negativo
    CMP [es_negativo], 0
    JE STRING_POSITIVO_FLOAT
    
    ; Si es negativo, agregamos el signo '-' al inicio
    MOV BYTE PTR [DI], '-'
    INC DI                ; Avanzamos al siguiente byte en el buffer
    
STRING_POSITIVO_FLOAT:
    ; Convertimos la parte entera a string
    MOV AX, [entero]
    
    ; Si la parte entera es negativa, la hacemos positiva (ya agregamos el -)
    CMP [es_negativo], 0
    JE ENTERO_YA_POSITIVO
    NEG AX
    
ENTERO_YA_POSITIVO:
    ; Caso especial: si el número es cero
    CMP AX, 0
    JNE CONVERTIR_DIGITOS_FLOAT
    
    MOV BYTE PTR [DI], '0'    ; Ponemos el carácter '0'
    INC DI                    ; Avanzamos en el buffer
    JMP AGREGAR_PUNTO         ; Continuamos con el punto decimal
    
CONVERTIR_DIGITOS_FLOAT:
    ; Necesitamos los dígitos en orden inverso
    ; Usamos la pila para invertir el orden
    MOV BX, 10      ; Divisor = 10
    XOR CX, CX      ; Contador de dígitos
    
BUCLE_DIGITOS_FLOAT:
    XOR DX, DX      ; Limpiamos DX para la división
    DIV BX          ; AX = AX / 10, DX = resto (dígito)
    
    PUSH DX         ; Guardamos el dígito en la pila
    INC CX          ; Incrementamos contador
    
    CMP AX, 0
    JNE BUCLE_DIGITOS_FLOAT   ; Si AX no es 0, continuamos
    
    ; Ahora sacamos los dígitos de la pila y los agregamos al buffer
AGREGAR_DIGITOS_FLOAT:
    POP DX          ; Recuperamos un dígito
    ADD DL, '0'     ; Convertimos a carácter ASCII
    MOV [DI], DL    ; Lo ponemos en el buffer
    INC DI          ; Avanzamos en el buffer
    LOOP AGREGAR_DIGITOS_FLOAT
    
AGREGAR_PUNTO:
    ; Agregamos el punto decimal
    MOV BYTE PTR [DI], '.'
    INC DI
    
    ; Ahora agregamos la parte decimal
    ; Si no hay dígitos decimales, agregamos un 0
    CMP BYTE PTR [dec_digitos], 0
    JNE HAY_DECIMALES
    
    MOV BYTE PTR [DI], '0'
    INC DI
    JMP FIN_STRING_FLOAT
    
HAY_DECIMALES:
    ; Calculamos cuántos ceros iniciales podríamos necesitar
    XOR CH, CH
    MOV CL, [dec_digitos]     ; CL = número de dígitos decimales
    MOV SI, CX                ; SI = total de dígitos decimales
    
    ; Contamos cuántos dígitos tiene decimal
    MOV AX, [decimal]
    XOR CX, CX                ; Contador de dígitos
    
    ; Caso especial: si decimal es 0
    CMP AX, 0
    JNE CONTAR_DIGITOS_DECIMAL
    
    ; Si decimal es 0, necesitamos SI ceros
    MOV CX, SI
AGREGAR_SOLO_CEROS:
    MOV BYTE PTR [DI], '0'
    INC DI
    LOOP AGREGAR_SOLO_CEROS
    JMP FIN_STRING_FLOAT
    
CONTAR_DIGITOS_DECIMAL:
    ; Contamos dígitos en decimal
    MOV BX, 10
BUCLE_CONTAR_DECIMAL:
    XOR DX, DX
    DIV BX
    INC CX
    CMP AX, 0
    JNE BUCLE_CONTAR_DECIMAL
    
    ; SI = total de dígitos requeridos, CX = dígitos que tiene decimal
    ; Calculamos cuántos ceros necesitamos
    MOV AX, SI
    SUB AX, CX
    
    ; Agregamos los ceros iniciales si son necesarios
    CMP AX, 0
    JLE AGREGAR_DECIMAL   ; No necesitamos ceros iniciales
    
    MOV CX, AX
AGREGAR_CEROS_INICIALES_FLOAT:
    MOV BYTE PTR [DI], '0'
    INC DI
    LOOP AGREGAR_CEROS_INICIALES_FLOAT
    
AGREGAR_DECIMAL:
    ; Ahora agregamos los dígitos de la parte decimal
    MOV AX, [decimal]
    MOV BX, 10      ; Divisor = 10
    XOR CX, CX      ; Contador de dígitos
    
BUCLE_DECIMAL_PARA_PILA:
    XOR DX, DX      ; Limpiamos DX para la división
    DIV BX          ; AX = AX / 10, DX = resto (dígito)
    
    PUSH DX         ; Guardamos el dígito en la pila
    INC CX          ; Incrementamos contador
    
    CMP AX, 0
    JNE BUCLE_DECIMAL_PARA_PILA   ; Si AX no es 0, continuamos
    
    ; Sacamos los dígitos de la pila en orden inverso
SACAR_DECIMAL_DE_PILA:
    POP DX          ; Recuperamos un dígito
    ADD DL, '0'     ; Convertimos a carácter ASCII
    MOV [DI], DL    ; Lo ponemos en el buffer
    INC DI          ; Avanzamos en el buffer
    LOOP SACAR_DECIMAL_DE_PILA
    
FIN_STRING_FLOAT:
    MOV BYTE PTR [DI], '$'  ; Terminador de string
    
    POP DI
    POP SI
    POP DX
    POP CX
    POP BX
    POP AX
    RET
FLOAT_A_STRING ENDP

;------------------------------------------------------------
; Procedimiento: FLOAT_A_CREATIVO
; Convierte el flotante a un valor de probabilidad basado en el primer dígito de la parte entera
;------------------------------------------------------------
FLOAT_A_CREATIVO PROC
    PUSH AX
    PUSH BX
    PUSH DX
    
    ; Verificamos si el flotante es 0.0
    CMP WORD PTR [entero], 0
    JNE NO_CERO_CREATIVO
    CMP WORD PTR [decimal], 0
    JNE NO_CERO_CREATIVO
    
    ; Si es 0.0, la probabilidad es 0
    MOV BYTE PTR [prob_valor], 0
    JMP CREATIVO_FIN_FLOAT
    
NO_CERO_CREATIVO:
    ; Obtenemos el valor absoluto de la parte entera
    MOV AX, [entero]
    CMP AX, 0
    JGE POSITIVO_CREATIVO
    NEG AX
    
POSITIVO_CREATIVO:
    ; Extraemos el primer dígito
    ; Si es un número de un solo dígito, ya lo tenemos
    CMP AX, 10
    JL DIGITO_UNICO_CREATIVO
    
    ; Si tiene más de un dígito, extraemos el primero
    MOV BX, 10

EXTRAER_PRIMER_DIGITO_CREATIVO:
    CMP AX, 10
    JL DIGITO_UNICO_CREATIVO  ; Si es menor que 10, ya tenemos un solo dígito
    
    XOR DX, DX
    DIV BX                    ; AX = AX / 10, DX = resto
    JMP EXTRAER_PRIMER_DIGITO_CREATIVO
    
DIGITO_UNICO_CREATIVO:
    ; Ahora AX contiene el primer dígito
    MOV [prob_valor], AL
    
CREATIVO_FIN_FLOAT:
    POP DX
    POP BX
    POP AX
    RET
FLOAT_A_CREATIVO ENDP

;------------------------------------------------------------
; Procedimiento: MOSTRAR_RESULTADOS
; Muestra el resultado original y todas las conversiones
;------------------------------------------------------------
MOSTRAR_RESULTADOS PROC
    ; Mostramos una nueva línea
    MOV AH, 09h
    LEA DX, nueva_lin
    INT 21h
    
    ; 1. Mostrar el flotante original
    MOV AH, 09h
    LEA DX, prompt_float
    INT 21h
    
    CALL MOSTRAR_FLOTANTE
    
    ; Nueva línea
    MOV AH, 09h
    LEA DX, nueva_lin
    INT 21h
    
    ; 2. Mostrar conversión a entero
    MOV AH, 09h
    LEA DX, prompt_int
    INT 21h
    
    MOV AX, [int_valor]
    CALL MOSTRAR_ENTERO
    
    ; Nueva línea
    MOV AH, 09h
    LEA DX, nueva_lin
    INT 21h
    
    ; 3. Mostrar conversión a caracter
    MOV AH, 09h
    LEA DX, prompt_char
    INT 21h
    
    MOV DL, [char_valor]
    MOV AH, 02h         ; Función 2: mostrar caracter
    INT 21h
    
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
    JE MOSTRAR_BOOL_FALSE_FLOAT
    
    MOV AH, 09h
    LEA DX, valor_true
    INT 21h
    JMP MOSTRAR_STR_FLOAT
    
MOSTRAR_BOOL_FALSE_FLOAT:
    MOV AH, 09h
    LEA DX, valor_false
    INT 21h
    
MOSTRAR_STR_FLOAT:
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
    
    ; Para el tipo creativo de probabilidad mostramos "0.X"
    MOV DL, '0'         ; El cero inicial
    MOV AH, 02h
    INT 21h
    
    ; Mostrar punto decimal
    MOV AH, 09h
    LEA DX, punto
    INT 21h
    
    ; Mostrar el valor de probabilidad
    MOV DL, [prob_valor]
    ADD DL, '0'         ; Convertir a carácter
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
    
    ; Verificamos si el número es negativo
    CMP AX, 0
    JGE NUM_POSITIVO   ; Si es >= 0, es positivo
    
    ; Si es negativo, mostramos el signo "-" y negamos el numero
    PUSH AX            ; Guardamos AX
    MOV DL, '-'
    MOV AH, 02h        ; Funcion 2 de DOS: mostrar un caracter
    INT 21h            ; Mostramos el signo menos
    POP AX             ; Recuperamos AX
    NEG AX             ; Negamos AX para trabajar con el valor positivo
    
NUM_POSITIVO:
    MOV BX, 10         ; Divisor (10) para obtener los digitos
    XOR CX, CX         ; Inicializamos contador de digitos a 0
    
    ; Caso especial: si el numero es cero
    CMP AX, 0
    JNE DIVIDIR
    
    MOV DL, '0'        ; Caracter '0'
    MOV AH, 02h        ; Funcion 2 de DOS: mostrar un caracter
    INT 21h
    JMP NUM_A_STR_FIN
    
DIVIDIR:
    ; Para cada digito: dividimos por 10, el resto es el digito actual, el cociente continua
    XOR DX, DX         ; Limpiamos DX para la division extendida DX:AX / BX
    DIV BX             ; AX = cociente, DX = resto (digito)
    
    PUSH DX            ; Guardamos el digito en la pila (para mostrarlo luego en orden inverso)
    INC CX             ; Incrementamos contador de digitos
    
    CMP AX, 0          ; ¿Terminamos? (cociente = 0)
    JNE DIVIDIR        ; Si no, continuamos con el siguiente digito
    
MOSTRAR_DIGITOS:
    ; Mostramos los digitos en orden inverso (sacandolos de la pila)
    POP DX             ; Recuperamos un digito
    ADD DL, '0'        ; Convertimos el valor numerico a caracter ASCII
    MOV AH, 02h        ; Funcion 2 de DOS: mostrar un caracter
    INT 21h            ; Mostramos el digito
    LOOP MOSTRAR_DIGITOS ; Repetimos para cada digito (CX veces)
    
NUM_A_STR_FIN:
    ; Restauramos los registros que modificamos
    POP DX
    POP CX
    POP BX
    POP AX
    RET                ; Retornamos al punto de llamada
MOSTRAR_ENTERO ENDP

;------------------------------------------------------------
; Procedimiento: MOSTRAR_FLOTANTE
; Muestra el número flotante original en pantalla
;------------------------------------------------------------
MOSTRAR_FLOTANTE PROC
    ; Guardamos los registros que vamos a modificar
    PUSH AX
    PUSH BX
    PUSH CX
    PUSH DX
    
    ; Mostrar la parte entera
    MOV AX, [entero]
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
    CMP WORD PTR [decimal], 0
    JNE DECIMALES_NO_CERO
    
MOSTRAR_SOLO_CEROS:
    MOV DL, '0'
    MOV AH, 02h
    INT 21h
    
    LOOP MOSTRAR_SOLO_CEROS
    JMP FIN_MOSTRAR_FLOTANTE
    
DECIMALES_NO_CERO:
    ; Si la parte decimal no es 0, mostrar su valor real
    ; Calculamos cuántos ceros iniciales podríamos necesitar
    PUSH CX                 ; Guardamos el contador de dígitos decimales
    
    MOV AX, [decimal]       ; Valor decimal a mostrar
    XOR CX, CX              ; Contador de dígitos reales
    MOV BX, 10              ; Divisor
    
CONTAR_DIGITOS_REALES:
    XOR DX, DX
    DIV BX                  ; AX = AX / 10, DX = resto
    
    INC CX                  ; Incrementamos contador
    
    CMP AX, 0
    JNE CONTAR_DIGITOS_REALES
    
    ; Recuperamos contador original y calculamos ceros necesarios
    POP BX                  ; BX = contador original de dígitos
    MOV AX, BX
    SUB AX, CX              ; AX = ceros a agregar al inicio
    
    ; Mostrar los ceros iniciales si son necesarios
    CMP AX, 0
    JLE MOSTRAR_DECIMAL_VALOR
    
    MOV CX, AX              ; CX = número de ceros a mostrar
MOSTRAR_CEROS_INICIALES:
    MOV DL, '0'
    MOV AH, 02h
    INT 21h
    
    LOOP MOSTRAR_CEROS_INICIALES
    
MOSTRAR_DECIMAL_VALOR:
    ; Ahora mostramos el valor decimal real
    MOV AX, [decimal]
    
    ; Convertir a dígitos (usando la pila para invertir orden)
    XOR CX, CX              ; Contador de dígitos
    MOV BX, 10              ; Divisor
    
DECIMAL_DIVIDIR:
    XOR DX, DX              ; Limpiar DX para división
    DIV BX                  ; AX = AX / 10, DX = resto (dígito)
    
    PUSH DX                 ; Guardar dígito en pila
    INC CX                  ; Incrementar contador
    
    CMP AX, 0               ; ¿Terminamos?
    JNE DECIMAL_DIVIDIR
    
DECIMAL_MOSTRAR:
    POP DX                  ; Obtener dígito de pila
    ADD DL, '0'             ; Convertir a carácter
    MOV AH, 02h             ; Función 2: mostrar carácter
    INT 21h                 ; Mostrar dígito
    LOOP DECIMAL_MOSTRAR
    
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