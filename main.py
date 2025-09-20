from generadorcsvavro import GeneradorCsvAvro

generador = GeneradorCsvAvro(
    tipo_entidad = 1,  # Debe ser int
    codigo_entidad = "123456",
    nombre_entidad = "CSISAS",
    fecha_corte=2070,
    ruta_schema="Esquema_AVRO.json",
    ruta_csv=r"Data\ArchivoCSV.csv"
)

generador.ejecutar("ArchivoGenerado.avro", "inconsistencias.log")
