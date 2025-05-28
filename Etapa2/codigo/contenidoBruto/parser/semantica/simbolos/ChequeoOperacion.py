def chequear_tipos_expresion(self, operador, tipo_izq, tipo_der):
    """Verifica compatibilidad de tipos en una operación binaria"""
    if operador in ['+', '-', '*', '/']:
        if tipo_izq not in ['int', 'float'] or tipo_der not in ['int', 'float']:
            self.reportar_error_semantico(f"Operación {operador} no válida entre {tipo_izq} y {tipo_der}")
    elif operador in ['&&', '||']:
        if tipo_izq != 'bool' or tipo_der != 'bool':
            self.reportar_error_semantico(f"Operación lógica {operador} requiere operandos booleanos")