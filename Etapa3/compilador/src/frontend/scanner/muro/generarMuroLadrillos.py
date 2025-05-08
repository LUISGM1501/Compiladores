#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador de muro de ladrillos HTML para visualización de tokens
"""

def generarLadrillos(contenido, estadisticaToken, lineasPrograma, numeroCaracteresEntrada, 
                    numeroComentariosLinea, numeroComentariosBloque, cantidadErrores):
    """
    Genera un archivo HTML con un muro de ladrillos de colores y estadísticas del análisis léxico.
    
    Args:
        contenido (list): Lista de strings con los lexemas a mostrar en ladrillos
        estadisticaToken (dict): Diccionario con estadísticas por familia de tokens
        lineasPrograma (int): Número de líneas del programa analizado
        numeroCaracteresEntrada (int): Número de caracteres del archivo de entrada
        numeroComentariosLinea (int): Cantidad de comentarios de línea
        numeroComentariosBloque (int): Cantidad de comentarios de bloque
        cantidadErrores (int): Cantidad de errores detectados
    """
    
    # Paleta de colores para los ladrillos (15 colores distintos)
    colores = [
        "#FF6B6B", "#4ECDC4", "#45B7D1", "#FFBE0B", "#FB5607",
        "#8338EC", "#3A86FF", "#FF006E", "#A5DD9B", "#F9C74F",
        "#90BE6D", "#43AA8B", "#577590", "#F94144", "#F3722C"
    ]
    
    # Color especial para errores
    color_error = "#FF0000"
    
    # Clasificar ciertos tipos de tokens para asignarles colores consistentes
    tipos_lexema = {
        # Palabras clave de estructura
        "WorldName": 0, "Bedrock": 0, "ResourcePack": 0, "Inventory": 0, 
        "Recipe": 0, "CraftingTable": 0, "SpawnPoint": 0, "worldSave": 0,
        
        # Tipos de datos
        "Stack": 1, "Rune": 1, "Spider": 1, "Torch": 1, "Chest": 1,
        "Book": 1, "Ghast": 1, "Shelf": 1, "Entity": 1,
        
        # Delimitadores de bloques
        "PolloCrudo": 2, "PolloAsado": 2,
        
        # Palabras clave de control
        "repeater": 3, "craft": 3, "target": 3, "hit": 3, "miss": 3,
        "jukebox": 3, "disc": 3, "silence": 3, "spawner": 3, "exhausted": 3,
        "walk": 3, "set": 3, "to": 3, "step": 3, "wither": 3,
        
        # Literales booleanas
        "On": 4, "Off": 4,
        
        # Declaraciones
        "Obsidian": 5, "Anvil": 5,
        
        # Funciones y procedimientos
        "Spell": 6, "Ritual": 6, "respawn": 6,
        
        # Operadores aritméticos
        "+": 7, "-": 7, "*": 7, "/": 7, "//": 7, "%": 7,
        "+=": 7, "-=": 7, "*=": 7, "/=": 7, "%=": 7,
        
        # Operadores de comparación
        "<": 8, ">": 8, "<=": 8, ">=": 8, "is": 8, "isNot": 8,
        
        # Delimitadores
        ";": 9, ",": 9, ".": 9, ":": 9, "(": 9, ")": 9, "[": 9, "]": 9, 
        "{": 9, "}": 9, "{:": 9, ":}": 9, "{/": 9, "/}": 9,
        
        # Operadores especiales
        "soulsand": 10, "magma": 10, "bind": 10, "#": 10, "chunk": 10,
        
        # Funciones de E/S
        "hopper": 11, "dropper": 11,
        
        # Funciones de float
        ":+": 12, ":-": 12, ":*": 12, "://": 12, ":%": 12,
        
        # Acceso a datos
        "@": 13, "->": 13, ">>": 13
    }
    
    # Generar los ladrillos con colores
    ladrillos_html = []
    
    for lexema in contenido:
        # Eliminar espacios al inicio y fin
        lexema_strip = lexema.strip()
        if not lexema_strip:
            continue
        
        # Determinar color basado en el tipo de lexema
        color_idx = 14  # Color por defecto
        
        # Buscar coincidencias parciales para tipos conocidos
        for tipo, idx in tipos_lexema.items():
            if lexema_strip == tipo or lexema_strip.startswith(tipo):
                color_idx = idx
                break
        
        # Verificar si parece un identificador (empieza con letra minúscula o _)
        if (lexema_strip[0].islower() or lexema_strip[0] == '_') and lexema_strip.isalnum():
            color_idx = 14
        
        # Verificar si parece un literal numérico
        if lexema_strip[0].isdigit() or (lexema_strip[0] == '-' and len(lexema_strip) > 1 and lexema_strip[1].isdigit()):
            color_idx = 13
        
        # Verificar si parece un literal de cadena
        if (lexema_strip.startswith('"') and lexema_strip.endswith('"')) or \
           (lexema_strip.startswith("'") and lexema_strip.endswith("'")):
            color_idx = 12
        
        # Seleccionar color
        color = colores[color_idx]
        
        # Escapar caracteres especiales para HTML
        lexema_escaped = lexema_strip.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        
        # Crear el ladrillo HTML
        ladrillo = f'<div class="ladrillo" style="background-color: {color}">{lexema_escaped}</div>'
        ladrillos_html.append(ladrillo)
    
    # Generar las estadísticas de familias de tokens (solo las que tienen count > 0)
    stats_tokens = []
    for familia, count in estadisticaToken.items():
        if count > 0:
            stats_tokens.append(f"<li>{familia}: {count}</li>")
    
    # Generar las otras estadísticas (solo si son > 0)
    otras_stats = []
    if lineasPrograma > 0:
        otras_stats.append(f"<li>Número de líneas del programa: {lineasPrograma}</li>")
    if numeroCaracteresEntrada > 0:
        otras_stats.append(f"<li>Número de caracteres del archivo: {numeroCaracteresEntrada}</li>")
    if numeroComentariosLinea > 0:
        otras_stats.append(f"<li>Comentarios de línea: {numeroComentariosLinea}</li>")
    if numeroComentariosBloque > 0:
        otras_stats.append(f"<li>Comentarios de bloque: {numeroComentariosBloque}</li>")
    if cantidadErrores > 0:
        otras_stats.append(f"<li>Errores detectados: {cantidadErrores}</li>")
    
    # Plantilla HTML mejorada
    html_template = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Análisis Léxico - Notch Engine</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f5f5f5;
            color: #333;
        }}
        header {{
            background-color: #2c3e50;
            color: white;
            padding: 20px;
            text-align: center;
            margin-bottom: 30px;
        }}
        h1 {{
            margin: 0;
            font-size: 2em;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
        }}
        h2 {{
            color: #2c3e50;
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
            margin-top: 40px;
        }}
        .muro {{
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-bottom: 30px;
            background-color: #34495e;
            padding: 20px;
            border-radius: 8px;
        }}
        .ladrillo {{
            display: inline-block;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            padding: 8px 12px;
            border-radius: 4px;
            color: white;
            font-weight: bold;
            box-shadow: 0 2px 4px rgba(0,0,0,0.2);
            text-align: center;
            max-width: 150px;
            min-width: 50px;
            margin: 4px;
            transition: all 0.3s ease;
        }}
        .ladrillo:hover {{
            transform: translateY(-3px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.3);
            z-index: 10;
            max-width: none;
        }}
        .stats-container {{
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }}
        .stats-list {{
            columns: 2;
            column-gap: 40px;
            list-style-type: none;
            padding: 0;
        }}
        .stats-list li {{
            margin-bottom: 10px;
            padding: 8px;
            background-color: #f8f9fa;
            border-radius: 4px;
        }}
        .error-info {{
            background-color: #ffebee;
            border-left: 4px solid #f44336;
            padding: 15px;
            margin-bottom: 20px;
            border-radius: 4px;
        }}
        footer {{
            background-color: #2c3e50;
            color: white;
            text-align: center;
            padding: 15px;
            margin-top: 50px;
        }}
        @media (max-width: 768px) {{
            .stats-list {{
                columns: 1;
            }}
            .ladrillo {{
                min-width: 30px;
                font-size: 0.9em;
            }}
        }}
    </style>
</head>
<body>
    <header>
        <h1>Análisis Léxico - Notch Engine</h1>
    </header>
    
    <div class="container">
        {f'<div class="error-info"><strong>¡Atención!</strong> Se encontraron {cantidadErrores} errores léxicos en el código.</div>' if cantidadErrores > 0 else ''}
        
        <h2>Muro de Ladrillos</h2>
        <p>Cada ladrillo representa un token reconocido por el analizador léxico. Los colores indican diferentes tipos de tokens.</p>
        <div class="muro">
            {"".join(ladrillos_html)}
        </div>
        
        <h2>Estadísticas de Tokens</h2>
        <div class="stats-container">
            <ul class="stats-list">
                {"".join(stats_tokens)}
            </ul>
        </div>
        
        <h2>Información del Análisis</h2>
        <div class="stats-container">
            <ul class="stats-list">
                {"".join(otras_stats)}
            </ul>
        </div>
    </div>
    
    <footer>
        <p>Notch Engine Scanner - Analizador Léxico</p>
    </footer>
</body>
</html>
    """
    
    # Guardar el archivo HTML
    with open("analisis_lexico.html", "w", encoding="utf-8") as f:
        f.write(html_template)
    
    print("Archivo HTML generado exitosamente: analisis_lexico.html")