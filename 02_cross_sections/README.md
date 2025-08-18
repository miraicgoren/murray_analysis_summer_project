***2) Cross-sections***

**semi_auto_cross_section_full.py:**
Semi-automates Slicer’s CrossSectionAnalysis for each case/side/curve {0,1,2}. For every model, it loads the surface and the corresponding centerline/curve markup, preps the module UI, and lets you click Apply (keeps you in control of parameters). It then saves cross_section_<case>_<side>_curve{idx}.csv capturing area and coordinates at regular steps along the path. The script expects consistent file names for markups (e.g., curve indices 0/1/2) and surfaces; if something is missing, that curve is skipped and noted in the console. Use this to produce all raw cross-section CSVs that downstream steps consume.
