"""
Token Cleaner para Notch Engine

Estudiantes: Cabrera Samir y Urbina Luis

Archivo: token_cleaner.py

Breve Descripcion: Limpieza de tokens para compatibilidad entre scanner y parser.
Convierte secuencias de tokens en operadores flotantes y corrige inconsistencias.
"""

from scanner.tokens import Token

def limpiar_tokens_para_parser(tokens):
    """
    Convierte secuencias DOS_PUNTOS+OPERADOR en tokens flotantes
    y BARRA en DIVISION para compatibilidad con la gramática
    
    Args:
        tokens: Lista de tokens original del scanner
        
    Returns:
        Lista de tokens modificada para compatibilidad con el parser
    """
    tokens_limpios = []
    i = 0
    
    while i < len(tokens):
        token = tokens[i]
        
        # MAQUILLAJE 1: Detectar secuencias flotantes DOS_PUNTOS + OPERADOR
        if (token.type == "DOS_PUNTOS" and 
            i + 1 < len(tokens)):
            
            next_token = tokens[i + 1]
            
            # Mapeo de operadores flotantes
            operadores_flotantes = {
                "SUMA": ("SUMA_FLOTANTE", ":+"),
                "RESTA": ("RESTA_FLOTANTE", ":-"),
                "MULTIPLICACION": ("MULTIPLICACION_FLOTANTE", ":*"),
                "DIVISION": ("DIVISION_FLOTANTE", ":/"),
                "BARRA": ("DIVISION_FLOTANTE", ":/"),  # Por si DIVISION está como BARRA
                "MODULO": ("MODULO_FLOTANTE", ":%")
            }
            
            if next_token.type in operadores_flotantes:
                nuevo_tipo, nuevo_lexema = operadores_flotantes[next_token.type]
                
                # Crear token flotante artificial combinando ambos
                nuevo_token = Token(
                    type=nuevo_tipo,
                    lexema=nuevo_lexema,
                    linea=token.linea,
                    columna=token.columna
                )
                tokens_limpios.append(nuevo_token)
                i += 2  # Saltar ambos tokens (DOS_PUNTOS y OPERADOR)
                continue
        
        # MAQUILLAJE 2: Convertir BARRA a DIVISION (para división regular)
        if token.type == "BARRA":
            nuevo_token = Token(
                type="DIVISION",
                lexema="/",
                linea=token.linea,
                columna=token.columna
            )
            tokens_limpios.append(nuevo_token)
        
        # MAQUILLAJE 3: Detectar secuencias de asignación flotante (:+=, :-=, etc.)
        elif (token.type in ["SUMA_IGUAL", "RESTA_IGUAL", "MULTIPLICACION_IGUAL", "DIVISION_IGUAL", "MODULO_IGUAL"] and
              i > 0 and 
              i - 1 >= 0 and
              tokens[i-1].type == "DOS_PUNTOS"):
            
            # Si el token anterior era DOS_PUNTOS, convertir a versión flotante
            asignacion_flotante = {
                "SUMA_IGUAL": "SUMA_FLOTANTE_IGUAL",
                "RESTA_IGUAL": "RESTA_FLOTANTE_IGUAL", 
                "MULTIPLICACION_IGUAL": "MULTIPLICACION_FLOTANTE_IGUAL",
                "DIVISION_IGUAL": "DIVISION_FLOTANTE_IGUAL",
                "MODULO_IGUAL": "MODULO_FLOTANTE_IGUAL"
            }
            
            if token.type in asignacion_flotante:
                # Remover el DOS_PUNTOS anterior que ya fue agregado
                if tokens_limpios and tokens_limpios[-1].type == "DOS_PUNTOS":
                    tokens_limpios.pop()
                
                # Crear token de asignación flotante
                nuevo_lexema = ":" + token.lexema  # :+=, :-=, etc.
                nuevo_token = Token(
                    type=asignacion_flotante[token.type],
                    lexema=nuevo_lexema,
                    linea=token.linea,
                    columna=token.columna
                )
                tokens_limpios.append(nuevo_token)
            else:
                tokens_limpios.append(token)
        
        # MAQUILLAJE 4: Manejo especial de identificadores que podrían ser palabras clave
        elif token.type == "IDENTIFICADOR":
            # Casos especiales como "pollocrudo", "polloasado", etc.
            lexema_lower = token.lexema.lower()
            
            mapeo_especial = {
                "pollocrudo": "POLLO_CRUDO",
                "polloasado": "POLLO_ASADO", 
                "worldsave": "WORLD_SAVE",
                "worldname": "WORLD_NAME",
                "resourcepack": "RESOURCE_PACK",
                "craftingtable": "CRAFTING_TABLE",
                "spawnpoint": "SPAWN_POINT"
            }
            
            if lexema_lower in mapeo_especial:
                nuevo_token = Token(
                    type=mapeo_especial[lexema_lower],
                    lexema=token.lexema,  # Mantener lexema original
                    linea=token.linea,
                    columna=token.columna
                )
                tokens_limpios.append(nuevo_token)
            else:
                tokens_limpios.append(token)
        
        # MAQUILLAJE 5: Casos especiales para mejorar compatibilidad
        elif token.type == "COMENTARIO":
            # Mantener comentarios (el parser los filtra)
            tokens_limpios.append(token)
        
        # Para todos los demás tokens, mantener como están
        else:
            tokens_limpios.append(token)
        
        i += 1
    
    return tokens_limpios

def mostrar_cambios_tokens(tokens_originales, tokens_limpios, mostrar_detalle=True):
    """
    Muestra qué cambios se realizaron en los tokens para debugging
    
    Args:
        tokens_originales: Lista de tokens original
        tokens_limpios: Lista de tokens después de la limpieza
        mostrar_detalle: Si True, muestra cada cambio individual
    """
    print("\n" + "="*60)
    print("              REPORTE DE LIMPIEZA DE TOKENS")
    print("="*60)
    
    cambios = []
    pos_original = 0
    pos_limpio = 0
    
    while pos_original < len(tokens_originales) and pos_limpio < len(tokens_limpios):
        token_orig = tokens_originales[pos_original]
        token_limpio = tokens_limpios[pos_limpio]
        
        # Detectar cambios
        if token_orig.type != token_limpio.type or token_orig.lexema != token_limpio.lexema:
            
            # Verificar si es una combinación (DOS_PUNTOS + OPERADOR -> FLOTANTE)
            if (pos_original + 1 < len(tokens_originales) and
                token_orig.type == "DOS_PUNTOS" and
                tokens_originales[pos_original + 1].type in ["SUMA", "RESTA", "MULTIPLICACION", "DIVISION", "BARRA", "MODULO"] and
                "FLOTANTE" in token_limpio.type):
                
                cambios.append({
                    "tipo": "COMBINACION",
                    "original": f"'{token_orig.lexema}' + '{tokens_originales[pos_original + 1].lexema}'",
                    "nuevo": f"'{token_limpio.lexema}' ({token_limpio.type})",
                    "linea": token_orig.linea
                })
                pos_original += 2  # Saltar ambos tokens originales
                pos_limpio += 1
                continue
            
            # Cambio simple
            elif token_orig.type == "BARRA" and token_limpio.type == "DIVISION":
                cambios.append({
                    "tipo": "CONVERSION",
                    "original": f"'{token_orig.lexema}' (BARRA)",
                    "nuevo": f"'{token_limpio.lexema}' (DIVISION)",
                    "linea": token_orig.linea
                })
            
            elif token_orig.type == "IDENTIFICADOR" and token_limpio.type != "IDENTIFICADOR":
                cambios.append({
                    "tipo": "PALABRA_CLAVE",
                    "original": f"'{token_orig.lexema}' (IDENTIFICADOR)",
                    "nuevo": f"'{token_limpio.lexema}' ({token_limpio.type})",
                    "linea": token_orig.linea
                })
            
            else:
                cambios.append({
                    "tipo": "OTRO",
                    "original": f"'{token_orig.lexema}' ({token_orig.type})",
                    "nuevo": f"'{token_limpio.lexema}' ({token_limpio.type})",
                    "linea": token_orig.linea
                })
        
        pos_original += 1
        pos_limpio += 1
    
    # Mostrar resumen
    print(f"Tokens originales: {len(tokens_originales)}")
    print(f"Tokens después de limpieza: {len(tokens_limpios)}")
    print(f"Cambios realizados: {len(cambios)}")
    
    if len(cambios) == 0:
        print("\n✅ No se realizaron cambios en los tokens")
    else:
        print(f"\n🔧 Se realizaron {len(cambios)} cambios:")
        
        # Agrupar por tipo
        tipos_cambios = {}
        for cambio in cambios:
            tipo = cambio["tipo"]
            if tipo not in tipos_cambios:
                tipos_cambios[tipo] = 0
            tipos_cambios[tipo] += 1
        
        for tipo, cantidad in tipos_cambios.items():
            print(f"   - {tipo}: {cantidad} cambios")
        
        if mostrar_detalle:
            print("\n📋 Detalle de cambios:")
            for i, cambio in enumerate(cambios, 1):
                print(f"   {i:2d}. [{cambio['tipo']}] Línea {cambio['linea']}: {cambio['original']} → {cambio['nuevo']}")
    
    print("="*60 + "\n")

def validar_tokens_limpios(tokens_limpios):
    """
    Valida que los tokens limpiados no tengan problemas obvios
    
    Args:
        tokens_limpios: Lista de tokens después de la limpieza
        
    Returns:
        tuple: (es_valido, lista_problemas)
    """
    problemas = []
    
    # Verificar tokens consecutivos problemáticos
    for i in range(len(tokens_limpios) - 1):
        token_actual = tokens_limpios[i]
        token_siguiente = tokens_limpios[i + 1]
        
        # Verificar secuencias que podrían causar problemas
        if (token_actual.type == "DOS_PUNTOS" and 
            token_siguiente.type in ["SUMA", "RESTA", "MULTIPLICACION", "DIVISION", "MODULO"]):
            problemas.append(f"Línea {token_actual.linea}: Secuencia DOS_PUNTOS + {token_siguiente.type} no fue convertida a operador flotante")
        
        if token_actual.type == "BARRA":
            problemas.append(f"Línea {token_actual.linea}: Token BARRA no fue convertido a DIVISION")
    
    # Verificar tokens especiales
    tokens_especiales = ["SUMA_FLOTANTE", "RESTA_FLOTANTE", "MULTIPLICACION_FLOTANTE", "DIVISION_FLOTANTE", "MODULO_FLOTANTE"]
    tokens_flotantes_encontrados = sum(1 for token in tokens_limpios if token.type in tokens_especiales)
    
    return len(problemas) == 0, problemas

def debug_tokens_para_parser(tokens_originales, tokens_limpios):
    """
    Función de debug completa que muestra toda la información útil
    """
    print("\n" + "🔍" + " DEBUG DE LIMPIEZA DE TOKENS " + "🔍")
    
    # Mostrar cambios
    mostrar_cambios_tokens(tokens_originales, tokens_limpios, mostrar_detalle=True)
    
    # Validar resultado
    es_valido, problemas = validar_tokens_limpios(tokens_limpios)
    
    if es_valido:
        print(" Validación: Tokens limpiados correctamente")
    else:
        print(" Validación: Se encontraron problemas:")
        for problema in problemas:
            print(f"   - {problema}")
    
    # Mostrar algunos tokens de ejemplo
    print("\n📋 Primeros 10 tokens limpiados:")
    for i, token in enumerate(tokens_limpios[:10]):
        print(f"   {i:2d}. {token.type} → '{token.lexema}' (L{token.linea}:C{token.columna})")
    
    if len(tokens_limpios) > 10:
        print(f"   ... y {len(tokens_limpios) - 10} tokens más")