from pathlib import Path
import xml.etree.ElementTree as ET

files = list(Path("data/raw/Carson").glob("*.xml"))[:5]
for f in files:
    tree = ET.parse(f)
    root = tree.getroot()
    cluster = root.find(".//Cluster")
    msid = root.find(".//MSID")
    print(f"{f.name}:")
    print(f"  Cluster: {cluster.text if cluster is not None else 'Not found'}")
    print(f"  MSID: {msid.text if msid is not None else 'Not found'}")
    print()
