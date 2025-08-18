import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize_scalar, root_scalar
import os

# -------------------- Config --------------------
input_csv = "diam_summary_full.csv"
output_csv = "murray_output_results2.csv"
skipped_csv = "skipped_models.csv"
qc_plot_dir = "qc_plots"
os.makedirs(qc_plot_dir, exist_ok=True)

# -------------------- Helpers --------------------
def murray_percent_deviation(r_ica, r_mca, r_aca):
    parent_cubed = r_ica ** 3
    child_sum_cubed = r_mca ** 3 + r_aca ** 3
    return 100 * (parent_cubed - child_sum_cubed) / parent_cubed

def empirical_k_loss(k, r_ica, r_mca, r_aca):
    return abs(r_ica**k - (r_mca**k + r_aca**k))

def find_optimal_exponent_minimize(r_ica, r_mca, r_aca):
    result = minimize_scalar(lambda k: empirical_k_loss(k, r_ica, r_mca, r_aca), bounds=(0.5, 10), method='bounded')
    return result.x if result.success else np.nan

def find_optimal_exponent_root(r_ica, r_mca, r_aca):
    def f(k): return r_ica**k - r_mca**k - r_aca**k
    try:
        result = root_scalar(f, bracket=[0.5, 10], method='brentq')
        return result.root if result.converged else np.nan
    except Exception:
        return np.nan

def plot_qc_curve(model_id, r_ica, r_mca, r_aca, k_empirical):
    k_vals = np.linspace(0.5, 10, 500)
    deviations = [empirical_k_loss(k, r_ica, r_mca, r_aca) for k in k_vals]

    plt.figure(figsize=(6, 4))
    plt.plot(k_vals, deviations, label="|Parent^k - (Child1^k + Child2^k)|")
    plt.axvline(k_empirical, color='r', linestyle='--', label=f"minimize k = {k_empirical:.3f}")
    plt.title(f"Murray's Law Fit: {model_id}")
    plt.xlabel("Exponent k")
    plt.ylabel("Deviation")
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(qc_plot_dir, f"{model_id}_murray_qc.png"))
    plt.close()

# -------------------- Main --------------------
df = pd.read_csv(input_csv)
results = []
skipped = []

for _, row in df.iterrows():
    model_id = row.get("Model_ID", "unknown")

    try:
        r_ica = float(row["ICA_CE_Radius"])
        r_mca = float(row["MCA_CE_Radius"])
        r_aca = float(row["ACA_CE_Radius"])

        if min(r_ica, r_mca, r_aca) <= 0 or np.isnan(r_ica) or np.isnan(r_mca) or np.isnan(r_aca):
            raise ValueError("Missing or non-positive radius")

        murray_dev = murray_percent_deviation(r_ica, r_mca, r_aca)
        k_min = find_optimal_exponent_minimize(r_ica, r_mca, r_aca)
        k_root = find_optimal_exponent_root(r_ica, r_mca, r_aca)

        # Plot QC using minimize method k
        plot_qc_curve(model_id, r_ica, r_mca, r_aca, k_min)

        results.append({
            "Model_ID": model_id,
            "ICA_CE_Radius": r_ica,
            "MCA_CE_Radius": r_mca,
            "ACA_CE_Radius": r_aca,
            "Murray_Deviation_Percent": round(murray_dev, 3),
            "Murray_Exponent_k_minimize": round(k_min, 5) if not np.isnan(k_min) else np.nan,
            "Murray_Exponent_k_root": round(k_root, 5) if not np.isnan(k_root) else np.nan
        })

    except Exception as e:
        print(f"⚠️ Skipping model {model_id}: {e}")
        skipped.append({"Model_ID": model_id, "Error": str(e)})

# -------------------- Save Outputs --------------------
pd.DataFrame(results).to_csv(output_csv, index=False)
pd.DataFrame(skipped).to_csv(skipped_csv, index=False)

print(f"✅ Analysis complete. Results saved to '{output_csv}', skipped models to '{skipped_csv}', QC plots to '{qc_plot_dir}/'")
