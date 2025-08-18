import os
import re

# Base directory containing bifurcation subfolders
base_dir = "/Users/miraicgoren/Desktop/TopCoW2024_Data_Release/cow_seg_labelsTr/vtk_surfaces"

# Regular expression to match curve files and extract index
curve_pattern = re.compile(r"curve_(.+?)_(L|R) \((\d+)\)\.mrk\.json")

# Collect problematic curves
unexpected_curves = []

# Traverse folders
for folder in os.listdir(base_dir):
    folder_path = os.path.join(base_dir, folder)
    if not os.path.isdir(folder_path):
        continue

    for filename in os.listdir(folder_path):
        match = curve_pattern.match(filename)
        if match:
            curve_index = int(match.group(3))
            if curve_index > 2:
                unexpected_curves.append((folder, filename))

# Output result
if unexpected_curves:
    print("⚠️ Unexpected curves found with index > 2:\n")
    for folder, filename in unexpected_curves:
        print(f"- {folder}/{filename}")
else:
    print("✅ No curves beyond index (2) were found.")
