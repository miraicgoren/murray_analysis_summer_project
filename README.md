# murray_analysis_summer_project
All the code and analysis for my project on ICA bifurcations and Murray’s Law. Used TopCoW 2024 dataset, semi-automated pipeline with 3D Slicer, extracted vessel diameters, calculated deviation and exponent k, and stat analysis to see how geometry differs across CT and MR.



## Scripts: 

make_bif_masks_full.sh: Builds L/R ICA bifurcation binary masks and converts them to VTK surfaces using headless Slicer

load_surfaces_one_by_one_dimmed.py: Shows each VTK in Slicer at 50% opacity, one at a time. User will manually generate and save the centerlines from each of the loaded surfaces.

semi_auto_cross_section_full.py: Runs CrossSectionAnalysis for curves 0/1/2 per case/side; saves cross_section_*.csv.

check_vtk_surfaces_excel.py: Checks that surface, centerline, curve markups, and cross-section CSVs exist. Writes processing_log.csv + processing_log_missing.csv

check_curves3_4.py: Flags unexpected curve indices (>2). Output message to console.

curve_labeling_check.py: Checks daughter labeling/orientation (ACA vs MCA, L/R) from RAS values. Writes curve_orientation_check_all.csv.

extract_diameters_only.py: Labels ACA/MCA, finds stable spans (low variation regions), averages diameters/radii. Writes diam_summary_full.csv, diam_log_full.txt, diam_failures.csv (+ generates QC plots).

murray_analysis_only.py: Computes Murray deviation and best-fit k from diam_summary_full.csv; writes murray_output_results.csv and skipped_models.csv

murray_final_stats_analysis: R notebook for explaratory data analysis & stats analysis (ANOVA/LME/ICC)


### For extract_diameters_only.py:

You can tune the parameters used to automatically extract the representative diameter values from each branch.

* Smoothing window (moving average on cross-sectional area)

* Variation threshold (max first difference allowed inside span)

* Target span length (number of consecutive samples that will be averaged out)



## Data Overview

This folder holds the imaging data and derived files used by the ICA bifurcation pipeline. Files follow the case naming used in TopCoW (`ct_001`, `mr_131`) with sides `L` / `R`. The data here are inputs for steps 01→06 (masks → surfaces → cross-sections → diameters → Murray analysis)

- `imagesTr/`  
  Raw images for each case (e.g., CT/MR volumes). Used for reference and mask creation.

- `cow_seg_labelsTr/`  
  Segmentation labels and derivatives for each case. Subfolders:
  - `bifurcation_masks/` – left/right ICA bifurcation **binary masks**.
  - `bifurcation_masks/vtk_surfaces/` – exported **surface meshes** (`.vtk`) used by Slicer/VMTK.
  - `centerlines/` – centerline models and markup files (`curve_<case>_<side> (0|1|2).mrk.json`) where:
    - `curve0` = ICA parent, `curve1`/`curve2` = daughter branches.
  - Cross-section CSVs – outputs from Slicer CrossSectionAnalysis: `cross_section_<case>_<side>_curve{0,1,2}.csv`.

### Naming

- **Cases**: `ct_###` or `mr_###`; **Sides**: `L`, `R`
- **Curves**: `curve0` (ICA), `curve1`/`curve2` (daughters)
- **Cross-section data**: `cross_section_<case>_<side>_curve{idx}.csv`
- **Model ID** downstream: `<case>_<side>` (`mr_042_L`)

## How it’s used in the pipeline

1. Masks in `cow_seg_labelsTr/bifurcation_masks/` are converted to **VTK surfaces**.
2. Surfaces + curve markups drive CrossSectionAnalysis → **cross_section_*.csv**.
3. Cross-section CSVs feed diameter extraction → **diam_summary_full.csv**.
4. The summary feeds Murray analysis → **murray_output_results.csv**.

