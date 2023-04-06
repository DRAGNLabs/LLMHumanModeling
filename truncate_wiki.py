import gzip
import xml.etree.ElementTree as ET

# Open the gzipped XML file
with gzip.open('./data/wiki/enwiki-latest-abstract.xml.gz', 'rb') as f:
    # Read the entire file into memory and parse it as an ElementTree object
    tree = ET.parse(f)

# Get the root element of the ElementTree object
root = tree.getroot()

# Truncate the root element to a certain length (e.g. 1000 elements)
root = root[:1000]

# Write the truncated ElementTree object to a new XML file
with open('truncated.xml', 'wb') as f:
    tree.write(f)
