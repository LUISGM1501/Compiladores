; ********************************************
; * El tipo de dato seleccionado es flotante *
; * Programa: SELECTED.ASM                   *
; * Descripcion: Manejo de numeros flotantes *
; * Autores: Luis Urbina, Samir Cabrera      *
; * Fecha: Viernes 07 de Marzo de 2025       *
; ********************************************

; El segmento DATOS contiene todas las variables y constantes que usara el programa
DATOS SEGMENT
    prompt_in   DB 'Ingrese un numero flotante (Ej: 3.14): $'  ; Mensaje para solicitar entrada al usuario
    prompt_out  DB 'El numero flotante es: $'                  ; Mensaje para mostrar antes del resultado
    buffer      DB 15, ?, 15 DUP(?)  ; Buffer para entrada (maximo 15 caracteres)
    entero      DW ?                  ; Variable para almacenar la parte entera del numero
    decimal     DW ?                  ; Variable para almacenar la parte decimal del numero
    dec_digitos DB ?                  ; Contador de digitos en la parte decimal
    es_negativo DB 0                  ; Bandera para indicar si el numero es negativo (1) o positivo (0)
    nueva_lin   DB 0Dh, 0Ah, '$'      ; Codigos para crear una nueva linea en pantalla
    punto       DB '.$'               ; Punto decimal seguido de terminador
    constante_diez DW 10              ; Constante 10 para calculos y conversiones
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
    
    ; Mostramos una nueva linea para separar la entrada de la salida
    MOV AH, 09h       ; Funcion 9 de DOS: mostrar una cadena
    LEA DX, nueva_lin ; Cargamos la direccion de la cadena de nueva linea
    INT 21h           ; Llamamos a la interrupcion 21h
    
    ; Mostramos el mensaje que precede al resultado
    MOV AH, 09h        ; Funcion 9 de DOS: mostrar una cadena
    LEA DX, prompt_out ; Cargamos la direccion del mensaje
    INT 21h            ; Llamamos a la interrupcion 21h
    
    ; Mostramos el numero flotante (parte entera, punto decimal y parte decimal)
    CALL MOSTRAR_FLOTANTE  ; Llamamos al procedimiento que muestra el numero
    
    ; Terminamos el programa y regresamos al sistema operativo
    MOV AX, 4C00h      ; Funcion 4Ch de DOS: terminar programa (con codigo de salida 0)
    INT 21h            ; Llamamos a la interrupcion 21h

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
    INC SI
    DEC BX
    
    ; Procesamos la parte entera hasta encontrar el punto decimal
PROC_ENTERO:
    CMP BX, 0             ; ¿Terminamos todos los caracteres?
    JE PROC_FIN
    
    MOV CL, [SI]          ; Obtenemos el caracter actual
    INC SI
    DEC BX
    
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
    INC SI
    DEC BX
    
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
    MOV DL, '0'
    MOV AH, 02h
    INT 21h
    JMP FIN_DECIMAL
    
TIENE_DECIMALES:
    ; Guardamos el numero original de digitos decimales en BX
    MOV CL, [dec_digitos]
    XOR CH, CH
    MOV BX, CX            ; BX = numero de digitos decimales
    
    ; Calculamos la potencia de 10 correspondiente al numero de digitos
    ; (por ejemplo, si hay 3 digitos, necesitamos 10^3 = 1000)
    MOV AX, 1
CALCULAR_POTENCIA:
    CMP CL, 0
    JE FIN_POTENCIA
    
    MUL WORD PTR [constante_diez]  ; AX = AX * 10
    
    DEC CL
    JMP CALCULAR_POTENCIA
    
FIN_POTENCIA:
    MOV CX, AX            ; CX = potencia de 10
    
    ; Verificamos si necesitamos mostrar ceros a la izquierda
    MOV AX, [decimal]
    
    ; Si el decimal es 0, mostramos todos los digitos como ceros
    CMP DX, 0
    JNE CONTAR_DIGITOS
    
    ; Mostramos la cantidad correcta de ceros
    MOV CX, BX            ; CX = numero de digitos decimales
MOSTRAR_SOLO_CEROS:
    CMP CX, 0
    JE FIN_DECIMAL
    
    MOV DL, '0'
    MOV AH, 02h
    INT 21h
    
    DEC CX
    JMP MOSTRAR_SOLO_CEROS
    
CONTAR_DIGITOS:
    ; Contamos cuantos digitos tiene la parte decimal para saber
    ; si necesitamos agregar ceros a la izquierda
    MOV AX, DX            ; AX = valor decimal
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
    MOV DL, '0'
    MOV AH, 02h
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
    MOV DL, '-'
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