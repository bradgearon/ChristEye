import math
from christeye.arbitration import action_choice_probabilities, immediate_priority, example_trajectories

def test_probas_sum_to_one_and_bounded():
    a,b,w=action_choice_probabilities(0.3,0.3,0.5,0.5,0.8)
    assert 0<=a<=1 and 0<=b<=1 and 0<=w<=1
    assert math.isclose(a+b,1,rel_tol=1e-10)

def test_directional_example_not_empirical_fact():
    low=immediate_priority(0.0,0.0,0.8,0.8)
    high=immediate_priority(0.8,0.8,0.0,0.0)
    assert high>low

def test_demo_has_provenance():
    d=example_trajectories(days=2,dt=0.5)
    assert d.provenance.eq('SYNTHETIC_UNCALIBRATED').all()
    assert d.p_immediate_neutral.between(0,1).all()
