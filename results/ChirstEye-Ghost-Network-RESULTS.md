# ChristEye Cross-Scale Atlas — Research findings, November 4, 2026

## Answer to the research question

The project identifies a *cross-domain modeling template*—a network that receives physical inputs, has measurable internal state, and changes over time—but **does not** identify a new universal law linking cerebral engrams to celestial networks. The strongest completed empirical track is a limited 61-point NOAA Kp time-series benchmark.

### Measured geomagnetic sample

- 61 genuine NOAA preliminary 3-hour planetary Kp measurements from 2026-10-28 00:00 UTC to 2026-11-04 12:00 UTC, supplied in the source package and reproducible offline.
- Lag-one sample correlation 0.6954; lag-two 0.5756; lag-three 0.5265. Short-term statistical persistence is present.
- Peak Kp 6.00 (2026-10-31 18:00 UTC); 4 observations had Kp >= 4, and only one Kp >= 5.
- Fixed chronological 40-train / 21-test one-step RMSE: persistence 0.7166, AR1 0.6737, AR2 0.7453, AR3 0.7452, AR1-plus-24h-history trace 0.7273, simple exponentially weighted mean 1.0261.
- Expanding refit from sample 24 onward (37 tests) RMSE: persistence 0.9004, AR1 0.8787, AR2 0.8563, AR3 0.8490, AR1-plus-history trace 0.9290.
- Circular-block exploratory bootstrap for *MSE difference* (AR1 minus persistence): −0.0596 [95% heuristic interval −0.1849, 0.0882] — crosses zero.
- For (AR1+trace minus AR1), difference +0.0750 [0.0048, 0.1651] — extra trace did worse in this small, selected holdout.
- One-day forecast errors are larger than 3-hour errors, and a simple training mean slightly beats recursive AR1 for 24h lead (RMSE 1.006 vs 1.036). The absolute numbers depend on this short interval.

### Biological response history — **published summaries only**

Dewa et al. (Nature, 2025) report amygdalar noradrenaline-sensor half-decay of 4.3 min after conditioning shock versus 13.5 min during fear recall: ratio ~3.14. Peaks were about 0.206 and 0.211 ΔF/F respectively. Under a *hypothetical single-exponential decay* approximation, area ratio ~3.22. The biological experiment is a legitimate example of context-dependent signal duration and astrocyte-related memory stabilization, but we did not independently process mouse-level counts, 1,903 astrocyte single-cell profiles, or 677-region data. No numerical correspondence to cosmic history has been demonstrated.

### Network topology — **synthetic negative control only**

A synthetic random-geometric graph and an edge-matched Erdos–Renyi graph each contained 160 vertices and 785 edges. Mean clustering was 0.6196 vs 0.0499. Geometric proximity can drive network clustering without any neural learning. Actual Vazza/Feletti image and graph files were not available in the execution environment, so this is *not* an independent replication of the cosmic/brain comparison.

### Cross-scale equations and tests

The prior 40 CE equations and 14 CS equations were preserved in the updated Word/PDF guide; CS-15–CS-24 formalize measured Kp autocorrelation, causal past-only trace, augmented forecast, empirical skill, solar-wind physical drivers, null clustering, published astrocyte signal durations, and domain-separated model skill.

No raw OMNI solar wind, real cosmic-web node/edge data, Gaia/GALAH spectra, or astrocyte individual mouse replicates were ingested. Scripts `src/run_solar_forcing.py` and `src/astrocyte_counts_template.py` are *data-ready templates*, not performed experiments.

## Most important falsification

For the one-week geomagnetic sample, the special 24-hour trace is **not justified over a simple AR(1)** predictor. The project still needs independent physical driving inputs (wind speed, IMF Bz, density), longer multi-year holdouts and controlled biological/astronomical data to establish any distinct predictive benefit from ChristEye's mappings. The result is an analysis workflow and pilot, not a verified new astrophysical theory or a treatment.

## Source links

- NOAA SWPC Kp: https://services.swpc.noaa.gov/products/noaa-planetary-k-index.json
- NASA OMNI: https://omniweb.gsfc.nasa.gov/ow.html
- Dewa et al. (2025): https://www.nature.com/articles/s41586-025-09619-2
- NCBI GEO GSE272414: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE272414
- Vazza & Feletti (2020): https://doi.org/10.3389/fphy.2020.525731
