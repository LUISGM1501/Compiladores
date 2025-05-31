# parser/semantica/ScopeManager.py

class ScopeManager:
    """
    Gestor de scopes para manejar variables locales y globales
    """
    
    def __init__(self):
        self.scopes = []  # Pila de scopes
        self.current_function = None  # Función actual
        
    def enter_global_scope(self):
        """Entra al scope global"""
        self.scopes = [{"type": "GLOBAL", "variables": {}, "function": None}]
        print("  [SCOPE] Entrando a scope GLOBAL")
        
    def enter_function_scope(self, function_name, parametros):
        """Entra a un scope de función/procedimiento"""
        scope = {
            "type": "FUNCTION",
            "function": function_name,
            "variables": {},
            "parametros": {param["nombre"]: param for param in parametros}
        }
        self.scopes.append(scope)
        self.current_function = function_name
        print(f"  [SCOPE] Entrando a función: {function_name}")
        
    def exit_function_scope(self):
        """Sale del scope de función actual"""
        if len(self.scopes) > 1:
            function_name = self.scopes[-1].get("function", "unknown")
            self.scopes.pop()
            self.current_function = self.scopes[-1].get("function") if self.scopes else None
            print(f"  [SCOPE] Saliendo de función: {function_name}")
            
    def declare_variable(self, nombre, tipo, categoria, valor=None):
        """Declara una variable en el scope actual"""
        if not self.scopes:
            raise Exception("No hay scope activo")
            
        current_scope = self.scopes[-1]
        
        # Verificar que no exista en el scope actual
        if nombre in current_scope["variables"]:
            raise ValueError(f"Variable '{nombre}' ya declarada en scope actual")
            
        # Verificar que no sea un parámetro (si estamos en función)
        if "parametros" in current_scope and nombre in current_scope["parametros"]:
            raise ValueError(f"'{nombre}' ya está declarado como parámetro")
            
        current_scope["variables"][nombre] = {
            "nombre": nombre,
            "tipo": tipo,
            "categoria": categoria,
            "valor": valor,
            "scope": current_scope["type"]
        }
        print(f"  [SCOPE] Variable '{nombre}' declarada en scope {current_scope['type']}")
        
    def lookup_variable(self, nombre):
        """Busca una variable en todos los scopes (desde el más local al más global)"""
        # Buscar en scopes desde el más interno al más externo
        for scope in reversed(self.scopes):
            # Buscar en variables del scope
            if nombre in scope["variables"]:
                return scope["variables"][nombre]
                
            # Buscar en parámetros si es un scope de función
            if "parametros" in scope and nombre in scope["parametros"]:
                param = scope["parametros"][nombre]
                return {
                    "nombre": param["nombre"],
                    "tipo": param["tipo"],
                    "categoria": "PARAMETRO",
                    "valor": None,
                    "scope": "FUNCTION"
                }
                
        return None
        
    def is_in_function(self):
        """Verifica si estamos dentro de una función"""
        return len(self.scopes) > 1 and self.scopes[-1]["type"] == "FUNCTION"
        
    def get_current_function(self):
        """Obtiene el nombre de la función actual"""
        return self.current_function

# Singleton para el gestor de scopes
_scope_manager_instance = None

def get_scope_manager():
    """Obtiene la instancia singleton del gestor de scopes"""
    global _scope_manager_instance
    if _scope_manager_instance is None:
        _scope_manager_instance = ScopeManager()
        _scope_manager_instance.enter_global_scope()  # Inicializar con scope global
    return _scope_manager_instance