import os
import csv

# Base paths
data_root = "/Users/miraicgoren/Desktop/TopCoW2024_Data_Release"
vtk_root = os.path.join(data_root, "cow_seg_labelsTr/bifurcation_masks/vtk_surfaces")
output_csv_all = os.path.join(data_root, "processing_log.csv")
output_csv_missing = os.path.join(data_root, "processing_log_missing.csv")

sides = ["L", "R"]
curve_indices = [0, 1, 2]

# Headers
header = [
    "Folder", "Side", "Surface Model", "Centerline Model",
    "Curve 0", "Curve 1", "Curve 2", "CSV 0", "CSV 1", "CSV 2"
]
all_rows = []
missing_rows = []

# Walk through each case
folders = sorted(os.listdir(vtk_root))
for folder in folders:
    folder_path = os.path.join(vtk_root, folder)
    if not os.path.isdir(folder_path):
        continue

    case_id = folder.replace("topcow_", "")

    for side in sides:
        row = [folder, side]
        missing_flag = False

        # Surface
        surface_file = os.path.join(folder_path, f"topcow_{case_id}_{side}_bif.vtk")
        has_surface = os.path.exists(surface_file)
        row.append("✅" if has_surface else "❌")
        if not has_surface: missing_flag = True

        # Centerline
        centerline_prefix = f"centermod_{case_id}_{side}"
        has_centerline = any(f.startswith(centerline_prefix) for f in os.listdir(folder_path))
        row.append("✅" if has_centerline else "❌")
        if not has_centerline: missing_flag = True

        # Curves
        for idx in curve_indices:
            curve_file = os.path.join(folder_path, f"curve_{case_id}_{side} ({idx}).mrk.json")
            has_curve = os.path.exists(curve_file)
            row.append("✅" if has_curve else "❌")
            if not has_curve: missing_flag = True

        # CSVs
        for idx in curve_indices:
            csv_file = os.path.join(folder_path, f"cross_section_{case_id}_{side}_curve{idx}.csv")
            has_csv = os.path.exists(csv_file) and os.path.getsize(csv_file) > 1
            row.append("✅" if has_csv else "❌")
            if not has_csv: missing_flag = True

        all_rows.append(row)
        if missing_flag:
            missing_rows.append(row)

# Save full log
with open(output_csv_all, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(all_rows)

# Save missing-only log
with open(output_csv_missing, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(missing_rows)

print(f"✅ Full log saved to: {output_csv_all}")
print(f"⚠️  Missing-only log saved to: {output_csv_missing}")
