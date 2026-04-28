"""
Converts Phase5Report.md to Phase5Report.pdf.

Usage:
    python report/generate_pdf.py

Dependencies (install once):
    pip install markdown xhtml2pdf
"""

from pathlib import Path
from io import BytesIO

import markdown
from xhtml2pdf import pisa

REPORT_DIR = Path(__file__).resolve().parent
MD_FILE = REPORT_DIR / "Phase5Report.md"
PDF_FILE = REPORT_DIR / "Phase5Report.pdf"

CSS = """
@page { size: letter; margin: 1.25in 1.25in 1in 1.25in; }

body {
    font-family: Times New Roman, Times, serif;
    font-size: 12pt;
    line-height: 1.5;
    color: #000;
}

h1 {
    font-size: 16pt;
    font-weight: bold;
    text-align: center;
    margin-bottom: 4pt;
}

h2 {
    font-size: 13pt;
    font-weight: bold;
    margin-top: 18pt;
    margin-bottom: 6pt;
    page-break-after: avoid;
}

h3 {
    font-size: 12pt;
    font-weight: bold;
    font-style: italic;
    margin-top: 12pt;
    margin-bottom: 4pt;
    page-break-after: avoid;
}

p { margin: 0 0 8pt 0; }

ul, ol { margin: 0 0 8pt 0; padding-left: 20pt; }
li { margin-bottom: 2pt; }

hr { border: none; border-top: 1px solid #000; margin: 14pt 0; }

pre {
    font-family: Courier New, Courier, monospace;
    font-size: 9pt;
    line-height: 1.4;
    background: #f5f5f5;
    border: 1px solid #ccc;
    padding: 8pt 10pt;
    margin: 8pt 0;
    page-break-inside: avoid;
}

code {
    font-family: Courier New, Courier, monospace;
    font-size: 9.5pt;
}

pre code { font-size: 9pt; }

table {
    width: 100%;
    border-collapse: collapse;
    font-size: 10.5pt;
    margin: 8pt 0 12pt 0;
    page-break-inside: avoid;
}

thead th {
    border: 1px solid #000;
    padding: 4pt 7pt;
    font-weight: bold;
    text-align: left;
    background: #e8e8e8;
}

tbody td {
    border: 1px solid #000;
    padding: 4pt 7pt;
    vertical-align: top;
}

img {
    display: block;
    max-width: 100%;
    margin: 12pt auto;
}

strong { font-weight: bold; }
em { font-style: italic; }
a { color: #000; }
"""


def build_html(md_text: str) -> str:
    body = markdown.markdown(
        md_text,
        extensions=["tables", "fenced_code", "nl2br"],
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <style>{CSS}</style>
</head>
<body>
{body}
</body>
</html>"""


def main() -> None:
    if not MD_FILE.exists():
        raise FileNotFoundError(f"Markdown source not found: {MD_FILE}")

    md_text = MD_FILE.read_text(encoding="utf-8")
    html = build_html(md_text)

    def link_callback(uri, rel):
        path = REPORT_DIR / uri
        return str(path) if path.exists() else uri

    print(f"Converting {MD_FILE.name} → {PDF_FILE.name} ...")
    with PDF_FILE.open("wb") as f:
        result = pisa.CreatePDF(
            BytesIO(html.encode("utf-8")), dest=f, link_callback=link_callback
        )

    if result.err:
        raise RuntimeError(f"PDF generation failed with {result.err} error(s).")

    print(f"Done: {PDF_FILE}")


if __name__ == "__main__":
    main()
