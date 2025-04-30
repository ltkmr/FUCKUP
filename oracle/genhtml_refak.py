def generate_index_html(html_path=HTML_OUTPUT_PATH):
    """Generates index.html listing all divinations nicely."""
    if not os.path.isdir(html_path):
        print(f"Error: HTML path '{html_path}' not found.")
        sys.exit(1)

    html_files = [f for f in os.listdir(html_path) if f.endswith('.html') and f != 'index.html']
    html_files.sort()

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
