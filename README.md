# Convertidor CSV a AVRO - Microservicio REST 🚀

![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-00a884)
![Python](https://img.shields.io/badge/Python-3.13-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)

Microservicio REST desarrollado con FastAPI para convertir archivos CSV a formato AVRO con validación de esquemas.

## 🌟 Características Principales

- ✅ **API REST** completa con FastAPI
- 📁 **Carga de archivos** CSV y esquemas AVRO
- 🔍 **Validación automática** de datos
- 📊 **Reportes detallados** de inconsistencias
- 📥 **Descarga de archivos** AVRO generados
- 📖 **Documentación interactiva** con Swagger UI
- 🧪 **Scripts de testing** automatizados

## 🚀 Inicio Rápido

### 1. Instalación
```bash
git clone https://github.com/hectorlaris/convertcsvavro.git
cd convertcsvavro
pip install -r requirements.txt
```

### 2. Iniciar Servidor
```bash
python api.py
```

### 3. Acceder a la Documentación
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📚 Documentación

| Documento | Descripción |
|-----------|-------------|
| [📋 PROYECTO_RESUMEN.md](PROYECTO_RESUMEN.md) | Resumen ejecutivo del proyecto |
| [🛠️ DOCUMENTACION_TECNICA.md](DOCUMENTACION_TECNICA.md) | Arquitectura y detalles técnicos |
| [🚀 API_README.md](API_README.md) | Guía de uso del API |

## 🎯 Uso del API

### Conversión Básica
```bash
curl -X POST "http://localhost:8000/convert-with-default-schema" \
  -F "tipo_entidad=1" \
  -F "codigo_entidad=123456" \
  -F "nombre_entidad=EMPRESA" \
  -F "fecha_corte=2024" \
  -F "csv_file=@archivo.csv"
```

### Conversión con Esquema Personalizado
```bash
curl -X POST "http://localhost:8000/convert" \
  -F "tipo_entidad=1" \
  -F "codigo_entidad=123456" \
  -F "nombre_entidad=EMPRESA" \
  -F "fecha_corte=2024" \
  -F "csv_file=@archivo.csv" \
  -F "schema_file=@esquema.json"
```

## 📊 Respuesta del API

```json
{
  "success": true,
  "message": "Conversión completada exitosamente",
  "registros_validos": 150,
  "registros_invalidos": 5,
  "inconsistencias": ["..."],
  "avro_file_path": "output/converted_1_123456_2024.avro"
}
```

## 🔧 Estructura del Proyecto

```
convertcsvavro/
├── api.py                    # 🌟 Microservicio FastAPI
├── generadorcsvavro.py       # 🔄 Clase de conversión
├── start_server.py           # 🚀 Script de inicio
├── test_api.py              # 🧪 Tests automatizados
├── requirements.txt         # 📦 Dependencias
├── Esquema_AVRO.json       # 📋 Esquema por defecto
├── Data/                   # 📂 Archivos de entrada
└── output/                 # 📁 Archivos generados
```

## 🧪 Testing

```bash
# Ejecutar tests automatizados
python test_api.py

# Verificar estado del servicio
curl http://localhost:8000/health
```

## 🐳 Docker (Próximamente)

```bash
# Build
docker build -t csv-avro-api .

# Run
docker run -p 8000:8000 csv-avro-api
```

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Agrega nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## 👨‍💻 Autor

**Héctor Laris**
- GitHub: [@hectorlaris](https://github.com/hectorlaris)
- Proyecto: [convertcsvavro](https://github.com/hectorlaris/convertcsvavro)

---

⭐ ¡No olvides dar una estrella al repo si te fue útil!

## Descripción

`GeneradorCsvAvro` es una clase en Python que facilita la conversión de archivos CSV a formato Avro. Esta clase fue diseñada para simplificar el proceso de transformación de datos y asegurar la compatibilidad con sistemas que utilizan Avro para el almacenamiento y transporte de datos.

## Características

- Convierte archivos CSV a formato Avro.
- Soporta esquemas personalizables para la generación de archivos Avro.
- Maneja grandes conjuntos de datos de manera eficiente.

## Requisitos

Este proyecto requiere Python 3.6 o superior y las siguientes bibliotecas de Python:

- `pandas`
- `fastavro`

Puedes instalar los requisitos con:
pip install pandas fastavro
## Uso

A continuación se presenta un ejemplo de cómo usar la clase `GenerarCsvAvro`: