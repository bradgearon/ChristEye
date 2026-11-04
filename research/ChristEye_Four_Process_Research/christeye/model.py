"""Illustrative dynamical model: four ChristEye process categories and senescence.

NOT a fitted mechanistic model or biomedical treatment guidance. The equations
are research hypotheses, and default coefficients are arbitrary demonstration
settings. Their values must not be interpreted as biological effect sizes.
"""
from dataclasses import dataclass, replace
import numpy as np
import pandas as pd

@dataclass(frozen=True)
class Params:
    onset_base: float = 0.09
    onset_evil_honey: float = 0.28
    onset_evil_milk: float = 0.20
    protection_good_honey: float = 0.095
    protection_good_milk: float = 0.065
    clearance: float = 0.055
    harmful_secretion_s: float = 0.34
    harmful_secretion_m: float = 0.08
    harmful_signal_decay: float = 0.34
    damaging_state_from_honey: float = 0.20
    damaging_state_from_s: float = 0.06
    damaging_state_recovery: float = 0.24
    good_honey_baseline: float = 0.11
    good_honey_decay: float = 0.18
    good_milk_baseline: float = 0.12
    good_milk_decay: float = 0.18
    supportive_recovery: float = 0.08
    fidelity_recovery: float = 0.12
    fidelity_disruption: float = 0.16

def clamp(x, low=0, high=1):
    return max(low, min(high, x))

def deriv(y, p: Params, control: dict):
    # s: fraction in hypothetical senescent state (not identified clinically)
    # he: damaging extracellular signal load (Honey Evil)
    # me: sustained dysfunctional physiological state (Milk Evil)
    # hg: recovery-supportive extracellular signaling (Honey Good)
    # mg: supportive homeostatic/metabolic capacity (Milk Good)
    # f: retained-response fidelity (functional, not direct engram readout)
    s, he, me, hg, mg, f = map(float,y)
    # Only dimensionless, normalized test variables are used.
    u_block = max(0, float(control.get('signal_containment', 0)))
    u_support = max(0, float(control.get('support', 0)))
    u_clear = max(0, float(control.get('clearance_support', 0)))
    hazard = max(0, p.onset_base + p.onset_evil_honey*he + p.onset_evil_milk*me
                     - p.protection_good_honey*hg - p.protection_good_milk*mg)
    ds = (1-s)*hazard - (p.clearance + u_clear)*s
    dhe = p.harmful_secretion_s*s + p.harmful_secretion_m*me - (p.harmful_signal_decay + u_block)*he
    dme = p.damaging_state_from_honey*he + p.damaging_state_from_s*s - (p.damaging_state_recovery + p.supportive_recovery*mg)*me
    dhg = p.good_honey_baseline + u_support - p.good_honey_decay*hg
    dmg = p.good_milk_baseline + u_support*0.5 - p.good_milk_decay*mg
    df = p.fidelity_recovery*(1-f)*(hg+mg)/2 - p.fidelity_disruption*f*(he+me)/2
    return np.array([ds, dhe, dme, dhg, dmg, df],dtype=float)

def simulate(days=50., dt=0.1, intervention_at=None, control=None, params=None,
             initial=(0.04,0.12,0.14,0.35,0.4,0.87)):
    p=params or Params(); control=control or {}
    if not (0<dt<=1 and days>0): raise ValueError('Require 0<dt<=1 and days>0')
    if len(initial)!=6:raise ValueError('Six model states required')
    y=np.array(initial,dtype=float)
    if np.any(y<0) or np.any(y>1):raise ValueError('Normalized initial values must be 0..1')
    rows=[]
    for t in np.arange(0,days+dt/2,dt):
        actual_control=control if intervention_at is not None and t>=intervention_at else {}
        rows.append(dict(day=round(float(t),5),senescent_fraction=y[0],honey_evil=y[1],milk_evil=y[2],honey_good=y[3],milk_good=y[4],response_fidelity=y[5]))
        y=np.clip(y+dt*deriv(y,p,actual_control),0,1)
    return pd.DataFrame(rows)

def scenarios(days=50,dt=0.1):
    p=Params(); scen={
      'no_control':(None,{}),
      'early_signal_containment':(5,{'signal_containment':0.24}),
      'late_signal_containment':(25,{'signal_containment':0.24}),
      'early_support':(5,{'support':0.16}),
      'early_combined':(5,{'signal_containment':0.24,'support':0.16}),
      'early_clearance_support':(5,{'clearance_support':0.025})
    }
    out=[]
    for name,(start,c) in scen.items():
      d=simulate(days,dt,start,c,p); d['scenario']=name;out.append(d)
    return pd.concat(out,ignore_index=True)
