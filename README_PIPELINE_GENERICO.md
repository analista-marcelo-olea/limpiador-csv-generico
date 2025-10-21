# Pipeline Genérico de Limpieza de Datasets

Un pipeline automático y genérico que funciona con **cualquier dataset CSV** sin necesidad de configuración manual.

## 🎯 Características

✅ **Detección automática** de:
- Delimitador (`;`, `,`, `\t`, `|`)
- Carácter de comilla (`"` o `'`)
- Encoding (UTF-8, Latin-1, ISO-8859-1, CP1252)
- Número de columnas y filas
- Problemas de calidad de datos

✅ **Análisis inteligente** que determina si la limpieza es necesaria

✅ **Limpieza automática** de:
- Caracteres Unicode problemáticos
- Entidades HTML
- Espacios en blanco
- Inconsistencias de separadores

✅ **Validación completa** del dataset limpio

✅ **Reportes detallados** en cada paso

## 📦 Archivos del Pipeline

- `config.py` - Detección automática de configuración
- `generic_analyzer.py` - Análisis de calidad
- `generic_cleaner.py` - Limpieza de datos
- `generic_validator.py` - Validación de resultados
- `generic_pipeline.py` - Orquestador principal

## 🚀 Uso

### Opción 1: Uso básico (recomendado)

```bash
python generic_pipeline.py Dataset.csv
```

El pipeline automáticamente:
1. Detecta la configuración del dataset
2. Analiza la calidad de datos
3. Limpia si es necesario
4. Valida los resultados
5. Genera reportes

### Opción 2: Especificar directorio de salida

```bash
python generic_pipeline.py Dataset.csv -o ./output
```

### Opción 3: Forzar limpieza

```bash
python generic_pipeline.py Dataset.csv -f
```

Limpia incluso si no detecta problemas.

## 📊 Salida del Pipeline

El pipeline genera los siguientes archivos:

```
Dataset_cleaned.csv                    # Dataset limpio
dataset_analysis_report.txt            # Reporte de análisis
dataset_cleaning_report.txt            # Reporte de limpieza
dataset_validation_report.txt          # Reporte de validación
dataset_cleaning.log                   # Log detallado
```

## 🔍 Ejemplo de Ejecución

```
$ python generic_pipeline.py Dataset.csv

======================================================================
🚀 PIPELINE GENÉRICO DE LIMPIEZA DE DATASETS
======================================================================
Archivo: Dataset.csv
Inicio: 2025-10-21 12:30:45

============================================================
DETECCIÓN AUTOMÁTICA DE CONFIGURACIÓN DEL DATASET
============================================================

✓ Delimitador detectado: ';'
✓ Carácter de comilla detectado: '"'
✓ Encoding detectado: utf-8
✓ Columnas detectadas: 35
✓ Filas detectadas: 1,784

📊 Análisis de Calidad:
   Problemas encontrados: 24476
   Necesita limpieza: Sí

✅ [12:30:46] Detección de Configuración: SUCCESS
   Configuración detectada:
   Delimitador: ';'
   Comilla: '"'
   Encoding: utf-8
   Columnas: 35
   Filas: 1,784

... (más pasos)

======================================================================
✅ PIPELINE COMPLETADO EXITOSAMENTE
======================================================================
```

## 🛠️ Personalización

### Modificar comportamiento de limpieza

Edita `generic_cleaner.py`:

```python
# Agregar más reemplazos de caracteres
self.char_replacements = {
    '"': '"',
    # ... agregar más aquí
}
```

### Agregar validaciones personalizadas

Edita `generic_validator.py` para agregar validaciones específicas de tu dominio.

## 📝 Notas Importantes

1. **Delimitadores soportados**: `;`, `,`, `\t`, `|`
2. **Encodings soportados**: UTF-8, Latin-1, ISO-8859-1, CP1252
3. **Preservación de datos**: El pipeline preserva la integridad de los datos
4. **Archivos temporales**: Se usan archivos `.tmp` para evitar corrupción

## ⚠️ Limitaciones

- No modifica la estructura del dataset (número de columnas)
- No elimina filas (solo omite si hay error de parsing)
- No realiza transformaciones de datos complejas

## 🐛 Troubleshooting

### Error: "Archivo no encontrado"
```bash
# Verifica que el archivo existe y la ruta es correcta
ls -la Dataset.csv
```

### Error: "Encoding no soportado"
El pipeline intentará detectar automáticamente. Si falla, especifica manualmente en `config.py`.

### Dataset no se limpia
Usa la opción `-f` para forzar limpieza:
```bash
python generic_pipeline.py Dataset.csv -f
```

## 📚 Estructura del Código

```
generic_pipeline.py (Orquestador)
├── config.py (Detección)
├── generic_analyzer.py (Análisis)
├── generic_cleaner.py (Limpieza)
└── generic_validator.py (Validación)
```

## 🎓 Ejemplo: Procesar múltiples datasets

```bash
#!/bin/bash

for file in *.csv; do
    echo "Procesando $file..."
    python generic_pipeline.py "$file" -o ./cleaned_data
done
```

## 📞 Soporte

Para problemas o sugerencias, revisa los logs en `dataset_cleaning.log`.

