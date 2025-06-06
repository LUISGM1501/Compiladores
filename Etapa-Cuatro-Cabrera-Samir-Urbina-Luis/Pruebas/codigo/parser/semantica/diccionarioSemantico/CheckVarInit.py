from ..HistorialSemantico import historialSemantico  # Si usas historial
from ..HistorialSemanticoNegativo import historialSemanticoNegativo

def checkInicializacionVariable(simbolo):
    """
    Regla Semántica 012: Verifica si una variable está siendo inicializada.
    """
    if simbolo.valor is None or simbolo.valor == "" or simbolo.valor == []:
        mensaje = (
            f"REGLA SEMANTICA 012: La variable '{simbolo.nombre}' (tipo: {simbolo.tipo}) "
            f"fue declarada pero NO ha sido inicializada. Línea: {simbolo.linea}, Columna: {simbolo.columna}."
        )
        historialSemanticoNegativo.agregar(mensaje)
    else:
        mensaje = (
            f"REGLA SEMANTICA 012: La variable '{simbolo.nombre}' (tipo: {simbolo.tipo}) "
            f"ha sido correctamente inicializada con el valor '{simbolo.valor}'. "
            f"Línea: {simbolo.linea}, Columna: {simbolo.columna}."
        )

    print(mensaje)
    historialSemantico.agregar(mensaje)  # Si estás registrando
