from pathlib import Path
import numpy as np
import pandas as pd
import pytest
from christeye.model import Params,simulate,scenarios
from christeye.make_demo import generate
from christeye.analysis import validate,summarized_measurements,contrast,predict_matched

def test_normalized_model():
 d=scenarios(days=7); assert len(d)>100
 assert d[['senescent_fraction','honey_evil','milk_evil','honey_good','milk_good','response_fidelity']].to_numpy().min()>=0
 assert d[['senescent_fraction','honey_evil','milk_evil','honey_good','milk_good','response_fidelity']].to_numpy().max()<=1

def test_demo_groups(tmp_path):
 d,w=generate(tmp_path);animal,summary=summarized_measurements(d)
 assert d.synthetic.all(); assert d.study_id.nunique()==4
 assert 'animal_id' in animal and summary.n_units.min()>=1
 assert len(contrast(d))>0
 assert predict_matched(w[w.study_id=='guayasamin_2025'])['status']=='illustrative'

def test_rejects_cross_study_predictions(tmp_path):
 _,w=generate(tmp_path)
 assert predict_matched(w)['status']=='skipped'

def test_bad_schema_rejected():
 with pytest.raises(ValueError):validate(pd.DataFrame({'value':[1]}))
