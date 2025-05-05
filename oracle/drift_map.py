# drift_map.py
# FUCKUP² Chaos Drift Visualizer (PCA & UMAP Combined, Colored by Date, Labeled by Section)

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from sklearn.decomposition import PCA
import umap
from oracle.vectorizer import embed_text
from oracle.qdrant_integration import get_client, COLLECTION_NAME
import pandas as pd
import time
from pathlib import Path

# Step 1: Fetch entries from Chaos Stockpile
client = get_client()

print("📥 Fetching stored divinations from Qdrant...")
points = client.scroll(collection_name=COLLECTION_NAME, scroll_filter=None, with_payload=True, with_vectors=False, limit=10000)[0]

# Step 2: Parse data
texts = []
metadata = []

for point in points:
    payload = point.payload
    content = payload.get("content")
    if not content:
        continue

    date_str = payload.get("date", "unknown")
    try:
        date_obj = pd.to_datetime(date_str, errors="coerce")
    except:
        date_obj = pd.NaT

    if pd.isna(date_obj):
        continue  # skip entries with invalid dates

    texts.append(content)
    metadata.append({
        "date": date_obj,
        "section": payload.get("section", "unknown"),
        "hexagram": payload.get("hexagram"),
        "text": content[:200]
    })

if not texts:
    print("⚠️ No embeddable entries with valid dates found.")
    exit(0)

print(f"🔍 Embedding {len(texts)} entries (cached)...")
start_time = time.time()
vectors = embed_text(texts)
print(f"⏱️ Embedding complete in {time.time() - start_time:.2f} seconds.")

# Convert metadata to DataFrame
df = pd.DataFrame(metadata)
df["date_numeric"] = df["date"].map(pd.Timestamp.toordinal)

# Step 3: Project using both PCA and UMAP
print("🔎 Projecting with PCA...")
df[["pca_x", "pca_y"]] = PCA(n_components=2).fit_transform(vectors)

print("🌀 Projecting with UMAP...")
df[["umap_x", "umap_y"]] = umap.UMAP(n_neighbors=15, min_dist=0.1, metric='cosine').fit_transform(vectors)

# Step 4: Plot and save PCA
plt.figure(figsize=(12, 9))
pca_scatter = plt.scatter(
    df["pca_x"], df["pca_y"], c=df["date_numeric"], cmap="plasma", alpha=0.8, s=40
)
cbar = plt.colorbar(pca_scatter)
cbar.set_ticks([min(df["date_numeric"]), max(df["date_numeric"])])
cbar.set_ticklabels([
    min(df["date"]).strftime("%Y-%m-%d"),
    max(df["date"]).strftime("%Y-%m-%d")
])
cbar.set_label("Date (chronological color scale)")

for _, row in df.iterrows():
    plt.text(row["pca_x"], row["pca_y"], ("R" if row["section"] == "advice" else row["section"][0].upper()), fontsize=7, alpha=0.6)

plt.title("FUCKUP² Drift Map (PCA Projection)")
plt.xlabel("PCA-1")
plt.ylabel("PCA-2")
plt.tight_layout()
Path("visuals").mkdir(exist_ok=True)
from datetime import datetime
stamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
pca_path = f"visuals/{stamp}_chaos_drift_map_pca_labeled.png"
plt.savefig(pca_path, dpi=300)
print(f"🖼️ PCA drift map saved to: {pca_path}")

# Step 5: Plot and save UMAP
plt.figure(figsize=(12, 9))
umap_scatter = plt.scatter(
    df["umap_x"], df["umap_y"], c=df["date_numeric"], cmap="viridis", alpha=0.8, s=40
)
cbar = plt.colorbar(umap_scatter)
cbar.set_ticks([min(df["date_numeric"]), max(df["date_numeric"])])
cbar.set_ticklabels([
    min(df["date"]).strftime("%Y-%m-%d"),
    max(df["date"]).strftime("%Y-%m-%d")
])
cbar.set_label("Date (chronological color scale)")

for _, row in df.iterrows():
    plt.text(row["umap_x"], row["umap_y"], row["section"][0].upper(), fontsize=7, alpha=0.6)

plt.title("FUCKUP² Drift Map (UMAP Projection)")
plt.xlabel("UMAP-X")
plt.ylabel("UMAP-Y")
plt.tight_layout()
umap_path = f"visuals/{stamp}_chaos_drift_map_umap_labeled.png"
plt.savefig(umap_path, dpi=300)
print(f"🖼️ UMAP drift map saved to: {umap_path}")
