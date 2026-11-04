"""ChristEye response-priority model; illustrative, not fitted to physiology.

Explores a distinction between retention (response_fidelity) and arbitration:
the probability that an immediate option is chosen when a learned contextual
option is also available. This is a *simulation*, not a human diagnosis or an
independent biological 'ghost' network.
"""
from dataclasses import dataclass
import numpy as np
import pandas as pd
from .model import scenarios, clamp

@dataclass(frozen=True)
class PriorityParams:
    baseline: float = -0.4
    damaging_honey: float = 1.15
    damaging_milk: float = 0.90
    protective_honey: float = 0.62
    supportive_milk: float = 0.68
    need_sensitivity: float = 0.55
    sensitivity: float = 4.0


def sigmoid(x):
    x=float(np.clip(x,-40,40))
    return float(1/(1+np.exp(-x)))


def immediate_priority(honey_evil, milk_evil, honey_good, milk_good, need=0.4, params=None):
    """Bounded priority weight. Units are normalized and arbitrary."""
    p=params or PriorityParams()
    v=p.baseline+p.damaging_honey*clamp(honey_evil)+p.damaging_milk*clamp(milk_evil) \
      -p.protective_honey*clamp(honey_good)-p.supportive_milk*clamp(milk_good) \
      +p.need_sensitivity*clamp(need)
    return sigmoid(v)


def action_choice_probabilities(honey_evil, milk_evil, honey_good, milk_good,
                                response_fidelity, need=0.4, params=None,
                                context='neutral'):
    """Returns (immediate, learned) action probabilities.

    Assumption for this demonstration: the learned action is context-appropriate
    for the neutral context; emergency context changes utilities. These labels
    must not be interpreted as 'good/bad' for a real action or molecule.
    """
    if context not in ('neutral','urgent'):
        raise ValueError('context must be neutral or urgent')
    p=params or PriorityParams()
    w=immediate_priority(honey_evil,milk_evil,honey_good,milk_good,need,p)
    k=clamp(response_fidelity)
    if context=='neutral':
        ui_imm, ui_learned, ul_imm, ul_learned = 1.0, 0.22, 0.12, k
    else:
        ui_imm, ui_learned, ul_imm, ul_learned = 1.0, 0.22, 0.74, k*0.75
    scores=np.array([w*ui_imm+(1-w)*ul_imm,
                     w*ui_learned+(1-w)*ul_learned])*p.sensitivity
    # Explicit normalizing exponentials; two alternatives, no hidden controller.
    z=np.exp(scores-scores.max());q=z/z.sum()
    return float(q[0]),float(q[1]),float(w)


def example_trajectories(days=50,dt=0.1,need=0.4):
    """Join existing synthetic six-state scenarios to a response-selection layer."""
    df=scenarios(days=days,dt=dt)
    scores=[action_choice_probabilities(row.honey_evil,row.milk_evil,row.honey_good,
                  row.milk_good,row.response_fidelity,need=need,context='neutral')
            for row in df.itertuples(index=False)]
    df['p_immediate_neutral']=[x[0] for x in scores]
    df['p_learned_neutral']=[x[1] for x in scores]
    df['immediate_priority_weight']=[x[2] for x in scores]
    df['example_need']=need
    df['provenance']='SYNTHETIC_UNCALIBRATED'
    return df
