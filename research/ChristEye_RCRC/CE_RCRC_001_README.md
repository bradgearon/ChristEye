# ChristEye Radiation Containment and Recovery Controller (CE-RCRC-001)

Version 1.0 — 2026-11-04

This is a non-radiological demonstration of measurement, transport modeling, and constrained feedback. It is **NOT** a radiation protection device. No radioactive sources, antimatter creation, irradiation, aerosol generation, or human/animal experiments are part of this kit.

Files:
- ChristEye_RCRC_001_Scientific_Basis_v1.docx — scientific basis and equation map
- ChristEye_RCRC_001_Construction_Guide_v1.docx — device modules, parts list and safe assembly
- ChristEye_RCRC_001_Experimental_Protocol_v1.docx — preregistration-ready validation protocol
- CE_RCRC_001_Digital_Twin.py — standard-library Python 3 synthetic simulator, **NO HARDWARE CONTROL**
- CE_RCRC_001_BOM.csv — indicative budget and materials
- CE_RCRC_001_Demo_Data/ — output from one 24-seed example run

## Run the offline simulation

```bash
python CE_RCRC_001_Digital_Twin.py --runs 24 --out trial_outputs
```

These calculations test logical consistency, not medical or radiation safety. Any real radiological deployment would require radiation-safety and regulatory engineering approvals with independent protective systems.
