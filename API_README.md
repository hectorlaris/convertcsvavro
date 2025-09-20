# Convertidor CSV a AVRO - Microservicio REST

Este proyecto convierte tu clase `GeneradorCsvAvro` en un microservicio REST usando FastAPI.

## Características

- 🚀 API REST con FastAPI
- 📁 Carga de archivos CSV y esquemas AVRO
- ✅ Validación de datos
- 📊 Reportes de inconsistencias
- 📥 Descarga de archivos AVRO generados
- 📖 Documentación automática con Swagger UI

## Instalación

1. Instala las dependencias:
```bash
pip install -r requirements.txt
```

## Uso

### Iniciar el servidor

```bash
python api.py
```

O usando uvicorn directamente:
```bash
uvicorn api:app --reload --host 0.0.0.0 --port 8000
```

El servidor estará disponible en: http://localhost:8000

### Documentación interactiva

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Endpoints

### 1. Información del servicio
- **GET** `/` - Información básica del servicio
- **GET** `/health` - Estado de salud del servicio

### 2. Conversión de archivos
- **POST** `/convert` - Convierte CSV a AVRO con esquema personalizado
- **POST** `/convert-with-default-schema` - Convierte CSV a AVRO con esquema por defecto

### 3. Descarga de archivos
- **GET** `/download/{filename}` - Descarga archivos AVRO generados

## Ejemplos de uso

### Convertir con esquema personalizado

```bash
curl -X POST "http://localhost:8000/convert" \
  -F "tipo_entidad=1" \
  -F "codigo_entidad=123456" \
  -F "nombre_entidad=CSISAS" \
  -F "fecha_corte=2070" \
  -F "csv_file=@Data/ArchivoCSV.csv" \
  -F "schema_file=@Esquema_AVRO.json"
```

### Convertir con esquema por defecto

```bash
curl -X POST "http://localhost:8000/convert-with-default-schema" \
  -F "tipo_entidad=1" \
  -F "codigo_entidad=123456" \
  -F "nombre_entidad=CSISAS" \
  -F "fecha_corte=2070" \
  -F "csv_file=@Data/ArchivoCSV.csv"
```

### Verificar estado del servicio

```bash
curl http://localhost:8000/health
```

## Estructura del proyecto

```
convertcsvavro/
├── api.py                    # Microservicio FastAPI
├── generadorcsvavro.py       # Clase original
├── main.py                   # Script original
├── requirements.txt          # Dependencias
├── Esquema_AVRO.json        # Esquema por defecto
├── Data/                    # Archivos de datos
└── output/                  # Archivos AVRO generados
```

## Respuesta de la API

La API devuelve un JSON con la siguiente estructura:

```json
{
  "success": true,
  "message": "Conversión completada exitosamente",
  "registros_validos": 150,
  "registros_invalidos": 5,
  "inconsistencias": [
    "Fila 3: Campo 'tipo_garantia' valor 'INVALID' no es válido para enum TipoGarantia"
  ],
  "avro_file_path": "output/converted_1_123456_2070.avro"
}
```

## Configuración adicional

### Variables de entorno (opcional)

Puedes configurar el servidor usando variables de entorno:

```bash
export HOST=0.0.0.0
export PORT=8000
export DEBUG=true
```

### Docker (próxima implementación)

Para facilitar el despliegue, se puede containerizar:

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Ventajas del microservicio

1. **Escalabilidad**: Puede manejar múltiples conversiones simultáneas
2. **Integración**: Fácil integración con otros sistemas via HTTP
3. **Documentación**: Swagger UI automático
4. **Validación**: Validación automática de parámetros
5. **Manejo de errores**: Respuestas HTTP estándar
6. **Flexibilidad**: Soporte para esquemas personalizados o por defecto
