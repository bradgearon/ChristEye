"""Evidence network: direct findings not confused with cross-study synthesis."""
from pathlib import Path
import networkx as nx
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def make_evidence_graph(csv_path, out_dir):
    d=pd.read_csv(csv_path)
    required={'source','target','relationship','evidence_level','study_id'}
    if not required.issubset(d):raise ValueError('Missing evidence fields')
    g=nx.MultiDiGraph()
    for r in d.itertuples():
      g.add_edge(r.source,r.target,relationship=r.relationship,evidence_level=r.evidence_level,study_id=r.study_id)
    out=Path(out_dir);out.mkdir(parents=True,exist_ok=True)
    nx.write_graphml(g,out/'evidence_graph.graphml')
    d.to_csv(out/'evidence_edges.csv',index=False)
    nodes=list(g.nodes()); pos=nx.spring_layout(g,seed=8,k=1.45)
    fig,ax=plt.subplots(figsize=(13,9));nx.draw_networkx_nodes(g,pos,node_size=1800,alpha=.75,ax=ax)
    direct=[(a,b) for a,b,k,t in g.edges(keys=True,data=True) if t['evidence_level']=='direct_in_study']
    synth=[(a,b) for a,b,k,t in g.edges(keys=True,data=True) if t['evidence_level']!='direct_in_study']
    nx.draw_networkx_edges(g,pos,edgelist=direct,arrows=True,width=2,alpha=.8,ax=ax)
    nx.draw_networkx_edges(g,pos,edgelist=synth,arrows=True,style='dashed',width=1,alpha=.65,ax=ax)
    nx.draw_networkx_labels(g,pos,font_size=8,ax=ax);ax.axis('off');ax.set_title('Evidence graph — solid: direct | dashed: cross-study hypothesis');fig.tight_layout();fig.savefig(out/'evidence_graph.png',dpi=170);plt.close(fig)
    return out
