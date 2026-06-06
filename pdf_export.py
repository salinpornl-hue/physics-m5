"""
pdf_export.py
Generate a printable HTML file of all exercise questions.
- Thai text rendered by the browser (no font dependency)
- Figures embedded as base64 PNG
- User opens the file in Chrome/Edge → Ctrl+P → Save as PDF
"""

import io
import base64
import html as html_lib
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def generate_problems_pdf(questions: list, get_plot_for_question) -> bytes:
    """
    Build a single HTML file containing all questions with embedded figures.
    Returns UTF-8 encoded bytes.

    Usage: save as .html, open in browser, Ctrl+P → Save as PDF.
    """
    N = len(questions)
    parts = [_html_header(N)]

    for idx, q_text in enumerate(questions):
        q_num = idx + 1
        q_fig = get_plot_for_question(q_num)

        img_tag = ""
        if q_fig is not None:
            buf = io.BytesIO()
            q_fig.savefig(buf, format='png', dpi=130,
                          bbox_inches='tight', facecolor='white')
            buf.seek(0)
            b64 = base64.b64encode(buf.read()).decode()
            plt.close(q_fig)
            img_tag = f'<img src="data:image/png;base64,{b64}" class="fig">'

        safe_text = html_lib.escape(q_text)
        parts.append(f"""
<div class="question">
  <div class="q-header">
    <span class="q-num">ข้อที่ {q_num}</span>
    <span class="q-counter">{q_num} / {N}</span>
  </div>
  <hr class="q-line">
  <p class="q-text">{safe_text}</p>
  {img_tag}
</div>
""")

    parts.append("</body></html>")
    return "".join(parts).encode("utf-8")


def _html_header(n: int) -> str:
    return f"""<!DOCTYPE html>
<html lang="th">
<head>
<meta charset="UTF-8">
<title>แบบฝึกหัดฟิสิกส์ — คลื่นกล ({n} ข้อ)</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Sarabun:wght@400;700&display=swap');

  * {{ box-sizing: border-box; margin: 0; padding: 0; }}

  body {{
    font-family: 'Sarabun', 'TH Sarabun New', Tahoma, sans-serif;
    font-size: 14pt;
    color: #0f172a;
    background: #fff;
    padding: 0;
  }}

  h1.title {{
    text-align: center;
    color: #1e3a8a;
    font-size: 20pt;
    padding: 28px 0 8px;
    border-bottom: 2px solid #2563eb;
    margin-bottom: 24px;
  }}

  .question {{
    padding: 18px 32px 22px;
    page-break-inside: avoid;
    break-inside: avoid;
  }}

  .question + .question {{
    border-top: 1px solid #e2e8f0;
  }}

  .q-header {{
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    margin-bottom: 4px;
  }}

  .q-num {{
    font-size: 15pt;
    font-weight: 700;
    color: #1e3a8a;
  }}

  .q-counter {{
    font-size: 9pt;
    color: #94a3b8;
  }}

  .q-line {{
    border: none;
    border-top: 1.5px solid #2563eb;
    margin: 5px 0 12px;
  }}

  .q-text {{
    line-height: 1.85;
    margin-bottom: 14px;
  }}

  img.fig {{
    display: block;
    max-width: 560px;
    width: 100%;
    margin: 0 auto;
  }}

  /* ── Print styles ── */
  @media print {{
    body {{ padding: 0; }}
    .question {{ padding: 14px 24px 18px; }}
    @page {{ margin: 1.8cm 1.5cm; size: A4; }}
  }}
</style>
</head>
<body>
<h1 class="title">แบบฝึกหัดฟิสิกส์ — คลื่นกล &nbsp;({n} ข้อ)</h1>
"""
