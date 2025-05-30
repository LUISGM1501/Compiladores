; ********************************************
; * Programa: SELECTED.ASM  (GHAST)         *
; * Descripcion: Operaciones sobre flotantes*
; * Autores: Luis Urbina, Samir Cabrera     *
; * Fecha: 10/05/2025                       *
; * Version: 1.0                            *
; * Curso: Compiladores e Interpretes       *
; * Proyecto: Notch Engine - Etapa 2        *
; ********************************************

DATOS SEGMENT
    ; Mensajes de entrada y salida
    titulo       DB "DEMOSTRACION DE OPERACIONES CON GHAST (FLOTANTES)", 0Dh, 0Ah, '$'
    separador    DB "----------------------------------------", 0Dh, 0Ah, '$'
    
    menu         DB "MENU DE OPERACIONES:", 0Dh, 0Ah
                 DB "1. Suma flotante (:+)", 0Dh, 0Ah
                 DB "2. Resta flotante (:-)", 0Dh, 0Ah
                 DB "3. Multiplicacion flotante (:*)", 0Dh, 0Ah
                 DB "4. Division flotante (://)", 0Dh, 0Ah
                 DB "5. Modulo flotante (:%)", 0Dh, 0Ah
                 DB "6. Asignaciones (:+=, :-=, :*=, ://=, :%=)", 0Dh, 0Ah
                 DB "7. Comparaciones (<, >, <=, >=, is, isNot)", 0Dh, 0Ah
                 DB "8. Convertir a otros tipos", 0Dh, 0Ah
                 DB "0. Salir", 0Dh, 0Ah
                 DB "Seleccione una opcion: $"

    submenu_asig DB 0Dh, 0Ah, "OPERACIONES DE ASIGNACION:", 0Dh, 0Ah
                 DB "1. Suma y asigna (:+=)", 0Dh, 0Ah
                 DB "2. Resta y asigna (:-=)", 0Dh, 0Ah
                 DB "3. Multiplica y asigna (:*=)", 0Dh, 0Ah
                 DB "4. Divide y asigna (://=)", 0Dh, 0Ah
                 DB "5. Modulo y asigna (:%=)", 0Dh, 0Ah
                 DB "Seleccione: $"
    
    prompt_conversiones_orig DB "El flotante original es: $"
    prompt_conv_int     DB "Convertido a Stack (entero): $"
    prompt_conv_bool    DB "Convertido a Torch (booleano): $"
    prompt_conv_char    DB "Convertido a Rune (caracter): $"
    prompt_conv_str     DB "Convertido a Spider (string): $"
    prompt_conv_creativo DB "Convertido a creativo (probabilidad): $"

    prompt_float1 DB "Ingrese primer numero flotante: $"
    prompt_float2 DB "Ingrese segundo numero flotante: $"
    result_msg    DB "Resultado: $"
    error_div     DB "Error: Division por cero", 0Dh, 0Ah, '$'

    ; Variables para operaciones con flotantes
    buffer1      DB 15, ?, 15 DUP(?)  ; Buffer para primer flotante
    buffer2      DB 15, ?, 15 DUP(?)  ; Buffer para segundo flotante
    
    ; Variables para el primer flotante
    entero1      DW ?                  ; Parte entera del primer flotante
    decimal1     DW ?                  ; Parte decimal del primer flotante
    dec_digitos1 DB ?                  ; Dígitos decimales del primer flotante
    es_negativo1 DB 0                  ; Bandera de signo del primer flotante
    
    ; Variables para el segundo flotante
    entero2      DW ?                  ; Parte entera del segundo flotante
    decimal2     DW ?                  ; Parte decimal del segundo flotante
    dec_digitos2 DB ?                  ; Dígitos decimales del segundo flotante
    es_negativo2 DB 0                  ; Bandera de signo del segundo flotante
    
    ; Variables para el resultado
    resultado_entero   DW ?            ; Parte entera del resultado
    resultado_decimal  DW ?            ; Parte decimal del resultado
    resultado_digitos  DB ?            ; Dígitos decimales del resultado
    resultado_negativo DB 0            ; Bandera de signo del resultado
    
    ; Variables para conversiones
    int_valor    DW ?                  ; Conversión a entero (Stack)
    bool_valor   DB ?                  ; Conversión a booleano (Torch)
    char_valor   DB ?                  ; Conversión a caracter (Rune)
    string_buffer DB 50 DUP(?),'$'    ; Conversión a string (Spider)
    prob_valor   DB ?                  ; Conversión a creativo (probabilidad)
    
    ; Mensajes para comparaciones
    msg_menor    DB "MENOR QUE (<): $"
    msg_mayor    DB "MAYOR QUE (>): $"
    msg_menig    DB "MENOR O IGUAL QUE (<=): $"
    msg_mayig    DB "MAYOR O IGUAL QUE (>=): $"
    msg_igual    DB "IGUAL A (is): $"
    msg_nig      DB "DISTINTO DE (isNot): $"
    
    ; Valores para mostrar booleanos
    valor_true   DB 'TRUE$'
    valor_false  DB 'FALSE$'
    
    ; Auxiliares
    nueva_lin    DB 0Dh, 0Ah, '$'
    punto        DB '.$'
    const_diez   DW 10
    const_cien   DW 100
    const_10000  DW 10000 
DATOS ENDS

CODIGO SEGMENT
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
    JNE @SELECTED_NOT1
    JMP OPCION_SUMA
@SELECTED_NOT1:
    CMP AL, '2'
    JNE @SELECTED_NOT2
    JMP OPCION_RESTA
@SELECTED_NOT2:
    CMP AL, '3'
    JNE @SELECTED_NOT3
    JMP OPCION_MULTIPLICACION
@SELECTED_NOT3:
    CMP AL, '4'
    JNE @SELECTED_NOT4
    JMP OPCION_DIVISION
@SELECTED_NOT4:
    CMP AL, '5'
    JNE @SELECTED_NOT5
    JMP OPCION_MODULO
@SELECTED_NOT5:
    CMP AL, '6'
    JNE @SELECTED_NOT6
    JMP OPCION_ASIGNACIONES
@SELECTED_NOT6:
    CMP AL, '7'
    JNE @SELECTED_NOT7
    JMP OPCION_COMPARACIONES
@SELECTED_NOT7:
    CMP AL, '8'
    JNE @SELECTED_NOT8
    JMP OPCION_CONVERSIONES
@SELECTED_NOT8:
    CMP AL, '0'
    JNE @SELECTED_NOT0
    JMP SALIR
@SELECTED_NOT0:
    
    ; Si llegamos aquí, la opción no es válida, volver al menú
    JMP MENU_PRINCIPAL

OPCION_SUMA:
    CALL NUEVA_LINEA
    CALL LEER_DOS_FLOTANTES
    
    ; Realizar la suma flotante (:+)
    CALL SUMAR_FLOTANTES
    
    ; Mostrar resultado
    CALL MOSTRAR_RESULTADO_FLOTANTE
    JMP MENU_PRINCIPAL

OPCION_RESTA:
    CALL NUEVA_LINEA
    CALL LEER_DOS_FLOTANTES
    
    ; Realizar la resta flotante (:-)
    CALL RESTAR_FLOTANTES
    
    ; Mostrar resultado
    CALL MOSTRAR_RESULTADO_FLOTANTE
    JMP MENU_PRINCIPAL

OPCION_MULTIPLICACION:
    CALL NUEVA_LINEA
    CALL LEER_DOS_FLOTANTES
    
    ; Realizar la multiplicación flotante (:*)
    CALL MULTIPLICAR_FLOTANTES
    
    ; Mostrar resultado
    CALL MOSTRAR_RESULTADO_FLOTANTE
    JMP MENU_PRINCIPAL

OPCION_DIVISION:
    CALL NUEVA_LINEA
    CALL LEER_DOS_FLOTANTES
    
    ; Verificar división por cero
    CALL VERIFICAR_CERO_SEGUNDO
    JC @SELECTED_ERROR_DIV
    
    ; Realizar la división flotante (://)
    CALL DIVIDIR_FLOTANTES
    
    ; Mostrar resultado
    CALL MOSTRAR_RESULTADO_FLOTANTE
    JMP MENU_PRINCIPAL

@SELECTED_ERROR_DIV:
    MOV AH, 09h
    LEA DX, error_div
    INT 21h
    JMP MENU_PRINCIPAL

OPCION_MODULO:
    CALL NUEVA_LINEA
    CALL LEER_DOS_FLOTANTES
    
    ; Verificar división por cero
    CALL VERIFICAR_CERO_SEGUNDO
    JC @SELECTED_ERROR_MOD
    
    ; Realizar el módulo flotante (:%)
    CALL MODULO_FLOTANTES
    
    ; Mostrar resultado
    CALL MOSTRAR_RESULTADO_FLOTANTE
    JMP MENU_PRINCIPAL

@SELECTED_ERROR_MOD:
    MOV AH, 09h
    LEA DX, error_div
    INT 21h
    JMP MENU_PRINCIPAL

OPCION_ASIGNACIONES:
    CALL NUEVA_LINEA
    
    ; Submenu para operaciones de asignación
    MOV AH, 09h
    LEA DX, submenu_asig
    INT 21h
    
    ; Leer subopción
    MOV AH, 01h
    INT 21h
    
    CMP AL, '1'
    JNE @SELECTED_ASIG_NOT1
    JMP ASIGNACION_SUMA
@SELECTED_ASIG_NOT1:
    CMP AL, '2'
    JNE @SELECTED_ASIG_NOT2
    JMP ASIGNACION_RESTA
@SELECTED_ASIG_NOT2:
    CMP AL, '3'
    JNE @SELECTED_ASIG_NOT3
    JMP ASIGNACION_MULT
@SELECTED_ASIG_NOT3:
    CMP AL, '4'
    JNE @SELECTED_ASIG_NOT4
    JMP ASIGNACION_DIV
@SELECTED_ASIG_NOT4:
    CMP AL, '5'
    JNE @SELECTED_ASIG_VOLVER
    JMP ASIGNACION_MOD
@SELECTED_ASIG_VOLVER:
    JMP MENU_PRINCIPAL

ASIGNACION_SUMA:
    ; Implementar A :+= B (equivale a A = A :+ B)
    CALL NUEVA_LINEA
    CALL LEER_DOS_FLOTANTES
    CALL SUMAR_FLOTANTES
    CALL MOSTRAR_RESULTADO_FLOTANTE
    JMP MENU_PRINCIPAL

ASIGNACION_RESTA:
    ; Implementar A :-= B (equivale a A = A :- B)
    CALL NUEVA_LINEA
    CALL LEER_DOS_FLOTANTES
    CALL RESTAR_FLOTANTES
    CALL MOSTRAR_RESULTADO_FLOTANTE
    JMP MENU_PRINCIPAL

ASIGNACION_MULT:
    ; Implementar A :*= B (equivale a A = A :* B)
    CALL NUEVA_LINEA
    CALL LEER_DOS_FLOTANTES
    CALL MULTIPLICAR_FLOTANTES
    CALL MOSTRAR_RESULTADO_FLOTANTE
    JMP MENU_PRINCIPAL

ASIGNACION_DIV:
    ; Implementar A ://= B (equivale a A = A :// B)
    CALL NUEVA_LINEA
    CALL LEER_DOS_FLOTANTES
    CALL VERIFICAR_CERO_SEGUNDO
    JC @SELECTED_ASIG_ERROR_DIV
    CALL DIVIDIR_FLOTANTES
    CALL MOSTRAR_RESULTADO_FLOTANTE
    JMP MENU_PRINCIPAL

@SELECTED_ASIG_ERROR_DIV:
    MOV AH, 09h
    LEA DX, error_div
    INT 21h
    JMP MENU_PRINCIPAL

ASIGNACION_MOD:
    ; Implementar A :%= B (equivale a A = A :% B)
    CALL NUEVA_LINEA
    CALL LEER_DOS_FLOTANTES
    CALL VERIFICAR_CERO_SEGUNDO
    JC @SELECTED_ASIG_ERROR_MOD
    CALL MODULO_FLOTANTES
    CALL MOSTRAR_RESULTADO_FLOTANTE
    JMP MENU_PRINCIPAL

@SELECTED_ASIG_ERROR_MOD:
    MOV AH, 09h
    LEA DX, error_div
    INT 21h
    JMP MENU_PRINCIPAL

OPCION_COMPARACIONES:
    CALL NUEVA_LINEA
    CALL LEER_DOS_FLOTANTES
    
    ; Comparar MENOR QUE (<)
    MOV AH, 09h
    LEA DX, msg_menor
    INT 21h
    
    CALL COMPARAR_FLOTANTES_MENOR
    MOV AH, 09h
    JZ @SELECTED_COMP_MENOR_TRUE
    LEA DX, valor_false
    JMP @SELECTED_SHOW_MENOR
@SELECTED_COMP_MENOR_TRUE:
    LEA DX, valor_true
@SELECTED_SHOW_MENOR:
    INT 21h
    
    ; Comparar MAYOR QUE (>)
    MOV AH, 09h
    LEA DX, msg_mayor
    INT 21h
    
    CALL COMPARAR_FLOTANTES_MAYOR
    MOV AH, 09h
    JZ @SELECTED_COMP_MAYOR_TRUE
    LEA DX, valor_false
    JMP @SELECTED_SHOW_MAYOR
@SELECTED_COMP_MAYOR_TRUE:
    LEA DX, valor_true
@SELECTED_SHOW_MAYOR:
    INT 21h
    
    ; Comparar MENOR O IGUAL QUE (<=)
    MOV AH, 09h
    LEA DX, msg_menig
    INT 21h
    
    CALL COMPARAR_FLOTANTES_MENOR_IGUAL
    MOV AH, 09h
    JZ @SELECTED_COMP_MENIG_TRUE
    LEA DX, valor_false
    JMP @SELECTED_SHOW_MENIG
@SELECTED_COMP_MENIG_TRUE:
    LEA DX, valor_true
@SELECTED_SHOW_MENIG:
    INT 21h
    
    ; Comparar MAYOR O IGUAL QUE (>=)
    MOV AH, 09h
    LEA DX, msg_mayig
    INT 21h
    
    CALL COMPARAR_FLOTANTES_MAYOR_IGUAL
    MOV AH, 09h
    JZ @SELECTED_COMP_MAYIG_TRUE
    LEA DX, valor_false
    JMP @SELECTED_SHOW_MAYIG
@SELECTED_COMP_MAYIG_TRUE:
    LEA DX, valor_true
@SELECTED_SHOW_MAYIG:
    INT 21h
    
    ; Comparar IGUAL A (is)
    MOV AH, 09h
    LEA DX, msg_igual
    INT 21h
    
    CALL COMPARAR_FLOTANTES_IGUAL
    MOV AH, 09h
    JZ @SELECTED_COMP_IGUAL_TRUE
    LEA DX, valor_false
    JMP @SELECTED_SHOW_IGUAL
@SELECTED_COMP_IGUAL_TRUE:
    LEA DX, valor_true
@SELECTED_SHOW_IGUAL:
    INT 21h
    
    ; Comparar DISTINTO DE (isNot)
    MOV AH, 09h
    LEA DX, msg_nig
    INT 21h
    
    CALL COMPARAR_FLOTANTES_DISTINTO
    MOV AH, 09h
    JZ @SELECTED_COMP_DISTINTO_TRUE
    LEA DX, valor_false
    JMP @SELECTED_SHOW_DISTINTO
@SELECTED_COMP_DISTINTO_TRUE:
    LEA DX, valor_true
@SELECTED_SHOW_DISTINTO:
    INT 21h
    
    CALL NUEVA_LINEA
    JMP MENU_PRINCIPAL

OPCION_CONVERSIONES:
    CALL NUEVA_LINEA
    
    ; Leer un flotante para convertir
    MOV AH, 09h
    LEA DX, prompt_float1
    INT 21h
    
    MOV AH, 0Ah
    LEA DX, buffer1
    INT 21h
    
    ; Procesar el flotante
    CALL PROCESAR_PRIMER_FLOTANTE
    
    ; Realizar todas las conversiones
    CALL FLOAT_A_INTEGER    ; A Stack (entero)
    CALL FLOAT_A_BOOLEAN    ; A Torch (booleano)
    CALL FLOAT_A_CHAR       ; A Rune (caracter)
    CALL FLOAT_A_STRING     ; A Spider (string)
    CALL FLOAT_A_CREATIVO   ; A tipo creativo
    
    ; Mostrar todas las conversiones
    CALL MOSTRAR_CONVERSIONES
    
    JMP MENU_PRINCIPAL

SALIR:
    ; Terminamos el programa y regresamos al sistema operativo
    MOV AX, 4C00h
    INT 21h

;------------------------------------------------------------
; Procedimiento: LEER_DOS_FLOTANTES
; Lee dos números flotantes desde la entrada estándar
;------------------------------------------------------------
LEER_DOS_FLOTANTES PROC
    ; Leer primer flotante
    MOV AH, 09h
    LEA DX, prompt_float1
    INT 21h
    
    MOV AH, 0Ah
    LEA DX, buffer1
    INT 21h
    
    ; Procesar primer flotante
    CALL PROCESAR_PRIMER_FLOTANTE
    
    CALL NUEVA_LINEA
    
    ; Leer segundo flotante
    MOV AH, 09h
    LEA DX, prompt_float2
    INT 21h
    
    MOV AH, 0Ah
    LEA DX, buffer2
    INT 21h
    
    ; Procesar segundo flotante
    CALL PROCESAR_SEGUNDO_FLOTANTE
    
    CALL NUEVA_LINEA
    
    RET
LEER_DOS_FLOTANTES ENDP

;------------------------------------------------------------
; Procedimiento: PROCESAR_PRIMER_FLOTANTE
; Procesa el primer flotante del buffer1
;------------------------------------------------------------
PROCESAR_PRIMER_FLOTANTE PROC
    PUSH AX
    PUSH BX
    PUSH CX
    PUSH DX
    PUSH SI
    
    ; Inicializar variables del primer flotante
    MOV [entero1], 0
    MOV [decimal1], 0
    MOV [dec_digitos1], 0
    MOV [es_negativo1], 0
    
    ; Obtener longitud y puntero
    MOV BL, [buffer1+1]
    XOR BH, BH
    LEA SI, [buffer1+2]
    
    ; Verificar si está vacío
    CMP BX, 0
    JE @SELECTED_PROC1_FIN
    
    ; Verificar signo negativo
    MOV CL, [SI]
    CMP CL, '-'
    JNE @SELECTED_PROC1_ENTERO
    
    MOV [es_negativo1], 1
    INC SI
    DEC BX
    
@SELECTED_PROC1_ENTERO:
    CMP BX, 0
    JE @SELECTED_PROC1_FIN
    
    MOV CL, [SI]
    INC SI
    DEC BX
    
    CMP CL, '.'
    JE @SELECTED_PROC1_DECIMAL
    
    ; Verificar si es dígito
    CMP CL, '0'
    JL @SELECTED_PROC1_ENTERO
    CMP CL, '9'
    JG @SELECTED_PROC1_ENTERO
    
    SUB CL, '0'
    XOR CH, CH
    
    ; entero1 = entero1 * 10 + dígito
    MOV AX, [entero1]
    MOV DX, 10
    MUL DX
    ADD AX, CX
    MOV [entero1], AX
    
    JMP @SELECTED_PROC1_ENTERO
    
@SELECTED_PROC1_DECIMAL:
    CMP BX, 0
    JE @SELECTED_PROC1_FIN
    
    MOV CL, [SI]
    INC SI
    DEC BX
    
    ; Verificar si es dígito
    CMP CL, '0'
    JL @SELECTED_PROC1_DECIMAL
    CMP CL, '9'
    JG @SELECTED_PROC1_DECIMAL
    
    SUB CL, '0'
    XOR CH, CH
    
    ; decimal1 = decimal1 * 10 + dígito
    MOV AX, [decimal1]
    MOV DX, 10
    MUL DX
    ADD AX, CX
    MOV [decimal1], AX
    
    ; Incrementar contador de dígitos decimales
    INC [dec_digitos1]
    
    JMP @SELECTED_PROC1_DECIMAL
    
@SELECTED_PROC1_FIN:
    POP SI
    POP DX
    POP CX
    POP BX
    POP AX
    RET
PROCESAR_PRIMER_FLOTANTE ENDP

;------------------------------------------------------------
; Procedimiento: PROCESAR_SEGUNDO_FLOTANTE
; Procesa el segundo flotante del buffer2 (similar al primero)
;------------------------------------------------------------
PROCESAR_SEGUNDO_FLOTANTE PROC
    PUSH AX
    PUSH BX
    PUSH CX
    PUSH DX
    PUSH SI
    
    ; Inicializar variables del segundo flotante
    MOV [entero2], 0
    MOV [decimal2], 0
    MOV [dec_digitos2], 0
    MOV [es_negativo2], 0
    
    ; Obtener longitud y puntero
    MOV BL, [buffer2+1]
    XOR BH, BH
    LEA SI, [buffer2+2]
    
    ; Verificar si está vacío
    CMP BX, 0
    JE @SELECTED_PROC2_FIN
    
    ; Verificar signo negativo
    MOV CL, [SI]
    CMP CL, '-'
    JNE @SELECTED_PROC2_ENTERO
    
    MOV [es_negativo2], 1
    INC SI
    DEC BX
    
@SELECTED_PROC2_ENTERO:
    CMP BX, 0
    JE @SELECTED_PROC2_FIN
    
    MOV CL, [SI]
    INC SI
    DEC BX
    
    CMP CL, '.'
    JE @SELECTED_PROC2_DECIMAL
    
    ; Verificar si es dígito
    CMP CL, '0'
    JL @SELECTED_PROC2_ENTERO
    CMP CL, '9'
    JG @SELECTED_PROC2_ENTERO
    
    SUB CL, '0'
    XOR CH, CH
    
    ; entero2 = entero2 * 10 + dígito
    MOV AX, [entero2]
    MOV DX, 10
    MUL DX
    ADD AX, CX
    MOV [entero2], AX
    
    JMP @SELECTED_PROC2_ENTERO
    
@SELECTED_PROC2_DECIMAL:
    CMP BX, 0
    JE @SELECTED_PROC2_FIN
    
    MOV CL, [SI]
    INC SI
    DEC BX
    
    ; Verificar si es dígito
    CMP CL, '0'
    JL @SELECTED_PROC2_DECIMAL
    CMP CL, '9'
    JG @SELECTED_PROC2_DECIMAL
    
    SUB CL, '0'
    XOR CH, CH
    
    ; decimal2 = decimal2 * 10 + dígito
    MOV AX, [decimal2]
    MOV DX, 10
    MUL DX
    ADD AX, CX
    MOV [decimal2], AX
    
    ; Incrementar contador de dígitos decimales
    INC [dec_digitos2]
    
    JMP @SELECTED_PROC2_DECIMAL
    
@SELECTED_PROC2_FIN:
    POP SI
    POP DX
    POP CX
    POP BX
    POP AX
    RET
PROCESAR_SEGUNDO_FLOTANTE ENDP

;------------------------------------------------------------
; Procedimiento: SUMAR_FLOTANTES  
; Realiza la suma de dos flotantes (:+)
;------------------------------------------------------------
SUMAR_FLOTANTES PROC
    PUSH AX
    PUSH BX
    PUSH CX
    PUSH DX
    
    ; Normalizar decimales para operación
    CALL NORMALIZAR_DECIMALES_PARA_OPERACION
    
    ; Determinar el tipo de operación según los signos
    MOV AL, [es_negativo1]
    MOV BL, [es_negativo2]
    
    CMP AL, 0
    JNE @SUMA_PRIMER_NEGATIVO
    
    ; Primer número es positivo
    CMP BL, 0
    JE @SUMA_AMBOS_POSITIVOS
    JMP @SUMA_POS_MAS_NEG      ; Positivo + Negativo
    
@SUMA_PRIMER_NEGATIVO:
    ; Primer número es negativo
    CMP BL, 0
    JE @SUMA_NEG_MAS_POS       ; Negativo + Positivo  
    JMP @SUMA_AMBOS_NEGATIVOS  ; Negativo + Negativo
    
@SUMA_AMBOS_POSITIVOS:
    ; A + B (ambos positivos)
    CALL SUMAR_VALORES_ABSOLUTOS
    MOV [resultado_negativo], 0
    JMP @SUMA_FIN
    
@SUMA_AMBOS_NEGATIVOS:
    ; (-A) + (-B) = -(A + B)
    CALL SUMAR_VALORES_ABSOLUTOS
    MOV [resultado_negativo], 1
    JMP @SUMA_FIN
    
@SUMA_POS_MAS_NEG:
    ; A + (-B) = A - B
    CALL RESTAR_VALORES_ABSOLUTOS_SUMA
    JMP @SUMA_FIN
    
@SUMA_NEG_MAS_POS:
    ; (-A) + B = B - A
    CALL RESTAR_SEGUNDO_MENOS_PRIMERO
    JMP @SUMA_FIN
    
@SUMA_FIN:
    POP DX
    POP CX
    POP BX
    POP AX
    RET
SUMAR_FLOTANTES ENDP

;------------------------------------------------------------
; Procedimiento: RESTAR_SEGUNDO_MENOS_PRIMERO
; Resta el segundo número del primero, considerando los signos
;------------------------------------------------------------

;------------------------------------------------------------
; Procedimiento: RESTAR_SEGUNDO_MENOS_PRIMERO  
; Maneja (-A) + B = B - A cuando signos son diferentes
;------------------------------------------------------------
RESTAR_SEGUNDO_MENOS_PRIMERO PROC
    PUSH AX
    PUSH BX
    PUSH CX
    PUSH DX
    
    ; Obtener valores absolutos para comparación
    MOV AX, [entero1]
    CMP [es_negativo1], 0
    JE @RSMP_ENT1_YA_ABS
    CMP AX, 0
    JGE @RSMP_ENT1_YA_ABS
    NEG AX
@RSMP_ENT1_YA_ABS:
    MOV BX, AX              ; BX = |entero1|
    
    MOV AX, [entero2]
    CMP [es_negativo2], 0
    JE @RSMP_ENT2_YA_ABS
    CMP AX, 0
    JGE @RSMP_ENT2_YA_ABS
    NEG AX
@RSMP_ENT2_YA_ABS:
    MOV CX, AX              ; CX = |entero2|
    
    ; Comparar magnitudes: ¿|val2| >= |val1|?
    CMP CX, BX
    JG @RSMP_SEGUNDO_MAYOR
    JL @RSMP_PRIMERO_MAYOR
    
    ; Partes enteras iguales, comparar decimales
    MOV AX, [decimal2]
    MOV DX, [decimal1]
    CMP AX, DX
    JGE @RSMP_SEGUNDO_MAYOR
    
@RSMP_PRIMERO_MAYOR:
    ; |primero| > |segundo|: resultado = |primero| - |segundo|
    ; Pero como es (-A) + B, el signo es el opuesto del primero
    
    MOV AX, BX              ; AX = |entero1|
    SUB AX, CX              ; AX = |entero1| - |entero2|
    MOV [resultado_entero], AX
    
    MOV AX, [decimal1]
    SUB AX, [decimal2]
    
    CMP AX, 0
    JGE @RSMP_DEC1_OK
    
    DEC WORD PTR [resultado_entero]
    MOV BL, [resultado_digitos]
    CALL CALCULAR_POTENCIA_10_BL
    ADD AX, BX
    
@RSMP_DEC1_OK:
    MOV [resultado_decimal], AX
    
    ; Signo opuesto al primer número (porque era negativo en la suma)
    MOV AL, [es_negativo1]
    MOV [resultado_negativo], AL
    JMP @RSMP_FIN
    
@RSMP_SEGUNDO_MAYOR:
    ; |segundo| >= |primero|: resultado = |segundo| - |primero|
    ; Signo del segundo número
    
    MOV AX, CX              ; AX = |entero2|
    SUB AX, BX              ; AX = |entero2| - |entero1|
    MOV [resultado_entero], AX
    
    MOV AX, [decimal2]
    SUB AX, [decimal1]
    
    CMP AX, 0
    JGE @RSMP_DEC2_OK
    
    DEC WORD PTR [resultado_entero]
    MOV BL, [resultado_digitos]
    CALL CALCULAR_POTENCIA_10_BL
    ADD AX, BX
    
@RSMP_DEC2_OK:
    MOV [resultado_decimal], AX
    
    ; Signo del segundo número
    MOV AL, [es_negativo2]
    MOV [resultado_negativo], AL
    
@RSMP_FIN:
    POP DX
    POP CX
    POP BX
    POP AX
    RET
RESTAR_SEGUNDO_MENOS_PRIMERO ENDP
;------------------------------------------------------------
; Procedimiento: RESTAR_VALORES_ABSOLUTOS_SUMA
; Resta valores absolutos cuando los signos son diferentes en suma
;------------------------------------------------------------
;------------------------------------------------------------
; Procedimiento: RESTAR_VALORES_ABSOLUTOS_SUMA
; Maneja A + (-B) = A - B cuando signos son diferentes
;------------------------------------------------------------
RESTAR_VALORES_ABSOLUTOS_SUMA PROC
    PUSH AX
    PUSH BX
    PUSH CX
    PUSH DX
    
    ; Obtener valores absolutos para comparación
    MOV AX, [entero1]
    CMP [es_negativo1], 0
    JE @RVAS_ENT1_YA_ABS
    CMP AX, 0
    JGE @RVAS_ENT1_YA_ABS
    NEG AX
@RVAS_ENT1_YA_ABS:
    MOV BX, AX              ; BX = |entero1|
    
    MOV AX, [entero2] 
    CMP [es_negativo2], 0
    JE @RVAS_ENT2_YA_ABS
    CMP AX, 0
    JGE @RVAS_ENT2_YA_ABS
    NEG AX
@RVAS_ENT2_YA_ABS:
    MOV CX, AX              ; CX = |entero2|
    
    ; Comparar magnitudes: ¿|val1| >= |val2|?
    CMP BX, CX
    JG @RVAS_PRIMERO_MAYOR
    JL @RVAS_SEGUNDO_MAYOR
    
    ; Partes enteras iguales, comparar decimales
    MOV AX, [decimal1]
    MOV DX, [decimal2]
    CMP AX, DX
    JGE @RVAS_PRIMERO_MAYOR
    
@RVAS_SEGUNDO_MAYOR:
    ; |segundo| > |primero|: resultado = |segundo| - |primero|
    ; Signo del resultado = signo del número con mayor magnitud
    
    ; Restar: |segundo| - |primero|
    MOV AX, CX              ; AX = |entero2|
    SUB AX, BX              ; AX = |entero2| - |entero1|
    MOV [resultado_entero], AX
    
    MOV AX, [decimal2]
    SUB AX, [decimal1]
    
    ; Manejar préstamo si es necesario
    CMP AX, 0
    JGE @RVAS_DEC2_OK
    
    DEC WORD PTR [resultado_entero]
    MOV BL, [resultado_digitos]
    CALL CALCULAR_POTENCIA_10_BL
    ADD AX, BX
    
@RVAS_DEC2_OK:
    MOV [resultado_decimal], AX
    
    ; El signo del resultado es el signo del segundo número
    MOV AL, [es_negativo2]
    MOV [resultado_negativo], AL
    JMP @RVAS_FIN
    
@RVAS_PRIMERO_MAYOR:
    ; |primero| >= |segundo|: resultado = |primero| - |segundo|
    ; Signo del resultado = signo del primer número
    
    ; Restar: |primero| - |segundo|
    MOV AX, BX              ; AX = |entero1|
    SUB AX, CX              ; AX = |entero1| - |entero2|
    MOV [resultado_entero], AX
    
    MOV AX, [decimal1]
    SUB AX, [decimal2]
    
    ; Manejar préstamo si es necesario
    CMP AX, 0
    JGE @RVAS_DEC1_OK
    
    DEC WORD PTR [resultado_entero]
    MOV BL, [resultado_digitos]
    CALL CALCULAR_POTENCIA_10_BL
    ADD AX, BX
    
@RVAS_DEC1_OK:
    MOV [resultado_decimal], AX
    
    ; El signo del resultado es el signo del primer número
    MOV AL, [es_negativo1]
    MOV [resultado_negativo], AL
    
@RVAS_FIN:
    POP DX
    POP CX
    POP BX
    POP AX
    RET
RESTAR_VALORES_ABSOLUTOS_SUMA ENDP

;------------------------------------------------------------
; Procedimiento: SUMA_DIRECTA_POSITIVOS
; Suma directa de dos números tratándolos como positivos
;------------------------------------------------------------
SUMA_DIRECTA_POSITIVOS PROC
    PUSH AX
    PUSH BX
    PUSH CX
    PUSH DX
    
    ; Sumar partes decimales
    MOV AX, [decimal1]
    ADD AX, [decimal2]
    
    ; Verificar acarreo
    XOR CX, CX  ; CX = acarreo
    MOV BL, [resultado_digitos]
    XOR BH, BH
    PUSH BX
    CALL CALCULAR_POTENCIA_10  ; AX retorna 10^digitos
    POP BX
    MOV DX, AX  ; DX = base decimal (10^digitos)
    
    MOV AX, [decimal1]
    ADD AX, [decimal2]
    
    CMP AX, DX
    JL @SELECTED_SUMA_DIR_SIN_ACARREO
    
    SUB AX, DX
    INC CX  ; Generar acarreo
    
@SELECTED_SUMA_DIR_SIN_ACARREO:
    MOV [resultado_decimal], AX
    
    ; Sumar partes enteras
    MOV AX, [entero1]
    ADD AX, [entero2]
    ADD AX, CX  ; Añadir acarreo
    MOV [resultado_entero], AX
    
    POP DX
    POP CX
    POP BX
    POP AX
    RET
SUMA_DIRECTA_POSITIVOS ENDP

;------------------------------------------------------------
; Procedimiento: RESTA_ABS_PRIMER_SEGUNDO
; Resta |primer| - |segundo| y determina signo correcto
;------------------------------------------------------------
RESTA_ABS_PRIMER_SEGUNDO PROC
    PUSH AX
    PUSH BX
    PUSH CX
    PUSH DX
    
    ; Obtener valores absolutos
    MOV AX, [entero1]
    CMP AX, 0
    JGE @SELECTED_RESTA_ABS_ENT1_POS
    NEG AX
@SELECTED_RESTA_ABS_ENT1_POS:
    MOV BX, AX  ; BX = |entero1|
    
    MOV AX, [entero2]
    CMP AX, 0
    JGE @SELECTED_RESTA_ABS_ENT2_POS
    NEG AX
@SELECTED_RESTA_ABS_ENT2_POS:
    MOV CX, AX  ; CX = |entero2|
    
    ; Comparar cuál es mayor para determinar signo
    CMP BX, CX
    JG @SELECTED_RESTA_ABS_PRIMERO_MAYOR
    JL @SELECTED_RESTA_ABS_SEGUNDO_MAYOR
    
    ; Partes enteras iguales, comparar decimales
    MOV AX, [decimal1]
    MOV DX, [decimal2]
    CMP AX, DX
    JGE @SELECTED_RESTA_ABS_PRIMERO_MAYOR
    
@SELECTED_RESTA_ABS_SEGUNDO_MAYOR:
    ; |segundo| > |primero|: resultado = |segundo| - |primero|
    ; Signo depende del signo original del segundo
    MOV AX, CX
    SUB AX, BX
    MOV [resultado_entero], AX
    
    MOV AX, [decimal2]
    SUB AX, [decimal1]
    MOV [resultado_decimal], AX
    
    ; Determinar signo: si era suma pos+neg, el resultado toma signo del mayor
    MOV AL, [es_negativo1]
    CMP AL, 0
    JE @SELECTED_RESTA_ABS_SIGNO_SEG_NEG
    ; Primer número era negativo, segundo positivo, segundo es mayor
    MOV [resultado_negativo], 0  ; Resultado positivo
    JMP @SELECTED_RESTA_ABS_FIN
    
@SELECTED_RESTA_ABS_SIGNO_SEG_NEG:
    ; Primer número era positivo, segundo negativo, segundo es mayor
    MOV [resultado_negativo], 1  ; Resultado negativo
    JMP @SELECTED_RESTA_ABS_FIN
    
@SELECTED_RESTA_ABS_PRIMERO_MAYOR:
    ; |primero| >= |segundo|: resultado = |primero| - |segundo|
    MOV AX, BX
    SUB AX, CX
    MOV [resultado_entero], AX
    
    MOV AX, [decimal1]
    SUB AX, [decimal2]
    MOV [resultado_decimal], AX
    
    ; Signo del resultado es el signo del primero
    MOV AL, [es_negativo1]
    MOV [resultado_negativo], AL
    
@SELECTED_RESTA_ABS_FIN:
    ; Manejar préstamo si decimal es negativo
    CMP WORD PTR [resultado_decimal], 0
    JGE @SELECTED_RESTA_ABS_DEC_OK
    
    ; Decimal negativo, pedir prestado de la parte entera
    DEC WORD PTR [resultado_entero]
    MOV AX, [resultado_decimal]
    ADD AX, 1000  ; Ajustar según dígitos decimales
    MOV [resultado_decimal], AX
    
@SELECTED_RESTA_ABS_DEC_OK:
    POP DX
    POP CX
    POP BX
    POP AX
    RET
RESTA_ABS_PRIMER_SEGUNDO ENDP

;------------------------------------------------------------
; Procedimiento: RESTAR_FLOTANTES  
; Realiza la resta de dos flotantes (:-)
;------------------------------------------------------------
RESTAR_FLOTANTES PROC
    PUSH AX
    PUSH BX
    
    ; A - B = A + (-B)
    ; Invertir el signo del segundo operando
    MOV AL, [es_negativo2]
    XOR AL, 1
    MOV [es_negativo2], AL
    
    ; Llamar a la suma (que ya maneja todos los casos correctamente)
    CALL SUMAR_FLOTANTES
    
    ; Restaurar el signo original del segundo operando
    MOV AL, [es_negativo2]
    XOR AL, 1
    MOV [es_negativo2], AL
    
    POP BX
    POP AX
    RET
RESTAR_FLOTANTES ENDP

;------------------------------------------------------------
; Procedimiento: RESTA_POSITIVOS_DIRECTA
; Resta A - B tratando ambos como positivos
;------------------------------------------------------------
RESTA_POSITIVOS_DIRECTA PROC
    PUSH AX
    PUSH BX
    PUSH CX
    PUSH DX
    
    ; Obtener valores absolutos para comparación
    MOV AX, [entero1]
    CMP AX, 0
    JGE @SELECTED_RPD_ENT1_ABS
    NEG AX
@SELECTED_RPD_ENT1_ABS:
    MOV BX, AX
    
    MOV AX, [entero2]
    CMP AX, 0
    JGE @SELECTED_RPD_ENT2_ABS
    NEG AX
@SELECTED_RPD_ENT2_ABS:
    MOV CX, AX
    
    ; Comparar magnitudes: ¿|A| >= |B|?
    CMP BX, CX
    JG @SELECTED_RPD_A_MAYOR
    JL @SELECTED_RPD_B_MAYOR
    
    ; Partes enteras iguales, comparar decimales
    MOV AX, [decimal1]
    CMP AX, [decimal2]
    JGE @SELECTED_RPD_A_MAYOR
    
@SELECTED_RPD_B_MAYOR:
    ; |B| > |A|: resultado = -(|B| - |A|)
    MOV AX, CX
    SUB AX, BX
    MOV [resultado_entero], AX
    
    MOV AX, [decimal2]
    SUB AX, [decimal1]
    MOV [resultado_decimal], AX
    
    ; Resultado es negativo
    MOV [resultado_negativo], 1
    JMP @SELECTED_RPD_AJUSTAR_PRESTAMO
    
@SELECTED_RPD_A_MAYOR:
    ; |A| >= |B|: resultado = |A| - |B|
    MOV AX, BX
    SUB AX, CX
    MOV [resultado_entero], AX
    
    MOV AX, [decimal1]
    SUB AX, [decimal2]
    MOV [resultado_decimal], AX
    
    ; Resultado es positivo
    MOV [resultado_negativo], 0
    
@SELECTED_RPD_AJUSTAR_PRESTAMO:
    ; Ajustar si la parte decimal es negativa
    CMP WORD PTR [resultado_decimal], 0
    JGE @SELECTED_RPD_FIN
    
    ; Pedir prestado de la parte entera
    DEC WORD PTR [resultado_entero]
    
    ; Calcular base decimal según dígitos
    MOV AL, [resultado_digitos]
    CALL CALCULAR_POTENCIA_10
    ADD [resultado_decimal], AX
    
    ; Si después del ajuste la parte entera se vuelve negativa, cambiar signo
    CMP WORD PTR [resultado_entero], 0
    JGE @SELECTED_RPD_FIN
    
    ; Cambiar signo del resultado completo
    MOV AX, [resultado_entero]
    NEG AX
    MOV [resultado_entero], AX
    
    MOV AL, [resultado_negativo]
    XOR AL, 1
    MOV [resultado_negativo], AL
    
@SELECTED_RPD_FIN:
    POP DX
    POP CX
    POP BX
    POP AX
    RET
RESTA_POSITIVOS_DIRECTA ENDP

;------------------------------------------------------------
; Procedimiento: RESTA_SEGUNDO_PRIMER
; Calcula segundo - primero (para caso (-A) - (-B) = B - A)
;------------------------------------------------------------
RESTA_SEGUNDO_PRIMER PROC
    PUSH AX
    PUSH BX
    PUSH CX
    PUSH DX
    
    ; Intercambiar temporalmente los valores
    MOV AX, [entero1]
    MOV BX, [entero2]
    MOV [entero1], BX
    MOV [entero2], AX
    
    MOV AX, [decimal1]
    MOV BX, [decimal2]
    MOV [decimal1], BX
    MOV [decimal2], AX
    
    ; Realizar resta normal
    CALL RESTA_POSITIVOS_DIRECTA
    
    ; Restaurar valores originales
    MOV AX, [entero1]
    MOV BX, [entero2]
    MOV [entero2], AX
    MOV [entero1], BX
    
    MOV AX, [decimal1]
    MOV BX, [decimal2]
    MOV [decimal2], AX
    MOV [decimal1], BX
    
    POP DX
    POP CX
    POP BX
    POP AX
    RET
RESTA_SEGUNDO_PRIMER ENDP

;------------------------------------------------------------
; Procedimiento: MULTIPLICAR_FLOTANTES  
; Realiza la multiplicación de dos flotantes (:*)
;------------------------------------------------------------
MULTIPLICAR_FLOTANTES PROC
    PUSH AX
    PUSH BX
    PUSH CX
    PUSH DX
    
    ; Determinar signo del resultado (XOR de los signos)
    MOV AL, [es_negativo1]
    MOV BL, [es_negativo2]
    XOR AL, BL
    MOV [resultado_negativo], AL
    
    ; Convertir ambos números a enteros (eliminando el punto decimal)
    ; Para el primer número
    MOV AX, [entero1]
    MOV BL, [dec_digitos1]
    CALL CONVERTIR_A_ENTERO
    MOV CX, AX  ; CX = primer número como entero
    
    ; Para el segundo número
    MOV AX, [entero2]
    MOV BL, [dec_digitos2]
    CALL CONVERTIR_A_ENTERO
    MOV BX, AX  ; BX = segundo número como entero
    
    ; Multiplicar los enteros
    MOV AX, CX
    MUL BX      ; DX:AX = AX * BX
    
    ; Calcular el factor de ajuste decimal
    MOV BL, [dec_digitos1]
    ADD BL, [dec_digitos2]
    MOV [resultado_digitos], BL
    
    ; Ajustar el resultado según los decimales
    CALL AJUSTAR_DECIMALES_MULT
    
    POP DX
    POP CX
    POP BX
    POP AX
    RET
MULTIPLICAR_FLOTANTES ENDP

;------------------------------------------------------------
; Procedimiento: CONVERTIR_A_ENTERO
; Convierte un flotante a entero (elimina punto decimal)
; Entrada: AX = parte entera, BL = dígitos decimales
; Salida: AX = número convertido
;------------------------------------------------------------
CONVERTIR_A_ENTERO PROC
    PUSH CX
    PUSH DX
    
    MOV CX, AX  ; Guardar parte entera
    
    ; Multiplicar parte entera por 10^digitos
    MOV AL, BL
    CALL CALCULAR_POTENCIA_10  ; AX = 10^digitos
    MOV BX, AX
    MOV AX, CX
    MUL BX      ; AX = entero * 10^digitos
    
    ; Sumar parte decimal (ya está ajustada)
    ADD AX, [decimal1]
    
    POP DX
    POP CX
    RET
CONVERTIR_A_ENTERO ENDP

;------------------------------------------------------------
; Procedimiento: AJUSTAR_DECIMALES_MULT
; Ajusta el resultado de la multiplicación según los decimales
;------------------------------------------------------------
AJUSTAR_DECIMALES_MULT PROC
    PUSH AX
    PUSH BX
    PUSH CX
    PUSH DX
    
    ; Calcular el factor de división (10^total_digitos)
    MOV AL, [resultado_digitos]
    CALL CALCULAR_POTENCIA_10  ; AX = 10^digitos
    
    ; Dividir el resultado por el factor
    MOV BX, AX
    MOV AX, [resultado_entero]
    XOR DX, DX
    DIV BX      ; AX = cociente, DX = resto
    
    ; El cociente es la parte entera
    MOV [resultado_entero], AX
    
    ; El resto es la parte decimal (ajustar a 4 dígitos)
    MOV AX, DX
    MOV BX, 100
    MUL BX      ; AX = resto * 100
    XOR DX, DX
    DIV WORD PTR [const_cien]  ; Ajustar a 2 decimales
    
    MOV [resultado_decimal], AX
    MOV [resultado_digitos], 2  ; Siempre mostrar 2 decimales
    
    POP DX
    POP CX
    POP BX
    POP AX
    RET
AJUSTAR_DECIMALES_MULT ENDP

;------------------------------------------------------------
; Procedimiento: NORMALIZAR_PARA_MULTIPLICACION
; Normaliza ambos números al mismo número de dígitos decimales
;------------------------------------------------------------
NORMALIZAR_PARA_MULTIPLICACION PROC
    PUSH AX
    PUSH BX
    PUSH CX
    
    ; Encontrar el máximo número de dígitos decimales
    MOV AL, [dec_digitos1]
    MOV BL, [dec_digitos2]
    CMP AL, BL
    JGE @SELECTED_NORM_MULT_MAX_ES_1
    
    ; Segundo tiene más dígitos, normalizar primero
    SUB BL, AL
    XOR BH, BH
    MOV CX, BX
    
    CMP CX, 0
    JE @SELECTED_NORM_MULT_FIN
    
@SELECTED_NORM_MULT_LOOP1:
    MOV AX, [decimal1]
    MUL WORD PTR [const_diez]
    MOV [decimal1], AX
    LOOP @SELECTED_NORM_MULT_LOOP1
    
    MOV AL, [dec_digitos2]
    MOV [dec_digitos1], AL
    JMP @SELECTED_NORM_MULT_FIN
    
@SELECTED_NORM_MULT_MAX_ES_1:
    ; Primero tiene más o igual dígitos, normalizar segundo
    SUB AL, BL
    XOR AH, AH
    MOV CX, AX
    
    CMP CX, 0
    JE @SELECTED_NORM_MULT_FIN
    
@SELECTED_NORM_MULT_LOOP2:
    MOV AX, [decimal2]
    MUL WORD PTR [const_diez]
    MOV [decimal2], AX
    LOOP @SELECTED_NORM_MULT_LOOP2
    
    MOV AL, [dec_digitos1]
    MOV [dec_digitos2], AL
    
@SELECTED_NORM_MULT_FIN:
    POP CX
    POP BX
    POP AX
    RET
NORMALIZAR_PARA_MULTIPLICACION ENDP

;------------------------------------------------------------
; Procedimiento: CALCULAR_DECIMAL_MULTIPLICACION
; Calcula la parte decimal del resultado de multiplicación
;------------------------------------------------------------
CALCULAR_DECIMAL_MULTIPLICACION PROC
    PUSH AX
    PUSH BX
    PUSH CX
    PUSH DX
    
    ; Para simplificar, usar los primeros dígitos del resto
    ; como parte decimal
    MOV [resultado_decimal], 0
    
    ; Si resultado_digitos > 0, ajustar
    CMP BYTE PTR [resultado_digitos], 0
    JE @SELECTED_CALC_DEC_MULT_FIN
    
    ; Simplificación: usar 2 dígitos decimales por defecto
    MOV [resultado_digitos], 2
    
@SELECTED_CALC_DEC_MULT_FIN:
    POP DX
    POP CX
    POP BX
    POP AX
    RET
CALCULAR_DECIMAL_MULTIPLICACION ENDP

;------------------------------------------------------------
; Procedimiento: SUMAR_PARTES_POSITIVAS
; Suma las partes de dos números positivos
;------------------------------------------------------------
SUMAR_PARTES_POSITIVAS PROC
    PUSH AX
    PUSH BX
    PUSH CX
    PUSH DX
    
    ; Sumar partes decimales
    MOV AX, [decimal1]
    ADD AX, [decimal2]
    MOV BX, AX
    
    ; Verificar acarreo en parte decimal
    XOR CX, CX  ; CX = acarreo
    
    ; Calcular la potencia de 10 según los dígitos decimales
    MOV AL, [resultado_digitos]
    CALL CALCULAR_POTENCIA_10
    ; AX contiene 10^digitos
    
    CMP BX, AX
    JL @SELECTED_SUMA_SIN_ACARREO
    
    SUB BX, AX  ; Restar la base para mantener en rango
    INC CX      ; Generar acarreo
    
@SELECTED_SUMA_SIN_ACARREO:
    MOV [resultado_decimal], BX
    
    ; Sumar partes enteras + acarreo
    MOV AX, [entero1]
    ADD AX, [entero2]
    ADD AX, CX
    MOV [resultado_entero], AX
    
    POP DX
    POP CX
    POP BX
    POP AX
    RET
SUMAR_PARTES_POSITIVAS ENDP

;------------------------------------------------------------
; Procedimiento: DIVIDIR_FLOTANTES  
; Realiza la división de dos flotantes (://)
;------------------------------------------------------------
DIVIDIR_FLOTANTES PROC
    PUSH AX
    PUSH BX
    PUSH CX
    PUSH DX
    
    ; Determinar signo del resultado
    MOV AL, [es_negativo1]
    MOV BL, [es_negativo2]
    XOR AL, BL
    MOV [resultado_negativo], AL
    
    ; Convertir dividendo a entero extendido (multiplicar por 10000)
    MOV AX, [entero1]
    MOV BX, 10000
    MUL BX              ; DX:AX = AX * 10000
    
    ; Agregar parte decimal ajustada
    MOV BX, [decimal1]
    MOV CL, [dec_digitos1]
    
    ; Ajustar decimal1 según sus dígitos
@DIV_AJUSTE_DEC1:
    CMP CL, 4
    JGE @DIV_DEC1_OK
    MOV DX, 10
    MUL DX              ; AX = AX * 10
    INC CL
    JMP @DIV_AJUSTE_DEC1
    
@DIV_DEC1_OK:
    ADD AX, BX          ; AX = dividendo completo
    
    ; Preparar divisor
    MOV BX, [entero2]
    MOV CL, [dec_digitos2]
    
    ; Convertir divisor a entero extendido
    MOV DX, 10000
    MOV AX, BX
    MUL DX              ; DX:AX = AX * 10000
    
    ; Ajustar según decimales
@DIV_AJUSTE_DEC2:
    CMP CL, 4
    JGE @DIV_DEC2_OK
    MOV DX, 10
    MUL DX              ; AX = AX * 10
    INC CL
    JMP @DIV_AJUSTE_DEC2
    
@DIV_DEC2_OK:
    ADD AX, [decimal2]  ; AX = divisor completo
    
    ; Realizar división: DX:AX / BX
    MOV BX, AX          ; BX = divisor
    MOV AX, [entero1]   ; AX = dividendo bajo
    MOV DX, [entero1+2] ; DX = dividendo alto (si es necesario)
    
    DIV BX              ; AX = cociente, DX = resto
    
    ; Separar resultado en entero y decimal
    MOV [resultado_entero], AX
    
    ; Calcular parte decimal: (resto * 10000) / divisor
    MOV AX, DX
    MOV BX, 10000
    MUL BX              ; DX:AX = resto * 10000
    DIV WORD PTR [entero2] ; AX = parte decimal
    
    MOV [resultado_decimal], AX
    MOV [resultado_digitos], 4  ; Precisión de 4 decimales
    
    POP DX
    POP CX
    POP BX
    POP AX
    RET
DIVIDIR_FLOTANTES ENDP

;------------------------------------------------------------
; Procedimiento: RESTAR_VALORES_ABSOLUTOS
; Resta valores absolutos para determinar signo correcto
;------------------------------------------------------------
RESTAR_VALORES_ABSOLUTOS PROC
    PUSH AX
    PUSH BX
    PUSH CX
    PUSH DX
    
    ; Obtener valores absolutos
    MOV AX, [entero1]
    CMP [es_negativo1], 0
    JE @RESTA_ABS_ENT1_POS
    NEG AX
@RESTA_ABS_ENT1_POS:
    MOV BX, AX  ; BX = |entero1|
    
    MOV AX, [entero2]
    CMP [es_negativo2], 0
    JE @RESTA_ABS_ENT2_POS
    NEG AX
@RESTA_ABS_ENT2_POS:
    MOV CX, AX  ; CX = |entero2|
    
    ; Comparar magnitudes para determinar signo
    CMP BX, CX
    JG @RESTA_ABS_PRIMERO_MAYOR
    JL @RESTA_ABS_SEGUNDO_MAYOR
    
    ; Partes enteras iguales, comparar decimales
    MOV AX, [decimal1]
    CMP AX, [decimal2]
    JGE @RESTA_ABS_PRIMERO_MAYOR
    
@RESTA_ABS_SEGUNDO_MAYOR:
    ; |segundo| > |primero|: resultado = |segundo| - |primero|
    MOV AX, CX
    SUB AX, BX
    MOV [resultado_entero], AX
    
    MOV AX, [decimal2]
    SUB AX, [decimal1]
    MOV [resultado_decimal], AX
    
    ; Signo: toma el signo del número con mayor valor absoluto
    MOV AL, [es_negativo2]
    MOV [resultado_negativo], AL
    JMP @RESTA_ABS_FIN
    
@RESTA_ABS_PRIMERO_MAYOR:
    ; |primero| >= |segundo|: resultado = |primero| - |segundo|
    MOV AX, BX
    SUB AX, CX
    MOV [resultado_entero], AX
    
    MOV AX, [decimal1]
    SUB AX, [decimal2]
    MOV [resultado_decimal], AX
    
    ; Signo: toma el signo del primer número
    MOV AL, [es_negativo1]
    MOV [resultado_negativo], AL
    
@RESTA_ABS_FIN:
    ; Manejar préstamo si decimal es negativo
    CMP WORD PTR [resultado_decimal], 0
    JGE @RESTA_ABS_DEC_OK
    
    ; Decimal negativo, pedir prestado de la parte entera
    DEC WORD PTR [resultado_entero]
    
    ; Calcular base decimal
    MOV BL, [resultado_digitos]
    CALL CALCULAR_POTENCIA_10_BL
    ADD [resultado_decimal], BX
    
@RESTA_ABS_DEC_OK:
    POP DX
    POP CX
    POP BX
    POP AX
    RET
RESTAR_VALORES_ABSOLUTOS ENDP

;------------------------------------------------------------
; Procedimiento: NORMALIZAR_DECIMALES_PARA_OPERACION
; Normaliza ambos decimales al mayor número de dígitos
;------------------------------------------------------------
NORMALIZAR_DECIMALES_PARA_OPERACION PROC
    PUSH AX
    PUSH BX
    PUSH CX
    PUSH DX
    
    ; Determinar el máximo número de dígitos decimales
    MOV AL, [dec_digitos1]
    MOV BL, [dec_digitos2]
    CMP AL, BL
    JAE @NORM_MAX_ES_DIG1
    MOV AL, BL
    
@NORM_MAX_ES_DIG1:
    MOV [resultado_digitos], AL
    
    ; Normalizar primer número
    MOV CL, [dec_digitos1]
    MOV CH, AL
    SUB CH, CL
    JZ @NORM_NUM2  ; Ya tiene los dígitos necesarios
    
    MOV AX, [decimal1]
    MOV BX, 10
@NORM_LOOP1:
    MUL BX
    DEC CH
    JNZ @NORM_LOOP1
    MOV [decimal1], AX
    MOV [dec_digitos1], AL
    
@NORM_NUM2:
    ; Normalizar segundo número
    MOV CL, [dec_digitos2]
    MOV CH, [resultado_digitos]
    SUB CH, CL
    JZ @NORM_FIN
    
    MOV AX, [decimal2]
    MOV BX, 10
@NORM_LOOP2:
    MUL BX
    DEC CH
    JNZ @NORM_LOOP2
    MOV [decimal2], AX
    MOV [dec_digitos2], AL
    
@NORM_FIN:
    POP DX
    POP CX
    POP BX
    POP AX
    RET
NORMALIZAR_DECIMALES_PARA_OPERACION ENDP

;------------------------------------------------------------
; Procedimiento: CALCULAR_POTENCIA_10_BL
; Calcula 10^BL y retorna en BX
;------------------------------------------------------------
CALCULAR_POTENCIA_10_BL PROC
    PUSH AX
    PUSH CX
    
    MOV BX, 1
    MOV CL, BL
    XOR CH, CH
    CMP CL, 0
    JE @POT_BL_FIN
    
@POT_BL_LOOP:
    MOV AX, BX
    MOV BX, 10
    MUL BX
    MOV BX, AX
    LOOP @POT_BL_LOOP
    
@POT_BL_FIN:
    POP CX
    POP AX
    RET
CALCULAR_POTENCIA_10_BL ENDP
;------------------------------------------------------------
; Procedimiento: MODULO_FLOTANTES
; Realiza el módulo de dos flotantes (:%)
;------------------------------------------------------------
MODULO_FLOTANTES PROC
    PUSH AX
    PUSH BX
    PUSH CX
    PUSH DX
    
    ; El módulo flotante se calcula como: A % B = A - (A // B) * B
    ; Donde // es división entera
    
    ; Primero calculamos A // B (división entera)
    CALL DIVISION_ENTERA_FLOTANTES
    ; Resultado en [resultado_entero]
    
    ; Multiplicar (A // B) * B
    MOV AX, [resultado_entero]
    MOV BX, [entero2]
    CMP [es_negativo2], 0
    JE @SELECTED_MOD_MULT_POS
    NEG BX
@SELECTED_MOD_MULT_POS:
    
    IMUL BX  ; AX = (A // B) * B
    
    ; Restar A - (A // B) * B
    MOV BX, [entero1]
    CMP [es_negativo1], 0
    JE @SELECTED_MOD_REST_POS
    NEG BX
@SELECTED_MOD_REST_POS:
    
    SUB BX, AX  ; BX = A - (A // B) * B
    
    ; El resultado es BX
    MOV [resultado_entero], BX
    MOV [resultado_decimal], 0
    MOV [resultado_digitos], 1
    MOV [resultado_negativo], 0
    
    ; Ajustar signo si es necesario
    CMP BX, 0
    JGE @SELECTED_MOD_FIN
    NEG BX
    MOV [resultado_entero], BX
    MOV [resultado_negativo], 1
    
@SELECTED_MOD_FIN:
    POP DX
    POP CX
    POP BX
    POP AX
    RET
MODULO_FLOTANTES ENDP

;------------------------------------------------------------
; Procedimiento: VERIFICAR_CERO_SEGUNDO
; Verifica si el segundo flotante es cero
; Salida: CF=1 si es cero, CF=0 si no es cero
;------------------------------------------------------------
VERIFICAR_CERO_SEGUNDO PROC
    PUSH AX
    
    ; Un flotante es cero si tanto la parte entera como decimal son 0
    CMP WORD PTR [entero2], 0
    JNE @SELECTED_NO_CERO
    CMP WORD PTR [decimal2], 0
    JNE @SELECTED_NO_CERO
    
    ; Es cero
    STC  ; Establecer Carry Flag
    JMP @SELECTED_VERIF_FIN
    
@SELECTED_NO_CERO:
    ; No es cero
    CLC  ; Limpiar Carry Flag
    
@SELECTED_VERIF_FIN:
    POP AX
    RET
VERIFICAR_CERO_SEGUNDO ENDP

;------------------------------------------------------------
; Procedimiento: NORMALIZAR_DECIMALES_SUMA
; Normaliza las partes decimales para tener el mismo número de dígitos
;------------------------------------------------------------
NORMALIZAR_DECIMALES_SUMA PROC
    PUSH AX
    PUSH BX
    PUSH CX
    PUSH DX
    
    ; Obtener número de dígitos de cada decimal
    MOV AL, [dec_digitos1]
    MOV BL, [dec_digitos2]
    
    ; Si son iguales, no hay que normalizar
    CMP AL, BL
    JE @SELECTED_NORM_FIN
    
    ; Determinar cuál tiene menos dígitos y normalizarlo
    CMP AL, BL
    JG @SELECTED_NORM_SEGUNDO  ; Primer número tiene más dígitos
    
    ; Segundo número tiene más dígitos, normalizar primero
    SUB BL, AL  ; Diferencia de dígitos
    XOR BH, BH
    MOV CX, BX  ; CX = diferencia
    
    MOV AX, [decimal1]
@SELECTED_NORM_LOOP1:
    MUL WORD PTR [const_diez]
    LOOP @SELECTED_NORM_LOOP1
    MOV [decimal1], AX
    
    ; Actualizar contador de dígitos
    MOV AL, [dec_digitos2]
    MOV [dec_digitos1], AL
    JMP @SELECTED_NORM_FIN
    
@SELECTED_NORM_SEGUNDO:
    ; Primer número tiene más dígitos, normalizar segundo
    SUB AL, BL  ; Diferencia de dígitos
    XOR AH, AH
    MOV CX, AX  ; CX = diferencia
    
    MOV AX, [decimal2]
@SELECTED_NORM_LOOP2:
    MUL WORD PTR [const_diez]
    LOOP @SELECTED_NORM_LOOP2
    MOV [decimal2], AX
    
    ; Actualizar contador de dígitos
    MOV AL, [dec_digitos1]
    MOV [dec_digitos2], AL
    
@SELECTED_NORM_FIN:
    POP DX
    POP CX
    POP BX
    POP AX
    RET
NORMALIZAR_DECIMALES_SUMA ENDP

;------------------------------------------------------------
; Procedimiento: SUMAR_VALORES_ABSOLUTOS
;------------------------------------------------------------
SUMAR_VALORES_ABSOLUTOS PROC
    PUSH AX
    PUSH BX
    PUSH CX
    PUSH DX
    
    ; Obtener valores absolutos de partes enteras
    MOV AX, [entero1]
    CMP [es_negativo1], 0
    JE @SUMA_ABS_ENT1_POS
    NEG AX
@SUMA_ABS_ENT1_POS:
    MOV BX, AX              ; BX = |entero1|
    
    MOV AX, [entero2]
    CMP [es_negativo2], 0
    JE @SUMA_ABS_ENT2_POS
    NEG AX
@SUMA_ABS_ENT2_POS:
    MOV CX, AX              ; CX = |entero2|
    
    ; Sumar partes decimales
    MOV AX, [decimal1]
    ADD AX, [decimal2]
    
    ; Calcular la base para verificar acarreo (10^resultado_digitos)
    PUSH BX                 ; Guardar |entero1|
    PUSH CX                 ; Guardar |entero2|
    
    MOV DL, [resultado_digitos]
    CALL CALCULAR_POTENCIA_10_DL
    ; BX contiene 10^digitos (base decimal)
    
    MOV DX, BX              ; DX = base decimal
    POP CX                  ; Restaurar |entero2|
    POP BX                  ; Restaurar |entero1|
    
    ; Verificar acarreo en decimales
    XOR DI, DI              ; DI = acarreo (0 inicialmente)
    CMP AX, DX
    JL @SUMA_ABS_SIN_ACARREO
    
    SUB AX, DX              ; Ajustar decimal
    MOV DI, 1               ; Hay acarreo
    
@SUMA_ABS_SIN_ACARREO:
    MOV [resultado_decimal], AX
    
    ; Sumar partes enteras + acarreo
    MOV AX, BX              ; AX = |entero1|
    ADD AX, CX              ; AX = |entero1| + |entero2|
    ADD AX, DI              ; AX = suma + acarreo
    MOV [resultado_entero], AX
    
    POP DX
    POP CX
    POP BX
    POP AX
    RET
SUMAR_VALORES_ABSOLUTOS ENDP

;------------------------------------------------------------
; Procedimiento: CALCULAR_POTENCIA_10_DL
;------------------------------------------------------------
CALCULAR_POTENCIA_10_DL PROC
    PUSH AX
    PUSH CX
    
    MOV BX, 1               ; Resultado inicial
    XOR DH, DH              ; Limpiar DH
    MOV CL, DL              ; CL = exponente
    
    CMP CL, 0
    JE @POT_DL_FIN
    
@POT_DL_LOOP:
    PUSH CX
    MOV AX, BX
    MOV CX, 10
    MUL CX                  ; AX = BX * 10
    MOV BX, AX              ; BX = resultado
    POP CX
    DEC CL
    JNZ @POT_DL_LOOP
    
@POT_DL_FIN:
    ; BX contiene 10^DL
    POP CX
    POP AX
    RET
CALCULAR_POTENCIA_10_DL ENDP

;------------------------------------------------------------
; Procedimiento: CALCULAR_POTENCIA_10
; Calcula 10^AL y devuelve el resultado en AX
; Entrada: AL = exponente
; Salida: AX = 10^AL
;------------------------------------------------------------
CALCULAR_POTENCIA_10 PROC
    PUSH BX
    PUSH CX
    
    XOR AH, AH  ; Limpiar parte alta
    MOV CX, AX  ; CX = exponente
    
    MOV AX, 1   ; Resultado inicial = 1
    
    CMP CX, 0
    JE @SELECTED_POT_FIN  ; 10^0 = 1
    
@SELECTED_POT_LOOP:
    MUL WORD PTR [const_diez]  ; AX = AX * 10
    LOOP @SELECTED_POT_LOOP
    
@SELECTED_POT_FIN:
    POP CX
    POP BX
    RET
CALCULAR_POTENCIA_10 ENDP


;------------------------------------------------------------
; Procedimiento: COMPARAR_FLOTANTES_IGUAL
; Compara si flotante1 == flotante2
; Salida: ZF=1 si son iguales, ZF=0 si son diferentes
;------------------------------------------------------------
COMPARAR_FLOTANTES_IGUAL PROC
    PUSH AX
    PUSH BX
    
    ; Comparar signos
    MOV AL, [es_negativo1]
    MOV BL, [es_negativo2]
    CMP AL, BL
    JNE @SELECTED_IGUAL_DIFERENTES
    
    ; Signos iguales, comparar valores absolutos
    CALL COMPARAR_VALORES_ABSOLUTOS_IGUAL
    JMP @SELECTED_IGUAL_FIN
    
@SELECTED_IGUAL_DIFERENTES:
    ; Signos diferentes, no son iguales
    MOV AX, 0
    CMP AX, 1  ; ZF=0 (diferentes)
    
@SELECTED_IGUAL_FIN:
    POP BX
    POP AX
    RET
COMPARAR_FLOTANTES_IGUAL ENDP

;------------------------------------------------------------
; Procedimiento: COMPARAR_FLOTANTES_DISTINTO
; Compara si flotante1 != flotante2
; Salida: ZF=0 si son diferentes, ZF=1 si son iguales
;------------------------------------------------------------
COMPARAR_FLOTANTES_DISTINTO PROC
    CALL COMPARAR_FLOTANTES_IGUAL
    
    ; Invertir el resultado
    JZ @SELECTED_DIST_ERAN_IGUALES
    
    ; Eran diferentes, devolver verdadero
    MOV AX, 1
    CMP AX, 1  ; ZF=1 (verdadero - son diferentes)
    JMP @SELECTED_DIST_FIN
    
@SELECTED_DIST_ERAN_IGUALES:
    ; Eran iguales, devolver falso
    MOV AX, 0
    CMP AX, 1  ; ZF=0 (falso - no son diferentes)
    
@SELECTED_DIST_FIN:
    RET
COMPARAR_FLOTANTES_DISTINTO ENDP

;------------------------------------------------------------
; Procedimiento: COMPARAR_FLOTANTES_MENOR  
; Compara si flotante1 < flotante2
; Salida: ZF=1 si es verdadero, ZF=0 si es falso
;------------------------------------------------------------
COMPARAR_FLOTANTES_MENOR PROC
    PUSH AX
    PUSH BX
    
    ; Normalizar decimales para comparación justa
    CALL NORMALIZAR_DECIMALES_SUMA
    
    ; Comparar signos primero
    MOV AL, [es_negativo1]
    MOV BL, [es_negativo2]
    
    CMP AL, 1
    JNE @SELECTED_COMP_MENOR_NO_NEG1
    
    ; Primer número es negativo
    CMP BL, 1
    JE @SELECTED_COMP_MENOR_AMBOS_NEG
    
    ; Negativo < Positivo = TRUE
    XOR AX, AX
    CMP AX, AX  ; ZF=1 (verdadero)
    JMP @SELECTED_COMP_MENOR_FIN
    
@SELECTED_COMP_MENOR_NO_NEG1:
    ; Primer número es positivo
    CMP BL, 1
    JNE @SELECTED_COMP_MENOR_AMBOS_POS
    
    ; Positivo < Negativo = FALSE
    MOV AX, 1
    CMP AX, 0   ; ZF=0 (falso)
    JMP @SELECTED_COMP_MENOR_FIN
    
@SELECTED_COMP_MENOR_AMBOS_POS:
    ; Ambos positivos: comparar valores directamente
    CALL COMPARAR_VALORES_ABSOLUTOS_MENOR
    JMP @SELECTED_COMP_MENOR_FIN
    
@SELECTED_COMP_MENOR_AMBOS_NEG:
    ; Ambos negativos: el de mayor valor absoluto es menor
    CALL COMPARAR_VALORES_ABSOLUTOS_MAYOR
    
@SELECTED_COMP_MENOR_FIN:
    POP BX
    POP AX
    RET
COMPARAR_FLOTANTES_MENOR ENDP

;------------------------------------------------------------
; Procedimiento: COMPARAR_FLOTANTES_MAYOR  
; Compara si flotante1 > flotante2
; Salida: ZF=1 si es verdadero, ZF=0 si es falso
;------------------------------------------------------------
COMPARAR_FLOTANTES_MAYOR PROC
    PUSH AX
    PUSH BX
    
    ; Normalizar decimales
    CALL NORMALIZAR_DECIMALES_SUMA
    
    ; Comparar signos
    MOV AL, [es_negativo1]
    MOV BL, [es_negativo2]
    
    CMP AL, 1
    JNE @SELECTED_COMP_MAYOR_NO_NEG1
    
    ; Primer número es negativo
    CMP BL, 1
    JE @SELECTED_COMP_MAYOR_AMBOS_NEG
    
    ; Negativo > Positivo = FALSE
    MOV AX, 1
    CMP AX, 0   ; ZF=0 (falso)
    JMP @SELECTED_COMP_MAYOR_FIN
    
@SELECTED_COMP_MAYOR_NO_NEG1:
    ; Primer número es positivo
    CMP BL, 1
    JNE @SELECTED_COMP_MAYOR_AMBOS_POS
    
    ; Positivo > Negativo = TRUE
    XOR AX, AX
    CMP AX, AX  ; ZF=1 (verdadero)
    JMP @SELECTED_COMP_MAYOR_FIN
    
@SELECTED_COMP_MAYOR_AMBOS_POS:
    ; Ambos positivos: comparar valores directamente
    CALL COMPARAR_VALORES_ABSOLUTOS_MAYOR
    JMP @SELECTED_COMP_MAYOR_FIN
    
@SELECTED_COMP_MAYOR_AMBOS_NEG:
    ; Ambos negativos: el de menor valor absoluto es mayor
    CALL COMPARAR_VALORES_ABSOLUTOS_MENOR
    
@SELECTED_COMP_MAYOR_FIN:
    POP BX
    POP AX
    RET
COMPARAR_FLOTANTES_MAYOR ENDP

;------------------------------------------------------------
; Procedimiento: COMPARAR_VALORES_ABSOLUTOS_MENOR  
; Compara valores absolutos para determinar si |val1| < |val2|
; Salida: ZF=1 si es verdadero, ZF=0 si es falso
;------------------------------------------------------------
COMPARAR_VALORES_ABSOLUTOS_MENOR PROC
    PUSH AX
    PUSH BX
    PUSH CX
    PUSH DX
    
    ; Obtener valores absolutos de partes enteras
    MOV AX, [entero1]
    CMP AX, 0
    JGE @SELECTED_ABS_MENOR_ENT1_ABS
    NEG AX
@SELECTED_ABS_MENOR_ENT1_ABS:
    MOV BX, AX  ; BX = |entero1|
    
    MOV AX, [entero2]
    CMP AX, 0
    JGE @SELECTED_ABS_MENOR_ENT2_ABS
    NEG AX
@SELECTED_ABS_MENOR_ENT2_ABS:
    MOV CX, AX  ; CX = |entero2|
    
    ; Comparar partes enteras
    CMP BX, CX
    JL @SELECTED_ABS_MENOR_VERDADERO   ; |ent1| < |ent2|
    JG @SELECTED_ABS_MENOR_FALSO       ; |ent1| > |ent2|
    
    ; Partes enteras iguales, comparar decimales
    MOV AX, [decimal1]
    MOV DX, [decimal2]
    
    CMP AX, DX
    JL @SELECTED_ABS_MENOR_VERDADERO   ; |dec1| < |dec2|
    JMP @SELECTED_ABS_MENOR_FALSO      ; |dec1| >= |dec2|
    
@SELECTED_ABS_MENOR_VERDADERO:
    XOR AX, AX
    CMP AX, AX  ; ZF=1 (verdadero)
    JMP @SELECTED_ABS_MENOR_FIN_CORR
    
@SELECTED_ABS_MENOR_FALSO:
    MOV AX, 1
    CMP AX, 0   ; ZF=0 (falso)
    
@SELECTED_ABS_MENOR_FIN_CORR:
    POP DX
    POP CX
    POP BX
    POP AX
    RET
COMPARAR_VALORES_ABSOLUTOS_MENOR ENDP

;------------------------------------------------------------
; Procedimiento: COMPARAR_VALORES_ABSOLUTOS_MAYOR  
; Compara valores absolutos para determinar si |val1| > |val2|
; Salida: ZF=1 si es verdadero, ZF=0 si es falso
;------------------------------------------------------------
COMPARAR_VALORES_ABSOLUTOS_MAYOR PROC
    PUSH AX
    PUSH BX
    PUSH CX
    PUSH DX
    
    ; Obtener valores absolutos de partes enteras
    MOV AX, [entero1]
    CMP AX, 0
    JGE @SELECTED_ABS_MAYOR_ENT1_ABS
    NEG AX
@SELECTED_ABS_MAYOR_ENT1_ABS:
    MOV BX, AX  ; BX = |entero1|
    
    MOV AX, [entero2]
    CMP AX, 0
    JGE @SELECTED_ABS_MAYOR_ENT2_ABS
    NEG AX
@SELECTED_ABS_MAYOR_ENT2_ABS:
    MOV CX, AX  ; CX = |entero2|
    
    ; Comparar partes enteras
    CMP BX, CX
    JG @SELECTED_ABS_MAYOR_VERDADERO   ; |ent1| > |ent2|
    JL @SELECTED_ABS_MAYOR_FALSO       ; |ent1| < |ent2|
    
    ; Partes enteras iguales, comparar decimales
    MOV AX, [decimal1]
    MOV DX, [decimal2]
    
    CMP AX, DX
    JG @SELECTED_ABS_MAYOR_VERDADERO   ; |dec1| > |dec2|
    JMP @SELECTED_ABS_MAYOR_FALSO      ; |dec1| <= |dec2|
    
@SELECTED_ABS_MAYOR_VERDADERO:
    XOR AX, AX
    CMP AX, AX  ; ZF=1 (verdadero)
    JMP @SELECTED_ABS_MAYOR_FIN_CORR
    
@SELECTED_ABS_MAYOR_FALSO:
    MOV AX, 1
    CMP AX, 0   ; ZF=0 (falso)
    
@SELECTED_ABS_MAYOR_FIN_CORR:
    POP DX
    POP CX
    POP BX
    POP AX
    RET
COMPARAR_VALORES_ABSOLUTOS_MAYOR ENDP

;------------------------------------------------------------
; Procedimiento: COMPARAR_VALORES_ABSOLUTOS_IGUAL
; Compara valores absolutos para determinar si |val1| == |val2|
; Salida: ZF=1 si son iguales, ZF=0 si son diferentes
;------------------------------------------------------------
COMPARAR_VALORES_ABSOLUTOS_IGUAL PROC
    PUSH AX
    PUSH BX
    
    ; Normalizar decimales para comparación justa
    CALL NORMALIZAR_DECIMALES_SUMA
    
    ; Comparar partes enteras
    MOV AX, [entero1]
    MOV BX, [entero2]
    
    ; Tomar valores absolutos
    CMP AX, 0
    JGE @SELECTED_ABS_IGUAL_ENT1_POS
    NEG AX
@SELECTED_ABS_IGUAL_ENT1_POS:
    
    CMP BX, 0
    JGE @SELECTED_ABS_IGUAL_ENT2_POS
    NEG BX
@SELECTED_ABS_IGUAL_ENT2_POS:
    
    CMP AX, BX
    JNE @SELECTED_ABS_IGUAL_FALSE
    
    ; Partes enteras iguales, comparar decimales
    MOV AX, [decimal1]
    MOV BX, [decimal2]
    
    CMP AX, BX
    JE @SELECTED_ABS_IGUAL_TRUE
    
@SELECTED_ABS_IGUAL_FALSE:
    MOV AX, 0
    CMP AX, 1  ; ZF=0 (diferentes)
    JMP @SELECTED_ABS_IGUAL_FIN
    
@SELECTED_ABS_IGUAL_TRUE:
    MOV AX, 1
    CMP AX, 1  ; ZF=1 (iguales)
    
@SELECTED_ABS_IGUAL_FIN:
    POP BX
    POP AX
    RET
COMPARAR_VALORES_ABSOLUTOS_IGUAL ENDP

;------------------------------------------------------------
; Procedimiento: FLOAT_A_INTEGER
; Convierte el flotante a entero (Stack) - trunca la parte decimal
;------------------------------------------------------------
FLOAT_A_INTEGER PROC
    ; Para flotante a entero, simplemente tomamos la parte entera
    MOV AX, [entero1]
    MOV [int_valor], AX
    
    RET
FLOAT_A_INTEGER ENDP

;------------------------------------------------------------
; Procedimiento: FLOAT_A_BOOLEAN
; Convierte el flotante a booleano (Torch)
; FALSE si es 0.0, TRUE en caso contrario
;------------------------------------------------------------
FLOAT_A_BOOLEAN PROC
    ; Un flotante es FALSE solo si tanto la parte entera como decimal son 0
    CMP WORD PTR [entero1], 0
    JNE @SELECTED_BOOL_TRUE
    CMP WORD PTR [decimal1], 0
    JNE @SELECTED_BOOL_TRUE
    
    ; Es 0.0, por tanto FALSE
    MOV [bool_valor], 0
    JMP @SELECTED_BOOL_FIN
    
@SELECTED_BOOL_TRUE:
    ; No es 0.0, por tanto TRUE
    MOV [bool_valor], 1
    
@SELECTED_BOOL_FIN:
    RET
FLOAT_A_BOOLEAN ENDP

;------------------------------------------------------------
; Procedimiento: FLOAT_A_CHAR
; Convierte el flotante a caracter (Rune)
; Toma el primer dígito de la parte entera
;------------------------------------------------------------
FLOAT_A_CHAR PROC
    PUSH AX
    PUSH BX
    PUSH DX
    
    ; Obtener valor absoluto de la parte entera
    MOV AX, [entero1]
    CMP AX, 0
    JGE @SELECTED_CHAR_POSITIVO
    NEG AX
    
@SELECTED_CHAR_POSITIVO:
    ; Extraer el primer dígito significativo
    CMP AX, 10
    JL @SELECTED_CHAR_UN_DIGITO
    
    ; Tiene más de un dígito, extraer el primero
    MOV BX, 10
@SELECTED_CHAR_EXTRAER:
    CMP AX, 10
    JL @SELECTED_CHAR_UN_DIGITO
    
    XOR DX, DX
    DIV BX  ; AX = AX / 10
    JMP @SELECTED_CHAR_EXTRAER
    
@SELECTED_CHAR_UN_DIGITO:
    ; Convertir a caracter ASCII
    ADD AL, '0'
    MOV [char_valor], AL
    
    POP DX
    POP BX
    POP AX
    RET
FLOAT_A_CHAR ENDP

;------------------------------------------------------------
; Procedimiento: FLOAT_A_STRING
; Convierte el flotante a string (Spider)
;------------------------------------------------------------
FLOAT_A_STRING PROC
    PUSH AX
    PUSH BX
    PUSH CX
    PUSH DX
    PUSH SI
    PUSH DI
    
    ; Limpiar buffer de string
    LEA DI, string_buffer
    
    ; Verificar si es negativo
    CMP [es_negativo1], 0
    JE @SELECTED_STR_POSITIVO
    
    ; Agregar signo negativo
    MOV BYTE PTR [DI], '-'
    INC DI
    
@SELECTED_STR_POSITIVO:
    ; Convertir parte entera a string
    MOV AX, [entero1]
    
    ; Tomar valor absoluto
    CMP [es_negativo1], 0
    JE @SELECTED_STR_ENT_ABS
    NEG AX
    
@SELECTED_STR_ENT_ABS:
    ; Caso especial: cero
    CMP AX, 0
    JNE @SELECTED_STR_ENT_NO_CERO
    
    MOV BYTE PTR [DI], '0'
    INC DI
    JMP @SELECTED_STR_PUNTO
    
@SELECTED_STR_ENT_NO_CERO:
    ; Convertir dígitos de la parte entera
    XOR CX, CX  ; Contador de dígitos
    MOV BX, 10  ; Divisor
    
@SELECTED_STR_DIV_LOOP:
    XOR DX, DX
    DIV BX      ; AX = AX / 10, DX = resto (dígito)
    PUSH DX     ; Guardar dígito en pila
    INC CX      ; Incrementar contador
    
    CMP AX, 0
    JNE @SELECTED_STR_DIV_LOOP
    
    ; Sacar dígitos de la pila en orden correcto
@SELECTED_STR_POP_LOOP:
    POP DX
    ADD DL, '0'
    MOV [DI], DL
    INC DI
    LOOP @SELECTED_STR_POP_LOOP
    
@SELECTED_STR_PUNTO:
    ; Agregar punto decimal
    MOV BYTE PTR [DI], '.'
    INC DI
    
    ; Convertir parte decimal
    CMP BYTE PTR [dec_digitos1], 0
    JNE @SELECTED_STR_HAY_DECIMALES
    
    ; No hay decimales, agregar 0
    MOV BYTE PTR [DI], '0'
    INC DI
    JMP @SELECTED_STR_TERMINAR
    
@SELECTED_STR_HAY_DECIMALES:
    ; Calcular cuántos ceros iniciales necesitamos
    XOR CH, CH
    MOV CL, [dec_digitos1]
    MOV SI, CX  ; SI = total de dígitos decimales necesarios
    
    ; Contar dígitos reales en decimal1
    MOV AX, [decimal1]
    CMP AX, 0
    JNE @SELECTED_STR_CONTAR_DEC
    
    ; decimal1 es 0, agregar todos ceros
    MOV CX, SI
@SELECTED_STR_CEROS_LOOP:
    MOV BYTE PTR [DI], '0'
    INC DI
    LOOP @SELECTED_STR_CEROS_LOOP
    JMP @SELECTED_STR_TERMINAR
    
@SELECTED_STR_CONTAR_DEC:
    ; Contar dígitos reales
    XOR CX, CX  ; Contador de dígitos reales
    MOV BX, 10
    
@SELECTED_STR_CONTAR_LOOP:
    XOR DX, DX
    DIV BX
    INC CX
    CMP AX, 0
    JNE @SELECTED_STR_CONTAR_LOOP
    
    ; SI = dígitos necesarios, CX = dígitos reales
    ; Agregar ceros iniciales si es necesario
    MOV AX, SI
    SUB AX, CX
    CMP AX, 0
    JLE @SELECTED_STR_SIN_CEROS_INIT
    
    MOV CX, AX
@SELECTED_STR_CEROS_INIT_LOOP:
    MOV BYTE PTR [DI], '0'
    INC DI
    LOOP @SELECTED_STR_CEROS_INIT_LOOP
    
@SELECTED_STR_SIN_CEROS_INIT:
    ; Agregar dígitos decimales reales
    MOV AX, [decimal1]
    XOR CX, CX
    MOV BX, 10
    
@SELECTED_STR_DEC_DIV_LOOP:
    XOR DX, DX
    DIV BX
    PUSH DX
    INC CX
    CMP AX, 0
    JNE @SELECTED_STR_DEC_DIV_LOOP
    
@SELECTED_STR_DEC_POP_LOOP:
    POP DX
    ADD DL, '0'
    MOV [DI], DL
    INC DI
    LOOP @SELECTED_STR_DEC_POP_LOOP
    
@SELECTED_STR_TERMINAR:
    ; Agregar terminador
    MOV BYTE PTR [DI], '$'
    
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
; Convierte el flotante a tipo creativo (probabilidad 0.X)
; Usa el primer dígito de la parte entera
;------------------------------------------------------------
FLOAT_A_CREATIVO PROC
    PUSH AX
    PUSH BX
    PUSH DX
    
    ; Verificar si el flotante es 0.0
    CMP WORD PTR [entero1], 0
    JNE @SELECTED_CREATIVO_NO_CERO
    CMP WORD PTR [decimal1], 0
    JNE @SELECTED_CREATIVO_NO_CERO
    
    ; Es 0.0, probabilidad es 0
    MOV BYTE PTR [prob_valor], 0
    JMP @SELECTED_CREATIVO_FIN
    
@SELECTED_CREATIVO_NO_CERO:
    ; Obtener valor absoluto de la parte entera
    MOV AX, [entero1]
    CMP AX, 0
    JGE @SELECTED_CREATIVO_POSITIVO
    NEG AX
    
@SELECTED_CREATIVO_POSITIVO:
    ; Extraer el primer dígito
    CMP AX, 10
    JL @SELECTED_CREATIVO_UN_DIGITO
    
    ; Tiene más de un dígito, extraer el primero
    MOV BX, 10
@SELECTED_CREATIVO_EXTRAER:
    CMP AX, 10
    JL @SELECTED_CREATIVO_UN_DIGITO
    
    XOR DX, DX
    DIV BX  ; AX = AX / 10
    JMP @SELECTED_CREATIVO_EXTRAER
    
@SELECTED_CREATIVO_UN_DIGITO:
    ; AX contiene el primer dígito (0-9)
    MOV [prob_valor], AL
    
@SELECTED_CREATIVO_FIN:
    POP DX
    POP BX
    POP AX
    RET
FLOAT_A_CREATIVO ENDP

;------------------------------------------------------------
; Procedimiento: MOSTRAR_RESULTADO_FLOTANTE
; Muestra el resultado de una operación flotante
;------------------------------------------------------------
MOSTRAR_RESULTADO_FLOTANTE PROC
    CALL NUEVA_LINEA
    
    MOV AH, 09h
    LEA DX, result_msg
    INT 21h
    
    ; Mostrar el flotante resultado
    CALL MOSTRAR_FLOTANTE_RESULTADO
    
    CALL NUEVA_LINEA
    CALL NUEVA_LINEA
    
    RET
MOSTRAR_RESULTADO_FLOTANTE ENDP

;------------------------------------------------------------
; Procedimiento: MOSTRAR_FLOTANTE_RESULTADO
; Muestra un flotante desde las variables de resultado
;------------------------------------------------------------
MOSTRAR_FLOTANTE_RESULTADO PROC
    PUSH AX
    PUSH BX
    PUSH CX
    PUSH DX
    
    ; Mostrar signo si es negativo
    CMP [resultado_negativo], 0
    JE @SELECTED_MOSTRAR_PARTE_ENTERA
    
    MOV DL, '-'
    MOV AH, 02h
    INT 21h
    
@SELECTED_MOSTRAR_PARTE_ENTERA:
    ; Mostrar parte entera
    MOV AX, [resultado_entero]
    
    ; Tomar valor absoluto para mostrar
    CMP [resultado_negativo], 0
    JE @SELECTED_MOSTRAR_ENT_POS
    CMP AX, 0
    JGE @SELECTED_MOSTRAR_ENT_POS
    NEG AX
    
@SELECTED_MOSTRAR_ENT_POS:
    CALL MOSTRAR_NUMERO_POSITIVO
    
    ; Mostrar punto decimal
    MOV AH, 09h
    LEA DX, punto
    INT 21h
    
    ; Mostrar parte decimal
    CALL MOSTRAR_DECIMAL_RESULTADO
    
    POP DX
    POP CX
    POP BX
    POP AX
    RET
MOSTRAR_FLOTANTE_RESULTADO ENDP

;------------------------------------------------------------
; Procedimiento: MOSTRAR_DECIMAL_RESULTADO
; Muestra la parte decimal del resultado
;------------------------------------------------------------
MOSTRAR_DECIMAL_RESULTADO PROC
    PUSH AX
    PUSH BX
    PUSH CX
    PUSH DX
    
    ; Verificar si hay dígitos decimales
    CMP BYTE PTR [resultado_digitos], 0
    JNE @SELECTED_MOSTRAR_DEC_HAY
    
    ; No hay decimales, mostrar 0
    MOV DL, '0'
    MOV AH, 02h
    INT 21h
    JMP @SELECTED_MOSTRAR_DEC_FIN
    
@SELECTED_MOSTRAR_DEC_HAY:
    ; Calcular cuántos dígitos necesitamos mostrar
    XOR CH, CH
    MOV CL, [resultado_digitos]
    MOV BX, CX  ; BX = total de dígitos necesarios
    
    ; Si resultado_decimal es 0, mostrar todos ceros
    CMP WORD PTR [resultado_decimal], 0
    JNE @SELECTED_MOSTRAR_DEC_NO_CERO
    
    MOV CX, BX
@SELECTED_MOSTRAR_DEC_SOLO_CEROS:
    MOV DL, '0'
    MOV AH, 02h
    INT 21h
    LOOP @SELECTED_MOSTRAR_DEC_SOLO_CEROS
    JMP @SELECTED_MOSTRAR_DEC_FIN
    
@SELECTED_MOSTRAR_DEC_NO_CERO:
    ; Contar dígitos reales en resultado_decimal
    MOV AX, [resultado_decimal]
    XOR CX, CX  ; Contador de dígitos reales
    PUSH BX     ; Guardar total de dígitos necesarios
    MOV BX, 10
    
@SELECTED_MOSTRAR_DEC_CONTAR:
    XOR DX, DX
    DIV BX
    INC CX
    CMP AX, 0
    JNE @SELECTED_MOSTRAR_DEC_CONTAR
    
    POP BX      ; Recuperar total de dígitos necesarios
    
    ; BX = dígitos necesarios, CX = dígitos reales
    ; Calcular ceros iniciales
    MOV AX, BX
    SUB AX, CX
    CMP AX, 0
    JLE @SELECTED_MOSTRAR_DEC_SIN_CEROS
    
    ; Mostrar ceros iniciales
    MOV CX, AX
@SELECTED_MOSTRAR_DEC_CEROS_INIT:
    MOV DL, '0'
    MOV AH, 02h
    INT 21h
    LOOP @SELECTED_MOSTRAR_DEC_CEROS_INIT
    
@SELECTED_MOSTRAR_DEC_SIN_CEROS:
    ; Mostrar dígitos reales
    MOV AX, [resultado_decimal]
    CALL MOSTRAR_NUMERO_POSITIVO
    
@SELECTED_MOSTRAR_DEC_FIN:
    POP DX
    POP CX
    POP BX
    POP AX
    RET
MOSTRAR_DECIMAL_RESULTADO ENDP

;------------------------------------------------------------
; Procedimiento: MOSTRAR_CONVERSIONES
; Muestra todas las conversiones del flotante
;------------------------------------------------------------
MOSTRAR_CONVERSIONES PROC
    CALL NUEVA_LINEA
    
    ; Mostrar flotante original
    MOV AH, 09h
    LEA DX, prompt_conversiones_orig
    INT 21h
    
    ; Mostrar el flotante original usando entero1, decimal1, etc.
    CALL MOSTRAR_FLOTANTE_ORIGINAL
    
    CALL NUEVA_LINEA
    
    ; Mostrar conversión a entero (Stack)
    MOV AH, 09h
    LEA DX, prompt_conv_int
    INT 21h
    
    MOV AX, [int_valor]
    CALL MOSTRAR_NUMERO_CON_SIGNO
    
    CALL NUEVA_LINEA
    
    ; Mostrar conversión a booleano (Torch)
    MOV AH, 09h
    LEA DX, prompt_conv_bool
    INT 21h
    
    CMP [bool_valor], 0
    JE @SELECTED_CONV_BOOL_FALSE
    
    LEA DX, valor_true
    JMP @SELECTED_CONV_BOOL_MOSTRAR
    
@SELECTED_CONV_BOOL_FALSE:
    LEA DX, valor_false
    
@SELECTED_CONV_BOOL_MOSTRAR:
    MOV AH, 09h
    INT 21h
    
    CALL NUEVA_LINEA
    
    ; Mostrar conversión a caracter (Rune)
    MOV AH, 09h
    LEA DX, prompt_conv_char
    INT 21h
    
    MOV DL, [char_valor]
    MOV AH, 02h
    INT 21h
    
    CALL NUEVA_LINEA
    
    ; Mostrar conversión a string (Spider)
    MOV AH, 09h
    LEA DX, prompt_conv_str
    INT 21h
    
    LEA DX, string_buffer
    INT 21h
    
    CALL NUEVA_LINEA
    
    ; Mostrar conversión a creativo (probabilidad)
    MOV AH, 09h
    LEA DX, prompt_conv_creativo
    INT 21h
    
    ; Mostrar formato 0.X
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
; Procedimiento: MOSTRAR_FLOTANTE_ORIGINAL
; Muestra el flotante original usando las variables 1
;------------------------------------------------------------
MOSTRAR_FLOTANTE_ORIGINAL PROC
    PUSH AX
    PUSH BX
    PUSH CX
    PUSH DX
    
    ; Mostrar signo si es negativo
    CMP [es_negativo1], 0
    JE @SELECTED_ORIG_PARTE_ENTERA
    
    MOV DL, '-'
    MOV AH, 02h
    INT 21h
    
@SELECTED_ORIG_PARTE_ENTERA:
    ; Mostrar parte entera
    MOV AX, [entero1]
    
    ; Tomar valor absoluto
    CMP [es_negativo1], 0
    JE @SELECTED_ORIG_ENT_POS
    CMP AX, 0
    JGE @SELECTED_ORIG_ENT_POS
    NEG AX
    
@SELECTED_ORIG_ENT_POS:
    CALL MOSTRAR_NUMERO_POSITIVO
    
    ; Mostrar punto decimal
    MOV AH, 09h
    LEA DX, punto
    INT 21h
    
    ; Mostrar parte decimal
    CMP BYTE PTR [dec_digitos1], 0
    JNE @SELECTED_ORIG_HAY_DECIMALES
    
    ; No hay decimales, mostrar 0
    MOV DL, '0'
    MOV AH, 02h
    INT 21h
    JMP @SELECTED_ORIG_FIN
    
@SELECTED_ORIG_HAY_DECIMALES:
    ; Mostrar decimales del flotante original
    XOR CH, CH
    MOV CL, [dec_digitos1]
    
    CMP WORD PTR [decimal1], 0
    JNE @SELECTED_ORIG_DEC_NO_CERO
    
    ; decimal1 es 0, mostrar ceros
@SELECTED_ORIG_CEROS_LOOP:
    MOV DL, '0'
    MOV AH, 02h
    INT 21h
    LOOP @SELECTED_ORIG_CEROS_LOOP
    JMP @SELECTED_ORIG_FIN
    
@SELECTED_ORIG_DEC_NO_CERO:
    ; Mostrar valor real de decimal1 con ceros iniciales si es necesario
    ; (Implementación similar a otros procedimientos de mostrar decimales)
    MOV AX, [decimal1]
    CALL MOSTRAR_NUMERO_POSITIVO
    
@SELECTED_ORIG_FIN:
    POP DX
    POP CX
    POP BX
    POP AX
    RET
MOSTRAR_FLOTANTE_ORIGINAL ENDP

;------------------------------------------------------------
; Procedimiento: MOSTRAR_NUMERO_POSITIVO
; Muestra un número positivo en pantalla
; Entrada: AX = número a mostrar (debe ser positivo)
;------------------------------------------------------------
MOSTRAR_NUMERO_POSITIVO PROC
    PUSH AX
    PUSH BX
    PUSH CX
    PUSH DX
    
    ; Caso especial: cero
    CMP AX, 0
    JNE @SELECTED_POS_NO_CERO
    
    MOV DL, '0'
    MOV AH, 02h
    INT 21h
    JMP @SELECTED_POS_FIN
    
@SELECTED_POS_NO_CERO:
    ; Convertir a dígitos usando pila
    XOR CX, CX  ; Contador de dígitos
    MOV BX, 10  ; Divisor
    
@SELECTED_POS_DIV_LOOP:
    XOR DX, DX
    DIV BX      ; AX = AX / 10, DX = resto (dígito)
    PUSH DX     ; Guardar dígito en pila
    INC CX      ; Incrementar contador
    
    CMP AX, 0
    JNE @SELECTED_POS_DIV_LOOP
    
    ; Mostrar dígitos en orden correcto
@SELECTED_POS_MOSTRAR_LOOP:
    POP DX
    ADD DL, '0'
    MOV AH, 02h
    INT 21h
    LOOP @SELECTED_POS_MOSTRAR_LOOP
    
@SELECTED_POS_FIN:
    POP DX
    POP CX
    POP BX
    POP AX
    RET
MOSTRAR_NUMERO_POSITIVO ENDP

;------------------------------------------------------------
; Procedimiento: RESTAR_PARTES_SUMA
; Resta partes para la suma (caso positivo + negativo)
;------------------------------------------------------------
RESTAR_PARTES_SUMA PROC
    PUSH AX
    PUSH BX
    
    ; Determinar cuál es mayor para definir el signo del resultado
    CALL COMPARAR_VALORES_ABSOLUTOS_MAYOR
    JZ @SELECTED_RESTA_SUMA_SEGUNDO_MAYOR
    
    ; Primer número es mayor: resultado = |num1| - |num2|
    MOV AX, [entero1]
    SUB AX, [entero2]
    MOV [resultado_entero], AX
    
    MOV AX, [decimal1]
    SUB AX, [decimal2]
    MOV [resultado_decimal], AX
    
    MOV [resultado_negativo], 0  ; Resultado positivo
    JMP @SELECTED_RESTA_SUMA_FIN
    
@SELECTED_RESTA_SUMA_SEGUNDO_MAYOR:
    ; Segundo número es mayor: resultado = |num2| - |num1|
    MOV AX, [entero2]
    SUB AX, [entero1]
    MOV [resultado_entero], AX
    
    MOV AX, [decimal2]
    SUB AX, [decimal1]
    MOV [resultado_decimal], AX
    
    MOV [resultado_negativo], 1  ; Resultado negativo
    
@SELECTED_RESTA_SUMA_FIN:
    POP BX
    POP AX
    RET
RESTAR_PARTES_SUMA ENDP

;------------------------------------------------------------
; Procedimiento: RESTAR_PARTES_SUMA_INV
; Resta partes para la suma (caso negativo + positivo)
;------------------------------------------------------------
RESTAR_PARTES_SUMA_INV PROC
    ; Similar a RESTAR_PARTES_SUMA pero invirtiendo los operandos
    CALL RESTAR_PARTES_SUMA
    RET
RESTAR_PARTES_SUMA_INV ENDP

;------------------------------------------------------------
; Procedimiento: CONVERTIR_A_ENTEROS_MULT
; Prepara números para multiplicación
;------------------------------------------------------------
CONVERTIR_A_ENTEROS_MULT PROC
    ; Simplificado para este ejemplo
    RET
CONVERTIR_A_ENTEROS_MULT ENDP

;------------------------------------------------------------
; Procedimiento: CONVERTIR_DE_ENTERO_MULT
; Convierte resultado de multiplicación de vuelta a flotante
;------------------------------------------------------------
CONVERTIR_DE_ENTERO_MULT PROC
    ; Simplificado para este ejemplo
    RET
CONVERTIR_DE_ENTERO_MULT ENDP

;------------------------------------------------------------
; Procedimiento: PREPARAR_DIVISION
; Prepara números para división
;------------------------------------------------------------
PREPARAR_DIVISION PROC
    ; Multiplicar el dividendo por 100 para obtener precisión decimal
    MOV AX, [entero1]
    MOV BX, 100
    MUL BX
    MOV [entero1], AX
    RET
PREPARAR_DIVISION ENDP

;------------------------------------------------------------
; Procedimiento: DIVISION_ENTERA_FLOTANTES
; Realiza división entera de flotantes
;------------------------------------------------------------
DIVISION_ENTERA_FLOTANTES PROC
    MOV AX, [entero1]
    MOV BX, [entero2]
    
    ; Tomar valores absolutos
    CMP AX, 0
    JGE @SELECTED_DIV_ENT_ABS1
    NEG AX
@SELECTED_DIV_ENT_ABS1:
    
    CMP BX, 0
    JGE @SELECTED_DIV_ENT_ABS2
    NEG BX
@SELECTED_DIV_ENT_ABS2:
    
    XOR DX, DX
    DIV BX
    MOV [resultado_entero], AX
    
    RET
DIVISION_ENTERA_FLOTANTES ENDP

;------------------------------------------------------------
; Procedimiento: COMPARAR_FLOTANTES_MENOR_IGUAL
; Compara si flotante1 <= flotante2
; Salida: ZF=1 si es verdadero, ZF=0 si es falso
;------------------------------------------------------------
COMPARAR_FLOTANTES_MENOR_IGUAL PROC
    ; A <= B es equivalente a (A < B) OR (A == B)
    
    CALL COMPARAR_FLOTANTES_MENOR
    JZ @SELECTED_MENIG_ES_MENOR  ; Si ZF=1, es menor
    
    ; No es menor, verificar si es igual
    CALL COMPARAR_FLOTANTES_IGUAL
    JMP @SELECTED_MENIG_FIN_NUEVO
    
@SELECTED_MENIG_ES_MENOR:
    ; Es menor, por tanto es menor o igual (ZF ya está en 1)
    
@SELECTED_MENIG_FIN_NUEVO:
    RET
COMPARAR_FLOTANTES_MENOR_IGUAL ENDP

;------------------------------------------------------------
; Procedimiento: COMPARAR_FLOTANTES_MAYOR_IGUAL
; Compara si flotante1 >= flotante2
; Salida: ZF=1 si es verdadero, ZF=0 si es falso
;------------------------------------------------------------
COMPARAR_FLOTANTES_MAYOR_IGUAL PROC
    ; A >= B es equivalente a (A > B) OR (A == B)
    
    CALL COMPARAR_FLOTANTES_MAYOR
    JZ @SELECTED_MAYIG_ES_MAYOR  ; Si ZF=1, es mayor
    
    ; No es mayor, verificar si es igual
    CALL COMPARAR_FLOTANTES_IGUAL
    JMP @SELECTED_MAYIG_FIN_NUEVO
    
@SELECTED_MAYIG_ES_MAYOR:
    ; Es mayor, por tanto es mayor o igual (ZF ya está en 1)
    
@SELECTED_MAYIG_FIN_NUEVO:
    RET
COMPARAR_FLOTANTES_MAYOR_IGUAL ENDP


;------------------------------------------------------------
; Procedimiento: MOSTRAR_NUMERO_CON_SIGNO
; Muestra un número con signo
; Entrada: AX = número a mostrar
;------------------------------------------------------------
MOSTRAR_NUMERO_CON_SIGNO PROC
    PUSH AX
    
    ; Verificar si es negativo
    CMP AX, 0
    JGE @SELECTED_SIGNO_POSITIVO
    
    ; Mostrar signo negativo
    PUSH AX
    MOV DL, '-'
    MOV AH, 02h
    INT 21h
    POP AX
    
    ; Hacer positivo
    NEG AX
    
@SELECTED_SIGNO_POSITIVO:
    ; Mostrar número positivo
    CALL MOSTRAR_NUMERO_POSITIVO
    
    POP AX
    RET
MOSTRAR_NUMERO_CON_SIGNO ENDP

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

CODIGO ENDS
END INICIO
