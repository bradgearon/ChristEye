# ChristEye Knowledge State Mapper — CE-MEM-DATA-005

**We Develop Software LLC | exploratory, nonclinical analysis project | 03 Nov 2026**

This Python project tests a *restricted, measurable* part of the ChristEye Knowledge State Genome (KSG) hypothesis: **are neuronal and astrocytic gene-expression patterns associated with different learning conditions, and do combined features distinguish those conditions at the level of independent biological preparations?**

The starting documents are `ChristEye_Molecular_Knowledge_State_Scientific_Basis_v1(2).docx` and `ChristEye_RNA_Transfer_Experiment(1).docx`. The project's KSG map covers G (gene reference), T (transcript expression), V (vesicle/RNA cargo, only with independent measurement), P (protein/receptor state, only with independent measurement), S (structure/proximity, only with spatial or anatomical data), and R (response/retention, only with matched behavioral endpoints). **RNA expression alone does not measure vesicular transfer, synaptic connectivity, memory content, or recall.**

## Quick start — works offline

In a terminal from the unzipped project directory:

```bash
python -m pip install -r requirements.txt
python -m christeye_ksm demo --out outputs/demo
python -m unittest discover -s tests -v
```

See `outputs/demo/analysis/REPORT.md`, `heldout_model_comparison.csv`, `molecular_state_pca.png`, `knowledge_state_evidence_graph.graphml`, and the separate spatial and RNA-provenance audit folders.

**Every output of `demo` is explicitly SYNTHETIC.** No real GEO expression matrix is included in the archive. The demo validates code structure, not a neuroscience discovery. This environment could verify repository metadata online but cannot download GEO datasets into the project, so it contains real-data adapters plus a reproducible download script instead of silently representing mock data as real data.

## Public data inventory (do not pool naïvely)

| Data | Study / question | Analysis possible | Important limitation |
|---|---|---|---|
| GSE246147 | Sun et al. mouse BLA fear-learning single-cell RNA | Neuron and astrocyte expression programs within the same study | Sample/animal identities and labels must be verified; cells are not independent replicates |
| GSE272414 | Dewa et al. amygdala astrocytes after NoFC/FC/NoFR/FR | Astrocyte priming, receptor and Igfbp2-associated transcription | Astrocyte-enriched study; cannot claim paired neuron–astrocyte interaction |
| Figshare 24424801 | Sun et al. MERFISH | Candidate proximity relationships within original samples | Distance alone is not synaptic contact, molecular transfer, or causation |

**These resources are different experiments. Never create a donor→recipient link between cells from different studies based on expression alone.**

### GSE246147 real-data path

1. Download lightweight annotations:

```bash
python scripts/fetch_gse246147.py --out data/raw/GSE246147
```

2. Download the large sparse matrix (~139 MB compressed, more when loaded) with explicit consent:

```bash
python scripts/fetch_gse246147.py --out data/raw/GSE246147 --include-matrix
```

3. Inspect annotation columns, *without inventing replicate labels*:

```bash
python -m christeye_ksm inspect --csv data/raw/GSE246147/GSE246147_cell_type_data.csv.gz --out outputs/annotation_audit.json
```

4. After inspecting, provide **actual** column names, as shown here with placeholders:

```bash
python -m christeye_ksm import-10x \
  --matrix data/raw/GSE246147/GSE246147_matrix.mtx.gz \
  --features data/raw/GSE246147/GSE246147_features.tsv.gz \
  --barcodes data/raw/GSE246147/GSE246147_barcodes.tsv.gz \
  --metadata data/raw/GSE246147/GSE246147_cell_type_data.csv.gz \
  --metadata-id-col ACTUAL_BARCODE_COLUMN \
  --celltype-col ACTUAL_CELLTYPE_COLUMN \
  --condition-col ACTUAL_CONDITION_COLUMN \
  --preparation-col ACTUAL_ANIMAL_OR_SAMPLE_COLUMN \
  --output data/processed/GSE246147_cells.csv
```

**If the metadata have no trustworthy animal/preparation or learning-condition column, omit those arguments**; the importer records `MISSING` and the analysis *skips supervised model inference* rather than treating cells as animals. It will still export descriptive gene summaries. Use `--phase-col` only if such a field exists. Barcode matches must be exact at ≥90%; otherwise import aborts. Gene values are library-size-normalized log1p counts per 10,000.

Run:

```bash
python -m christeye_ksm analyze --cells data/processed/GSE246147_cells.csv --out outputs/GSE246147
```

### GSE272414 real-data path

Open [GEO GSE272414](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE272414). Review its supplementary files and study-specific metadata. Follow a source-specific, audited conversion to a **wide CSV** with one row per cell and numeric gene columns (e.g. `Arc`, `Fos`, `Igfbp2`, `Adrb1`, `Adra1a`). For example, if your exported CSV has `cell_barcode`, `annotation`, `animal`, `group`:

```bash
python -m christeye_ksm import-csv --source my_gse272414_export.csv \
  --cell-id-col cell_barcode --celltype-col annotation \
  --condition-col group --preparation-col animal \
  --output data/processed/GSE272414_cells.csv
python -m christeye_ksm analyze --cells data/processed/GSE272414_cells.csv \
  --out outputs/GSE272414 --task-a FC --task-b FR
```

Note: FC versus FR contrasts conditioning with recall and may involve different behavioral conditions; they are **not** two arbitrarily trained memory identities. Avoid describing discrimination as a decoder of personal memory contents.

### MERFISH spatial analysis

Prepare a CSV with `cell_id,sample_id,cell_type,x_um,y_um`, where all coordinates use **micrometers within a single original section/sample**. Then:

```bash
python -m christeye_ksm spatial --csv my_merfish_cells.csv --out outputs/MERFISH
```

The output records closest neuron–astrocyte pairs *within* sample, always labeled `spatial_proximity_only`. These are NOT confirmed physical contacts or transfer edges. The real Figshare download is intentionally manual because the original file formats and metadata must be inspected before mapping.

### RNA provenance (not inferred from these GEO studies)

If an independent experiment produces per-candidate donor/recipient provenance with explicit contamination and functional controls, provide a CSV with `donor_id,recipient_id,cargo_id,source_identified,recipient_entry_verified,contamination_excluded,functional_change_verified`:

```bash
python -m christeye_ksm audit-transfer --csv candidates.csv --out outputs/provenance
```

Status is `not_established`, `source_resolved_candidate`, or `functional_candidate`. **Even a functional candidate cannot by itself demonstrate transfer of learned knowledge** without causal, content-specific tests.

## Strict interpretation rules

- The output `knowledge_state_evidence_graph.graphml` links samples with **measured** gene features, *not axons or synapses*.
- No graphs are constructed across datasets unless grounded sample-level alignment is present.
- Cells from the same animal are aggregated into a single independent preparation-level observation before classification; rows with missing authentic replicates disable predictive modeling.
- Comparisons are exploratory. The default demo produces two tasks with synthetic signals on purpose, making a convincing plot expected rather than a discovery.
- Expression of `Arc`, `Fos`, or `Igfbp2` alone cannot identify a specific remembered experience; these may change with arousal, stress, and generic activity.
- Real work requires preregistration, batch controls, negative controls, multiple biological preparations, independent datasets, and outside-animal validation where possible.
- No clinical, cell-engineering, biological delivery, or human brain interface procedures are provided.

## Files

- `christeye_ksm/synthetic.py`: deterministic **SYNTHETIC** data with known task labels.
- `christeye_ksm/io.py`: audited GEO 10x importer and mapped CSV input.
- `christeye_ksm/analysis.py`: preparation-level descriptive/predictive models, spatial nearest-neighbor, provenance gate.
- `christeye_ksm/__main__.py`: CLI entry point.
- `scripts/fetch_gse246147.py`: opt-in GEO source downloader with SHA256 manifest.
- `configs/datasets.json`: GEO and MERFISH provenance registry.
- `tests/test_pipeline.py`: smoke, isolation, and fail-closed tests.
- `outputs/demo/`: **SYNTHETIC only**, precomputed test run.

## Citations

1. Sun et al., *Nature* (2024), https://doi.org/10.1038/s41586-023-07011-6
2. Dewa et al., *Nature* (2025), https://doi.org/10.1038/s41586-025-09619-2
3. Sánchez Romero and Navarrete, *Nature Reviews Neuroscience* (2026), https://doi.org/10.1038/s41583-025-01012-2
4. Pastuzyn et al., *Cell* (2018), https://doi.org/10.1016/j.cell.2017.12.024
5. Uytiepo et al., *Science* (2025), https://doi.org/10.1126/science.ado8316

Licensed for research and education as a prototype; assess third-party dataset licenses separately.
