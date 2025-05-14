import re

def convertir_formato_comentarios(texto):
    lineas = texto.strip().splitlines()
    resultado = []

    for linea in lineas:
        # Saltar líneas con "Doble predicción" o similares
        if re.search(r'Doble predicci[oó]n', linea, re.IGNORECASE):
            continue

        # Extraer el comentario entre /* ... */
        comentario_match = re.search(r'/\*\s*(.*?)\s*\*/', linea)
        if not comentario_match:
            continue
        comentario = comentario_match.group(1).strip()

        # Extraer el contenido entre llaves {}
        contenido_match = re.search(r'\{(.*)\}', linea)
        if not contenido_match:
            continue
        contenido = contenido_match.group(1).strip()

        # Separar por comas y limpiar
        elementos = [elem.strip() for elem in contenido.split(',')]

        # Construir la salida
        resultado.append(f"# {comentario}")
        resultado.append(f"        [{', '.join(elementos)}],\n")

    return "\n".join(resultado)

# Ejemplo de uso
input_texto = """
/* <program> */ {Gramatica.MARCA_DERECHA,-1,-1},
/* Doble predicción en la línea siguiente con el terminal ON */
/* Doble predicción en la línea siguiente con el terminal OFF */
/* <section> */ {Gramatica.MARCA_DERECHA,1,2,3},
"""

print(convertir_formato_comentarios(input_texto))
