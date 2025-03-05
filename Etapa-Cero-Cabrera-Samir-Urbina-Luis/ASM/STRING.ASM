; ********************************************
; * Programa: BOOKANDQ.ASM                  *
; * Descripcion: Manejo de strings          *
; * Autores: Luis Urbina, Samir Cabrera     *
; * Fecha: Viernes 07 de Marzo de 2025      *
; ********************************************

; El segmento DATOS contiene todas las variables y constantes que usara el programa
DATOS SEGMENT
    prompt_in  DB 'Ingrese un texto (max 50 caracteres): $'  ; Mensaje para solicitar la entrada al usuario
    prompt_out DB 'El texto ingresado es: $'                 ; Mensaje para mostrar antes del resultado
    buffer     DB 52, ?, 52 DUP(?)  ; Buffer para entrada:
                                   ; - Primer byte (52): tamano maximo del buffer
                                   ; - Segundo byte (?): aqui DOS guardara cuantos caracteres se leyeron
                                   ; - Resto (52 DUP(?)): espacio para almacenar los caracteres ingresados
    nueva_lin  DB 0Dh, 0Ah, '$'     ; Codigos para crear una nueva linea en pantalla 
                                   ; (0Dh = retorno de carro, 0Ah = salto de linea, $ = terminador)
DATOS ENDS

; El segmento CODIGO contiene las instrucciones que ejecutara el programa
CODIGO SEGMENT
    ; Indicamos al ensamblador donde encontrar nuestros datos y codigo
    ASSUME CS:CODIGO, DS:DATOS
INICIO:
    ; Inicializacion: Cargamos la direccion del segmento de datos en el registro DS
    ; para poder acceder a nuestras variables
    MOV AX, DATOS
    MOV DS, AX
    
    ; Mostramos el mensaje pidiendo al usuario que ingrese un texto
    MOV AH, 09h       ; Funcion 9 de DOS: mostrar una cadena terminada en $
    LEA DX, prompt_in ; Cargamos la direccion del mensaje en DX
    INT 21h           ; Llamamos a la interrupcion 21h (servicios de DOS)
    
    ; Leemos una cadena de texto del teclado
    MOV AH, 0Ah       ; Funcion 0Ah de DOS: leer una cadena (con buffer)
    LEA DX, buffer    ; Cargamos la direccion del buffer en DX
    INT 21h           ; Llamamos a la interrupcion 21h
    
    ; Agregamos un terminador $ al final del texto ingresado para poder mostrarlo despues
    MOV BL, [buffer+1]    ; En buffer+1 esta la cantidad de caracteres leidos
    XOR BH, BH            ; Limpiamos BH (para que BX solo contenga el valor de BL)
    MOV BYTE PTR [buffer+BX+2], '$' ; Colocamos el terminador $ despues del ultimo caracter
                                   ; buffer+2 es donde comienzan los caracteres, +BX es la longitud
    
    ; Mostramos una nueva linea para separar la entrada de la salida
    MOV AH, 09h       ; Funcion 9 de DOS: mostrar una cadena
    LEA DX, nueva_lin ; Cargamos la direccion de la cadena de nueva linea
    INT 21h           ; Llamamos a la interrupcion 21h
    
    ; Mostramos el mensaje que precede al resultado
    MOV AH, 09h        ; Funcion 9 de DOS: mostrar una cadena
    LEA DX, prompt_out ; Cargamos la direccion del mensaje
    INT 21h            ; Llamamos a la interrupcion 21h
    
    ; Mostramos el texto que el usuario ingreso
    MOV AH, 09h        ; Funcion 9 de DOS: mostrar una cadena terminada en $
    LEA DX, [buffer+2] ; Cargamos la direccion donde comienzan los caracteres
                      ; buffer+0: tamano maximo, buffer+1: caracteres leidos, buffer+2: primer caracter
    INT 21h            ; Llamamos a la interrupcion 21h
    
    ; Terminamos el programa y regresamos al sistema operativo
    MOV AX, 4C00h      ; Funcion 4Ch de DOS: terminar programa (con codigo de salida 0)
    INT 21h            ; Llamamos a la interrupcion 21h
CODIGO ENDS
END INICIO              ; Indicamos el punto de entrada del programa