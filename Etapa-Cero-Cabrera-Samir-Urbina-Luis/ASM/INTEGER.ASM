; ********************************************
; * Programa: INTEGER.ASM                   *
; * Descripcion: Manejo de numeros enteros  *
; * Autores: Luis Urbina, Samir Cabrera     *
; * Fecha: Viernes 07 de Marzo de 2025      *
; ********************************************

; El segmento DATOS contiene todas las variables y constantes que usara el programa
DATOS SEGMENT
    prompt_in  DB 'Ingrese un numero entero: $'  ; Mensaje para solicitar entrada al usuario
    prompt_out DB 'El numero ingresado es: $'    ; Mensaje para mostrar antes del resultado
    buffer     DB 10, ?, 10 DUP(?)  ; Buffer para entrada (maximo 10 caracteres):
                                   ; - Primer byte (10): tamano maximo
                                   ; - Segundo byte (?): aqui DOS guardara cuantos caracteres se leyeron
                                   ; - Resto: espacio para los caracteres ingresados
    numero     DW ?                 ; Variable para almacenar el numero convertido a binario (2 bytes)
    es_negativo DB 0                ; Bandera (flag) para indicar si el numero es negativo (1) o positivo (0)
    nueva_lin  DB 0Dh, 0Ah, '$'     ; Codigos para crear una nueva linea en pantalla
DATOS ENDS

; El segmento CODIGO contiene las instrucciones que ejecutara el programa
CODIGO SEGMENT
    ; Indicamos al ensamblador donde encontrar nuestros datos y codigo
    ASSUME CS:CODIGO, DS:DATOS
INICIO:
    ; Inicializacion: Preparamos el acceso al segmento de datos
    MOV AX, DATOS
    MOV DS, AX
    
    ; Mostramos el mensaje pidiendo al usuario que ingrese un numero
    MOV AH, 09h       ; Funcion 9 de DOS: mostrar una cadena terminada en $
    LEA DX, prompt_in ; Cargamos la direccion del mensaje en DX
    INT 21h           ; Llamamos a la interrupcion 21h (servicios de DOS)
    
    ; Leemos la entrada del usuario como texto
    MOV AH, 0Ah       ; Funcion 0Ah de DOS: leer una cadena (con buffer)
    LEA DX, buffer    ; Cargamos la direccion del buffer en DX
    INT 21h           ; Llamamos a la interrupcion 21h
    
    ; Convertimos la cadena de texto a un numero binario
    CALL STR_A_NUM    ; Llamamos al procedimiento que hace la conversion
    
    ; Mostramos una nueva linea para separar la entrada de la salida
    MOV AH, 09h       ; Funcion 9 de DOS: mostrar una cadena
    LEA DX, nueva_lin ; Cargamos la direccion de la cadena de nueva linea
    INT 21h           ; Llamamos a la interrupcion 21h
    
    ; Mostramos el mensaje que precede al resultado
    MOV AH, 09h        ; Funcion 9 de DOS: mostrar una cadena
    LEA DX, prompt_out ; Cargamos la direccion del mensaje
    INT 21h            ; Llamamos a la interrupcion 21h
    
    ; Convertimos el numero binario a texto y lo mostramos
    MOV AX, [numero]   ; Cargamos el numero en AX para la conversion
    CALL NUM_A_STR     ; Llamamos al procedimiento que hace la conversion y muestra el resultado
    
    ; Terminamos el programa y regresamos al sistema operativo
    MOV AX, 4C00h      ; Funcion 4Ch de DOS: terminar programa (con codigo de salida 0)
    INT 21h            ; Llamamos a la interrupcion 21h

; Este procedimiento convierte una cadena de texto (en el buffer) a un numero binario
; y lo guarda en la variable 'numero'
STR_A_NUM PROC
    ; Guardamos los registros que vamos a modificar para restaurarlos al final
    PUSH AX            ; Guardamos AX en la pila
    PUSH BX            ; Guardamos BX en la pila
    PUSH CX            ; Guardamos CX en la pila
    PUSH DX            ; Guardamos DX en la pila
    PUSH SI            ; Guardamos SI en la pila (indice de origen)
    
    XOR AX, AX         ; Inicializamos AX a 0 (aqui iremos acumulando el resultado)
    MOV BL, [buffer+1] ; En buffer+1 esta la cantidad de caracteres leidos
    XOR BH, BH         ; Limpiamos BH (para que BX solo contenga el valor de BL)
    LEA SI, [buffer+2] ; SI apunta al primer caracter del texto ingresado
    
    ; Reseteamos la bandera de negativo
    MOV [es_negativo], 0
    
    ; Verificamos si el primer caracter es un signo negativo (-)
    CMP BX, 0
    JE CONVERSION_FIN  ; Si la cadena esta vacia, terminamos
    
    MOV CL, [SI]       ; Obtenemos el primer caracter
    CMP CL, '-'        ; ¿Es un signo negativo?
    JNE CONVERSION     ; Si no es negativo, continuamos con la conversion normal
    
    ; Si es negativo, marcamos la bandera y avanzamos al siguiente caracter
    MOV [es_negativo], 1
    INC SI             ; Avanzamos al siguiente caracter
    DEC BX             ; Reducimos el contador de caracteres
    
CONVERSION:
    ; Recorremos cada caracter de la cadena
    CMP BX, 0          ; ¿Terminamos de procesar todos los caracteres?
    JE CONVERSION_PROCESAR
    
    MOV CL, [SI]       ; Obtenemos el caracter actual
    INC SI             ; Avanzamos al siguiente caracter
    
    ; Verificamos si el caracter es un digito (entre '0' y '9')
    CMP CL, '0'
    JL NO_DIGITO       ; Si es menor que '0', no es un digito
    CMP CL, '9'
    JG NO_DIGITO       ; Si es mayor que '9', no es un digito
    
    SUB CL, '0'        ; Convertimos el caracter ASCII a su valor numerico (restando '0')
    XOR CH, CH         ; Limpiamos CH (para que CX solo contenga el valor de CL)
    
    ; Formula para construir el numero: resultado = resultado * 10 + digito
    PUSH BX            ; Guardamos BX temporalmente
    MOV BX, 10
    MUL BX             ; AX = AX * 10
    POP BX             ; Recuperamos BX
    ADD AX, CX         ; AX = AX + digito
    
NO_DIGITO:
    DEC BX             ; Reducimos el contador de caracteres
    JMP CONVERSION     ; Procesamos el siguiente caracter
    
CONVERSION_PROCESAR:
    ; Si el numero es negativo, lo negamos
    CMP [es_negativo], 1
    JNE CONVERSION_FIN
    
    NEG AX             ; Negamos AX (complemento a 2 para obtener el valor negativo)
    
CONVERSION_FIN:
    MOV [numero], AX   ; Guardamos el resultado en la variable 'numero'
    
    ; Restauramos los registros que modificamos
    POP SI
    POP DX
    POP CX
    POP BX
    POP AX
    RET                ; Retornamos al punto de llamada
STR_A_NUM ENDP

; Este procedimiento convierte un numero binario (en AX) a texto y lo muestra en pantalla
NUM_A_STR PROC
    ; Guardamos los registros que vamos a modificar
    PUSH AX
    PUSH BX
    PUSH CX
    PUSH DX
    
    ; Verificamos si el numero es negativo
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
NUM_A_STR ENDP

CODIGO ENDS
END INICIO              ; Indicamos el punto de entrada del programa