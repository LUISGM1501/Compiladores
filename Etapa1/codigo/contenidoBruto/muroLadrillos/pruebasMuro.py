# /Etapa1/codigo/contenidoBruto/muroLadrillos/pruebasMuro.py
from muroLadrillos import generarLadrillos

# Datos de ejemplo
contenido = ["if", "(", "x", ">", "5", ")", "{", "print", "(", "'Hola'", ")", "}", "// Comentario", "/* Otro comentario */", "error","if", "(", "x", ">", "5", ")", "{", "print", "(", "'Hola'", ")", "}", "// Comentario", "/* Otro comentario */", "error","if", "(", "x", ">", "5", ")", "{", "print", "(", "'Hola'", ")", "}", "// Comentario", "/* Otro comentario */", "error","if", "(", "x", ">", "5", ")", "{", "print", "(", "'Hola'", ")", "}", "// Comentario", "/* Otro comentario */", "error","if", "(", "x", ">", "5", ")", "{", "print", "(", "'Hola'", ")", "}", "// Comentario", "/* Otro comentario */", "error","if", "(", "x", ">", "5", ")", "{", "print", "(", "'Hola'", ")", "}", "// Comentario", "/* Otro comentario */", "error","if", "(", "x", ">", "5", ")", "{", "print", "(", "'Hola'", ")", "}", "// Comentario", "/* Otro comentario */", "error","if", "(", "x", ">", "5", ")", "{", "print", "(", "'Hola'", ")", "}", "// Comentario", "/* Otro comentario */", "error"]

estadisticaToken = {
    "Estructura del Programa": 3,
    "Tipos de datos": 0,  # No se mostrará
    "Control de flujo": 1,
    "Operadores de comparación": 1,
    "Funciones de entrada/salida": 1
}

# Llamar a la función
generarLadrillos(
    contenido=contenido,
    estadisticaToken=estadisticaToken,
    lineasPrograma=15,
    numeroCaracteresEntrada=256,
    numeroComentariosLinea=1,
    numeroComentariosBloque=1,
    cantidadErrores=1
)