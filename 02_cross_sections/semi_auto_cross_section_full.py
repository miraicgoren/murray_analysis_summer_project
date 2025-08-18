import os
import slicer
import slicer.util
import qt

# Define case IDs — ct starts from 042 now
case_ids = [f"ct_{i:03d}" for i in list(range(1, 91)) + list(range(131, 166))] + \
           [f"mr_{i:03d}" for i in list(range(1, 91)) + list(range(131, 166))]
sides = ["L", "R"]
curve_indices = [0, 1, 2]

# Path to TopCoW2024 bifurcation surface data
base_root = "/Users/miraicgoren/Desktop/TopCoW2024_Data_Release/cow_seg_labelsTr/bifurcation_masks/vtk_surfaces"

# Reusable dialog to prompt user to press "Apply"
dialog = qt.QDialog()
dialog.setWindowTitle("Action Required")
dialog_layout = qt.QVBoxLayout()
dialog.setLayout(dialog_layout)
label = qt.QLabel("Press 'Apply' in CrossSectionAnalysis, then click 'Continue'.")
dialog_layout.addWidget(label)
button = qt.QPushButton("Continue")
dialog_layout.addWidget(button)
dialog.setModal(False)
button.clicked.connect(lambda: dialog.done(1))

# Make sure module is loaded
slicer.util.selectModule("CrossSectionAnalysis")
slicer.app.processEvents()

# Access or create the parameter node
try:
    paramNode = slicer.util.getNode("CrossSectionAnalysis")
except slicer.util.MRMLNodeNotFoundException:
    paramNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLScriptedModuleNode", "CrossSectionAnalysis")

# === MAIN LOOP ===
for case_id in case_ids:
    topcow_id = f"topcow_{case_id}"
    base_folder = os.path.join(base_root, topcow_id)

    if not os.path.exists(base_folder):
        print(f"⚠️ Folder missing: {base_folder}")
        continue

    for side in sides:
        surface_path = os.path.join(base_folder, f"{topcow_id}_{side}_bif.vtk")
        if not os.path.exists(surface_path):
            print(f"⚠️ Surface missing: {surface_path}")
            continue

        print(f"\n=== Processing {case_id.upper()} {side} bifurcation ===")

        try:
            surfaceNode = slicer.util.loadModel(surface_path)
            paramNode.SetNodeReferenceID("InputSurface", surfaceNode.GetID())  # ✅ Auto-set surface input
        except Exception as e:
            print(f"❌ Error loading surface: {e}")
            continue

        # Loop over 3 curve indices
        for idx in curve_indices:
            curve_file = f"curve_{case_id}_{side} ({idx}).mrk.json"
            curve_path = os.path.join(base_folder, curve_file)

            if not os.path.exists(curve_path):
                print(f"⚠️ Curve missing: {curve_path}")
                continue

            print(f"* Loading curve: {curve_file}")
            try:
                curveNode = slicer.util.loadMarkups(curve_path)
                paramNode.SetNodeReferenceID("InputCenterline", curveNode.GetID())  # ✅ Auto-set curve input
            except Exception as e:
                print(f"❌ Error loading curve: {e}")
                continue

            # Create and assign output table
            output_table_name = f"cross_section_{case_id}_{side}_curve{idx}"
            output_csv_path = os.path.join(base_folder, f"{output_table_name}.csv")
            output_table = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTableNode", output_table_name)
            paramNode.SetNodeReferenceID("OutputTable", output_table.GetID())  # ✅ Auto-set output table

            slicer.app.processEvents()

            # Prompt user for Apply → Continue
            dialog.setResult(0)
            dialog.show()
            slicer.app.processEvents()
            while dialog.result() == 0:
                slicer.app.processEvents()

            # Save CSV
            success = slicer.util.saveNode(output_table, output_csv_path)
            if success:
                print(f"✓ Saved: {output_csv_path}")
            else:
                print(f"❌ Failed to save: {output_csv_path}")
