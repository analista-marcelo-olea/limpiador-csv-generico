#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Visualize Changes - Herramienta interactiva para visualizar cambios
Muestra cambios de forma clara y organizada
"""

import csv
import sys
from pathlib import Path
from typing import List, Dict, Tuple
from collections import defaultdict
import argparse


class ChangeAnalyzer:
    """Analiza y visualiza cambios entre archivos"""

    def __init__(self, original: str, cleaned: str, delimiter: str = ';'):
        self.original = original
        self.cleaned = cleaned
        self.delimiter = delimiter
        self.changes = []
        self.empty_cells = []  # Celdas vacías detectadas
        self.stats = {
            'total_rows': 0,
            'total_cols': 0,
            'changed_rows': 0,
            'changed_cells': 0,
            'char_removed': 0,
            'char_added': 0,
            'empty_cells_original': 0,
            'empty_cells_cleaned': 0,
            'changes_by_type': defaultdict(int)
        }
        self.column_stats = {}  # Estadísticas por columna
    
    def read_file(self, filepath: str) -> List[List[str]]:
        """Lee archivo CSV"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                reader = csv.reader(f, delimiter=self.delimiter, quotechar='"')
                return list(reader)
        except Exception as e:
            print(f"❌ Error: {e}")
            return []
    
    def analyze(self) -> None:
        """Analiza cambios entre archivos"""
        original_data = self.read_file(self.original)
        cleaned_data = self.read_file(self.cleaned)

        if not original_data or not cleaned_data:
            print("❌ Error al leer archivos")
            return

        self.stats['total_rows'] = len(original_data)
        self.stats['total_cols'] = len(original_data[0]) if original_data else 0

        # Inicializar estadísticas por columna
        self._init_column_stats(original_data)

        changed_rows = set()

        # Comparar fila por fila
        for row_idx in range(min(len(original_data), len(cleaned_data))):
            orig_row = original_data[row_idx]
            clean_row = cleaned_data[row_idx]

            for col_idx in range(min(len(orig_row), len(clean_row))):
                orig_val = orig_row[col_idx]
                clean_val = clean_row[col_idx]

                # Detectar celdas vacías
                if not orig_val.strip():
                    self.stats['empty_cells_original'] += 1
                if not clean_val.strip():
                    self.stats['empty_cells_cleaned'] += 1

                # Actualizar estadísticas por columna
                self._update_column_stats(col_idx, orig_val, clean_val)

                if orig_val != clean_val:
                    changed_rows.add(row_idx)
                    self.stats['changed_cells'] += 1

                    # Determinar tipo de cambio
                    change_type = self._classify_change(orig_val, clean_val)
                    self.stats['changes_by_type'][change_type] += 1

                    # Calcular caracteres
                    self.stats['char_removed'] += len(orig_val)
                    self.stats['char_added'] += len(clean_val)

                    self.changes.append({
                        'row': row_idx + 1,
                        'col': col_idx + 1,
                        'col_name': original_data[0][col_idx] if row_idx == 0 else 'N/A',
                        'original': orig_val,
                        'cleaned': clean_val,
                        'type': change_type
                    })

        self.stats['changed_rows'] = len(changed_rows)
    
    def _init_column_stats(self, data: List[List[str]]) -> None:
        """Inicializa estadísticas por columna"""
        num_cols = len(data[0]) if data else 0
        for col_idx in range(num_cols):
            col_name = data[0][col_idx] if data else f"Col_{col_idx}"
            self.column_stats[col_idx] = {
                'name': col_name,
                'empty_count': 0,
                'filled_count': 0,
                'total_count': 0,
                'sample_values': []
            }

    def _update_column_stats(self, col_idx: int, orig_val: str, clean_val: str) -> None:
        """Actualiza estadísticas de columna"""
        if col_idx not in self.column_stats:
            return

        stats = self.column_stats[col_idx]
        stats['total_count'] += 1

        if not clean_val.strip():
            stats['empty_count'] += 1
        else:
            stats['filled_count'] += 1
            # Guardar ejemplos de valores
            if len(stats['sample_values']) < 3:
                stats['sample_values'].append(clean_val[:50])

    def _classify_change(self, original: str, cleaned: str) -> str:
        """Clasifica el tipo de cambio"""
        # Detectar si es cambio de vacío a lleno o viceversa
        orig_empty = not original.strip()
        clean_empty = not cleaned.strip()

        if orig_empty and not clean_empty:
            return "Relleno"
        elif not orig_empty and clean_empty:
            return "Vaciado"
        elif len(original) > len(cleaned):
            return "Reducción"
        elif len(original) < len(cleaned):
            return "Expansión"
        elif original.strip() != cleaned.strip():
            return "Espacios"
        else:
            return "Caracteres"
    
    def print_summary(self) -> None:
        """Imprime resumen de cambios"""
        print("\n" + "╔" + "═" * 78 + "╗")
        print("║" + "RESUMEN DE CAMBIOS".center(78) + "║")
        print("╚" + "═" * 78 + "╝\n")

        print(f"📊 ESTADÍSTICAS GENERALES")
        print(f"  Total de filas: {self.stats['total_rows']}")
        print(f"  Total de columnas: {self.stats['total_cols']}")
        print(f"  Filas modificadas: {self.stats['changed_rows']}")
        print(f"  Celdas modificadas: {self.stats['changed_cells']}")
        print(f"  Caracteres removidos: {self.stats['char_removed']}")
        print(f"  Caracteres agregados: {self.stats['char_added']}")
        print()

        # Mostrar estadísticas de valores vacíos
        print(f"🔍 ANÁLISIS DE VALORES VACÍOS")
        print(f"  Celdas vacías en original: {self.stats['empty_cells_original']}")
        print(f"  Celdas vacías en limpio: {self.stats['empty_cells_cleaned']}")
        print()

        if self.stats['changes_by_type']:
            print(f"📈 TIPOS DE CAMBIOS")
            for change_type, count in sorted(self.stats['changes_by_type'].items(),
                                            key=lambda x: x[1], reverse=True):
                print(f"  {change_type}: {count}")
            print()
    
    def print_changes(self, limit: int = 10) -> None:
        """Imprime cambios detectados"""
        if not self.changes:
            print("✓ No se encontraron cambios")
            return
        
        print(f"📝 CAMBIOS DETECTADOS (mostrando {min(limit, len(self.changes))} de {len(self.changes)})\n")
        
        for idx, change in enumerate(self.changes[:limit], 1):
            print(f"Cambio #{idx}")
            print(f"  📍 Ubicación: Fila {change['row']}, Columna {change['col']}")
            print(f"  📋 Campo: {change['col_name']}")
            print(f"  🔄 Tipo: {change['type']}")
            print(f"  ❌ Original: {repr(change['original'][:60])}")
            print(f"  ✅ Limpio:   {repr(change['cleaned'][:60])}")
            print()
        
        if len(self.changes) > limit:
            print(f"⚠️  Hay {len(self.changes) - limit} cambios más no mostrados\n")
            self._print_remaining_summary(limit)
    
    def _print_remaining_summary(self, limit: int) -> None:
        """Imprime resumen de cambios restantes"""
        print("📋 RESUMEN DE CAMBIOS RESTANTES\n")

        changes_by_row = defaultdict(list)
        for change in self.changes[limit:]:
            changes_by_row[change['row']].append(change['col'])

        print(f"Total de cambios restantes: {len(self.changes) - limit}\n")
        print("Ubicaciones (Fila → Columnas):\n")

        for row in sorted(changes_by_row.keys())[:20]:  # Mostrar primeras 20 filas
            cols = sorted(changes_by_row[row])
            print(f"  Fila {row:4d} → Columnas {cols}")

        if len(changes_by_row) > 20:
            print(f"  ... y {len(changes_by_row) - 20} filas más")

    def print_empty_cells_analysis(self) -> None:
        """Imprime análisis de valores vacíos por columna"""
        print("\n" + "╔" + "═" * 78 + "╗")
        print("║" + "ANÁLISIS DE VALORES VACÍOS POR COLUMNA".center(78) + "║")
        print("╚" + "═" * 78 + "╝\n")

        # Filtrar columnas con valores vacíos
        empty_columns = []
        for col_idx, stats in self.column_stats.items():
            if stats['empty_count'] > 0:
                empty_percentage = (stats['empty_count'] / stats['total_count'] * 100) if stats['total_count'] > 0 else 0
                empty_columns.append({
                    'idx': col_idx,
                    'name': stats['name'],
                    'empty_count': stats['empty_count'],
                    'filled_count': stats['filled_count'],
                    'percentage': empty_percentage,
                    'samples': stats['sample_values']
                })

        if not empty_columns:
            print("✓ No se encontraron valores vacíos\n")
            return

        # Ordenar por porcentaje de vacíos
        empty_columns.sort(key=lambda x: x['percentage'], reverse=True)

        print(f"📊 COLUMNAS CON VALORES VACÍOS ({len(empty_columns)} columnas)\n")

        for col in empty_columns:
            print(f"Columna {col['idx'] + 1}: {col['name']}")
            print(f"  Vacíos: {col['empty_count']} ({col['percentage']:.1f}%)")
            print(f"  Llenos: {col['filled_count']}")

            # Sugerir acción
            if col['percentage'] > 80:
                print(f"  💡 SUGERENCIA: Eliminar columna (>80% vacíos)")
            elif col['percentage'] > 50:
                print(f"  💡 SUGERENCIA: Revisar si debe eliminarse (>50% vacíos)")
            elif col['percentage'] > 20:
                print(f"  💡 SUGERENCIA: Considerar rellenar con valor por defecto")
            else:
                print(f"  💡 SUGERENCIA: Rellenar manualmente o con interpolación")

            # Mostrar ejemplos de valores
            if col['samples']:
                print(f"  Ejemplos: {', '.join(col['samples'][:2])}")
            print()
    
    def export_report(self, output_file: str) -> None:
        """Exporta reporte a archivo"""
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("REPORTE DE CAMBIOS - VISUALIZADOR\n")
            f.write("=" * 80 + "\n\n")
            
            # Resumen
            f.write("ESTADÍSTICAS GENERALES\n")
            f.write("-" * 80 + "\n")
            f.write(f"Total de filas: {self.stats['total_rows']}\n")
            f.write(f"Total de columnas: {self.stats['total_cols']}\n")
            f.write(f"Filas modificadas: {self.stats['changed_rows']}\n")
            f.write(f"Celdas modificadas: {self.stats['changed_cells']}\n")
            f.write(f"Caracteres removidos: {self.stats['char_removed']}\n")
            f.write(f"Caracteres agregados: {self.stats['char_added']}\n\n")
            
            # Tipos de cambios
            f.write("TIPOS DE CAMBIOS\n")
            f.write("-" * 80 + "\n")
            for change_type, count in sorted(self.stats['changes_by_type'].items()):
                f.write(f"{change_type}: {count}\n")
            f.write("\n")
            
            # Cambios
            f.write("CAMBIOS DETECTADOS\n")
            f.write("-" * 80 + "\n")
            for idx, change in enumerate(self.changes, 1):
                f.write(f"\nCambio #{idx}\n")
                f.write(f"  Ubicación: Fila {change['row']}, Columna {change['col']}\n")
                f.write(f"  Campo: {change['col_name']}\n")
                f.write(f"  Tipo: {change['type']}\n")
                f.write(f"  Original: {repr(change['original'])}\n")
                f.write(f"  Limpio: {repr(change['cleaned'])}\n")
        
        print(f"✓ Reporte exportado a: {output_file}")


def main():
    parser = argparse.ArgumentParser(
        description='Visualiza cambios entre archivo original y limpio'
    )
    parser.add_argument('original', help='Archivo original')
    parser.add_argument('cleaned', help='Archivo limpio')
    parser.add_argument('-o', '--output', help='Archivo de salida para reporte')
    parser.add_argument('-l', '--limit', type=int, default=10,
                       help='Número de cambios a mostrar (default: 10)')
    parser.add_argument('--empty', action='store_true',
                       help='Mostrar análisis de valores vacíos')

    args = parser.parse_args()

    # Verificar archivos
    if not Path(args.original).exists():
        print(f"❌ Error: {args.original} no existe")
        sys.exit(1)

    if not Path(args.cleaned).exists():
        print(f"❌ Error: {args.cleaned} no existe")
        sys.exit(1)

    # Analizar
    print("🔍 Analizando cambios...")
    analyzer = ChangeAnalyzer(args.original, args.cleaned)
    analyzer.analyze()

    # Mostrar resultados
    analyzer.print_summary()
    analyzer.print_changes(args.limit)

    # Mostrar análisis de valores vacíos si se solicita
    if args.empty:
        analyzer.print_empty_cells_analysis()

    # Exportar si se especifica
    if args.output:
        analyzer.export_report(args.output)


if __name__ == '__main__':
    main()

