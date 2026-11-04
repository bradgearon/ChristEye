import argparse,json
from pathlib import Path
import pandas as pd
from .analysis import summarized_measurements,contrast,predict_matched,validate
from .make_demo import generate
from .model import scenarios
from .arbitration import example_trajectories
from .viz import plot_trajectories,plot_four_states

def save_analysis(df,out):
    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    animal,summary=summarized_measurements(df)
    animal.to_csv(out/'animal_level.csv',index=False)
    summary.to_csv(out/'group_summary.csv',index=False)
    result=contrast(df)
    result.to_csv(out/'within_study_contrasts.csv',index=False)
    return len(animal),len(result)

def main():
    ap=argparse.ArgumentParser(description='ChristEye research evidence mapper (not a treatment tool)')
    sub=ap.add_subparsers(dest='cmd',required=True)
    p=sub.add_parser('demo');p.add_argument('--out',default='outputs/demo')
    p=sub.add_parser('analyze');p.add_argument('--input',required=True);p.add_argument('--out',default='outputs/analysis')
    p=sub.add_parser('predict');p.add_argument('--input',required=True);p.add_argument('--study',required=True)
    p=sub.add_parser('simulate');p.add_argument('--out',default='outputs/simulation')
    p=sub.add_parser('arbitrate');p.add_argument('--out',default='outputs/arbitration');p.add_argument('--need',type=float,default=0.4)
    args=ap.parse_args()
    if args.cmd=='demo':
      out=Path(args.out);df,wide=generate(out);save_analysis(df,out)
      pred={s:predict_matched(g.reset_index(drop=True)) for s,g in wide.groupby('study_id')}
      (out/'predictive_illustration.json').write_text(json.dumps(pred,indent=2))
      sim=scenarios();sim.to_csv(out/'simulation_trajectories.csv',index=False)
      plot_trajectories(sim,out/'senescence_scenario_comparison.png')
      plot_four_states(sim,out/'four_process_trajectories.png')
      sim.groupby('scenario').tail(1)[['scenario','senescent_fraction','response_fidelity']].to_csv(out/'simulation_final_states.csv',index=False)
      (out/'PROVENANCE.txt').write_text('All generated observations are SYNTHETIC. The model coefficients are uncalibrated illustrative values. No biological discovery or intervention efficacy is demonstrated.\n')
      print(f'Demo complete at {out}. SYNTHETIC DATA ONLY.')
    elif args.cmd=='analyze':
      df=validate(pd.read_csv(args.input));n,m=save_analysis(df,args.out)
      print(f'Processed {n} independent sample × measure rows; {m} within-study comparisons. Verify biological-unit labels and assay scale.')
    elif args.cmd=='predict':
      df=pd.read_csv(args.input);g=df[df.study_id==args.study]
      print(json.dumps(predict_matched(g),indent=2))
    elif args.cmd=='arbitrate':
      if not (0<=args.need<=1):raise ValueError('need must be in 0..1')
      out=Path(args.out);out.mkdir(parents=True,exist_ok=True)
      sim=example_trajectories(need=args.need)
      sim.to_csv(out/'response_priority_trajectories.csv',index=False)
      sim.groupby('scenario').tail(1)[['scenario','p_immediate_neutral','p_learned_neutral','immediate_priority_weight']].to_csv(out/'scenario_response_summary.csv',index=False)
      (out/'PROVENANCE.txt').write_text('SYNTHETIC EXAMPLE: arbitrary coefficients. No patient or animal responses were measured. This does not validate a ghost network.\n')
      print(f'Arbitration demo at {out}; SYNTHETIC, not a physiological finding.')
    elif args.cmd=='simulate':
      out=Path(args.out);out.mkdir(parents=True,exist_ok=True)
      sim=scenarios();sim.to_csv(out/'simulation_trajectories.csv',index=False)
      plot_trajectories(sim,out/'senescence_scenario_comparison.png')
      plot_four_states(sim,out/'four_process_trajectories.png')
      print(f'Illustrative simulation saved in {out}; no fitted biological parameters.')

if __name__=='__main__':main()
