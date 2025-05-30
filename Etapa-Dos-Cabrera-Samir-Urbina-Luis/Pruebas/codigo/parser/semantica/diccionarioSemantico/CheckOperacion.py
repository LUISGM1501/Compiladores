from ..HistorialSemantico import historialSemantico

def chequear_tipos_expresion(tipo_esperado, valor):
    """Verifica que un valor o conjunto de valores sea compatible con el tipo esperado

    Args:
        tipo_esperado (str): Tipo esperado (Stack, Rune, Spider, Torch, Ghast)
        valor: Valor individual o lista de valores a verificar

    Returns:
        Valor o lista de valores convertidos al tipo esperado, o valores por defecto si hay error
    """
    tipos = {
        'STACK': {
            'tipo_base': 'int',
            'default': 0,
            'alias': ['int', 'entero']
        },
        'GHAST': {
            'tipo_base': 'float',
            'default': 0.0,
            'alias': ['float', 'flotante']
        },
        'TORCH': {
            'tipo_base': 'bool',
            'default': 'On',
            'alias': ['bool', 'boolean']
        },
        'SPIDER': {
            'tipo_base': 'str',
            'default': '',
            'alias': ['str', 'string']
        },
        'RUNE': {
            'tipo_base': 'char',
            'default': '\0',
            'alias': ['char', 'character']
        }
    }

    def verificar_item(item):
        tipo_info = tipos.get(tipo_esperado)
        if not tipo_info:
            mensaje = f"REGLA SEMANTICA 000: Tipo desconocido '{tipo_esperado}' para el valor '{item}'"
            historialSemantico.agregar(mensaje)
            return item  # Tipo no reconocido

        try:
            if tipo_esperado == 'STACK':
                if isinstance(item, bool):
                    resultado = int(item)
                    mensaje = f"REGLA SEMANTICA 000: Valor '{item}' (bool) convertido a STACK → {resultado}"
                    historialSemantico.agregar(mensaje)
                    return resultado
                if isinstance(item, (int, float)):
                    resultado = int(item)
                    mensaje = f"REGLA SEMANTICA 000: Valor '{item}' ({type(item).__name__}) convertido a STACK → {resultado}"
                    historialSemantico.agregar(mensaje)
                    return resultado
                if isinstance(item, str):
                    if item.lower() in ('on', 'off'):
                        resultado = 1 if item.lower() == 'on' else 0
                        mensaje = f"REGLA SEMANTICA 000: Valor '{item}' (str) interpretado como booleano para STACK → {resultado}"
                        historialSemantico.agregar(mensaje)
                        return resultado
                    resultado = int(float(item))
                    mensaje = f"REGLA SEMANTICA 000: Valor '{item}' (str) convertido a STACK → {resultado}"
                    historialSemantico.agregar(mensaje)
                    return resultado

            elif tipo_esperado == 'GHAST':
                if isinstance(item, bool):
                    resultado = float(item)
                    mensaje = f"REGLA SEMANTICA 000: Valor '{item}' (bool) convertido a GHAST → {resultado}"
                    historialSemantico.agregar(mensaje)
                    return resultado
                if isinstance(item, (int, float)):
                    resultado = float(item)
                    mensaje = f"REGLA SEMANTICA 000: Valor '{item}' ({type(item).__name__}) convertido a GHAST → {resultado}"
                    historialSemantico.agregar(mensaje)
                    return resultado
                if isinstance(item, str):
                    if item.lower() in ('on', 'off'):
                        resultado = 1.0 if item.lower() == 'on' else 0.0
                        mensaje = f"REGLA SEMANTICA 000: Valor '{item}' (str) interpretado como booleano para GHAST → {resultado}"
                        historialSemantico.agregar(mensaje)
                        return resultado
                    resultado = float(item)
                    mensaje = f"REGLA SEMANTICA 000: Valor '{item}' (str) convertido a GHAST → {resultado}"
                    historialSemantico.agregar(mensaje)
                    return resultado

            elif tipo_esperado == 'TORCH':
                if isinstance(item, str):
                    if item.lower() in ('on', 'off', 'true', 'false', '1', '0'):
                        resultado = 'On' if item.lower() in ('on', 'true', '1') else 'Off'
                        mensaje = f"REGLA SEMANTICA 000: Valor '{item}' (str) convertido a TORCH → {resultado}"
                        historialSemantico.agregar(mensaje)
                        return resultado
                if isinstance(item, (int, float)):
                    resultado = 'On' if item != 0 else 'Off'
                    mensaje = f"REGLA SEMANTICA 000: Valor '{item}' ({type(item).__name__}) convertido a TORCH → {resultado}"
                    historialSemantico.agregar(mensaje)
                    return resultado
                if isinstance(item, bool):
                    resultado = 'On' if item else 'Off'
                    mensaje = f"REGLA SEMANTICA 000: Valor '{item}' (bool) convertido a TORCH → {resultado}"
                    historialSemantico.agregar(mensaje)
                    return resultado

            elif tipo_esperado == 'SPIDER':
                resultado = str(item)
                mensaje = f"REGLA SEMANTICA 000: Valor '{item}' convertido a SPIDER → '{resultado}'"
                historialSemantico.agregar(mensaje)
                return resultado

            elif tipo_esperado == 'RUNE':
                s = str(item)
                resultado = s[0] if len(s) > 0 else '\0'
                mensaje = f"REGLA SEMANTICA 000: Valor '{item}' convertido a RUNE → '{resultado}'"
                historialSemantico.agregar(mensaje)
                return resultado

        except (ValueError, TypeError):
            pass  # Manejo de error abajo

        # Fallo de conversión
        mensaje = (f"REGLA SEMANTICA 000: ERROR al convertir '{item}' al tipo '{tipo_esperado}', "
                   f"se asigna valor por defecto: {tipo_info['default']}")
        historialSemantico.agregar(mensaje)
        return tipo_info['default']

    if isinstance(valor, list):
        return [verificar_item(item) for item in valor]
    return verificar_item(valor)
