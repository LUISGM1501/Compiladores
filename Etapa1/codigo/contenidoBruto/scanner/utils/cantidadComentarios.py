def contar_comentarios_linea(texto):
    """
    Cuenta la cantidad de comentarios de línea que comienzan con '$$'.
    Cada comentario de línea termina al final de la línea.
    """
    contador = 0
    lineas = texto.splitlines()
    
    for linea in lineas:
        if '$$' in linea:
            contador += 1
    
    return contador


def contar_comentarios_bloque(texto):
    """
    Cuenta la cantidad de bloques de comentarios que empiezan con '$*' y terminan con '*$'.
    No importa si hay saltos de línea dentro del comentario.
    """
    contador = 0
    indice = 0
    longitud = len(texto)
    
    while indice < longitud:
        inicio = texto.find('$*', indice)
        if inicio == -1:
            break  # No hay más bloques
        
        fin = texto.find('*$', inicio + 2)
        if fin == -1:
            break  # No se encontró el cierre
        
        contador += 1
        indice = fin + 2  # Avanzar después del cierre '*$'
    
    return contador
