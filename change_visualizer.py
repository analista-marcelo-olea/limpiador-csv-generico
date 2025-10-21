#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Change Visualizer - Visualiza los cambios realizados por el limpiador
Compara el archivo original con el limpio y genera un reporte detallado
"""

import csv
import sys
from pathlib import Path
from typing import List, Tuple, Dict
from datetime import datetime


class ChangeVisualizer:
    """Visualiza cambios entre archivo original y limpio"""
    
    def __init__(self, original_file: str, cleaned_file: str, config: Dict = None):
        self.original_file = original_file
        self.cleaned_file = cleaned_file
        self.config = config or {}
        self.delimiter = self.config.get('delimiter', ';')
        self.quotechar = self.config.get('quotechar', '"')
        self.changes = []
        self.max_display = 10
        
    def read_csv_file(self, filepath: str) -> List[List[str]]:
        """Lee archivo CSV con configuración automática"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                reader = csv.reader(f, delimiter=self.delimiter, quotechar=self.quotechar)
                return list(reader)
        except Exception as e:
            print(f"Error leyendo {filepath}: {e}")
            return []
    
    def compare_files(self) -> None:
        """Compara archivos original y limpio"""
        original = self.read_csv_file(self.original_file)
        cleaned = self.read_csv_file(self.cleaned_file)
        
        if not original or not cleaned:
            print("Error: No se pudieron leer los archivos")
            return
        
        # Comparar fila por fila
        for row_idx in range(min(len(original), len(cleaned))):
            original_row = original[row_idx]
            cleaned_row = cleaned[row_idx]
            
            # Comparar celda por celda
            for col_idx in range(min(len(original_row), len(cleaned_row))):
                if original_row[col_idx] != cleaned_row[col_idx]:
                    self.changes.append({
                        'row': row_idx + 1,
                        'col': col_idx + 1,
                        'original': original_row[col_idx],
                        'cleaned': cleaned_row[col_idx],
                        'column_name': original[0][col_idx] if row_idx > 0 else 'N/A'
                    })
    
    def generate_report(self, output_file: str = None) -> str:
        """Genera reporte de cambios"""
        if not self.changes:
            return "✓ No se encontraron cambios"
        
        report = []
        report.append("╔" + "═" * 78 + "╗")
        report.append("║" + " " * 78 + "║")
        report.append("║" + "REPORTE DE CAMBIOS - VISUALIZADOR DE LIMPIEZA".center(78) + "║")
        report.append("║" + " " * 78 + "║")
        report.append("╚" + "═" * 78 + "╝")
        report.append("")
        report.append(f"📊 RESUMEN")
        report.append(f"  Total de cambios: {len(self.changes)}")
        report.append(f"  Archivo original: {self.original_file}")
        report.append(f"  Archivo limpio: {self.cleaned_file}")
        report.append(f"  Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        # Mostrar primeros 10 cambios
        report.append("📝 PRIMEROS CAMBIOS DETECTADOS")
        report.append("")
        
        for idx, change in enumerate(self.changes[:self.max_display], 1):
            report.append(f"Cambio #{idx}")
            report.append(f"  Ubicación: Fila {change['row']}, Columna {change['col']}")
            report.append(f"  Columna: {change['column_name']}")
            report.append(f"  Original:  {repr(change['original'][:50])}")
            report.append(f"  Limpio:    {repr(change['cleaned'][:50])}")
            
            # Mostrar diferencia
            if len(change['original']) != len(change['cleaned']):
                report.append(f"  Diferencia: {len(change['original'])} → {len(change['cleaned'])} caracteres")
            report.append("")
        
        # Si hay más de 10 cambios, mostrar resumen
        if len(self.changes) > self.max_display:
            report.append("📋 RESUMEN DE CAMBIOS RESTANTES")
            report.append("")
            report.append(f"Total de cambios restantes: {len(self.changes) - self.max_display}")
            report.append("")
            report.append("Ubicaciones de cambios (Fila, Columna):")
            report.append("")
            
            # Agrupar por fila
            changes_by_row = {}
            for change in self.changes[self.max_display:]:
                row = change['row']
                if row not in changes_by_row:
                    changes_by_row[row] = []
                changes_by_row[row].append(change['col'])
            
            for row in sorted(changes_by_row.keys()):
                cols = sorted(changes_by_row[row])
                report.append(f"  Fila {row}: Columnas {cols}")
        
        report.append("")
        report.append("═" * 80)
        
        report_text = "\n".join(report)
        
        # Guardar en archivo si se especifica
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(report_text)
            print(f"✓ Reporte guardado en: {output_file}")
        
        return report_text
    
    def print_report(self) -> None:
        """Imprime el reporte en consola"""
        report = self.generate_report()
        print(report)


def main():
    """Función principal"""
    if len(sys.argv) < 3:
        print("Uso: python change_visualizer.py <archivo_original> <archivo_limpio> [archivo_salida]")
        print("")
        print("Ejemplo:")
        print("  python change_visualizer.py ../Dataset.csv ../Dataset_cleaned.csv changes_report.txt")
        sys.exit(1)
    
    original_file = sys.argv[1]
    cleaned_file = sys.argv[2]
    output_file = sys.argv[3] if len(sys.argv) > 3 else None
    
    # Verificar que los archivos existen
    if not Path(original_file).exists():
        print(f"Error: Archivo no encontrado: {original_file}")
        sys.exit(1)
    
    if not Path(cleaned_file).exists():
        print(f"Error: Archivo no encontrado: {cleaned_file}")
        sys.exit(1)
    
    # Crear visualizador
    visualizer = ChangeVisualizer(original_file, cleaned_file)
    
    # Comparar archivos
    print("Comparando archivos...")
    visualizer.compare_files()
    
    # Generar reporte
    if output_file:
        visualizer.generate_report(output_file)
    
    # Imprimir reporte
    visualizer.print_report()


if __name__ == '__main__':
    main()

