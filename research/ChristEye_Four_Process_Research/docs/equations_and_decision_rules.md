# ChristEye: Four-process systems model (proposed, not validated)

## Four functional categories — not moral or molecular identities

**Honey of Evil / HE**: concentration-weighted *external* secreted factors whose experimentally verified effects maintain damage, e.g., selected SASP, DAMPs, inflammatory ligands in a defined receiving tissue. **Not** a named molecule or a supernatural entity.

**Milk of Evil / ME**: persistent *internal / functional* states that reduce viable or appropriate function, e.g., mitochondrial dysfunction, chronic nonresolving inflammatory programs, or rigorously assessed senescence state. **Not** synonymous with normal acute inflammation.

**Honey of Good / HG**: *external* context-specific resolution / repair-oriented signaling and recognition. Too much of an otherwise beneficial factor may be harmful.

**Milk of Good / MG**: *internal or environmental support* (physiological ion regulation, metabolism, functional recovery, viable tissue). Not a recommendation to administer nutrient or ion loads.

These categories operationalize the user's ChristEye framework; they are **not** a scientific consensus taxonomy. Classification requires a receiving-cell type, time window, baseline, outcome, and empirical evidence. The same molecule can fall into different functional bins in different contexts. Senescence has important roles in tissue development, wound repair and tumor suppression, so suppressing all senescence would be unsafe.

## Proposed normalized scores

Define measurement `z_j(t)` for a selected factor j relative to its validated, context-matched reference range, and `w_j >= 0` calibrated from held-out data. A provisional context-dependent external harm signature can be written:

`HE(t) = sum_j w_j * max(0, z_j(t))`  with weights included only for factors causally linked to damage in the relevant context.

Likewise, `HG` is constructed from verified repair-related signals; `ME` is constructed from validated persistent-dysfunction indicators; `MG` is constructed from measured homeostatic function. **These scores cannot be calculated from a simple unvalidated marker list** and must not be used clinically.

## Six-state illustrative dynamical system

All variables are normalized to [0,1].

- `s`: fraction of cells classified as senescent by a **multimarker** definition
- `he`: damaging extracellular signal load (Honey of Evil)
- `me`: sustained cellular dysfunction (Milk of Evil)
- `hg`: verified resolution / protective signaling (Honey of Good)
- `mg`: support capacity and normal homeostasis (Milk of Good)
- `f`: functional task-response fidelity (not direct memory contents)

The model in `christeye/model.py` uses:

`hazard = max(0, a0 + ae*he + am*me - ag*hg - as*mg)`

`ds/dt = (1-s)*hazard - (clearance + u_clear)*s`

`dhe/dt = k_s*s + k_m*me - (d_e + u_block)*he`

`dme/dt = b_e*he + b_s*s - (d_m + b_g*mg)*me`

`dhg/dt = p_g + u_support - d_g*hg`

`dmg/dt = p_m + (u_support/2) - d_mg*mg`

`df/dt = k_rec*(1-f)*(hg+mg)/2 - k_dis*f*(he+me)/2`

Here `u_*` denotes a hypothetical **mathematical control**, not any specific treatment, drug, molecule, dose, or device setting. There is **no inferred biological effect size** in the coefficients, and no inference that these processes are mechanistically independent.

`clearance` refers to removal of senescent cells from tissue; a falling senescent fraction does **not** establish reversal of senescence inside the same cell. The `s` term is conceptually meaningful only after rigorous multimarker validation.

## Clinical safety constraint (research only)

A potential future controller would need to minimize a prespecified loss:

`J = E[lambda_s*s(t) + lambda_d*me(t) + lambda_e*he(t) + lambda_f*(1-f(t)) + lambda_h*harm(t)]`

subject to hard constraints on cell survival, immune protection, tissue repair, tumor surveillance, adverse effects, and uncertainty. Never optimize simply to make cytokines or all senescent cells disappear. If the evidence does not support a safe action, the correct controller response is **no intervention / escalation for expert review**.

## Early-detection question

The proposed onset-warning objective is to estimate a **calibrated conditional probability**:

`Pr(new senescence state within tau | longitudinal marker history, cell type, context)`

A valid signal must predict outcomes in held-out biological replicates and distinguish senescence from temporary inflammation, differentiation, quiescence, and acute damage. A low false-positive rate is especially important. Do not use single-marker p16, p21, or SA-beta-gal alone.

## Falsification criteria

1. Adding extracellular signatures does not improve out-of-sample senescence prediction over cell-intrinsic markers.
2. Changes predicted as restoration do not improve viable tissue function, or worsen normal immune defense.
3. A supposed model intervention reduces a secreted marker but fails to change persistent dysfunction.
4. Model direction varies substantially by cell type, stage, or tissue and is not invariant across cohorts.
5. The reported link between astrocyte memory and senescence cannot be reproduced within *the same measured biological system*.

## Interpretation of outputs

The numerical demonstration compares early/late *idealized* containment and support scenarios solely to test numerical behavior and sensitivity. It is not an anti-aging efficacy estimate, clinical decision support, or evidence that senescence has been prevented in an organism.


## v0.2 addition — response arbitration (not established biology)

Separate retained learned response from which action is chosen. With H-/M- and H+/M+ context-valued states, and need N:

`wI = sigmoid(b0 + bE*H- + bM*M- - bG*H+ - bS*M+ + bN*N)`

`P(action=a) = softmax_a(beta * (wI * U_immediate(a) + (1-wI) * U_learned(a)))`

**Do not treat labels as moral chemistry, assume all immediate actions are harmful, or interpret simulated choice probabilities as measured animal or human behavior.**

Study-specific discrimination index: `D=P(response|learned cue)-P(response|neutral cue)`. A comparison requires the same animal and task conditions; memory-content substitution is not inferred from one mismatched response.


## v0.2 addition — response arbitration (not established biology)

Separate retained learned response from which action is chosen. With H-/M- and H+/M+ context-valued states, and need N:

`wI = sigmoid(b0 + bE*H- + bM*M- - bG*H+ - bS*M+ + bN*N)`

`P(action=a) = softmax_a(beta * (wI * U_immediate(a) + (1-wI) * U_learned(a)))`

**Do not treat labels as moral chemistry, assume all immediate actions are harmful, or interpret simulated choice probabilities as measured animal or human behavior.**

Study-specific discrimination index: `D=P(response|learned cue)-P(response|neutral cue)`. A comparison requires the same animal and task conditions; memory-content substitution is not inferred from one mismatched response.


## v0.2 addition — response arbitration (not established biology)

Separate retained learned response from which action is chosen. With H-/M- and H+/M+ context-valued states, and need N:

`wI = sigmoid(b0 + bE*H- + bM*M- - bG*H+ - bS*M+ + bN*N)`

`P(action=a) = softmax_a(beta * (wI * U_immediate(a) + (1-wI) * U_learned(a)))`

**Do not treat labels as moral chemistry, assume all immediate actions are harmful, or interpret simulated choice probabilities as measured animal or human behavior.**

Study-specific discrimination index: `D=P(response|learned cue)-P(response|neutral cue)`. A comparison requires the same animal and task conditions; memory-content substitution is not inferred from one mismatched response.
