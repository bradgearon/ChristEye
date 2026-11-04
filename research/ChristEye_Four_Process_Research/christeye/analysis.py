"""Conservative research-level analysis; keeps source studies separate."""
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import ttest_ind
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import balanced_accuracy_score, roc_auc_score
from sklearn.model_selection import GroupShuffleSplit
from sklearn.pipeline import make_pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler

REQUIRED=('study_id','animal_id','condition','measure','value')
VALID_STUDIES={'guayasamin_2025','bukalo_2026','dewa_2025','senescence_2026'}

def validate(df):
    absent=[c for c in REQUIRED if c not in df.columns]
    if absent:raise ValueError('Missing required columns: '+', '.join(absent))
    if df['animal_id'].isna().any():raise ValueError('Missing biological unit identity')
    if not set(df.study_id.astype(str)).issubset(VALID_STUDIES):
        raise ValueError('Unknown study_id; update schema explicitly')
    df=df.copy();df['value']=pd.to_numeric(df.value,errors='raise')
    if not np.isfinite(df['value']).all():raise ValueError('Non-finite observations')
    return df

def summarized_measurements(df):
    df=validate(df)
    # aggregate replicates to biological unit, avoiding pseudoreplication
    cols=['study_id','condition','measure','animal_id']
    for optional in ('phase','cue'):
      if optional in df.columns:cols.insert(-1,optional)
    animal=df.groupby(cols,dropna=False,as_index=False)['value'].mean()
    groupcols=[c for c in cols if c!='animal_id']
    summary=animal.groupby(groupcols,dropna=False).agg(n_units=('animal_id','nunique'),mean=('value','mean'),sd=('value','std')).reset_index()
    return animal,summary

def contrast(df):
    animal,_=summarized_measurements(df)
    groupcols=['study_id','measure']+[x for x in ('phase','cue') if x in animal.columns]
    results=[]
    for key,g in animal.groupby(groupcols,dropna=False):
        conditions=sorted(g.condition.unique().tolist())
        if len(conditions)!=2:continue
        a=g.loc[g.condition==conditions[0],'value'].values
        b=g.loc[g.condition==conditions[1],'value'].values
        if len(a)<3 or len(b)<3:continue
        t,p=ttest_ind(a,b,equal_var=False)
        pooled=np.sqrt(((len(a)-1)*np.var(a,ddof=1)+(len(b)-1)*np.var(b,ddof=1))/(len(a)+len(b)-2))
        d=(np.mean(b)-np.mean(a))/pooled if pooled>0 else np.nan
        hedges=d*(1-3/(4*(len(a)+len(b))-9))
        row=dict(zip(groupcols,key if isinstance(key,tuple) else (key,)))
        row.update(group_a=conditions[0],group_b=conditions[1],n_a=len(a),n_b=len(b),mean_a=np.mean(a),mean_b=np.mean(b),difference_b_minus_a=np.mean(b)-np.mean(a),p=float(p) if np.isfinite(p) else np.nan,hedges_g=float(hedges) if np.isfinite(hedges) else np.nan)
        results.append(row)
    out=pd.DataFrame(results)
    if not out.empty:
        out['q_bh']=np.nan
        # Benjamini-Hochberg within each source study only
        for sid,g in out.groupby('study_id'):
          ix=g.index; pvals=out.loc[ix,'p'].values.astype(float); valid=np.isfinite(pvals)
          if valid.any():
            pvalid=pvals[valid]; order=np.argsort(pvalid); rank=np.arange(1,len(order)+1)
            qsorted=np.minimum.accumulate((pvalid[order]*len(order)/rank)[::-1])[::-1]
            q=np.empty(len(order));q[order]=np.minimum(qsorted,1)
            arr=np.full(len(pvals),np.nan);arr[valid]=q
            out.loc[ix,'q_bh']=arr
    return out

def predict_matched(df, outcome='correct', groups='animal_id', min_units=12):
    """Use ONLY matched task/animal-level data; group split avoids cell/slice leakage.
    Accepts wide flat table with one row per observation; no cross-study joins.
    Returns a conservative status if no suitable matched data exist.
    """
    needed={'study_id',groups,outcome}
    if not needed.issubset(df):return {'status':'skipped','reason':'Missing required matched columns.'}
    if df.study_id.nunique()!=1:return {'status':'skipped','reason':'Do not pool unmatched studies.'}
    if df[groups].nunique()<min_units:return {'status':'skipped','reason':'Insufficient independent biological units.'}
    y=df[outcome]
    if not set(y.dropna().unique()).issubset({0,1}) or y.nunique()!=2:return {'status':'skipped','reason':'Need binary outcome with both classes.'}
    forbidden={groups,outcome,'study_id','condition','batch','phase','cue','subject_id','trial_id'}
    features=[c for c in df.select_dtypes(include='number').columns if c not in forbidden]
    features=[c for c in features if df[c].notna().sum()>=3]
    if not features:return {'status':'skipped','reason':'No numeric predictors.'}
    splitter=GroupShuffleSplit(n_splits=1,test_size=.3,random_state=41)
    tr,te=next(splitter.split(df[features],y,groups=df[groups]))
    if y.iloc[tr].nunique()!=2 or y.iloc[te].nunique()!=2:return {'status':'skipped','reason':'Split lacks both outcomes.'}
    estimator=make_pipeline(SimpleImputer(strategy='median'),StandardScaler(),LogisticRegression(max_iter=1000))
    estimator.fit(df.iloc[tr][features],y.iloc[tr])
    score=estimator.predict_proba(df.iloc[te][features])[:,1]
    return {'status':'illustrative' if 'synthetic' in df.columns and bool(df.synthetic.any()) else 'observational',
            'n_train_animals':int(df.iloc[tr][groups].nunique()),'n_test_animals':int(df.iloc[te][groups].nunique()),
            'roc_auc':round(float(roc_auc_score(y.iloc[te],score)),3),
            'balanced_accuracy':round(float(balanced_accuracy_score(y.iloc[te],score>=.5)),3),'features':features}
