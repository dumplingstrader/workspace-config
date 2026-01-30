"""
Extractors Package

Data extraction modules for parsing source files (XML, CSV) into typed data models.
"""

from v2.pipeline.extractors.base_extractor import BaseExtractor, ExtractionResult
from v2.pipeline.extractors.xml_extractor import XmlExtractor
from v2.pipeline.extractors.csv_extractor import CsvExtractor


__all__ = [
    'BaseExtractor',
    'ExtractionResult',
    'XmlExtractor',
    'CsvExtractor',
]
