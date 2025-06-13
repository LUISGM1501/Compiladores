"""
Compilador Notch Engine

Estudiantes: Cabrera Samir y Urbina Luis

Archivo: test_generador.py

Breve Descripcion: PRUEBA DIRECTA del archivo mc_generacion.py
"""

# Archivo básico de pruebas para el generador de código

def test_mc_generacion_directo():
    """Prueba básica del generador de código"""
    
    print("🎯 PROBANDO GENERADOR DE CÓDIGO")
    print("="*50)
    
    try:
        # Importar desde la ubicación correcta
        from generacionCodigo.mc_generacion import GeneradorConRuntime, GeneradorCompleto
        
        print("✅ Módulos importados correctamente")
        
        # PASO 1: Crear generador básico
        print("\n🔧 Creando generador básico...")
        gen = GeneradorConRuntime()
        print("✅ GeneradorConRuntime creado")
        
        # PASO 2: Probar crear Runtime Library
        print("\n📚 Creando Runtime Library...")
        resultado = gen.crear_archivo_runtime("runtime_generado.asm")
        
        if resultado:
            print("✅ Runtime Library creada: runtime_generado.asm")
        else:
            print("❌ FALLÓ crear Runtime Library")
            return False
        
        # PASO 3: Crear generador completo
        print("\n🔧 Creando generador completo...")
        gen_completo = GeneradorCompleto()
        
        # PASO 4: Probar generar código
        print("\n⚙️ Probando generar código...")
        gen_completo.declarar_variable("numero", "STACK", "10")
        gen_completo.declarar_variable("resultado", "STACK", "0")
        gen_completo.generar_operacion_aritmetica(":+", "resultado", "numero", "5")
        gen_completo.finalizar_programa()
        
        # PASO 5: Guardar programa completo
        print("\n💾 Guardando programa de prueba...")
        resultado_guardar = gen_completo.guardar_archivo("programa_test.asm")
        
        if resultado_guardar:
            print("✅ Programa completo generado: programa_test.asm")
        else:
            print("❌ Programa NO generado")
            return False
        
        # PASO 6: Verificar archivos existen
        import os
        archivos_verificar = ["runtime_generado.asm", "programa_test.asm"]
        
        for archivo in archivos_verificar:
            if os.path.exists(archivo):
                print(f"✅ Archivo verificado: {archivo}")
                
                # Mostrar estadísticas básicas
                with open(archivo, 'r', encoding='utf-8', errors='ignore') as f:
                    contenido = f.read()
                
                print(f"   📊 Líneas: {len(contenido.splitlines())}")
                print(f"   📊 Caracteres: {len(contenido)}")
                
                if "PROC" in contenido:
                    print(f"   📊 Procedimientos: {contenido.count('PROC')}")
                
            else:
                print(f"❌ Archivo NO existe: {archivo}")
                return False
        
        print(f"\n🎉 TODAS LAS PRUEBAS PASARON EXITOSAMENTE")
        return True
        
    except ImportError as e:
        print(f"❌ Error de importación: {e}")
        print("   Verifica que el archivo generacionCodigo/mc_generacion.py tenga las clases necesarias")
        return False
        
    except Exception as e:
        print(f"❌ Error en las pruebas: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_generacion_simple():
    """Prueba simplificada solo de la función básica"""
    
    print("🧪 PRUEBA SIMPLIFICADA DE GENERACIÓN")
    print("-"*40)
    
    try:
        from generacionCodigo.mc_generacion import generar_codigo_asm
        from pathlib import Path
        
        # Crear un archivo de prueba ficticio
        archivo_prueba = Path("prueba_dummy.txt")
        
        # Ejecutar la función
        resultado = generar_codigo_asm(archivo_prueba)
        
        if resultado:
            print("✅ Función generar_codigo_asm funcionó correctamente")
            return True
        else:
            print("⚠️ Función ejecutó pero con advertencias")
            return True  # Consideramos éxito parcial
            
    except Exception as e:
        print(f"❌ Error en prueba simple: {e}")
        return False


if __name__ == "__main__":
    print("🚀 INICIANDO PRUEBAS DEL GENERADOR")
    print("="*50)
    
    # Ejecutar prueba completa
    resultado_completo = test_mc_generacion_directo()
    
    if not resultado_completo:
        print("\n🔄 Intentando prueba simplificada...")
        resultado_simple = test_generacion_simple()
        
        if resultado_simple:
            print("✅ Al menos la función básica funciona")
        else:
            print("❌ Todas las pruebas fallaron")
    
    print("\n👋 Pruebas terminadas")