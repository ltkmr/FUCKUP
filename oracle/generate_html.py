import os
import sys
import re
from hijri_converter import Gregorian

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ARCHIVE_PATH = os.path.join(SCRIPT_DIR, "..", "archive")
HTML_OUTPUT_PATH = os.path.join(SCRIPT_DIR, "..", "web")

def find_latest_timestamp(archive_path=ARCHIVE_PATH):
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
    timestamp = timestamp_raw.replace('-', '_')

    print(f"[INFO] Using timestamp from archive: {timestamp}")
    return timestamp

def extract_hexagram_data_from_archive(timestamp):
    archive_filename = timestamp.replace('_', '-') + ".txt"
    archive_path = os.path.join(ARCHIVE_PATH, archive_filename)

    try:
        with open(archive_path, "r", encoding="utf-8") as f:
            content = f.read()

        match = re.search(r"Today's Hexagram #(\d+): (.+?)\s+[\u4DC0-\u4DFF]", content)
        if not match:
            raise ValueError("Hexagram line not found or improperly formatted.")

        hexagram_number = match.group(1)
        hexagram_title = match.group(2)

        metadata_match = re.search(r"<<<METADATA_START>>>\s*(.*?)\s*<<<METADATA_END>>>", content, re.DOTALL)
        metadata = metadata_match.group(1).strip() if metadata_match else "N/A"

        analysis_match = re.search(r"<<<ANALYSIS_START>>>\s*(.*?)\s*<<<ANALYSIS_COMPLETE>>>", content, re.DOTALL)
        interpretation_match = re.search(r"<<<INTERPRETATION_START>>>\s*(.*?)\s*<<<INTERPRETATION_COMPLETE>>>", content, re.DOTALL)
        recommendation_match = re.search(r"<<<RECOMMANDATION_START>>>\s*(.*?)\s*<<<RECOMMANDATION_COMPLETE>>>", content, re.DOTALL)

        analysis = analysis_match.group(1).strip() if analysis_match else "N/A"
        interpretation = interpretation_match.group(1).strip() if interpretation_match else "N/A"
        recommendation_text = recommendation_match.group(1).strip() if recommendation_match else "N/A"

        return {
            "number": hexagram_number,
            "title": hexagram_title,
            "glyph": chr(0x4DC0 + int(hexagram_number) - 1),
            "metadata": metadata,
            "analysis": analysis,
            "interpretation": interpretation,
            "recommendation": recommendation_text
        }

    except Exception as e:
        print(f"[ERROR] Failed to extract hexagram info: {e}")
        sys.exit(1)

def generate_hexagram_html(timestamp):
    data = extract_hexagram_data_from_archive(timestamp)

    filename = f"{timestamp}_hexagram-{data['number']}.html"
    output_path = os.path.join(HTML_OUTPUT_PATH, filename)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    content = f"""<html>
<head>
    <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono&display=swap" rel="stylesheet">
    <title>FUCKUP Divination {timestamp}</title>
    <style>
        body {{
            font-family: 'IBM Plex Mono', monospace;
            background-color: #0b1a1f;
            color: #d0d0c0;
            margin: 40px;
            line-height: 1.6;
        }}
        h1, h2 {{
            color: #e3e3b5;
            border-bottom: 1px dotted #3f4a4f;
            padding-bottom: 0.2em;
        }}
        .glyph {{
            font-size: 96px;
            text-align: center;
            color: #8fddff;
            margin: 30px 0;
        }}
        .metadata {{
            font-size: 14px;
            color: #aaa;
            text-align: center;
            margin-bottom: 20px;
            white-space: pre-line;
        }}
        a {{
            color: #57e389;
            text-decoration: none;
        }}
        a:hover {{
            text-decoration: underline;
        }}
        .backlink {{
            margin: 20px 0;
            text-align: left;
            font-size: 14px;
            color: #999;
        }}
        .section {{
            margin-top: 40px;
            padding: 10px;
            border: 1px dashed #3f4a4f;
            background-color: rgba(255,255,255,0.02);
        }}
        .section p {{
            white-space: pre-line;
            margin: 0;
        }}
        .oracle-header {{
            font-size: 14px;
            color: #777;
            border-bottom: 1px dashed #3f4a4f;
            margin-bottom: 20px;
            padding-bottom: 10px;
        }}
        .container {{
            max-width: 800px;
            margin: 0 auto;
        }}
  
    </style>
</head>
<body>
<div class=\"container\">
<div class=\"oracle-header\">
==============================<br>
::FUCKUP² ORACLE STATION::<br>
Subchannel: Depth Rituals<br>
==============================
</div>
<div class=\"backlink\">
  <a href=\"index.html\">&larr; Back to Archive Index</a>
</div>
<h1>Hexagram {data['number']}: {data['title']}</h1>
<div class=\"glyph\">{data['glyph']}</div>
<div class=\"metadata\">{data['metadata']}</div>
<p><strong>Divination performed on:</strong> {timestamp.replace('_', ' ')}</p>

<h2>Analysis</h2>
<div class=\"section\">
  <p>{data['analysis']}</p>
</div>

<h2>Interpretation</h2>
<div class=\"section\">
  <p>{data['interpretation']}</p>
</div>

<h2>Recommendation</h2>
<div class=\"section\">
  <p>{data['recommendation']}</p>
</div>

<div class=\"backlink\">
  <a href=\"index.html\">&larr; Back to Archive Index</a>
</div>
</div>
</body>
</html>"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"[INFO] Generated full hexagram HTML: {output_path}")

def generate_index_html(html_path=HTML_OUTPUT_PATH):
    if not os.path.isdir(html_path):
        print(f"Error: HTML path '{html_path}' not found.")
        sys.exit(1)

    html_files = [f for f in os.listdir(html_path) if f.endswith('.html') and f != 'index.html']
    html_files.sort(reverse=True)

    content = """<html>
<head>
    <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono&display=swap" rel="stylesheet">
    <title>FUCKUP Divination Archive</title>
    <style>
        body {
            font-family: 'IBM Plex Mono', monospace;
            background-color: #0b1a1f;
            color: #d0d0c0;
            margin: 40px;
            line-height: 1.6;
        }
        h1 {
            color: #e3e3b5;
            border-bottom: 1px dotted #3f4a4f;
            padding-bottom: 0.2em;
        }
        ul {
            list-style-type: none;
            padding: 0;
        }
        li {
            margin-bottom: 10px;
        }
        a {
            color: #57e389;
            text-decoration: none;
            font-size: 18px;
        }
        a:hover {
            text-decoration: underline;
        }
        .section {
            margin-top: 40px;
            padding: 10px;
            border: 1px dashed #3f4a4f;
            background-color: rgba(255,255,255,0.02);
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
        }
    </style>
</head>
<body>
<div class=\"container\">
<div class=\"oracle-header\">
==============================<br>
::FUCKUP² ORACLE STATION::<br>
Subchannel: Depth Rituals<br>
==============================
</div>
<h1>FUCKUP Divination Archive</h1>
<div class=\"section\">
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
</div>
</div>
</body>
</html>"""

    index_path = os.path.join(html_path, "index.html")

    with open(index_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"[INFO] Generated styled index HTML: {index_path}")

if __name__ == "__main__":
    timestamp = find_latest_timestamp()
    generate_hexagram_html(timestamp)
    generate_index_html()
