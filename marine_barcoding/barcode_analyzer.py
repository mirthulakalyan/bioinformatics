from Bio import SeqIO
from Bio.SeqUtils import gc_fraction
import pandas as pd
import matplotlib.pyplot as plt

# 1. LOAD THE REAL NCBI DATASET FILE
raw_records = list(SeqIO.parse("sequence.fasta", "fasta"))
print(f"Loaded {len(raw_records)} raw sequences from sequence.fasta")

# 2. DATA CLEANING (Filtering out messy or partial reads)
clean_records = []
for record in raw_records:
    seq_str = str(record.seq).upper()
    if "N" not in seq_str and 600 <= len(seq_str) <= 700:
        clean_records.append(record)

print(f"Kept {len(clean_records)} high-quality sequences after filtering out 'N's and partial reads.")

# 3. EXTRACT CLEAN SPECIES NAMES & CALCULATE GC CONTENT
data = []
for record in clean_records:
    clean_desc = record.description.replace("UNVERIFIED: ", "")
    parts = clean_desc.split()
    species_name = f"{parts[1]} {parts[2]}" if len(parts) >= 3 else record.id
    
    data.append({
        "Accession": record.id,
        "Species": species_name,
        "Length (bp)": len(record.seq),
        "GC Content (%)": round(gc_fraction(record.seq) * 100, 2)
    })

df = pd.DataFrame(data)

# Group by species to calculate average GC content and sample count
summary = df.groupby("Species").agg(
    Sample_Count=("Accession", "count"),
    Avg_Length=("Length (bp)", "mean"),
    Avg_GC_Percent=("GC Content (%)", "mean")
).round(2).reset_index()

# Keep the top 5 most common tuna species in the dataset
top_species = summary.sort_values(by="Sample_Count", ascending=False).head(5)

print("\n--- Real Dataset Species Summary ---")
print(top_species.to_string(index=False))

# 4. GENERATE PORTFOLIO VISUALIZATION
plt.figure(figsize=(10, 5))
bars = plt.bar(top_species["Species"], top_species["Avg_GC_Percent"], color="#0077b6")
plt.title("Average COI GC Content Across Real Tuna Species (NCBI Dataset)", fontweight="bold")
plt.ylabel("Average GC Content (%)")
plt.ylim(40, 52)
plt.xticks(rotation=15, ha="right")
plt.grid(axis="y", linestyle="--", alpha=0.5)

for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 0.3, f"{yval}%", ha="center", fontsize=10)

plt.tight_layout()
plt.savefig("real_dataset_gc_chart.png", dpi=300)
print("\nSaved chart to real_dataset_gc_chart.png!")