"""
Limpiador genérico de datasets CSV
Funciona con cualquier delimitador y estructura
"""

import csv
import re
import html
import unicodedata
import os
import shutil
from typing import List, Tuple, Dict, Any
import logging


class GenericDatasetCleaner:
    """
    Limpiador genérico que se adapta a cualquier dataset.
    """

    def __init__(self, input_file: str, output_file: str, config: Dict[str, Any]):
        """
        Inicializa el limpiador con configuración automática.
        
        Args:
            input_file: Ruta del archivo original
            output_file: Ruta del archivo limpio
            config: Diccionario con configuración (delimiter, quotechar, encoding, etc.)
        """
        self.input_file = input_file
        self.output_file = output_file
        self.config = config
        
        # Configurar logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('dataset_cleaning.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

        # Estadísticas
        self.stats = {
            'total_rows': 0,
            'cleaned_rows': 0,
            'skipped_rows': 0,
            'character_replacements': 0,
            'html_entities_fixed': 0,
            'whitespace_normalized': 0
        }

        # Diccionario de reemplazos
        self.char_replacements = {
            '"': '"',  # Comilla izquierda
            '"': '"',  # Comilla derecha
            ''': "'",  # Apóstrofo izquierdo
            ''': "'",  # Apóstrofo derecho
            '–': "-",  # Guion medio
            '—': "-",  # Guion largo
            ' ': " ",  # Espacio no rompible
            '…': "...",  # Puntos suspensivos
            '®': "(R)",  # Signo de registro
            '©': "(C)",  # Signo de derechos de autor
            '™': "(TM)",  # Marca registrada
        }

    def normalize_unicode(self, text: str) -> str:
        """Normaliza caracteres Unicode."""
        if not text:
            return text
        
        normalized = unicodedata.normalize('NFD', text)
        
        for old_char, new_char in self.char_replacements.items():
            if old_char in normalized:
                normalized = normalized.replace(old_char, new_char)
                self.stats['character_replacements'] += 1
        
        return normalized

    def clean_html_entities(self, text: str) -> str:
        """Limpia entidades HTML."""
        if not text:
            return text
        
        text = html.unescape(text)
        
        html_fixes = {
            '&#269;': 'c',
            '&#305;': 'i',
            '&#345;': 'r',
            '&#8217;': "'",
            '&#8230;': '...',
        }
        
        for entity, replacement in html_fixes.items():
            if entity in text:
                text = text.replace(entity, replacement)
                self.stats['html_entities_fixed'] += 1
        
        text = re.sub(r'<br\s*/?>', ' ', text)
        text = re.sub(r'<[^>]+>', '', text)
        
        return text

    def normalize_whitespace(self, text: str) -> str:
        """Normaliza espacios en blanco."""
        if not text:
            return text
        
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        self.stats['whitespace_normalized'] += 1
        
        return text

    def clean_row(self, row_data: str) -> Tuple[List[str], bool]:
        """Limpia una fila completa."""
        try:
            import io
            delimiter = self.config['delimiter']
            quotechar = self.config['quotechar']
            
            csv_reader = csv.reader(
                io.StringIO(row_data),
                quotechar=quotechar,
                delimiter=delimiter
            )
            
            try:
                fields = next(csv_reader)
            except (csv.Error, StopIteration):
                fields = row_data.split(delimiter)
            
            cleaned_fields = []
            for field in fields:
                cleaned_field = field
                cleaned_field = self.normalize_unicode(cleaned_field)
                cleaned_field = self.clean_html_entities(cleaned_field)
                cleaned_field = self.normalize_whitespace(cleaned_field)
                cleaned_fields.append(cleaned_field)
            
            return cleaned_fields, True
        
        except Exception as e:
            self.logger.warning(f"Error limpiando fila: {str(e)[:100]}...")
            return [], False

    def process_file(self) -> Dict[str, Any]:
        """Procesa el archivo completo."""
        self.logger.info(f"Iniciando limpieza de {self.input_file}")
        
        temp_output = self.output_file + '.tmp'
        delimiter = self.config['delimiter']
        quotechar = self.config['quotechar']
        encoding = self.config['encoding']
        
        with open(self.input_file, 'r', encoding=encoding) as infile, \
             open(temp_output, 'w', encoding='utf-8', newline='') as outfile:
            
            csv_writer = csv.writer(
                outfile,
                quoting=csv.QUOTE_MINIMAL,
                delimiter=delimiter
            )
            
            for line_num, line in enumerate(infile, 1):
                self.stats['total_rows'] += 1
                line = line.rstrip('\n\r')
                
                if line_num == 1:
                    # Header
                    header_fields = line.split(delimiter)
                    csv_writer.writerow(header_fields)
                    self.stats['cleaned_rows'] += 1
                    continue
                
                if not line.strip():
                    self.stats['skipped_rows'] += 1
                    continue
                
                cleaned_fields, success = self.clean_row(line)
                
                if success and len(cleaned_fields) > 0:
                    csv_writer.writerow(cleaned_fields)
                    self.stats['cleaned_rows'] += 1
                else:
                    self.stats['skipped_rows'] += 1
                
                if line_num % 10000 == 0:
                    self.logger.info(f"Procesadas {line_num:,} filas...")
        
        # Renombrar archivo temporal
        try:
            if os.path.exists(self.output_file):
                os.remove(self.output_file)
            shutil.move(temp_output, self.output_file)
        except Exception as e:
            self.logger.error(f"Error renombrando archivo: {str(e)}")
            raise
        
        self.logger.info(f"Limpieza completada. Archivo guardado: {self.output_file}")
        return self.stats

    def generate_report(self) -> str:
        """Genera reporte de limpieza."""
        from datetime import date
        
        report = []
        report.append("=" * 60)
        report.append("REPORTE DE LIMPIEZA DE DATOS")
        report.append("=" * 60)
        report.append(f"Archivo original: {self.input_file}")
        report.append(f"Archivo limpio: {self.output_file}")
        report.append(f"Fecha: {date.today()}")
        report.append("")
        
        stats = self.stats
        report.append("ESTADÍSTICAS:")
        report.append(f"- Total de filas: {stats['total_rows']:,}")
        report.append(f"- Filas limpiadas: {stats['cleaned_rows']:,}")
        report.append(f"- Filas omitidas: {stats['skipped_rows']:,}")
        report.append(f"- Tasa de éxito: {(stats['cleaned_rows']/stats['total_rows']*100):.2f}%")
        report.append("")
        
        report.append("CORRECCIONES APLICADAS:")
        report.append(f"- Caracteres normalizados: {stats['character_replacements']:,}")
        report.append(f"- Entidades HTML corregidas: {stats['html_entities_fixed']:,}")
        report.append(f"- Espacios normalizados: {stats['whitespace_normalized']:,}")
        
        return "\n".join(report)

