import pandas as pd
import json
from fastavro import writer, parse_schema
from pathlib import Path
from io import BytesIO

class GeneradorCsvAvro:
    def __init__(self, tipo_entidad, codigo_entidad, nombre_entidad, fecha_corte, ruta_schema, ruta_csv):
        self.tipo_entidad = tipo_entidad
        self.codigo_entidad = codigo_entidad
        self.nombre_entidad = nombre_entidad
        self.fecha_corte = fecha_corte
        self.ruta_schema = Path(ruta_schema)
        self.ruta_csv = Path(ruta_csv)
        self.schema = self._cargar_schema()
        self.garantias = []
        self.inconsistencias = []

    def _cargar_schema(self):
        with open(self.ruta_schema, 'r', encoding='utf-8') as f:
            return parse_schema(json.load(f))

    def validar_campos_principales(self):
        errores = []
        if not isinstance(self.tipo_entidad, int):
            errores.append("tipo_entidad debe ser int")
        if not isinstance(self.codigo_entidad, str):
            errores.append("codigo_entidad debe ser str")
        if not isinstance(self.nombre_entidad, str):
            errores.append("nombre_entidad debe ser str")
        if not isinstance(self.fecha_corte, int):
            errores.append("fecha_corte debe ser int")
        return errores

    def cargar_garantias(self):
        df = pd.read_csv(self.ruta_csv, sep=';', dtype=str).fillna('')
        df['FECHA_CORTE'] = self.fecha_corte
        self.garantias = df.to_dict(orient='records')

    def ajustar_garantias_a_schema(self):
        campos_schema = {field['name'] for field in self.schema['fields']}
        # Obtener el sub-esquema de Detalle_Garantias
        detalle_schema = None
        for field in self.schema['fields']:
            if field['name'] == 'Detalle_Garantias':
                detalle_type = field['type']
                if isinstance(detalle_type, list):
                    detalle_type = next((t for t in detalle_type if isinstance(t, dict) and t.get('type') == 'array'), None)
                if detalle_type and isinstance(detalle_type, dict) and detalle_type.get('type') == 'array':
                    detalle_schema = detalle_type['items']
        # Mapeo explícito de campos del CSV a los del esquema Avro
        mapeo = {f['name']: f['name'] for f in detalle_schema['fields']}
        tipo_entidad_valor = self.tipo_entidad
        codigo_entidad_valor = self.codigo_entidad
        nombre_entidad_valor = self.nombre_entidad
        fecha_corte_valor = self.fecha_corte
        nuevas_garantias = []
        for garantia in self.garantias:
            registro = {}
            registro['tipo_entidad'] = int(tipo_entidad_valor)
            registro['codigo_entidad'] = int(codigo_entidad_valor)
            registro['nombre_entidad'] = str(nombre_entidad_valor)
            registro['fecha_corte'] = int(fecha_corte_valor)
            detalle = {}
            for csv_key, avro_key in mapeo.items():
                # Buscar el tipo esperado en el sub-esquema
                tipo_campo = next((f['type'] for f in detalle_schema['fields'] if f['name'] == avro_key), None)
                detalle[avro_key] = self._convertir_tipo_tipo(tipo_campo, garantia.get(csv_key))
            registro['Detalle_Garantias'] = [self._limpiar_garantia(detalle)]
            for campo in campos_schema:
                registro.setdefault(campo, None)
            nuevas_garantias.append(registro)
        self.garantias = nuevas_garantias

    def _convertir_tipo_tipo(self, tipo, valor):
        # Si es union, tomar el tipo principal (no null)
        if isinstance(tipo, list):
            tipo = next((t for t in tipo if t != 'null'), None)
        # Si es enum, dejar como string
        if isinstance(tipo, dict) and tipo.get('type') == 'enum':
            return valor if valor != '' else None
        # Si es int
        if tipo == 'int' or (isinstance(tipo, dict) and tipo.get('type') == 'int'):
            try:
                return int(valor) if valor not in (None, '') else None
            except:
                return None
        # Si es float
        if tipo == 'float' or (isinstance(tipo, dict) and tipo.get('type') == 'float'):
            try:
                return float(valor) if valor not in (None, '') else None
            except:
                return None
        # Si es string
        if tipo == 'string' or (isinstance(tipo, dict) and tipo.get('type') == 'string'):
            return str(valor) if valor not in (None, '') else None
        # Otros casos
        return valor if valor != '' else None

    def _convertir_tipo(self, campo, valor):
        # Buscar el tipo esperado en el esquema Avro para el campo
        def buscar_tipo(schema, campo):
            if 'fields' in schema:
                for f in schema['fields']:
                    if f['name'] == campo:
                        return f['type']
            if isinstance(schema, dict) and schema.get('type') == 'record':
                for f in schema.get('fields', []):
                    if f['name'] == campo:
                        return f['type']
            return None
        tipo = buscar_tipo(self.schema, campo)
        # Si es union, tomar el tipo principal (no null)
        if isinstance(tipo, list):
            tipo = next((t for t in tipo if t != 'null'), None)
        # Si es enum, dejar como string
        if isinstance(tipo, dict) and tipo.get('type') == 'enum':
            return valor if valor != '' else None
        # Si es int
        if tipo == 'int' or (isinstance(tipo, dict) and tipo.get('type') == 'int'):
            try:
                return int(valor) if valor not in (None, '') else None
            except:
                return None
        # Si es float
        if tipo == 'float' or (isinstance(tipo, dict) and tipo.get('type') == 'float'):
            try:
                return float(valor) if valor not in (None, '') else None
            except:
                return None
        # Si es string
        if tipo == 'string' or (isinstance(tipo, dict) and tipo.get('type') == 'string'):
            return str(valor) if valor not in (None, '') else None
        # Otros casos
        return valor if valor != '' else None

    def _limpiar_garantia(self, garantia):
        return {k: (None if pd.isna(v) else v) for k, v in garantia.items()}

    def validar_garantias_contra_schema(self):
        def validar_campo(valor, tipo, nombre, fila, path):
            # Validación especial para enums
            if isinstance(tipo, list):
                tipos_enum = [t for t in tipo if isinstance(t, dict) and t.get('type') == 'enum']
                for t_enum in tipos_enum:
                    if valor is not None and valor != '' and valor not in t_enum.get('symbols', []):
                        self.inconsistencias.append(f"Fila {fila}: Campo '{path}{nombre}' valor '{valor}' no es válido para enum {t_enum.get('name')}")
            elif isinstance(tipo, dict) and tipo.get('type') == 'enum':
                if valor is not None and valor != '' and valor not in tipo.get('symbols', []):
                    self.inconsistencias.append(f"Fila {fila}: Campo '{path}{nombre}' valor '{valor}' no es válido para enum {tipo.get('name')}")
            # Validación estándar
            if not self._validar_tipo(valor, tipo):
                self.inconsistencias.append(f"Fila {fila}: Campo '{path}{nombre}' con valor inválido '{valor}'")
            # Validación recursiva para records y arrays
            if isinstance(tipo, dict):
                if tipo.get('type') == 'record' and isinstance(valor, dict):
                    for subfield in tipo.get('fields', []):
                        subnombre = subfield['name']
                        subtipo = subfield['type']
                        validar_campo(valor.get(subnombre), subtipo, subnombre, fila, f"{path}{nombre}.")
                elif tipo.get('type') == 'array' and isinstance(valor, list):
                    items_type = tipo.get('items')
                    for i, item in enumerate(valor):
                        if isinstance(items_type, dict) and items_type.get('type') == 'record':
                            for subfield in items_type.get('fields', []):
                                subnombre = subfield['name']
                                subtipo = subfield['type']
                                validar_campo(item.get(subnombre), subtipo, subnombre, fila, f"{path}{nombre}[{i}].")
                        else:
                            validar_campo(item, items_type, nombre, fila, f"{path}{nombre}[{i}].")
        for idx, garantia in enumerate(self.garantias):
            for field in self.schema['fields']:
                nombre = field['name']
                tipo = field['type']
                valor = garantia.get(nombre)
                validar_campo(valor, tipo, nombre, idx+1, "")
    
    def _validar_tipo(self, valor, tipo):
        if isinstance(tipo, list):  # union
            return any(self._validar_tipo(valor, t) for t in tipo if t != 'null')
        if tipo == 'string':
            return isinstance(valor, str) or valor is None
        if tipo == 'int':
            return isinstance(valor, int) or valor is None
        return True  # otros tipos pueden extenderse

    def generar_avro(self, ruta_salida):
        with open(ruta_salida, 'wb') as out:
            writer(out, self.schema, self.garantias)

    def guardar_inconsistencias(self, ruta_log):
        if self.inconsistencias:
            with open(ruta_log, 'w', encoding='utf-8') as f:
                for error in self.inconsistencias:
                    f.write(error + '\n')

    def ejecutar(self, ruta_salida_avro, ruta_log):
        errores = self.validar_campos_principales()
        if errores:
            raise ValueError(f"Errores en campos principales: {errores}")
        self.cargar_garantias()
        self.ajustar_garantias_a_schema()
        # Validar y filtrar registros válidos
        registros_validos = []
        registros_invalidos = []
        for idx, garantia in enumerate(self.garantias):
            self.inconsistencias = []
            # Validar campos principales
            for field in self.schema['fields']:
                nombre = field['name']
                tipo = field['type']
                valor = garantia.get(nombre)
                # Validar Detalle_Garantias como array de record
                if nombre == 'Detalle_Garantias' and isinstance(valor, list):
                    # Obtener el sub-esquema
                    detalle_schema = None
                    if isinstance(tipo, list):
                        tipo = next((t for t in tipo if isinstance(t, dict) and t.get('type') == 'array'), None)
                    if tipo and isinstance(tipo, dict) and tipo.get('type') == 'array':
                        detalle_schema = tipo['items']
                    for i, item in enumerate(valor):
                        for subfield in detalle_schema['fields']:
                            subnombre = subfield['name']
                            subtipo = subfield['type']
                            subvalor = item.get(subnombre)
                            # Validación especial para enums
                            if isinstance(subtipo, list):
                                tipos_enum = [t for t in subtipo if isinstance(t, dict) and t.get('type') == 'enum']
                                for t_enum in tipos_enum:
                                    if subvalor is not None and subvalor != '' and subvalor not in t_enum.get('symbols', []):
                                        self.inconsistencias.append(f"Fila {idx+1}: Campo 'Detalle_Garantias[{i}].{subnombre}' valor '{subvalor}' no es válido para enum {t_enum.get('name')}")
                            elif isinstance(subtipo, dict) and subtipo.get('type') == 'enum':
                                if subvalor is not None and subvalor != '' and subvalor not in subtipo.get('symbols', []):
                                    self.inconsistencias.append(f"Fila {idx+1}: Campo 'Detalle_Garantias[{i}].{subnombre}' valor '{subvalor}' no es válido para enum {subtipo.get('name')}")
                            # Validación estándar
                            if not self._validar_tipo(subvalor, subtipo):
                                self.inconsistencias.append(f"Fila {idx+1}: Campo 'Detalle_Garantias[{i}].{subnombre}' con valor inválido '{subvalor}'")
                else:
                    # Validación especial para enums
                    if isinstance(tipo, list):
                        tipos_enum = [t for t in tipo if isinstance(t, dict) and t.get('type') == 'enum']
                        for t_enum in tipos_enum:
                            if valor is not None and valor != '' and valor not in t_enum.get('symbols', []):
                                self.inconsistencias.append(f"Fila {idx+1}: Campo '{nombre}' valor '{valor}' no es válido para enum {t_enum.get('name')}")
                    elif isinstance(tipo, dict) and tipo.get('type') == 'enum':
                        if valor is not None and valor != '' and valor not in tipo.get('symbols', []):
                            self.inconsistencias.append(f"Fila {idx+1}: Campo '{nombre}' valor '{valor}' no es válido para enum {tipo.get('name')}")
                    # Validación estándar
                    if not self._validar_tipo(valor, tipo):
                        self.inconsistencias.append(f"Fila {idx+1}: Campo '{nombre}' con valor inválido '{valor}'")
            if self.inconsistencias:
                registros_invalidos.append((garantia, list(self.inconsistencias)))
            else:
                registros_validos.append(garantia)
        print(f"Registros válidos: {len(registros_validos)}")
        print(f"Registros inválidos: {len(registros_invalidos)}")
        for reg, incs in registros_invalidos:
            for inc in incs:
                print(inc)
        # Guardar inconsistencias en el log
        if registros_invalidos:
            with open(ruta_log, 'w', encoding='utf-8') as f:
                for reg, incs in registros_invalidos:
                    for inc in incs:
                        f.write(inc + '\n')
        # Solo escribir los registros válidos en el Avro
        if registros_validos:
            self.garantias = registros_validos
            self.generar_avro(ruta_salida_avro)
