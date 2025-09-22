from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any
import tempfile
import os
import json
from pathlib import Path
import shutil
from generadorcsvavro import GeneradorCsvAvro

app = FastAPI(
    title="Convertidor CSV a AVRO",
    description="Microservicio para convertir archivos CSV a formato AVRO con validación de esquemas",
    version="1.0.0"
)

class ConversionRequest(BaseModel):
    tipo_entidad: int
    codigo_entidad: str
    nombre_entidad: str
    fecha_corte: int

class ConversionResponse(BaseModel):
    success: bool
    message: str
    registros_validos: int
    registros_invalidos: int
    inconsistencias: Optional[list] = None
    avro_file_path: Optional[str] = None

@app.get("/")
async def root():
    """Endpoint raíz con información básica del servicio"""
    return {
        "service": "Convertidor CSV a AVRO",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "convert": "/convert - POST - Convierte CSV a AVRO",
            "health": "/health - GET - Estado del servicio",
            "docs": "/docs - Documentación interactiva"
        }
    }

@app.get("/health")
async def health_check():
    """Endpoint de verificación de salud del servicio"""
    return {"status": "healthy", "service": "csv-to-avro-converter"}

@app.post("/convert", response_model=ConversionResponse)
async def convert_csv_to_avro(
    tipo_entidad: int = Form(...),
    codigo_entidad: str = Form(...),
    nombre_entidad: str = Form(...),
    fecha_corte: int = Form(...),
    csv_file: UploadFile = File(...),
    schema_file: UploadFile = File(...)
):
    """
    Convierte un archivo CSV a formato AVRO usando el esquema proporcionado
    
    - **tipo_entidad**: Tipo de entidad (int)
    - **codigo_entidad**: Código de la entidad (string)
    - **nombre_entidad**: Nombre de la entidad (string)
    - **fecha_corte**: Fecha de corte (int)
    - **csv_file**: Archivo CSV a convertir
    - **schema_file**: Archivo de esquema AVRO en formato JSON
    """
    
    # Validar tipos de archivo
    if not csv_file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="El archivo debe ser un CSV")
    
    if not schema_file.filename.endswith('.json'):
        raise HTTPException(status_code=400, detail="El esquema debe ser un archivo JSON")
    
    # Crear directorio temporal para procesar archivos
    with tempfile.TemporaryDirectory() as temp_dir:
        try:
            # Guardar archivos temporalmente
            csv_path = Path(temp_dir) / "input.csv"
            schema_path = Path(temp_dir) / "schema.json"
            avro_path = Path(temp_dir) / "output.avro"
            log_path = Path(temp_dir) / "inconsistencias.log"
            
            # Escribir archivos
            with open(csv_path, "wb") as f:
                shutil.copyfileobj(csv_file.file, f)
            
            with open(schema_path, "wb") as f:
                shutil.copyfileobj(schema_file.file, f)
            
            # Validar que el esquema JSON es válido
            try:
                with open(schema_path, 'r', encoding='utf-8') as f:
                    json.load(f)
            except json.JSONDecodeError:
                raise HTTPException(status_code=400, detail="El archivo de esquema no es un JSON válido")
            
            # Crear instancia del generador
            generador = GeneradorCsvAvro(
                tipo_entidad=tipo_entidad,
                codigo_entidad=codigo_entidad,
                nombre_entidad=nombre_entidad,
                fecha_corte=fecha_corte,
                ruta_schema=str(schema_path),
                ruta_csv=str(csv_path)
            )
            
            # Ejecutar conversión
            generador.ejecutar(str(avro_path), str(log_path))
            
            # Leer inconsistencias si existen
            inconsistencias = []
            if log_path.exists():
                with open(log_path, 'r', encoding='utf-8') as f:
                    inconsistencias = [line.strip() for line in f.readlines()]
            
            # Contar registros
            registros_validos = len(generador.garantias) if hasattr(generador, 'garantias') else 0
            registros_invalidos = len(inconsistencias)
            
            # Copiar archivo AVRO a ubicación permanente (opcional)
            output_dir = Path("output")
            output_dir.mkdir(exist_ok=True)
            final_avro_path = output_dir / f"converted_{tipo_entidad}_{codigo_entidad}_{fecha_corte}.avro"
            
            if avro_path.exists():
                shutil.copy2(avro_path, final_avro_path)
                
                # Solo devolver el nombre del archivo, no la ruta completa
                filename_only = final_avro_path.name
                
                return ConversionResponse(
                    success=True,
                    message="Conversión completada exitosamente",
                    registros_validos=registros_validos,
                    registros_invalidos=registros_invalidos,
                    inconsistencias=inconsistencias if inconsistencias else None,
                    avro_file_path=filename_only  # Solo el nombre del archivo
                )
            else:
                return ConversionResponse(
                    success=False,
                    message="Error: No se pudo generar el archivo AVRO",
                    registros_validos=0,
                    registros_invalidos=registros_invalidos,
                    inconsistencias=inconsistencias
                )
                
        except ValueError as e:
            raise HTTPException(status_code=400, detail=f"Error de validación: {str(e)}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

@app.get("/download/{filename}")
async def download_file(filename: str):
    """
    Descarga un archivo AVRO generado
    """
    file_path = Path("output") / filename
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Archivo no encontrado")
    
    return FileResponse(
        path=str(file_path),
        filename=filename,
        media_type='application/octet-stream'
    )

@app.post("/convert-with-default-schema")
async def convert_with_default_schema(
    tipo_entidad: int = Form(...),
    codigo_entidad: str = Form(...),
    nombre_entidad: str = Form(...),
    fecha_corte: int = Form(...),
    csv_file: UploadFile = File(...)
):
    """
    Convierte un archivo CSV a formato AVRO usando el esquema por defecto del proyecto
    """
    
    if not csv_file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="El archivo debe ser un CSV")
    
    # Verificar que existe el esquema por defecto
    default_schema_path = Path("Esquema_AVRO.json")
    if not default_schema_path.exists():
        raise HTTPException(status_code=404, detail="Esquema por defecto no encontrado")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        try:
            csv_path = Path(temp_dir) / "input.csv"
            avro_path = Path(temp_dir) / "output.avro"
            log_path = Path(temp_dir) / "inconsistencias.log"
            
            # Escribir CSV temporal
            with open(csv_path, "wb") as f:
                shutil.copyfileobj(csv_file.file, f)
            
            # Crear instancia del generador con esquema por defecto
            generador = GeneradorCsvAvro(
                tipo_entidad=tipo_entidad,
                codigo_entidad=codigo_entidad,
                nombre_entidad=nombre_entidad,
                fecha_corte=fecha_corte,
                ruta_schema=str(default_schema_path),
                ruta_csv=str(csv_path)
            )
            
            # Ejecutar conversión
            generador.ejecutar(str(avro_path), str(log_path))
            
            # Leer inconsistencias
            inconsistencias = []
            if log_path.exists():
                with open(log_path, 'r', encoding='utf-8') as f:
                    inconsistencias = [line.strip() for line in f.readlines()]
            
            registros_validos = len(generador.garantias) if hasattr(generador, 'garantias') else 0
            registros_invalidos = len(inconsistencias)
            
            # Guardar archivo AVRO
            output_dir = Path("output")
            output_dir.mkdir(exist_ok=True)
            final_avro_path = output_dir / f"converted_default_{tipo_entidad}_{codigo_entidad}_{fecha_corte}.avro"
            
            if avro_path.exists():
                shutil.copy2(avro_path, final_avro_path)
                
                # Solo devolver el nombre del archivo, no la ruta completa
                filename_only = final_avro_path.name
                
                return ConversionResponse(
                    success=True,
                    message="Conversión completada con esquema por defecto",
                    registros_validos=registros_validos,
                    registros_invalidos=registros_invalidos,
                    inconsistencias=inconsistencias if inconsistencias else None,
                    avro_file_path=filename_only  # Solo el nombre del archivo
                )
            else:
                return ConversionResponse(
                    success=False,
                    message="Error: No se pudo generar el archivo AVRO",
                    registros_validos=0,
                    registros_invalidos=registros_invalidos,
                    inconsistencias=inconsistencias
                )
                
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
