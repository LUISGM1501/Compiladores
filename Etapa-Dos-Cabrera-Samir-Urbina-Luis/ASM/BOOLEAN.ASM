; ********************************************
; * Programa: BOOLEAN.ASM  (TORCH)          *
; * Descripcion: Operaciones sobre booleanos*
; * Autores: Luis Urbina, Samir Cabrera     *
; * Fecha: 10/05/2025                       *
; * Version: 1.0                            *
; * Curso: Compiladores e Interpretes       *
; * Proyecto: Notch Engine - Etapa 2        *
; ********************************************

; El segmento DATOS contiene todas las variables y constantes que usara el programa
DATOS SEGMENT
    ; Mensajes de entrada y salida
    titulo       DB "DEMOSTRACION DE OPERACIONES CON TORCH (BOOLEANOS)", 0Dh, 0Ah, '$'
    separador    DB "----------------------------------------", 0Dh, 0Ah, '$'
    
    menu         DB "MENU DE OPERACIONES:", 0Dh, 0Ah
                 DB "1. AND - Conjuncion logica", 0Dh, 0Ah
                 DB "2. OR - Disyuncion logica", 0Dh, 0Ah
                 DB "3. NOT - Negacion logica", 0Dh, 0Ah
                 DB "4. XOR - Disyuncion exclusiva", 0Dh, 0Ah
                 DB "5. Comparaciones de valores booleanos", 0Dh, 0Ah
                 DB "6. Convertir a otros tipos", 0Dh, 0Ah
                 DB "0. Salir", 0Dh, 0Ah
                 DB "Seleccione una opcion: $"
    
    prompt_bool1  DB "Ingrese primer valor booleano (1=On, 0=Off): $"
    prompt_bool2  DB "Ingrese segundo valor booleano (1=On, 0=Off): $"
    result_msg    DB "Resultado: $"
    
    prompt_bool   DB 'El valor booleano ingresado es: $'
    prompt_int    DB 'Convertido a entero: $'
    prompt_float  DB 'Convertido a flotante: $'
    prompt_char   DB 'Convertido a caracter: $'
    prompt_string DB 'Convertido a string: $'
    prompt_creativo DB 'Convertido a creativo (probabilidad): $'
    
    ; Variables para almacenar valores
    bool_valor1   DB ?     ; Primer valor booleano (1=On, 0=Off)
    bool_valor2   DB ?     ; Segundo valor booleano
    resultado_bool DB ?    ; Resultado de operación booleana
    
    ; Valores para mostrar booleanos
    valor_true    DB 'TRUE$'
    valor_false   DB 'FALSE$'
    str_on        DB 'On$'
    str_off       DB 'Off$'
    
    ; Variables para conversiones
    entero_result  DW ?    ; Conversión a entero
    float_entero   DW ?    ; Parte entera del flotante
    float_decimal  DW ?    ; Parte decimal del flotante
    dec_digitos    DB ?    ; Dígitos decimales
    char_result    DB ?    ; Conversión a carácter
    string_buffer  DB 10 DUP(?), '$' ; Buffer para conversión a string
    prob_valor     DB ?    ; Valor para tipo creativo
    
    ; Mensajes para comparaciones
    msg_igual    DB 0Dh, 0Ah, "IGUAL A (is): $"
    msg_distinto DB 0Dh, 0Ah, "DISTINTO DE (isNot): $"
    
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
    JNE @NOT1
    JMP OPCION_AND
@NOT1:
    CMP AL, '2'
    JNE @NOT2
    JMP OPCION_OR
@NOT2:
    CMP AL, '3'
    JNE @NOT3
    JMP OPCION_NOT
@NOT3:
    CMP AL, '4'
    JNE @NOT4
    JMP OPCION_XOR
@NOT4:
    CMP AL, '5'
    JNE @NOT5
    JMP OPCION_COMPARACIONES
@NOT5:
    CMP AL, '6'
    JNE @NOT6
    JMP OPCION_CONVERSIONES
@NOT6:
    CMP AL, '0'
    JNE @NOT0
    JMP SALIR
@NOT0:
    
    ; Si llegamos aquí, la opción no es válida, volver al menú
    JMP MENU_PRINCIPAL

    OPCION_AND:
    CALL NUEVA_LINEA
    CALL LEER_DOS_BOOLEANOS
    
    ; Realizar la operación AND
    MOV AL, [bool_valor1]
    AND AL, [bool_valor2]
    MOV [resultado_bool], AL
    
    ; Mostrar resultado
    CALL MOSTRAR_RESULTADO_BOOL
    JMP MENU_PRINCIPAL
    
OPCION_OR:
    CALL NUEVA_LINEA
    CALL LEER_DOS_BOOLEANOS
    
    ; Realizar la operación OR
    MOV AL, [bool_valor1]
    OR AL, [bool_valor2]
    MOV [resultado_bool], AL
    
    ; Mostrar resultado
    CALL MOSTRAR_RESULTADO_BOOL
    JMP MENU_PRINCIPAL

OPCION_NOT:
    CALL NUEVA_LINEA
    
    ; Leer un solo valor booleano
    MOV AH, 09h
    LEA DX, prompt_bool1
    INT 21h
    
    CALL LEER_BOOLEANO
    MOV [bool_valor1], AL
    
    ; Realizar la operación NOT
    MOV AL, [bool_valor1]
    XOR AL, 1       ; Invertir el bit menos significativo (0->1, 1->0)
    MOV [resultado_bool], AL
    
    ; Mostrar resultado
    CALL MOSTRAR_RESULTADO_BOOL
    JMP MENU_PRINCIPAL

OPCION_XOR:
    CALL NUEVA_LINEA
    CALL LEER_DOS_BOOLEANOS
    
    ; Realizar la operación XOR
    MOV AL, [bool_valor1]
    XOR AL, [bool_valor2]
    MOV [resultado_bool], AL
    
    ; Mostrar resultado
    CALL MOSTRAR_RESULTADO_BOOL
    JMP MENU_PRINCIPAL

    OPCION_COMPARACIONES:
    CALL NUEVA_LINEA
    CALL LEER_DOS_BOOLEANOS
    
    ; Comparar IGUAL A (is)
    MOV AH, 09h
    LEA DX, msg_igual
    INT 21h
    
    MOV AL, [bool_valor1]
    CMP AL, [bool_valor2]
    MOV AH, 09h
    JE @COMP_IGUAL_TRUE
    LEA DX, valor_false
    JMP @SHOW_IGUAL
@COMP_IGUAL_TRUE:
    LEA DX, valor_true
@SHOW_IGUAL:
    INT 21h
    
    ; Comparar DISTINTO DE (isNot)
    MOV AH, 09h
    LEA DX, msg_distinto
    INT 21h
    
    MOV AL, [bool_valor1]
    CMP AL, [bool_valor2]
    MOV AH, 09h
    JNE @COMP_NOEQ_TRUE
    LEA DX, valor_false
    JMP @SHOW_NOEQ
@COMP_NOEQ_TRUE:
    LEA DX, valor_true
@SHOW_NOEQ:
    INT 21h
    
    CALL NUEVA_LINEA
    JMP MENU_PRINCIPAL

OPCION_CONVERSIONES:
    CALL NUEVA_LINEA
    
    ; Leer un valor booleano
    MOV AH, 09h
    LEA DX, prompt_bool1
    INT 21h
    
    CALL LEER_BOOLEANO
    MOV [bool_valor1], AL
    
    ; Realizar todas las conversiones
    CALL BOOL_A_INT
    CALL BOOL_A_FLOAT
    CALL BOOL_A_CHAR
    CALL BOOL_A_STRING
    CALL BOOL_A_CREATIVO
    
    ; Mostrar el valor original y todas las conversiones
    CALL MOSTRAR_CONVERSIONES
    
    JMP MENU_PRINCIPAL

    ;------------------------------------------------------------
; Procedimiento: BOOL_A_INT
; Convierte el valor booleano a entero (0 o 1)
;------------------------------------------------------------
BOOL_A_INT PROC
    ; Para booleano a entero, copiamos el valor tal cual
    XOR AX, AX              ; Limpiamos AX
    MOV AL, [bool_valor1]   ; Cargamos el valor booleano
    MOV [entero_result], AX ; Guardamos en la variable entero
    
    RET
BOOL_A_INT ENDP

;------------------------------------------------------------
; Procedimiento: BOOL_A_FLOAT
; Convierte el valor booleano a flotante (0.0 o 1.0)
;------------------------------------------------------------
BOOL_A_FLOAT PROC
    ; Para booleano a flotante, usamos 0.0 para Off y 1.0 para On
    XOR AX, AX
    MOV AL, [bool_valor1]
    MOV [float_entero], AX    ; Parte entera
    
    ; La parte decimal es siempre 0
    MOV WORD PTR [float_decimal], 0
    MOV BYTE PTR [dec_digitos], 1  ; Un dígito decimal (0)
    
    RET
BOOL_A_FLOAT ENDP

;------------------------------------------------------------
; Procedimiento: BOOL_A_CHAR
; Convierte el valor booleano a caracter ('0' o '1')
;------------------------------------------------------------
BOOL_A_CHAR PROC
    ; Para booleano a caracter, usamos '0' o '1'
    MOV AL, [bool_valor1]
    ADD AL, '0'             ; Convertir a ASCII
    MOV [char_result], AL
    
    RET
BOOL_A_CHAR ENDP

;------------------------------------------------------------
; Procedimiento: BOOL_A_STRING
; Convierte el valor booleano a string ("On" o "Off")
;------------------------------------------------------------
BOOL_A_STRING PROC
    ; Para booleano a string, usamos "On" o "Off"
    ; En este procedimiento, en lugar de generar el string,
    ; sólo establecemos un puntero a la cadena apropiada
    
    CMP BYTE PTR [bool_valor1], 0
    JE BOOL_STRING_OFF
    
    ; Si el valor es 1 (On)
    MOV SI, OFFSET str_on
    JMP COPY_BOOL_STRING
    
BOOL_STRING_OFF:
    ; Si el valor es 0 (Off)
    MOV SI, OFFSET str_off
    
COPY_BOOL_STRING:
    ; Copiar el string al buffer (sin incluir el $)
    MOV DI, OFFSET string_buffer
    
COPY_LOOP:
    MOV AL, [SI]
    MOV [DI], AL
    
    CMP AL, '$'
    JE END_COPY
    
    INC SI
    INC DI
    JMP COPY_LOOP
    
END_COPY:
    RET
BOOL_A_STRING ENDP

;------------------------------------------------------------
; Procedimiento: BOOL_A_CREATIVO
; Convierte el valor booleano a creativo (0.0 o 1.0)
;------------------------------------------------------------
BOOL_A_CREATIVO PROC
    ; Para creativo, usamos directamente el valor booleano
    MOV AL, [bool_valor1]
    MOV [prob_valor], AL
    
    RET
BOOL_A_CREATIVO ENDP

;------------------------------------------------------------
; Procedimiento: LEER_BOOLEANO
; Lee un valor booleano (0 o 1) desde la entrada estándar
; Retorna: AL = 0 (Off) o 1 (On)
;------------------------------------------------------------
LEER_BOOLEANO PROC
    ; Leer un carácter
    MOV AH, 01h
    INT 21h
    
    ; Convertir a valor booleano
    CMP AL, '1'
    JE VALOR_ON
    
    ; Si no es '1', asumimos 0 (Off)
    XOR AL, AL   ; AL = 0
    RET
    
VALOR_ON:
    MOV AL, 1    ; AL = 1
    RET
LEER_BOOLEANO ENDP

;------------------------------------------------------------
; Procedimiento: LEER_DOS_BOOLEANOS
; Lee dos valores booleanos desde la entrada estándar
;------------------------------------------------------------
LEER_DOS_BOOLEANOS PROC
    ; Leer primer valor
    MOV AH, 09h
    LEA DX, prompt_bool1
    INT 21h
    
    CALL LEER_BOOLEANO
    MOV [bool_valor1], AL
    
    ; Leer segundo valor
    MOV AH, 09h
    LEA DX, prompt_bool2
    INT 21h
    
    CALL LEER_BOOLEANO
    MOV [bool_valor2], AL
    
    RET
LEER_DOS_BOOLEANOS ENDP

;------------------------------------------------------------
; Procedimiento: MOSTRAR_RESULTADO_BOOL
; Muestra el resultado de una operación booleana
;------------------------------------------------------------
MOSTRAR_RESULTADO_BOOL PROC
    CALL NUEVA_LINEA
    
    MOV AH, 09h
    LEA DX, result_msg
    INT 21h
    
    ; Mostrar "TRUE" o "FALSE" según el resultado
    CMP BYTE PTR [resultado_bool], 0
    JE MOSTRAR_FALSE
    
    LEA DX, valor_true
    JMP MOSTRAR_BOOL_VALOR
    
MOSTRAR_FALSE:
    LEA DX, valor_false
    
MOSTRAR_BOOL_VALOR:
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
    ; Mostrar el valor booleano original
    CALL NUEVA_LINEA
    MOV AH, 09h
    LEA DX, prompt_bool
    INT 21h
    
    ; Mostrar "TRUE" o "FALSE"
    CMP BYTE PTR [bool_valor1], 0
    JE @MOSTRAR_ORIG_FALSE
    
    LEA DX, valor_true
    JMP @MOSTRAR_ORIG_VALOR
    
@MOSTRAR_ORIG_FALSE:
    LEA DX, valor_false
    
@MOSTRAR_ORIG_VALOR:
    MOV AH, 09h
    INT 21h
    
    ; Mostrar conversión a entero
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
    
    ; Mostrar conversión a carácter
    CALL NUEVA_LINEA
    MOV AH, 09h
    LEA DX, prompt_char
    INT 21h
    
    MOV DL, [char_result]
    MOV AH, 02h
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
    JNE @ENTERO_NO_CERO
    
    MOV DL, '0'
    MOV AH, 02h
    INT 21h
    JMP @FIN_MOSTRAR_NUMERO
    
@ENTERO_NO_CERO:
    ; Verificar si es negativo
    TEST AX, 8000h
    JZ @ENTERO_POSITIVO
    
    PUSH AX
    MOV DL, '-'
    MOV AH, 02h
    INT 21h
    POP AX
    NEG AX
    
@ENTERO_POSITIVO:
    ; Convertir a dígitos y mostrar
    MOV BX, 10
    XOR CX, CX
    
@DIV_LOOP:
    XOR DX, DX
    DIV BX
    PUSH DX
    INC CX
    
    CMP AX, 0
    JNE @DIV_LOOP
    
@MOSTRAR_DIGITOS:
    POP DX
    ADD DL, '0'
    MOV AH, 02h
    INT 21h
    LOOP @MOSTRAR_DIGITOS
    
@FIN_MOSTRAR_NUMERO:
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
    
    ; Mostrar parte decimal (siempre 0 en este caso)
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