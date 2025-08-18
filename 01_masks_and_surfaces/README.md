***01 – Masks & surfaces***

**make_bif_masks_full.sh** – builds all the left/right ICA bifurcation binary masks from your labeled volumes and exports VTK surface models via headless 3D Slicer. Iterates through all CT/MR cases and both sides, generates a tiny Slicer Python script on the fly, and saves surfaces under .../bifurcation_masks/vtk_surfaces/. Requires FSL + Slicer on PATH; adjust the dataset root path if you’ve moved the TopCoW folder.

**load_surfaces_one_by_one_dimmed.py** – A small Slicer helper to visually quality check the exported VTK surfaces. Loads one model at a time at ~0.5 opacity, hides others, and waits for a “Continue” click so you can step through the set. Purely visual (no outputs); run inside Slicer’s Python console and update the folder path as needed.
