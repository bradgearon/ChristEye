# ChristEye / CE-MEM-DATA-006 — Knowledge Retention and Mouse Behavior–Gene Mapping

**We Develop Software LLC · 3 November 2026 · Completed computational test, not biological validation**

## Executive result

The mapper now evaluates held-out **delayed-response prediction** rather than only training-condition recognition. It also constructs a **mouse behavior-to-expressed-gene atlas**, with optional reference-genome loci when an authenticated GTF is supplied. All experimental results below use **synthetic data by design**; no real GEO expression matrices or matched mouse retention measurements were loaded. The project has **nine passing automated tests**.

## Experiment and controls

For each of four simulated scenarios, 135 animals (45 per condition: control, task A, task B) provide 2,700 simulated cells (10 neurons + 10 astrocytes per animal) with 16 assayed gene symbols. Each scenario uses 16 repeated train/test splits grouped by animal. Model performance is evaluated against a baseline that knows condition identity but not expression.

The scenarios deliberately set independent hidden retention factors in neural and/or astrocytic transcript abundance. That design is a **positive control for the software**: success is expected if feature handling, sample alignment and splitting work. The null scenario plants no additional retention signal.

| Synthetic scenario | Condition baseline RMSE | Neuron-only RMSE | Astrocyte-only RMSE | Combined RMSE | Added value of combined vs baseline |
|:--|--:|--:|--:|--:|--:|
| No expression→retention signal | 0.0878 | 0.0886 | 0.0886 | 0.0891 | **−0.0013** |
| Astrocyte features carry planted signal | 0.1931 | 0.1965 | 0.1030 | 0.0970 | **+0.0961** |
| Neuronal features carry planted signal | 0.1678 | 0.0895 | 0.1703 | 0.0900 | **+0.0778** |
| Independent neuron + astrocyte signal | 0.2207 | 0.1867 | 0.1652 | 0.1021 | **+0.1186** |

RMSE is averaged over *dependent repeated holdouts*, not independent experiments. These values are not confidence intervals and do not report biological prediction accuracy. Lower RMSE is better.

## Mouse behavior to 'genome' map

**What is actually mapped:** the synthetic animal's measured delayed-response score → a mouse-preparation expression profile → the contributing gene-symbol/compartment features. These are not personal genome variants or DNA sequences.

- In the astrocyte-planted scenario, the highest within-condition correlations are astrocytic **Igfbp2** (~0.844), **Adrb1** (~0.841), and **Ldha** (~0.835).
- In the neuron-planted scenario, the highest correlations are neuronal **Arc** (~0.842), **Camk2b** (~0.832), and **Gria1** (~0.831).
- In the null scenario, the highest absolute correlation is only ~0.058; multiple-testing-adjusted q-values are ~0.99.
- In the independent two-compartment scenario, both classes contribute and the combined model predicts better than either class alone.

**The values above are properties deliberately planted into synthetic data. They are not observations about real mice or demonstrations of a genomic code for knowledge.**

The program also exports a distinct **published behavior-cohort map**. The real studies used the mouse basolateral-amygdala fear-learning paradigm (GSE246147) and NoFC, FC, NoFR, and FR cohorts (GSE272414). The atlas includes carefully labeled *literature-derived gene candidates* but does not invent genotype, individual freezing scores, paired transcriptomic–behavior data, or RNA exchange between animals.

## Falsification and audit

1. **Null gate:** combined transcriptomics does not help when the synthetic retention signal is independent of expression.
2. **Compartment specificity:** neuron-only input fails to recover a planted astrocyte-specific signal, and the reverse.
3. **Complementarity:** for two independent planted sources, the combined model wins.
4. **Animal grouping:** the same animal never occurs in both train and held-out partitions.
5. **Exact data linkage:** missing subject identities or mismatched expression/behavior preparations cause a hard error.
6. **Genome coordinates:** gene chromosome positions are absent unless an explicit GTF and genome assembly are supplied; the test GTF is synthetic and never passed off as a real locus.
7. **Study separation:** real GEO cohorts are described in a literature map, not incorrectly fused into one mouse-level dataset.

## Next scientifically decisive test

Access *authentic animal-matched* behavioral retention readouts and RNA expression from the **same animals**, with animal IDs, task/phase, batch and assay documentation. Then preregister whether neuron+astrocyte expression predicts a held-out quantitative retention measure better than a condition-only and neuron-only baseline. If no matched readout exists, the next step is a controlled prospective study—not inferring missing behavior from condition labels.

**Why this matters:** classifying fear-conditioning versus recall groups is not the same as predicting retention for a particular animal. Gene-expression correlations alone do not show RNA transfer, neural network integration, or memory cloning.

## Source references

- Sun et al., *Nature* (2024), fear-memory-associated neuron/astrocyte programs, https://doi.org/10.1038/s41586-023-07011-6 ; GEO https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE246147
- Dewa et al., *Nature* (2025), astrocyte eligibility trace, IGFBP2, fear/recall cohorts, https://doi.org/10.1038/s41586-025-09619-2 ; GEO https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE272414
- Pastuzyn et al., *Cell* (2018), ARC mRNA transport, https://doi.org/10.1016/j.cell.2017.12.024

**Status:** software test passed; public cohort labels verified; independent real-data replication **not performed**.
