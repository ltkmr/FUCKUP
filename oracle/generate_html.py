import os
import sys
import re

# --- Canonical Path Handling ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ARCHIVE_PATH = os.path.join(SCRIPT_DIR, "..", "archive")
HTML_OUTPUT_PATH = os.path.join(SCRIPT_DIR, "..", "web")

# --- Step 1: Locate latest archive file ---

def find_latest_timestamp(archive_path=ARCHIVE_PATH):
    """Finds the newest archive file and extracts the timestamp."""
    if not os.path.isdir(archive_path):
        print(f"Error: Archive path '{archive_path}' not found.")
        sys.exit(1)

    txt_files = [f for f in os.listdir(archive_path) if f.endswith('.txt')]
    if not txt_files:
        print(f"Error: No .txt files found in '{archive_path}'.")
        sys.exit(1)

    txt_files.sort()
    latest_file = txt_files[-1]
    timestamp_raw = latest_file.replace('.txt', '')
    timestamp = timestamp_raw.replace('-', '_')  # Format: YYYY-MM-DD_HHMMSS

    print(f"[INFO] Using timestamp from archive: {timestamp}")
    return timestamp

# --- Step 2: Extract divinatory metadata from archive file ---

def extract_hexagram_data_from_archive(timestamp):
    archive_filename = timestamp.replace('_', '-') + ".txt"
    archive_path = os.path.join(ARCHIVE_PATH, archive_filename)

    try:
        with open(archive_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Match the hexagram line
        match = re.search(r"Today's Hexagram #(\d+): (.+?)\s+[\u4DC0-\u4DFF]", content)
        if not match:
            raise ValueError("Hexagram line not found or improperly formatted.")

        hexagram_number = match.group(1)
        hexagram_title = match.group(2)

        # Extract Segments
        analysis_match = re.search(r"<<<ANALYSIS_START>>>\s*(.*?)\s*<<<ANALYSIS_COMPLETE>>>", content, re.DOTALL)
        interpretation_match = re.search(r"<<<INTERPRETATION_START>>>\s*(.*?)\s*<<<INTERPRETATION_COMPLETE>>>", content, re.DOTALL)
        recommendation_match = re.search(r"<<<RECOMMANDATION_START>>>\s*(.*?)\s*<<<RECOMMANDATION_COMPLETE>>>", content, re.DOTALL)

        analysis = analysis_match.group(1).strip() if analysis_match else "N/A"
        interpretation = interpretation_match.group(1).strip() if interpretation_match else "N/A"
        recommendation_text = recommendation_match.group(1).strip() if recommendation_match else "N/A"

        return {
            "number": hexagram_number,
            "title": hexagram_title,
            "analysis": analysis,
            "interpretation": interpretation,
            "recommendation": recommendation_text
        }

    except Exception as e:
        print(f"[ERROR] Failed to extract hexagram info: {e}")
        sys.exit(1)

# --- Step 3: Generate HTML output for hexagram ---

def generate_hexagram_html(timestamp):
    data = extract_hexagram_data_from_archive(timestamp)

    filename = f"{timestamp}_hexagram-{data['number']}.html"
    output_path = os.path.join(HTML_OUTPUT_PATH, filename)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    content = f"""<html>
<head>
    <title>FUCKUP Divination {timestamp}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            color: #333;
            margin: 40px;
        }}
        h1 {{
            color: #444;
        }}
        h2 {{
            margin-top: 30px;
        }}
        p {{
            font-size: 18px;
            line-height: 1.6;
        }}
    </style>
</head>
<body>
<h1>Hexagram {data['number']}: {data['title']}</h1>
<p><strong>Divination performed on:</strong> {timestamp.replace('_', ' ')}</p>

<h2>Analysis</h2>
<p style="white-space: pre-line;">{data['analysis']}</p>

<h2>Interpretation</h2>
<p style="white-space: pre-line;">{data['interpretation']}</p>

<h2>Recommendation</h2>
<p style="white-space: pre-line;">{data['recommendation']}</p>

</body>
</html>"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"[INFO] Generated hexagram HTML: {output_path}")

# --- Step 4: Rebuild styled and reversed index.html ---

def generate_index_html(html_path=HTML_OUTPUT_PATH):
    if not os.path.isdir(html_path):
        print(f"Error: HTML path '{html_path}' not found.")
        sys.exit(1)

    html_files = [f for f in os.listdir(html_path) if f.endswith('.html') and f != 'index.html']
    html_files.sort(reverse=True)  # Show newest first

    content = """<html>
<head>
    <title>FUCKUP Divination Archive</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            color: #333;
            margin: 40px;
        }
        h1 {
            color: #222;
        }
        ul {
            list-style-type: none;
            padding: 0;
        }
        li {
            margin-bottom: 10px;
        }
        a {
            color: #0066cc;
            text-decoration: none;
            font-size: 18px;
        }
        a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
<h1>FUCKUP Divination Archive</h1>
<ul>
"""

    for file in html_files:
        try:
            basename = file.replace('.html', '')
            timestamp_part, hexagram_part = basename.split('_hexagram-')
            display_timestamp = timestamp_part.replace('_', ' ').replace('-', ':', 2).replace('-', ' ', 1)
            hexagram_number = hexagram_part
            title = f"Divination for {display_timestamp} — Hexagram {hexagram_number}"
            content += f'  <li><a href="{file}">{title}</a></li>\n'
        except ValueError:
            content += f'  <li><a href="{file}">{file}</a></li>\n'

    content += """</ul>
</body>
</html>"""

    index_path = os.path.join(html_path, "index.html")

    with open(index_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"[INFO] Generated styled index HTML: {index_path}")

# --- Entry Point ---

if __name__ == "__main__":
    timestamp = find_latest_timestamp()
    generate_hexagram_html(timestamp)
    generate_index_html()
