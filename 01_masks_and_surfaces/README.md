***01 – Masks & surfaces***

**make_bif_masks_full.sh**: 
Builds left and right ICA bifurcation masks from your labeled images and converts those masks into 3D VTK surface files using 3D Slicer in headless mode. It loops through all CT/MR cases and both sides, runs basic image math to make a clean binary mask for the bifurcation, then calls Slicer to turn each mask into a watertight surface. You need FSL and Slicer installed and the paths in the script set to your dataset and Slicer executable. When it finishes, you’ll have one VTK surface per case/side saved under .../bifurcation_masks/vtk_surfaces/, and the console output will tell you what succeeded or failed.

**load_surfaces_one_by_one_dimmed.py** 
A small Slicer helper that opens each VTK surface one at a time so you can visually check them. It loads the current model, sets it to 50% opacity, hides the others, and waits for you to click a “Continue” button to move on. It doesn’t save anything; it just helps you spot obvious problems like flipped models, holes, or wrong sides before you go further. Run it inside Slicer’s Python console after updating the folder path at the top of the script.
