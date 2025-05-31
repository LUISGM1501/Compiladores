# HistorialSemantico.py

class HistorialSemanticoNegativoSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(HistorialSemanticoNegativoSingleton, cls).__new__(cls)
            cls._instance._historialnegativo = []  # ⚠️ Instancia, no clase
        return cls._instance

    def agregar(self, elemento):
        self._historialnegativo.append(elemento)

    def obtener(self):
        return self._historialnegativo

    def limpiar(self):
        self._historialnegativo.clear()

    def imprimir_historial(self):
        print("\nHistorial Semántico:\n" + "-" * 40)
        for i, entrada in enumerate(self.obtener(), 1):
            print(f"{i:02d}. {entrada}")
        print("-" * 40 + "\n")

# Alias para uso directo
historialSemanticoNegativo = HistorialSemanticoNegativoSingleton()
