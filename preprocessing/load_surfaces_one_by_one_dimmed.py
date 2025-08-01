import os
import slicer
import slicer.util
import qt

# Set your surface model root folder
surface_root = "/Users/miraicgoren/Desktop/TopCoW2024_Data_Release/cow_seg_labelsTr/bifurcation_masks/vtk_surfaces"

# Set up non-blocking dialog
dialog = qt.QDialog()
dialog.setWindowTitle("Continue to Next Surface")
layout = qt.QVBoxLayout()
dialog.setLayout(layout)
label = qt.QLabel("Current surface loaded and dimmed.\nClick 'Continue' to load the next one.")
layout.addWidget(label)
button = qt.QPushButton("Continue")
layout.addWidget(button)
dialog.setModal(False)
button.clicked.connect(lambda: dialog.done(1))

# Loop through folders and files
for subfolder in sorted(os.listdir(surface_root)):
    subpath = os.path.join(surface_root, subfolder)
    if not os.path.isdir(subpath):
        continue

    for filename in sorted(os.listdir(subpath)):
        if not filename.endswith(".vtk"):
            continue

        vtk_path = os.path.join(subpath, filename)
        print(f"\n=== Loading: {filename} ===")
        
        # Load the model
        modelNode = slicer.util.loadModel(vtk_path)
        if modelNode is None:
            print(f"❌ Failed to load: {filename}")
            continue

        # Rename for clarity and ensure display node
        modelNode.SetName(filename)
        modelNode.CreateDefaultDisplayNodes()
        modelNode.GetDisplayNode().SetOpacity(0.5)
        modelNode.GetDisplayNode().SetVisibility(True)

        # Hide all others
        for other in slicer.util.getNodesByClass("vtkMRMLModelNode"):
            if other != modelNode and other.GetDisplayNode():
                other.GetDisplayNode().SetVisibility(False)

        # Show dialog and wait for "Continue"
        dialog.setResult(0)
        dialog.show()
        slicer.app.processEvents()
        while dialog.result() == 0:
            slicer.app.processEvents()
