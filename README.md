# 🚀 Pipeline Genérico de Limpieza de Datasets

Un pipeline automático e inteligente que limpia y valida **cualquier dataset CSV** sin necesidad de configuración manual. Detecta automáticamente delimitadores, encodings y problemas de calidad de datos.

## ✨ Características Principales

### 🔍 Detección Automática
- **Delimitador**: `;`, `,`, `\t`, `|`
- **Encoding**: UTF-8, Latin-1, ISO-8859-1, CP1252
- **Carácter de comilla**: `"` o `'`
- **Estructura**: Número de columnas y filas
- **Problemas de calidad**: Caracteres Unicode, entidades HTML, espacios inconsistentes

### 🧹 Limpieza Inteligente
- Elimina caracteres Unicode problemáticos
- Convierte entidades HTML
- Normaliza espacios en blanco
- Corrige inconsistencias de separadores
- Preserva la integridad de los datos

### ✅ Validación Completa
- Verifica estructura del dataset
- Valida tipos de datos
- Detecta valores faltantes
- Genera reportes detallados

### 📊 Análisis de Valores Vacíos
- Detecta celdas vacías por columna
- Calcula porcentajes de vacíos
- Proporciona sugerencias automáticas
- Ayuda a decidir si eliminar o rellenar columnas

## 📦 Contenido del Pipeline

```
pipeline_generico/
├── generic_pipeline.py          # Orquestador principal
├── config.py                    # Detección automática de configuración
├── generic_analyzer.py          # Análisis de calidad de datos
├── generic_cleaner.py           # Limpieza de datos
├── generic_validator.py         # Validación de resultados
├── batch_process.py             # Procesamiento de múltiples archivos
├── visualize_changes.py         # Visualizador de cambios
└── change_visualizer.py         # Alternativa de visualizador
```

## 🚀 Inicio Rápido

### Instalación

```bash
# Clonar o descargar el repositorio
git clone <limpiador-csv-generico>
cd pipeline_generico
```

### Uso Básico

```bash
# Procesar un dataset
python generic_pipeline.py Dataset.csv
```

El pipeline automáticamente:
1. ✅ Detecta la configuración del dataset
2. ✅ Analiza la calidad de datos
3. ✅ Limpia si es necesario
4. ✅ Valida los resultados
5. ✅ Genera reportes detallados

### Opciones Disponibles

```bash
# Especificar directorio de salida
python generic_pipeline.py Dataset.csv -o ./output

# Forzar limpieza (incluso si no detecta problemas)
python generic_pipeline.py Dataset.csv -f

# Procesar múltiples datasets
python batch_process.py "*.csv"

# Procesar carpeta específica
python batch_process.py "data/*.csv" -o ./cleaned_data
```

## 📊 Archivos Generados

Después de ejecutar el pipeline, encontrarás:

```
Dataset_cleaned.csv                    # Dataset limpio
dataset_analysis_report.txt            # Reporte de análisis
dataset_cleaning_report.txt            # Reporte de limpieza
dataset_validation_report.txt          # Reporte de validación
dataset_cleaning.log                   # Log detallado
```

## 🔍 Visualizar Cambios

Compara el dataset original con el limpio:

```bash
# Ver cambios en consola
python visualize_changes.py Dataset.csv Dataset_cleaned.csv

# Analizar valores vacíos
python visualize_changes.py Dataset.csv Dataset_cleaned.csv --empty

# Guardar reporte
python visualize_changes.py Dataset.csv Dataset_cleaned.csv --empty -o reporte.txt

# Mostrar más cambios
python visualize_changes.py Dataset.csv Dataset_cleaned.csv -l 20
```

### Tipos de Cambios Detectados

| Tipo | Descripción | Ejemplo |
|------|-------------|---------|
| **Reducción** | Se removieron caracteres | `'9,"""9814'` → `'9,9814'` |
| **Expansión** | Se agregaron caracteres | `'test'` → `'test  '` |
| **Espacios** | Se normalizaron espacios | `'  test  '` → `'test'` |
| **Caracteres** | Se reemplazaron caracteres | `'café'` → `'cafe'` |
| **Relleno** | Se rellenó un valor vacío | `''` → `'valor'` |
| **Vaciado** | Se vació un valor | `'valor'` → `''` |

## 💡 Casos de Uso

### Caso 1: Dataset con delimitador `;`
```bash
python generic_pipeline.py ventas.csv
```
Detecta automáticamente el delimitador.

### Caso 2: Procesar carpeta completa
```bash
python batch_process.py "datasets/*.csv" -o ./cleaned_datasets
```
Procesa todos los CSV y guarda en carpeta de salida.

### Caso 3: Identificar columnas problemáticas
```bash
python visualize_changes.py Dataset.csv Dataset_cleaned.csv --empty
```
Muestra qué columnas tienen muchos valores vacíos.

### Caso 4: Generar reporte completo
```bash
python visualize_changes.py Dataset.csv Dataset_cleaned.csv --empty -l 20 -o reporte_completo.txt
```
Análisis completo con cambios y valores vacíos.

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

## 📋 Requisitos

- Python 3.7+
- Librerías estándar (csv, chardet, etc.)

## ⚠️ Limitaciones

- No modifica la estructura del dataset (número de columnas)
- No elimina filas (solo omite si hay error de parsing)
- No realiza transformaciones de datos complejas

## 🐛 Troubleshooting

### Error: "Archivo no encontrado"
```bash
# Verifica que el archivo existe
ls -la Dataset.csv
```

### Error: "Encoding no soportado"
El pipeline intentará detectar automáticamente. Si falla, especifica manualmente en `config.py`.

### Dataset no se limpia
Usa la opción `-f` para forzar limpieza:
```bash
python generic_pipeline.py Dataset.csv -f
```

## 📈 Ejemplo de Salida

```
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

## 📚 Documentación Adicional

- `README_PIPELINE_GENERICO.md` - Documentación técnica completa
- `GUIA_RAPIDA.md` - Guía de inicio rápido
- `VISUALIZADOR_CAMBIOS.md` - Documentación del visualizador
- `EJEMPLOS_AVANZADOS.md` - Casos de uso avanzados

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:
1. Fork el proyecto
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo licencia MIT.

## 📞 Soporte

Para problemas o sugerencias, revisa los logs en `dataset_cleaning.log` o abre un issue en el repositorio.
Contacto: analista.marcelo.olea@gmail.com

---

**¡Hecho con ❤️ para simplificar la limpieza de datos!**

