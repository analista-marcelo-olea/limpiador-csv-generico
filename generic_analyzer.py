"""
Analizador genérico de datasets CSV
"""

import csv
import re
from collections import Counter, defaultdict
from typing import Dict, List, Any


class GenericDatasetAnalyzer:
    """
    Analizador genérico que funciona con cualquier dataset.
    """

    def __init__(self, filepath: str, config: Dict[str, Any]):
        """
        Inicializa el analizador.
        
        Args:
            filepath: Ruta del archivo
            config: Diccionario con configuración (delimiter, quotechar, encoding)
        """
        self.filepath = filepath
        self.config = config
        self.issues = defaultdict(list)
        self.stats = {}

    def analyze_file_structure(self) -> Dict[str, Any]:
        """Analiza la estructura básica del archivo."""
        print("\n=== ANÁLISIS DE ESTRUCTURA ===")
        
        with open(self.filepath, 'r', encoding=self.config['encoding']) as f:
            content = f.read()
        
        lines = content.split('\n')
        
        stats = {
            'total_lines': len(lines),
            'file_size_chars': len(content),
            'empty_lines': sum(1 for line in lines if not line.strip()),
            'header': lines[0] if lines else None
        }
        
        print(f"Total de líneas: {stats['total_lines']:,}")
        print(f"Tamaño: {stats['file_size_chars']:,} caracteres")
        print(f"Líneas vacías: {stats['empty_lines']}")
        
        self.stats.update(stats)
        return stats

    def analyze_separators(self) -> Dict[str, Any]:
        """Analiza consistencia de separadores."""
        print("\n=== ANÁLISIS DE SEPARADORES ===")
        
        delimiter = self.config['delimiter']
        quotechar = self.config['quotechar']
        
        with open(self.filepath, 'r', encoding=self.config['encoding']) as f:
            reader = csv.reader(f, delimiter=delimiter, quotechar=quotechar)
            
            header = next(reader)
            expected_cols = len(header)
            
            inconsistent_rows = []
            
            for i, row in enumerate(reader, 2):
                if i > 100:  # Analizar primeras 100 filas
                    break
                
                if len(row) != expected_cols:
                    inconsistent_rows.append((i, len(row), expected_cols))
                    self.issues['separator_inconsistency'].append({
                        'line': i,
                        'found': len(row),
                        'expected': expected_cols
                    })
        
        separator_stats = {
            'expected_columns': expected_cols,
            'inconsistent_rows': len(inconsistent_rows),
            'delimiter': delimiter
        }
        
        print(f"Columnas esperadas: {expected_cols}")
        print(f"Filas inconsistentes: {len(inconsistent_rows)}")
        
        self.stats.update(separator_stats)
        return separator_stats

    def analyze_character_encoding(self) -> Dict[str, Any]:
        """Analiza problemas de codificación."""
        print("\n=== ANÁLISIS DE CODIFICACIÓN ===")
        
        with open(self.filepath, 'r', encoding=self.config['encoding']) as f:
            content = f.read()
        
        problematic_chars = set()
        html_entities = []
        
        for char in content:
            if ord(char) > 127:
                problematic_chars.add(char)
        
        html_pattern = re.compile(r'&[a-zA-Z]+;|&#\d+;')
        html_entities = html_pattern.findall(content)
        
        encoding_stats = {
            'non_ascii_chars': len(problematic_chars),
            'html_entities': len(set(html_entities))
        }
        
        print(f"Caracteres no ASCII: {len(problematic_chars)}")
        print(f"Entidades HTML: {len(set(html_entities))}")
        
        self.stats.update(encoding_stats)
        return encoding_stats

    def analyze_data_quality(self) -> Dict[str, Any]:
        """Analiza la calidad general de los datos."""
        print("\n=== ANÁLISIS DE CALIDAD ===")
        
        delimiter = self.config['delimiter']
        quotechar = self.config['quotechar']
        
        quality_stats = {
            'empty_fields': 0,
            'duplicate_rows': 0,
            'rows_analyzed': 0
        }
        
        with open(self.filepath, 'r', encoding=self.config['encoding']) as f:
            reader = csv.reader(f, delimiter=delimiter, quotechar=quotechar)
            next(reader)  # Skip header
            
            seen_rows = set()
            
            for i, row in enumerate(reader):
                if i >= 1000:  # Analizar primeras 1000 filas
                    break
                
                quality_stats['rows_analyzed'] += 1
                
                # Contar campos vacíos
                empty_count = sum(1 for field in row if not field.strip())
                quality_stats['empty_fields'] += empty_count
                
                # Detectar duplicados
                row_tuple = tuple(row)
                if row_tuple in seen_rows:
                    quality_stats['duplicate_rows'] += 1
                seen_rows.add(row_tuple)
        
        print(f"Filas analizadas: {quality_stats['rows_analyzed']}")
        print(f"Campos vacíos: {quality_stats['empty_fields']}")
        print(f"Filas duplicadas: {quality_stats['duplicate_rows']}")
        
        self.stats.update(quality_stats)
        return quality_stats

    def generate_report(self) -> str:
        """Genera reporte de análisis."""
        report = []
        report.append("=" * 60)
        report.append("REPORTE DE ANÁLISIS DE DATASET")
        report.append("=" * 60)
        report.append(f"Archivo: {self.filepath}")
        report.append("")
        
        report.append("CONFIGURACIÓN DETECTADA:")
        report.append(f"- Delimitador: {repr(self.config['delimiter'])}")
        report.append(f"- Comilla: {repr(self.config['quotechar'])}")
        report.append(f"- Encoding: {self.config['encoding']}")
        report.append("")
        
        report.append("ESTADÍSTICAS:")
        for key, value in self.stats.items():
            report.append(f"- {key}: {value}")
        report.append("")
        
        total_issues = sum(len(v) for v in self.issues.values())
        report.append(f"PROBLEMAS ENCONTRADOS: {total_issues}")
        
        if total_issues > 0:
            report.append("\nRECOMENDACIONES:")
            report.append("1. Ejecutar limpieza de datos")
            report.append("2. Validar después de la limpieza")
        
        return "\n".join(report)

