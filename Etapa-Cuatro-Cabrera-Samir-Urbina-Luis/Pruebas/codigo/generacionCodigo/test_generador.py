# test_mc_generacion.py
# PRUEBA DIRECTA del archivo mc_generacion.py

def test_mc_generacion_directo():
    """Prueba DIRECTA de mc_generacion.py"""
    
    print("🎯 PROBANDO mc_generacion.py DIRECTAMENTE")
    print("="*50)
    
    # PASO 1: Importar y crear generador
    from mc_generacion import GeneradorConRuntime
    
    gen = GeneradorConRuntime()
    print("✅ Generador creado")
    
    # PASO 2: Probar crear Runtime Library
    resultado = gen.crear_archivo_runtime("runtime_generado.asm")
    
    if resultado:
        print("✅ Runtime Library creada: runtime_generado.asm")
    else:
        print("❌ FALLÓ crear Runtime Library")
        return
    
    # PASO 3: Verificar archivo existe
    import os
    if os.path.exists("runtime_generado.asm"):
        print("✅ Archivo existe")
        
        # Leer y mostrar stats básicas
        with open("runtime_generado.asm", 'r', encoding='utf-8', errors='ignore') as f:
            contenido = f.read()
            
        print(f"📊 Líneas: {len(contenido.split())}")
        print(f"📊 Contiene SUMAR_ENTEROS: {'SUMAR_ENTEROS' in contenido}")
        print(f"📊 Contiene MODULO_ENTEROS: {'MODULO_ENTEROS' in contenido}")
        print(f"📊 Total PROC: {contenido.count('PROC')}")
        
    else:
        print("❌ Archivo NO existe")
    
    # PASO 4: Probar generar código
    print("\n🔧 Probando generar código...")
    
    gen.declarar_variable("numero", "STACK", "10")
    gen.generar_operacion_aritmetica(":+", "resultado", "numero", "5")
    gen.finalizar_programa()
    
    # Guardar programa completo
    gen.guardar_archivo("programa_test.asm")
    
    if os.path.exists("programa_test.asm"):
        print("✅ Programa completo generado: programa_test.asm")
    else:
        print("❌ Programa NO generado")

if __name__ == "__main__":
    test_mc_generacion_directo()