# 🚀 PRUEBAS DE POSTMAN - INSTRUCCIONES PASO A PASO

## ✅ ESTADO ACTUAL
- 🟢 **Servidor ACTIVO**: http://localhost:8001
- 🟢 **Documentación**: http://localhost:8001/docs
- 🟢 **Archivos Postman**: Listos para importar

---

## 📥 PASO 1: IMPORTAR A POSTMAN

### A. Abrir Postman
- **Desktop**: Abrir aplicación Postman
- **Web**: Ir a https://web.postman.co/

### B. Importar Colección
1. **Clic en "Import"** (botón azul superior izquierda)
2. **Drag & Drop o Browse**
3. **Seleccionar**: `Postman_Collection.json`
4. **Clic "Import"**

### C. Importar Environment
1. **Clic en icono ⚙️** (Manage Environments)
2. **Clic "Import"**
3. **Seleccionar**: `Postman_Environment.json`
4. **Clic "Import"**

### D. Activar Environment
1. **Dropdown superior derecha**
2. **Seleccionar**: "CSV to AVRO Converter Environment"

---

## 🔧 PASO 2: CONFIGURAR RUTAS DE ARCHIVOS

### Requests que necesitan archivos:

#### **Request: "03 - Convert with Default Schema"**
- En **Body > form-data**
- Campo `csv_file` → **Browse** → Seleccionar:
  ```
  D:\Python\convertcsvavro\Data\ArchivoCSV.csv
  ```

#### **Request: "04 - Convert with Custom Schema"**
- En **Body > form-data**
- Campo `csv_file` → **Browse** → Seleccionar:
  ```
  D:\Python\convertcsvavro\Data\ArchivoCSV.csv
  ```
- Campo `schema_file` → **Browse** → Seleccionar:
  ```
  D:\Python\convertcsvavro\Esquema_AVRO.json
  ```

---

## 🧪 PASO 3: EJECUTAR PRUEBAS

### Opción A: Pruebas Individuales

**Orden recomendado:**

1. **01 - Health Check** ✅
   - **Clic "Send"**
   - **Resultado esperado**: Status 200, `{"status": "healthy"}`

2. **02 - Service Info** ✅
   - **Clic "Send"**
   - **Resultado esperado**: Información del servicio

3. **03 - Convert with Default Schema** ✅
   - **Verificar ruta CSV** en Body
   - **Clic "Send"**
   - **Resultado esperado**: Conversión exitosa

4. **04 - Convert with Custom Schema** ✅
   - **Verificar rutas CSV y Schema** en Body
   - **Clic "Send"**
   - **Resultado esperado**: Conversión exitosa

5. **05 - Download AVRO File** ✅
   - **Se ejecuta automáticamente** después del test #3
   - **Resultado esperado**: Descarga de archivo

6. **Tests de Error (06-08)** ✅
   - **Ejecutar uno por uno**
   - **Verificar códigos de error**

### Opción B: Collection Runner (Automático)

1. **Clic derecho** en la colección "CSV to AVRO Converter API"
2. **Seleccionar "Run collection"**
3. **Configurar**:
   - Environment: `CSV to AVRO Converter Environment`
   - Iterations: `1`
   - Delay: `1000ms`
4. **Clic "Run CSV to AVRO Converter API"**

---

## 📊 PASO 4: INTERPRETAR RESULTADOS

### ✅ **Respuesta Exitosa**
```json
{
  "success": true,
  "message": "Conversión completada exitosamente",
  "registros_validos": 150,
  "registros_invalidos": 5,
  "inconsistencias": ["..."],
  "avro_file_path": "output/converted_default_1_123456_2024.avro"
}
```

### ❌ **Respuesta de Error (Esperada)**
```json
{
  "detail": "El archivo debe ser un CSV"
}
```

### 📈 **Tests Automatizados**
- **Status Code**: Verifica códigos HTTP correctos
- **Response Structure**: Valida estructura JSON
- **Response Time**: Mide tiempo de respuesta
- **Business Logic**: Verifica lógica de negocio

---

## 🎯 VALIDACIONES ESPERADAS

| Test | Endpoint | Código | Validación |
|------|----------|--------|------------|
| Health Check | GET /health | 200 | Service healthy |
| Service Info | GET / | 200 | API information |
| Convert Default | POST /convert-with-default-schema | 200 | Successful conversion |
| Convert Custom | POST /convert | 200 | Successful conversion |
| Download | GET /download/{file} | 200 | File download |
| Error - Invalid CSV | POST /convert-with-default-schema | 400 | Error handling |
| Error - Missing Params | POST /convert-with-default-schema | 422 | Validation error |
| Error - File Not Found | GET /download/invalid | 404 | Not found error |

---

## 🔍 TROUBLESHOOTING

### ❌ **Error de Conexión**
```
Could not get any response
```
**Solución**: Verificar que el servidor esté corriendo en http://localhost:8001

### ❌ **404 Not Found**
```
{"detail":"Not Found"}
```
**Solución**: Verificar URL y método HTTP correcto

### ❌ **422 Validation Error**
```
{"detail":[{"type":"missing",...}]}
```
**Solución**: Verificar que todos los campos requeridos estén llenos

### ❌ **Archivos no encontrados**
```
{"detail":"El archivo debe ser un CSV"}
```
**Solución**: 
1. Verificar rutas de archivos en Body > form-data
2. Seleccionar archivos usando Browse en lugar de escribir rutas

---

## 📋 CHECKLIST FINAL

### Antes de ejecutar:
- [ ] ✅ Servidor corriendo en puerto 8001
- [ ] ✅ Colección importada en Postman
- [ ] ✅ Environment importado y activo
- [ ] ✅ Rutas de archivos configuradas

### Durante las pruebas:
- [ ] ✅ Health Check responde 200
- [ ] ✅ Conversión default exitosa  
- [ ] ✅ Conversión custom exitosa
- [ ] ✅ Descarga de archivos funciona
- [ ] ✅ Tests de error responden códigos correctos

### Después de las pruebas:
- [ ] ✅ Todos los tests pasaron (verde)
- [ ] ✅ Archivos AVRO generados en carpeta `output/`
- [ ] ✅ Reportes de Collection Runner revisados

---

## 🎉 ¡LISTO PARA EMPEZAR!

**Tu microservicio está completamente funcional y listo para pruebas profesionales con Postman.**

### Enlaces rápidos:
- 🌐 **API**: http://localhost:8001
- 📖 **Docs**: http://localhost:8001/docs
- 🧪 **Health**: http://localhost:8001/health

**¡Importa los archivos a Postman y comienza las pruebas!** 🚀
