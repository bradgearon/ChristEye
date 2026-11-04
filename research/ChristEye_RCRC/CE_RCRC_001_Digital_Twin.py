#!/usr/bin/env python3
"""CE-RCRC-001: safe, OFFLINE, synthetic containment-controller comparison.

NO hardware I/O. NO radiation control. NO radioactive sources. No clinical data.
Uses only the Python standard library.
Run: python CE_RCRC_001_Digital_Twin.py --runs 24 --out trial_outputs
"""
from __future__ import annotations
import argparse, csv, math, random, statistics
from pathlib import Path

DT_MIN=0.25
V_M3=0.10
Q_ON_M3_H=0.50     # illustrative measured CADR; replace with real measurements
ETA=1.00           # effective CADR already includes filter efficiency
K_LOSS_H=0.20
DURATION_MIN=75
OBS_SIGMA=0.7
TARGET=10.0


def source_profile(t, variant):
    # Synthetic airborne particle INPUT, expressed in ug/m3/min after volume division.
    # Not a physical aerosol release instruction.
    starts=(12 + variant % 5, 35 + (variant*3)%8, 55+(variant*7)%6)
    heights=(4.5, 2.0 + .4*(variant%4), 3.0)
    return sum(h if st <= t < st+5 else 0.0 for st,h in zip(starts,heights))


def controller(strategy, c, source_est, t, prev, prev_reading):
    if strategy == 'fixed_schedule':
        return int((int(t)//12) % 2 == 1)
    if strategy == 'hysteresis':
        return int(c >= 13.5 or (prev and c >= 8.0))
    if strategy == 'christeye_candidate':
        # One-step forecast, with explicit effort/air-quality tradeoff. Illustrative.
        # Predicted change uses only the known model and an estimated source input.
        kl=K_LOSS_H/60
        with_fan=Q_ON_M3_H/V_M3/60
        pred_off=max(0, c + DT_MIN*(source_est-kl*c))
        pred_on=max(0, c + DT_MIN*(source_est-(kl+with_fan)*c))
        loss_off=max(0, pred_off-TARGET)**2
        loss_on=max(0, pred_on-TARGET)**2 + 0.32
        return int(loss_on < loss_off or (prev and c > 12.0))
    raise ValueError(strategy)


def run_scenario(seed, strategy):
    rng=random.Random(5000+seed)
    c=6.0+(seed%4)*0.3
    prev_u=0
    prev_y=c
    source_est=0.
    records=[]
    source_integral=removed_integral=loss_integral=0.
    total_energy=total_exceedance=0.
    for step in range(int(DURATION_MIN/DT_MIN)):
        t=step*DT_MIN
        measured=max(0.0,c+rng.gauss(0,OBS_SIGMA))
        # Inferring a source from serial differences is deliberately noisy.
        if step:
            rate=(measured-prev_y)/DT_MIN
            source_est=max(0.,min(8.,0.20*rate+0.80*source_est))
        u=controller(strategy,measured,source_est,t,prev_u,prev_y)
        source=source_profile(t,seed)
        k_filter=ETA*(Q_ON_M3_H/V_M3)/60*u
        k_loss=K_LOSS_H/60
        removal=k_filter*c
        loss=k_loss*c
        new_c=max(0.,c+DT_MIN*(source-removal-loss))
        source_integral+=source*DT_MIN
        removed_integral+=removal*DT_MIN
        loss_integral+=loss*DT_MIN
        total_energy+=u*DT_MIN
        total_exceedance+=max(0,c-TARGET)*DT_MIN
        records.append((round(t,2), round(source,4), round(c,4),round(measured,4),u,round(source_est,4)))
        c,prev_u,prev_y=new_c,u,measured
    # Discrete balance uses explicit Euler and tracks each exact discrete increment.
    residual=c-records[0][2]-source_integral+removed_integral+loss_integral
    # Starting c is not exactly rounded; calculate using raw initial value.
    init_c=6.0+(seed%4)*0.3
    residual=c-init_c-source_integral+removed_integral+loss_integral
    return {'seed':seed, 'strategy':strategy,'exceedance_ug_min_m3':total_exceedance,
            'fan_on_minutes':total_energy,'final_pm_ug_m3':c,
            'conservation_error_ug_m3':residual},records


def poisson_alarm_cutoff(mean, alpha=0.001):
    # Small tail probabilities from a stable CDF recursion, mean in COUNTS per bin.
    term=math.exp(-mean)
    cdf=term
    n=0
    while 1-cdf>alpha and n<100000:
        n+=1
        term*=mean/n
        cdf+=term
    return n+1 # 'alarm at count >= n+1' because P(X >= n+1)=1-CDF(n)


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--runs',type=int,default=24)
    ap.add_argument('--out',default='trial_outputs')
    a=ap.parse_args()
    assert 1 <= a.runs <= 1000
    out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
    strategies=['fixed_schedule','hysteresis','christeye_candidate']
    all_summary=[]
    for s in strategies:
        for seed in range(a.runs):
            summary,records=run_scenario(seed,s)
            all_summary.append(summary)
            if seed==0:
                with (out/f'timeseries_{s}.csv').open('w',newline='') as f:
                    w=csv.writer(f)
                    w.writerow(['time_min','synthetic_input_ug_m3_min','true_pm_ug_m3',
                                'sensor_pm_ug_m3','fan_binary','source_est_ug_m3_min'])
                    w.writerows(records)
    with (out/'summary_runs.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=all_summary[0].keys())
        w.writeheader();w.writerows(all_summary)
    print('CE-RCRC-001 SYNTHETIC ONLY. Not evidence of physical radiation protection.')
    for s in strategies:
        subset=[r for r in all_summary if r['strategy']==s]
        err=max(abs(r['conservation_error_ug_m3']) for r in subset)
        print(f'{s:22} | mean exceedance={statistics.mean(r["exceedance_ug_min_m3"] for r in subset):.1f} | mean fan min={statistics.mean(r["fan_on_minutes"] for r in subset):.1f} | worst mass-balance residual={err:.2e}')
    print('Example synthetic 20 counts/min background, 1-minute window, one-sided alpha 0.001 alarm at count >=',poisson_alarm_cutoff(20.0))
    print('Example normalized biological R = (0.4+0.3)/(0.5+B): B=0 ->',round(.7/.5,3),'; B=0.4 ->',round(.7/.9,3))
    print('Saved CSV data under',out)

if __name__=='__main__':main()
