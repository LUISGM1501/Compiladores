import re

def convertir_formato_comentarios(texto):
    lineas = texto.strip().splitlines()
    resultado = []

    for linea in lineas:
        # Extraer el comentario entre /* ... */
        comentario_match = re.search(r'/\*\s*(.*?)\s*\*/', linea)
        if not comentario_match:
            continue
        comentario = comentario_match.group(1)

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
/* <program> */ {Gramatica.MARCA_DERECHA,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1},
/* <program_sections> */ {Gramatica.MARCA_DERECHA,9,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1},
/* <section> */ {Gramatica.MARCA_DERECHA,1,2,3,4,5,6,9,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1},
/* <bedrock_section> */ {Gramatica.MARCA_DERECHA,1,2,3,4,5,6,9,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1},
/* <constant_decl> */ {Gramatica.MARCA_DERECHA,7,1,2,3,4,5,6,9,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1},
"""

print(convertir_formato_comentarios(input_texto))
