***04) Labelling Orientation QC***

**curve_labeling_check.py:**
Double-checks that the daughter branches are labeled and oriented sensibly. It reads the cross-section CSVs for curve 1 and curve 2, looks at simple RAS coordinates near the far ends of the curves (how up or to the right they are), decides which daughter is anatomically “higher,” and checks whether left/right alignment looks correct. It writes everything into _curve_orientation_check_all.csv_, including which daughter is higher, the difference between them, and a pass/fail flag for alignment, so you can catch swapped labels or flipped coordinate frames early.

**curve_orientation_check_all.csv:**
Output CSV of the daughter orientation check. For each case/side it lists simple averages taken from the daughter curves’ CSVs (like how up and to the right each daughter is), which daughter came out “higher,” how far apart they were on that measure, and whether left/right alignment looked okay. Review the rows that fail the alignment test.
