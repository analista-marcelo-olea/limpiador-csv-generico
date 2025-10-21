"""
Configuración automática para detectar características del dataset
"""

import csv
from typing import Dict, Any, Tuple
from collections import Counter


class DatasetConfig:
    """
    Detecta automáticamente las características del dataset
    (delimitador, quotechar, encoding, etc.)
    """

    def __init__(self, filepath: str):
        self.filepath = filepath
        self.config = {}

    def detect_delimiter(self) -> str:
        """
        Detecta automáticamente el delimitador del CSV.
        Prueba: ; , \t | 
        """
        delimiters = [';', ',', '\t', '|']
        
        with open(self.filepath, 'r', encoding='utf-8') as f:
            first_line = f.readline()
        
        # Contar ocurrencias de cada delimitador
        delimiter_counts = {d: first_line.count(d) for d in delimiters}
        
        # El delimitador más probable es el que más aparece
        detected = max(delimiter_counts, key=delimiter_counts.get)
        
        print(f"✓ Delimitador detectado: {repr(detected)}")
        return detected

    def detect_quotechar(self) -> str:
        """
        Detecta el carácter de comilla usado.
        Típicamente: " o '
        """
        with open(self.filepath, 'r', encoding='utf-8') as f:
            content = f.read(10000)  # Primeros 10KB
        
        double_quotes = content.count('"')
        single_quotes = content.count("'")
        
        quotechar = '"' if double_quotes > single_quotes else "'"
        print(f"✓ Carácter de comilla detectado: {repr(quotechar)}")
        return quotechar

    def detect_encoding(self) -> str:
        """
        Detecta el encoding del archivo.
        """
        encodings = ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252']
        
        for encoding in encodings:
            try:
                with open(self.filepath, 'r', encoding=encoding) as f:
                    f.read(1000)
                print(f"✓ Encoding detectado: {encoding}")
                return encoding
            except (UnicodeDecodeError, LookupError):
                continue
        
        print("⚠ Encoding por defecto: utf-8")
        return 'utf-8'

    def detect_column_count(self, delimiter: str, quotechar: str) -> int:
        """
        Detecta el número de columnas.
        """
        with open(self.filepath, 'r', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter=delimiter, quotechar=quotechar)
            header = next(reader)
            col_count = len(header)
        
        print(f"✓ Columnas detectadas: {col_count}")
        return col_count

    def detect_row_count(self) -> int:
        """
        Detecta el número de filas de datos.
        """
        with open(self.filepath, 'r', encoding='utf-8') as f:
            row_count = sum(1 for _ in f) - 1  # Restar header
        
        print(f"✓ Filas detectadas: {row_count:,}")
        return row_count

    def analyze_data_quality(self, delimiter: str, quotechar: str) -> Dict[str, Any]:
        """
        Analiza la calidad de los datos para determinar si necesita limpieza.
        """
        issues = {
            'encoding_issues': 0,
            'separator_inconsistencies': 0,
            'unbalanced_quotes': 0,
            'empty_fields': 0,
            'html_entities': 0,
            'special_chars': 0
        }
        
        with open(self.filepath, 'r', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter=delimiter, quotechar=quotechar)
            header = next(reader)
            expected_cols = len(header)
            
            for i, row in enumerate(reader):
                if i >= 1000:  # Analizar primeras 1000 filas
                    break
                
                # Verificar inconsistencias de separadores
                if len(row) != expected_cols:
                    issues['separator_inconsistencies'] += 1
                
                # Verificar campos vacíos
                empty_count = sum(1 for field in row if not field.strip())
                if empty_count > 0:
                    issues['empty_fields'] += empty_count
                
                # Verificar entidades HTML
                for field in row:
                    if '&' in field and ';' in field:
                        issues['html_entities'] += 1
                        break
                    
                    # Verificar caracteres especiales problemáticos
                    for char in field:
                        if ord(char) > 127 and char not in 'áéíóúñüÁÉÍÓÚÑÜ':
                            issues['special_chars'] += 1
                            break
        
        return issues

    def get_config(self) -> Dict[str, Any]:
        """
        Retorna la configuración completa del dataset.
        """
        print("\n" + "=" * 60)
        print("DETECCIÓN AUTOMÁTICA DE CONFIGURACIÓN DEL DATASET")
        print("=" * 60 + "\n")
        
        delimiter = self.detect_delimiter()
        quotechar = self.detect_quotechar()
        encoding = self.detect_encoding()
        col_count = self.detect_column_count(delimiter, quotechar)
        row_count = self.detect_row_count()
        quality_issues = self.analyze_data_quality(delimiter, quotechar)
        
        # Determinar si necesita limpieza
        total_issues = sum(quality_issues.values())
        needs_cleaning = total_issues > 0
        
        self.config = {
            'filepath': self.filepath,
            'delimiter': delimiter,
            'quotechar': quotechar,
            'encoding': encoding,
            'columns': col_count,
            'rows': row_count,
            'quality_issues': quality_issues,
            'total_issues': total_issues,
            'needs_cleaning': needs_cleaning
        }
        
        print(f"\n📊 Análisis de Calidad:")
        print(f"   Problemas encontrados: {total_issues}")
        print(f"   Necesita limpieza: {'Sí' if needs_cleaning else 'No'}")
        
        return self.config

