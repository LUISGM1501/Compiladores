from ..HistorialSemantico import historialSemantico
from ..HistorialSemanticoNegativo import historialSemanticoNegativo

def checkArchivoNombre(valores):
    """
    Regla Semántica 010: Verifica que el primer valor de una instrucción BOOK
    sea un archivo con extensión .txt.
    """
    if not valores:
        return False  # No hay valores que verificar

    archivo = valores[0]

    # Limpieza si el archivo viene con comillas
    if archivo.startswith('"') and archivo.endswith('"'):
        archivo = archivo[1:-1]

    if archivo.endswith(".txt"):
        mensaje = f"REGLA SEMANTICA 010: El archivo '{archivo}' tiene una extensión válida (.txt)."
        historialSemantico.agregar(mensaje)
        return True
    else:
        mensaje = f"REGLA SEMANTICA 010: El archivo '{archivo}' NO tiene extensión .txt."
        historialSemanticoNegativo.agregar(mensaje)
        historialSemantico.agregar(mensaje)
        return False
