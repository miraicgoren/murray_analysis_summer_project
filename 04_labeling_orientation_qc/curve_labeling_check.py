import os
import pandas as pd

# Config
base_root = "/Users/miraicgoren/Desktop/TopCoW2024_Data_Release/cow_seg_labelsTr/vtk_surfaces"
output_csv = "/Users/miraicgoren/Desktop/TopCoW2024_Data_Release/curve_orientation_check_all.csv"

case_ids = [f"ct_{i:03d}" for i in list(range(1, 91)) + list(range(131, 166))] + \
           [f"mr_{i:03d}" for i in list(range(1, 91)) + list(range(131, 166))]
sides = ["L", "R"]

results = []

for case_id in case_ids:
    for side in sides:
        folder = os.path.join(base_root, f"topcow_{case_id}")
        curve1_file = os.path.join(folder, f"cross_section_{case_id}_{side}_curve1.csv")
        curve2_file = os.path.join(folder, f"cross_section_{case_id}_{side}_curve2.csv")

        if not (os.path.exists(curve1_file) and os.path.exists(curve2_file)):
            continue

        try:
            df1 = pd.read_csv(curve1_file)
            df2 = pd.read_csv(curve2_file)

            if df1.empty or df2.empty:
                continue

            s1 = df1['RAS_S'].iloc[-5:].mean()
            s2 = df2['RAS_S'].iloc[-5:].mean()
            r1 = df1['RAS_R'].iloc[-5:].mean()
            r2 = df2['RAS_R'].iloc[-5:].mean()

            diff_s = abs(s1 - s2)

            superior_idx = 1 if s1 > s2 else 2
            more_right_idx = 1 if r1 > r2 else 2

            if side == "R":
                correct = (superior_idx == 1 and r1 < r2) or (superior_idx == 2 and r2 < r1)
            else:  # L side
                correct = (superior_idx == 1 and r1 > r2) or (superior_idx == 2 and r2 > r1)

            emoji = "✅" if correct else "❌"

            results.append({
                "Case_ID": case_id,
                "Side": side,
                "Curve1_RAS_S_Avg": round(s1, 2),
                "Curve2_RAS_S_Avg": round(s2, 2),
                "Curve1_RAS_R_Avg": round(r1, 2),
                "Curve2_RAS_R_Avg": round(r2, 2),
                "Superior Curve": f"curve{superior_idx}",
                "RAS_S Diff": round(diff_s, 2),
                "RAS_R Alignment Check": emoji
            })

        except Exception as e:
            print(f"Error in {case_id}_{side}: {e}")
            continue

# Export to CSV
df = pd.DataFrame(results)
df.to_csv(output_csv, index=False)
print(f"✅ Orientation check results saved to: {output_csv}")

