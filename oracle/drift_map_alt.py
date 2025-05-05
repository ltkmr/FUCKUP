# drift_map.py
# FUCKUP² Chaos Drift Visualizer (Human-Readable Date Coloring, PCA Variant)

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from sklearn.decomposition import PCA
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

# Step 3: PCA projection (instead of UMAP)
print("🔎 Projecting to 2D with PCA...")
proj = PCA(n_components=2).fit_transform(vectors)

# Step 4: Build DataFrame for plotting
df = pd.DataFrame(proj, columns=["x", "y"])
df["section"] = [m["section"] for m in metadata]
df["date"] = [m["date"] for m in metadata]
df["text"] = [m["text"] for m in metadata]
df["date_numeric"] = df["date"].map(pd.Timestamp.toordinal)

# Step 5: Plot with human-readable date colorbar
plt.figure(figsize=(12, 9))
scatter = plt.scatter(
    df["x"],
    df["y"],
    c=df["date_numeric"],
    cmap="plasma",
    alpha=0.8,
    s=40
)

cbar = plt.colorbar(scatter)
date_ticks = mdates.num2date(sorted(df["date_numeric"].unique()))
cbar.set_ticks([min(df["date_numeric"]), max(df["date_numeric"])])
cbar.set_ticklabels([
    min(df["date"]).strftime("%Y-%m-%d"),
    max(df["date"]).strftime("%Y-%m-%d")
])
cbar.set_label("Date (chronological color scale)")

plt.title("FUCKUP² Drift Map (PCA Projection, Colored by Date)")
plt.xlabel("PCA-1")
plt.ylabel("PCA-2")
plt.tight_layout()

# Step 6: Save to file
output_dir = Path("visuals")
output_dir.mkdir(exist_ok=True)
output_path = output_dir / "chaos_drift_map_pca.png"
plt.savefig(output_path, dpi=300)
print(f"🖼️ PCA drift map saved to: {output_path}")
