"""
Compilador Notch Engine

Estudiantes: Cabrera Samir y Urbina Luis

Archivo: main.py

Breve Descripcion: Archivo de gestion principal
"""

import sys
import os
from pathlib import Path

# Asegurarse de que el directorio actual está en el path para las importaciones
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scanner.mc_scanner import procesar_archivo
from parser.mc_parser import iniciar_parser
from parser.gramatica.Gramatica import Gramatica
from parser.semantica.TablaSimbolos import TablaSimbolos
from parser.semantica.HistorialSemantico import HistorialSemanticoSingleton
from parser.semantica.HistorialSemanticoNegativo import HistorialSemanticoNegativoSingleton
from token_cleaner import limpiar_tokens_para_parser, debug_tokens_para_parser
from generacionCodigo.mc_generacion import generar_codigo_asm

# Importar módulos de prueba de generación
try:
    from generacionCodigo.test_generador import test_mc_generacion_directo
    from generacionCodigo.mc_generacion import GeneradorConRuntime, GeneradorCompleto
    GENERACION_PRUEBAS_DISPONIBLE = True
except ImportError as e:
    print(f"⚠️ Módulos de prueba de generación no disponibles: {e}")
    GENERACION_PRUEBAS_DISPONIBLE = False

# Verificar integridad
Gramatica.verificarIntegridadRangos()

# Diagnosticar símbolos problemáticos
for simbolo in [220, 222, 224, 225, 226, 227, 228, 229, 230, 231]:
    print(Gramatica.diagnosticarSimbolo(simbolo))


def menu_principal():
    """Menú principal mejorado con opciones de generación"""
    while True:
        print("\n" + "="*60)
        print("COMPILADOR NOTCH ENGINE - MENÚ PRINCIPAL".center(60))
        print("="*60)
        print("1. Ejecutar análisis completo de archivo (Modo Original)")
        print("2. Ejecutar pruebas de generación de código")
        print("3. Procesar todos los archivos de prueba")
        print("4. Generar Runtime Library independiente")
        print("5. Análisis individual con generación completa")
        print("0. Salir")
        print("-" * 60)
        
        try:
            opcion = int(input("Seleccione una opción: "))
            
            if opcion == 0:
                print("👋 ¡Hasta luego!")
                break
            elif opcion == 1:
                ejecucion()  # Función original
            elif opcion == 2:
                ejecutar_pruebas_generacion()
            elif opcion == 3:
                procesar_todos_los_archivos()
            elif opcion == 4:
                generar_runtime_library()
            elif opcion == 5:
                ejecutar_analisis_completo_individual()
            else:
                print("❌ Opción no válida")
                
        except ValueError:
            print("❌ Por favor ingrese un número válido")
        except KeyboardInterrupt:
            print("\n👋 ¡Hasta luego!")
            break


def ejecucion():
    """Modo interactivo original (mantenido sin cambios)"""
    pruebas_dir = Path("Pruebas")
    pruebas = sorted([p for p in pruebas_dir.glob("*.txt")])
    
    if not pruebas:
        print("No se encontraron archivos de prueba en la carpeta Pruebas/")
        return
    
    # Mostrar menú
    print("\n" + "="*50)
    print("MC Scanner - Menú de Pruebas".center(50))
    print("="*50)
    for i, prueba in enumerate(pruebas, 1):
        print(f"{i:2d}. {prueba.name}")
    print("\n0. Salir")
    
    # Selección
    while True:
        try:
            seleccion = int(input("\nSeleccione una prueba (número): "))
            if 0 <= seleccion <= len(pruebas):
                break
            print("Error: Selección fuera de rango")
        except ValueError:
            print("Error: Ingrese un número válido")
    
    if seleccion == 0:
        print("Saliendo...")
        return
    
    archivo_prueba = pruebas[seleccion-1]
    print(f"\nEjecutando prueba: {archivo_prueba.name}")
    
    #################################################################
    #################################################################
    ##                    INICIO SCANER                            ##
    #################################################################
    # Procesar y obtener tokens
    tokens = procesar_archivo(archivo_prueba)
    print("\nTokens generados (primeros 10):")
    for i, token in enumerate(tokens[:10]):
        print(f"{i}: {token}")
    
    #################################################################
    #################################################################
    ##                 LIMPIEZA DE TOKENS                          ##
    #################################################################
    print("\n" + "="*60)
    print("              APLICANDO LIMPIEZA DE TOKENS")
    print("="*60)
    
    # *** NUEVA FUNCIONALIDAD: Limpiar tokens ***
    tokens_limpios = limpiar_tokens_para_parser(tokens)
    
    # Debug de la limpieza (opcional, comentar si no quieres tanto detalle)
    debug_tokens_para_parser(tokens, tokens_limpios)
    
    #################################################################
    #################################################################
    ##                    INICIO ANALISIS                          ##
    ##                  SINTACTICO Y SEMANTICO                     ##
    #################################################################
    # Funcionamiento del parser con tokens limpios
    iniciar_parser(tokens_limpios, debug=False, nivel_debug=1) 

    mostrar_menu(archivo_prueba)
    
    # NUEVO: Mostrar resultados de operadores compuestos
    mostrar_resultados_operadores_compuestos()
    
    #################################################################
    #################################################################


def ejecutar_analisis_completo_individual():
    """Ejecuta análisis completo con generación de código para un archivo individual"""
    pruebas_dir = Path("Pruebas")
    pruebas = sorted([p for p in pruebas_dir.glob("*.txt")])
    
    if not pruebas:
        print("❌ No se encontraron archivos de prueba")
        return
    
    print("\nArchivos de prueba disponibles:")
    for i, prueba in enumerate(pruebas, 1):
        print(f"{i:2d}. {prueba.name}")
    
    try:
        seleccion = int(input("\nSeleccione un archivo (número): "))
        if 1 <= seleccion <= len(pruebas):
            archivo_seleccionado = pruebas[seleccion - 1]
            procesar_archivo_completo_con_generacion(archivo_seleccionado)
        else:
            print("❌ Selección fuera de rango")
    except ValueError:
        print("❌ Por favor ingrese un número válido")


def procesar_archivo_completo_con_generacion(archivo_prueba):
    """Procesa un archivo completo desde tokens hasta generación de código"""
    print(f"\n{'='*60}")
    print(f"PROCESANDO ARCHIVO COMPLETO: {archivo_prueba.name}")
    print(f"{'='*60}")
    
    try:
        # ETAPA 1: ANÁLISIS LÉXICO (igual que el original)
        print("\n🔍 ETAPA 1: ANÁLISIS LÉXICO")
        print("-" * 40)
        tokens = procesar_archivo(archivo_prueba)
        
        if not tokens:
            print("❌ No se generaron tokens")
            return False
        
        print(f"✅ Tokens generados: {len(tokens)}")
        print(f"   Primeros 5 tokens:")
        for i, token in enumerate(tokens[:5]):
            print(f"     {i+1}: {token}")
        
        # ETAPA 2: LIMPIEZA DE TOKENS (igual que el original)
        print("\n🧹 ETAPA 2: LIMPIEZA DE TOKENS")
        print("-" * 40)
        tokens_limpios = limpiar_tokens_para_parser(tokens)
        print(f"✅ Tokens limpios: {len(tokens_limpios)}")
        
        # ETAPA 3: ANÁLISIS SINTÁCTICO Y SEMÁNTICO (igual que el original)
        print("\n📖 ETAPA 3: ANÁLISIS SINTÁCTICO Y SEMÁNTICO")
        print("-" * 40)
        
        # Ejecutar parser (manteniendo compatibilidad con versión original)
        resultado_parser = iniciar_parser(tokens_limpios, debug=False, nivel_debug=1)
        
        print("✅ Análisis sintáctico y semántico completado")
        
        # Mostrar información semántica como en el original
        tabla = TablaSimbolos.instancia()
        print(f"✅ Análisis semántico completado")
        
        # ETAPA 4: GENERACIÓN DE CÓDIGO (nueva funcionalidad)
        print("\n⚙️ ETAPA 4: GENERACIÓN DE CÓDIGO")
        print("-" * 40)
        
        # Crear directorio de resultados
        resultados_dir = Path("resultadosASM")
        resultados_dir.mkdir(exist_ok=True)
        
        # Usar la función original de generación
        print("🔧 Ejecutando generación de código original...")
        resultado_generacion = generar_codigo_asm(archivo_prueba)
        
        if resultado_generacion:
            print("✅ Generación de código original exitosa")
        else:
            print("⚠️ Generación de código original tuvo problemas")
        
        # ETAPA 5: PRUEBAS ADICIONALES DE GENERACIÓN (si están disponibles)
        if GENERACION_PRUEBAS_DISPONIBLE:
            print("\n🧪 ETAPA 5: PRUEBAS ADICIONALES DE GENERACIÓN")
            print("-" * 40)
            
            try:
                generador = GeneradorCompleto()
                
                # Generar Runtime Library si no existe
                runtime_path = resultados_dir / "runtime_library.asm"
                if not runtime_path.exists():
                    print("📚 Creando Runtime Library...")
                    generador.crear_archivo_runtime(str(runtime_path))
                
                # Generar código adicional basado en los tokens
                nombre_archivo_extra = f"EXTRA_{archivo_prueba.stem}.ASM"
                ruta_archivo_extra = resultados_dir / nombre_archivo_extra
                
                print(f"🔧 Generando código adicional: {nombre_archivo_extra}")
                
                # Procesar algunos tokens básicos para demostración
                if procesar_tokens_basicos_para_generacion(generador, tokens_limpios):
                    generador.finalizar_programa()
                    generador.guardar_archivo(str(ruta_archivo_extra))
                    print(f"✅ Archivo adicional generado: {ruta_archivo_extra}")
                    
                    # Mostrar estadísticas
                    stats = generador.obtener_estadisticas()
                    print(f"📊 Estadísticas adicionales:")
                    print(f"   Variables: {stats['variables_declaradas']}")
                    print(f"   Uso datos: {stats['tamaño_datos']} bytes")
                    print(f"   Uso código: {stats['tamaño_codigo']} bytes")
                else:
                    print("⚠️ Error procesando tokens para generación adicional")
                    
            except Exception as e:
                print(f"⚠️ Error en pruebas adicionales: {e}")
        
        print(f"\n🎉 PROCESAMIENTO COMPLETO DE {archivo_prueba.name} FINALIZADO")
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR GENERAL: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def procesar_tokens_basicos_para_generacion(generador, tokens):
    """Procesa tokens básicos para generar código de demostración"""
    try:
        # Buscar declaraciones de variables básicas
        for i, token in enumerate(tokens):
            if token.tipo in ["STACK", "GHAST", "TORCH"] and i + 1 < len(tokens):
                if tokens[i + 1].tipo == "IDENTIFICADOR":
                    nombre_var = tokens[i + 1].lexema
                    tipo_var = token.tipo
                    generador.declarar_variable(nombre_var, tipo_var, "0")
                    print(f"  📝 Variable de demo: {tipo_var} {nombre_var}")
        
        # Generar una operación de ejemplo
        generador.declarar_variable("demo_resultado", "STACK", "0")
        generador.generar_operacion_aritmetica(":+", "demo_resultado", "10", "5")
        
        return True
    except Exception as e:
        print(f"Error en procesamiento básico: {e}")
        return False


def ejecutar_pruebas_generacion():
    """Ejecuta pruebas específicas de generación de código"""
    print("\n🧪 EJECUTANDO PRUEBAS DE GENERACIÓN DE CÓDIGO")
    print("=" * 60)
    
    if not GENERACION_PRUEBAS_DISPONIBLE:
        print("❌ Módulos de prueba de generación no disponibles")
        return False
    
    try:
        # Crear directorio de pruebas de generación
        pruebas_gen_dir = Path("pruebasGeneracion")
        pruebas_gen_dir.mkdir(exist_ok=True)
        
        # Cambiar al directorio de pruebas
        original_dir = os.getcwd()
        os.chdir(str(pruebas_gen_dir))
        
        try:
            # PRUEBA 1: Test básico del generador
            print("\n🔬 PRUEBA 1: Funcionalidad Básica")
            print("-" * 40)
            resultado1 = test_mc_generacion_directo()
            
            # PRUEBA 2: Crear Runtime Library completa
            print("\n🔬 PRUEBA 2: Runtime Library Completa")
            print("-" * 40)
            generador = GeneradorConRuntime()
            resultado2 = generador.crear_archivo_runtime("runtime_completa.asm")
            if resultado2:
                print("✅ Runtime Library completa creada")
            else:
                print("❌ Error creando Runtime Library")
            
            # PRUEBA 3: Generador completo con control de flujo
            print("\n🔬 PRUEBA 3: Generador con Control de Flujo")
            print("-" * 40)
            generador_completo = GeneradorCompleto()
            generador_completo.declarar_variable("numero", "STACK", "10")
            generador_completo.declarar_variable("resultado", "STACK", "0")
            generador_completo.generar_operacion_aritmetica(":+", "resultado", "numero", "5")
            generador_completo.finalizar_programa()
            resultado3 = generador_completo.guardar_archivo("prueba_completa.asm")
            
            # Resumen
            resultados = [resultado1, resultado2, resultado3]
            exitosas = sum(1 for r in resultados if r)
            
            print(f"\n📊 RESUMEN DE PRUEBAS DE GENERACIÓN")
            print(f"   Exitosas: {exitosas}/{len(resultados)}")
            
            return exitosas == len(resultados)
            
        finally:
            os.chdir(original_dir)
            
    except Exception as e:
        print(f"❌ Error en pruebas de generación: {str(e)}")
        return False


def procesar_todos_los_archivos():
    """Procesa todos los archivos de prueba"""
    pruebas_dir = Path("Pruebas")
    pruebas = sorted([p for p in pruebas_dir.glob("*.txt")])
    
    if not pruebas:
        print("❌ No se encontraron archivos de prueba")
        return
    
    print(f"\n🔄 PROCESANDO {len(pruebas)} ARCHIVOS DE PRUEBA")
    print("=" * 60)
    
    exitosos = 0
    for i, archivo in enumerate(pruebas, 1):
        print(f"\n[{i}/{len(pruebas)}] Procesando: {archivo.name}")
        if procesar_archivo_completo_con_generacion(archivo):
            exitosos += 1
    
    print(f"\n📊 RESUMEN FINAL")
    print(f"   Archivos procesados exitosamente: {exitosos}/{len(pruebas)}")
    print(f"   Porcentaje de éxito: {(exitosos/len(pruebas)*100):.1f}%")


def generar_runtime_library():
    """Genera la Runtime Library independientemente"""
    if not GENERACION_PRUEBAS_DISPONIBLE:
        print("❌ Módulos de generación no disponibles")
        return
    
    print("\n📚 GENERANDO RUNTIME LIBRARY")
    print("-" * 40)
    
    try:
        generador = GeneradorConRuntime()
        resultado = generador.crear_archivo_runtime("runtime_library_standalone.asm")
        
        if resultado:
            print("✅ Runtime Library generada exitosamente")
            print("📁 Archivo: runtime_library_standalone.asm")
        else:
            print("❌ Error generando Runtime Library")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")


def mostrar_resultados_operadores_compuestos():
    """Muestra los resultados de las operaciones compuestas (función original mantenida)"""
    tabla = TablaSimbolos.instancia()
    
    print("\n" + "="*50)
    print("RESULTADOS DE OPERADORES COMPUESTOS")
    print("="*50)
    
    variables_interes = ["numero1", "numero2", "flotante1", "flotante2", "cadena1", "cadena2"]
    
    for var_nombre in variables_interes:
        simbolo = tabla.buscar(var_nombre)
        if simbolo:
            print(f"{var_nombre} ({simbolo.tipo}): {simbolo.valor}")
        else:
            print(f"{var_nombre}: No encontrado")
    
    print("="*50)


def mostrar_menu(archivo_prueba):
    """Función original del menú mantenida sin cambios"""
    print("\n\n\n\n\n\n\n\n--- MENÚ DE INFORMACIÓN SEMÁNTICA ---")
    print("1. Ver información de la tabla de símbolos")
    print("2. Ver historial semántico positivo")
    print("3. Ver historial semántico negativo")
    print("4. Salir")

    opcion = input("Seleccione una opción: ")

    if opcion == "1":
        tabla = TablaSimbolos.instancia()
        print("\n\nInformación de la tabla de símbolos:")
        tabla.imprimir_tabla()
        mostrar_menu(archivo_prueba)
    elif opcion == "2":
        historial = HistorialSemanticoSingleton()
        print("\n\nHistorial semántico completo:")
        historial.imprimir_historial()
        mostrar_menu(archivo_prueba)
    elif opcion == "3":
        historial_neg = HistorialSemanticoNegativoSingleton()
        print("\n\nHistorial semántico negativo:")
        historial_neg.imprimir_historial()
        mostrar_menu(archivo_prueba)
    elif opcion == "4":
        print("\nSaliendo del sistema...")
        #################################################################
        #################################################################
        ##                 LLAMADA A GENERACION DE CODIGO             ##
        ################################################################
        ################################################################
        print("\n" + "=" * 60)
        print("              GENERANDO CÓDIGO ASM")
        print("=" * 60)

        # Generar código ASM (función original mantenida)
        generar_codigo_asm(archivo_prueba)
        sys.exit()
    else:
        print("\nOpción inválida. Por favor intente de nuevo.")
        mostrar_menu(archivo_prueba)


if __name__ == "__main__":
    menu_principal()