# 🚀 INICIO RÁPIDO - Pruebas con Postman

## ✅ Estado Actual del Sistema

### Servidor API
- ✅ **Corriendo en**: http://localhost:8001
- ✅ **Documentación**: http://localhost:8001/docs
- ✅ **Health Check**: http://localhost:8001/health

### Archivos Creados para Postman
- ✅ `Postman_Collection.json` - Colección completa con 8 tests
- ✅ `Postman_Environment.json` - Variables de entorno
- ✅ `POSTMAN_TESTING_GUIDE.md` - Guía detallada de uso

## 🎯 PASOS PARA INICIAR PRUEBAS

### 1. **Abrir Postman**
- Desktop App o Web (https://web.postman.co/)

### 2. **Importar Colección**
- Clic en **"Import"**
- Seleccionar archivo: `Postman_Collection.json`
- Confirmar importación

### 3. **Importar Environment**
- Clic en icono ⚙️ (Manage Environments)
- Clic en **"Import"**
- Seleccionar archivo: `Postman_Environment.json`

### 4. **Activar Environment**
- En dropdown superior derecho
- Seleccionar: **"CSV to AVRO Converter Environment"**

### 5. **Configurar Rutas de Archivos**
En los requests que usan archivos, actualizar las rutas:

#### Request: "03 - Convert with Default Schema"
- Campo `csv_file` → Ruta: `D:\\Python\\convertcsvavro\\Data\\ArchivoCSV.csv`

#### Request: "04 - Convert with Custom Schema"  
- Campo `csv_file` → Ruta: `D:\\Python\\convertcsvavro\\Data\\ArchivoCSV.csv`
- Campo `schema_file` → Ruta: `D:\\Python\\convertcsvavro\\Esquema_AVRO.json`

## 🧪 TESTS INCLUIDOS

| # | Test | Descripción | Código Esperado |
|---|------|-------------|----------------|
| 1 | Health Check | Verificar servicio activo | 200 |
| 2 | Service Info | Información del API | 200 |
| 3 | Convert Default | Conversión con esquema por defecto | 200 |
| 4 | Convert Custom | Conversión con esquema personalizado | 200 |
| 5 | Download File | Descarga archivo AVRO | 200 |
| 6 | Error - Invalid CSV | Enviar archivo incorrecto | 400 |
| 7 | Error - Missing Params | Parámetros faltantes | 422 |
| 8 | Error - File Not Found | Archivo inexistente | 404 |

## ⚡ EJECUCIÓN RÁPIDA

### Opción A: Tests Individuales
1. Ejecutar cada request manualmente
2. Revisar respuestas y tests
3. Verificar códigos de estado

### Opción B: Collection Runner
1. Clic derecho en colección
2. **"Run collection"**
3. Configurar:
   - Environment: CSV to AVRO Converter Environment
   - Iterations: 1
   - Delay: 1000ms
4. **"Run"**

## 📊 RESULTADOS ESPERADOS

### ✅ Conversión Exitosa
```json
{
  "success": true,
  "message": "Conversión completada exitosamente",
  "registros_validos": 150,
  "registros_invalidos": 5,
  "avro_file_path": "output/converted_default_1_123456_2024.avro"
}
```

### ❌ Error Esperado
```json
{
  "detail": "El archivo debe ser un CSV"
}
```

## 🔧 TROUBLESHOOTING

### Problema: "Connection Error"
**Solución**: Verificar que el servidor esté corriendo en puerto 8001

### Problema: "File not found"  
**Solución**: Actualizar rutas absolutas en el body de los requests

### Problema: Tests fallan
**Solución**: Verificar que el environment esté activo

## 📁 ARCHIVOS NECESARIOS

```
D:\Python\convertcsvavro\
├── Data\ArchivoCSV.csv          ← Archivo CSV de prueba
├── Esquema_AVRO.json            ← Esquema AVRO
├── Postman_Collection.json      ← Colección de tests
├── Postman_Environment.json     ← Variables de entorno
└── output\                      ← Directorio de salida
```

## 🎉 ¡LISTO PARA PROBAR!

1. ✅ Servidor corriendo
2. ✅ Archivos de Postman creados
3. ✅ Datos de prueba disponibles
4. ✅ Documentación completa

**🚀 Importa los archivos a Postman y comienza las pruebas!**

---

*Si necesitas ayuda adicional, consulta `POSTMAN_TESTING_GUIDE.md` para instrucciones detalladas.*
