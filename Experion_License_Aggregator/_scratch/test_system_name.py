#!/usr/bin/env python3
"""Quick test to verify system_name extraction"""

from v2.pipeline.extractors.xml_extractor import XmlExtractor
from pathlib import Path

extractor = XmlExtractor()
xml_path = Path('data/raw/Carson/ESVT0 M0614 60806/M0614_Experion_PKS_R52X_x_60806_42.xml')

result = extractor.extract_from_file(xml_path)

if result.success:
    lic = result.data
    print(f"✓ Extraction successful")
    print(f"  MSID: {lic.msid}")
    print(f"  Cluster: {lic.cluster}")
    print(f"  System Name: {lic.system_name}")
    print(f"  System Number: {lic.system_number}")
else:
    print("✗ Extraction failed")
    print(f"  Errors: {result.errors}")
