def chequear_tipos_expresion(tipo_esperado, valor):
    """Verifica que un valor o conjunto de valores sea compatible con el tipo esperado
    
    Args:
        tipo_esperado (str): Tipo esperado (Stack, Rune, Spider, Torch, Ghast)
        valor: Valor individual o lista de valores a verificar
    
    Returns:
        Valor o lista de valores convertidos al tipo esperado, o valores por defecto si hay error
    """
    # Mapeo de tipos con sus propiedades
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

    # Función interna para verificar un ítem individual
    def verificar_item(item):
        tipo_info = tipos.get(tipo_esperado)
        if not tipo_info:
            print(f"Tipo desconocido: {tipo_esperado}")
            return item  # Retorna el valor original si el tipo es desconocido

        # Intentar conversión según el tipo esperado
        try:
            if tipo_esperado == 'STACK':
                if isinstance(item, bool):
                    return int(item)
                if isinstance(item, (int, float)):
                    return int(item)
                if isinstance(item, str):
                    if item.lower() in ('on', 'off'):
                        return 1 if item.lower() == 'on' else 0
                    return int(float(item))  # Para manejar strings numéricos
                
            elif tipo_esperado == 'GHAST':
                if isinstance(item, bool):
                    return float(item)
                if isinstance(item, (int, float)):
                    return float(item)
                if isinstance(item, str):
                    if item.lower() in ('on', 'off'):
                        return 1.0 if item.lower() == 'on' else 0.0
                    return float(item)
                
            elif tipo_esperado == 'TORCH':
                if isinstance(item, str):
                    if item.lower() in ('on', 'off', 'true', 'false', '1', '0'):
                        return 'On' if item.lower() in ('on', 'true', '1') else 'Off'
                if isinstance(item, (int, float)):
                    return 'On' if item != 0 else 'Off'
                if isinstance(item, bool):
                    return 'On' if item else 'Off'
                
            elif tipo_esperado == 'SPIDER':
                return str(item)
                
            elif tipo_esperado == 'RUNE':
                s = str(item)
                return s[0] if len(s) > 0 else '\0'
                
        except (ValueError, TypeError):
            pass  # Más abajo se maneja el error

        # Si llegamos aquí es porque no se pudo convertir
        print(f"\n\n ERROR SEMANTICO: Variable de tipo {tipo_esperado} recibió un valor incompatible: {item}")
        return tipo_info['default']

    # Procesar valor individual o lista
    if isinstance(valor, list):
        return [verificar_item(item) for item in valor]
    return verificar_item(valor)