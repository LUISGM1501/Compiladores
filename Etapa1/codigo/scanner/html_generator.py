# /Etapa1/codigo/scanner/html_generator.py
"""
Generador de muros de ladrillos HTML
"""

import os
import html

class HtmlGenerator:
    """
    Clase para generar los muros de ladrillos HTML
    """
    def __init__(self):
        """
        Inicializa el generador HTML
        """
        self.tokens = []
        self.estadisticas = {
            "lineas": 0,
            "caracteres": 0,
            "comentarios_linea": 0,
            "comentarios_bloque": 0,
            "errores": 0,
            "tokens_por_tipo": {}
        }
    
    def agregar_token(self, token):
        """
        Agrega un token al muro de ladrillos
        
        Argumentos:
            token: Token a agregar
        """
        self.tokens.append(token)
        
        # Actualizar estadísticas por tipo de token
        tipo = token.tipo
        if tipo not in self.estadisticas["tokens_por_tipo"]:
            self.estadisticas["tokens_por_tipo"][tipo] = 0
        self.estadisticas["tokens_por_tipo"][tipo] += 1
        
        # Actualizar estadísticas específicas
        if tipo == "COMENTARIO":
            if token.lexema.startswith("$$"):
                self.estadisticas["comentarios_linea"] += 1
            elif token.lexema.startswith("$*"):
                self.estadisticas["comentarios_bloque"] += 1
        elif tipo == "ERROR":
            self.estadisticas["errores"] += 1
    
    def establecer_estadisticas_archivo(self, lineas, caracteres):
        """
        Establece las estadísticas del archivo
        
        Argumentos:
            lineas: Número de líneas
            caracteres: Número de caracteres
        """
        self.estadisticas["lineas"] = lineas
        self.estadisticas["caracteres"] = caracteres
    
    def generar_html(self, nombre_archivo_salida):
        """
        Genera el archivo HTML con el muro de ladrillos
        
        Argumentos:
            nombre_archivo_salida: Nombre del archivo HTML de salida
        """
        # Crear la estructura HTML
        html_content = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Muro de Ladrillos - Notch Engine</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }
        h1, h2 {
            color: #333;
        }
        .wall {
            display: flex;
            flex-wrap: wrap;
            gap: 5px;
            margin: 20px 0;
            padding: 10px;
            background-color: #e0e0e0;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        .brick {
            padding: 5px 10px;
            border-radius: 3px;
            font-family: monospace;
            font-size: 14px;
            color: white;
            position: relative;
        }
        .brick:hover::after {
            content: attr(data-info);
            position: absolute;
            bottom: 100%;
            left: 50%;
            transform: translateX(-50%);
            background-color: #333;
            color: white;
            padding: 5px;
            border-radius: 3px;
            font-size: 12px;
            white-space: nowrap;
            z-index: 1;
        }
        .identifier { background-color: #4CAF50; }
        .number { background-color: #2196F3; }
        .string { background-color: #9C27B0; }
        .keyword { background-color: #FF9800; }
        .operator { background-color: #F44336; }
        .comment { background-color: #607D8B; }
        .error { background-color: #f44336; }
        .punctuation { background-color: #795548; }
        
        .stats {
            margin-top: 30px;
            padding: 15px;
            background-color: white;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 15px;
        }
        .stat-item {
            background-color: #f9f9f9;
            padding: 10px;
            border-radius: 3px;
        }
    </style>
</head>
<body>
    <h1>Análisis Léxico - Notch Engine</h1>
    <h2>Muro de Ladrillos</h2>
    <div class="wall">
"""
        
        # Agregar los tokens (ladrillos)
        for token in self.tokens:
            if token.tipo == "EOF":
                continue
                
            # Determinar la clase CSS según el tipo de token
            css_class = "brick "
            if token.tipo == "IDENTIFICADOR":
                css_class += "identifier"
            elif token.tipo in ["NUMERO_ENTERO", "NUMERO_DECIMAL"]:
                css_class += "number"
            elif token.tipo in ["CADENA", "CARACTER"]:
                css_class += "string"
            elif token.tipo == "COMENTARIO":
                css_class += "comment"
            elif token.tipo == "ERROR":
                css_class += "error"
            elif token.tipo in ["SUMA", "RESTA", "MULTIPLICACION", "DIVISION", "MODULO", 
                              "MAYOR_QUE", "MENOR_QUE", "MAYOR_IGUAL", "MENOR_IGUAL", 
                              "IGUAL", "SUMA_FLOTANTE", "RESTA_FLOTANTE", "MULTIPLICACION_FLOTANTE",
                              "DIVISION_FLOTANTE", "MODULO_FLOTANTE", "DIVISION_ENTERA"]:
                css_class += "operator"
            elif token.tipo in ["PUNTO_Y_COMA", "COMA", "PUNTO", "DOS_PUNTOS", 
                              "PARENTESIS_ABRE", "PARENTESIS_CIERRA", 
                              "CORCHETE_ABRE", "CORCHETE_CIERRA", 
                              "LLAVE_ABRE", "LLAVE_CIERRA"]:
                css_class += "punctuation"
            else:
                css_class += "keyword"
            
            # Escapar el lexema para HTML
            lexema_html = html.escape(token.lexema)
            
            # Crear el ladrillo (token)
            info = f"{token.tipo} ({token.linea}:{token.columna})"
            html_content += f'        <div class="{css_class}" data-info="{info}">{lexema_html}</div>\n'
        
        # Cerrar la pared de ladrillos
        html_content += """    </div>

    <h2>Estadísticas</h2>
    <div class="stats">
        <div class="stats-grid">
"""
        
        # Agregar estadísticas generales
        html_content += f'            <div class="stat-item"><strong>Líneas de código:</strong> {self.estadisticas["lineas"]}</div>\n'
        html_content += f'            <div class="stat-item"><strong>Caracteres:</strong> {self.estadisticas["caracteres"]}</div>\n'
        
        # Agregar estadísticas de comentarios si hay
        if self.estadisticas["comentarios_linea"] > 0:
            html_content += f'            <div class="stat-item"><strong>Comentarios de línea:</strong> {self.estadisticas["comentarios_linea"]}</div>\n'
        if self.estadisticas["comentarios_bloque"] > 0:
            html_content += f'            <div class="stat-item"><strong>Comentarios de bloque:</strong> {self.estadisticas["comentarios_bloque"]}</div>\n'
        
        # Agregar errores si hay
        if self.estadisticas["errores"] > 0:
            html_content += f'            <div class="stat-item"><strong>Errores léxicos:</strong> {self.estadisticas["errores"]}</div>\n'
        
        # Agregar estadísticas por familia de tokens
        for tipo, cantidad in self.estadisticas["tokens_por_tipo"].items():
            # Saltamos EOF, ERROR y COMENTARIO (ya están contados en otra parte)
            if tipo in ["EOF", "ERROR", "COMENTARIO"]:
                continue
            html_content += f'            <div class="stat-item"><strong>Tokens {tipo}:</strong> {cantidad}</div>\n'
        
        # Cerrar el HTML
        html_content += """        </div>
    </div>
</body>
</html>
"""
        
        # Escribir el contenido al archivo
        with open(nombre_archivo_salida, 'w', encoding='utf-8') as archivo:
            archivo.write(html_content)
        
        print(f"Archivo HTML generado: {nombre_archivo_salida}")