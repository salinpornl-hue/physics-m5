"""
pdf_export.py
Generate a printable PDF of all exercise questions using fpdf2.
Thai text is fully supported via the system Tahoma font.
"""

import io
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from fpdf import FPDF


# ── Find Thai-capable TTF font on Windows ────────────────────────────────────
_FONT_CANDIDATES = [
    r"C:\Windows\Fonts\tahoma.ttf",
    r"C:\Windows\Fonts\tahomabd.ttf",
    r"C:\Windows\Fonts\cordia.ttf",
    r"C:\Windows\Fonts\leelawad.ttf",
]

def _find_font() -> str:
    for path in _FONT_CANDIDATES:
        if os.path.exists(path):
            return path
    raise FileNotFoundError(
        "ไม่พบ font ภาษาไทย กรุณาตรวจสอบว่า tahoma.ttf อยู่ใน C:\\Windows\\Fonts\\"
    )


# ── PDF generation ───────────────────────────────────────────────────────────
def generate_problems_pdf(questions: list, get_plot_for_question) -> bytes:
    """
    Build a multi-page A4 PDF: one question per page.
    Returns raw PDF bytes.
    """
    font_path = _find_font()
    font_bold_path = r"C:\Windows\Fonts\tahomabd.ttf"

    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_font('Thai', '', font_path)
    if os.path.exists(font_bold_path):
        pdf.add_font('Thai', 'B', font_bold_path)

    N = len(questions)
    PAGE_W = 210  # A4 width mm
    MARGIN = 15
    CONTENT_W = PAGE_W - 2 * MARGIN

    for idx, q_text in enumerate(questions):
        q_num = idx + 1
        pdf.add_page()

        # ── Header ──────────────────────────────────────────────────────
        pdf.set_font('Thai', 'B', 15)
        pdf.set_text_color(30, 58, 138)   # dark blue
        pdf.set_x(MARGIN)
        pdf.cell(CONTENT_W * 0.7, 9, f'ข้อที่  {q_num}', ln=0)

        pdf.set_font('Thai', '', 9)
        pdf.set_text_color(148, 163, 184)  # slate
        pdf.cell(CONTENT_W * 0.3, 9, f'{q_num} / {N}', ln=1, align='R')

        # Blue separator line
        pdf.set_draw_color(37, 99, 235)
        pdf.set_line_width(0.6)
        pdf.line(MARGIN, pdf.get_y(), PAGE_W - MARGIN, pdf.get_y())
        pdf.ln(4)

        # ── Question text ────────────────────────────────────────────────
        pdf.set_font('Thai', '', 12)
        pdf.set_text_color(15, 23, 42)    # near-black
        pdf.set_x(MARGIN)
        pdf.multi_cell(CONTENT_W, 8, q_text)
        pdf.ln(4)

        # ── Figure (if any) ──────────────────────────────────────────────
        q_fig = get_plot_for_question(q_num)
        if q_fig is not None:
            img_buf = io.BytesIO()
            q_fig.savefig(img_buf, format='png', dpi=130,
                          bbox_inches='tight', facecolor='white')
            img_buf.seek(0)
            plt.close(q_fig)

            # Centre the image; cap width at CONTENT_W
            img_w_mm = min(CONTENT_W, 160)
            pdf.set_x(MARGIN + (CONTENT_W - img_w_mm) / 2)
            pdf.image(img_buf, w=img_w_mm)

        # ── Footer ───────────────────────────────────────────────────────
        pdf.set_y(-14)
        pdf.set_draw_color(226, 232, 240)
        pdf.set_line_width(0.3)
        pdf.line(MARGIN, pdf.get_y(), PAGE_W - MARGIN, pdf.get_y())
        pdf.set_font('Thai', '', 8)
        pdf.set_text_color(148, 163, 184)
        pdf.cell(CONTENT_W, 6, 'ฟิสิกส์ — คลื่นกล', align='C')

    return bytes(pdf.output())
