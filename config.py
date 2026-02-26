# =============================================================================
#  AmpClip — Configuration
#  Edit this file before each run. Do not touch ampclip.py.
# =============================================================================

# -----------------------------------------------------------------------------
#  INPUT / OUTPUT
# -----------------------------------------------------------------------------

# Path to the input prestack SEG-Y file.
INPUT_FILE = r"E:\Others\4Caro\Data\SRME_SUB.sgy"

# Path for the output SEG-Y file.
# Set to None to auto-generate a timestamped folder next to the input file.
# Example: OUTPUT_FILE = r"E:\Others\4Caro\Data\SRME_SUB_ge_clipped.sgy"
OUTPUT_FILE = r"E:\Others\4Caro\Data\SRME_SUB_clipped_30.sgy"
# -----------------------------------------------------------------------------
#  THRESHOLD
#
#  Three modes — pick one by setting THRESHOLD_MODE, then fill in the
#  corresponding parameter below.
#
#  "absolute"   — you supply a fixed number in THRESHOLD.
#                 Any sample with |amplitude| > THRESHOLD is zeroed.
#                 Use this when you know the data range or have inspected
#                 the amplitude histogram from a previous run.
#
#  "percentile" — set THRESHOLD to None; the tool scans SCAN_TRACES traces
#                 and zeros everything above the THRESHOLD_PERCENTILE-th
#                 percentile of |amplitude|.
#                 Good starting point: 99.9 (kills the top 0.1 %).
#
#  "rms"        — set THRESHOLD to None; the threshold is
#                 THRESHOLD_RMS_FACTOR × global RMS of the scanned traces.
#                 Factor 8–15 is typical for marine spike muting.
# -----------------------------------------------------------------------------

THRESHOLD_MODE = "absolute"   # "absolute" | "percentile" | "rms"

# Used when THRESHOLD_MODE = "absolute"
THRESHOLD = 30                # e.g. 5.85  (float, must be > 0)

# Used when THRESHOLD_MODE = "percentile"
THRESHOLD_PERCENTILE = 99.9     # float in range (0, 100)

# Used when THRESHOLD_MODE = "rms"
THRESHOLD_RMS_FACTOR = 10.0     # multiplier applied to global RMS

# Number of evenly spaced traces to scan when estimating the threshold.
# Higher = more accurate estimate, slightly slower.
SCAN_TRACES = 5000

# -----------------------------------------------------------------------------
#  MUTE OPTIONS
# -----------------------------------------------------------------------------

# Cosine taper half-width in samples applied on each side of a muted zone.
# 0 = hard rectangular mute (default).
# 5–10 samples softens the boundary and avoids sharp spectral artefacts.
TAPER_SAMPLES = 0

# Invert the mute polarity:
#   False (default) — zero samples ABOVE threshold  (noise spike removal)
#   True            — zero samples BELOW threshold  (keep only large amplitudes,
#                     useful for spike isolation / QC)
INVERT = False

# -----------------------------------------------------------------------------
#  QC / OUTPUT
# -----------------------------------------------------------------------------

# Run a post-write verification check (recommended).
# Confirms that the output SEG-Y has amplitudes within threshold and that
# all trace headers are byte-identical to the input.
VERIFY = True

# Generate QC plots (requires matplotlib).
# Plots are saved in the output directory under plots/.
MAKE_PLOTS = False

# Number of traces shown in the seismic section plots.
# Reduce if the file is very large and plots are slow.
PLOT_N_TRACES = 300

# Verbosity: 10 = DEBUG, 20 = INFO, 30 = WARNING
LOG_LEVEL = 20
