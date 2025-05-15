def convertir_formato(texto):
    lineas = texto.strip().splitlines()
    resultado = []

    for linea in lineas:
        linea = linea.strip().replace('{', '[').replace('}', ']')
        resultado.append(f"        {linea}")

    return "\n".join(resultado)

# Ejemplo de uso
input_texto = """
{9,135,112,91,0,-1,-1,-1,-1},
{135,136,-1,-1,-1,-1,-1,-1,-1},
{-1,-1,-1,-1,-1,-1,-1,-1,-1},
{137,1,-1,-1,-1,-1,-1,-1,-1},
{140,2,-1,-1,-1,-1,-1,-1,-1},
"""

print(convertir_formato(input_texto))
