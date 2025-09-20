import requests
import json
from pathlib import Path

def test_api():
    """Script para probar el API del convertidor CSV a AVRO"""
    
    base_url = "http://localhost:8000"
    
    print("🧪 Iniciando pruebas del API CSV to AVRO")
    print("=" * 50)
    
    # 1. Probar endpoint de salud
    print("\n1. Probando endpoint de salud...")
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            print("✅ Servicio saludable:", response.json())
        else:
            print("❌ Error en health check:", response.status_code)
            return
    except requests.exceptions.ConnectionError:
        print("❌ No se puede conectar al servidor. ¿Está ejecutándose?")
        print("   Ejecuta: python api.py")
        return
    
    # 2. Probar endpoint raíz
    print("\n2. Probando endpoint raíz...")
    try:
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            print("✅ Información del servicio:", response.json())
        else:
            print("❌ Error en endpoint raíz:", response.status_code)
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # 3. Verificar archivos necesarios
    print("\n3. Verificando archivos necesarios...")
    csv_file = Path("Data/ArchivoCSV.csv")
    schema_file = Path("Esquema_AVRO.json")
    
    if not csv_file.exists():
        print(f"❌ Archivo CSV no encontrado: {csv_file}")
        print("   Crea un archivo CSV de ejemplo en la carpeta Data/")
        return
    else:
        print(f"✅ Archivo CSV encontrado: {csv_file}")
    
    if not schema_file.exists():
        print(f"❌ Archivo de esquema no encontrado: {schema_file}")
        print("   Asegúrate de tener el archivo Esquema_AVRO.json")
        return
    else:
        print(f"✅ Archivo de esquema encontrado: {schema_file}")
    
    # 4. Probar conversión con esquema por defecto
    print("\n4. Probando conversión con esquema por defecto...")
    try:
        files = {
            'csv_file': ('test.csv', open(csv_file, 'rb'), 'text/csv')
        }
        data = {
            'tipo_entidad': 1,
            'codigo_entidad': '123456',
            'nombre_entidad': 'TEST_API',
            'fecha_corte': 2024
        }
        
        response = requests.post(f"{base_url}/convert-with-default-schema", files=files, data=data)
        files['csv_file'][1].close()  # Cerrar archivo
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Conversión exitosa:")
            print(f"   - Registros válidos: {result.get('registros_validos', 0)}")
            print(f"   - Registros inválidos: {result.get('registros_invalidos', 0)}")
            print(f"   - Archivo generado: {result.get('avro_file_path', 'N/A')}")
            
            if result.get('inconsistencias'):
                print(f"   - Inconsistencias encontradas: {len(result['inconsistencias'])}")
                for i, inc in enumerate(result['inconsistencias'][:3]):  # Mostrar solo las primeras 3
                    print(f"     {i+1}. {inc}")
                if len(result['inconsistencias']) > 3:
                    print(f"     ... y {len(result['inconsistencias']) - 3} más")
        else:
            print(f"❌ Error en conversión: {response.status_code}")
            print(f"   Respuesta: {response.text}")
            
    except Exception as e:
        print(f"❌ Error al probar conversión: {e}")
    
    # 5. Probar conversión con esquema personalizado
    print("\n5. Probando conversión con esquema personalizado...")
    try:
        files = {
            'csv_file': ('test.csv', open(csv_file, 'rb'), 'text/csv'),
            'schema_file': ('schema.json', open(schema_file, 'rb'), 'application/json')
        }
        data = {
            'tipo_entidad': 1,
            'codigo_entidad': '789012',
            'nombre_entidad': 'TEST_CUSTOM',
            'fecha_corte': 2024
        }
        
        response = requests.post(f"{base_url}/convert", files=files, data=data)
        files['csv_file'][1].close()
        files['schema_file'][1].close()
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Conversión con esquema personalizado exitosa:")
            print(f"   - Registros válidos: {result.get('registros_validos', 0)}")
            print(f"   - Registros inválidos: {result.get('registros_invalidos', 0)}")
            print(f"   - Archivo generado: {result.get('avro_file_path', 'N/A')}")
        else:
            print(f"❌ Error en conversión personalizada: {response.status_code}")
            print(f"   Respuesta: {response.text}")
            
    except Exception as e:
        print(f"❌ Error al probar conversión personalizada: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Pruebas completadas!")
    print(f"📖 Documentación disponible en: {base_url}/docs")
    print(f"📋 Documentación alternativa en: {base_url}/redoc")

if __name__ == "__main__":
    test_api()
