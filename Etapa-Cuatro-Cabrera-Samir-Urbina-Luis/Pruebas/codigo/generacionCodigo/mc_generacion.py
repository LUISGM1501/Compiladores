"""
Archivo: mc_generacion.py

Autores: Samir Cabrera y Luis Urbina
Curso: Compiladores e Intérpretes, IC5701

Descripción: Módulo principal para la generación de código ASM
"""

from pathlib import Path
from generacionCodigo.plantillaBasica import generar_plantilla


def generar_codigo_asm(nombre_prueba):
    """
    Función principal para generar código ASM
    Args:
        nombre_prueba: Nombre del archivo de prueba
        tokens_limpios: Lista de tokens procesados
    """
    # Crear directorio de resultados si no existe
    resultados_dir = Path("resultadosASM")
    resultados_dir.mkdir(exist_ok=True)

    # Generar nombre del archivo de salida
    nombre_archivo = f"RSLT{nombre_prueba.stem}.ASM"
    ruta_archivo = resultados_dir / nombre_archivo

    # Generar contenido inicial
    contenido = generar_plantilla(nombre_prueba.name)

    # Guardar archivo
    try:
        with open(ruta_archivo, 'w') as f:
            f.write(contenido)
        print(f"\n✅ Archivo ASM generado en: {ruta_archivo}")
    except Exception as e:
        print(f"\n⚠️ Error al generar archivo ASM: {e}")

    # Aquí se agregará la generación de código real basado en los tokens
    # en futuras implementaciones

    return ruta_archivo