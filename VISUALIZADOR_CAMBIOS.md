# Visualizador de Cambios

## 📋 Descripción

El visualizador de cambios es una herramienta que compara el archivo original con el archivo limpio y muestra:

- **Cambios detectados** - Qué se modificó
- **Ubicación exacta** - Fila y columna de cada cambio
- **Tipo de cambio** - Reducción, expansión, espacios, caracteres
- **Estadísticas** - Resumen de cambios realizados
- **Resumen de ubicaciones** - Si hay más de 10 cambios, muestra dónde están

## 🚀 Uso Rápido

### Opción 1: Visualizar cambios en consola

```bash
python visualize_changes.py ../Dataset.csv ../Dataset_cleaned.csv
```

### Opción 2: Exportar reporte a archivo

```bash
python visualize_changes.py ../Dataset.csv ../Dataset_cleaned.csv -o cambios_report.txt
```

### Opción 3: Mostrar más cambios

```bash
python visualize_changes.py ../Dataset.csv ../Dataset_cleaned.csv -l 20
```

## 📊 Ejemplo de Salida

```
╔══════════════════════════════════════════════════════════════════════════╗
║                        RESUMEN DE CAMBIOS                               ║
╚══════════════════════════════════════════════════════════════════════════╝

📊 ESTADÍSTICAS GENERALES
  Total de filas: 1,784
  Total de columnas: 35
  Filas modificadas: 45
  Celdas modificadas: 127
  Caracteres removidos: 2,456
  Caracteres agregados: 1,890

📈 TIPOS DE CAMBIOS
  Reducción: 89
  Espacios: 25
  Caracteres: 13

📝 CAMBIOS DETECTADOS (mostrando 10 de 127)

Cambio #1
  📍 Ubicación: Fila 4, Columna 19
  📋 Campo: cantidad_toneladas
  🔄 Tipo: Reducción
  ❌ Original: '9,"""9814'
  ✅ Limpio:   '9,9814'

Cambio #2
  📍 Ubicación: Fila 5, Columna 19
  📋 Campo: cantidad_toneladas
  🔄 Tipo: Reducción
  ❌ Original: '75,"""204'
  ✅ Limpio:   '75,204'

...

⚠️  Hay 117 cambios más no mostrados

📋 RESUMEN DE CAMBIOS RESTANTES

Total de cambios restantes: 117

Ubicaciones (Fila → Columnas):

  Fila    6 → Columnas [19]
  Fila    7 → Columnas [19, 25]
  Fila    8 → Columnas [19]
  ...
```

## 🔧 Opciones de Línea de Comandos

### `visualize_changes.py`

```bash
python visualize_changes.py <original> <cleaned> [opciones]
```

**Argumentos:**
- `original` - Ruta del archivo original
- `cleaned` - Ruta del archivo limpio

**Opciones:**
- `-o, --output FILE` - Guardar reporte en archivo
- `-l, --limit N` - Mostrar N cambios (default: 10)

**Ejemplos:**

```bash
# Mostrar cambios en consola
python visualize_changes.py ../Dataset.csv ../Dataset_cleaned.csv

# Guardar reporte
python visualize_changes.py ../Dataset.csv ../Dataset_cleaned.csv -o reporte.txt

# Mostrar 20 cambios
python visualize_changes.py ../Dataset.csv ../Dataset_cleaned.csv -l 20

# Mostrar 20 cambios y guardar reporte
python visualize_changes.py ../Dataset.csv ../Dataset_cleaned.csv -l 20 -o reporte.txt
```

## 📈 Interpretación de Resultados

### Tipos de Cambios

| Tipo | Descripción | Ejemplo |
|------|-------------|---------|
| **Reducción** | Se removieron caracteres | `'9,"""9814'` → `'9,9814'` |
| **Expansión** | Se agregaron caracteres | `'test'` → `'test  '` |
| **Espacios** | Se normalizaron espacios | `'  test  '` → `'test'` |
| **Caracteres** | Se reemplazaron caracteres | `'café'` → `'cafe'` |

### Estadísticas

- **Filas modificadas** - Número de filas que tienen al menos un cambio
- **Celdas modificadas** - Número total de celdas que cambiaron
- **Caracteres removidos** - Total de caracteres eliminados
- **Caracteres agregados** - Total de caracteres añadidos

## 💡 Casos de Uso

### Caso 1: Verificar cambios después de limpiar

```bash
python visualize_changes.py ../Dataset.csv ../Dataset_cleaned.csv
```

### Caso 2: Generar reporte detallado

```bash
python visualize_changes.py ../Dataset.csv ../Dataset_cleaned.csv -o cambios_detallados.txt
```

### Caso 3: Analizar cambios específicos

```bash
python visualize_changes.py ../Dataset.csv ../Dataset_cleaned.csv -l 50
```

### Caso 4: Comparar múltiples limpiezas

```bash
# Primera limpieza
python visualize_changes.py ../Dataset.csv ../Dataset_cleaned_v1.csv -o cambios_v1.txt

# Segunda limpieza
python visualize_changes.py ../Dataset.csv ../Dataset_cleaned_v2.csv -o cambios_v2.txt

# Comparar reportes
diff cambios_v1.txt cambios_v2.txt
```

## 🎯 Flujo de Trabajo Recomendado

1. **Ejecutar limpieza**
   ```bash
   python generic_pipeline.py ../Dataset.csv
   ```

2. **Visualizar cambios**
   ```bash
   python visualize_changes.py ../Dataset.csv ../Dataset_cleaned.csv
   ```

3. **Revisar reporte**
   - Verificar que los cambios son correctos
   - Identificar patrones de cambios
   - Validar que no se perdieron datos importantes

4. **Exportar reporte** (opcional)
   ```bash
   python visualize_changes.py ../Dataset.csv ../Dataset_cleaned.csv -o cambios_report.txt
   ```

5. **Usar dataset limpio**
   - El archivo `Dataset_cleaned.csv` está listo para usar

## 📝 Archivos Generados

Después de ejecutar el visualizador:

- **Consola** - Resumen y cambios mostrados en pantalla
- **Archivo de reporte** (si se especifica `-o`) - Reporte completo en archivo

## ⚙️ Configuración

El visualizador detecta automáticamente:
- Delimitador (`;`, `,`, `\t`, `|`)
- Carácter de comilla (`"`, `'`)
- Encoding (UTF-8, Latin-1, etc.)

Para cambiar el delimitador, edita `visualize_changes.py` línea ~20:

```python
analyzer = ChangeAnalyzer(args.original, args.cleaned, delimiter=';')
```

## 🐛 Solución de Problemas

### Error: "Archivo no existe"
- Verifica que las rutas sean correctas
- Usa rutas relativas o absolutas según sea necesario

### No se muestran cambios
- Verifica que los archivos sean diferentes
- Comprueba que el delimitador sea correcto

### Reporte muy largo
- Usa `-l 5` para mostrar solo 5 cambios
- Usa `-o archivo.txt` para guardar en archivo

## 📞 Soporte

Para más información, consulta:
- `GUIA_RAPIDA.md` - Guía rápida del pipeline
- `README_PIPELINE_GENERICO.md` - Documentación completa
- `INDICE_ARCHIVOS.md` - Índice de archivos

---

**¡Usa el visualizador para verificar que tu limpieza es correcta!** ✓

