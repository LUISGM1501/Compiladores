; ********************************************
; * Programa: CREATIV.ASM                   *
; * Descripcion: Conversiones desde creativo*
; * (probabilidad entre 0 y 1)              *
; * Autores: Luis Urbina, Samir Cabrera     *
; * Fecha de entrega: 10/04/2025            *
; ********************************************

; Este archivo implementa conversiones desde el tipo creativo "SpyderEye"
; que representa datos para el manejo de probabilidad con rango de 0 a 1.

; El segmento DATOS contiene todas las variables y constantes que usara el programa
DATOS SEGMENT
    ; Mensajes de entrada y salida
    prompt_in    DB 'Ingrese una probabilidad entre 0 y 1: $'  ; Mensaje para solicitar entrada al usuario
    prompt_prob  DB 'El valor de probabilidad es: $'           ; Mensaje para mostrar el valor original
    prompt_bool  DB 'Convertido a booleano: $'                 ; Mensaje para mostrar la conversión a booleano
    prompt_int   DB 'Convertido a entero: $'                   ; Mensaje para mostrar la conversión a entero
    prompt_float DB 'Convertido a flotante: $'                 ; Mensaje para mostrar la conversión a flotante
    prompt_char  DB 'Convertido a caracter: $'                 ; Mensaje para mostrar la conversión a carácter
    prompt_str   DB 'Convertido a string: $'                   ; Mensaje para mostrar la conversión a string
    
    ; Valores para mostrar booleanos
    valor_true   DB 'TRUE$'        ; Cadena de texto para mostrar cuando el valor es verdadero
    valor_false  DB 'FALSE$'       ; Cadena de texto para mostrar cuando el valor es falso
    
    ; Variables para almacenar valores
    buffer       DB 15, ?, 15 DUP(?)  ; Buffer para entrada (maximo 15 caracteres)
    entero       DW ?                  ; Variable para almacenar la parte entera del numero
    decimal      DW ?                  ; Variable para almacenar la parte decimal del numero
    dec_digitos  DB ?                  ; Contador de digitos en la parte decimal
    es_negativo  DB 0                  ; Bandera para indicar si el numero es negativo (1) o positivo (0)
    bool_valor   DB ?                  ; Valor booleano convertido
    int_valor    DW ?                  ; Valor entero convertido
    char_valor   DB ?                  ; Valor carácter convertido
    string_valor DB 50 DUP (?)         ; Valor string convertido
    valor_mayor_05 DB 0                ; Bandera para indicar si la probabilidad es mayor a 0.5
    primer_digito_decimal DB ?         ; Variable para almacenar el primer dígito decimal
    
    ; Auxiliares
    nueva_lin    DB 0Dh, 0Ah, '$'      ; Codigos para crear una nueva linea en pantalla
    punto        DB '.$'               ; Punto decimal seguido de terminador
    constante_diez DW 10               ; Constante 10 para calculos y conversiones
    constante_cien DW 100              ; Constante 100 para calculos y conversiones
    error_rango  DB 'Error: El numero debe estar en el rango de 0 a 1$'  ; Mensaje de error
DATOS ENDS

; El segmento CODIGO contiene las instrucciones que ejecutara el programa
CODIGO SEGMENT
    ; Indicamos al ensamblador donde encontrar nuestros datos y codigo
    ASSUME CS:CODIGO, DS:DATOS
INICIO:
    ; Inicializacion: Preparamos el acceso al segmento de datos
    MOV AX, DATOS
    MOV DS, AX
    
    ; Mostramos el mensaje pidiendo al usuario que ingrese un numero entre 0 y 1
    MOV AH, 09h       ; Funcion 9 de DOS: mostrar una cadena terminada en $
    LEA DX, prompt_in ; Cargamos la direccion del mensaje en DX
    INT 21h           ; Llamamos a la interrupcion 21h (servicios de DOS)
    
    ; Leemos la entrada del usuario como texto
    MOV AH, 0Ah       ; Funcion 0Ah de DOS: leer una cadena (con buffer)
    LEA DX, buffer    ; Cargamos la direccion del buffer en DX
    INT 21h           ; Llamamos a la interrupcion 21h
    
    ; Procesamos el numero flotante (separando parte entera y decimal)
    CALL PROCESAR_FLOTANTE  ; Llamamos al procedimiento que separa las partes
    
    ; Verificamos que el numero este entre 0 y 1 (incluidos)
    CALL VALIDAR_RANGO       ; Validamos el rango del numero
    JC MOSTRAR_ERROR_RANGO   ; Si CF=1 (Carry Flag), el numero esta fuera de rango
    
    ; Realizamos todas las conversiones
    CALL REALIZAR_CONVERSIONES
    
    ; Si el numero es valido, mostramos una nueva linea
    MOV AH, 09h       ; Funcion 9 de DOS: mostrar una cadena
    LEA DX, nueva_lin ; Cargamos la direccion de la cadena de nueva linea
    INT 21h           ; Llamamos a la interrupcion 21h
    
    ; Mostramos todos los resultados de conversión
    CALL MOSTRAR_RESULTADOS
    
    JMP FIN_PROGRAMA       ; Saltamos al final del programa
    
MOSTRAR_ERROR_RANGO:
    ; Si el numero esta fuera de rango, mostramos un mensaje de error
    MOV AH, 09h       ; Funcion 9 de DOS: mostrar una cadena
    LEA DX, nueva_lin ; Primero mostramos una nueva linea
    INT 21h           ; Llamamos a la interrupcion 21h
    
    MOV AH, 09h        ; Funcion 9 de DOS: mostrar una cadena
    LEA DX, error_rango ; Cargamos la direccion del mensaje de error
    INT 21h            ; Llamamos a la interrupcion 21h
    
FIN_PROGRAMA:
    ; Terminamos el programa y regresamos al sistema operativo
    MOV AX, 4C00h      ; Funcion 4Ch de DOS: terminar programa (con codigo de salida 0)
    INT 21h            ; Llamamos a la interrupcion 21h


;------------------------------------------------------------
; Procedimiento: REALIZAR_CONVERSIONES
; Realiza todas las conversiones desde el valor creativo a otros tipos
;------------------------------------------------------------
REALIZAR_CONVERSIONES PROC
    ; Guardamos los registros que vamos a modificar
    PUSH AX
    PUSH BX
    PUSH CX
    PUSH DX
    
    ; 1. Conversión a booleano (si es > 0.5, entonces TRUE)
    ; Primero verificamos si la parte entera es 0
    CMP [entero], 0
    JE VERIFICAR_DECIMAL_BOOL
    
    ; Si la parte entera es 1, entonces es TRUE
    MOV [bool_valor], 1   ; TRUE
    JMP CONVERSION_ENTERO
    
VERIFICAR_DECIMAL_BOOL:
    ; Si la parte entera es 0, verificamos si la parte decimal es > 0.5
    MOV AX, [decimal]
    MOV BX, 5              ; Para comparar con 0.5
    XOR CX, CX             ; Limpiamos CX
    MOV CL, [dec_digitos]  ; Número de dígitos decimales
    CMP CX, 1              ; Si solo hay un dígito decimal
    JE UN_DIGITO_DECIMAL
    
    ; Si hay más de un dígito, comparamos el primer dígito
    MOV DX, 10             ; Para extraer el primer dígito
EXTRAER_PRIMER_DIGITO:
    XOR DX, DX
    DIV WORD PTR [constante_diez]
    LOOP EXTRAER_PRIMER_DIGITO
    
    CMP DX, 5              ; Comparamos el primer dígito con 5
    JAE BOOL_TRUE          ; Si es >= 5, entonces TRUE
    JMP BOOL_FALSE         ; Si es < 5, entonces FALSE
    
UN_DIGITO_DECIMAL:
    CMP AX, 5              ; Comparamos con 5
    JAE BOOL_TRUE          ; Si es >= 5, entonces TRUE
    
BOOL_FALSE:
    MOV [bool_valor], 0    ; FALSE
    MOV [valor_mayor_05], 0 ; Marcamos que no es mayor a 0.5
    JMP CONVERSION_ENTERO
    
BOOL_TRUE:
    MOV [bool_valor], 1    ; TRUE
    MOV [valor_mayor_05], 1 ; Marcamos que es mayor a 0.5
    
    ; 2. Conversión a entero (tomar decimal y representarlo tal cual)
    ; Ejemplo: 0.56 = 56
CONVERSION_ENTERO:
    MOV AX, [decimal]
    MOV [int_valor], AX
    
    ; 3. Conversión a carácter (extraer primer dígito decimal)
    ; MODIFICACIÓN: Ahora extraemos el primer dígito decimal del valor de probabilidad
    MOV AX, [decimal]
    
    ; Si decimal es 0, el dígito es 0
    CMP AX, 0
    JE PRIMER_DIGITO_CERO
    
    ; Extraer el primer dígito de la parte decimal
    ; Si tenemos más de un dígito decimal, necesitamos extraer el primero
    MOV BX, 10              ; Divisor = 10
    XOR CH, CH                ; Limpiar la parte alta (CH)
    MOV CL, [dec_digitos]     ; Cargar el byte en la parte baja (CL)    CMP CX, 1
    JE UN_DIGITO_DECIMAL_CHAR ; Si solo hay un dígito, ya lo tenemos en AX
    
    ; Si hay más de un dígito, dividimos repetidamente por 10 hasta obtener
    ; el primer dígito (el más significativo)
    DEC CX                  ; Decrementamos porque necesitamos hacer n-1 divisiones
EXTRAER_DIGITO_LOOP:
    CMP CX, 0
    JE DIGITO_ENCONTRADO    ; Si CX = 0, ya tenemos el primer dígito en AX
    
    XOR DX, DX              ; Limpiar DX para división
    DIV BX                  ; AX = AX / 10, DX = resto
    
    DEC CX                  ; Decrementar contador
    JMP EXTRAER_DIGITO_LOOP ; Seguir dividiendo
    
UN_DIGITO_DECIMAL_CHAR:
    ; Ya tenemos el dígito en AX
    JMP DIGITO_ENCONTRADO
    
DIGITO_ENCONTRADO:
    ; AX contiene el primer dígito decimal
    MOV [primer_digito_decimal], AL
    JMP CONVERSION_CHAR_FIN
    
PRIMER_DIGITO_CERO:
    MOV [primer_digito_decimal], 0
    
CONVERSION_CHAR_FIN:
    ; Convertir el dígito a carácter sumando '0'
    MOV AL, [primer_digito_decimal]
    ADD AL, '0'             ; Convertir a carácter ASCII
    MOV [char_valor], AL
    
    ; 4. Conversión a string (mantener representación como string)
CONVERSION_STRING:
    ; Utilizamos el buffer actual como representación en string
    ; La conversión a flotante no es necesaria, ya tenemos el valor
    
    ; Restauramos los registros que modificamos
    POP DX
    POP CX
    POP BX
    POP AX
    RET
REALIZAR_CONVERSIONES ENDP
;------------------------------------------------------------
; Procedimiento: MOSTRAR_RESULTADOS
; Muestra todos los resultados de las conversiones
;------------------------------------------------------------
MOSTRAR_RESULTADOS PROC
    ; 1. Mostrar el valor creativo original
    MOV AH, 09h
    LEA DX, prompt_prob
    INT 21h
    
    CALL MOSTRAR_FLOTANTE  ; Mostramos el número original
    
    ; Nueva línea
    MOV AH, 09h
    LEA DX, nueva_lin
    INT 21h
    
    ; 2. Mostrar conversión a booleano
    MOV AH, 09h
    LEA DX, prompt_bool
    INT 21h
    
    CMP [bool_valor], 0
    JE MOSTRAR_BOOL_FALSE
    
    MOV AH, 09h
    LEA DX, valor_true
    INT 21h
    JMP MOSTRAR_INT
    
MOSTRAR_BOOL_FALSE:
    MOV AH, 09h
    LEA DX, valor_false
    INT 21h
    
MOSTRAR_INT:
    ; Nueva línea
    MOV AH, 09h
    LEA DX, nueva_lin
    INT 21h
    
    ; 3. Mostrar conversión a entero
    MOV AH, 09h
    LEA DX, prompt_int
    INT 21h
    
    MOV AX, [int_valor]
    CALL MOSTRAR_ENTERO_SIMPLE
    
    ; Nueva línea
    MOV AH, 09h
    LEA DX, nueva_lin
    INT 21h
    
    ; 4. Mostrar conversión a flotante (mismo valor que el original)
    MOV AH, 09h
    LEA DX, prompt_float
    INT 21h
    
    CALL MOSTRAR_FLOTANTE
    
    ; Nueva línea
    MOV AH, 09h
    LEA DX, nueva_lin
    INT 21h
    
    ; 5. Mostrar conversión a carácter
    MOV AH, 09h
    LEA DX, prompt_char
    INT 21h
    
    MOV DL, [char_valor]
    MOV AH, 02h
    INT 21h
    
    ; Nueva línea
    MOV AH, 09h
    LEA DX, nueva_lin
    INT 21h
    
    ; 6. Mostrar conversión a string
    MOV AH, 09h
    LEA DX, prompt_str
    INT 21h
    
    ; Mostramos el mismo valor que mostramos como flotante
    CALL MOSTRAR_FLOTANTE
    
    RET
MOSTRAR_RESULTADOS ENDP

;------------------------------------------------------------
; Procedimiento: MOSTRAR_ENTERO_SIMPLE
; Muestra un número entero sin signo
; Entrada: AX = número a mostrar
;------------------------------------------------------------
MOSTRAR_ENTERO_SIMPLE PROC
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
    JMP FIN_MOSTRAR_ENTERO_SIMPLE
    
ENTERO_NO_CERO:
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
    
FIN_MOSTRAR_ENTERO_SIMPLE:
    ; Restaurar registros
    POP DX
    POP CX
    POP BX
    POP AX
    RET
MOSTRAR_ENTERO_SIMPLE ENDP

; Este procedimiento verifica si el numero esta en el rango de 0 a 1
; Si el numero esta en rango, CF=0 (no hay error)
; Si el numero esta fuera de rango, CF=1 (hay error)
VALIDAR_RANGO PROC
    PUSH AX            ; Guardamos AX para restaurarlo despues
    
    ; Primero verificamos si es negativo (debe ser mayor o igual a 0)
    CMP [es_negativo], 1
    JE FUERA_DE_RANGO  ; Si es negativo, esta fuera de rango
    
    ; Verificamos que la parte entera sea 0 o 1
    MOV AX, [entero]
    CMP AX, 0
    JE RANGO_VALIDO    ; Si es 0, es valido independientemente de la parte decimal
    CMP AX, 1
    JE VERIFICAR_DECIMAL ; Si es 1, hay que verificar que la parte decimal sea 0
    JMP FUERA_DE_RANGO   ; Si es > 1, no es valido
    
VERIFICAR_DECIMAL:
    ; Si la parte entera es 1, la parte decimal debe ser 0 para estar en rango (exactamente 1.0)
    CMP WORD PTR [decimal], 0
    JNE FUERA_DE_RANGO   ; Si la parte decimal no es 0, entonces es > 1
    
RANGO_VALIDO:
    CLC                  ; Limpiamos el Carry Flag (CF=0) para indicar que no hay error
    JMP FIN_VALIDACION   ; Vamos al final del procedimiento
    
FUERA_DE_RANGO:
    STC                  ; Establecemos el Carry Flag (CF=1) para indicar que hay error
    
FIN_VALIDACION:
    POP AX               ; Restauramos AX
    RET                  ; Retornamos al punto de llamada
VALIDAR_RANGO ENDP


; Este procedimiento analiza la entrada del usuario y extrae la parte entera y decimal del numero
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

; Este procedimiento muestra el numero flotante en pantalla
MOSTRAR_FLOTANTE PROC
    ; Guardamos los registros que vamos a modificar
    PUSH AX
    PUSH BX
    PUSH CX
    PUSH DX
    
    ; Primero mostramos la parte entera
    MOV AX, [entero]
    CALL MOSTRAR_ENTERO   ; Mostramos la parte entera con su signo si es necesario
    
    ; Luego mostramos el punto decimal
    MOV AH, 09h
    LEA DX, punto
    INT 21h
    
    ; Finalmente mostramos la parte decimal
    CALL MOSTRAR_DECIMAL  ; Mostramos la parte decimal
    
    ; Restauramos los registros que modificamos
    POP DX
    POP CX
    POP BX
    POP AX
    RET                   ; Retornamos al punto de llamada
MOSTRAR_FLOTANTE ENDP

; Este procedimiento muestra la parte decimal del numero
MOSTRAR_DECIMAL PROC
    ; Guardamos los registros que vamos a modificar
    PUSH AX
    PUSH BX
    PUSH CX
    PUSH DX
    
    ; Verificamos si hay digitos decimales
    CMP BYTE PTR [dec_digitos], 0
    JNE TIENE_DECIMALES
    
    ; Si no hay decimales, mostramos un 0
    MOV DL, '0'           ; Caracter '0'
    MOV AH, 02h           ; Funcion 2 de DOS: mostrar un caracter
    INT 21h
    JMP FIN_DECIMAL
    
TIENE_DECIMALES:
    ; Guardamos el numero original de digitos decimales en BX
    MOV CL, [dec_digitos]
    XOR CH, CH
    MOV BX, CX            ; BX = numero de digitos decimales
    
    ; Calculamos la potencia de 10 correspondiente al numero de digitos
    ; (por ejemplo, si hay 3 digitos, necesitamos 10^3 = 1000)
    MOV AX, 1             ; Comenzamos con 1
CALCULAR_POTENCIA:
    CMP CL, 0             ; ¿Llegamos a 0?
    JE FIN_POTENCIA
    
    MUL WORD PTR [constante_diez]  ; AX = AX * 10
    
    DEC CL                ; Reducimos el contador
    JMP CALCULAR_POTENCIA
    
FIN_POTENCIA:
    MOV CX, AX            ; CX = potencia de 10
    
    ; Verificamos si necesitamos mostrar ceros a la izquierda
    MOV AX, [decimal]     ; AX = valor decimal
    
    ; Si el decimal es 0, mostramos todos los digitos como ceros
    CMP AX, 0
    JNE CONTAR_DIGITOS
    
    ; Mostramos la cantidad correcta de ceros
    MOV CX, BX            ; CX = numero de digitos decimales
MOSTRAR_SOLO_CEROS:
    CMP CX, 0
    JE FIN_DECIMAL
    
    MOV DL, '0'           ; Caracter '0'
    MOV AH, 02h           ; Funcion 2 de DOS: mostrar un caracter
    INT 21h
    
    DEC CX                ; Reducimos el contador
    JMP MOSTRAR_SOLO_CEROS
    
CONTAR_DIGITOS:
    ; Contamos cuantos digitos tiene la parte decimal para saber
    ; si necesitamos agregar ceros a la izquierda
    MOV AX, [decimal]     ; AX = valor decimal
    XOR CX, CX            ; CX = contador de digitos
    
BUCLE_CONTAR:
    INC CX                ; Incrementamos contador
    
    XOR DX, DX
    DIV WORD PTR [constante_diez]  ; AX = AX / 10, DX = resto
    
    CMP AX, 0
    JNE BUCLE_CONTAR      ; Si el cociente no es 0, continuamos contando
    
    ; Calculamos cuantos ceros necesitamos al inicio
    MOV AX, BX            ; AX = numero total de digitos necesarios
    SUB AX, CX            ; AX = ceros a agregar al inicio
    
    ; Mostramos los ceros iniciales si son necesarios
    CMP AX, 0
    JLE MOSTRAR_DECIMAL_VALOR  ; Si no necesitamos ceros, mostramos el valor
    
    MOV CX, AX            ; CX = numero de ceros a mostrar
MOSTRAR_CEROS_INICIALES:
    MOV DL, '0'           ; Caracter '0'
    MOV AH, 02h           ; Funcion 2 de DOS: mostrar un caracter
    INT 21h
    
    LOOP MOSTRAR_CEROS_INICIALES  ; Repetimos CX veces
    
MOSTRAR_DECIMAL_VALOR:
    ; Ahora mostramos el valor decimal real
    MOV AX, [decimal]
    
    ; Usamos la funcion que muestra numeros positivos
    CALL MOSTRAR_NUMERO_POSITIVO
    
FIN_DECIMAL:
    ; Restauramos los registros que modificamos
    POP DX
    POP CX
    POP BX
    POP AX
    RET                   ; Retornamos al punto de llamada
MOSTRAR_DECIMAL ENDP

; Este procedimiento muestra un numero entero con signo
MOSTRAR_ENTERO PROC
    ; Guardamos los registros que vamos a modificar
    PUSH AX
    PUSH BX
    PUSH CX
    PUSH DX
    
    ; Verificamos si el numero es negativo
    CMP AX, 0
    JGE ENTERO_POSITIVO   ; Si es >= 0, es positivo
    
    ; Si es negativo, mostramos el signo "-" y negamos el numero
    PUSH AX            ; Guardamos AX
    MOV DL, '-'        ; Caracter '-'
    MOV AH, 02h        ; Funcion 2 de DOS: mostrar un caracter
    INT 21h            ; Mostramos el signo menos
    POP AX             ; Recuperamos AX
    NEG AX             ; Negamos AX para trabajar con el valor positivo
    
ENTERO_POSITIVO:
    ; Utilizamos la funcion para mostrar numeros positivos
    CALL MOSTRAR_NUMERO_POSITIVO
    
    ; Restauramos los registros que modificamos
    POP DX
    POP CX
    POP BX
    POP AX
    RET                ; Retornamos al punto de llamada
MOSTRAR_ENTERO ENDP

; Este procedimiento muestra un numero positivo
MOSTRAR_NUMERO_POSITIVO PROC
    ; Guardamos los registros que vamos a modificar
    PUSH AX
    PUSH BX
    PUSH CX
    PUSH DX
    
    ; Caso especial: si el numero es cero
    CMP AX, 0
    JNE CONVERTIR_DIGITOS
    
    MOV DL, '0'        ; Caracter '0'
    MOV AH, 02h        ; Funcion 2 de DOS: mostrar un caracter
    INT 21h
    JMP FIN_POSITIVO
    
CONVERTIR_DIGITOS:
    ; Convertimos el numero a digitos individuales usando divisiones sucesivas por 10
    ; Los digitos se obtienen de derecha a izquierda, asi que los guardamos en la pila
    XOR CX, CX         ; Inicializamos contador de digitos a 0
    MOV BX, 10         ; Divisor = 10
    
BUCLE_DIVISION:
    XOR DX, DX         ; Limpiamos DX para la division
    DIV BX             ; AX = AX / 10, DX = resto (digito actual)
    
    PUSH DX            ; Guardamos el digito en la pila
    INC CX             ; Incrementamos contador de digitos
    
    CMP AX, 0          ; ¿El cociente es 0?
    JNE BUCLE_DIVISION ; Si no, continuamos con el siguiente digito
    
    ; Ahora mostramos los digitos en orden correcto (de la pila)
BUCLE_MOSTRAR:
    POP DX             ; Recuperamos un digito
    ADD DL, '0'        ; Convertimos el valor numerico a caracter ASCII
    
    MOV AH, 02h        ; Funcion 2 de DOS: mostrar un caracter
    INT 21h            ; Mostramos el digito
    
    LOOP BUCLE_MOSTRAR ; Repetimos para cada digito (CX veces)
    
FIN_POSITIVO:
    ; Restauramos los registros que modificamos
    POP DX
    POP CX
    POP BX
    POP AX
    RET                ; Retornamos al punto de llamada
MOSTRAR_NUMERO_POSITIVO ENDP

CODIGO ENDS
END INICIO              ; Indicamos el punto de entrada del programa