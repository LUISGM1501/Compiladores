# verificador_uso_variables.py

from ..HistorialSemanticoNegativo import HistorialSemanticoNegativoSingleton
from ..HistorialSemantico import historialSemantico


class VerificadorUsoVariables:
    def __init__(self):
        # Diccionario: clave = nombre de variable, valor = contador de usos
        self.uso_variables = {}

    def registrar_declaracion(self, nombre_variable):
        if nombre_variable not in self.uso_variables:
            self.uso_variables[nombre_variable] = 0
            mensaje = f"REGLA SEMANTICA 007: Variable '{nombre_variable}' declarada, contador inicializado en 0."
            historialSemantico.agregar(mensaje)

    def registrar_uso(self, nombre_variable):
        if nombre_variable in self.uso_variables:
            self.uso_variables[nombre_variable] += 1
            mensaje=f"REGLA SEMANTICA 007: Variable '{nombre_variable}' utilizada, contador actualizado a {self.uso_variables[nombre_variable]}."
            historialSemantico.agregar(mensaje)
        else:
            mensaje = f"[AVISO] Variable '{nombre_variable}' usada sin haber sido declarada explícitamente para el contador de uso."
            historialSemantico.agregar(mensaje)

    def verificar_variables_no_usadas(self):
        historial = HistorialSemanticoNegativoSingleton()
        for nombre, contador in self.uso_variables.items():
            if contador == 0:
                mensaje = f"REGLA SEMANTICA 007: La variable '{nombre}' fue declarada pero nunca utilizada."
                print(mensaje)
                historial.agregar(mensaje)

# Instancia global para usar desde otros módulos
verificador_uso_variables = VerificadorUsoVariables()
