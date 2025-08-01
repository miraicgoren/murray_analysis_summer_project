import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize_scalar
from datetime import datetime

# ------------------ Config ------------------

output_dir = os.path.expanduser("~/Desktop/TopCoW2024_Data_Release")
os.makedirs(output_dir, exist_ok=True)

base_root = os.path.join(output_dir, "cow_seg_labelsTr", "vtk_surfaces")
case_ids = [f"ct_{i:03d}" for i in list(range(1, 91)) + list(range(131, 166))] + \
           [f"mr_{i:03d}" for i in list(range(1, 91)) + list(range(131, 166))]
sides = ["L", "R"]
output_csv = os.path.join(output_dir, "diam_summary_full.csv")
log_file = os.path.join(output_dir, "diam_log_full.txt")
failures_csv_path = os.path.join(output_dir, "diam_failures.csv")

# ------------------ Helper Functions ------------------

def smooth_series(series, window_size=5):
    return series.rolling(window=window_size, center=True, min_periods=1).mean()

def find_stabilized_index(area_series, threshold=0.08, window_size=8, stable_span=20, min_span=2, step=2):
    smoothed = smooth_series(area_series, window_size)
    diffs = smoothed.diff().abs()
    for span in range(stable_span, min_span - 1, -step):
        for i in range(len(diffs) - span):
            if diffs[i:i+span].max() < threshold:
                return i, span
    return None, None

def extract_stabilized_points(df, vessel_type):
    df_use = df[::-1].reset_index(drop=True) if vessel_type == 'ICA' else df.reset_index(drop=True)
    idx, actual_span = find_stabilized_index(df_use['Cross-section area'])
    if idx is None:
        return None, None, None
    selected = df_use.iloc[idx:idx+actual_span].copy()
    selected = selected[::-1].reset_index(drop=True) if vessel_type == 'ICA' else selected
    original_idx = len(df) - (idx + actual_span) if vessel_type == 'ICA' else idx
    return selected, original_idx, actual_span

def classify_aca_mca(df1, df2, side, n=5):
    r1 = df1['RAS_R'].iloc[-n:].mean()
    r2 = df2['RAS_R'].iloc[-n:].mean()

    if side == "L":
        return ('ACA', 'MCA') if r1 > r2 else ('MCA', 'ACA')
    else:  # side == "R"
        return ('ACA', 'MCA') if r1 < r2 else ('MCA', 'ACA')

def generate_qc_plot(df, start_idx, span_len, vessel_type, outpath):
    end_idx = start_idx + span_len
    start_dist = df['Distance'].iloc[start_idx]
    end_dist = df['Distance'].iloc[end_idx - 1]
    plt.figure(figsize=(8, 4))
    plt.plot(df['Distance'], df['Cross-section area'], label='Cross-sectional area')
    plt.axvline(start_dist, color='green', linestyle='--', label='Stable Start')
    plt.axvline(end_dist, color='red', linestyle='--', label='Stable End')
    plt.axvspan(start_dist, end_dist, color='green', alpha=0.2)
    plt.title(f'{vessel_type} - Stabilized Region QC')
    plt.xlabel('Distance (mm)')
    plt.ylabel('Cross-section area (mm²)')
    plt.legend()
    plt.tight_layout()
    plt.savefig(outpath)
    plt.close()

# ------------------ Main Loop ------------------

summary_rows = []
log_lines = [f"=== Murray’s Law Adaptive Analysis Log ===\n{datetime.now()}\n"]
count_success = 0
count_failed = 0

for case_id in case_ids:
    for side in sides:
        folder = os.path.join(base_root, f"topcow_{case_id}")

        ica_file = os.path.join(folder, f"cross_section_{case_id}_{side}_curve0.csv")
        b1_file  = os.path.join(folder, f"cross_section_{case_id}_{side}_curve1.csv")
        b2_file  = os.path.join(folder, f"cross_section_{case_id}_{side}_curve2.csv")

        try:
            if not all(map(os.path.exists, [ica_file, b1_file, b2_file])):
                log_lines.append(f"❌ Missing curves for {case_id} {side}")
                count_failed += 1
                continue

            ica_df = pd.read_csv(ica_file)
            b1_df = pd.read_csv(b1_file)
            b2_df = pd.read_csv(b2_file)

            aca_label, mca_label = classify_aca_mca(b1_df, b2_df, side)

            if aca_label == 'ACA':
                aca_df = b1_df
                mca_df = b2_df
            else:
                aca_df = b2_df
                mca_df = b1_df

            curve_data = {
                0: ('ICA', ica_df),
                1: ('ACA', aca_df),
                2: ('MCA', mca_df),
            }

            all_outputs = []
            failed = False
            branch_span_info = []
            span_tracker = {}

            for idx, (vessel_type, df) in curve_data.items():
                extracted, start_idx, span = extract_stabilized_points(df, vessel_type)
                if extracted is None:
                    log_lines.append(f"⚠️ No stable region for {case_id} {side} {vessel_type}")
                    failed = True
                    break

                extracted['Branch'] = vessel_type
                extracted['Curve_Index'] = idx
                extracted['RAS_R'] = df['RAS_R'].iloc[extracted.index].values
                extracted['RAS_A'] = df['RAS_A'].iloc[extracted.index].values
                extracted['RAS_S'] = df['RAS_S'].iloc[extracted.index].values
                all_outputs.append(extracted)

                plot_path = os.path.join(folder, f"{side}_plot_{vessel_type}.png")
                generate_qc_plot(df, start_idx, span, vessel_type, plot_path)
                branch_span_info.append(f"{vessel_type}:{span}")
                span_tracker[f"{vessel_type}_Span"] = span

            if failed:
                count_failed += 1
                continue

            final_df = pd.concat(all_outputs, ignore_index=True)
            summary = {'Model_ID': f"{case_id}_{side}", **span_tracker}

            for branch in ['ICA', 'ACA', 'MCA']:
                sub = final_df[final_df['Branch'] == branch]
                mean_ce = sub['Diameter (CE)'].mean()
                mean_mis = sub['Diameter (MIS)'].mean()
                ce_r = mean_ce / 2
                mis_r = mean_mis / 2
                roundness = mis_r / ce_r if ce_r else np.nan

                summary[f'{branch}_Mean_CE_Diameter'] = mean_ce
                summary[f'{branch}_Mean_MIS_Diameter'] = mean_mis
                summary[f'{branch}_CE_Radius'] = ce_r
                summary[f'{branch}_Roundness_Index'] = roundness

            rp = summary['ICA_CE_Radius']
            r1 = summary['ACA_CE_Radius']
            r2 = summary['MCA_CE_Radius']

            summary_rows.append(summary)
            log_lines.append(f"✅ Processed {case_id} {side} | Stable spans: {', '.join(branch_span_info)}")
            count_success += 1

        except Exception as e:
            log_lines.append(f"❌ Error in {case_id} {side}: {str(e)}")
            count_failed += 1

# ------------------ Output ------------------

pd.DataFrame(summary_rows).to_csv(output_csv, index=False)
with open(log_file, "w") as f:
    f.write("\n".join(log_lines))

print(f"\n✅ Done. Summary saved to: {output_csv}")
print(f"📄 Log file saved to: {log_file}")
print(f"\n📊 Total processed successfully: {count_success}")
print(f"❌ Total failed/skipped: {count_failed}")

# ------------------ Summarize Failures ------------------

failure_records = []

for line in log_lines:
    if line.startswith("❌ Missing curves for"):
        parts = line.split("for")[1].strip().split()
        case_id, side = parts[0], parts[1]
        failure_records.append({'Case_ID': case_id, 'Side': side, 'Reason': 'Missing curves'})

    elif line.startswith("⚠️ No stable region"):
        parts = line.split("for")[1].strip().split()
        case_id, side, vessel = parts[0], parts[1], parts[2]
        failure_records.append({'Case_ID': case_id, 'Side': side, 'Reason': f'No stable region in {vessel}'})

    elif line.startswith("❌ Error in"):
        parts = line.split("in")[1].strip().split(":")[0].split()
        case_id, side = parts[0], parts[1]
        failure_records.append({'Case_ID': case_id, 'Side': side, 'Reason': 'Unhandled exception'})

pd.DataFrame(failure_records).to_csv(failures_csv_path, index=False)
print(f"\n🛑 Failure details saved to: {failures_csv_path}")
