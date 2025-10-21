"""
Validador genérico de datasets CSV
"""

import csv
import re
from typing import Dict, Any


class GenericDatasetValidator:
    """
    Validador genérico que funciona con cualquier dataset.
    """

    def __init__(self, original_file: str, cleaned_file: str, config: Dict[str, Any]):
        """
        Inicializa el validador.
        
        Args:
            original_file: Ruta del archivo original
            cleaned_file: Ruta del archivo limpio
            config: Diccionario con configuración
        """
        self.original_file = original_file
        self.cleaned_file = cleaned_file
        self.config = config
        self.validation_results = {}

    def validate_csv_structure(self) -> Dict[str, Any]:
        """Valida la estructura del CSV limpio."""
        print("\n=== VALIDACIÓN DE ESTRUCTURA ===")
        
        results = {
            'is_valid_csv': True,
            'total_rows': 0,
            'total_columns': 0,
            'consistent_columns': True,
            'errors': []
        }
        
        try:
            delimiter = self.config['delimiter']
            quotechar = self.config['quotechar']
            
            with open(self.cleaned_file, 'r', encoding='utf-8') as f:
                reader = csv.reader(f, delimiter=delimiter, quotechar=quotechar)
                
                header = next(reader)
                expected_columns = len(header)
                results['total_columns'] = expected_columns
                results['header'] = header
                
                for row_num, row in enumerate(reader, 2):
                    results['total_rows'] += 1
                    
                    if len(row) != expected_columns:
                        results['consistent_columns'] = False
                        results['errors'].append(
                            f"Fila {row_num}: {len(row)} columnas (esperadas: {expected_columns})"
                        )
                        
                        if len(results['errors']) >= 10:
                            break
        
        except Exception as e:
            results['is_valid_csv'] = False
            results['errors'].append(f"Error leyendo CSV: {str(e)}")
        
        # Mostrar resultados
        if results['is_valid_csv']:
            print(f"✓ CSV válido")
            print(f"  Filas: {results['total_rows']:,}")
            print(f"  Columnas: {results['total_columns']}")
            
            if results['consistent_columns']:
                print(f"✓ Estructura consistente")
            else:
                print(f"⚠ Inconsistencias encontradas: {len(results['errors'])}")
        else:
            print(f"✗ CSV inválido")
        
        self.validation_results['structure'] = results
        return results

    def validate_character_encoding(self) -> Dict[str, Any]:
        """Valida la codificación de caracteres."""
        print("\n=== VALIDACIÓN DE CODIFICACIÓN ===")
        
        results = {
            'problematic_chars_found': 0,
            'html_entities_found': 0,
            'encoding_issues': []
        }
        
        with open(self.cleaned_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Buscar caracteres problemáticos
        problematic_chars = set()
        for char in content:
            if ord(char) > 127 and char not in 'áéíóúñüÁÉÍÓÚÑÜ':
                problematic_chars.add(char)
        
        results['problematic_chars_found'] = len(problematic_chars)
        
        # Buscar entidades HTML
        html_pattern = re.compile(r'&[a-zA-Z]+;|&#\d+;')
        html_entities = html_pattern.findall(content)
        results['html_entities_found'] = len(html_entities)
        
        if results['problematic_chars_found'] == 0:
            print(f"✓ No hay caracteres problemáticos")
        else:
            print(f"⚠ Caracteres problemáticos: {results['problematic_chars_found']}")
        
        if results['html_entities_found'] == 0:
            print(f"✓ No hay entidades HTML residuales")
        else:
            print(f"⚠ Entidades HTML: {results['html_entities_found']}")
        
        self.validation_results['encoding'] = results
        return results

    def validate_data_integrity(self) -> Dict[str, Any]:
        """Valida la integridad de los datos."""
        print("\n=== VALIDACIÓN DE INTEGRIDAD ===")
        
        results = {
            'original_rows': 0,
            'cleaned_rows': 0,
            'row_difference': 0,
            'data_preserved': True
        }
        
        # Contar filas originales
        try:
            with open(self.original_file, 'r', encoding=self.config['encoding']) as f:
                results['original_rows'] = sum(1 for _ in f) - 1  # Restar header
        except Exception as e:
            print(f"⚠ Error leyendo original: {e}")
        
        # Contar filas limpias
        try:
            delimiter = self.config['delimiter']
            quotechar = self.config['quotechar']
            
            with open(self.cleaned_file, 'r', encoding='utf-8') as f:
                reader = csv.reader(f, delimiter=delimiter, quotechar=quotechar)
                next(reader)  # Skip header
                results['cleaned_rows'] = sum(1 for _ in reader)
        except Exception as e:
            print(f"⚠ Error leyendo limpio: {e}")
        
        results['row_difference'] = abs(results['original_rows'] - results['cleaned_rows'])
        
        # Permitir pequeña diferencia (filas vacías, etc.)
        if results['row_difference'] <= 5:
            print(f"✓ Integridad de datos preservada")
            print(f"  Original: {results['original_rows']:,} filas")
            print(f"  Limpio: {results['cleaned_rows']:,} filas")
        else:
            print(f"⚠ Diferencia significativa: {results['row_difference']} filas")
            results['data_preserved'] = False
        
        self.validation_results['integrity'] = results
        return results

    def generate_report(self) -> str:
        """Genera reporte de validación."""
        report = []
        report.append("=" * 60)
        report.append("REPORTE DE VALIDACIÓN")
        report.append("=" * 60)
        report.append(f"Archivo original: {self.original_file}")
        report.append(f"Archivo limpio: {self.cleaned_file}")
        report.append("")
        
        # Resumen
        structure_ok = self.validation_results.get('structure', {}).get('is_valid_csv', False)
        encoding_ok = self.validation_results.get('encoding', {}).get('problematic_chars_found', 1) == 0
        integrity_ok = self.validation_results.get('integrity', {}).get('data_preserved', False)
        
        report.append("RESUMEN:")
        report.append(f"- Estructura CSV: {'✓ OK' if structure_ok else '✗ ERROR'}")
        report.append(f"- Codificación: {'✓ OK' if encoding_ok else '✗ ERROR'}")
        report.append(f"- Integridad: {'✓ OK' if integrity_ok else '✗ ERROR'}")
        report.append("")
        
        if all([structure_ok, encoding_ok, integrity_ok]):
            report.append("✓ VALIDACIÓN EXITOSA")
        else:
            report.append("⚠ VALIDACIÓN CON OBSERVACIONES")
        
        return "\n".join(report)

