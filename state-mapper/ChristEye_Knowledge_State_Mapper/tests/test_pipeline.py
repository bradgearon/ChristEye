from pathlib import Path
import tempfile
import unittest
import pandas as pd
from christeye_ksm.synthetic import generate
from christeye_ksm.analysis import run_analysis, run_spatial, audit_transfer

class MapperTests(unittest.TestCase):
    def test_end_to_end_synthetic(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);files=generate(root/'synthetic',n_per_condition=7,cells_per_type=5)
            rep=run_analysis(files['cells'],root/'analysis')
            self.assertEqual(len(rep['models']),2)
            self.assertTrue((root/'analysis'/'knowledge_state_evidence_graph.graphml').exists())
            self.assertEqual(rep['data_origin'],['SYNTHETIC'])
            spatial=run_spatial(files['spatial'],root/'spatial');self.assertGreater(spatial['pairs'],0)
            provenance=audit_transfer(root/'synthetic'/'transfer_candidates_SYNTHETIC.csv',root/'audit')
            self.assertEqual(provenance['status_counts'].get('functional_candidate'),1)
            statuses=pd.read_csv(root/'audit'/'provenance_audit.csv').set_index('donor_id')
            self.assertEqual(statuses.loc['n001','status'],'not_established')
    def test_missing_independent_samples_disables_model(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);f=generate(root/'synthetic',n_per_condition=7,cells_per_type=3)
            df=pd.read_csv(f['cells']);df.preparation_id='MISSING'
            path=root/'bad.csv';df.to_csv(path,index=False)
            rep=run_analysis(path,root/'out')
            self.assertTrue(str(rep['models']).startswith('SKIPPED'))
    def test_spatial_cross_sample_no_edges(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)
            p=root/'cells.csv'
            pd.DataFrame([{'cell_id':'a','sample_id':'S1','cell_type':'neuron','x_um':0,'y_um':0},
                          {'cell_id':'b','sample_id':'S2','cell_type':'astrocyte','x_um':0,'y_um':0}]).to_csv(p,index=False)
            rep=run_spatial(p,root/'out');self.assertEqual(rep['pairs'],0)
if __name__=='__main__':unittest.main()
