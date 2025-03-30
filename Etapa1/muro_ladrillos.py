"""
Generador de Muros de Ladrillos HTML para EnderLang
Autores: Samir Cabrera, Luis Urbina
Fecha de entrega: 10/04/2025

Este archivo implementa un generador de "muros de ladrillos" HTML
que muestra los tokens de un programa EnderLang como ladrillos de diferentes colores.
"""

import sys
import os
from scanner import Scanner
from token import Token

class GeneradorMuroLadrillos:
    """
    Genera un archivo HTML que muestra los tokens de un programa como ladrillos de colores.
    """
    
    def __init__(self):
        """
        Constructor de la clase GeneradorMuroLadrillos
        """
        # Mapeo de tipos de token a colores
        self.colores_token = {
            Token.TK_PALABRA_RESERVADA: "#4CAF50",  # Verde
            Token.TK_IDENTIFICADOR: "#2196F3",      # Azul
            Token.TK_ENTERO: "#FF9800",             # Naranja
            Token.TK_FLOTANTE: "#FF5722",           # Naranja oscuro
            Token.TK_CARACTER: "#9C27B0",           # Púrpura
            Token.TK_STRING: "#E91E63",             # Rosa
            Token.TK_OPERADOR: "#FF5252",           # Rojo claro
            Token.TK_SIMBOLO: "#607D8B",            # Gris azulado
            Token.TK_COMENTARIO: "#9E9E9E",         # Gris
            Token.TK_ERROR: "#F44336",              # Rojo
            Token.TK_EOF: "#000000"                 # Negro
        }
    
    def generar_muro(self, nombre_archivo_entrada, nombre_archivo_salida=None):
        """
        Lee los tokens de un archivo de entrada y genera un muro de ladrillos HTML
        
        Parámetros:
            nombre_archivo_entrada (str): Ruta al archivo fuente a analizar
            nombre_archivo_salida (str, opcional): Ruta al archivo HTML de salida.
                                               Si no se especifica, se usa el nombre
                                               del archivo de entrada con extensión .html
        
        Retorna:
            bool: True si se generó correctamente, False en caso contrario
        """
        # Si no se especificó un nombre para el archivo de salida, generar uno
        if nombre_archivo_salida is None:
            nombre_base = os.path.basename(nombre_archivo_entrada)
            nombre_archivo_salida = f"{nombre_base}.html"
        
        # Crear instancia del scanner y abrirlo
        scanner = Scanner()
        if not scanner.inicializar_scanner(nombre_archivo_entrada):
            print(f"Error: No se pudo abrir el archivo de entrada '{nombre_archivo_entrada}'")
            return False
        
        # Recopilar tokens y estadísticas
        tokens = []
        estadisticas = {
            "palabras_reservadas": 0,
            "identificadores": 0,
            "enteros": 0,
            "flotantes": 0,
            "caracteres": 0,
            "strings": 0,
            "operadores": 0,
            "simbolos": 0,
            "comentarios_linea": 0,
            "comentarios_bloque": 0,
            "errores": 0,
            "lineas": 0,
            "caracteres": 0
        }
        
        # Leer todos los tokens
        while True:
            token = scanner.tomar_token()
            tokens.append(token)
            
            # Actualizar estadísticas según el tipo de token
            if token.tipo == Token.TK_PALABRA_RESERVADA:
                estadisticas["palabras_reservadas"] += 1
            elif token.tipo == Token.TK_IDENTIFICADOR:
                estadisticas["identificadores"] += 1
            elif token.tipo == Token.TK_ENTERO:
                estadisticas["enteros"] += 1
            elif token.tipo == Token.TK_FLOTANTE:
                estadisticas["flotantes"] += 1
            elif token.tipo == Token.TK_CARACTER:
                estadisticas["caracteres"] += 1
            elif token.tipo == Token.TK_STRING:
                estadisticas["strings"] += 1
            elif token.tipo == Token.TK_OPERADOR:
                estadisticas["operadores"] += 1
            elif token.tipo == Token.TK_SIMBOLO:
                estadisticas["simbolos"] += 1
            elif token.tipo == Token.TK_COMENTARIO:
                if token.lexema.startswith("//"):
                    estadisticas["comentarios_linea"] += 1
                else:
                    estadisticas["comentarios_bloque"] += 1
            elif token.tipo == Token.TK_ERROR:
                estadisticas["errores"] += 1
            
            # Salir del bucle al encontrar el fin de archivo
            if token.tipo == Token.TK_EOF:
                break
        
        # Cerrar el scanner
        scanner.finalizar_scanner()
        
        # Calcular estadísticas adicionales del archivo
        try:
            with open(nombre_archivo_entrada, 'r', encoding='utf-8') as archivo:
                contenido = archivo.read()
                estadisticas["caracteres"] = len(contenido)
                estadisticas["lineas"] = contenido.count('\n') + 1
        except Exception as e:
            print(f"Advertencia: No se pudieron calcular algunas estadísticas del archivo: {e}")
        
        # Generar el archivo HTML
        try:
            with open(nombre_archivo_salida, 'w', encoding='utf-8') as archivo_html:
                # Escribir encabezado HTML
                archivo_html.write(self._generar_encabezado_html(nombre_archivo_entrada))
                
                # Escribir los ladrillos (tokens)
                archivo_html.write('    <div class="muro">\n')
                for token in tokens:
                    if token.tipo == Token.TK_EOF:
                        continue  # No mostrar el token EOF
                    
                    color = self.colores_token.get(token.tipo, "#333333")
                    # Escapar caracteres especiales en HTML
                    lexema = token.lexema.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                    tipo = token.tipo
                    
                    archivo_html.write(f'        <div class="ladrillo" style="background-color: {color};" '
                                      f'title="{tipo} (L{token.linea}, C{token.columna})">{lexema}</div>\n')
                
                archivo_html.write('    </div>\n')
                
                # Escribir estadísticas
                archivo_html.write(self._generar_estadisticas_html(estadisticas))
                
                # Cerrar el HTML
                archivo_html.write('</body>\n</html>')
            
            print(f"Muro de ladrillos generado correctamente en '{nombre_archivo_salida}'")
            return True
            
        except Exception as e:
            print(f"Error al generar el archivo HTML: {e}")
            return False
    
    def _generar_encabezado_html(self, nombre_archivo):
        """
        Genera el encabezado HTML con los estilos necesarios
        """
        return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Muro de Ladrillos - EnderLang</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f0f0f0;
        }}
        h1 {{
            color: #333;
            text-align: center;
        }}
        .archivo-info {{
            text-align: center;
            margin-bottom: 20px;
            color: #555;
        }}
        .muro {{
            display: flex;
            flex-wrap: wrap;
            margin: 20px 0;
            background-color: #ddd;
            padding: 10px;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }}
        .ladrillo {{
            margin: 3px;
            padding: 6px 10px;
            border-radius: 4px;
            display: inline-block;
            color: white;
            font-family: monospace;
            font-size: 14px;
            font-weight: bold;
            max-width: 300px;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
            box-shadow: 0 1px 3px rgba(0,0,0,0.2);
            transition: all 0.2s ease;
        }}
        .ladrillo:hover {{
            max-width: none;
            white-space: normal;
            z-index: 1;
            position: relative;
            transform: scale(1.05);
            box-shadow: 0 3px 10px rgba(0,0,0,0.3);
        }}
        .estadisticas {{
            background-color: white;
            padding: 15px;
            border-radius: 5px;
            margin-top: 20px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }}
        .estadisticas h2 {{
            margin-top: 0;
            color: #333;
            border-bottom: 1px solid #eee;
            padding-bottom: 10px;
        }}
        .leyenda {{
            display: flex;
            flex-wrap: wrap;
            margin-top: 20px;
            justify-content: center;
        }}
        .leyenda-item {{
            display: flex;
            align-items: center;
            margin: 5px 10px;
        }}
        .leyenda-color {{
            width: 20px;
            height: 20px;
            border-radius: 3px;
            margin-right: 5px;
        }}
    </style>
</head>
<body>
    <h1>Muro de Ladrillos - EnderLang</h1>
    <div class="archivo-info">Archivo: <strong>{nombre_archivo}</strong></div>
"""
    
    def _generar_estadisticas_html(self, estadisticas):
        """
        Genera el HTML para mostrar las estadísticas
        """
        html = '    <div class="estadisticas">\n'
        html += '        <h2>Estadísticas</h2>\n'
        html += '        <ul>\n'
        
        # Agregar solo las estadísticas con valores mayores a cero
        if estadisticas["lineas"] > 0:
            html += f'            <li>Líneas: {estadisticas["lineas"]}</li>\n'
        
        if estadisticas["caracteres"] > 0:
            html += f'            <li>Caracteres: {estadisticas["caracteres"]}</li>\n'
        
        if estadisticas["palabras_reservadas"] > 0:
            html += f'            <li>Palabras reservadas: {estadisticas["palabras_reservadas"]}</li>\n'
        
        if estadisticas["identificadores"] > 0:
            html += f'            <li>Identificadores: {estadisticas["identificadores"]}</li>\n'
        
        if estadisticas["enteros"] > 0:
            html += f'            <li>Números enteros: {estadisticas["enteros"]}</li>\n'
        
        if estadisticas["flotantes"] > 0:
            html += f'            <li>Números flotantes: {estadisticas["flotantes"]}</li>\n'
        
        if estadisticas["caracteres"] > 0:
            html += f'            <li>Caracteres: {estadisticas["caracteres"]}</li>\n'
        
        if estadisticas["strings"] > 0:
            html += f'            <li>Strings: {estadisticas["strings"]}</li>\n'
        
        if estadisticas["operadores"] > 0:
            html += f'            <li>Operadores: {estadisticas["operadores"]}</li>\n'
        
        if estadisticas["simbolos"] > 0:
            html += f'            <li>Símbolos: {estadisticas["simbolos"]}</li>\n'
        
        total_comentarios = estadisticas["comentarios_linea"] + estadisticas["comentarios_bloque"]
        if total_comentarios > 0:
            html += f'            <li>Comentarios: {total_comentarios} '
            html += f'(Línea: {estadisticas["comentarios_linea"]}, '
            html += f'Bloque: {estadisticas["comentarios_bloque"]})</li>\n'
        
        if estadisticas["errores"] > 0:
            html += f'            <li><strong>Errores detectados: {estadisticas["errores"]}</strong></li>\n'
        
        html += '        </ul>\n'
        
        # Agregar leyenda de colores
        html += '        <div class="leyenda">\n'
        for tipo, color in self.colores_token.items():
            if tipo != Token.TK_EOF:  # No mostrar el EOF en la leyenda
                html += f'            <div class="leyenda-item">\n'
                html += f'                <div class="leyenda-color" style="background-color: {color};"></div>\n'
                html += f'                <span>{tipo}</span>\n'
                html += f'            </div>\n'
        html += '        </div>\n'
        html += '    </div>\n'
        
        return html


# Función principal para ejecutar desde línea de comandos
def main():
    """
    Función principal que se ejecuta cuando se llama al script
    """
    # Verificar argumentos
    if len(sys.argv) < 2:
        print("Error: Se requiere especificar un archivo de entrada.")
        print("Uso: python muro_ladrillos.py <archivo_entrada> [archivo_salida]")
        return 1
    
    # Obtener argumentos
    nombre_archivo_entrada = sys.argv[1]
    nombre_archivo_salida = sys.argv[2] if len(sys.argv) > 2 else None
    
    # Crear generador y procesar archivo
    generador = GeneradorMuroLadrillos()
    resultado = generador.generar_muro(nombre_archivo_entrada, nombre_archivo_salida)
    
    return 0 if resultado else 1


# Ejecutar el programa si se llama directamente
if __name__ == "__main__":
    sys.exit(main())