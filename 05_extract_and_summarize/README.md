***05) Extracting Diameters***

**extract_diameters_only.py:**
Main code for extracting the diameters of each branch. It takes the cross-section CSVs for curve 0 (ICA), curve 1, and curve 2, decides which daughter is ACA vs MCA. Then it finds a stable stretch of each curve where the cross-section area doesn’t jump around much (it smooths the series and applies a small variation threshold). Inside that stable span it averages circle-equivalent diameters (CE diameters) and radii and computes a roundness measure. It also saves a QC plot that marks the chosen span. Results are saved in _diam_summary_full.csv_, a run log is saved in _diam_log_full.txt_, and any problems (such as missing CSVs or “no stable span”) are listed in _diam_failures.csv_. Possible to adjust the smoothing window, span length, and threshold in the script. 

**diam_summary_full.csv:**
Main summary from the extractor script, per model. For ICA, ACA, and MCA it records the length of the stable span that was chosen and the average sizes (diameters and radii -- both CE and MIS) computed inside that span, as well as a roundness index. This file is the direct input to the Murray analysis script.

**diam_log_full.txt:**
Readable log from the diameter extraction run. It lists the time, which models were processed, what stable span lengths were selected for each branch, and any warnings such as missing curves or “no stable region found.”

**diam_failures.csv:**
CSV lists cases and sides where the extractor script couldn’t produce valid sizes and explains why (for example, a missing curve CSV or no span passed the stability test).
