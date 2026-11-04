"""Official GEO URLs. Downloads only annotation files unless --include-matrix is specified."""
import argparse,hashlib,json,urllib.request
from pathlib import Path
ROOT='https://ftp.ncbi.nlm.nih.gov/geo/series/GSE246nnn/GSE246147/suppl/'
FILES={'barcodes':'GSE246147_barcodes.tsv.gz',
       'features':'GSE246147_features.tsv.gz',
       'celltypes':'GSE246147_cell_type_data.csv.gz',
       'umap':'GSE246147_umap_data.csv.gz',
       'matrix':'GSE246147_matrix.mtx.gz'}
def hashfile(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for x in iter(lambda:f.read(1024*1024),b''):h.update(x)
    return h.hexdigest()
def main():
    p=argparse.ArgumentParser(description='Download files from the documented GEO GSE246147 supplement (network required)')
    p.add_argument('--out',default='data/raw/GSE246147');p.add_argument('--include-matrix',action='store_true')
    a=p.parse_args();out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
    names=list(FILES) if a.include_matrix else [x for x in FILES if x!='matrix']
    manifest={'accession':'GSE246147','source':ROOT,'files':{},'data_origin':'GEO_REAL'}
    for key in names:
        name=FILES[key]; dest=out/name
        if not dest.exists():
            print('Downloading',name)
            urllib.request.urlretrieve(ROOT+name,dest)
        manifest['files'][name]={'sha256':hashfile(dest),'size':dest.stat().st_size}
    (out/'download_manifest.json').write_text(json.dumps(manifest,indent=2))
    print('Saved',out/'download_manifest.json')
if __name__=='__main__':main()
