; ********************************************
; * Programa: BOOLEAN.ASM                   *
; * Descripcion: Manejo de booleanos        *
; * Autores: Luis Urbina, Samir Cabrera     *
; * Fecha: Viernes 07 de Marzo de 2025      *
; ********************************************

; El segmento DATOS contiene todas las variables y constantes que usara el programa
DATOS SEGMENT
    prompt_in  DB 'Ingrese 1 para TRUE o 0 para FALSE: $'  ; Mensaje para solicitar entrada al usuario
    prompt_out DB 'El valor booleano es: $'                ; Mensaje para mostrar antes del resultado
    valor_true DB 'TRUE$'     ; Cadena de texto para mostrar cuando el valor es verdadero
    valor_false DB 'FALSE$'   ; Cadena de texto para mostrar cuando el valor es falso
    booleano   DB ?           ; Variable para almacenar el valor booleano (1 = TRUE, 0 = FALSE)
    nueva_lin  DB 0Dh, 0Ah, '$'  ; Codigos para crear una nueva linea en pantalla
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
    JMP MOSTRAR_RESULTADO
    
ES_TRUE:
    MOV [booleano], 1 ; Almacenamos 1 (TRUE) en la variable booleano
    
MOSTRAR_RESULTADO:
    ; Mostramos una nueva linea para separar la entrada de la salida
    MOV AH, 09h       ; Funcion 9 de DOS: mostrar una cadena
    LEA DX, nueva_lin ; Cargamos la direccion de la cadena de nueva linea
    INT 21h           ; Llamamos a la interrupcion 21h
    
    ; Mostramos el mensaje que precede al resultado
    MOV AH, 09h        ; Funcion 9 de DOS: mostrar una cadena
    LEA DX, prompt_out ; Cargamos la direccion del mensaje
    INT 21h            ; Llamamos a la interrupcion 21h
    
    ; Verificamos el valor booleano para mostrar "TRUE" o "FALSE"
    CMP [booleano], 0   ; ¿El valor es 0 (FALSE)?
    JE MOSTRAR_FALSE    ; Si es 0, saltamos a MOSTRAR_FALSE
    
    ; Si llegamos aqui, el valor es 1 (TRUE)
    MOV AH, 09h         ; Funcion 9 de DOS: mostrar una cadena
    LEA DX, valor_true  ; Cargamos la direccion de la cadena "TRUE"
    INT 21h             ; Llamamos a la interrupcion 21h
    JMP FIN_PROGRAMA    ; Saltamos al final del programa
    
MOSTRAR_FALSE:
    ; Mostramos "FALSE"
    MOV AH, 09h          ; Funcion 9 de DOS: mostrar una cadena
    LEA DX, valor_false  ; Cargamos la direccion de la cadena "FALSE"
    INT 21h              ; Llamamos a la interrupcion 21h
    
FIN_PROGRAMA:
    ; Terminamos el programa y regresamos al sistema operativo
    MOV AX, 4C00h      ; Funcion 4Ch de DOS: terminar programa (con codigo de salida 0)
    INT 21h            ; Llamamos a la interrupcion 21h
CODIGO ENDS
END INICIO              ; Indicamos el punto de entrada del programa