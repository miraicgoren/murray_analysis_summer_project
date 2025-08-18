***03) Input QC***

**check_vtk_surfaces_excel.py:**
To check if we have everything needed to progress. For each case and side it looks for the surface model, the centerline model, the three curve markups (0/1/2), and the three cross-section CSVs (0/1/2). It writes a full report called *processing_log.csv* with ✅/❌ for each item, and a shorter *processing_log_missing.csv* that lists only the rows with something missing. Use these tables to see exactly what needs to be created or fixed before you extract diameters.

**check_curves3_4.py:**
Check scans your curve markup files and flags any curve indices higher than 2, which usually means a stray or duplicate curve that could confuse later steps. It prints a short list to the console and doesn’t write any files. Rename the script to remove the colon so it behaves well on all systems.

**processing_log.csv:**
Report from check_vtk_surfaces_excel.py. Each row is a case/side, and the columns show whether the surface, centerline, curve markups (0/1/2), and cross-section CSVs (0/1/2) exist. Sort by any ❌ column to see what you needs to be fixed before running the diameter extractor script.

**processing_log_missing.csv:**
Filtered version of the processing log that keeps only rows with at least one ❌ (summary)
