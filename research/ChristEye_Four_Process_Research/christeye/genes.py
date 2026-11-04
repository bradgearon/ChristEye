"""Within-dataset per-biological-replicate RNA expression comparisons.
Requires cell-level counts to have already been quality controlled and normalized.
"""
import numpy as np
import pandas as pd
from scipy.stats import mannwhitneyu

def gene_changes(df, study_col='study_id', unit_col='biological_unit', condition_col='condition', cell_col='cell_type', gene_col='gene', value_col='normalized_expression'):
    required={study_col,unit_col,condition_col,cell_col,gene_col,value_col}
    if not required.issubset(df.columns):raise ValueError('Missing '+str(required-set(df.columns)))
    # Average cells WITHIN animal/biological replicate first; never treat cells as independent animals.
    rep=df.groupby([study_col,unit_col,condition_col,cell_col,gene_col],as_index=False)[value_col].mean()
    rows=[]
    for (study,ctype,gene),d in rep.groupby([study_col,cell_col,gene_col]):
      cond=sorted(d[condition_col].unique())
      if len(cond)!=2:continue
      a=d[d[condition_col]==cond[0]][value_col].to_numpy(float)
      b=d[d[condition_col]==cond[1]][value_col].to_numpy(float)
      if len(a)<3 or len(b)<3:continue
      if np.min(np.r_[a,b])<0:raise ValueError('Expression must be nonnegative before log fold change')
      p=mannwhitneyu(a,b,alternative='two-sided').pvalue
      # Delta on log2(1+x) scale: not a raw count fold change
      log_diff=float(np.mean(np.log2(1+b))-np.mean(np.log2(1+a)))
      rows.append(dict(study_id=study,cell_type=ctype,gene=gene,group_a=cond[0],group_b=cond[1],n_a=len(a),n_b=len(b),delta_mean_log2_1p=log_diff,p=p))
    result=pd.DataFrame(rows)
    if len(result):
      result['q_bh']=np.nan
      for (_, _),g in result.groupby(['study_id','cell_type']):
        ix=g.index;p=result.loc[ix,'p'].to_numpy();order=np.argsort(p);qrank=np.minimum.accumulate((p[order]*len(p)/np.arange(1,len(p)+1))[::-1])[::-1]
        q=np.empty(len(p));q[order]=np.clip(qrank,0,1);result.loc[ix,'q_bh']=q
    return result
