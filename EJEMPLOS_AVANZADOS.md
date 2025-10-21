# Ejemplos Avanzados - Pipeline Genérico

## 1. Procesar Múltiples Datasets en Paralelo

### Script: `process_all.sh`

```bash
#!/bin/bash

# Procesar todos los CSV en la carpeta actual
for file in *.csv; do
    echo "Procesando $file..."
    python generic_pipeline.py "$file" -o ./cleaned &
done

# Esperar a que terminen todos
wait
echo "¡Todos los datasets han sido procesados!"
```

Uso:
```bash
chmod +x process_all.sh
./process_all.sh
```

## 2. Procesar Datasets de Múltiples Carpetas

### Script: `process_recursive.py`

```python
import os
from pathlib import Path
from generic_pipeline import GenericDataPipeline

# Procesar todos los CSV en subcarpetas
for csv_file in Path('.').rglob('*.csv'):
    print(f"Procesando {csv_file}...")
    pipeline = GenericDataPipeline(str(csv_file))
    pipeline.execute()
```

Uso:
```bash
python process_recursive.py
```

## 3. Procesar con Filtros Personalizados

### Script: `process_filtered.py`

```python
import os
from pathlib import Path
from generic_pipeline import GenericDataPipeline

# Procesar solo archivos mayores a 1MB
min_size = 1024 * 1024  # 1MB

for csv_file in Path('.').glob('*.csv'):
    if csv_file.stat().st_size > min_size:
        print(f"Procesando {csv_file} ({csv_file.stat().st_size / 1024 / 1024:.2f}MB)...")
        pipeline = GenericDataPipeline(str(csv_file))
        pipeline.execute()
```

## 4. Procesar y Generar Reporte Consolidado

### Script: `process_with_report.py`

```python
import os
from datetime import datetime
from generic_pipeline import GenericDataPipeline
from pathlib import Path

# Procesar todos los CSV y generar reporte consolidado
results = []
start_time = datetime.now()

for csv_file in Path('.').glob('*.csv'):
    print(f"Procesando {csv_file}...")
    pipeline = GenericDataPipeline(str(csv_file))
    success = pipeline.execute()
    
    results.append({
        'file': str(csv_file),
        'status': 'SUCCESS' if success else 'FAILED',
        'time': datetime.now()
    })

# Generar reporte consolidado
report = []
report.append("=" * 70)
report.append("REPORTE CONSOLIDADO DE PROCESAMIENTO")
report.append("=" * 70)
report.append(f"Fecha: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
report.append(f"Total de archivos: {len(results)}")
report.append(f"Exitosos: {sum(1 for r in results if r['status'] == 'SUCCESS')}")
report.append(f"Fallidos: {sum(1 for r in results if r['status'] == 'FAILED')}")
report.append("")

for result in results:
    status_icon = "✓" if result['status'] == 'SUCCESS' else "✗"
    report.append(f"{status_icon} {result['file']}: {result['status']}")

# Guardar reporte
with open('reporte_consolidado.txt', 'w') as f:
    f.write('\n'.join(report))

print('\n'.join(report))
```

## 5. Procesar con Validación Personalizada

### Script: `process_with_validation.py`

```python
from generic_pipeline import GenericDataPipeline
from generic_validator import GenericDatasetValidator
import csv

class CustomValidator(GenericDatasetValidator):
    """Validador personalizado con reglas adicionales"""
    
    def validate_custom_rules(self):
        """Valida reglas específicas del dominio"""
        print("\n=== VALIDACIÓN PERSONALIZADA ===")
        
        with open(self.cleaned_file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter=self.config['delimiter'])
            header = next(reader)
            
            # Ejemplo: Validar que cantidad_toneladas sea numérico
            if 'cantidad_toneladas' in header:
                idx = header.index('cantidad_toneladas')
                
                for row_num, row in enumerate(reader, 2):
                    try:
                        value = row[idx].replace(',', '.')
                        float(value)
                    except ValueError:
                        print(f"⚠ Fila {row_num}: cantidad_toneladas no es numérico: {row[idx]}")

# Usar validador personalizado
pipeline = GenericDataPipeline('Dataset.csv')
pipeline.execute()

# Validación personalizada
validator = CustomValidator('Dataset.csv', 'Dataset_cleaned.csv', pipeline.config)
validator.validate_custom_rules()
```

## 6. Procesar con Transformaciones Adicionales

### Script: `process_with_transform.py`

```python
from generic_pipeline import GenericDataPipeline
from generic_cleaner import GenericDatasetCleaner
import csv

class EnhancedCleaner(GenericDatasetCleaner):
    """Limpiador mejorado con transformaciones adicionales"""
    
    def clean_row(self, row_data):
        """Limpia y transforma una fila"""
        fields, success = super().clean_row(row_data)
        
        if success:
            # Agregar transformaciones personalizadas
            transformed_fields = []
            for field in fields:
                # Ejemplo: Convertir a mayúsculas
                if field:
                    field = field.upper()
                transformed_fields.append(field)
            
            return transformed_fields, True
        
        return fields, success

# Usar limpiador mejorado
pipeline = GenericDataPipeline('Dataset.csv')
pipeline.detect_configuration()
pipeline.analyze_dataset()

# Usar limpiador personalizado
cleaner = EnhancedCleaner('Dataset.csv', 'Dataset_cleaned.csv', pipeline.config)
cleaner.process_file()
```

## 7. Monitoreo en Tiempo Real

### Script: `monitor_processing.py`

```python
import time
import os
from pathlib import Path
from generic_pipeline import GenericDataPipeline

# Monitorear carpeta y procesar nuevos archivos
watched_dir = './data'
processed = set()

print(f"Monitoreando {watched_dir}...")

while True:
    # Buscar nuevos archivos
    for csv_file in Path(watched_dir).glob('*.csv'):
        if str(csv_file) not in processed:
            print(f"\n🆕 Nuevo archivo detectado: {csv_file}")
            
            try:
                pipeline = GenericDataPipeline(str(csv_file))
                pipeline.execute()
                processed.add(str(csv_file))
                print(f"✓ {csv_file} procesado exitosamente")
            except Exception as e:
                print(f"✗ Error procesando {csv_file}: {e}")
    
    # Esperar antes de verificar nuevamente
    time.sleep(10)
```

## 8. Integración con Base de Datos

### Script: `process_and_load.py`

```python
import sqlite3
import csv
from generic_pipeline import GenericDataPipeline

# Procesar dataset
pipeline = GenericDataPipeline('Dataset.csv')
pipeline.execute()

# Cargar en base de datos
conn = sqlite3.connect('datos.db')
cursor = conn.cursor()

with open('Dataset_cleaned.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f, delimiter=';')
    header = next(reader)
    
    # Crear tabla
    columns = ', '.join([f'"{col}" TEXT' for col in header])
    cursor.execute(f'CREATE TABLE IF NOT EXISTS datos ({columns})')
    
    # Insertar datos
    placeholders = ', '.join(['?' for _ in header])
    for row in reader:
        cursor.execute(f'INSERT INTO datos VALUES ({placeholders})', row)

conn.commit()
conn.close()

print("✓ Datos cargados en base de datos")
```

## 9. Generar Estadísticas Comparativas

### Script: `compare_datasets.py`

```python
import csv
from generic_pipeline import GenericDataPipeline

def get_stats(filepath, delimiter):
    """Obtiene estadísticas de un archivo"""
    stats = {
        'rows': 0,
        'columns': 0,
        'empty_fields': 0,
        'total_chars': 0
    }
    
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=delimiter)
        header = next(reader)
        stats['columns'] = len(header)
        
        for row in reader:
            stats['rows'] += 1
            stats['empty_fields'] += sum(1 for field in row if not field.strip())
            stats['total_chars'] += sum(len(field) for field in row)
    
    return stats

# Procesar
pipeline = GenericDataPipeline('Dataset.csv')
pipeline.execute()

# Comparar
original_stats = get_stats('Dataset.csv', ';')
cleaned_stats = get_stats('Dataset_cleaned.csv', ';')

print("COMPARACIÓN ORIGINAL vs LIMPIO:")
print(f"Filas: {original_stats['rows']} → {cleaned_stats['rows']}")
print(f"Campos vacíos: {original_stats['empty_fields']} → {cleaned_stats['empty_fields']}")
print(f"Caracteres totales: {original_stats['total_chars']} → {cleaned_stats['total_chars']}")
```

## 10. Automatización con Cron (Linux/Mac)

### Archivo: `crontab_setup.sh`

```bash
#!/bin/bash

# Agregar tarea cron para procesar datasets diariamente a las 2 AM
(crontab -l 2>/dev/null; echo "0 2 * * * cd /path/to/project && python batch_process.py '*.csv' -o ./cleaned") | crontab -

echo "✓ Tarea cron configurada"
```

Uso:
```bash
chmod +x crontab_setup.sh
./crontab_setup.sh
```

## 11. Automatización con Task Scheduler (Windows)

### Script: `setup_scheduler.ps1`

```powershell
# Crear tarea programada en Windows
$action = New-ScheduledTaskAction -Execute "python" -Argument "batch_process.py '*.csv' -o ./cleaned" -WorkingDirectory "C:\path\to\project"
$trigger = New-ScheduledTaskTrigger -Daily -At 2am
Register-ScheduledTask -Action $action -Trigger $trigger -TaskName "ProcessDatasets" -Description "Procesar datasets diariamente"

Write-Host "✓ Tarea programada configurada"
```

Uso:
```powershell
.\setup_scheduler.ps1
```

---

Estos ejemplos muestran cómo extender y personalizar el pipeline para casos de uso más complejos. ¡Adapta según tus necesidades!

