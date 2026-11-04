"""Generate synthetic test fixtures. NOT observations from published papers."""
from pathlib import Path
import numpy as np
import pandas as pd

def generate(out):
    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    rng=np.random.default_rng(20261104)
    specifications=[
     ('guayasamin_2025','control','ELS', [('Cx43_normalized',1.,-.18),('astro_Ca_frequency',1.,-.28),('neutral_cue_freezing_pct',18.,13.)]),
     ('bukalo_2026','control','astrocyte_perturbed',[('astro_Ca_AUC',1.,-.21),('memory_retrieval_pct',70.,-14.),('extinction_discrimination',.62,-.17)]),
     ('dewa_2025','NoFR','FR',[('astrocyte_Fos_score',.4,.33),('IGFBP2_score',.4,.22),('retention_pct',48.,16.)]),
     ('senescence_2026','control','senescence_like',[('CCL2_proxy',.2,.35),('MIF_proxy',.2,.27),('p21_proxy',.2,.32)])
    ]
    rows=[]
    for study,a,b,features in specifications:
      for cond in (a,b):
        for i in range(18):
          unit=f'{study}_{cond}_{i:03d}'
          for measure,base,delta in features:
            scale=max(.06,abs(base)*.1,abs(delta)*.5)
            rows.append({'study_id':study,'animal_id':unit,'condition':cond,'phase':'demo',
                         'measure':measure,'value':float(base+(delta if cond==b else 0)+rng.normal(0,scale)),
                         'synthetic':True,'source':'SYNTHETIC / NOT PUBLISHED DATA'})
    df=pd.DataFrame(rows);df.to_csv(out/'synthetic_long.csv',index=False)
    # deliberately only one row per animal, with no cross-study pooling
    wide=df.pivot_table(index=['study_id','animal_id','condition'],columns='measure',values='value').reset_index()
    wide['synthetic']=True
    # synthetic binary learning outcome, weakly related to prepared differences; no causal claim
    for study in wide.study_id.unique():
      mask=wide.study_id==study
      col={'guayasamin_2025':'Cx43_normalized','bukalo_2026':'astro_Ca_AUC','dewa_2025':'IGFBP2_score','senescence_2026':'CCL2_proxy'}[study]
      x=wide.loc[mask,col].fillna(0).to_numpy()
      cutoff=float(np.median(x))
      wide.loc[mask,'correct']=(x+rng.normal(0,max(.06,x.std()),size=len(x))>cutoff).astype(int)
    wide.to_csv(out/'synthetic_matched.csv',index=False)
    return df,wide
