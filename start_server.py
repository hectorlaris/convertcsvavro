#!/usr/bin/env python
"""
Script para iniciar el servidor FastAPI del convertidor CSV a AVRO
"""

import uvicorn
import sys
from pathlib import Path

def main():
    """Función principal para iniciar el servidor"""
    
    print("🚀 Iniciando servidor CSV to AVRO API")
    print("=" * 50)
    
    # Verificar archivos necesarios
    required_files = [
        "generadorcsvavro.py",
        "api.py",
        "Esquema_AVRO.json"
    ]
    
    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print("❌ Archivos faltantes:")
        for file in missing_files:
            print(f"   - {file}")
        print("\n   Asegúrate de que todos los archivos necesarios estén presentes.")
        sys.exit(1)
    
    print("✅ Todos los archivos necesarios están presentes")
    
    # Crear directorio de salida si no existe
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    print(f"✅ Directorio de salida: {output_dir.absolute()}")
    
    # Configuración del servidor
    host = "0.0.0.0"
    port = 8000
    
    print(f"\n📡 Servidor iniciándose en: http://{host}:{port}")
    print(f"📖 Documentación disponible en: http://localhost:{port}/docs")
    print(f"📋 Documentación alternativa en: http://localhost:{port}/redoc")
    print("\n⚡ Para detener el servidor presiona Ctrl+C")
    print("=" * 50)
    
    try:
        # Iniciar servidor
        uvicorn.run(
            "api:app",
            host=host,
            port=port,
            reload=True,  # Recarga automática en desarrollo
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n\n👋 Servidor detenido por el usuario")
    except Exception as e:
        print(f"\n❌ Error al iniciar el servidor: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
