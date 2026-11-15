#Data Visualization
#Mock theoretical data --> .png / .pdf

import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# Set a clean, academic style for the presentation slides
sns.set_theme(style="whitegrid", context="talk")

def load_or_simulate_metrics(csv_path="data/metrics_output.csv"):
    """
    Loads the computed metrics CSV if it exists. 
    Injects placeholder expectations for the human datasets that are still pending.
    """
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
    else:
        # Fallback dummy data so you can generate slides tonight
        print("Metrics CSV not found. Generating combined synthetic & expected data...")
        data = [
            {"Dataset": "Uniform Random (1Mb)", "Class": "Control", "Mean_LCP": 14, "Max_LCP": 25, "BWT_Runs": 750000},
            {"Dataset": "Synthetic Diverged (10%)", "Class": "Synthetic", "Mean_LCP": 50, "Max_LCP": 300, "BWT_Runs": 600000},
            {"Dataset": "Synthetic Exact Repeat", "Class": "Synthetic", "Mean_LCP": 500000, "Max_LCP": 999000, "BWT_Runs": 10000},
            {"Dataset": "Alu/SINE (Expected)", "Class": "Interspersed", "Mean_LCP": 300, "Max_LCP": 1000, "BWT_Runs": 450000},
            {"Dataset": "L1/LINE (Expected)", "Class": "Interspersed", "Mean_LCP": 800, "Max_LCP": 6000, "BWT_Runs": 350000},
            {"Dataset": "CenSat Alpha (Expected)", "Class": "Tandem", "Mean_LCP": 15000, "Max_LCP": 50000, "BWT_Runs": 50000},
            {"Dataset": "Segmental Duplication (Expected)", "Class": "SegDup", "Mean_LCP": 100, "Max_LCP": 85000, "BWT_Runs": 550000}
        ]
        df = pd.DataFrame(data)
    return df

def plot_lcp_signatures(df, output_dir):
    """Plot 1: Scatter plot of the data architecture (Mean vs Max LCP)"""
    plt.figure(figsize=(10, 6))
    
    ax = sns.scatterplot(
        data=df, x="Mean_LCP", y="Max_LCP", hue="Class", style="Class", 
        s=200, palette="Set1", edgecolor="black", linewidth=1.5
    )
    
    # Log scale is critical because LCP ranges from ~10 bp to 1,000,000 bp
    ax.set_xscale("log")
    ax.set_yscale("log")
    
    plt.title("Architectural Signatures of Genomic Repeats", pad=20, fontweight="bold")
    plt.xlabel("Mean LCP (Log Scale)")
    plt.ylabel("Maximum LCP (Log Scale)")
    
    # Move legend outside the plot for cleaner presentation
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "plot_1_lcp_signatures.png"), dpi=300)
    plt.close()

def plot_expected_scaling(output_dir):
    """Plot 2: Theoretical Time Scaling for the algorithms based on 1, 2, 4 Mb targets"""
    sizes_mb = np.array([1, 2, 4])
    
    # Mock mathematical scaling based on your hypotheses
    # SA-IS: Strictly linear O(N)
    time_sais = sizes_mb * 1.5 
    
    # Prefix Doubling: O(N * log(Max_LCP)). Assuming a highly repetitive sequence (large penalty)
    time_pd = sizes_mb * (1.2 * np.log2(50000) / 10) 
    
    # Naive: O(N * Mean_LCP). Exponential blow-up on repeats.
    time_naive = (sizes_mb ** 2) * 2 

    df_scaling = pd.DataFrame({
        "Sequence Size (Mb)": np.tile(sizes_mb, 3),
        "Wall Time (Seconds)": np.concatenate([time_sais, time_pd, time_naive]),
        "Algorithm": ["SA-IS (O(N))"]*3 + ["Prefix Doubling (O(N log(LCP)))"]*3 + ["Naive Sort (O(N * Mean LCP))"]*3
    })

    plt.figure(figsize=(9, 6))
    sns.lineplot(
        data=df_scaling, x="Sequence Size (Mb)", y="Wall Time (Seconds)", 
        hue="Algorithm", marker="o", linewidth=3, markersize=10
    )
    
    plt.title("Hypothesized Algorithm Scaling on Repetitive DNA", pad=20, fontweight="bold")
    plt.xticks([1, 2, 4])
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "plot_2_time_scaling.png"), dpi=300)
    plt.close()

def plot_expected_memory(output_dir):
    """Plot 3: Theoretical Peak Memory (RSS) Footprint"""
    # Expected memory multipliers relative to input size N (bytes)
    # Naive: ~5N, Prefix Doubling: ~9N, SA-IS: ~15N to 20N (due to deep recursion arrays)
    algorithms = ["Naive Sort", "Prefix Doubling", "SA-IS"]
    memory_multiplier = [5, 9, 18]
    
    plt.figure(figsize=(8, 6))
    ax = sns.barplot(x=algorithms, y=memory_multiplier, palette="viridis")
    
    plt.title("Expected Peak Memory Tradeoff", pad=20, fontweight="bold")
    plt.ylabel("Peak RAM Multiplier (Relative to N)")
    plt.axhline(y=1, color='red', linestyle='--', label="Input Size (1x)")
    
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "plot_3_memory_tradeoff.png"), dpi=300)
    plt.close()

def main():
    output_dir = "presentation_plots"
    os.makedirs(output_dir, exist_ok=True)
    
    print("Loading metrics...")
    df_metrics = load_or_simulate_metrics()
    
    print("Generating Plot 1: LCP Signatures...")
    plot_lcp_signatures(df_metrics, output_dir)
    
    print("Generating Plot 2: Time Scaling...")
    plot_expected_scaling(output_dir)
    
    print("Generating Plot 3: Memory Footprints...")
    plot_expected_memory(output_dir)
    
    print(f"Done! Slides are ready in the '{output_dir}' directory.")

if __name__ == "__main__":
    main()
    