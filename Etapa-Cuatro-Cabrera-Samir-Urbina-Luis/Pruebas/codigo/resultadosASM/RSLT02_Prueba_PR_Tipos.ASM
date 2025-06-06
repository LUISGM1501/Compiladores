; =============================================
; Archivo generado por el compilador Notch Engine
; 
; Autores: Samir Cabrera y Luis Urbina
; Curso: Compiladores e Intérpretes, IC5701
; Prueba: 02_Prueba_PR_Tipos.txt
; =============================================

section .data
    ; Variables globales inicializadas

section .bss
    ; Variables globales no inicializadas

section .text
    global _start

_start:
    ; Código principal aquí

    ; Terminar programa
    mov eax, 1      ; syscall exit
    mov ebx, 0      ; status 0
    int 0x80        ; llamar al kernel
