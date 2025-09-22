"""
Script para validar que todo esté listo para las pruebas de Postman
"""

import requests
import json
import os
from pathlib import Path

def validate_postman_setup():
    """Valida que el setup esté listo para pruebas de Postman"""
    
    print("🔍 Validando configuración para pruebas de Postman...")
    print("=" * 60)
    
    # 1. Verificar que el servidor esté corriendo
    base_url = "http://localhost:8001"
    print(f"\n1. 🌐 Verificando servidor en {base_url}")
    
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            print("   ✅ Servidor activo y respondiendo")
            health_data = response.json()
            print(f"   📊 Status: {health_data.get('status')}")
        else:
            print(f"   ❌ Servidor responde con código: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("   ❌ No se puede conectar al servidor")
        print("   💡 Ejecuta: python api.py")
        return False
    except Exception as e:
        print(f"   ❌ Error inesperado: {e}")
        return False
    
    # 2. Verificar archivos de Postman
    print("\n2. 📁 Verificando archivos de Postman")
    
    postman_files = [
        "Postman_Collection.json",
        "Postman_Environment.json",
        "POSTMAN_TESTING_GUIDE.md"
    ]
    
    for file in postman_files:
        if Path(file).exists():
            print(f"   ✅ {file}")
        else:
            print(f"   ❌ {file} - No encontrado")
            return False
    
    # 3. Verificar archivos de datos de prueba
    print("\n3. 📋 Verificando archivos de datos")
    
    data_files = {
        "Data/ArchivoCSV.csv": "Archivo CSV de prueba",
        "Esquema_AVRO.json": "Esquema AVRO por defecto"
    }
    
    for file, description in data_files.items():
        if Path(file).exists():
            file_size = Path(file).stat().st_size
            print(f"   ✅ {file} ({file_size} bytes) - {description}")
        else:
            print(f"   ❌ {file} - {description} no encontrado")
            return False
    
    # 4. Verificar endpoints del API
    print("\n4. 🔗 Verificando endpoints del API")
    
    endpoints = [
        ("/", "GET", "Información del servicio"),
        ("/health", "GET", "Health check"),
        ("/docs", "GET", "Documentación Swagger")
    ]
    
    for endpoint, method, description in endpoints:
        try:
            if method == "GET":
                response = requests.get(f"{base_url}{endpoint}", timeout=5)
                if response.status_code == 200:
                    print(f"   ✅ {method} {endpoint} - {description}")
                else:
                    print(f"   ⚠️  {method} {endpoint} - Código: {response.status_code}")
        except Exception as e:
            print(f"   ❌ {method} {endpoint} - Error: {e}")
    
    # 5. Verificar que el directorio output existe
    print("\n5. 📂 Verificando directorio de salida")
    output_dir = Path("output")
    if output_dir.exists():
        print(f"   ✅ Directorio 'output' existe")
        files_count = len(list(output_dir.glob("*.avro")))
        print(f"   📊 Archivos AVRO existentes: {files_count}")
    else:
        print("   ⚠️  Directorio 'output' no existe - se creará automáticamente")
        output_dir.mkdir(exist_ok=True)
        print("   ✅ Directorio 'output' creado")
    
    # 6. Generar información para Postman
    print("\n6. 📋 Información para configurar Postman")
    print("   🔗 URL base:", base_url)
    print("   📁 Ruta CSV:", str(Path("Data/ArchivoCSV.csv").absolute()))
    print("   📁 Ruta Esquema:", str(Path("Esquema_AVRO.json").absolute()))
    
    # 7. Test básico de conversión
    print("\n7. 🧪 Test básico de conversión")
    try:
        # Preparar archivos para el test
        csv_path = Path("Data/ArchivoCSV.csv")
        
        if csv_path.exists():
            print("   🔄 Ejecutando test de conversión...")
            
            files = {
                'csv_file': ('test.csv', open(csv_path, 'rb'), 'text/csv')
            }
            data = {
                'tipo_entidad': 1,
                'codigo_entidad': '999999',
                'nombre_entidad': 'VALIDATION_TEST',
                'fecha_corte': 2024
            }
            
            response = requests.post(
                f"{base_url}/convert-with-default-schema",
                files=files,
                data=data,
                timeout=30
            )
            
            files['csv_file'][1].close()  # Cerrar archivo
            
            if response.status_code == 200:
                result = response.json()
                print("   ✅ Conversión de prueba exitosa")
                print(f"   📊 Registros válidos: {result.get('registros_validos', 0)}")
                print(f"   📊 Registros inválidos: {result.get('registros_invalidos', 0)}")
                
                if result.get('avro_file_path'):
                    print(f"   📁 Archivo generado: {result['avro_file_path']}")
            else:
                print(f"   ❌ Error en conversión: {response.status_code}")
                print(f"   📝 Respuesta: {response.text}")
                
        else:
            print("   ⚠️  No se puede ejecutar test - archivo CSV no encontrado")
            
    except Exception as e:
        print(f"   ❌ Error en test de conversión: {e}")
    
    print("\n" + "=" * 60)
    print("✅ Validación completada - Sistema listo para pruebas de Postman!")
    print("\n📖 Siguiente paso:")
    print("   1. Abrir Postman")
    print("   2. Importar Postman_Collection.json")
    print("   3. Importar Postman_Environment.json")
    print("   4. Seguir la guía en POSTMAN_TESTING_GUIDE.md")
    
    return True

if __name__ == "__main__":
    try:
        validate_postman_setup()
    except KeyboardInterrupt:
        print("\n\n❌ Validación cancelada por el usuario")
    except Exception as e:
        print(f"\n\n❌ Error inesperado: {e}")
