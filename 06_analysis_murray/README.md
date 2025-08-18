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
