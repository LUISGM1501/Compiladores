# Notch Engine Scanner

Un analizador léxico (scanner) para el lenguaje de programación Notch Engine, inspirado en Minecraft.

## Características Principales

- **Reconocimiento completo de tokens**: Identifica todos los elementos léxicos del lenguaje Notch Engine.
- **Detección de errores**: Detecta y reporta errores léxicos según las especificaciones.
- **Recuperación de errores**: Implementa mecanismos para evitar errores en cascada.
- **Visualización**: Genera un "muro de ladrillos" HTML para visualizar los tokens reconocidos.
- **Estadísticas**: Proporciona estadísticas detalladas sobre el análisis.

## Requisitos

- Python 3.6 o superior

## Estructura del Proyecto

```
Etapa1/
├── codigo/
│   ├── scanner/
│   │   ├── automata/
│   │   │   ├── __init__.py
│   │   │   ├── base.py        # Autómata base
│   │   │   ├── comments.py    # Autómata para comentarios
│   │   │   ├── identifiers.py # Autómata para identificadores
│   │   │   ├── numbers.py     # Autómata para números
│   │   │   ├── operators.py   # Autómata para operadores
│   │   │   └── strings.py     # Autómata para strings
│   │   ├── __init__.py
│   │   ├── core.py            # Núcleo del scanner
│   │   ├── error_handling.py  # Manejo de errores
│   │   ├── tokens.py          # Definición de tokens
│   │   └── utils/
│   │       └── cantidadComentarios.py
│   ├── muroLadrillos/
│   │   └── generarMuroLadrillos.py
│   └── mc_scan.py             # Script principal
├── Pruebas/                   # Directorio para archivos de prueba
└── resultados/                # Directorio para resultados del análisis
```

## Uso

### Modo Interactivo

Para ejecutar el scanner en modo interactivo:

```bash
python mc_scan.py
```

Esto mostrará un menú con los archivos disponibles en la carpeta `Pruebas/` para seleccionar.

### Modo Línea de Comandos

Para analizar un archivo específico:

```bash
python mc_scan.py ruta/al/archivo.txt
```

## Errores Léxicos Detectados

El scanner puede detectar los siguientes errores:

- **E1**: Carácter no reconocido
- **E2**: Carácter Unicode no soportado
- **E3**: String sin cerrar
- **E4**: Carácter sin cerrar
- **E5**: Literal de carácter vacío
- **E6**: Secuencia de escape inválida
- **E7**: Múltiples caracteres en literal de carácter
- **E8**: Comentario de bloque sin cerrar
- **E9**: Múltiples puntos decimales
- **E10**: Número mal formado
- **E11**: Operador flotante incompleto
- **E12**: Literal de conjunto mal formado
- **E13**: Literal de archivo mal formado
- **E14**: Literal de registro mal formado
- **E15**: Literal de arreglo mal formado
- **E16**: Identificador mal formado
- **E17**: Identificador demasiado largo
- **E18**: Delimitador PolloCrudo sin cerrar
- **E19**: PolloAsado sin apertura
- **E20**: Delimitadores de estructuras de control incompletos
- **E21**: Palabra reservada mal escrita
- **E22**: Palabra reservada en contexto incorrecto
- **E23**: Operador de coerción incompleto
- **E24**: Operador de acceso incompleto
- **E25**: Error de lectura de archivo
- **E26**: Fin de archivo inesperado
- **E27**: Buffer overflow

## Resultados

Después de analizar un archivo, el scanner generará un archivo HTML en la carpeta `resultados/` con el nombre `<nombre_archivo>_Resultado.html`. Este archivo contiene:

1. Un muro de ladrillos donde cada ladrillo representa un token.
2. Estadísticas sobre los tokens encontrados.
3. Información general sobre el análisis.
4. Un resumen de los errores detectados (si los hay).

## Mejoras Implementadas

1. **Detección robusta de errores**: Se implementaron mecanismos para detectar todos los errores especificados.
2. **Recuperación de errores**: El scanner puede recuperarse de errores para evitar cascadas.
3. **Validación contextual**: Verificación de que las palabras reservadas se usen en el contexto correcto.
4. **Estructura mejorada de autómatas**: Diseño modular con autómatas especializados.
5. **Visualización mejorada**: El muro de ladrillos es más informativo y estéticamente agradable.
6. **Estadísticas detalladas**: Mayor información sobre los tokens y errores encontrados.

## Ejemplo de Salida HTML

El archivo HTML generado incluirá:

- **Muro de Ladrillos**: Representación visual de tokens.
- **Estadísticas de Tokens**: Distribución por categorías.
- **Información del Análisis**: Datos generales como líneas, caracteres, etc.
- **Advertencias y Errores**: Si se detectaron problemas.

## Notas Adicionales

- El scanner ignora espacios en blanco y comentarios en la generación de tokens finales.
- Los errores se reportan con información detallada para facilitar su corrección.
- La recuperación de errores permite que el análisis continúe incluso después de encontrar problemas.