# AmpClip

> **Prestack SEG-Y Amplitude Threshold Muting Tool**  
> *by Beni*

Reads a prestack (or stacked) SEG-Y file, zeroes all samples whose absolute amplitude exceeds a user-defined threshold, and writes an output SEG-Y that is structurally identical to the input — same binary header, same text header, same trace order, same trace headers. Only the sample values that exceed the threshold change.

---

## Why does this exist?

Prestack data regularly contains noise spikes, marine swell noise, equipment glitches, or other high-amplitude artefacts that survive SRME, deconvolution, and other processing steps. These spikes can distort stacking, velocity analysis, and AVO workflows.

AmpClip removes them cleanly in a single pass, producing an output file that any standard seismic interpretation or processing package can read without modification.

---

## Features

- **Three threshold modes**: explicit absolute value, percentile of the amplitude distribution, or a multiple of the global RMS — pick whatever fits your workflow.
- **Optional cosine taper**: softens the mute boundary with a configurable half-width (in samples) so the transition is not a hard rectangular window.
- **Invert mode**: keep only samples *above* the threshold and zero everything else (useful for spike isolation / QC).
- **Full header preservation**: binary header, EBCDIC text header, and all 240 bytes of every trace header are copied verbatim — no re-indexing, no geometry scrambling.
- **Post-write verification**: optional spot-check that confirms amplitudes are within threshold and headers are intact before you declare success.
- **Structured output directory**: timestamped folder with the output SEG-Y, a plain-text report, a JSON summary, and a detailed log file.
- **tqdm progress bars**: because you deserve to know what is happening.

---

## Installation

```bash
pip install segyio numpy tqdm
```

Or use the requirements file:

```bash
pip install -r requirements.txt
```

---

## Quick Start

Open `ampclip.py`, scroll to the **USER CONFIGURATION** block at the bottom, set your paths and parameters, and run:

```bash
python ampclip.py
```

### Example — percentile threshold (recommended starting point)

```python
INPUT_FILE           = r"/data/SRME_SUB_ge.sgy"
THRESHOLD            = None
THRESHOLD_MODE       = "percentile"
THRESHOLD_PERCENTILE = 99.9        # mute the top 0.1 % of amplitudes
TAPER_SAMPLES        = 5           # 5-sample cosine taper on each side
OUTPUT_FILE          = None        # auto-generated in timestamped directory
VERIFY               = True
```

### Example — explicit absolute threshold

```python
INPUT_FILE     = r"/data/SRME_SUB_ge.sgy"
THRESHOLD      = 1.5e6             # your known threshold
THRESHOLD_MODE = "absolute"
OUTPUT_FILE    = r"/data/SRME_SUB_ge_clipped.sgy"
VERIFY         = True
```

### Example — RMS-factor threshold

```python
INPUT_FILE           = r"/data/SRME_SUB_ge.sgy"
THRESHOLD            = None
THRESHOLD_MODE       = "rms"
THRESHOLD_RMS_FACTOR = 10.0        # mute anything > 10 × global RMS
```

---

## API usage

You can also call the functions directly from another script:

```python
from ampclip import run, estimate_threshold_from_percentile

# Estimate a threshold first
thr = estimate_threshold_from_percentile("/data/shot_gathers.sgy", percentile=99.9)
print(f"Suggested threshold: {thr:.4g}")

# Run the muting
output = run(
    input_path    = "/data/shot_gathers.sgy",
    threshold     = thr,
    taper_samples = 5,
    verify        = True,
)
print(f"Output: {output}")
```

---

## Output structure

```
<stem>_AMPCLIP_<YYYYMMDD_HHMMSS>/
├── logs/
│   └── ampclip.log          ← full DEBUG log
└── reports/
    ├── ampclip_report.txt   ← human-readable summary
    └── ampclip_summary.json ← machine-readable summary
```

The clipped SEG-Y is written inside this directory unless you specify `OUTPUT_FILE` explicitly.

---

## Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `input_path` | str | — | Path to the input SEG-Y file |
| `threshold` | float \| None | None | Absolute amplitude threshold. `None` triggers auto-estimation. |
| `output_path` | str \| None | None | Output SEG-Y path. `None` = auto-generated. |
| `taper_samples` | int | 0 | Half-width of cosine taper in samples. 0 = hard mute. |
| `invert` | bool | False | If True, zero samples *below* threshold instead. |
| `verify` | bool | True | Post-write spot-check. |
| `threshold_mode` | str | "absolute" | `"absolute"` \| `"percentile"` \| `"rms"` |
| `threshold_percentile` | float | 99.9 | Percentile used when `threshold_mode="percentile"`. |
| `threshold_rms_factor` | float | 10.0 | RMS multiplier used when `threshold_mode="rms"`. |
| `scan_traces` | int | 5000 | Traces scanned for auto-estimation. |

---

## Threshold guidance

| Situation | Recommended mode | Typical value |
|---|---|---|
| Known data range / physical units | `absolute` | based on data |
| First pass, unknown data | `percentile` | 99.9 – 99.99 % |
| Spike muting on marine data | `rms` | 8–15 × RMS |
| Conservative clip (protect signal) | `percentile` | 99.99 % |
| Aggressive clip (heavy noise) | `rms` | 5 × RMS |

Start conservative. The report tells you exactly how many samples and traces were affected, so you can iterate quickly.

---

## Verification

When `verify=True` (default), AmpClip opens the output file after writing and checks:

1. Trace count matches input.
2. Sample count matches input.
3. A random sample of traces contains no amplitudes exceeding the threshold.
4. All trace header bytes of sampled traces are identical to the input.

The result is logged and written to the JSON summary. A failing verification does **not** delete the output file — it logs a warning so you can inspect.

---

## Notes

- The output file is written with `segyio.create`, which preserves the data format code (IBM float, IEEE float, etc.) from the input binary header. The amplitude threshold is applied in floating-point arithmetic regardless of the stored format.
- Very large files are processed trace-by-trace in a single pass; memory usage is O(samples_per_trace), not O(file_size).
- The cosine taper is applied purely to the data — trace headers are never modified.

---

## Requirements

- Python ≥ 3.8
- segyio ≥ 1.9.0
- numpy ≥ 1.21.0
- tqdm ≥ 4.62.0

---

## License

MIT — by Beni.
