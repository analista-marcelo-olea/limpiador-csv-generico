# Índice de Archivos - Pipeline Genérico

## 📋 Estructura del Proyecto

```
dataset1/
├── MÓDULOS PRINCIPALES
│   ├── config.py                    ← Detección automática de configuración
│   ├── generic_analyzer.py          ← Análisis genérico de calidad
│   ├── generic_cleaner.py           ← Limpieza genérica de datos
│   ├── generic_validator.py         ← Validación genérica de resultados
│   ├── generic_pipeline.py          ← Orquestador principal
│   └── batch_process.py             ← Procesamiento en lote
│
├── DOCUMENTACIÓN
│   ├── GUIA_RAPIDA.md               ← Inicio rápido (LEER PRIMERO)
│   ├── README_PIPELINE_GENERICO.md  ← Documentación completa
│   ├── RESUMEN_PIPELINE_GENERICO.md ← Resumen técnico
│   ├── EJEMPLOS_AVANZADOS.md        ← Casos de uso avanzados
│   ├── IMPLEMENTACION_COMPLETADA.txt ← Detalles de implementación
│   ├── RESUMEN_FINAL.txt            ← Resumen visual
│   └── INDICE_ARCHIVOS.md           ← Este archivo
│
├── DATOS
│   ├── Dataset.csv                  ← Dataset original
│   └── Dataset_cleaned.csv          ← Dataset limpio (generado)
│
├── REPORTES (generados automáticamente)
│   ├── dataset_analysis_report.txt
│   ├── dataset_cleaning_report.txt
│   ├── dataset_validation_report.txt
│   └── dataset_cleaning.log
│
└── ARCHIVOS ANTIGUOS (para referencia)
    ├── cleaner_dataset.py           ← Pipeline anterior (específico)
    ├── pipeline_dataset.py          ← Pipeline anterior (específico)
    ├── analisis_dataset.py          ← Análisis anterior (específico)
    ├── validator_dataset.py         ← Validador anterior (específico)
    └── SOLUCION_PROBLEMA.md         ← Documentación anterior
```

## 🎯 Dónde Empezar

### 1️⃣ PRIMERO: Lee la Guía Rápida
**Archivo:** `GUIA_RAPIDA.md`
- Inicio rápido en 5 minutos
- Ejemplos simples
- Comandos básicos

### 2️⃣ SEGUNDO: Ejecuta el Pipeline
```bash
python generic_pipeline.py Dataset.csv
```

### 3️⃣ TERCERO: Revisa los Reportes
- `dataset_analysis_report.txt` - Análisis inicial
- `dataset_cleaning_report.txt` - Detalles de limpieza
- `dataset_validation_report.txt` - Validación final

### 4️⃣ CUARTO: Personaliza si es Necesario
Consulta `EJEMPLOS_AVANZADOS.md` para casos complejos.

## 📚 Descripción de Archivos

### Módulos Principales

#### `config.py` (150 líneas)
**Propósito:** Detección automática de configuración
**Funciones principales:**
- `detect_delimiter()` - Detecta delimitador
- `detect_quotechar()` - Detecta carácter de comilla
- `detect_encoding()` - Detecta encoding
- `detect_column_count()` - Detecta número de columnas
- `analyze_data_quality()` - Analiza calidad de datos

**Uso:**
```python
from config import DatasetConfig
config = DatasetConfig('Dataset.csv')
config_dict = config.get_config()
```

#### `generic_analyzer.py` (150 líneas)
**Propósito:** Análisis genérico de calidad
**Funciones principales:**
- `analyze_file_structure()` - Analiza estructura
- `analyze_separators()` - Verifica separadores
- `analyze_character_encoding()` - Analiza codificación
- `analyze_data_quality()` - Analiza calidad

**Uso:**
```python
from generic_analyzer import GenericDatasetAnalyzer
analyzer = GenericDatasetAnalyzer('Dataset.csv', config)
analyzer.analyze_file_structure()
```

#### `generic_cleaner.py` (200 líneas)
**Propósito:** Limpieza genérica de datos
**Funciones principales:**
- `normalize_unicode()` - Normaliza Unicode
- `clean_html_entities()` - Limpia HTML
- `normalize_whitespace()` - Normaliza espacios
- `process_file()` - Procesa archivo completo

**Uso:**
```python
from generic_cleaner import GenericDatasetCleaner
cleaner = GenericDatasetCleaner('Dataset.csv', 'Dataset_cleaned.csv', config)
cleaner.process_file()
```

#### `generic_validator.py` (150 líneas)
**Propósito:** Validación genérica de resultados
**Funciones principales:**
- `validate_csv_structure()` - Valida estructura
- `validate_character_encoding()` - Valida codificación
- `validate_data_integrity()` - Valida integridad

**Uso:**
```python
from generic_validator import GenericDatasetValidator
validator = GenericDatasetValidator('Dataset.csv', 'Dataset_cleaned.csv', config)
validator.validate_csv_structure()
```

#### `generic_pipeline.py` (250 líneas)
**Propósito:** Orquestador principal
**Funciones principales:**
- `detect_configuration()` - Detecta configuración
- `analyze_dataset()` - Analiza dataset
- `clean_dataset()` - Limpia dataset
- `validate_dataset()` - Valida dataset
- `execute()` - Ejecuta pipeline completo

**Uso:**
```bash
python generic_pipeline.py Dataset.csv
python generic_pipeline.py Dataset.csv -o ./output
python generic_pipeline.py Dataset.csv -f
```

#### `batch_process.py` (100 líneas)
**Propósito:** Procesamiento en lote
**Funciones principales:**
- `find_files()` - Encuentra archivos
- `process_all()` - Procesa todos
- `print_summary()` - Imprime resumen

**Uso:**
```bash
python batch_process.py "*.csv"
python batch_process.py "data/*.csv" -o ./cleaned
```

### Documentación

#### `GUIA_RAPIDA.md`
- Inicio rápido
- Casos de uso comunes
- Ejemplos prácticos
- **LEER PRIMERO**

#### `README_PIPELINE_GENERICO.md`
- Documentación completa
- Características detalladas
- Troubleshooting
- Personalización

#### `RESUMEN_PIPELINE_GENERICO.md`
- Resumen técnico
- Flujo del pipeline
- Mejoras respecto al anterior
- Próximos pasos

#### `EJEMPLOS_AVANZADOS.md`
- Casos de uso avanzados
- Scripts personalizados
- Integración con otras herramientas
- Automatización

#### `IMPLEMENTACION_COMPLETADA.txt`
- Detalles de implementación
- Checklist de implementación
- Conclusión

#### `RESUMEN_FINAL.txt`
- Resumen visual
- Características principales
- Cómo usar
- Próximos pasos

## 🔄 Flujo de Uso

```
1. Leer GUIA_RAPIDA.md
   ↓
2. Ejecutar: python generic_pipeline.py Dataset.csv
   ↓
3. Revisar reportes generados
   ↓
4. Usar Dataset_cleaned.csv
   ↓
5. (Opcional) Personalizar según necesidades
   ↓
6. (Opcional) Procesar múltiples datasets con batch_process.py
```

## 📊 Archivos Generados por el Pipeline

Después de ejecutar `python generic_pipeline.py Dataset.csv`:

| Archivo | Descripción |
|---------|-------------|
| `Dataset_cleaned.csv` | Dataset limpio |
| `dataset_analysis_report.txt` | Análisis inicial |
| `dataset_cleaning_report.txt` | Detalles de limpieza |
| `dataset_validation_report.txt` | Validación final |
| `dataset_cleaning.log` | Log detallado |

## 🎯 Casos de Uso

### Caso 1: Procesar un dataset
```bash
python generic_pipeline.py ventas.csv
```

### Caso 2: Procesar múltiples datasets
```bash
python batch_process.py "*.csv"
```

### Caso 3: Procesar con directorio de salida
```bash
python generic_pipeline.py Dataset.csv -o ./output
```

### Caso 4: Forzar limpieza
```bash
python generic_pipeline.py Dataset.csv -f
```

## 🔧 Personalización

Para personalizar el pipeline, edita:

1. **Caracteres a normalizar:** `generic_cleaner.py` línea ~60
2. **Criterios de limpieza:** `config.py` método `analyze_data_quality()`
3. **Validaciones:** `generic_validator.py` agrega métodos `validate_*()`
4. **Análisis:** `generic_analyzer.py` agrega métodos `analyze_*()`

## 📞 Soporte

- Revisa `dataset_cleaning.log` para detalles
- Verifica los reportes generados
- Consulta `GUIA_RAPIDA.md` para ejemplos
- Edita archivos según necesidades

## ✅ Checklist

- [ ] Leí `GUIA_RAPIDA.md`
- [ ] Ejecuté `python generic_pipeline.py Dataset.csv`
- [ ] Revisé los reportes generados
- [ ] Verifiqué `Dataset_cleaned.csv`
- [ ] (Opcional) Personalicé según necesidades
- [ ] (Opcional) Procesé múltiples datasets

---

**¡El pipeline está listo para usar!** 🚀

