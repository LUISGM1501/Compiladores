"""
Compilador Notch Engine

Estudiantes: Cabrera Samir y Urbina Luis

Archivo: generarMuroLadrillos.py

Breve Descripcion: Encargado de generar el muro de ladrillos
con los lexemas del programa. 
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
    
    # Generar los ladrillos con colores cíclicos
    ladrillos_html = []
    for i, lexema in enumerate(contenido):
        print("CONTENIDO DEL LADRILLO: ",lexema)
        color = colores[i % len(colores)]
        # Escapar caracteres especiales para HTML
        lexema_escaped = lexema.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
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
    
    # Plantilla HTML completa
    html_template = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Análisis Léxico - Resultados</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        h1, h2 {{
            color: #333;
        }}
        .muro {{
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-bottom: 30px;
        }}
        .ladrillo {{
            white-space: nowrap;  /* Evita que el texto se divida */
            word-break: keep-all; /* Mantiene las palabras completas */
            padding: 8px 12px;
            margin: 2px;
            border-radius: 4px;
            color: white;
            font-weight: bold;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            text-align: center;
        }}
        .stats-container {{
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }}
        .stats-list {{
            columns: 2;
            list-style-type: none;
            padding: 0;
        }}
        @media (max-width: 768px) {{
            .stats-list {{
                columns: 1;
            }}
        }}
    </style>
</head>
<body>
    <h1>Resultados del Análisis Léxico</h1>
    
    <h2>Muro de Ladrillos</h2>
    <div class="muro">
        {"".join(ladrillos_html)}
    </div>
    
    <div class="stats-container">
        <h2>Estadísticas de Tokens</h2>
        <ul class="stats-list">
            {"".join(stats_tokens)}
        </ul>
    </div>
    
    <div class="stats-container">
        <h2>Otras Estadísticas</h2>
        <ul class="stats-list">
            {"".join(otras_stats)}
        </ul>
    </div>
</body>
</html>
    """
    
    # Guardar el archivo HTML
    with open("analisis_lexico.html", "w", encoding="utf-8") as f:
        f.write(html_template)
    
    print("Archivo HTML generado exitosamente: analisis_lexico.html")