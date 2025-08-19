06) Analysis for Murray's Law Metrics

**murray_analysis_only.py:**
This script calculates Murray’s deviation and the best exponent k from the radii in diam_summary_full.csv. Deviation is reported as a percent difference between the parent’s radius³ and the sum of the daughters’ radius³, normalized by the parent; positive means the parent looks bigger than the daughters predict, negative means smaller. 
For k, it tries two methods: 
(1) a  minimization that finds the k minimizing the absolute error in rp^k = r1^k + r2^k (Murray's Law power relationship with exponent k)
(2) a root-finding attempt that solves the equation directly if possible. 
It saves a tidy _murray_output_results.csv_ with radii, deviation, and both k estimates, writes simple QC plots per model to a folder, and lists any skipped models (invalid or missing radii) in _skipped_models.csv_.

**murray_output_results.csv:**
Final results table for Murray’s law. For each model it includes the ICA, MCA, and ACA radii pulled from the summary, the deviation percentage, and the best-fit k from the minimization (and, if the equation crossed zero, also from root-finding). This is the file that's later analyzed in R to compare modality and side. 

**skipped_models.csv:**
Short CSV lists any models that the Murray step had to skip, usually because the radii were missing, zero, or NaN. There are some missing curves / sides, so most probably won't be empty.

**murray_final_stats_analysis:**
R Markdown script analyzes Murray’s Law results for the ICA bifurcations. It reads murray_output_results.csv (radii for ICA/ACA/MCA, Murray deviation %, and two k estimates), cleans the data (drops missing/invalid rows, prefers k_root when available, otherwise uses k_minimize), and produces visualizations (histograms of deviation and k, scatter of k vs. deviation with a smooth trend). It tests whether modality (CT vs. MR) and side (L vs. R) affect deviation and k using two-way ANOVA. Uses a linear mixed effects models to include a random intercept for Patient_ID (parsed from Model_ID). Calculates  ICC to show inter-subject vs intra-patient variance.
