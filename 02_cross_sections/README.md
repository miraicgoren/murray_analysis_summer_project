***2) Cross-sections***

**semi_auto_cross_section_full.py:**
Automates running Slicer’s CrossSectionAnalysis for every case, side, and curve (0 = ICA parent, 1 and 2 = daughters). For each curve it loads the surface and the matching markup file, sets up the module, and you click “Apply” to generate a table of cross-sections along the path. It then saves a CSV named like _cross_section_<case>_<side>_curve{idx}.csv_. It expects consistent file naming for curves and surfaces; if a needed file is missing, it skips that curve and moves on.
