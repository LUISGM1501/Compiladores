# HistorialSemantico.py

class HistorialSemanticoSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(HistorialSemanticoSingleton, cls).__new__(cls)
            cls._instance._historial = []  # ⚠️ Instancia, no clase
        return cls._instance

    def agregar(self, elemento):
        self._historial.append(elemento)

    def obtener(self):
        return self._historial

    def limpiar(self):
        self._historial.clear()

    def imprimir_historial(self):
        print("\nHistorial Semántico:\n" + "-" * 40)
        for i, entrada in enumerate(self.obtener(), 1):
            print(f"{i:02d}. {entrada}")
        print("-" * 40 + "\n")

# Alias para uso directo
historialSemantico = HistorialSemanticoSingleton()
