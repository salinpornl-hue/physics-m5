"""
pdf_export.py
Generate a printable PDF of all exercise questions.
Uses only matplotlib (no extra dependencies).
"""

import io
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.font_manager as fm
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.lines import Line2D


# ── Font selection ──────────────────────────────────────────────────────────
def _thai_font() -> str:
    """Return a font family name that can render Thai glyphs."""
    for name in ['Tahoma', 'Arial Unicode MS', 'Leelawadee UI',
                 'Leelawadee', 'Cordia New', 'FreeSans']:
        try:
            path = fm.findfont(fm.FontProperties(family=name), fallback_to_default=False)
            if path and 'DejaVu' not in path and 'ttf' in path.lower() or 'ttc' in path.lower():
                return name
        except Exception:
            pass
    return 'DejaVu Sans'


# ── Text wrapping ────────────────────────────────────────────────────────────
def _wrap(text: str, max_chars: int = 60) -> str:
    """
    Wrap text at max_chars per line.
    Breaks at the last space within the limit when possible;
    otherwise hard-wraps (needed for Thai which has no word spaces).
    """
    if len(text) <= max_chars:
        return text
    lines = []
    while len(text) > max_chars:
        bp = text.rfind(' ', 0, max_chars)
        if bp == -1:
            bp = max_chars
        lines.append(text[:bp].rstrip())
        text = text[bp:].lstrip()
    if text:
        lines.append(text)
    return '\n'.join(lines)


# ── PDF generation ───────────────────────────────────────────────────────────
def generate_problems_pdf(questions: list, get_plot_for_question) -> bytes:
    """
    Build a multi-page A4 PDF: one question per page.
    Returns raw PDF bytes.

    Parameters
    ----------
    questions : list[str]
        Question texts (index 0 = question 1).
    get_plot_for_question : callable
        Function(int) → matplotlib Figure | None
    """
    font = _thai_font()
    A4_W, A4_H = 8.27, 11.69   # inches
    N = len(questions)

    buf = io.BytesIO()
    with PdfPages(buf) as pdf:
        for idx, q_text in enumerate(questions):
            q_num = idx + 1
            q_fig = get_plot_for_question(q_num)   # may be None

            # ── Create A4 page ──────────────────────────────────────────────
            page = plt.figure(figsize=(A4_W, A4_H), facecolor='white')

            # Normalised margins
            ml = 0.08; mr = 0.08   # left / right
            mt = 0.06; mb = 0.04   # top gap (below header) / bottom

            # Header band (question number + separator)
            HDR_H = 0.07          # fraction of page height
            hdr_y = 1 - mt - HDR_H

            # Blue accent line below header
            page.add_artist(Line2D(
                [ml, 1 - mr], [hdr_y, hdr_y],
                transform=page.transFigure,
                color='#2563eb', lw=2.0, solid_capstyle='round'
            ))

            # Question number
            page.text(
                ml, 1 - mt - 0.005,
                f'ข้อที่  {q_num}',
                transform=page.transFigure,
                fontsize=15, fontweight='bold', color='#1e3a8a',
                fontfamily=font, va='top'
            )
            # Right-side counter
            page.text(
                1 - mr, 1 - mt - 0.005,
                f'{q_num} / {N}',
                transform=page.transFigure,
                fontsize=9, color='#94a3b8',
                fontfamily=font, va='top', ha='right'
            )

            if q_fig is not None:
                # ── Layout with figure ──────────────────────────────────────
                # Question text occupies top portion, figure below
                TEXT_H = 0.30   # fraction of page for text block
                FIG_H  = 0.47   # fraction of page for figure
                GAP    = 0.02

                text_top = hdr_y - 0.015
                text_bot = text_top - TEXT_H
                fig_top  = text_bot - GAP
                fig_bot  = mb + 0.02

                ax_t = page.add_axes([ml, text_bot, 1 - ml - mr, TEXT_H])
                ax_f = page.add_axes([ml, fig_bot,  1 - ml - mr, fig_top - fig_bot])
                ax_t.axis('off')
                ax_f.axis('off')

                # Render question text
                ax_t.text(0, 1, _wrap(q_text, 62),
                          fontsize=11.5, fontfamily=font,
                          va='top', ha='left', linespacing=1.75,
                          transform=ax_t.transAxes)

                # Render question figure as raster image
                img_buf = io.BytesIO()
                q_fig.savefig(img_buf, format='png', dpi=130,
                              bbox_inches='tight', facecolor='white')
                img_buf.seek(0)
                img = mpimg.imread(img_buf)
                ax_f.imshow(img, aspect='equal')
                plt.close(q_fig)

            else:
                # ── Layout without figure ───────────────────────────────────
                TEXT_H = 0.78
                text_bot = hdr_y - 0.02 - TEXT_H

                ax_t = page.add_axes([ml, text_bot, 1 - ml - mr, TEXT_H])
                ax_t.axis('off')

                ax_t.text(0, 1, _wrap(q_text, 62),
                          fontsize=12, fontfamily=font,
                          va='top', ha='left', linespacing=1.85,
                          transform=ax_t.transAxes)

            # Page bottom border
            page.add_artist(Line2D(
                [ml, 1 - mr], [mb, mb],
                transform=page.transFigure,
                color='#e2e8f0', lw=1.0
            ))

            pdf.savefig(page, bbox_inches='tight', facecolor='white')
            plt.close(page)

    buf.seek(0)
    return buf.getvalue()
