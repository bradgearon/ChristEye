from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def plot_trajectories(df,path):
    fig,ax=plt.subplots(figsize=(9.5,5.2))
    for name,g in df.groupby('scenario'):
      ax.plot(g.day,g.senescent_fraction,label=name,linewidth=2)
    ax.set(title='ILLUSTRATIVE MODEL • Senescence-like state fraction',xlabel='Simulated time (arbitrary days)',ylabel='Modeled fraction (dimensionless)',ylim=(0,1))
    ax.legend(fontsize=8,ncol=2,loc='upper left');ax.grid(alpha=.2);fig.tight_layout();fig.savefig(path,dpi=170);plt.close(fig)

def plot_four_states(df,path):
    fig,ax=plt.subplots(figsize=(9.5,5.2))
    g=df[df.scenario=='no_control']
    for col in ('honey_evil','milk_evil','honey_good','milk_good','response_fidelity'):
      ax.plot(g.day,g[col],label=col,linewidth=2)
    ax.set(title='ILLUSTRATIVE MODEL • Process-level trajectories',xlabel='Simulated time (arbitrary days)',ylabel='Normalized state (0–1)')
    ax.legend(fontsize=8,ncol=2);ax.grid(alpha=.2);fig.tight_layout();fig.savefig(path,dpi=170);plt.close(fig)
