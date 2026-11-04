"""External real-data RNA analysis; requires harmonized biology-unit IDs and normalized expression."""
import argparse
import pandas as pd
from christeye.genes import gene_changes
p=argparse.ArgumentParser();p.add_argument('--input',required=True);p.add_argument('--output',default='outputs/gene_changes.csv');a=p.parse_args()
d=gene_changes(pd.read_csv(a.input));d.to_csv(a.output,index=False)
print(f'Within-dataset contrasts: {len(d)}. Requires external validation; no between-study fold-change pooling.')
