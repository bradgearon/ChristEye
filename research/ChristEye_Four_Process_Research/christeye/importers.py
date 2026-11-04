"""Audit and convert real source files with explicit schema, without fabricated identifiers."""
from pathlib import Path
import json
import pandas as pd

def inspect(path):
    path=Path(path)
    if path.suffix.lower() in ('.xlsx','.xls'):
        xls=pd.ExcelFile(path); out=[]
        for sheet in xls.sheet_names:
            frame=pd.read_excel(path,sheet_name=sheet,nrows=10)
            out.append({'sheet':sheet,'columns':frame.columns.astype(str).tolist(),'first_10_rows':len(frame)})
        return {'file':str(path),'sheets':out}
    elif path.suffix.lower() in ('.csv','.tsv'):
        frame=pd.read_csv(path,nrows=10,sep='\t' if path.suffix.lower()=='.tsv' else ',')
        return {'file':str(path),'columns':frame.columns.astype(str).tolist(),'first_10_rows':len(frame)}
    else:raise ValueError('Use .xlsx/.csv/.tsv')

def wide_to_long(path,mapping_path,out,sheet=None):
    """User config explicitly maps source columns. No guessed animal IDs."""
    config=json.loads(Path(mapping_path).read_text())
    for key in ('study_id','unit_id_col','condition_col','measure_cols'):
        if key not in config:raise ValueError('Mapping requires '+key)
    if config['study_id'] not in {'guayasamin_2025','bukalo_2026','dewa_2025','senescence_2026'}:
        raise ValueError('Unsupported study_id')
    source=Path(path)
    if source.suffix.lower()=='.xlsx':df=pd.read_excel(source,sheet_name=sheet or 0)
    else:df=pd.read_csv(source,sep='\t' if source.suffix.lower()=='.tsv' else ',')
    required=[config['unit_id_col'],config['condition_col']]+list(config['measure_cols'])
    for opt in ('phase_col','cue_col','batch_col'):
      if config.get(opt):required.append(config[opt])
    absent=[x for x in required if x not in df.columns]
    if absent:raise ValueError('Missing source columns: '+repr(absent))
    output=[]
    for _,row in df.iterrows():
      unit=row[config['unit_id_col']]
      if pd.isna(unit):raise ValueError('No biological-unit identity; DO NOT invent an animal ID from row number.')
      for m in config['measure_cols']:
        if pd.isna(row[m]):continue
        entry={'study_id':config['study_id'],'animal_id':str(unit),'condition':str(row[config['condition_col']]),
               'measure':config['measure_cols'][m],'value':row[m],'source':str(path),'synthetic':False}
        for target,opt in [('phase','phase_col'),('cue','cue_col'),('batch','batch_col')]:
          entry[target]=str(row[config[opt]]) if config.get(opt) else ''
        output.append(entry)
    result=pd.DataFrame(output)
    if not len(result):raise ValueError('No finite measurements converted')
    from .analysis import validate
    validate(result)
    Path(out).parent.mkdir(parents=True,exist_ok=True)
    result.to_csv(out,index=False)
    return result
