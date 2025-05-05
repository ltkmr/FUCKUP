# import_archive.py
# FUCKUP² Ritual Archive Importer (Segmented Version with Deterministic IDs)

import os
import re
import hashlib
from pathlib import Path
from oracle.vectorizer import embed_text
from oracle.qdrant_integration import store_divination
from qdrant_client.models import PointStruct

ARCHIVE_PATH = Path("archive")  # Adjust if needed


def extract_between(text, start_tag, end_tag):
    pattern = re.compile(re.escape(start_tag) + r"(.*?)" + re.escape(end_tag), re.DOTALL)
    match = pattern.search(text)
    return match.group(1).strip() if match else ""

def parse_hexagram(text):
    match = re.search(r"Hexagram #?(\d+):\s+(.+?)\s", text)
    if match:
        return int(match.group(1)), match.group(2)
    return None, None

def parse_date(text):
    match = re.search(r"(\d{4}-\d{2}-\d{2})", text)
    return match.group(1) if match else None

def generate_id(file_name, section):
    raw = f"{file_name}_{section}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()

def store_segment(section_name, content, date, hexagram_num, hexagram_name, file_name):
    if not content:
        return

    vector = embed_text(content)
    payload = {
        "section": section_name,
        "content": content,
        "date": date,
        "hexagram": hexagram_num,
        "hexagram_name": hexagram_name,
        "oracle_excerpt": content[:300],
        "source_file": file_name
    }
    uid = generate_id(file_name, section_name)
    point = PointStruct(id=uid, vector=vector, payload=payload)
    print(f"→ Storing [{section_name}] from {file_name} (ID: {uid[:8]}...)")
    store_divination(vector, payload, point_id=uid)

def import_one_file(file_path):
    with open(file_path, encoding="utf-8") as f:
        raw = f.read()

    date = parse_date(raw)
    hexagram_num, hexagram_name = parse_hexagram(raw)

    analysis = extract_between(raw, "<<<ANALYSIS_START>>>", "<<<ANALYSIS_COMPLETE>>>")
    oracle = extract_between(raw, "<<<INTERPRETATION_START>>>", "<<<INTERPRETATION_COMPLETE>>>")
    advice = extract_between(raw, "<<<RECOMMANDATION_START>>>", "<<<RECOMMANDATION_COMPLETE>>>")

    store_segment("analysis", analysis, date, hexagram_num, hexagram_name, file_path.name)
    store_segment("oracle", oracle, date, hexagram_num, hexagram_name, file_path.name)
    store_segment("advice", advice, date, hexagram_num, hexagram_name, file_path.name)

def import_all():
    files = sorted(ARCHIVE_PATH.glob("*.txt"))
    print(f"Found {len(files)} archive files.")

    for file in files:
        try:
            import_one_file(file)
        except Exception as e:
            print(f"⚠️ Error importing {file.name}: {e}")

if __name__ == "__main__":
    import_all()
