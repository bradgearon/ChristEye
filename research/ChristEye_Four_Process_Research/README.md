# ChristEye — Astrocyte Memory & Four-Process Senescence Atlas

**Version 0.2 · We Develop Software LLC · November 2026 · Research analysis, not a treatment**

This is a runnable, reproducible Python project to investigate whether **extracellular state plus glial state** helps explain: (1) accurate versus misgeneralized learned responses, (2) memory retrieval and extinction, (3) multiday astrocyte memory-associated regulation, and (4) paracrine spread of senescence-associated changes.

It uses four **proposed ChristEye functional process categories**:

| Process | Operational meaning |
|---|---|
| Honey of Evil | Extracellular signals experimentally associated with persistent damage in a specific context |
| Milk of Evil | Sustained intracellular, tissue, or metabolic dysfunction |
| Honey of Good | Context-specific signaling that supports resolution, adaptation, or repair |
| Milk of Good | Physiological support and stable function |

These are *modeling labels*, not scientific evidence of moral agents or a universal chemical network. The infographic supplied by the user inspired the Life/Damage/Conditional mapping, but the software does not infer moral meaning from a molecule.

## New in v0.2: response arbitration

The "ghost network" is now explicitly defined as a **proposed influence of extracellular/glial/metabolic state on response prioritization**, not an identified independent controller or a literal source of moral accusations. The software models **learned action vs immediate action** as competing options; it keeps retrieval fidelity separate from action priority. This is the inventor's conceptual vocabulary, not established biology. See `docs/response_arbitration_hypothesis.md` and `source_data/response_arbitration_evidence.csv`.

Run `python -m christeye arbitrate --out outputs/arbitration` to create synthetic trajectories and scenario probabilities. No drug efficacy or human behavior is inferred from these simulations.

## Quick start

Requires Python 3.10+.

```bash
python -m pip install -r requirements.txt
python -m christeye demo --out outputs/demo
python -m christeye arbitrate --out outputs/arbitration
python make_evidence_graph.py
python -m pytest -q
```

Windows: double-click `run_demo.bat` in the extracted folder.

Outputs: `outputs/demo/senescence_scenario_comparison.png`, `four_process_trajectories.png`, `simulation_trajectories.csv`, `group_summary.csv`, `within_study_contrasts.csv`, `synthetic_matched.csv`, and `outputs/evidence_graph/evidence_graph.png`.

**ALL included demo observations are SYNTHETIC, and mathematical coefficients are not fitted to biological data.** These demonstrate that the analysis program runs, not that a scientific hypothesis is true.

## Four source projects and their specific purposes

### 1. Guayasamin et al., eLife (2025), astrocyte dysfunction and fear generalization
- Article: https://elifesciences.org/articles/99988
- Original source data: https://osf.io/zsw6j/
- Key analyses: neutral versus conditioned cue discrimination by animal; Cx43; astrocytic calcium; LTP; corticosterone; normal learning versus impaired discrimination.
- Do **not** interpret early-life stress as measured brain-cell senescence.

### 2. Bukalo et al., Nature (2026), astrocytes and neuronal fear representations
- Article: https://www.nature.com/articles/s41586-025-10068-0
- Source data XLSX and Supplementary Table from article's **Source data** and **Supplementary information** sections.
- Key analyses: within-mouse memory stage; astrocyte/neuronal Ca signals, time-to-peak, fear retrieval, extinction, identity of actual independent animal.
- Caveat: bulk photometry, event-level imaging, and mouse-level behavior do not all have the same independent sample count.

### 3. Dewa et al., Nature (2025), multiday astrocytic memory trace
- Article: https://www.nature.com/articles/s41586-025-09619-2
- Transcriptomics: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE272414
- Experimental data and regional counts: https://neurodata.riken.jp/id/20250831-001
- Analysis code: https://github.com/Jun-Nagai-Lab/Dewa-et-al
- Key analyses: memory-related astrocyte expression, Fos, Adrb1/Adra1a, Igfbp2; brain-region-specific responses; independent biological sample groups.
- Caveat: these observations do not prove astrocytes independently store specific memory content.

### 4. Russo et al., Aging Cell (2026), senescence propagation
- Article: https://doi.org/10.1111/acel.70673
- Transcriptomic reference: https://www.ebi.ac.uk/biostudies/arrayexpress/studies/E-MTAB-15005
- Key analyses: cell-type-specific senescence programs, selected secretions including CCL2 and MIF, and candidate recipient-state changes.
- Critical limitation: E-MTAB-15005 is shared with a related 2025 brain-cell senescence study; it is **not a complete table of cytokine secretions or recipient behavioral outcomes**. Do not infer direct secretome-to-memory causal links from the RNA data.

### Data acquisition limitation

This project does **not** bundle copyrighted or remotely hosted individual-animal matrices. The original repositories must be downloaded by the user or institution. Some experiments supply figure-level source data instead of full synchronized longitudinal datasets. `source_data/published_reported_results.csv` records a small set of verified *published summary results*; it is not input for animal-level statistical analysis.

## Import a real dataset safely

First **inspect source fields**:

```bash
python inspect_or_import.py inspect path/to/supplement.xlsx
```

Then copy `schemas/example_wide_mapping.json`, and fill in the **actual source column names**, animal IDs, and experimental grouping; use an identity for the biological replicate (animal, independent culture preparation, or experimental batch as applicable). The example mapping is just a template; don't assume the publisher uses those exact column names.

```bash
python inspect_or_import.py convert path/to/actual_file.xlsx schemas/mapping_guayasamin.json outputs/real_guayasamin.csv --sheet Sheet1
python -m christeye analyze --input outputs/real_guayasamin.csv --out outputs/guayasamin
```

For another study, create a **new mapping and output**; never concatenate animal rows from different papers as if they were the same animals. Metadata and assay scales are not automatically harmonized.

For a separately validated RNA gene-expression table with fields `study_id,biological_unit,condition,cell_type,gene,normalized_expression`, run:

```bash
python gene_analysis.py --input outputs/prepared_gene_expression.csv --output outputs/gene_changes.csv
```

Expression must already be processed with appropriate technical QC and cell-type annotation; the tool aggregates cells to biological replicates before testing. Per-gene comparisons are exploratory and require independent validation.

To predict an outcome from **paired, same-study data** with distinct biological-unit IDs:

```bash
python -m christeye predict --input outputs/actual_matched_animal_table.csv --study guayasamin_2025
```

The predictor refuses to pool different studies, skips insufficient sample sizes and outputs the held-out animal score only when sufficient grouped data exist. It is not a generalized medical diagnostic.

## Equations and policy

Read `docs/equations_and_decision_rules.md` for four-process score definitions, the six-state simulated system, falsification criteria, and hard safety constraints. An early-warning model must distinguish *reversible inflammatory stress* from *cellular senescence*, while recognizing that transient senescence can contribute to wound healing and tumor protection.

## Interpreting results

- A downregulated inflammatory marker is not the same thing as restored tissue health.
- A cell's p16/p21 activity is insufficient evidence of senescence without multiple markers.
- Restoring fear discrimination is not evidence that any memory was “overwritten.”
- Correlation does not establish directed cell-to-cell signal transmission.
- Cross-paper synthesis is useful for hypothesis generation, not direct estimation of a universal causal pathway.
- No mechanism here establishes the ability to prevent, reverse, or cure all senescence in humans.

## Additional arbitration-specific measurement requirements

If a future dataset includes choice behavior, compare (a) cue-conditional response discrimination, (b) independent retained learning, (c) response latency, and (d) stress/motor/perceptual control tasks. Never use inflammatory proteins alone as ground-truth evidence of motive, anger, deception, or a second mind. The `response_priority_observations_columns.csv` schema is a **planning schema**, not proof that any cited study provides every field.

## Suggested next real-data milestones

1. Download and map Guayasamin animal-level source data; compute within-mouse conditioned versus neutral response differences, then link to astrocyte measurements *only if animal identities are matched*.
2. Extract Bukalo source data at valid independent levels; compare neural-only and neural-plus-astrocyte prediction of retrieval/extinction after grouped splitting.
3. Reproduce Dewa region-by-region Fos astrocyte signals and per-animal transcriptomics, separating condition and batch.
4. Reanalyze senescence RNA in a **separate module**; test signaling candidates against cell-type and stress conditions and assess the need for secretome data that are not available in E-MTAB alone.
5. If a qualified research institution obtains matched cell-state, extracellular secretion, and behavioral measurements in one model, test the entire proposed mediation chain prospectively.

**Use:** computational hypothesis exploration; no direct human treatment, drug selection, senolytic deployment, electrical stimulation, or wet-lab operating protocol.
