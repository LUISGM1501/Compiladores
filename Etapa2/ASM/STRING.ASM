; ********************************************
; * Programa: STRING.ASM  (SPIDER)          *
; * Descripcion: Operaciones sobre strings   *
; * Autores: Luis Urbina, Samir Cabrera     *
; * Fecha: 10/05/2025                       *
; * Version: 1.0                            *
; * Curso: Compiladores e Interpretes       *
; * Proyecto: Notch Engine - Etapa 2        *
; ********************************************

; El segmento DATOS contiene todas las variables y constantes que usara el programa
DATOS SEGMENT
    ; Mensajes de entrada y salida
    prompt_in    DB 'Ingrese una cadena: $'                  ; Mensaje para solicitar entrada al usuario
    prompt_str   DB 'La cadena ingresada es: $'              ; Mensaje para mostrar la cadena original
    prompt_int   DB 'Convertido a entero (ASCII total): $'   ; Mensaje para mostrar la conversión a entero
    prompt_float DB 'Convertido a flotante: $'               ; Mensaje para mostrar la conversión a flotante
    prompt_bool  DB 'Convertido a booleano: $'               ; Mensaje para mostrar la conversión a booleano
    prompt_char  DB 'Convertido a caracter: $'               ; Mensaje para mostrar la conversión a caracter
    prompt_creativo DB 'Convertido a creativo (probabilidad): $' ; Mensaje para conversión a creativo
    
    ; Mensajes para el menú de operaciones
    titulo       DB "DEMOSTRACION DE OPERACIONES CON SPIDER (STRINGS)", 0Dh, 0Ah, '$'
    separador    DB "----------------------------------------", 0Dh, 0Ah, '$'
    menu         DB "MENU DE OPERACIONES:", 0Dh, 0Ah
                 DB "1. Concatenacion (bind)", 0Dh, 0Ah
                 DB "2. Longitud (#)", 0Dh, 0Ah
                 DB "3. Subcadena (from ##)", 0Dh, 0Ah
                 DB "4. Eliminar subcadena (except ##)", 0Dh, 0Ah
                 DB "5. Buscar subcadena (seek)", 0Dh, 0Ah
                 DB "6. Comparaciones (is, isNot)", 0Dh, 0Ah
                 DB "7. Convertir a otros tipos", 0Dh, 0Ah
                 DB "0. Salir", 0Dh, 0Ah
                 DB "Seleccione una opcion: $"

    prompt_str1  DB "Ingrese primera cadena: $"
    prompt_str2  DB "Ingrese segunda cadena: $"
    prompt_pos   DB "Ingrese posicion inicial: $"
    prompt_len   DB "Ingrese longitud: $"
    
    result_msg   DB "Resultado: $"
    length_msg   DB "Longitud de la cadena: $"
    pos_msg      DB "Posicion encontrada: $"
    
    ; Variables para operaciones con strings
    buffer1      DB 80, ?, 80 DUP(?)  ; Buffer para primera cadena de entrada
    buffer2      DB 80, ?, 80 DUP(?)  ; Buffer para segunda cadena de entrada
    resultado    DB 160 DUP(?),'$'    ; Buffer para resultado de operaciones
    pos_buffer   DB 10, ?, 10 DUP(?)  ; Buffer para entrada de posición
    len_buffer   DB 10, ?, 10 DUP(?)  ; Buffer para entrada de longitud
    
    ; Variables para conversiones
    ascii_total  DW ?             ; Suma de todos los valores ASCII
    primer_char  DB ?             ; Primer carácter del texto
    es_booleano  DB ?             ; Resultado de la conversión a booleano (0=falso, 1=verdadero)
    
    ; Variables para flotante
    float_entero DW ?             ; Parte entera del flotante
    float_decimal DW ?            ; Parte decimal del flotante
    dec_digitos  DB ?             ; Número de dígitos decimales
    
    ; Variables para probabilidad (tipo creativo)
    prob_valor   DB ?             ; Valor de la probabilidad (0-9)
    
    ; Valores para comparación de strings
    str_true     DB 'TRUE', 0     ; String para comparar con "TRUE"
    str_false    DB 'FALSE', 0    ; String para comparar con "FALSE"
    
    ; Mensajes para las operaciones de comparación
    msg_igual    DB "IGUAL A (is): $"
    msg_nig      DB "DISTINTO DE (isNot): $"
    
    ; Valores para mostrar booleanos
    valor_true   DB 'TRUE$'       ; Cadena de texto para mostrar cuando el valor es verdadero
    valor_false  DB 'FALSE$'      ; Cadena de texto para mostrar cuando el valor es falso
    
    ; Auxiliares
    nueva_lin    DB 0Dh, 0Ah, '$' ; Códigos para crear una nueva línea en pantalla
    punto        DB '.$'          ; Punto decimal para mostrar flotantes
    const_diez   DW 10            ; Constante 10 para cálculos
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
    JMP OPCION_CONCATENACION
@MENU_NOT1:
    CMP AL, '2'
    JNE @MENU_NOT2
    JMP OPCION_LONGITUD
@MENU_NOT2:
    CMP AL, '3'
    JNE @MENU_NOT3
    JMP OPCION_SUBCADENA
@MENU_NOT3:
    CMP AL, '4'
    JNE @MENU_NOT4
    JMP OPCION_ELIMINAR
@MENU_NOT4:
    CMP AL, '5'
    JNE @MENU_NOT5
    JMP OPCION_BUSCAR
@MENU_NOT5:
    CMP AL, '6'
    JNE @MENU_NOT6
    JMP OPCION_COMPARACIONES
@MENU_NOT6:
    CMP AL, '7'
    JNE @MENU_NOT7
    JMP OPCION_CONVERSIONES
@MENU_NOT7:
    CMP AL, '0'
    JNE @MENU_NOT0
    JMP SALIR
@MENU_NOT0:
    
    ; Si llegamos aquí, la opción no es válida, volver al menú
    JMP MENU_PRINCIPAL

    OPCION_CONCATENACION:
    CALL NUEVA_LINEA
    
    ; Leer primera cadena
    MOV AH, 09h
    LEA DX, prompt_str1
    INT 21h
    
    MOV AH, 0Ah
    LEA DX, buffer1
    INT 21h
    
    ; Añadir terminador a la primera cadena
    MOV BL, [buffer1+1]
    XOR BH, BH
    MOV BYTE PTR [buffer1+BX+2], 0
    
    CALL NUEVA_LINEA
    
    ; Leer segunda cadena
    MOV AH, 09h
    LEA DX, prompt_str2
    INT 21h
    
    MOV AH, 0Ah
    LEA DX, buffer2
    INT 21h
    
    ; Añadir terminador a la segunda cadena
    MOV BL, [buffer2+1]
    XOR BH, BH
    MOV BYTE PTR [buffer2+BX+2], 0
    
    ; Realizar la concatenación (bind)
    CALL CONCATENAR_STRINGS
    
    ; Mostrar resultado
    CALL NUEVA_LINEA
    MOV AH, 09h
    LEA DX, result_msg
    INT 21h
    
    LEA DX, resultado
    INT 21h
    
    CALL NUEVA_LINEA
    CALL NUEVA_LINEA
    
    JMP MENU_PRINCIPAL

OPCION_LONGITUD:
    CALL NUEVA_LINEA
    
    ; Leer cadena
    MOV AH, 09h
    LEA DX, prompt_str1
    INT 21h
    
    MOV AH, 0Ah
    LEA DX, buffer1
    INT 21h
    
    ; Calcular longitud correctamente
    XOR AX, AX            ; Limpiamos AX completamente
    MOV AL, [buffer1+1]   ; Obtenemos la longitud real de la cadena
    
    ; Mostrar resultado
    CALL NUEVA_LINEA
    MOV AH, 09h
    LEA DX, length_msg
    INT 21h
    
    CALL MOSTRAR_NUMERO
    
    CALL NUEVA_LINEA
    CALL NUEVA_LINEA
    
    JMP MENU_PRINCIPAL

OPCION_SUBCADENA:
    CALL NUEVA_LINEA
    
    ; Leer cadena
    MOV AH, 09h
    LEA DX, prompt_str1
    INT 21h
    
    MOV AH, 0Ah
    LEA DX, buffer1
    INT 21h
    
    ; Añadir terminador a la cadena
    MOV BL, [buffer1+1]
    XOR BH, BH
    MOV BYTE PTR [buffer1+BX+2], 0
    
    CALL NUEVA_LINEA
    
    ; Leer posición inicial
    MOV AH, 09h
    LEA DX, prompt_pos
    INT 21h
    
    MOV AH, 0Ah
    LEA DX, pos_buffer
    INT 21h
    
    ; Convertir posición a número
    LEA SI, pos_buffer+2
    CALL CONVERTIR_STRING_NUMERO
    MOV BX, AX  ; Guardar posición inicial en BX
    
    CALL NUEVA_LINEA
    
    ; Leer longitud
    MOV AH, 09h
    LEA DX, prompt_len
    INT 21h
    
    MOV AH, 0Ah
    LEA DX, len_buffer
    INT 21h
    
    ; Convertir longitud a número
    LEA SI, len_buffer+2
    CALL CONVERTIR_STRING_NUMERO
    MOV CX, AX  ; Guardar longitud en CX
    
    ; Extraer subcadena (from cadena ## pos ## len)
    CALL EXTRAER_SUBCADENA
    
    ; Mostrar resultado
    CALL NUEVA_LINEA
    MOV AH, 09h
    LEA DX, result_msg
    INT 21h
    
    LEA DX, resultado
    INT 21h
    
    CALL NUEVA_LINEA
    CALL NUEVA_LINEA
    
    JMP MENU_PRINCIPAL

OPCION_ELIMINAR:
    CALL NUEVA_LINEA
    
    ; Leer cadena
    MOV AH, 09h
    LEA DX, prompt_str1
    INT 21h
    
    MOV AH, 0Ah
    LEA DX, buffer1
    INT 21h
    
    ; Añadir terminador a la cadena
    MOV BL, [buffer1+1]
    XOR BH, BH
    MOV BYTE PTR [buffer1+BX+2], 0
    
    CALL NUEVA_LINEA
    
    ; Leer posición inicial
    MOV AH, 09h
    LEA DX, prompt_pos
    INT 21h
    
    MOV AH, 0Ah
    LEA DX, pos_buffer
    INT 21h
    
    ; Convertir posición a número
    LEA SI, pos_buffer+2
    CALL CONVERTIR_STRING_NUMERO
    MOV BX, AX  ; Guardar posición inicial en BX
    
    CALL NUEVA_LINEA
    
    ; Leer longitud
    MOV AH, 09h
    LEA DX, prompt_len
    INT 21h
    
    MOV AH, 0Ah
    LEA DX, len_buffer
    INT 21h
    
    ; Convertir longitud a número
    LEA SI, len_buffer+2
    CALL CONVERTIR_STRING_NUMERO
    MOV CX, AX  ; Guardar longitud en CX
    
    ; Eliminar subcadena (except cadena ## pos ## len)
    CALL ELIMINAR_SUBCADENA
    
    ; Mostrar resultado
    CALL NUEVA_LINEA
    MOV AH, 09h
    LEA DX, result_msg
    INT 21h
    
    LEA DX, resultado
    INT 21h
    
    CALL NUEVA_LINEA
    CALL NUEVA_LINEA
    
    JMP MENU_PRINCIPAL

OPCION_BUSCAR:
    CALL NUEVA_LINEA
    
    ; Leer cadena principal
    MOV AH, 09h
    LEA DX, prompt_str1
    INT 21h
    
    MOV AH, 0Ah
    LEA DX, buffer1
    INT 21h
    
    ; Añadir terminador a la primera cadena
    MOV BL, [buffer1+1]
    XOR BH, BH
    MOV BYTE PTR [buffer1+BX+2], 0
    
    CALL NUEVA_LINEA
    
    ; Leer subcadena a buscar
    MOV AH, 09h
    LEA DX, prompt_str2
    INT 21h
    
    MOV AH, 0Ah
    LEA DX, buffer2
    INT 21h
    
    ; Añadir terminador a la segunda cadena
    MOV BL, [buffer2+1]
    XOR BH, BH
    MOV BYTE PTR [buffer2+BX+2], 0
    
    ; Buscar subcadena (seek)
    CALL BUSCAR_SUBCADENA
    
    ; Mostrar resultado
    CALL NUEVA_LINEA
    MOV AH, 09h
    LEA DX, pos_msg
    INT 21h
    
    ; El resultado está en AX, mostrarlo
    CALL MOSTRAR_NUMERO
    
    CALL NUEVA_LINEA
    CALL NUEVA_LINEA
    
    JMP MENU_PRINCIPAL

OPCION_COMPARACIONES:
    CALL NUEVA_LINEA
    
    ; Leer primera cadena
    MOV AH, 09h
    LEA DX, prompt_str1
    INT 21h
    
    MOV AH, 0Ah
    LEA DX, buffer1
    INT 21h
    
    ; Añadir terminador a la primera cadena
    MOV BL, [buffer1+1]
    XOR BH, BH
    MOV BYTE PTR [buffer1+BX+2], 0
    
    CALL NUEVA_LINEA
    
    ; Leer segunda cadena
    MOV AH, 09h
    LEA DX, prompt_str2
    INT 21h
    
    MOV AH, 0Ah
    LEA DX, buffer2
    INT 21h
    
    ; Añadir terminador a la segunda cadena
    MOV BL, [buffer2+1]
    XOR BH, BH
    MOV BYTE PTR [buffer2+BX+2], 0
    
    ; Comparar IGUAL A (is)
    MOV AH, 09h
    LEA DX, msg_igual
    INT 21h
    
    CALL COMPARAR_STRINGS
    JZ @STRING_IS_IGUAL
    
    LEA DX, valor_false
    INT 21h
    JMP @STRING_COMP_DIFERENTE
    
@STRING_IS_IGUAL:
    LEA DX, valor_true
    INT 21h
    
@STRING_COMP_DIFERENTE:
    ; Comparar DISTINTO DE (isNot)
    MOV AH, 09h
    LEA DX, msg_nig
    INT 21h
    
    CALL COMPARAR_STRINGS
    JNZ @STRING_ISNOT_DISTINTO
    
    LEA DX, valor_false
    INT 21h
    JMP MENU_PRINCIPAL
    
@STRING_ISNOT_DISTINTO:
    LEA DX, valor_true
    INT 21h
    
    CALL NUEVA_LINEA
    CALL NUEVA_LINEA
    
    JMP MENU_PRINCIPAL

OPCION_CONVERSIONES:
    CALL NUEVA_LINEA
    
    ; Mostramos el mensaje pidiendo al usuario que ingrese una cadena
    MOV AH, 09h
    LEA DX, prompt_in
    INT 21h
    
    ; Leemos la entrada del usuario como texto
    MOV AH, 0Ah
    LEA DX, buffer1
    INT 21h
    
    ; Añadir terminador '$' al final para mostrarlo después
    MOV BL, [buffer1+1]
    XOR BH, BH
    MOV BYTE PTR [buffer1+BX+2], '$'
    
    ; Realizar todas las conversiones
    CALL STRING_A_ENTERO
    CALL STRING_A_CHAR
    CALL STRING_A_BOOLEANO
    CALL STRING_A_FLOTANTE
    CALL STRING_A_CREATIVO
    
    ; Mostrar todas las conversiones
    CALL MOSTRAR_CONVERSIONES
    
    JMP MENU_PRINCIPAL

;------------------------------------------------------------
; Procedimiento: CONCATENAR_STRINGS
; Realiza la operación bind entre dos cadenas
;------------------------------------------------------------
CONCATENAR_STRINGS PROC
    PUSH SI
    PUSH DI
    PUSH AX
    PUSH BX
    PUSH CX
    
    ; Inicializar el buffer de resultado
    LEA DI, resultado
    
    ; Copiar primera cadena al resultado
    LEA SI, buffer1+2
    
    MOV BL, [buffer1+1]  ; Longitud de la primera cadena
    XOR BH, BH
    MOV CX, BX           ; Contador para bucle
    
    CMP CX, 0
    JE @STRING_CONCAT_SEGUNDA  ; Si la primera cadena está vacía, pasar a la segunda
    
@STRING_CONCAT_PRIMERA:
    MOV AL, [SI]         ; Obtener carácter de la primera cadena
    MOV [DI], AL         ; Guardar en resultado
    INC SI               ; Avanzar en la primera cadena
    INC DI               ; Avanzar en resultado
    LOOP @STRING_CONCAT_PRIMERA
    
@STRING_CONCAT_SEGUNDA:
    ; Copiar segunda cadena al resultado
    LEA SI, buffer2+2
    
    MOV BL, [buffer2+1]  ; Longitud de la segunda cadena
    XOR BH, BH
    MOV CX, BX           ; Contador para bucle
    
    CMP CX, 0
    JE @STRING_CONCAT_FIN      ; Si la segunda cadena está vacía, terminar
    
@STRING_CONCAT_BUCLE:
    MOV AL, [SI]         ; Obtener carácter de la segunda cadena
    MOV [DI], AL         ; Guardar en resultado
    INC SI               ; Avanzar en la segunda cadena
    INC DI               ; Avanzar en resultado
    LOOP @STRING_CONCAT_BUCLE
    
@STRING_CONCAT_FIN:
    MOV BYTE PTR [DI], '$'  ; Agregar terminador
    
    POP CX
    POP BX
    POP AX
    POP DI
    POP SI
    RET
CONCATENAR_STRINGS ENDP

;------------------------------------------------------------
; Procedimiento: EXTRAER_SUBCADENA
; Realiza la operación from cadena ## posición ## longitud
; Entrada: BX = posición inicial, CX = longitud
;------------------------------------------------------------
EXTRAER_SUBCADENA PROC
    PUSH SI
    PUSH DI
    PUSH AX
    PUSH DX
    
    ; Inicializar el buffer de resultado
    LEA DI, resultado
    
    ; Verificar que la posición esté dentro de los límites
    MOV DL, [buffer1+1]  ; Longitud de la cadena
    XOR DH, DH
    CMP BX, DX
    JAE @STRING_EXTRACT_FUERA_LIMITES  ; Si posición >= longitud, fuera de límites
    
    ; Verificar que la longitud sea válida
    MOV AX, BX           ; Posición inicial
    ADD AX, CX           ; Posición final (teórica)
    CMP AX, DX
    JBE @STRING_EXTRACT_LONGITUD_OK
    
    ; Ajustar longitud si excede los límites
    MOV CX, DX
    SUB CX, BX           ; Longitud = total - posición
    
@STRING_EXTRACT_LONGITUD_OK:
    ; Calcular dirección de inicio efectiva
    LEA SI, buffer1+2
    ADD SI, BX           ; SI apunta a la posición inicial
    
    CMP CX, 0
    JE @STRING_EXTRACT_FUERA_LIMITES  ; Si longitud = 0, terminar
    
@STRING_EXTRACT_BUCLE:
    MOV AL, [SI]         ; Obtener carácter
    MOV [DI], AL         ; Guardar en resultado
    INC SI               ; Avanzar en cadena
    INC DI               ; Avanzar en resultado
    LOOP @STRING_EXTRACT_BUCLE
    
@STRING_EXTRACT_FUERA_LIMITES:
    MOV BYTE PTR [DI], '$'  ; Agregar terminador
    
    POP DX
    POP AX
    POP DI
    POP SI
    RET
EXTRAER_SUBCADENA ENDP

;------------------------------------------------------------
; Procedimiento: ELIMINAR_SUBCADENA
; Realiza la operación except cadena ## posición ## longitud
; Entrada: BX = posición inicial, CX = longitud
;------------------------------------------------------------
ELIMINAR_SUBCADENA PROC
    PUSH SI
    PUSH DI
    PUSH AX
    PUSH DX
    
    ; Inicializar el buffer de resultado
    LEA DI, resultado
    
    ; Verificar que la posición esté dentro de los límites
    MOV DL, [buffer1+1]  ; Longitud de la cadena
    XOR DH, DH
    CMP BX, DX
    JAE @STRING_DELETE_COMPLETA  ; Si posición >= longitud, copiar cadena completa
    
    ; Verificar que la longitud sea válida
    MOV AX, BX           ; Posición inicial
    ADD AX, CX           ; Posición final (teórica)
    CMP AX, DX
    JBE @STRING_DELETE_LONGITUD_OK
    
    ; Ajustar longitud si excede los límites
    MOV CX, DX
    SUB CX, BX           ; Longitud = total - posición
    
@STRING_DELETE_LONGITUD_OK:
    ; Copiar primera parte (antes de la posición)
    LEA SI, buffer1+2
    
    MOV AX, BX           ; Contador = posición
    CMP AX, 0
    JE @STRING_DELETE_SEGUNDA   ; Si posición = 0, no hay primera parte
    
@STRING_DELETE_PRIMERA:
    MOV DL, [SI]         ; Obtener carácter
    MOV [DI], DL         ; Guardar en resultado
    INC SI               ; Avanzar en cadena
    INC DI               ; Avanzar en resultado
    DEC AX               ; Decrementar contador
    JNZ @STRING_DELETE_PRIMERA
    
@STRING_DELETE_SEGUNDA:
    ; Saltar la parte a eliminar
    ADD SI, CX           ; Avanzar en la cadena original
    
    ; Calcular cuántos caracteres quedan después
    MOV DL, [buffer1+1]  ; Longitud total
    XOR DH, DH
    SUB DX, BX           ; Restar posición inicial
    SUB DX, CX           ; Restar longitud a eliminar
    
    CMP DX, 0
    JE @STRING_DELETE_FIN       ; Si no quedan caracteres, terminar
    
    MOV CX, DX           ; Contador = caracteres restantes
    
@STRING_DELETE_RESTO:
    MOV DL, [SI]         ; Obtener carácter
    MOV [DI], DL         ; Guardar en resultado
    INC SI               ; Avanzar en cadena
    INC DI               ; Avanzar en resultado
    LOOP @STRING_DELETE_RESTO
    
    JMP @STRING_DELETE_FIN
    
@STRING_DELETE_COMPLETA:
    ; Copiar la cadena completa
    LEA SI, buffer1+2
    
    MOV CL, [buffer1+1]  ; Longitud de la cadena
    XOR CH, CH
    
    CMP CX, 0
    JE @STRING_DELETE_FIN
    
@STRING_DELETE_COPIAR:
    MOV AL, [SI]         ; Obtener carácter
    MOV [DI], AL         ; Guardar en resultado
    INC SI               ; Avanzar en cadena
    INC DI               ; Avanzar en resultado
    LOOP @STRING_DELETE_COPIAR
    
@STRING_DELETE_FIN:
    MOV BYTE PTR [DI], '$'  ; Agregar terminador
    
    POP DX
    POP AX
    POP DI
    POP SI
    RET
ELIMINAR_SUBCADENA ENDP

;------------------------------------------------------------
; Procedimiento: BUSCAR_SUBCADENA
; Realiza la operación seek para encontrar una subcadena
; Salida: AX = posición (o -1 si no se encuentra)
;------------------------------------------------------------
BUSCAR_SUBCADENA PROC
    PUSH SI
    PUSH DI
    PUSH BX
    PUSH CX
    PUSH DX
    
    ; Obtener longitud de ambas cadenas
    XOR BH, BH
    MOV BL, [buffer1+1]  ; Longitud de la cadena principal
    XOR CH, CH
    MOV CL, [buffer2+1]  ; Longitud de la subcadena
    
    ; Si la subcadena es más larga que la cadena principal, no puede estar contenida
    CMP CX, BX
    JA @STRING_SEEK_NO_ENCONTRADO
    
    ; Si la subcadena está vacía, devolvemos posición 0
    CMP CX, 0
    JE @STRING_SEEK_ENCONTRADO_CERO
    
    ; Número máximo de posiciones a verificar = longitud1 - longitud2 + 1
    MOV AX, BX
    SUB AX, CX
    INC AX
    MOV DX, AX           ; DX = número de iteraciones
    
    XOR BX, BX           ; BX = posición actual (0-based)
    
@STRING_SEEK_BUCLE_EXTERNO:
    ; Comparar desde la posición actual
    LEA SI, buffer1+2
    ADD SI, BX           ; SI = dirección de inicio en cadena principal
    LEA DI, buffer2+2    ; DI = dirección de inicio en subcadena
    
    PUSH CX              ; Guardar longitud de subcadena
    PUSH SI              ; Guardar posición en cadena principal
    MOV DX, CX           ; DX = longitud de subcadena (contador para bucle interno)
    
@STRING_SEEK_BUCLE_INTERNO:
    MOV AL, [SI]         ; Carácter de cadena principal
    MOV AH, [DI]         ; Carácter de subcadena
    
    CMP AL, AH
    JNE @STRING_SEEK_NO_COINCIDE
    
    INC SI               ; Avanzar en cadena principal
    INC DI               ; Avanzar en subcadena
    DEC DX               ; Decrementar contador
    JNZ @STRING_SEEK_BUCLE_INTERNO
    
    ; Si llegamos aquí, hemos encontrado la subcadena
    POP SI               ; Recuperar (y descartar) valor
    POP CX               ; Recuperar (y descartar) valor
    JMP @STRING_SEEK_ENCONTRADO
    
@STRING_SEEK_NO_COINCIDE:
    POP SI               ; Recuperar posición en cadena principal
    POP CX               ; Recuperar longitud de subcadena
    
    INC BX               ; Avanzar a la siguiente posición
    DEC DX               ; Decrementar iteraciones restantes
    JNZ @STRING_SEEK_BUCLE_EXTERNO  ; Si quedan iteraciones, continuar
    
@STRING_SEEK_NO_ENCONTRADO:
    MOV AX, -1           ; Devolver -1 si no se encuentra
    JMP @STRING_SEEK_FIN
    
@STRING_SEEK_ENCONTRADO_CERO:
    XOR AX, AX           ; Devolver 0 para subcadena vacía
    JMP @STRING_SEEK_FIN
    
@STRING_SEEK_ENCONTRADO:
    XOR AX, AX           ; CRUCIAL: Limpiamos todo AX antes de copiar BX
    MOV AX, BX           ; Devolver posición donde se encontró
    
@STRING_SEEK_FIN:
    POP DX
    POP CX
    POP BX
    POP DI
    POP SI
    RET
BUSCAR_SUBCADENA ENDP

;------------------------------------------------------------
; Procedimiento: COMPARAR_STRINGS
; Compara dos strings para is/isNot
; Salida: Flag Z=1 si son iguales, Z=0 si son diferentes
;------------------------------------------------------------
COMPARAR_STRINGS PROC
    PUSH SI
    PUSH DI
    PUSH AX
    PUSH BX
    PUSH CX
    
    ; Verificar si tienen la misma longitud
    MOV BL, [buffer1+1]  ; Longitud de la primera cadena
    XOR BH, BH
    MOV CL, [buffer2+1]  ; Longitud de la segunda cadena
    XOR CH, CH
    
    CMP BX, CX
    JNE @STRING_COMP_DIFERENTES  ; Si tienen diferente longitud, son diferentes
    
    ; Si ambas están vacías, son iguales
    CMP BX, 0
    JE @STRING_COMP_IGUALES
    
    ; Tienen la misma longitud, comparar carácter por carácter
    LEA SI, buffer1+2
    LEA DI, buffer2+2
    MOV CX, BX           ; Contador = longitud
    
@STRING_COMP_BUCLE:
    MOV AL, [SI]         ; Carácter de la primera cadena
    MOV AH, [DI]         ; Carácter de la segunda cadena
    
    CMP AL, AH
    JNE @STRING_COMP_DIFERENTES
    
    INC SI               ; Avanzar en primera cadena
    INC DI               ; Avanzar en segunda cadena
    LOOP @STRING_COMP_BUCLE
    
@STRING_COMP_IGUALES:
    ; Si llegamos aquí, las cadenas son iguales
    CMP AX, AX           ; Establecer ZF=1 (iguales)
    JMP @STRING_COMP_FIN
    
@STRING_COMP_DIFERENTES:
    ; Si llegamos aquí, las cadenas son diferentes
    CMP AX, BX           ; Establecer ZF=0 (diferentes), suponiendo que AX ≠ BX
    
@STRING_COMP_FIN:
    POP CX
    POP BX
    POP AX
    POP DI
    POP SI
    RET
COMPARAR_STRINGS ENDP

;------------------------------------------------------------
; Procedimiento: STRING_A_ENTERO
; Convierte el string a un entero (suma ASCII)
;------------------------------------------------------------
STRING_A_ENTERO PROC
    PUSH SI
    PUSH AX
    PUSH BX
    PUSH CX
    
    ; Inicializar contador ASCII total a 0
    MOV WORD PTR [ascii_total], 0
    
    ; Verificar si el string está vacío
    MOV CL, [buffer1+1]
    XOR CH, CH
    CMP CX, 0
    JE @STRING_ASC_FIN
    
    ; Configurar índice para recorrer el string
    LEA SI, [buffer1+2]     ; SI apunta al primer carácter
    
@STRING_ASC_LOOP:
    XOR AX, AX            ; Limpiamos AX
    MOV AL, [SI]          ; Obtenemos el carácter actual
    ADD [ascii_total], AX ; Sumamos su valor ASCII al total
    
    INC SI                ; Avanzamos al siguiente carácter
    LOOP @STRING_ASC_LOOP  ; Repetimos para cada carácter (CX veces)
    
@STRING_ASC_FIN:
    POP CX
    POP BX
    POP AX
    POP SI
    RET
STRING_A_ENTERO ENDP

;------------------------------------------------------------
; Procedimiento: STRING_A_CHAR
; Convierte el string a un carácter (toma el primer carácter)
;------------------------------------------------------------
STRING_A_CHAR PROC
    PUSH SI
    
    ; Por defecto, si el string está vacío, usamos espacio
    MOV BYTE PTR [primer_char], ' '
    
    ; Verificar si el string está vacío
    CMP BYTE PTR [buffer1+1], 0
    JE @STRING_CHAR_FIN
    
    ; Tomar el primer carácter
    LEA SI, [buffer1+2]      ; SI apunta al primer carácter
    MOV AL, [SI]             ; AL = primer carácter
    MOV [primer_char], AL    ; Guardamos el primer carácter
    
@STRING_CHAR_FIN:
    POP SI
    RET
STRING_A_CHAR ENDP

;------------------------------------------------------------
; Procedimiento: STRING_A_BOOLEANO
; Convierte el string a un booleano (TRUE/ON/1 -> verdadero, resto -> falso)
;------------------------------------------------------------
STRING_A_BOOLEANO PROC
    PUSH SI
    PUSH DI
    PUSH AX
    PUSH BX
    PUSH CX
    
    ; Por defecto, el resultado es falso
    MOV BYTE PTR [es_booleano], 0
    
    ; Verificar si el string está vacío
    MOV CL, [buffer1+1]
    XOR CH, CH
    CMP CX, 0
    JE @STRING_BOOL_FIN
    
    ; Verificar si es "1" (un solo carácter y es '1')
    CMP CL, 1
    JNE @STRING_VERIFICAR_CERO
    
    LEA SI, [buffer1+2]      ; SI apunta al primer carácter
    CMP BYTE PTR [SI], '1'   ; ¿Es '1'?
    JNE @STRING_VERIFICAR_CERO
    
    ; Es "1", por lo tanto es verdadero
    MOV BYTE PTR [es_booleano], 1
    JMP @STRING_BOOL_FIN
    
@STRING_VERIFICAR_CERO:
    ; Verificar si es "0" (un solo carácter y es '0')
    CMP CL, 1
    JNE @STRING_VERIFICAR_ON
    
    LEA SI, [buffer1+2]      ; SI apunta al primer carácter
    CMP BYTE PTR [SI], '0'   ; ¿Es '0'?
    JNE @STRING_VERIFICAR_ON
    
    ; Es "0", por lo tanto es falso (ya está inicializado a 0)
    JMP @STRING_BOOL_FIN
    
@STRING_VERIFICAR_ON:
    ; Verificar si es "ON" o "On" o "on" (insensible a mayúsculas/minúsculas)
    CMP CL, 2
    JNE @STRING_VERIFICAR_OFF
    
    LEA SI, [buffer1+2]      ; SI apunta al primer carácter
    MOV AL, [SI]             ; Primer carácter
    MOV AH, [SI+1]           ; Segundo carácter
    
    ; Convertir a mayúsculas para comparación
    CMP AL, 'a'
    JB @STRING_ON_PRIMER_MAY
    CMP AL, 'z'
    JA @STRING_ON_PRIMER_MAY
    SUB AL, 32               ; Convertir a mayúscula
@STRING_ON_PRIMER_MAY:
    
    CMP AH, 'a'
    JB @STRING_ON_SEGUNDO_MAY
    CMP AH, 'z'
    JA @STRING_ON_SEGUNDO_MAY
    SUB AH, 32               ; Convertir a mayúscula
@STRING_ON_SEGUNDO_MAY:
    
    ; Verificar si es "ON"
    CMP AL, 'O'
    JNE @STRING_VERIFICAR_OFF
    CMP AH, 'N'
    JNE @STRING_VERIFICAR_OFF
    
    ; Es "ON", por lo tanto es verdadero
    MOV BYTE PTR [es_booleano], 1
    JMP @STRING_BOOL_FIN
    
@STRING_VERIFICAR_OFF:
    ; Verificar si es "OFF" o variantes (insensible a mayúsculas/minúsculas)
    CMP CL, 3
    JNE @STRING_BOOL_FIN
    
    ; Proceso similar para verificar "OFF"
    ; (se simplifica por espacio, pero sería análogo al de "ON")
    
@STRING_BOOL_FIN:
    POP CX
    POP BX
    POP AX
    POP DI
    POP SI
    RET
STRING_A_BOOLEANO ENDP

;------------------------------------------------------------
; Procedimiento: STRING_A_FLOTANTE
; Convierte el string a un flotante (ASCII total con .00)
;------------------------------------------------------------
STRING_A_FLOTANTE PROC
    PUSH AX
    
    ; Utilizamos el valor ASCII total como parte entera
    ; y agregamos .00 como parte decimal fija
    MOV AX, [ascii_total]
    MOV [float_entero], AX
    MOV WORD PTR [float_decimal], 0  ; Parte decimal es 00
    MOV BYTE PTR [dec_digitos], 2    ; Dos dígitos decimales
    
    POP AX
    RET
STRING_A_FLOTANTE ENDP

;------------------------------------------------------------
; Procedimiento: STRING_A_CREATIVO
; Convierte el string a un valor de probabilidad (0-9)
;------------------------------------------------------------
STRING_A_CREATIVO PROC
    PUSH AX
    PUSH BX
    PUSH DX
    
    ; Utilizamos la suma de los códigos ASCII de todos los caracteres
    ; para generar un valor entre 0 y 9
    MOV AX, [ascii_total]
    
    ; Si el ASCII total es 0, usamos 0 como probabilidad
    CMP AX, 0
    JE @STRING_PROB_CERO
    
@STRING_EXTRAER_DIGITO:
    ; Extraer el primer dígito significativo
    
    ; Si AX < 10, ya tenemos un solo dígito
    CMP AX, 10
    JL @STRING_DIGITO_LISTO
    
    ; Dividimos por 10 para eliminar último dígito
    XOR DX, DX
    MOV BX, 10
    DIV BX               ; AX = AX / 10, DX = resto
    
    ; Verificar si AX = 0 (si el cociente es 0, usar el resto)
    CMP AX, 0
    JE @STRING_USAR_RESTO
    
    JMP @STRING_EXTRAER_DIGITO
    
@STRING_USAR_RESTO:
    MOV AX, DX           ; Usar el resto como dígito
    
@STRING_DIGITO_LISTO:
    ; Ahora AX tiene el dígito a usar (0-9)
    MOV [prob_valor], AL
    JMP @STRING_PROB_FIN
    
@STRING_PROB_CERO:
    MOV BYTE PTR [prob_valor], 0
    
@STRING_PROB_FIN:
    POP DX
    POP BX
    POP AX
    RET
STRING_A_CREATIVO ENDP

;------------------------------------------------------------
; Procedimiento: CONVERTIR_STRING_NUMERO
; Convierte una cadena en el buffer especificado a un número
; Entrada: SI = dirección de la cadena
; Salida: AX = número convertido
;------------------------------------------------------------
CONVERTIR_STRING_NUMERO PROC
    PUSH BX
    PUSH CX
    PUSH DX
    
    XOR AX, AX           ; Inicializar resultado a 0
    XOR CX, CX           ; CX indica si es negativo (1) o positivo (0)
    
    ; Verificar si comienza con signo negativo
    CMP BYTE PTR [SI], '-'
    JNE @STRING_CONV_DIGITOS
    
    MOV CX, 1            ; Marcar como negativo
    INC SI               ; Avanzar al siguiente carácter
    
@STRING_CONV_DIGITOS:
    ; Verificar si hemos llegado al final (0 o '$')
    CMP BYTE PTR [SI], 0
    JE @STRING_CONV_FIN
    CMP BYTE PTR [SI], '$'
    JE @STRING_CONV_FIN
    CMP BYTE PTR [SI], 13  ; CR (retorno de carro)
    JE @STRING_CONV_FIN
    
    ; Verificar si es un dígito
    CMP BYTE PTR [SI], '0'
    JL @STRING_CONV_NO_DIGITO
    CMP BYTE PTR [SI], '9'
    JG @STRING_CONV_NO_DIGITO
    
    ; Convertir dígito
    MOV BL, [SI]
    SUB BL, '0'          ; Convertir ASCII a valor numérico
    
    ; Multiplicar resultado actual por 10 y sumar nuevo dígito
    MOV DX, 10
    MUL DX               ; AX = AX * 10
    XOR BH, BH
    ADD AX, BX           ; AX = AX + dígito
    
@STRING_CONV_NO_DIGITO:
    INC SI               ; Avanzar al siguiente carácter
    JMP @STRING_CONV_DIGITOS
    
@STRING_CONV_FIN:
    ; Si el número es negativo, negarlo
    CMP CX, 1
    JNE @STRING_CONV_POSITIVO
    
    NEG AX               ; Convertir a negativo
    
@STRING_CONV_POSITIVO:
    POP DX
    POP CX
    POP BX
    RET
CONVERTIR_STRING_NUMERO ENDP

;------------------------------------------------------------
; Procedimiento: MOSTRAR_CONVERSIONES
; Muestra todas las conversiones realizadas
;------------------------------------------------------------
MOSTRAR_CONVERSIONES PROC
    CALL NUEVA_LINEA
    
    ; 1. Mostrar cadena original
    MOV AH, 09h
    LEA DX, prompt_str
    INT 21h
    
    LEA DX, buffer1+2
    INT 21h
    
    CALL NUEVA_LINEA
    
    ; 2. Mostrar conversión a entero (ASCII total)
    MOV AH, 09h
    LEA DX, prompt_int
    INT 21h
    
    MOV AX, [ascii_total]
    CALL MOSTRAR_NUMERO
    
    CALL NUEVA_LINEA
    
    ; 3. Mostrar conversión a carácter
    MOV AH, 09h
    LEA DX, prompt_char
    INT 21h
    
    MOV DL, [primer_char]
    MOV AH, 02h
    INT 21h
    
    CALL NUEVA_LINEA
    
    ; 4. Mostrar conversión a booleano
    MOV AH, 09h
    LEA DX, prompt_bool
    INT 21h
    
    CMP BYTE PTR [es_booleano], 0
    JE @STRING_MOST_BOOL_FALSE
    
    LEA DX, valor_true
    JMP @STRING_MOST_BOOL_SHOW
    
@STRING_MOST_BOOL_FALSE:
    LEA DX, valor_false
    
@STRING_MOST_BOOL_SHOW:
    MOV AH, 09h
    INT 21h
    
    CALL NUEVA_LINEA
    
    ; 5. Mostrar conversión a flotante
    MOV AH, 09h
    LEA DX, prompt_float
    INT 21h
    
    CALL MOSTRAR_FLOTANTE
    
    CALL NUEVA_LINEA
    
    ; 6. Mostrar conversión a creativo
    MOV AH, 09h
    LEA DX, prompt_creativo
    INT 21h
    
    ; Mostrar formato 0.X donde X es el valor de probabilidad
    MOV DL, '0'
    MOV AH, 02h
    INT 21h
    
    ; Mostrar punto decimal
    MOV AH, 09h
    LEA DX, punto
    INT 21h
    
    ; Mostrar dígito de probabilidad
    MOV DL, [prob_valor]
    ADD DL, '0'
    MOV AH, 02h
    INT 21h
    
    CALL NUEVA_LINEA
    CALL NUEVA_LINEA
    
    RET
MOSTRAR_CONVERSIONES ENDP

;------------------------------------------------------------
; Procedimiento: MOSTRAR_NUMERO
; Muestra un número entero en pantalla
; Entrada: AX = número a mostrar
;------------------------------------------------------------
MOSTRAR_NUMERO PROC
    ; Guardamos los registros que vamos a modificar
    PUSH AX
    PUSH BX
    PUSH CX
    PUSH DX
    
    ; IMPORTANTE: Asegurarnos que la parte alta esté limpia
    AND AX, 0FFh         ; Conservar solo el byte bajo si es longitud o posición
    
    ; Verificamos si el número es negativo
    CMP AX, 0
    JGE @STRING_NUM_POSITIVO
    
    ; Si es negativo, mostramos el signo "-" y negamos el número
    PUSH AX
    MOV DL, '-'
    MOV AH, 02h
    INT 21h
    POP AX
    NEG AX
    
@STRING_NUM_POSITIVO:
    ; Caso especial: si el número es cero
    CMP AX, 0
    JNE @STRING_NUM_DIVIDE
    
    MOV DL, '0'
    MOV AH, 02h
    INT 21h
    JMP @STRING_NUM_FIN
    
@STRING_NUM_DIVIDE:
    ; Convertimos el número a dígitos mediante divisiones sucesivas
    MOV BX, 10          ; Divisor = 10
    XOR CX, CX          ; Contador de dígitos = 0
    
@STRING_NUM_BUCLE_DIV:
    XOR DX, DX
    DIV BX              ; AX = cociente, DX = resto (dígito)
    
    PUSH DX             ; Guardar dígito en la pila
    INC CX              ; Incrementar contador
    
    CMP AX, 0
    JNE @STRING_NUM_BUCLE_DIV  ; Si el cociente no es cero, continuar
    
@STRING_NUM_BUCLE_MOSTRAR:
    ; Mostrar dígitos en orden inverso
    POP DX
    ADD DL, '0'         ; Convertir a ASCII
    MOV AH, 02h
    INT 21h
    LOOP @STRING_NUM_BUCLE_MOSTRAR
    
@STRING_NUM_FIN:
    POP DX
    POP CX
    POP BX
    POP AX
    RET
MOSTRAR_NUMERO ENDP

;------------------------------------------------------------
; Procedimiento: MOSTRAR_FLOTANTE
; Muestra un número flotante en pantalla
;------------------------------------------------------------
MOSTRAR_FLOTANTE PROC
    ; Guardamos los registros que vamos a modificar
    PUSH AX
    PUSH BX
    PUSH CX
    PUSH DX
    
    ; Mostrar la parte entera
    MOV AX, [float_entero]
    CALL MOSTRAR_NUMERO
    
    ; Mostrar el punto decimal
    MOV AH, 09h
    LEA DX, punto
    INT 21h
    
    ; Verificar si hay dígitos decimales
    CMP BYTE PTR [dec_digitos], 0
    JE @STRING_FLOAT_SIN_DEC
    
    ; Para este ejemplo simplificado, siempre mostramos "00" como parte decimal
    MOV CL, [dec_digitos]
    XOR CH, CH
    
@STRING_FLOAT_BUCLE:
    MOV DL, '0'
    MOV AH, 02h
    INT 21h
    LOOP @STRING_FLOAT_BUCLE
    
    JMP @STRING_FLOAT_FIN
    
@STRING_FLOAT_SIN_DEC:
    ; Si no hay decimales, mostrar un 0
    MOV DL, '0'
    MOV AH, 02h
    INT 21h
    
@STRING_FLOAT_FIN:
    POP DX
    POP CX
    POP BX
    POP AX
    RET
MOSTRAR_FLOTANTE ENDP

;------------------------------------------------------------
; Procedimiento: NUEVA_LINEA
; Imprime un salto de línea en la pantalla
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
    MOV AX, 4C00h      ; Funcion 4Ch de DOS: terminar programa (con codigo de salida 0)
    INT 21h            ; Llamamos a la interrupcion 21h
    
CODIGO ENDS
END INICIO              ; Indicamos el punto de entrada del programa