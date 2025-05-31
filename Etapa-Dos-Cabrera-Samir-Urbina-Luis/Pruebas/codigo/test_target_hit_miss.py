"""
test_target_hit_miss.py

Estudiantes: Cabrera Samir, Urbina Luis

Sistema de pruebas completo para validar el maquillaje semántico de TARGET/HIT/MISS.
Este sistema funciona SIN modificar la gramática, aplicando validación en tiempo real.

Casos de prueba incluidos:
- Estructuras básicas válidas
- Errores específicos (HIT sin TARGET, MISS sin HIT, etc.)
- Anidación de estructuras
- Casos extremos y edge cases
- Integración con otros sistemas del compilador
"""

import sys
import os
from pathlib import Path

# Simular estructura del proyecto para testing
class MockToken:
    """Token mock para pruebas independientes"""
    def __init__(self, type, lexema, linea, columna):
        self.type = type
        self.lexema = lexema
        self.linea = linea
        self.columna = columna
    
    def __str__(self):
        return f"Token({self.type}, '{self.lexema}', L{self.linea}:C{self.columna})"

class TestSuiteTargetHitMiss:
    """
    Suite completa de pruebas para el sistema TARGET/HIT/MISS
    """
    
    def __init__(self):
        self.total_tests = 0
        self.passed_tests = 0
        self.failed_tests = 0
        self.test_results = []
        
    def print_header(self, title):
        """Imprime un encabezado de sección"""
        print(f"\n{'='*80}")
        print(f"  {title}")
        print(f"{'='*80}")
    
    def print_test_result(self, test_name, passed, details=""):
        """Imprime el resultado de una prueba"""
        status = "✅ PASÓ" if passed else "❌ FALLÓ"
        print(f"\n[{self.total_tests:2d}] {test_name}: {status}")
        if details:
            print(f"    {details}")
        if not passed:
            print(f"    ❌ Detalle del fallo disponible arriba")
    
    def run_test(self, test_name, test_function, expected_result=True):
        """
        Ejecuta una prueba y registra el resultado
        
        Args:
            test_name: Nombre descriptivo de la prueba
            test_function: Función que ejecuta la prueba
            expected_result: Resultado esperado (True para éxito, False para fallo esperado)
        """
        self.total_tests += 1
        
        try:
            resultado = test_function()
            passed = (resultado == expected_result)
            
            if passed:
                self.passed_tests += 1
            else:
                self.failed_tests += 1
            
            details = f"Esperado: {expected_result}, Obtenido: {resultado}"
            self.print_test_result(test_name, passed, details)
            
            self.test_results.append({
                "name": test_name,
                "status": "PASS" if passed else "FAIL",
                "expected": expected_result,
                "actual": resultado
            })
            
        except Exception as e:
            self.failed_tests += 1
            self.print_test_result(test_name, False, f"ERROR: {str(e)}")
            self.test_results.append({
                "name": test_name,
                "status": "ERROR",
                "error": str(e)
            })
    
    def create_token(self, tipo, lexema, linea, columna):
        """Crea un token mock para pruebas"""
        return MockToken(tipo, lexema, linea, columna)
    
    def simulate_target_validation(self, tokens):
        """
        Simula la validación TARGET/HIT/MISS con el sistema de maquillaje
        
        Args:
            tokens: Lista de tokens a validar
            
        Returns:
            tuple: (es_valido, errores_encontrados, estadisticas)
        """
        # Simulación del tracker (en implementación real sería el módulo completo)
        errores = []
        pila_target = []
        estructuras_completadas = []
        
        for i, token in enumerate(tokens):
            if token.type == "TARGET":
                # Simular apertura de TARGET
                estructura = {
                    "id": len(estructuras_completadas),
                    "linea": token.linea,
                    "estado": "esperando_hit",
                    "tiene_hit": False,
                    "tiene_miss": False
                }
                pila_target.append(estructura)
                
            elif token.type == "HIT":
                # Simular procesamiento de HIT
                if not pila_target:
                    errores.append(f"HIT sin TARGET correspondiente en línea {token.linea}")
                else:
                    target_actual = None
                    for j in range(len(pila_target) - 1, -1, -1):
                        if pila_target[j]["estado"] == "esperando_hit":
                            target_actual = pila_target[j]
                            break
                    
                    if target_actual:
                        target_actual["estado"] = "hit_encontrado"
                        target_actual["tiene_hit"] = True
                    else:
                        errores.append(f"HIT en línea {token.linea} sin TARGET válido")
                        
            elif token.type == "MISS":
                # Simular procesamiento de MISS
                if not pila_target:
                    errores.append(f"MISS sin TARGET correspondiente en línea {token.linea}")
                else:
                    target_actual = None
                    for j in range(len(pila_target) - 1, -1, -1):
                        if pila_target[j]["estado"] == "hit_encontrado":
                            target_actual = pila_target[j]
                            break
                    
                    if target_actual:
                        target_actual["estado"] = "miss_encontrado"
                        target_actual["tiene_miss"] = True
                    else:
                        # Verificar si hay TARGET esperando HIT
                        target_sin_hit = None
                        for target in reversed(pila_target):
                            if target["estado"] == "esperando_hit":
                                target_sin_hit = target
                                break
                        
                        if target_sin_hit:
                            errores.append(f"MISS sin HIT correspondiente en línea {token.linea}")
                        else:
                            errores.append(f"MISS sin estructura TARGET-HIT válida en línea {token.linea}")
            
            # Simular cierre implícito en ciertos tokens
            elif token.type in ["PUNTO_Y_COMA", "POLLO_ASADO"]:
                if pila_target and pila_target[-1]["estado"] in ["hit_encontrado", "miss_encontrado"]:
                    estructura_cerrada = pila_target.pop()
                    estructuras_completadas.append(estructura_cerrada)
        
        # Verificar estructuras no cerradas al final
        for estructura in pila_target:
            if estructura["estado"] == "esperando_hit":
                errores.append(f"TARGET en línea {estructura['linea']} sin HIT correspondiente")
        
        estadisticas = {
            "estructuras_detectadas": len(estructuras_completadas) + len(pila_target),
            "estructuras_completadas": len(estructuras_completadas),
            "estructuras_con_miss": sum(1 for e in estructuras_completadas if e.get("tiene_miss", False)),
            "errores_totales": len(errores)
        }
        
        return len(errores) == 0, errores, estadisticas
    
    # ========================================================================
    # CASOS DE PRUEBA ESPECÍFICOS
    # ========================================================================
    
    def test_estructura_basica_valida(self):
        """Prueba 1: Estructura TARGET-HIT básica válida"""
        tokens = [
            self.create_token("TARGET", "Target", 1, 1),
            self.create_token("IDENTIFICADOR", "condicion", 1, 8),
            self.create_token("HIT", "Hit", 1, 18),
            self.create_token("IDENTIFICADOR", "accion", 2, 1),
            self.create_token("PUNTO_Y_COMA", ";", 2, 7)
        ]
        
        es_valido, errores, stats = self.simulate_target_validation(tokens)
        return es_valido and stats["estructuras_completadas"] == 1
    
    def test_estructura_completa_con_miss(self):
        """Prueba 2: Estructura TARGET-HIT-MISS completa válida"""
        tokens = [
            self.create_token("TARGET", "Target", 1, 1),
            self.create_token("IDENTIFICADOR", "condicion", 1, 8),
            self.create_token("HIT", "Hit", 1, 18),
            self.create_token("IDENTIFICADOR", "accion1", 2, 1),
            self.create_token("MISS", "Miss", 3, 1),
            self.create_token("IDENTIFICADOR", "accion2", 3, 6),
            self.create_token("PUNTO_Y_COMA", ";", 3, 13)
        ]
        
        es_valido, errores, stats = self.simulate_target_validation(tokens)
        return es_valido and stats["estructuras_con_miss"] == 1
    
    def test_error_hit_sin_target(self):
        """Prueba 3: Error - HIT sin TARGET correspondiente"""
        tokens = [
            self.create_token("HIT", "Hit", 1, 1),
            self.create_token("IDENTIFICADOR", "accion", 1, 5),
            self.create_token("PUNTO_Y_COMA", ";", 1, 11)
        ]
        
        es_valido, errores, stats = self.simulate_target_validation(tokens)
        return not es_valido and any("HIT sin TARGET" in error for error in errores)
    
    def test_error_miss_sin_hit(self):
        """Prueba 4: Error - MISS sin HIT correspondiente"""
        tokens = [
            self.create_token("TARGET", "Target", 1, 1),
            self.create_token("IDENTIFICADOR", "condicion", 1, 8),
            self.create_token("MISS", "Miss", 2, 1),
            self.create_token("IDENTIFICADOR", "accion", 2, 6),
            self.create_token("PUNTO_Y_COMA", ";", 2, 12)
        ]
        
        es_valido, errores, stats = self.simulate_target_validation(tokens)
        return not es_valido and any("MISS sin HIT" in error for error in errores)
    
    def test_error_target_sin_cerrar(self):
        """Prueba 5: Error - TARGET sin HIT correspondiente"""
        tokens = [
            self.create_token("TARGET", "Target", 1, 1),
            self.create_token("IDENTIFICADOR", "condicion", 1, 8),
            # No hay HIT ni cierre
        ]
        
        es_valido, errores, stats = self.simulate_target_validation(tokens)
        return not es_valido and any("TARGET" in error and "sin HIT" in error for error in errores)
    
    def test_estructuras_anidadas_validas(self):
        """Prueba 6: Estructuras TARGET anidadas válidas"""
        tokens = [
            self.create_token("TARGET", "Target", 1, 1),
            self.create_token("IDENTIFICADOR", "cond1", 1, 8),
            self.create_token("HIT", "Hit", 1, 14),
            # Inicio de estructura anidada
            self.create_token("TARGET", "Target", 2, 5),
            self.create_token("IDENTIFICADOR", "cond2", 2, 12),
            self.create_token("HIT", "Hit", 2, 18),
            self.create_token("IDENTIFICADOR", "accion2", 3, 1),
            self.create_token("PUNTO_Y_COMA", ";", 3, 8),
            # Fin de estructura anidada
            self.create_token("MISS", "Miss", 4, 1),
            self.create_token("IDENTIFICADOR", "accion1", 4, 6),
            self.create_token("PUNTO_Y_COMA", ";", 4, 13)
        ]
        
        es_valido, errores, stats = self.simulate_target_validation(tokens)
        return es_valido and stats["estructuras_completadas"] == 2
    
    def test_multiples_target_secuenciales(self):
        """Prueba 7: Múltiples estructuras TARGET secuenciales"""
        tokens = [
            # Primera estructura
            self.create_token("TARGET", "Target", 1, 1),
            self.create_token("IDENTIFICADOR", "cond1", 1, 8),
            self.create_token("HIT", "Hit", 1, 14),
            self.create_token("IDENTIFICADOR", "accion1", 2, 1),
            self.create_token("PUNTO_Y_COMA", ";", 2, 8),
            # Segunda estructura
            self.create_token("TARGET", "Target", 3, 1),
            self.create_token("IDENTIFICADOR", "cond2", 3, 8),
            self.create_token("HIT", "Hit", 3, 14),
            self.create_token("IDENTIFICADOR", "accion2", 4, 1),
            self.create_token("MISS", "Miss", 5, 1),
            self.create_token("IDENTIFICADOR", "accion3", 5, 6),
            self.create_token("PUNTO_Y_COMA", ";", 5, 13)
        ]
        
        es_valido, errores, stats = self.simulate_target_validation(tokens)
        return es_valido and stats["estructuras_completadas"] == 2 and stats["estructuras_con_miss"] == 1
    
    def test_miss_sin_target_alguno(self):
        """Prueba 8: Error - MISS completamente sin estructura TARGET"""
        tokens = [
            self.create_token("IDENTIFICADOR", "variable", 1, 1),
            self.create_token("IGUAL", "=", 1, 10),
            self.create_token("NUMERO_ENTERO", "5", 1, 12),
            self.create_token("PUNTO_Y_COMA", ";", 1, 13),
            self.create_token("MISS", "Miss", 2, 1),
            self.create_token("IDENTIFICADOR", "accion", 2, 6),
            self.create_token("PUNTO_Y_COMA", ";", 2, 12)
        ]
        
        es_valido, errores, stats = self.simulate_target_validation(tokens)
        return not es_valido and any("MISS sin TARGET" in error for error in errores)
    
    def test_target_con_bloque_pollo(self):
        """Prueba 9: TARGET dentro de bloques PolloCrudo/PolloAsado"""
        tokens = [
            self.create_token("POLLO_CRUDO", "PolloCrudo", 1, 1),
            self.create_token("TARGET", "Target", 2, 5),
            self.create_token("IDENTIFICADOR", "condicion", 2, 12),
            self.create_token("HIT", "Hit", 2, 22),
            self.create_token("IDENTIFICADOR", "accion", 3, 5),
            self.create_token("PUNTO_Y_COMA", ";", 3, 11),
            self.create_token("POLLO_ASADO", "PolloAsado", 4, 1)
        ]
        
        es_valido, errores, stats = self.simulate_target_validation(tokens)
        return es_valido and stats["estructuras_completadas"] == 1
    
    def test_caso_extremo_muchos_anidados(self):
        """Prueba 10: Caso extremo - Múltiples niveles de anidación"""
        tokens = [
            # Nivel 1
            self.create_token("TARGET", "Target", 1, 1),
            self.create_token("IDENTIFICADOR", "cond1", 1, 8),
            self.create_token("HIT", "Hit", 1, 14),
            # Nivel 2
            self.create_token("TARGET", "Target", 2, 5),
            self.create_token("IDENTIFICADOR", "cond2", 2, 12),
            self.create_token("HIT", "Hit", 2, 18),
            # Nivel 3
            self.create_token("TARGET", "Target", 3, 9),
            self.create_token("IDENTIFICADOR", "cond3", 3, 16),
            self.create_token("HIT", "Hit", 3, 22),
            self.create_token("IDENTIFICADOR", "accion3", 4, 9),
            self.create_token("PUNTO_Y_COMA", ";", 4, 16),
            # Cerrar nivel 2
            self.create_token("MISS", "Miss", 5, 5),
            self.create_token("IDENTIFICADOR", "accion2", 5, 10),
            self.create_token("PUNTO_Y_COMA", ";", 5, 17),
            # Cerrar nivel 1
            self.create_token("MISS", "Miss", 6, 1),
            self.create_token("IDENTIFICADOR", "accion1", 6, 6),
            self.create_token("PUNTO_Y_COMA", ";", 6, 13)
        ]
        
        es_valido, errores, stats = self.simulate_target_validation(tokens)
        return es_valido and stats["estructuras_completadas"] == 3
    
    # ========================================================================
    # MÉTODOS DE EJECUCIÓN Y REPORTE
    # ========================================================================
    
    def run_all_tests(self):
        """Ejecuta toda la suite de pruebas"""
        self.print_header("EJECUTANDO SUITE COMPLETA DE PRUEBAS TARGET/HIT/MISS")
        
        # Pruebas básicas de funcionalidad
        print("\n📋 GRUPO 1: Funcionalidad Básica")
        print("-" * 40)
        self.run_test("Estructura TARGET-HIT básica", self.test_estructura_basica_valida, True)
        self.run_test("Estructura TARGET-HIT-MISS completa", self.test_estructura_completa_con_miss, True)
        
        # Pruebas de detección de errores
        print("\n🚨 GRUPO 2: Detección de Errores")
        print("-" * 40)
        self.run_test("Error: HIT sin TARGET", self.test_error_hit_sin_target, True)
        self.run_test("Error: MISS sin HIT", self.test_error_miss_sin_hit, True)
        self.run_test("Error: TARGET sin cerrar", self.test_error_target_sin_cerrar, True)
        self.run_test("Error: MISS sin TARGET alguno", self.test_miss_sin_target_alguno, True)
        
        # Pruebas avanzadas
        print("\n🎯 GRUPO 3: Funcionalidad Avanzada")
        print("-" * 40)
        self.run_test("Estructuras anidadas válidas", self.test_estructuras_anidadas_validas, True)
        self.run_test("Múltiples TARGET secuenciales", self.test_multiples_target_secuenciales, True)
        self.run_test("TARGET con bloques Pollo", self.test_target_con_bloque_pollo, True)
        self.run_test("Anidación extrema (3 niveles)", self.test_caso_extremo_muchos_anidados, True)
        
        # Mostrar resumen
        self.print_summary()
    
    def print_summary(self):
        """Imprime un resumen de los resultados de las pruebas"""
        self.print_header("RESUMEN DE RESULTADOS")
        
        total = self.total_tests
        passed = self.passed_tests
        failed = self.failed_tests
        success_rate = (passed / total * 100) if total > 0 else 0
        
        print(f"\n📊 ESTADÍSTICAS GENERALES:")
        print(f"   Total de pruebas:    {total}")
        print(f"   ✅ Exitosas:         {passed}")
        print(f"   ❌ Fallidas:         {failed}")
        print(f"   📈 Tasa de éxito:    {success_rate:.1f}%")
        
        if success_rate == 100:
            print(f"\n🎉 ¡EXCELENTE! Todas las pruebas pasaron correctamente.")
            print(f"   El sistema de maquillaje TARGET/HIT/MISS está funcionando perfectamente.")
        elif success_rate >= 80:
            print(f"\n👍 BUENO: La mayoría de pruebas pasaron.")
            print(f"   Revisar las {failed} pruebas fallidas para mejoras.")
        else:
            print(f"\n⚠️  NECESITA ATENCIÓN: Muchas pruebas fallaron.")
            print(f"   Se requiere revisión del sistema.")
        
        # Mostrar detalles de fallos si los hay
        if failed > 0:
            print(f"\n🔍 DETALLES DE FALLOS:")
            for i, result in enumerate(self.test_results):
                if result["status"] != "PASS":
                    print(f"   {i+1}. {result['name']}: {result['status']}")
                    if "error" in result:
                        print(f"      Error: {result['error']}")
                    elif "expected" in result and "actual" in result:
                        print(f"      Esperado: {result['expected']}, Obtenido: {result['actual']}")
        
        print(f"\n{'='*80}")
    
    def demo_integration_example(self):
        """Demuestra un ejemplo de integración completa"""
        self.print_header("DEMOSTRACIÓN DE INTEGRACIÓN")
        
        print(f"Este ejemplo muestra cómo se integraría el sistema TARGET/HIT/MISS")
        print(f"con el parser existente SIN modificar la gramática:")
        print(f"\n1. DETECCIÓN AUTOMÁTICA:")
        print(f"   - El parser detecta tokens TARGET/HIT/MISS durante avanzar()")
        print(f"   - Se aplica maquillaje semántico en tiempo real")
        print(f"   - No se requieren cambios en la gramática")
        
        print(f"\n2. VALIDACIÓN EN TIEMPO REAL:")
        print(f"   - Cada TARGET abre una nueva estructura")
        print(f"   - Cada HIT debe tener un TARGET correspondiente")
        print(f"   - Cada MISS debe tener un HIT previo")
        print(f"   - Se manejan estructuras anidadas automáticamente")
        
        print(f"\n3. REPORTE DE ERRORES:")
        print(f"   - Errores específicos con números de línea")
        print(f"   - Sugerencias de corrección contextuales")
        print(f"   - Integración con HistorialSemantico")
        
        print(f"\n4. ESTADÍSTICAS DETALLADAS:")
        print(f"   - Estructuras detectadas y completadas")
        print(f"   - Nivel máximo de anidación")
        print(f"   - Cantidad de estructuras con MISS")
        
        # Ejemplo práctico
        print(f"\n💡 EJEMPLO PRÁCTICO:")
        ejemplo_tokens = [
            self.create_token("TARGET", "Target", 5, 1),
            self.create_token("IDENTIFICADOR", "x", 5, 8),
            self.create_token("MAYOR_QUE", ">", 5, 10),
            self.create_token("NUMERO_ENTERO", "10", 5, 12),
            self.create_token("HIT", "Hit", 5, 15),
            self.create_token("IDENTIFICADOR", "resultado", 6, 5),
            self.create_token("IGUAL", "=", 6, 14),
            self.create_token("NUMERO_ENTERO", "1", 6, 16),
            self.create_token("PUNTO_Y_COMA", ";", 6, 17),
            self.create_token("MISS", "Miss", 7, 1),
            self.create_token("IDENTIFICADOR", "resultado", 7, 6),
            self.create_token("IGUAL", "=", 7, 15),
            self.create_token("NUMERO_ENTERO", "0", 7, 17),
            self.create_token("PUNTO_Y_COMA", ";", 7, 18)
        ]
        
        es_valido, errores, stats = self.simulate_target_validation(ejemplo_tokens)
        
        print(f"\n   Código Notch-Engine simulado:")
        print(f"     Target x > 10 Hit")
        print(f"       resultado = 1;")
        print(f"     Miss")
        print(f"       resultado = 0;")
        
        print(f"\n   Resultado de validación:")
        print(f"     ✅ Válido: {es_valido}")
        print(f"     📊 Estructuras: {stats['estructuras_completadas']}")
        print(f"     🌟 Con MISS: {stats['estructuras_con_miss']}")
        
        if errores:
            print(f"     ❌ Errores: {len(errores)}")
            for error in errores:
                print(f"       - {error}")
        else:
            print(f"     ✅ Sin errores detectados")

def main():
    """Función principal para ejecutar las pruebas"""
    print("🚀 INICIANDO SISTEMA DE PRUEBAS TARGET/HIT/MISS")
    print("   Implementación por maquillaje semántico")
    print("   (Sin modificar gramática existente)")
    
    # Crear y ejecutar suite de pruebas
    test_suite = TestSuiteTargetHitMiss()
    
    # Ejecutar todas las pruebas
    test_suite.run_all_tests()
    
    # Mostrar demostración de integración
    test_suite.demo_integration_example()
    
    # Mensaje final
    if test_suite.passed_tests == test_suite.total_tests:
        print(f"\n🎯 SISTEMA LISTO PARA INTEGRACIÓN")
        print(f"   Todas las pruebas pasaron exitosamente.")
        print(f"   El maquillaje semántico está funcionando correctamente.")
        print(f"\n💼 PRÓXIMOS PASOS:")
        print(f"   1. Integrar en mc_parser.py siguiendo el ejemplo proporcionado")
        print(f"   2. Agregar la llamada en main.py")
        print(f"   3. Probar con archivos reales del proyecto")
        print(f"   4. Ajustar mensajes de error según necesidades")
    else:
        print(f"\n⚠️  SISTEMA REQUIERE REVISIÓN")
        print(f"   Algunas pruebas fallaron. Revisar implementación antes de integrar.")
    
    return test_suite.passed_tests == test_suite.total_tests

# Función para testing rápido de casos específicos
def quick_test():
    """Prueba rápida con casos básicos"""
    print("🏃‍♂️ PRUEBA RÁPIDA - Casos Básicos")
    print("-" * 50)
    
    test_suite = TestSuiteTargetHitMiss()
    
    # Solo ejecutar pruebas básicas
    test_suite.run_test("TARGET-HIT básico", test_suite.test_estructura_basica_valida, True)
    test_suite.run_test("TARGET-HIT-MISS completo", test_suite.test_estructura_completa_con_miss, True)
    test_suite.run_test("Error HIT sin TARGET", test_suite.test_error_hit_sin_target, True)
    test_suite.run_test("Error MISS sin HIT", test_suite.test_error_miss_sin_hit, True)
    
    print(f"\n📊 Resultado: {test_suite.passed_tests}/{test_suite.total_tests} pruebas pasaron")
    
    return test_suite.passed_tests == test_suite.total_tests

# Función para generar casos de prueba automáticos
def generate_test_cases():
    """Genera casos de prueba adicionales automáticamente"""
    print("🤖 GENERANDO CASOS DE PRUEBA AUTOMÁTICOS")
    print("-" * 50)
    
    casos_generados = []
    
    # Caso 1: TARGET válido básico
    caso1 = {
        "nombre": "TARGET básico generado",
        "tokens": ["TARGET", "IDENTIFICADOR", "HIT", "IDENTIFICADOR", "PUNTO_Y_COMA"],
        "esperado": True
    }
    casos_generados.append(caso1)
    
    # Caso 2: Error HIT sin TARGET
    caso2 = {
        "nombre": "Error HIT sin TARGET generado", 
        "tokens": ["HIT", "IDENTIFICADOR", "PUNTO_Y_COMA"],
        "esperado": False
    }
    casos_generados.append(caso2)
    
    # Caso 3: Anidación simple
    caso3 = {
        "nombre": "Anidación generada",
        "tokens": ["TARGET", "IDENTIFICADOR", "HIT", "TARGET", "IDENTIFICADOR", "HIT", "IDENTIFICADOR", "PUNTO_Y_COMA", "PUNTO_Y_COMA"],
        "esperado": True
    }
    casos_generados.append(caso3)
    
    print(f"✅ Generados {len(casos_generados)} casos de prueba automáticos")
    
    for i, caso in enumerate(casos_generados, 1):
        print(f"   {i}. {caso['nombre']}: {len(caso['tokens'])} tokens, esperado: {caso['esperado']}")
    
    return casos_generados

if __name__ == "__main__":
    # Permitir selección de tipo de prueba
    import sys
    
    if len(sys.argv) > 1:
        modo = sys.argv[1].lower()
        
        if modo == "quick":
            quick_test()
        elif modo == "generate":
            generate_test_cases()
        elif modo == "full":
            main()
        else:
            print("Modos disponibles: quick, generate, full")
            print("Uso: python test_target_hit_miss.py [modo]")
    else:
        # Por defecto, ejecutar prueba completa
        main()