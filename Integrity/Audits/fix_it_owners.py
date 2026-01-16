import re

# Read the file
with open('c:/Users/GF99/Documentation/Integrity/Audits/regenerate_checklist.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace all instances of ', 'IT', ' with ', 'IT/OT', '
content = content.replace("', 'IT', '", "', 'IT/OT', '")

# Write back
with open('c:/Users/GF99/Documentation/Integrity/Audits/regenerate_checklist.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✓ Replaced all IT owner instances with IT/OT")
