class TablaSimbolos:
    _instancia = None  # Atributo de clase para almacenar la única instancia

    def __init__(self, tamaño=101):
        if TablaSimbolos._instancia is not None:
            raise Exception("Usa TablaSimbolos.instancia() para obtener la instancia.")
        self.tamaño = tamaño
        self.tabla = [[] for _ in range(tamaño)]

    @classmethod
    def instancia(cls):
        if cls._instancia is None:
            cls._instancia = TablaSimbolos()
        return cls._instancia

    def _hash(self, nombre):
        return sum(ord(c) * (i + 1) for i, c in enumerate(nombre)) % self.tamaño

    def insertar(self, simbolo):
        idx = self._hash(simbolo.nombre)
        for sym in self.tabla[idx]:
            if sym.nombre == simbolo.nombre:
                raise ValueError(f"Identificador '{simbolo.nombre}' ya declarado")
        self.tabla[idx].append(simbolo)

    def buscar(self, nombre):
        idx = self._hash(nombre)
        for sym in self.tabla[idx]:
            if sym.nombre == nombre:
                return sym
        return None

    def eliminar(self, nombre):
        idx = self._hash(nombre)
        self.tabla[idx] = [sym for sym in self.tabla[idx] if sym.nombre != nombre]
