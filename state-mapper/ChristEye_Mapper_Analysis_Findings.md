# ChristEye Knowledge State Mapper — Execution and Scientific Audit

**We Develop Software LLC · CE-MEM-DATA-005 · 3 November 2026**  
**Execution status:** Software tests passed. Extended computational checks completed. **All numeric results below are from synthetic data, not real molecular measurements.**

## Executive conclusion

The program correctly executes its analysis of independent simulated preparations and includes important safeguards against treating individual cells as independent biological replicates. It can identify condition-specific expression patterns in a deliberately engineered simulator. **The current evidence does not establish that ARC-containing RNA encodes a memory, that IGFBP2 indexes memories, or that knowledge was transferred to another network.**

The most informative new result is that perfect simulated *task identity classification* did not translate into better *delayed-response prediction*. This exposes a distinction the next phase of ChristEye should prioritize: a molecular signature of having experienced an event versus a molecular signature of how well a specific learned response persists.

## Data and methods actually used

- Input: the **supplied project** and its **explicitly SYNTHETIC** `cells.csv`, `endpoints.csv`, `spatial.csv`, and provenance fixture.
- Size: **3,024** synthetic cells, **54** synthetic preparations (18 each for control, task A, task B), **16** genes. The task A/B classifier uses **36** independent simulated preparations. Preparation-level averages were used, not individual cells as independent test observations.
- Verification: `python -m unittest discover -s tests -v` — **3/3 tests passed**. Fresh `python -m christeye_ksm demo` run succeeded, including spatial and provenance exports.
- Extension: within the supplied project, `scripts/extended_analysis.py` compares cell-compartment ablations, single-gene models, 80 label permutations, compartment shuffles, and held-out prediction of a separate synthetic delayed-response variable.
- Modeling: 5-fold stratified cross-validation for task A/B classification; 6-fold held-out regression for delayed response with condition identity controlled; independent preparation-level observations in both.
- **Public-data status:** GSE246147 was confirmed as an appropriate public mouse basolateral-amygdala transcriptional study. Its matrix and annotations were not fetched into this execution environment because outbound file retrieval was unavailable. **No real GEO expression matrix was analyzed.**

## A. Original project: task A versus task B

| Model | Balanced accuracy | Macro-F1 |
|---|---:|---:|
| Neuron only (16 markers) | 1.000 | 1.000 |
| Neuron plus astrocyte (32 compartment-specific markers) | 1.000 | 1.000 |

The 100% values are **by design**: the generator increases **Penk**, **Arc**, **Gria1** in task-A neurons; **Tac1**, **Fos**, **Gria2** in task-B neurons; **Igfbp2**, **Adrb1** in task-A astrocytes; and **Adra1a**, **Ldha** in task-B astrocytes. Real data do not have these deliberately guaranteed separations.

## B. New feature-ablation findings — synthetic only

| Features | Balanced accuracy |
|---|---:|
| Neuron only | 1.000 |
| Astrocyte only | 1.000 |
| Both compartments | 1.000 |
| Neuronal Arc only | 0.778 |
| Astrocytic Igfbp2 only | 1.000 |
| Arc plus Igfbp2 | 0.972 |
| Nontarget cell-identity markers | 0.500 |

**Interpretation:** The procedure recognizes the deliberately encoded difference between the simulated conditions, and the nontarget marker control is at chance. The strong Igfbp2 result is a *direct consequence of how the simulator was written*. It is not evidence that IGFBP2 decodes biological memory content. Slightly lower performance with both Arc and Igfbp2 than Igfbp2 alone is possible with small datasets and model regularization.

## C. Compartment falsification — synthetic only

| Manipulation | Neuron-only | Astrocyte-only | Both |
|---|---:|---:|---:|
| Original data | 1.000 | 1.000 | 1.000 |
| Shuffle neuron profiles across task labels | 0.556 | 1.000 | 1.000 |
| Shuffle astrocyte profiles across task labels | 1.000 | 0.500 | 1.000 |
| Shuffle both compartments | 0.556 | 0.500 | 0.583 |

These deliberately destructive controls show that the software can distinguish which simulated compartment contains task-label information. However, **the current simulator does not test transfer**, and the shuffling test does not establish that a molecular state *causes* a learned behavior.

**Label permutation:** 80 independent task-label permutations produced mean balanced accuracy **0.519** (5th–95th percentile: **0.332–0.667**) versus original **1.000**. This is expected from artificial label-conditioned signals and is not an empirical neuroscience significance test.

## D. Important new result: delayed-response prediction — synthetic only

This analysis joins the existing simulated `endpoints.csv` to the preparation-level features. It assesses a separate target: **48-hour delayed response score**, and includes task identity as a control so a molecular model cannot win merely by recognizing task A versus task B.

| Model | Out-of-fold RMSE (lower better) | Out-of-fold R² |
|---|---:|---:|
| Task-condition average only | **0.06795** | **0.5334** |
| Condition + neuronal expression | 0.08218 | 0.3176 |
| Condition + astrocytic expression | 0.08628 | 0.2478 |
| Condition + both compartments | 0.07904 | 0.3687 |

The simpler baseline performed better. A model can be excellent at *classifying condition identity* while adding no predictive value for *memory persistence*. This is a **failure to support the incremental retention-prediction hypothesis in the existing synthetic fixture**, not a biological falsification: the fixture did not deliberately encode a strong condition-independent retention mechanism.

## E. Limits and code-audit observations

1. **GEO not loaded:** Do not attribute synthetic plots or quantitative results to GSE246147, GSE272414, or any actual mouse.
2. **Task discrimination is not memory decoding:** Task labels were used to generate specific genes in the fixture, so the models recover information embedded by the data generator.
3. **Endpoint omission in the original pipeline:** The supplied `run_analysis()` does not use `endpoints.csv`; this separate extension newly evaluates delayed response.
4. **Only two models are built in:** The supplied classifier compares neurons versus combined; the extension adds astrocyte-only, individual markers, and negative controls.
5. **Preprocessing leakage risk:** The original classifier imputes missing values using the full candidate dataset *before* cross-validation. It does not affect the complete synthetic matrix, but for real data imputation should be inside each training fold. The extension does this for classification and regression.
6. **Preparation versus animal independence:** The code aggregates by `preparation_id`; real data additionally require confirmation that the same animal does not appear under several preparation IDs, and that batch or phase does not confound condition.
7. **Spatial graph scope:** Its 4,536 simulated neuron–astrocyte proximity pairs are geometry only, not confirmed synapses or RNA transfer edges. The median distance in the demo is 14.58 simulated micrometers.
8. **RNA provenance:** One simulated row is labeled `functional_candidate`, but it is not empirical transfer; the audit is a decision-rule illustration.
9. **Raw RNA *sequences* are not analyzed:** The project currently measures named gene expression features, not the nucleotide structure, isoforms, source-specific RNA sequences, RNA packaging, or transfer paths.
10. **No causal interventions:** None of the outputs demonstrates necessity or sufficiency of ARC or IGFBP2 for any task-specific response.

## F. Prioritized real-data research plan

**Milestone 1 — Molecular expression reproducibility.** Obtain the actual raw/processed matrices and metadata from GSE246147. Inspect biological preparation identifiers, condition, phase, cells, batches, and quality controls. Replicate published neuronal trends (e.g., Penk/Tac-associated subpopulations) and quantify astrocyte profiles **within each authentic animal**. Compare single-gene, neuron-only, astrocyte-only, and combined models; apply permutation and independent-animal holdouts. Analyze GSE272414 separately for astrocyte priming/recall patterns; never infer cross-study RNA transfer.

**Milestone 2 — Test incremental astrocyte information.** Prespecify whether astrocyte features add **out-of-sample** predictive value beyond neuronal activity and preparation covariates. A negative outcome is informative. Distinguish which condition was measured from how well memory was retained.

**Milestone 3 — Spatial controls.** Analyze original MERFISH section coordinates using within-section spatial permutations and cell-density controls. Report *proximity* until independent imaging or physiology supports contact or communication.

**Milestone 4 — Retention-linked multimodal data.** Use appropriately overseen nonclinical research with matched behavior measured at delay, neuronal activity, molecular state, and astrocyte state in the same biological preparations. Test whether molecular features predict performance **beyond training condition, activity, and stress**.

**Milestone 5 — RNA provenance and functional transfer.** A separate future experimental study would need donor-specific RNA identification, verified recipient entry, contamination exclusion, downstream functional change, and an independently retained, task-specific response. Existing GEO gene-expression tables cannot supply those observations.

## G. Testable hypotheses produced by this audit

- **H1 / Incremental support:** Astrocyte molecular state may add predictive information for *later retention* after controlling neuronal measures—not necessarily for task identity.
- **H2 / Archive vs traffic:** RNA abundance alone may weakly predict retention; compartmental localization, protein/receptor state and synaptic structure could be stronger predictors, if measured.
- **H3 / Specificity requirement:** A molecular archive model should distinguish two experiences with similar arousal or activity, rather than merely distinguishing stimulated from unstimulated tissue.
- **H4 / Transfer requires causation:** A candidate RNA cargo should be traced by origin and tested for a recipient-specific effect independent of ordinary signaling; joint expression cannot establish transfer.
- **H5 / Knowledge persistence:** In a proposed network-joining system, a truly inherited response must remain measurable after the source network is inaccessible, including on unseen examples.

## Reproduction

From the extracted project root:

```bash
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python -m christeye_ksm demo --out outputs/demo
python scripts/extended_analysis.py
```

Inspect `outputs/extended_synthetic_audit/feature_ablation.csv`, `compartment_shuffle.csv`, `delayed_response_prediction.csv`, `permutation_control.json`, and the corresponding PNG figures.

## Data sources and scientific context

- User-supplied *Mapping the Molecular Knowledge State* basis, CE-MEM-DATA-005, 3 November 2026.
- Sun et al., *Nature* (2024), doi:10.1038/s41586-023-07011-6; public GEO **GSE246147**: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE246147
- Dewa et al., *Nature* (2025), doi:10.1038/s41586-025-09619-2; public GEO **GSE272414**: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE272414
- Pastuzyn et al., *Cell* (2018), doi:10.1016/j.cell.2017.12.024.

**Conclusion:** The project is a usable computational prototype and a sound starting point for falsifiable molecular-memory research. The current demonstrable achievement is validating a measurement/analysis framework against synthetic ground truth, *not* establishing a molecular archive of knowledge or memory transfer. The next scientifically decisive output is a replicated, independent-animal real-data analysis—then, ultimately, retention-linked data.
