"""Utilities for reviewing real source spreadsheets before any analysis.
Examples:
 python inspect_or_import.py inspect data.xlsx
 python inspect_or_import.py convert data.xlsx schemas/my_mapping.json outputs/real_long.csv --sheet Sheet1
"""
import argparse,json
from christeye.importers import inspect,wide_to_long
p=argparse.ArgumentParser();s=p.add_subparsers(dest='command',required=True)
a=s.add_parser('inspect');a.add_argument('file')
b=s.add_parser('convert');b.add_argument('file');b.add_argument('mapping');b.add_argument('output');b.add_argument('--sheet')
c=p.parse_args()
if c.command=='inspect':print(json.dumps(inspect(c.file),indent=2))
else:
 r=wide_to_long(c.file,c.mapping,c.output,c.sheet)
 print('Converted',len(r),'rows. Verify independent units and condition labels in the output.')
