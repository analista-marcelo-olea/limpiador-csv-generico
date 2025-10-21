"""
Pipeline genérico y automático para limpieza de datasets
Funciona con cualquier CSV sin necesidad de configuración manual
"""

import os
import sys
import argparse
from datetime import datetime
from pathlib import Path

from config import DatasetConfig
from generic_analyzer import GenericDatasetAnalyzer
from generic_cleaner import GenericDatasetCleaner
from generic_validator import GenericDatasetValidator


class GenericDataPipeline:
    """
    Pipeline automático y genérico para cualquier dataset CSV.
    """

    def __init__(self, input_file: str, output_dir: str = None, force_clean: bool = False):
        """
        Inicializa el pipeline.
        
        Args:
            input_file: Ruta del archivo CSV a procesar
            output_dir: Directorio de salida (por defecto, mismo que input)
            force_clean: Forzar limpieza incluso si no hay problemas detectados
        """
        self.input_file = input_file
        self.output_dir = output_dir or os.path.dirname(input_file) or '.'
        self.force_clean = force_clean
        self.config = None
        self.start_time = datetime.now()
        self.execution_log = []

    def log_step(self, step_name: str, status: str, details: str = ""):
        """Registra un paso del pipeline."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        status_icon = {
            'SUCCESS': '✅',
            'ERROR': '❌',
            'WARNING': '⚠️',
            'INFO': 'ℹ️'
        }.get(status, '📝')
        
        print(f"{status_icon} [{timestamp}] {step_name}: {status}")
        if details:
            for line in details.splitlines():
                print(f"   {line}")
        
        self.execution_log.append({
            'timestamp': timestamp,
            'step': step_name,
            'status': status,
            'details': details
        })

    def detect_configuration(self) -> bool:
        """Detecta automáticamente la configuración del dataset."""
        try:
            self.log_step("Detección de Configuración", "INFO", "Analizando estructura del dataset...")
            
            config_detector = DatasetConfig(self.input_file)
            self.config = config_detector.get_config()
            
            self.log_step("Detección de Configuración", "SUCCESS", 
                         f"Configuración detectada:\n"
                         f"  Delimitador: {repr(self.config['delimiter'])}\n"
                         f"  Comilla: {repr(self.config['quotechar'])}\n"
                         f"  Encoding: {self.config['encoding']}\n"
                         f"  Columnas: {self.config['columns']}\n"
                         f"  Filas: {self.config['rows']:,}")
            return True
        
        except Exception as e:
            self.log_step("Detección de Configuración", "ERROR", str(e))
            return False

    def analyze_dataset(self) -> bool:
        """Analiza la calidad del dataset."""
        try:
            self.log_step("Análisis de Calidad", "INFO", "Analizando calidad de datos...")
            
            analyzer = GenericDatasetAnalyzer(self.input_file, self.config)
            analyzer.analyze_file_structure()
            analyzer.analyze_separators()
            analyzer.analyze_character_encoding()
            analyzer.analyze_data_quality()
            
            report = analyzer.generate_report()
            print("\n" + report)
            
            # Guardar reporte
            report_file = os.path.join(self.output_dir, 'dataset_analysis_report.txt')
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(report)
            
            self.log_step("Análisis de Calidad", "SUCCESS", f"Reporte guardado: {report_file}")
            return True
        
        except Exception as e:
            self.log_step("Análisis de Calidad", "ERROR", str(e))
            return False

    def clean_dataset(self) -> bool:
        """Limpia el dataset si es necesario."""
        try:
            if not self.config['needs_cleaning'] and not self.force_clean:
                self.log_step("Limpieza de Datos", "INFO", "Dataset no requiere limpieza")
                return True
            
            self.log_step("Limpieza de Datos", "INFO", "Iniciando limpieza...")
            
            output_file = os.path.join(self.output_dir, 'Dataset_cleaned.csv')
            
            cleaner = GenericDatasetCleaner(self.input_file, output_file, self.config)
            stats = cleaner.process_file()
            
            report = cleaner.generate_report()
            print("\n" + report)
            
            # Guardar reporte
            report_file = os.path.join(self.output_dir, 'dataset_cleaning_report.txt')
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(report)
            
            self.log_step("Limpieza de Datos", "SUCCESS", 
                         f"Dataset limpio guardado: {output_file}\n"
                         f"Reporte: {report_file}")
            
            return True
        
        except Exception as e:
            self.log_step("Limpieza de Datos", "ERROR", str(e))
            return False

    def validate_dataset(self) -> bool:
        """Valida el dataset limpio."""
        try:
            cleaned_file = os.path.join(self.output_dir, 'Dataset_cleaned.csv')
            
            if not os.path.exists(cleaned_file):
                self.log_step("Validación", "INFO", "No hay dataset limpio para validar")
                return True
            
            self.log_step("Validación", "INFO", "Validando dataset limpio...")
            
            validator = GenericDatasetValidator(self.input_file, cleaned_file, self.config)
            validator.validate_csv_structure()
            validator.validate_character_encoding()
            validator.validate_data_integrity()
            
            report = validator.generate_report()
            print("\n" + report)
            
            # Guardar reporte
            report_file = os.path.join(self.output_dir, 'dataset_validation_report.txt')
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(report)
            
            self.log_step("Validación", "SUCCESS", f"Reporte guardado: {report_file}")
            return True
        
        except Exception as e:
            self.log_step("Validación", "ERROR", str(e))
            return False

    def execute(self) -> bool:
        """Ejecuta el pipeline completo."""
        print("=" * 70)
        print("🚀 PIPELINE GENÉRICO DE LIMPIEZA DE DATASETS")
        print("=" * 70)
        print(f"Archivo: {self.input_file}")
        print(f"Inicio: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # Paso 1: Detectar configuración
        if not self.detect_configuration():
            return False
        
        print()
        
        # Paso 2: Analizar dataset
        if not self.analyze_dataset():
            return False
        
        print()
        
        # Paso 3: Limpiar dataset
        if not self.clean_dataset():
            return False
        
        print()
        
        # Paso 4: Validar dataset
        if not self.validate_dataset():
            return False
        
        print()
        print("=" * 70)
        print("✅ PIPELINE COMPLETADO EXITOSAMENTE")
        print("=" * 70)
        
        return True


def main():
    """Función principal."""
    parser = argparse.ArgumentParser(
        description='Pipeline genérico para limpieza de datasets CSV'
    )
    parser.add_argument('input_file', help='Archivo CSV a procesar')
    parser.add_argument('-o', '--output', help='Directorio de salida')
    parser.add_argument('-f', '--force', action='store_true', 
                       help='Forzar limpieza incluso sin problemas detectados')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.input_file):
        print(f"❌ Error: Archivo no encontrado: {args.input_file}")
        sys.exit(1)
    
    pipeline = GenericDataPipeline(
        args.input_file,
        args.output,
        args.force
    )
    
    success = pipeline.execute()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

