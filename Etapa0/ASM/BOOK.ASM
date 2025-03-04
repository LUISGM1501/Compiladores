; ********************************************
; * Programa: BOOK.ASM                      *
; * Descripcion: Manejo de caracteres       *
; * Autores: Luis Urbina, Samir Cabrera     *
; * Fecha: Viernes 07 de Marzo de 2025      *
; ********************************************

; El segmento DATOS contiene todas las variables y constantes que usara el programa
DATOS SEGMENT
    ; Mensajes que se mostraran al usuario
    prompt_in  DB 'Ingrese un caracter: $'    ; Mensaje para solicitar entrada
    prompt_out DB 'El caracter ingresado es: $' ; Mensaje para mostrar el resultado
    caracter   DB ?                 ; Variable para almacenar el caracter (1 byte)
    nueva_lin  DB 0Dh, 0Ah, '$'     ; Codigos para crear una nueva linea en pantalla (retorno de carro + salto de linea)
DATOS ENDS

; El segmento CODIGO contiene las instrucciones del programa
CODIGO SEGMENT
    ; Indicamos al ensamblador donde encontrar nuestros datos y codigo
    ASSUME CS:CODIGO, DS:DATOS
INICIO:
    ; Inicializacion: Cargamos la direccion del segmento de datos en el registro DS
    ; para poder acceder a nuestras variables
    MOV AX, DATOS
    MOV DS, AX
    
    ; Mostramos el mensaje pidiendo al usuario que ingrese un caracter
    MOV AH, 09h       ; Funcion 9 de DOS: mostrar una cadena en pantalla
    LEA DX, prompt_in ; Cargamos la direccion del mensaje en DX
    INT 21h           ; Llamamos a la interrupcion 21h (servicios de DOS)
    
    ; Leemos un caracter del teclado
    MOV AH, 01h       ; Funcion 1 de DOS: leer un caracter con eco (se muestra en pantalla)
    INT 21h           ; Llamamos a la interrupcion 21h
    MOV [caracter], AL ; Guardamos el caracter leido (que esta en AL) en nuestra variable
    
    ; Mostramos una nueva linea para separar la entrada de la salida
    MOV AH, 09h       ; Funcion 9 de DOS: mostrar una cadena
    LEA DX, nueva_lin ; Cargamos la direccion de la cadena de nueva linea
    INT 21h           ; Llamamos a la interrupcion 21h
    
    ; Mostramos el mensaje que precede al resultado
    MOV AH, 09h        ; Funcion 9 de DOS: mostrar una cadena
    LEA DX, prompt_out ; Cargamos la direccion del mensaje
    INT 21h            ; Llamamos a la interrupcion 21h
    
    ; Mostramos el caracter que el usuario ingreso
    MOV DL, [caracter] ; Cargamos el caracter almacenado en nuestra variable
    MOV AH, 02h        ; Funcion 2 de DOS: mostrar un caracter en pantalla
    INT 21h            ; Llamamos a la interrupcion 21h
    
    ; Terminamos el programa y regresamos al sistema operativo
    MOV AX, 4C00h      ; Funcion 4Ch de DOS: terminar programa (con codigo de salida 0)
    INT 21h            ; Llamamos a la interrupcion 21h
CODIGO ENDS
END INICIO              ; Indicamos el punto de entrada del programa