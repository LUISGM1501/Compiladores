; ********************************************
; * Programa: INTEGER.ASM  (STACK)          *
; * Descripcion: Operaciones sobre enteros  *
; * Autores: Luis Urbina, Samir Cabrera     *
; * Fecha: 10/05/2025                       *
; * Version: 1.0                            *
; * Curso: Compiladores e Interpretes       *
; * Proyecto: Notch Engine - Etapa 2        *
; ********************************************

; El segmento DATOS contiene todas las variables y constantes que usara el programa
DATOS SEGMENT
    ; Mensajes de entrada y salida
    prompt_in    DB 'Ingrese un numero entero: $'            ; Mensaje para solicitar entrada al usuario
    prompt_int   DB 'El numero entero ingresado es: $'       ; Mensaje para mostrar el entero original
    prompt_char  DB 'Convertido a caracter: $'               ; Mensaje para mostrar la conversión a caracter
    prompt_float DB 'Convertido a flotante: $'               ; Mensaje para mostrar la conversión a flotante
    prompt_bool  DB 'Convertido a booleano: $'               ; Mensaje para mostrar la conversión a booleano
    prompt_str   DB 'Convertido a string: $'                 ; Mensaje para mostrar la conversión a string
    prompt_creativo DB 'Convertido a creativo (probabilidad): $' ; Mensaje para conversión a creativo
    
    ; Mensajes para el menú de operaciones
    titulo       DB "DEMOSTRACION DE OPERACIONES CON STACK (ENTEROS)", 0Dh, 0Ah, '$'
    separador    DB "----------------------------------------", 0Dh, 0Ah, '$'
    menu         DB "MENU DE OPERACIONES:", 0Dh, 0Ah
                 DB "1. Suma (+)", 0Dh, 0Ah
                 DB "2. Resta (-)", 0Dh, 0Ah
                 DB "3. Multiplicacion (*)", 0Dh, 0Ah
                 DB "4. Division entera (//)", 0Dh, 0Ah
                 DB "5. Modulo (%)", 0Dh, 0Ah
                 DB "6. Incremento (soulsand)", 0Dh, 0Ah
                 DB "7. Decremento (magma)", 0Dh, 0Ah
                 DB "8. Comparaciones (<, >, <=, >=, is, isNot)", 0Dh, 0Ah
                 DB "9. Convertir a otros tipos", 0Dh, 0Ah
                 DB "0. Salir", 0Dh, 0Ah
                 DB "Seleccione una opcion: $"

    prompt_num1  DB "Ingrese primer numero: $"
    prompt_num2  DB "Ingrese segundo numero: $"
    result_msg   DB "Resultado: $"
    comp_result  DB "Resultado de comparacion: $"
    error_div    DB "Error: Division por cero", 0Dh, 0Ah, '$'
    
    ; Variables para almacenar valores
    buffer      DB 10, ?, 10 DUP(?)  ; Buffer para entrada (maximo 10 caracteres)
    entero      DW ?                 ; Variable para almacenar el numero convertido a binario
    bool_valor  DB ?                 ; Variable para almacenar el valor booleano
    caracter    DB ?                 ; Variable para almacenar el caracter convertido
    num1        DW ?                 ; Variable para el primer número en operaciones
    num2        DW ?                 ; Variable para el segundo número en operaciones
    resultado   DW ?                 ; Variable para el resultado de operaciones
    
    ; Variables para valor flotante
    float_entero DW ?                ; Parte entera del flotante
    float_decimal DW ?               ; Parte decimal del flotante
    dec_digitos  DB ?                ; Número de dígitos decimales
    
    ; Variable para valor string
    string_buffer DB 20 DUP(?),'$'   ; Buffer para la conversión a string
    
    ; Variables para valor creativo (probabilidad)
    primer_digito DB ?               ; Primer dígito del entero para probabilidad
    prob_valor    DB ?               ; Valor final de la probabilidad (0.X)
    es_negativo   DB 0               ; Bandera para indicar si el numero es negativo
    
    ; Mensajes para las operaciones de comparación
    msg_menor    DB "MENOR QUE (<): $"
    msg_mayor    DB "MAYOR QUE (>): $"
    msg_menig    DB "MENOR O IGUAL QUE (<=): $"
    msg_mayig    DB "MAYOR O IGUAL QUE (>=): $"
    msg_igual    DB "IGUAL A (is): $"
    msg_nig      DB "DISTINTO DE (isNot): $"
    
    ; Valores para mostrar booleanos
    valor_true   DB 'TRUE$'          ; Cadena de texto para mostrar cuando el valor es verdadero
    valor_false  DB 'FALSE$'         ; Cadena de texto para mostrar cuando el valor es falso
    
    ; Auxiliares
    nueva_lin    DB 0Dh, 0Ah, '$'    ; Códigos para crear una nueva línea en pantalla
    punto        DB '.$'             ; Punto decimal para mostrar flotantes
    const_diez   DW 10               ; Constante 10 para cálculos
DATOS ENDS

; El segmento CODIGO contiene las instrucciones que ejecutara el programa
CODIGO SEGMENT
    ; Indicamos al ensamblador donde encontrar nuestros datos y codigo
    ASSUME CS:CODIGO, DS:DATOS
INICIO:
    ; Inicializacion: Preparamos el acceso al segmento de datos
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
    
    ; Comparar con las opciones disponibles
    CMP AL, '1'
    JE OPCION_SUMA
    CMP AL, '2'
    JE OPCION_RESTA
    CMP AL, '3'
    JE OPCION_MULTIPLICACION
    CMP AL, '4'
    JE OPCION_DIVISION

    CMP AL, '5'
    JNE @NOT5
    JMP OPCION_MODULO
@NOT5:
    CMP AL, '6'
    JNE @NOT6
    JMP OPCION_INCREMENTO
@NOT6:
    CMP AL, '7'
    JNE @NOT7
    JMP OPCION_DECREMENTO
@NOT7:
    CMP AL, '8'
    JNE @NOT8
    JMP OPCION_COMPARACIONES
@NOT8:
    CMP AL, '9'
    JNE @NOT9
    JMP OPCION_CONVERSIONES
@NOT9:
    CMP AL, '0'
    JNE @NOT0
    JMP SALIR
@NOT0:
    
    ; Si llegamos aquí, la opción no es válida, volver al menú
    JMP MENU_PRINCIPAL

    OPCION_SUMA:
    CALL NUEVA_LINEA
    CALL LEER_DOS_NUMEROS
    
    ; Realizar la suma
    MOV AX, [num1]
    ADD AX, [num2]
    MOV [resultado], AX
    
    ; Mostrar resultado
    CALL MOSTRAR_RESULTADO
    JMP MENU_PRINCIPAL
    
OPCION_RESTA:
    CALL NUEVA_LINEA
    CALL LEER_DOS_NUMEROS
    
    ; Realizar la resta
    MOV AX, [num1]
    SUB AX, [num2]
    MOV [resultado], AX
    
    ; Mostrar resultado
    CALL MOSTRAR_RESULTADO
    JMP MENU_PRINCIPAL

OPCION_MULTIPLICACION:
    CALL NUEVA_LINEA
    CALL LEER_DOS_NUMEROS
    
    ; Realizar la multiplicación
    MOV AX, [num1]
    IMUL WORD PTR [num2]  ; Multiplicación con signo
    MOV [resultado], AX
    
    ; Mostrar resultado
    CALL MOSTRAR_RESULTADO
    JMP MENU_PRINCIPAL

OPCION_DIVISION:
    CALL NUEVA_LINEA
    CALL LEER_DOS_NUMEROS
    
    ; Verificar división por cero
    CMP WORD PTR [num2], 0
    JE ERROR_DIVISION_CERO
    
    ; Realizar la división
    MOV AX, [num1]
    CWD                    ; Extender el signo de AX a DX:AX
    IDIV WORD PTR [num2]   ; División con signo
    MOV [resultado], AX    ; El cociente queda en AX
    
    ; Mostrar resultado
    CALL MOSTRAR_RESULTADO
    JMP MENU_PRINCIPAL
    
ERROR_DIVISION_CERO:
    MOV AH, 09h
    LEA DX, error_div
    INT 21h
    JMP MENU_PRINCIPAL

OPCION_MODULO:
    CALL NUEVA_LINEA
    CALL LEER_DOS_NUMEROS
    
    ; Verificar división por cero
    CMP WORD PTR [num2], 0
    JE ERROR_DIVISION_CERO
    
    ; Realizar la operación módulo
    MOV AX, [num1]
    CWD                    ; Extender el signo de AX a DX:AX
    IDIV WORD PTR [num2]   ; División con signo
    MOV [resultado], DX    ; El resto queda en DX
    
    ; Mostrar resultado
    CALL MOSTRAR_RESULTADO
    JMP MENU_PRINCIPAL

    OPCION_INCREMENTO:
    CALL NUEVA_LINEA
    
    ; Leer un solo número
    MOV AH, 09h
    LEA DX, prompt_num1
    INT 21h
    
    CALL LEER_NUMERO
    MOV [num1], AX
    
    ; Realizar el incremento (soulsand)
    INC WORD PTR [num1]
    MOV AX, [num1]
    MOV [resultado], AX
    
    ; Mostrar resultado
    CALL MOSTRAR_RESULTADO
    JMP MENU_PRINCIPAL

OPCION_DECREMENTO:
    CALL NUEVA_LINEA
    
    ; Leer un solo número
    MOV AH, 09h
    LEA DX, prompt_num1
    INT 21h
    
    CALL LEER_NUMERO
    MOV [num1], AX
    
    ; Realizar el decremento (magma)
    DEC WORD PTR [num1]
    MOV AX, [num1]
    MOV [resultado], AX
    
    ; Mostrar resultado
    CALL MOSTRAR_RESULTADO
    JMP MENU_PRINCIPAL

    OPCION_COMPARACIONES:
    CALL NUEVA_LINEA
    CALL LEER_DOS_NUMEROS
    
    ; Comparar MENOR QUE (<)
    MOV AH, 09h
    LEA DX, msg_menor
    INT 21h
    
    MOV AX, [num1]
    CMP AX, [num2]
    JL COMP_MENOR_TRUE
    
    LEA DX, valor_false
    INT 21h
    JMP COMP_MAYOR
    
COMP_MENOR_TRUE:
    LEA DX, valor_true
    INT 21h
    
COMP_MAYOR:
    ; Comparar MAYOR QUE (>)
    MOV AH, 09h
    LEA DX, msg_mayor
    INT 21h
    
    MOV AX, [num1]
    CMP AX, [num2]
    JG COMP_MAYOR_TRUE
    
    LEA DX, valor_false
    INT 21h
    JMP COMP_MENIG
    
COMP_MAYOR_TRUE:
    LEA DX, valor_true
    INT 21h
    
COMP_MENIG:
    ; Comparar MENOR O IGUAL QUE (<=)
    MOV AH, 09h
    LEA DX, msg_menig
    INT 21h
    
    MOV AX, [num1]
    CMP AX, [num2]
    JLE COMP_MENIG_TRUE
    
    LEA DX, valor_false
    INT 21h
    JMP COMP_MAYIG
    
COMP_MENIG_TRUE:
    LEA DX, valor_true
    INT 21h
    
COMP_MAYIG:
    ; Comparar MAYOR O IGUAL QUE (>=)
    MOV AH, 09h
    LEA DX, msg_mayig
    INT 21h
    
    MOV AX, [num1]
    CMP AX, [num2]
    JGE COMP_MAYIG_TRUE
    
    LEA DX, valor_false
    INT 21h
    JMP COMP_IGUAL
    
COMP_MAYIG_TRUE:
    LEA DX, valor_true
    INT 21h
    
COMP_IGUAL:
    ; Comparar IGUAL A (is)
    MOV AH, 09h
    LEA DX, msg_igual
    INT 21h
    
    MOV AX, [num1]
    CMP AX, [num2]
    JE COMP_IGUAL_TRUE
    
    LEA DX, valor_false
    INT 21h
    JMP COMP_NOEQ
    
COMP_IGUAL_TRUE:
    LEA DX, valor_true
    INT 21h
    
COMP_NOEQ:
    ; Comparar DISTINTO DE (isNot)
    MOV AH, 09h
    LEA DX, msg_nig
    INT 21h
    
    MOV AX, [num1]
    CMP AX, [num2]
    JNE COMP_NOEQ_TRUE
    
    LEA DX, valor_false
    INT 21h
    JMP MENU_PRINCIPAL
    
COMP_NOEQ_TRUE:
    LEA DX, valor_true
    INT 21h
    JMP MENU_PRINCIPAL

    OPCION_CONVERSIONES:
    CALL NUEVA_LINEA
    
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
    
    ; Realizar todas las conversiones desde el entero
    CALL INT_A_CHAR      ; Convertir a caracter
    CALL INT_A_FLOTANTE  ; Convertir a flotante
    CALL INT_A_BOOLEANO  ; Convertir a booleano
    CALL INT_A_STRING    ; Convertir a string
    CALL INT_A_CREATIVO  ; Convertir a creativo (probabilidad)
    
    ; Mostrar todas las conversiones
    CALL MOSTRAR_RESULTADOS
    
    JMP MENU_PRINCIPAL

    ;------------------------------------------------------------
; Procedimiento: STR_A_NUM
; Este procedimiento convierte una cadena de texto (en el buffer) a un numero binario
; y lo guarda en la variable 'entero'
;------------------------------------------------------------
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
    ; Guardamos el primer dígito para el creativo (si existe)
    CMP BX, 0
    JE CONVERSION_PROCESAR  ; Si no hay dígitos, saltamos
    
    MOV CL, [SI]           ; Obtenemos el primer caracter
    CMP CL, '0'             ; Verificamos si es un dígito
    JL PRIMER_DIGITO_LISTO
    CMP CL, '9'
    JG PRIMER_DIGITO_LISTO
    
    ; Si es un dígito, lo guardamos (primer dígito válido)
    SUB CL, '0'             ; Convertimos ASCII a valor numérico
    MOV [primer_digito], CL
    
PRIMER_DIGITO_LISTO:
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
    MOV [entero], AX   ; Guardamos el resultado en la variable 'entero'
    
    ; Restauramos los registros que modificamos
    POP SI
    POP DX
    POP CX
    POP BX
    POP AX
    RET                ; Retornamos al punto de llamada
STR_A_NUM ENDP

;------------------------------------------------------------
; Procedimiento: INT_A_CHAR
; Convierte el entero al primer dígito del número como caracter
;------------------------------------------------------------
INT_A_CHAR PROC
    ; Para entero a caracter, convertimos el primer dígito del número
    ; a su representación como caracter
    PUSH AX
    PUSH BX
    PUSH DX
    
    ; Primero verificamos si es negativo
    MOV AX, [entero]
    CMP AX, 0
    JGE INT_POSITIVO
    
    ; Si es negativo, lo hacemos positivo para obtener dígitos
    NEG AX
    
INT_POSITIVO:
    ; Determinar el primer dígito (el más significativo)
    ; Dividimos repetidamente por 10 hasta que quede un solo dígito
    MOV BX, 10
    
OBTENER_PRIMER_DIGITO:
    CMP AX, 10
    JL DIGITO_ENCONTRADO   ; Si es menor que 10, ya tenemos un solo dígito
    
    XOR DX, DX
    DIV BX                 ; AX = AX / 10, DX = resto (último dígito)
    ; Seguimos hasta obtener el primer dígito (el más significativo)
    JMP OBTENER_PRIMER_DIGITO
    
DIGITO_ENCONTRADO:
    ; Ahora AX contiene el primer dígito
    ADD AL, '0'            ; Convertir a ASCII
    MOV [caracter], AL     ; Guardar el caracter
    
    POP DX
    POP BX
    POP AX
    RET
INT_A_CHAR ENDP

;------------------------------------------------------------
; Procedimiento: INT_A_FLOTANTE
; Convierte el entero a flotante (valor.00)
;------------------------------------------------------------
INT_A_FLOTANTE PROC
    ; Para entero a flotante, usamos el mismo valor como parte entera
    ; y la parte decimal es siempre 0
    MOV AX, [entero]
    MOV [float_entero], AX    ; Guardamos en la parte entera del flotante
    
    ; La parte decimal es siempre 0 para esta conversión
    MOV WORD PTR [float_decimal], 0
    MOV BYTE PTR [dec_digitos], 2     ; Dos dígitos decimales (00)
    
    RET
INT_A_FLOTANTE ENDP

;------------------------------------------------------------
; Procedimiento: INT_A_BOOLEANO
; Convierte el entero a booleano (FALSE si es 0, TRUE en caso contrario)
;------------------------------------------------------------
INT_A_BOOLEANO PROC
    ; Para entero a booleano, es FALSE solo si el valor es 0
    CMP WORD PTR [entero], 0
    JE ES_FALSO
    
    ; Si llegamos aquí, el entero es distinto de 0
    MOV [bool_valor], 1       ; TRUE
    JMP BOOL_FIN
    
ES_FALSO:
    MOV [bool_valor], 0       ; FALSE
    
BOOL_FIN:
    RET
INT_A_BOOLEANO ENDP

;------------------------------------------------------------
; Procedimiento: INT_A_STRING
; Convierte el entero a su representación textual
;------------------------------------------------------------
INT_A_STRING PROC
    PUSH AX
    PUSH BX
    PUSH CX
    PUSH DX
    PUSH DI
    
    ; Empezamos con el buffer vacío
    LEA DI, string_buffer
    
    ; Verificamos si el número es negativo
    MOV AX, [entero]
    CMP AX, 0
    JGE STRING_POSITIVO
    
    ; Si es negativo, agregamos el signo '-' al inicio
    MOV BYTE PTR [DI], '-'
    INC DI            ; Avanzamos al siguiente byte en el buffer
    NEG AX            ; Hacemos positivo el número para procesarlo
    
STRING_POSITIVO:
    ; Caso especial: si el número es cero
    CMP AX, 0
    JNE CONVERTIR_DIGITOS
    
    MOV BYTE PTR [DI], '0'    ; Ponemos el carácter '0'
    INC DI                    ; Avanzamos en el buffer
    JMP FIN_STRING            ; Terminamos
    
CONVERTIR_DIGITOS:
    ; Necesitamos los dígitos en orden inverso
    ; Usamos la pila para invertir el orden
    MOV BX, 10      ; Divisor = 10
    XOR CX, CX      ; Contador de dígitos
    
BUCLE_DIGITOS:
    XOR DX, DX      ; Limpiamos DX para la división
    DIV BX          ; AX = AX / 10, DX = resto (dígito)
    
    PUSH DX         ; Guardamos el dígito en la pila
    INC CX          ; Incrementamos contador
    
    CMP AX, 0
    JNE BUCLE_DIGITOS  ; Si AX no es 0, continuamos
    
    ; Ahora sacamos los dígitos de la pila y los agregamos al buffer
AGREGAR_DIGITOS:
    POP DX          ; Recuperamos un dígito
    ADD DL, '0'     ; Convertimos a carácter ASCII
    MOV [DI], DL    ; Lo ponemos en el buffer
    INC DI          ; Avanzamos en el buffer
    LOOP AGREGAR_DIGITOS
    
FIN_STRING:
    MOV BYTE PTR [DI], '$'  ; Terminador de string
    
    POP DI
    POP DX
    POP CX
    POP BX
    POP AX
    RET
INT_A_STRING ENDP

;------------------------------------------------------------
; Procedimiento: INT_A_CREATIVO
; Convierte el entero a un valor de probabilidad basado en su primer dígito
;------------------------------------------------------------
INT_A_CREATIVO PROC
    ; Extraemos el primer dígito del número para usar como probabilidad (0.X)
    PUSH AX
    PUSH BX
    PUSH DX
    
    ; Verificamos primero si el número es 0
    MOV AX, [entero]
    CMP AX, 0
    JE PROB_CERO
    
    ; Si es negativo, lo hacemos positivo para trabajar
    CMP AX, 0
    JGE POSITIVO_PROB
    NEG AX
    
POSITIVO_PROB:
    ; Ahora extraemos el primer dígito
    ; Hacemos divisiones hasta que quede un solo dígito
    MOV BX, 10
    
EXTRAER_PRIMER_DIGITO:
    ; Si AX < 10, ya tenemos un solo dígito
    CMP AX, 10
    JL DIGITO_UNICO
    
    ; Dividimos por 10 para eliminar el último dígito
    XOR DX, DX
    DIV BX                 ; AX = AX / 10, DX = resto
    JMP EXTRAER_PRIMER_DIGITO
    
DIGITO_UNICO:
    ; Ahora AX tiene el primer dígito (el más significativo)
    MOV [prob_valor], AL
    JMP CREATIVO_FIN
    
PROB_CERO:
    ; Si el número es 0, la probabilidad es 0
    MOV BYTE PTR [prob_valor], 0
    
CREATIVO_FIN:
    POP DX
    POP BX
    POP AX
    RET
INT_A_CREATIVO ENDP

;------------------------------------------------------------
; Procedimiento: LEER_DOS_NUMEROS
; Lee dos números enteros de la entrada estándar
;------------------------------------------------------------
LEER_DOS_NUMEROS PROC
    ; Leer primer número
    MOV AH, 09h
    LEA DX, prompt_num1
    INT 21h
    
    CALL LEER_NUMERO
    MOV [num1], AX
    
    ; Leer segundo número
    MOV AH, 09h
    LEA DX, prompt_num2
    INT 21h
    
    CALL LEER_NUMERO
    MOV [num2], AX
    
    RET
LEER_DOS_NUMEROS ENDP

;------------------------------------------------------------
; Procedimiento: LEER_NUMERO
; Lee un número entero de la entrada estándar
;------------------------------------------------------------
LEER_NUMERO PROC
    ; Esta función lee un número entero desde la entrada estándar
    PUSH BX
    PUSH CX
    PUSH DX
    
    XOR BX, BX          ; BX contendrá el número
    XOR CX, CX          ; CX indicará si es negativo (1) o positivo (0)
    
    ; Leer primer carácter
    MOV AH, 01h
    INT 21h
    
    ; Verificar si es el signo negativo
    CMP AL, '-'
    JNE LEER_DIGITO    ; Si no es negativo, procesar como dígito
    
    MOV CX, 1          ; Marcar como negativo
    
    ; Leer siguiente carácter (primer dígito)
    MOV AH, 01h
    INT 21h
    
LEER_DIGITO:
    ; Verificar si el carácter es un dígito
    CMP AL, '0'
    JL FIN_LECTURA     ; Si es menor que '0', no es dígito
    CMP AL, '9'
    JG FIN_LECTURA     ; Si es mayor que '
    ; Verificar si el carácter es un dígito
    CMP AL, '0'
    JL FIN_LECTURA     ; Si es menor que '0', no es dígito
    CMP AL, '9'
    JG FIN_LECTURA     ; Si es mayor que '9', no es dígito
    
    ; Convertir carácter a dígito
    SUB AL, '0'
    
    ; Multiplicar número actual por 10 y sumar el nuevo dígito
    PUSH AX            ; Guardar el dígito
    MOV AX, BX         ; Cargar número actual en AX
    MOV DX, 10         ; Multiplicador = 10
    MUL DX             ; AX = AX * 10
    MOV BX, AX         ; Guardar resultado en BX
    POP AX             ; Recuperar dígito
    
    XOR AH, AH         ; Limpiar AH
    ADD BX, AX         ; Añadir dígito al número
    
    ; Leer siguiente carácter
    MOV AH, 01h
    INT 21h
    
    JMP LEER_DIGITO    ; Procesar siguiente carácter
    
FIN_LECTURA:
    ; Si el número es negativo, negarlo
    CMP CX, 1
    JNE NUMERO_POSITIVO
    
    NEG BX             ; Negar el número
    
NUMERO_POSITIVO:
    MOV AX, BX         ; Poner resultado en AX
    
    POP DX
    POP CX
    POP BX
    RET
LEER_NUMERO ENDP

;------------------------------------------------------------
; Procedimiento: MOSTRAR_RESULTADO
; Muestra el resultado de una operación
;------------------------------------------------------------
MOSTRAR_RESULTADO PROC
    CALL NUEVA_LINEA
    
    MOV AH, 09h
    LEA DX, result_msg
    INT 21h
    
    MOV AX, [resultado]
    CALL MOSTRAR_NUMERO
    
    CALL NUEVA_LINEA
    CALL NUEVA_LINEA
    
    RET
MOSTRAR_RESULTADO ENDP

;------------------------------------------------------------
; Procedimiento: MOSTRAR_NUMERO
; Muestra un número entero en pantalla
;------------------------------------------------------------
MOSTRAR_NUMERO PROC
    ; Esta función muestra un número entero en pantalla
    PUSH AX
    PUSH BX
    PUSH CX
    PUSH DX
    
    MOV BX, AX         ; Guardar número en BX
    
    ; Si el número es negativo, mostrar signo menos
    TEST BX, 8000h      ; Verificar bit de signo
    JZ MOSTRAR_POSITIVO
    
    PUSH BX
    MOV AH, 02h
    MOV DL, '-'
    INT 21h
    POP BX
    
    NEG BX             ; Convertir a positivo
    
MOSTRAR_POSITIVO:
    MOV AX, BX
    XOR CX, CX         ; Contador de dígitos
    MOV BX, 10         ; Divisor
    
    ; Caso especial: si el número es cero
    CMP AX, 0
    JNE EXTRAER_DIGITOS
    
    MOV AH, 02h
    MOV DL, '0'
    INT 21h
    JMP FIN_MOSTRAR_NUMERO
    
EXTRAER_DIGITOS:
    ; Dividir número entre 10
    XOR DX, DX
    DIV BX             ; AX = cociente, DX = resto
    
    PUSH DX            ; Guardar dígito en la pila
    INC CX             ; Incrementar contador de dígitos
    
    CMP AX, 0
    JNE EXTRAER_DIGITOS ; Si el cociente no es cero, continuar
    
    ; Mostrar dígitos en orden inverso
MOSTRAR_DIGITOS:
    POP DX
    ADD DL, '0'         ; Convertir a ASCII
    MOV AH, 02h
    INT 21h
    LOOP MOSTRAR_DIGITOS
    
FIN_MOSTRAR_NUMERO:
    POP DX
    POP CX
    POP BX
    POP AX
    RET
MOSTRAR_NUMERO ENDP

;------------------------------------------------------------
; Procedimiento: NUEVA_LINEA
; Muestra un salto de línea en pantalla
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

;------------------------------------------------------------
; Procedimiento: MOSTRAR_RESULTADOS
; Muestra el resultado original y todas las conversiones
;------------------------------------------------------------
MOSTRAR_RESULTADOS PROC
    ; Mostramos una nueva línea
    MOV AH, 09h
    LEA DX, nueva_lin
    INT 21h
    
    ; 1. Mostrar el entero original
    MOV AH, 09h
    LEA DX, prompt_int
    INT 21h
    
    MOV AX, [entero]
    CALL MOSTRAR_ENTERO
    
    ; Nueva línea
    MOV AH, 09h
    LEA DX, nueva_lin
    INT 21h
    
    ; 2. Mostrar conversión a caracter
    MOV AH, 09h
    LEA DX, prompt_char
    INT 21h
    
    MOV DL, [caracter]
    MOV AH, 02h         ; Función 2: mostrar caracter
    INT 21h
    
    ; Nueva línea
    MOV AH, 09h
    LEA DX, nueva_lin
    INT 21h
    
    ; 3. Mostrar conversión a flotante
    MOV AH, 09h
    LEA DX, prompt_float
    INT 21h
    
    CALL MOSTRAR_FLOTANTE
    
    ; Nueva línea
    MOV AH, 09h
    LEA DX, nueva_lin
    INT 21h
    
    ; 4. Mostrar conversión a booleano
    MOV AH, 09h
    LEA DX, prompt_bool
    INT 21h
    
    ; Decidir si mostrar "TRUE" o "FALSE"
    CMP [bool_valor], 0
    JE MOSTRAR_BOOL_FALSE
    
    MOV AH, 09h
    LEA DX, valor_true
    INT 21h
    JMP MOSTRAR_STR
    
MOSTRAR_BOOL_FALSE:
    MOV AH, 09h
    LEA DX, valor_false
    INT 21h
    
MOSTRAR_STR:
    ; Nueva línea
    MOV AH, 09h
    LEA DX, nueva_lin
    INT 21h
    
    ; 5. Mostrar conversión a string
    MOV AH, 09h
    LEA DX, prompt_str
    INT 21h
    
    MOV AH, 09h
    LEA DX, string_buffer
    INT 21h
    
    ; Nueva línea
    MOV AH, 09h
    LEA DX, nueva_lin
    INT 21h
    
    ; 6. Mostrar conversión a creativo (probabilidad)
    MOV AH, 09h
    LEA DX, prompt_creativo
    INT 21h
    
    ; Para el tipo creativo de probabilidad mostramos "0.X"
    MOV DL, '0'         ; El cero inicial
    MOV AH, 02h
    INT 21h
    
    ; Mostrar punto decimal
    MOV AH, 09h
    LEA DX, punto
    INT 21h
    
    ; Mostrar el valor de probabilidad
    MOV DL, [prob_valor]
    ADD DL, '0'         ; Convertir a carácter
    MOV AH, 02h
    INT 21h
    
    CALL NUEVA_LINEA
    
    RET
MOSTRAR_RESULTADOS ENDP

;------------------------------------------------------------
; Procedimiento: MOSTRAR_ENTERO
; Muestra un número entero en pantalla
; Entrada: AX = número a mostrar
;------------------------------------------------------------
MOSTRAR_ENTERO PROC
    ; Guardamos los registros que vamos a modificar
    PUSH AX
    PUSH BX
    PUSH CX
    PUSH DX
    
    ; Verificamos si el número es negativo
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
    
MOSTRAR_DIGITOS_INT:
    ; Mostramos los digitos en orden inverso (sacandolos de la pila)
    POP DX             ; Recuperamos un digito
    ADD DL, '0'        ; Convertimos el valor numerico a caracter ASCII
    MOV AH, 02h        ; Funcion 2 de DOS: mostrar un caracter
    INT 21h            ; Mostramos el digito
    LOOP MOSTRAR_DIGITOS_INT ; Repetimos para cada digito (CX veces)
    
NUM_A_STR_FIN:
    ; Restauramos los registros que modificamos
    POP DX
    POP CX
    POP BX
    POP AX
    RET                ; Retornamos al punto de llamada
MOSTRAR_ENTERO ENDP

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
    CALL MOSTRAR_ENTERO
    
    ; Mostrar el punto decimal
    MOV AH, 09h
    LEA DX, punto
    INT 21h
    
    ; Verificar si hay dígitos decimales
    CMP BYTE PTR [dec_digitos], 0
    JE FLOTANTE_SIN_DECIMALES
    
    ; Mostrar la parte decimal
    XOR CH, CH                ; Limpiar la parte alta (CH)
    MOV CL, [dec_digitos]     ; Cargar el byte en la parte baja (CL)
    
    ; Si la parte decimal es 0, mostrar todos los dígitos como ceros
    CMP WORD PTR [float_decimal], 0
    JNE DECIMALES_NO_CERO
    
MOSTRAR_SOLO_CEROS:
    MOV DL, '0'
    MOV AH, 02h
    INT 21h
    
    LOOP MOSTRAR_SOLO_CEROS
    JMP FIN_MOSTRAR_FLOTANTE
    
DECIMALES_NO_CERO:
    ; Si llegamos aquí, tenemos decimales distintos de cero
    ; (pero para esta conversión siempre son ceros)
    JMP MOSTRAR_SOLO_CEROS
    
FLOTANTE_SIN_DECIMALES:
    ; Si no hay decimales, mostrar un 0
    MOV DL, '0'
    MOV AH, 02h
    INT 21h
    
FIN_MOSTRAR_FLOTANTE:
    ; Restaurar registros
    POP DX
    POP CX
    POP BX
    POP AX
    RET
MOSTRAR_FLOTANTE ENDP

SALIR:
    ; Terminamos el programa y regresamos al sistema operativo
    MOV AX, 4C00h      ; Funcion 4Ch de DOS: terminar programa (con codigo de salida 0)
    INT 21h            ; Llamamos a la interrupcion 21h
    
CODIGO ENDS
END INICIO              ; Indicamos el punto de entrada del programa