***01 – Masks & surfaces***

**make_bif_masks_full.sh**: 
Batch-builds left/right ICA-bifurcation binary masks from your labeled volumes and exports VTK surface models via headless 3D Slicer. It loops over all CT/MR cases and both sides, assembles per-side masks (using FSL/ImageMath), then launches Slicer without a GUI to convert each mask to a watertight surface. Paths to the dataset root and Slicer binary are set in the script and must match your machine. The script prints progress for each exported model, making failures easy to spot. Outputs land under cow_seg_labelsTr/bifurcation_masks/vtk_surfaces/ with consistent case/side naming .

**load_surfaces_one_by_one_dimmed.py** – A small Slicer visualization helper for quick QA of exported VTK surfaces. It iterates models in your surfaces folder, loads one at a time, sets opacity to ~0.5 so edges and overlaps are visible, hides everything else, then waits for a Continue click before advancing. Use it to catch obvious geometry issues (holes, flips, wrong side) before cross-sectioning. It writes no files and assumes you run it inside Slicer’s Python console. Update the folder path near the top to your local surfaces directory.
