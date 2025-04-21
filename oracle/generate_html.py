from pathlib import Path
from typing import List

# Templates

PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <link rel="stylesheet" type="text/css" href="style.css">
</head>
<body>
    <h1>{title}</h1>
    <pre>{content}</pre>
    <p><a href="index.html">Back to archive index</a></p>
</body>
</html>
"""

INDEX_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>FUCKUP² Oracle Archive</title>
    <link rel="stylesheet" type="text/css" href="style.css">
</head>
<body>
    <h1>FUCKUP² Oracle Archive</h1>
    <ul>
        {links}
    </ul>
</body>
</html>
"""

LINK_TEMPLATE = '<li><a href="{filename}">{display_name}</a></li>'

# Paths
project_dir = Path(__file__).parent.parent
archive_dir = project_dir / "archive"
output_dir = project_dir / "web"

# Make sure output directory exists
output_dir.mkdir(exist_ok=True)


def create_index(pages: List[Path]):
    links_html = "\n".join(LINK_TEMPLATE.format(filename=page, display_name=page.stem) for page in pages)

    index_html = INDEX_TEMPLATE.format(links=links_html)

    index_path = output_dir / "index.html"
    with index_path.open("w", encoding="utf-8") as f:
        f.write(index_html)

    print(f"✅ Index page generated at {index_path}")


def create_page(filename: Path) -> Path:
    archive_path = archive_dir / filename
    output_filename = filename.with_suffix(".html")
    output_path = output_dir / output_filename

    with archive_path.open("r", encoding="utf-8") as src:
        content = src.read()

    page_html = PAGE_TEMPLATE.format(title="FUCKUP² Prophecy", content=content)

    with output_path.open("w", encoding="utf-8") as f:
        f.write(page_html)

    print(f"✅ Generated page: {output_filename}")
    return output_filename


def main():
    print("🌐 Generating web archive...")

    # Find all archive files
    archive_files = [f for f in archive_dir.iterdir() if f.endswith(".txt")]
    archive_files.sort(reverse=True)  # Show latest first

    # Generate HTML pages
    generated_pages = [create_page(f) for f in archive_files]

    # Generate index page
    create_index(generated_pages)

    print("🎉 Web archive generation complete!")


if __name__ == "__main__":
    main()
