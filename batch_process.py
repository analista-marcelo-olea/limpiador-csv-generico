"""
Script para procesar múltiples datasets en lote
"""

import os
import sys
import argparse
from pathlib import Path
from generic_pipeline import GenericDataPipeline


class BatchProcessor:
    """
    Procesa múltiples datasets automáticamente.
    """

    def __init__(self, input_pattern: str, output_dir: str = None, force_clean: bool = False):
        """
        Inicializa el procesador en lote.
        
        Args:
            input_pattern: Patrón de archivos (ej: "*.csv", "data/*.csv")
            output_dir: Directorio de salida
            force_clean: Forzar limpieza
        """
        self.input_pattern = input_pattern
        self.output_dir = output_dir
        self.force_clean = force_clean
        self.results = []

    def find_files(self) -> list:
        """Encuentra archivos que coinciden con el patrón."""
        files = list(Path('.').glob(self.input_pattern))
        return sorted([str(f) for f in files])

    def process_all(self) -> bool:
        """Procesa todos los archivos encontrados."""
        files = self.find_files()
        
        if not files:
            print(f"❌ No se encontraron archivos con patrón: {self.input_pattern}")
            return False
        
        print("=" * 70)
        print(f"🔄 PROCESAMIENTO EN LOTE")
        print("=" * 70)
        print(f"Patrón: {self.input_pattern}")
        print(f"Archivos encontrados: {len(files)}")
        print()
        
        for i, filepath in enumerate(files, 1):
            print(f"\n[{i}/{len(files)}] Procesando: {filepath}")
            print("-" * 70)
            
            try:
                # Determinar directorio de salida
                output_dir = self.output_dir or os.path.dirname(filepath) or '.'
                
                # Crear directorio si no existe
                os.makedirs(output_dir, exist_ok=True)
                
                # Ejecutar pipeline
                pipeline = GenericDataPipeline(filepath, output_dir, self.force_clean)
                success = pipeline.execute()
                
                self.results.append({
                    'file': filepath,
                    'status': 'SUCCESS' if success else 'FAILED'
                })
                
            except Exception as e:
                print(f"❌ Error procesando {filepath}: {e}")
                self.results.append({
                    'file': filepath,
                    'status': 'ERROR',
                    'error': str(e)
                })
        
        # Mostrar resumen
        self.print_summary()
        return True

    def print_summary(self):
        """Imprime resumen de resultados."""
        print("\n" + "=" * 70)
        print("📊 RESUMEN DE PROCESAMIENTO EN LOTE")
        print("=" * 70)
        
        successful = sum(1 for r in self.results if r['status'] == 'SUCCESS')
        failed = sum(1 for r in self.results if r['status'] in ['FAILED', 'ERROR'])
        
        print(f"\nTotal de archivos: {len(self.results)}")
        print(f"✅ Exitosos: {successful}")
        print(f"❌ Fallidos: {failed}")
        print()
        
        if failed > 0:
            print("Archivos con problemas:")
            for result in self.results:
                if result['status'] != 'SUCCESS':
                    print(f"  - {result['file']}: {result['status']}")
                    if 'error' in result:
                        print(f"    Error: {result['error']}")
        
        print()
        print("=" * 70)


def main():
    """Función principal."""
    parser = argparse.ArgumentParser(
        description='Procesar múltiples datasets en lote'
    )
    parser.add_argument('pattern', help='Patrón de archivos (ej: "*.csv", "data/*.csv")')
    parser.add_argument('-o', '--output', help='Directorio de salida')
    parser.add_argument('-f', '--force', action='store_true',
                       help='Forzar limpieza para todos los archivos')
    
    args = parser.parse_args()
    
    processor = BatchProcessor(args.pattern, args.output, args.force)
    success = processor.process_all()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

