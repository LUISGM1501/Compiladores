; ********************************************
; * Programa: CHAR.ASM  (RUNE)              *
; * Descripcion: Operaciones sobre caracteres*
; * Autores: Luis Urbina, Samir Cabrera     *
; * Fecha: 10/05/2025                       *
; * Version: 1.0                            *
; * Curso: Compiladores e Interpretes       *
; * Proyecto: Notch Engine - Etapa 2        *
; ********************************************

; El segmento DATOS contiene todas las variables y constantes que usara el programa
DATOS SEGMENT
    ; Mensajes de entrada y salida
    titulo       DB "DEMOSTRACION DE OPERACIONES CON RUNE (CARACTERES)", 0Dh, 0Ah, '$'
    separador    DB "----------------------------------------", 0Dh, 0Ah, '$'
    
    menu         DB "MENU DE OPERACIONES:", 0Dh, 0Ah
                 DB "1. isEngraved - Verificar si es letra", 0Dh, 0Ah
                 DB "2. isInscribed - Verificar si es digito", 0Dh, 0Ah
                 DB "3. etchUp - Convertir a mayuscula", 0Dh, 0Ah
                 DB "4. etchDown - Convertir a minuscula", 0Dh, 0Ah
                 DB "5. Comparacion de caracteres", 0Dh, 0Ah
                 DB "6. Convertir a otros tipos", 0Dh, 0Ah
                 DB "0. Salir", 0Dh, 0Ah
                 DB "Seleccione una opcion: $"
    
    prompt_char   DB "Ingrese un caracter: $"
    prompt_chars  DB "Ingrese dos caracteres (sin espacio): $"
    result_msg    DB "Resultado: $"
    
    ; Mensajes para resultados específicos
    msg_is_letter      DB "El caracter es una letra: $"
    msg_is_digit       DB "El caracter es un digito: $"
    msg_uppercase      DB "En mayuscula: $"
    msg_lowercase      DB "En minuscula: $"
    
    ; Mensajes para comparaciones
    msg_menor    DB 0Dh, 0Ah, "MENOR QUE (<): $"
    msg_mayor    DB 0Dh, 0Ah, "MAYOR QUE (>): $"
    msg_menig    DB 0Dh, 0Ah, "MENOR O IGUAL QUE (<=): $"
    msg_mayig    DB 0Dh, 0Ah, "MAYOR O IGUAL QUE (>=): $"
    msg_igual    DB 0Dh, 0Ah, "IGUAL A (is): $"
    msg_nig      DB 0Dh, 0Ah, "DISTINTO DE (isNot): $"
    
    ; Mensajes para conversiones
    prompt_original DB 'El caracter ingresado es: $'
    prompt_int      DB 'Convertido a entero (ASCII): $'
    prompt_float    DB 'Convertido a flotante: $'
    prompt_bool     DB 'Convertido a booleano: $'
    prompt_string   DB 'Convertido a string: $'
    prompt_creativo DB 'Convertido a creativo (probabilidad): $'
    
    ; Variables para almacenar valores
    caracter1       DB ?     ; Primer caracter
    caracter2       DB ?     ; Segundo caracter
    resultado_bool  DB ?     ; Resultado booleano
    
    ; Variables para conversiones
    entero_result   DW ?     ; Conversión a entero
    float_entero    DW ?     ; Parte entera del flotante
    float_decimal   DW ?     ; Parte decimal del flotante
    dec_digitos     DB ?     ; Dígitos decimales
    bool_result     DB ?     ; Conversión a booleano
    string_buffer   DB 2 DUP(?), '$' ; Buffer para conversión a string
    prob_valor      DB ?     ; Valor para tipo creativo
    
    ; Valores para mostrar booleanos
    valor_true    DB 'TRUE$'
    valor_false   DB 'FALSE$'
    
    ; Auxiliares
    nueva_lin    DB 0Dh, 0Ah, '$'
    punto        DB '.$'
DATOS ENDS

; El segmento CODIGO contiene las instrucciones que ejecutara el programa
CODIGO SEGMENT
    ; Indicamos al ensamblador donde encontrar nuestros datos y codigo
    ASSUME CS:CODIGO, DS:DATOS
INICIO:
    ; Inicialización: Preparamos el acceso al segmento de datos
    MOV AX, DATOS
    MOV DS, AX
    
    ; Mostrar título
    MOV AH, 09h
    LEA DX, titulo
    INT 21h
    
    LEA DX, separador
    INT 21h

MENU_PRINCIPAL:
    ; Mostrar menú de opciones
    MOV AH, 09h
    LEA DX, menu
    INT 21h
    
    ; Leer opción del usuario
    MOV AH, 01h
    INT 21h
    
    ; Comparar con las opciones disponibles - usando saltos largos
    CMP AL, '1'
    JNE @MENU_NOT1
    JMP OPCION_IS_LETTER
@MENU_NOT1:
    CMP AL, '2'
    JNE @MENU_NOT2
    JMP OPCION_IS_DIGIT
@MENU_NOT2:
    CMP AL, '3'
    JNE @MENU_NOT3
    JMP OPCION_TO_UPPERCASE
@MENU_NOT3:
    CMP AL, '4'
    JNE @MENU_NOT4
    JMP OPCION_TO_LOWERCASE
@MENU_NOT4:
    CMP AL, '5'
    JNE @MENU_NOT5
    JMP OPCION_COMPARACIONES
@MENU_NOT5:
    CMP AL, '6'
    JNE @MENU_NOT6
    JMP OPCION_CONVERSIONES
@MENU_NOT6:
    CMP AL, '0'
    JNE @MENU_NOT0
    JMP SALIR
@MENU_NOT0:
    
    ; Si llegamos aquí, la opción no es válida, volver al menú
    JMP MENU_PRINCIPAL

    OPCION_IS_LETTER:
    CALL NUEVA_LINEA
    CALL LEER_CARACTER
    
    ; Verificar si es letra (isEngraved)
    MOV AL, [caracter1]
    CALL ES_LETRA
    MOV [resultado_bool], AL
    
    ; Mostrar resultado
    MOV AH, 09h
    LEA DX, msg_is_letter
    INT 21h
    
    CALL MOSTRAR_RESULTADO_BOOL
    JMP MENU_PRINCIPAL
    
OPCION_IS_DIGIT:
    CALL NUEVA_LINEA
    CALL LEER_CARACTER
    
    ; Verificar si es dígito (isInscribed)
    MOV AL, [caracter1]
    CALL ES_DIGITO
    MOV [resultado_bool], AL
    
    ; Mostrar resultado
    MOV AH, 09h
    LEA DX, msg_is_digit
    INT 21h
    
    CALL MOSTRAR_RESULTADO_BOOL
    JMP MENU_PRINCIPAL

OPCION_TO_UPPERCASE:
    CALL NUEVA_LINEA
    CALL LEER_CARACTER
    
    ; Convertir a mayúscula (etchUp)
    MOV AL, [caracter1]
    CALL A_MAYUSCULA
    MOV [caracter2], AL
    
    ; Mostrar resultado
    MOV AH, 09h
    LEA DX, msg_uppercase
    INT 21h
    
    MOV DL, [caracter2]
    MOV AH, 02h
    INT 21h
    
    CALL NUEVA_LINEA
    CALL NUEVA_LINEA
    JMP MENU_PRINCIPAL

OPCION_TO_LOWERCASE:
    CALL NUEVA_LINEA
    CALL LEER_CARACTER
    
    ; Convertir a minúscula (etchDown)
    MOV AL, [caracter1]
    CALL A_MINUSCULA
    MOV [caracter2], AL
    
    ; Mostrar resultado
    MOV AH, 09h
    LEA DX, msg_lowercase
    INT 21h
    
    MOV DL, [caracter2]
    MOV AH, 02h
    INT 21h
    
    CALL NUEVA_LINEA
    CALL NUEVA_LINEA
    JMP MENU_PRINCIPAL

    OPCION_COMPARACIONES:
    CALL NUEVA_LINEA
    CALL LEER_DOS_CARACTERES
    
    ; Comparar MENOR QUE (<)
    MOV AH, 09h
    LEA DX, msg_menor
    INT 21h
    
    MOV AL, [caracter1]
    CMP AL, [caracter2]
    MOV AH, 09h
    JL @CHAR_COMP_MENOR_TRUE
    LEA DX, valor_false
    JMP @CHAR_SHOW_MENOR
@CHAR_COMP_MENOR_TRUE:
    LEA DX, valor_true
@CHAR_SHOW_MENOR:
    INT 21h
    
    ; Comparar MAYOR QUE (>)
    MOV AH, 09h
    LEA DX, msg_mayor
    INT 21h
    
    MOV AL, [caracter1]
    CMP AL, [caracter2]
    MOV AH, 09h
    JG @CHAR_COMP_MAYOR_TRUE
    LEA DX, valor_false
    JMP @CHAR_SHOW_MAYOR
@CHAR_COMP_MAYOR_TRUE:
    LEA DX, valor_true
@CHAR_SHOW_MAYOR:
    INT 21h
    
    ; Comparar MENOR O IGUAL QUE (<=)
    MOV AH, 09h
    LEA DX, msg_menig
    INT 21h
    
    MOV AL, [caracter1]
    CMP AL, [caracter2]
    MOV AH, 09h
    JLE @CHAR_COMP_MENIG_TRUE
    LEA DX, valor_false
    JMP @CHAR_SHOW_MENIG
@CHAR_COMP_MENIG_TRUE:
    LEA DX, valor_true
@CHAR_SHOW_MENIG:
    INT 21h
    
    ; Comparar MAYOR O IGUAL QUE (>=)
    MOV AH, 09h
    LEA DX, msg_mayig
    INT 21h
    
    MOV AL, [caracter1]
    CMP AL, [caracter2]
    MOV AH, 09h
    JGE @CHAR_COMP_MAYIG_TRUE
    LEA DX, valor_false
    JMP @CHAR_SHOW_MAYIG
@CHAR_COMP_MAYIG_TRUE:
    LEA DX, valor_true
@CHAR_SHOW_MAYIG:
    INT 21h
    
    ; Comparar IGUAL A (is)
    MOV AH, 09h
    LEA DX, msg_igual
    INT 21h
    
    MOV AL, [caracter1]
    CMP AL, [caracter2]
    MOV AH, 09h
    JE @CHAR_COMP_IGUAL_TRUE
    LEA DX, valor_false
    JMP @CHAR_SHOW_IGUAL
@CHAR_COMP_IGUAL_TRUE:
    LEA DX, valor_true
@CHAR_SHOW_IGUAL:
    INT 21h
    
    ; Comparar DISTINTO DE (isNot)
    MOV AH, 09h
    LEA DX, msg_nig
    INT 21h
    
    MOV AL, [caracter1]
    CMP AL, [caracter2]
    MOV AH, 09h
    JNE @CHAR_COMP_NOEQ_TRUE
    LEA DX, valor_false
    JMP @CHAR_SHOW_NOEQ
@CHAR_COMP_NOEQ_TRUE:
    LEA DX, valor_true
@CHAR_SHOW_NOEQ:
    INT 21h
    
    CALL NUEVA_LINEA
    JMP MENU_PRINCIPAL

OPCION_CONVERSIONES:
    CALL NUEVA_LINEA
    CALL LEER_CARACTER
    
    ; Realizar todas las conversiones
    CALL CHAR_A_INT
    CALL CHAR_A_FLOAT
    CALL CHAR_A_BOOL
    CALL CHAR_A_STRING
    CALL CHAR_A_CREATIVO
    
    ; Mostrar el valor original y todas las conversiones
    CALL MOSTRAR_CONVERSIONES
    
    JMP MENU_PRINCIPAL

    ;------------------------------------------------------------
; Procedimiento: ES_LETRA
; Verifica si un carácter es una letra (isEngraved)
; Entrada: AL = carácter a verificar
; Salida: AL = 1 si es letra, 0 si no
;------------------------------------------------------------
ES_LETRA PROC
    ; Verificar si es letra mayúscula (A-Z)
    CMP AL, 'A'
    JL @LETRA_NO_ES_MAYUSCULA
    CMP AL, 'Z'
    JLE @LETRA_ES_LETRA
    
@LETRA_NO_ES_MAYUSCULA:
    ; Verificar si es letra minúscula (a-z)
    CMP AL, 'a'
    JL @LETRA_NO_ES_LETRA
    CMP AL, 'z'
    JLE @LETRA_ES_LETRA
    
@LETRA_NO_ES_LETRA:
    ; No es letra
    XOR AL, AL    ; AL = 0 (falso)
    RET
    
@LETRA_ES_LETRA:
    ; Es letra
    MOV AL, 1     ; AL = 1 (verdadero)
    RET
ES_LETRA ENDP

;------------------------------------------------------------
; Procedimiento: ES_DIGITO
; Verifica si un carácter es un dígito (isInscribed)
; Entrada: AL = carácter a verificar
; Salida: AL = 1 si es dígito, 0 si no
;------------------------------------------------------------
ES_DIGITO PROC
    ; Verificar si es dígito (0-9)
    CMP AL, '0'
    JL @DIGITO_NO_ES_DIGITO
    CMP AL, '9'
    JG @DIGITO_NO_ES_DIGITO
    
    ; Es dígito
    MOV AL, 1     ; AL = 1 (verdadero)
    RET
    
@DIGITO_NO_ES_DIGITO:
    ; No es dígito
    XOR AL, AL    ; AL = 0 (falso)
    RET
ES_DIGITO ENDP

;------------------------------------------------------------
; Procedimiento: A_MAYUSCULA
; Convierte un carácter a mayúscula (etchUp)
; Entrada: AL = carácter a convertir
; Salida: AL = carácter convertido
;------------------------------------------------------------
A_MAYUSCULA PROC
    ; Verificar si es letra minúscula
    CMP AL, 'a'
    JL @MAYUS_NO_CONVERTIR
    CMP AL, 'z'
    JG @MAYUS_NO_CONVERTIR
    
    ; Convertir a mayúscula (restar 32)
    SUB AL, 32
    RET
    
@MAYUS_NO_CONVERTIR:
    ; No es letra minúscula, devolver sin cambios
    RET
A_MAYUSCULA ENDP

;------------------------------------------------------------
; Procedimiento: A_MINUSCULA
; Convierte un carácter a minúscula (etchDown)
; Entrada: AL = carácter a convertir
; Salida: AL = carácter convertido
;------------------------------------------------------------
A_MINUSCULA PROC
    ; Verificar si es letra mayúscula
    CMP AL, 'A'
    JL @MINUS_NO_CONVERTIR
    CMP AL, 'Z'
    JG @MINUS_NO_CONVERTIR
    
    ; Convertir a minúscula (sumar 32)
    ADD AL, 32
    RET
    
@MINUS_NO_CONVERTIR:
    ; No es letra mayúscula, devolver sin cambios
    RET
A_MINUSCULA ENDP

;------------------------------------------------------------
; Procedimiento: CHAR_A_INT
; Convierte un carácter a entero (código ASCII)
;------------------------------------------------------------
CHAR_A_INT PROC
    ; Para carácter a entero, usamos el código ASCII
    XOR AH, AH
    MOV AL, [caracter1]
    MOV [entero_result], AX
    
    RET
CHAR_A_INT ENDP

;------------------------------------------------------------
; Procedimiento: CHAR_A_FLOAT
; Convierte un carácter a flotante (código ASCII.00)
;------------------------------------------------------------
CHAR_A_FLOAT PROC
    ; Para carácter a flotante, usamos el código ASCII como parte entera
    XOR AH, AH
    MOV AL, [caracter1]
    MOV [float_entero], AX
    
    ; La parte decimal es 0
    MOV WORD PTR [float_decimal], 0
    MOV BYTE PTR [dec_digitos], 2    ; Dos dígitos decimales (00)
    
    RET
CHAR_A_FLOAT ENDP

;------------------------------------------------------------
; Procedimiento: CHAR_A_BOOL
; Convierte un carácter a booleano (false si nulo, true en caso contrario)
;------------------------------------------------------------
CHAR_A_BOOL PROC
    ; Para carácter a booleano, es FALSE solo si el código ASCII es 0
    CMP BYTE PTR [caracter1], 0
    JE @CHAR_BOOL_FALSE
    
    ; Si no es carácter nulo, es TRUE
    MOV [bool_result], 1
    JMP @CHAR_BOOL_FIN
    
@CHAR_BOOL_FALSE:
    MOV [bool_result], 0
    
@CHAR_BOOL_FIN:
    RET
CHAR_A_BOOL ENDP

;------------------------------------------------------------
; Procedimiento: CHAR_A_STRING
; Convierte un carácter a string (caracter + terminador)
;------------------------------------------------------------
CHAR_A_STRING PROC
    ; Para carácter a string, copiamos el carácter al buffer
    MOV AL, [caracter1]
    MOV [string_buffer], AL
    MOV BYTE PTR [string_buffer+1], '$'    ; Terminador
    
    RET
CHAR_A_STRING ENDP

;------------------------------------------------------------
; Procedimiento: CHAR_A_CREATIVO
; Convierte un carácter a creativo (0 si nulo, 1 en caso contrario)
;------------------------------------------------------------
CHAR_A_CREATIVO PROC
    ; Para carácter a creativo (probabilidad)
    CMP BYTE PTR [caracter1], 0
    JE @CHAR_PROB_CERO
    
    ; Si no es carácter nulo, es 1
    MOV [prob_valor], 1
    JMP @CHAR_CREATIVO_FIN
    
@CHAR_PROB_CERO:
    MOV [prob_valor], 0
    
@CHAR_CREATIVO_FIN:
    RET
CHAR_A_CREATIVO ENDP

;------------------------------------------------------------
; Procedimiento: LEER_CARACTER
; Lee un carácter desde la entrada estándar
;------------------------------------------------------------
LEER_CARACTER PROC
    ; Mostrar mensaje
    MOV AH, 09h
    LEA DX, prompt_char
    INT 21h
    
    ; Leer un carácter
    MOV AH, 01h
    INT 21h
    
    ; Guardar el carácter
    MOV [caracter1], AL
    
    CALL NUEVA_LINEA
    
    RET
LEER_CARACTER ENDP

;------------------------------------------------------------
; Procedimiento: LEER_DOS_CARACTERES
; Lee dos caracteres desde la entrada estándar
;------------------------------------------------------------
LEER_DOS_CARACTERES PROC
    ; Mostrar mensaje
    MOV AH, 09h
    LEA DX, prompt_chars
    INT 21h
    
    ; Leer primer carácter
    MOV AH, 01h
    INT 21h
    MOV [caracter1], AL
    
    ; Leer segundo carácter
    MOV AH, 01h
    INT 21h
    MOV [caracter2], AL
    
    CALL NUEVA_LINEA
    
    RET
LEER_DOS_CARACTERES ENDP

;------------------------------------------------------------
; Procedimiento: MOSTRAR_RESULTADO_BOOL
; Muestra un resultado booleano como TRUE o FALSE
;------------------------------------------------------------
MOSTRAR_RESULTADO_BOOL PROC
    ; Mostrar "TRUE" o "FALSE" según el resultado
    CMP BYTE PTR [resultado_bool], 0
    JE @CHAR_MOSTRAR_RESULT_FALSE
    
    LEA DX, valor_true
    JMP @CHAR_MOSTRAR_RESULT_VALOR
    
@CHAR_MOSTRAR_RESULT_FALSE:
    LEA DX, valor_false
    
@CHAR_MOSTRAR_RESULT_VALOR:
    MOV AH, 09h
    INT 21h
    
    CALL NUEVA_LINEA
    CALL NUEVA_LINEA
    
    RET
MOSTRAR_RESULTADO_BOOL ENDP

;------------------------------------------------------------
; Procedimiento: MOSTRAR_CONVERSIONES
; Muestra los resultados de todas las conversiones
;------------------------------------------------------------
MOSTRAR_CONVERSIONES PROC
    ; Mostrar el carácter original
    CALL NUEVA_LINEA
    MOV AH, 09h
    LEA DX, prompt_original
    INT 21h
    
    MOV DL, [caracter1]
    MOV AH, 02h
    INT 21h
    
    ; Mostrar conversión a entero (ASCII)
    CALL NUEVA_LINEA
    MOV AH, 09h
    LEA DX, prompt_int
    INT 21h
    
    MOV AX, [entero_result]
    CALL MOSTRAR_NUMERO
    
    ; Mostrar conversión a flotante
    CALL NUEVA_LINEA
    MOV AH, 09h
    LEA DX, prompt_float
    INT 21h
    
    CALL MOSTRAR_FLOTANTE
    
    ; Mostrar conversión a booleano
    CALL NUEVA_LINEA
    MOV AH, 09h
    LEA DX, prompt_bool
    INT 21h
    
    ; Mostrar "TRUE" o "FALSE"
    CMP BYTE PTR [bool_result], 0
    JE @CHAR_MOSTRAR_CONV_FALSE
    
    LEA DX, valor_true
    JMP @CHAR_MOSTRAR_CONV_VALOR
    
@CHAR_MOSTRAR_CONV_FALSE:
    LEA DX, valor_false
    
@CHAR_MOSTRAR_CONV_VALOR:
    MOV AH, 09h
    INT 21h
    
    ; Mostrar conversión a string
    CALL NUEVA_LINEA
    MOV AH, 09h
    LEA DX, prompt_string
    INT 21h
    
    LEA DX, string_buffer
    INT 21h
    
    ; Mostrar conversión a creativo
    CALL NUEVA_LINEA
    MOV AH, 09h
    LEA DX, prompt_creativo
    INT 21h
    
    ; Mostrar valor creativo como "0.X"
    MOV DL, '0'
    MOV AH, 02h
    INT 21h
    
    MOV AH, 09h
    LEA DX, punto
    INT 21h
    
    MOV DL, [prob_valor]
    ADD DL, '0'
    MOV AH, 02h
    INT 21h
    
    CALL NUEVA_LINEA
    
    RET
MOSTRAR_CONVERSIONES ENDP

;------------------------------------------------------------
; Procedimiento: MOSTRAR_NUMERO
; Muestra un número entero en pantalla
; Entrada: AX = número a mostrar
;------------------------------------------------------------
MOSTRAR_NUMERO PROC
    PUSH BX
    PUSH CX
    PUSH DX
    
    ; Caso especial: si el número es cero
    CMP AX, 0
    JNE @CHAR_ENTERO_NO_CERO
    
    MOV DL, '0'
    MOV AH, 02h
    INT 21h
    JMP @CHAR_FIN_MOSTRAR_NUMERO
    
@CHAR_ENTERO_NO_CERO:
    ; Convertir a dígitos y mostrar
    MOV BX, 10
    XOR CX, CX
    
@CHAR_DIV_LOOP:
    XOR DX, DX
    DIV BX
    PUSH DX
    INC CX
    
    CMP AX, 0
    JNE @CHAR_DIV_LOOP
    
@CHAR_MOSTRAR_DIGITOS:
    POP DX
    ADD DL, '0'
    MOV AH, 02h
    INT 21h
    LOOP @CHAR_MOSTRAR_DIGITOS
    
@CHAR_FIN_MOSTRAR_NUMERO:
    POP DX
    POP CX
    POP BX
    RET
MOSTRAR_NUMERO ENDP

;------------------------------------------------------------
; Procedimiento: MOSTRAR_FLOTANTE
; Muestra un número flotante
;------------------------------------------------------------
MOSTRAR_FLOTANTE PROC
    PUSH AX
    PUSH BX
    PUSH CX
    PUSH DX
    
    ; Mostrar parte entera
    MOV AX, [float_entero]
    CALL MOSTRAR_NUMERO
    
    ; Mostrar punto decimal
    MOV AH, 09h
    LEA DX, punto
    INT 21h
    
    ; Mostrar parte decimal (siempre 00 en este caso)
    MOV DL, '0'
    MOV AH, 02h
    INT 21h
    
    MOV DL, '0'
    MOV AH, 02h
    INT 21h
    
    POP DX
    POP CX
    POP BX
    POP AX
    RET
MOSTRAR_FLOTANTE ENDP

;------------------------------------------------------------
; Procedimiento: NUEVA_LINEA
; Muestra un salto de línea
;------------------------------------------------------------
NUEVA_LINEA PROC
    PUSH AX
    PUSH DX
    
    MOV AH, 09h
    LEA DX, nueva_lin
    INT 21h
    
    POP DX
    POP AX
    RET
NUEVA_LINEA ENDP

SALIR:
    ; Terminamos el programa y regresamos al sistema operativo
    MOV AX, 4C00h      ; Función 4Ch de DOS: terminar programa (con código de salida 0)
    INT 21h            ; Llamamos a la interrupción 21h
    
CODIGO ENDS
END INICIO              ; Indicamos el punto de entrada del programa