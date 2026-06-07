"""
summary_diffraction.py
Summary tab: Single-Slit Diffraction  (🔬 การเลี้ยวเบน)
English-only, card-based layout — matches standing-waves style.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Arc, FancyBboxPatch, Rectangle
import streamlit as st

# ── colour palette (shared with other summaries) ──────────────────────────────
CB   = '#2563eb'   # blue
CR   = '#dc2626'   # red
CG   = '#16a34a'   # green
CRED = '#dc2626'
CGR  = '#64748b'   # slate-grey
CDK  = '#0f172a'   # near-black
CBG  = '#f8fafc'   # page background
CPURP= '#7c3aed'   # purple

RC = {
    'font.family':  'DejaVu Sans',
    'axes.facecolor': CBG,
    'figure.facecolor': CBG,
    'text.color': CDK,
    'axes.labelcolor': CGR,
    'xtick.color': CGR,
    'ytick.color': CGR,
}

# ── CSS ───────────────────────────────────────────────────────────────────────
_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

.dif-wrap  { font-family:'Inter',sans-serif; color:#0f172a; max-width:820px; margin:0 auto; }
.dif-h1    { font-size:1.55rem; font-weight:800; color:#1e3a8a;
             border-bottom:3px solid #2563eb; padding-bottom:6px; margin:0 0 20px; }
.dif-h2    { font-size:1.05rem; font-weight:700; color:#1e40af; margin:22px 0 10px; }

/* section card */
.dif-card  { background:#fff; border:1px solid #e2e8f0; border-radius:12px;
             padding:18px 20px 14px; margin-bottom:16px;
             box-shadow:0 1px 4px rgba(0,0,0,.05); }
.dif-card-title {
             font-size:.85rem; font-weight:700; text-transform:uppercase;
             letter-spacing:.06em; color:#64748b; margin-bottom:10px; }
.dif-tag   { display:inline-block; font-size:.72rem; font-weight:700;
             border-radius:6px; padding:2px 8px; margin-right:6px; }
.tag-blue  { background:#dbeafe; color:#1d4ed8; }
.tag-red   { background:#fee2e2; color:#b91c1c; }
.tag-green { background:#dcfce7; color:#15803d; }
.tag-purp  { background:#ede9fe; color:#6d28d9; }

/* formula box */
.dif-formula {
             background:#f1f5f9; border-left:4px solid #2563eb;
             border-radius:0 8px 8px 0; padding:10px 16px;
             font-size:1.05rem; font-weight:600; color:#1e3a8a;
             margin:8px 0; font-family:'Courier New',monospace; }

/* two-col grid */
.dif-grid  { display:grid; grid-template-columns:1fr 1fr; gap:14px; }
.dif-grid3 { display:grid; grid-template-columns:1fr 1fr 1fr; gap:12px; }

/* mini info box */
.dif-info  { background:#f8fafc; border:1px solid #e2e8f0; border-radius:8px;
             padding:10px 14px; font-size:.83rem; line-height:1.7; }
.dif-info b { color:#1e40af; }

/* highlight box */
.dif-hl    { background:#eff6ff; border:1.5px solid #93c5fd; border-radius:8px;
             padding:10px 16px; margin:8px 0; font-size:.88rem; line-height:1.75; }
.dif-hl-g  { background:#f0fdf4; border-color:#86efac; }
.dif-hl-r  { background:#fff5f5; border-color:#fca5a5; }
.dif-hl-p  { background:#f5f3ff; border-color:#c4b5fd; }

/* ref table */
.dif-ref   { width:100%; border-collapse:collapse; font-size:.82rem; }
.dif-ref th{ background:#1e3a8a; color:#fff; padding:7px 12px; text-align:left; }
.dif-ref td{ padding:6px 12px; border-bottom:1px solid #e2e8f0; }
.dif-ref tr:nth-child(even) td { background:#f8fafc; }
</style>
"""


# ── Figures ───────────────────────────────────────────────────────────────────

@st.cache_data
def _fig_geometry():
    """Single-slit geometry diagram: slit width a, angle θ, nodal/antinodal lines."""
    with plt.rc_context(RC):
        fig, ax = plt.subplots(figsize=(9, 5.2))
        ax.set_facecolor('#f0f7ff')
        fig.patch.set_facecolor('#f0f7ff')
        ax.set_aspect('equal')
        ax.axis('off')

        a    = 3.0   # slit width (display units)
        lam  = 1.0
        nmax = int(a / lam)   # = 3
        X_SC = 7.5            # screen x-position
        Y_MAX = 4.5

        ax.set_xlim(-3.5, X_SC + 2.0)
        ax.set_ylim(-Y_MAX, Y_MAX + 0.4)

        # ── barrier ──────────────────────────────────────────────────
        bw = 0.22
        for y0, y1 in [(-Y_MAX, -a/2), (a/2, Y_MAX)]:
            ax.add_patch(Rectangle((-bw, y0), 2*bw, y1-y0,
                                   fc='#475569', ec='none', alpha=0.88, zorder=6))
        ax.text(-bw-0.15, -Y_MAX+0.1, 'Barrier',
                color='#475569', fontsize=7.5, ha='right', va='bottom',
                fontweight='700', zorder=9)

        # ── slit opening markers ──────────────────────────────────────
        ax.plot(0,  a/2, 'D', color=CB, ms=8, zorder=10,
                markeredgecolor='white', markeredgewidth=1.4)
        ax.plot(0, -a/2, 'D', color=CB, ms=8, zorder=10,
                markeredgecolor='white', markeredgewidth=1.4)
        ax.plot(0,    0, 's', color=CPURP, ms=7, zorder=10,
                markeredgecolor='white', markeredgewidth=1.3)
        ax.text(0.3,  a/2, 'top edge', color=CB,
                fontsize=7.5, va='center', fontweight='600')
        ax.text(0.3, -a/2, 'bottom edge', color=CB,
                fontsize=7.5, va='center', fontweight='600')
        ax.text(0.3,    0, 'centre', color=CPURP,
                fontsize=7.5, va='center', fontweight='600')

        # ── slit width annotation ─────────────────────────────────────
        ax.annotate('', xy=(-1.0, a/2), xytext=(-1.0, -a/2),
                    arrowprops=dict(arrowstyle='<->', color=CDK, lw=1.4))
        ax.text(-1.35, 0, 'a', fontsize=13, color=CDK,
                ha='center', va='center', fontweight='bold')

        # ── incoming plane wavefronts ─────────────────────────────────
        for xi in np.arange(-3.2, -0.05, lam):
            ax.plot([xi, xi], [-Y_MAX, -a/2-0.15],
                    color=CB, lw=1.1, alpha=0.40, zorder=2)
            ax.plot([xi, xi], [ a/2+0.15, Y_MAX],
                    color=CB, lw=1.1, alpha=0.40, zorder=2)
        ax.annotate('', xy=(-0.55, 0), xytext=(-2.8, 0),
                    arrowprops=dict(arrowstyle='->', color=CB, lw=1.8,
                                   mutation_scale=16), zorder=9)
        ax.text(-3.2, 0.6, 'Plane wave →', color=CB,
                fontsize=8, fontweight='600', ha='left')

        # ── screen ────────────────────────────────────────────────────
        ax.plot([X_SC, X_SC], [-Y_MAX, Y_MAX],
                color='#1e293b', lw=3.5, zorder=6, solid_capstyle='round')
        ax.text(X_SC + 0.12, Y_MAX - 0.05, 'Screen',
                color='#1e293b', fontsize=8, va='top', fontweight='600')

        # ── L annotation ─────────────────────────────────────────────
        y_L = -Y_MAX + 0.15
        ax.annotate('', xy=(X_SC, y_L), xytext=(0, y_L),
                    arrowprops=dict(arrowstyle='<->', color=CGR, lw=1.2,
                                   mutation_scale=11))
        ax.text(X_SC/2, y_L - 0.42, 'L  (distance to screen)',
                ha='center', fontsize=8, color=CGR)

        # ── nodal & antinodal lines ───────────────────────────────────
        plotted_anti_label = False
        for n in range(1, nmax+1):
            sin_n = n * lam / a
            if abs(sin_n) > 1: break
            th_n = np.arcsin(sin_n)
            for sign in [1, -1]:
                y_sc = X_SC * np.tan(sign * th_n)
                if abs(y_sc) > Y_MAX + 0.1: continue
                kw = dict(color=CRED, lw=1.3, ls='--', alpha=0.80, zorder=4)
                ax.plot([0, X_SC], [0, y_sc], **kw)
                ax.plot(X_SC, y_sc, 'x', color=CRED, ms=6,
                        markeredgewidth=1.6, zorder=7)
                ax.text(X_SC+0.15, y_sc,
                        f'N{n}  (dark)', color=CRED, fontsize=7.5,
                        va='center', ha='left', fontweight='600')

            # antinodal between n-1 and n (approximate midpoint angle)
            sin_a = (n - 0.5) * lam / a
            if abs(sin_a) <= 1:
                th_a = np.arcsin(sin_a)
                for sign in [1, -1]:
                    y_sc = X_SC * np.tan(sign * th_a)
                    if abs(y_sc) > Y_MAX + 0.1: continue
                    ax.plot([0, X_SC], [0, y_sc],
                            color=CG, lw=1.1, alpha=0.55,
                            ls=':', zorder=3)

        # central max
        ax.plot([0, X_SC], [0, 0], color=CG, lw=2.4, alpha=0.9, zorder=4)
        ax.plot(X_SC, 0, 'o', color=CG, ms=8, zorder=7,
                markeredgecolor='white', markeredgewidth=1.4)
        ax.text(X_SC+0.15, 0, 'A₀  Central max\n(brightest, widest)',
                color=CG, fontsize=7.5, va='center', ha='left', fontweight='700')

        # θ₁ angle arc
        th1 = np.arcsin(lam / a)
        ax.add_patch(Arc((0, 0), 2.6, 2.6, angle=0,
                         theta1=0, theta2=np.degrees(th1),
                         color=CPURP, lw=1.8, zorder=7))
        ax.text(1.55, 0.28, 'θ₁', fontsize=10, color=CPURP, fontweight='bold')

        # legend
        leg_N = mpatches.Patch(color=CRED, label='Nodal line (dark fringe)')
        leg_A = mpatches.Patch(color=CG,   label='Antinodal line (bright fringe)')
        ax.legend(handles=[leg_A, leg_N], fontsize=7.5,
                  loc='upper left', framealpha=0.92, edgecolor='#e2e8f0')

        ax.set_title('Single-Slit Diffraction — geometry (a = 3λ  →  3 nodal lines per side)',
                     fontsize=9.5, color=CDK, pad=6, fontweight='700')
        fig.tight_layout(pad=0.4)
    return fig


@st.cache_data
def _fig_pattern():
    """Visual pattern: nodal/antinodal on the slit axis."""
    with plt.rc_context(RC):
        fig, ax = plt.subplots(figsize=(10, 3.6))
        ax.set_facecolor(CBG)
        fig.patch.set_facecolor(CBG)
        ax.axis('off')

        a = 6.0; lam = 2.0
        nmax = int(a / lam)       # 3
        total_node = 2 * nmax     # 6
        total_anti = 2 * nmax - 1 # 5  (side antinodes) + central = 2nmax-1+1...
        # antinodal lines: central (n=0) + (nmax-1) pairs each side? No:
        # Between N1 and N2 is A1; between N2 and N3 is A2; beyond N3 nothing clean
        # So antinodal side lines = nmax-1 pairs + central = 2(nmax-1)+1

        ax.set_xlim(-1.5, 12.5)
        ax.set_ylim(-1.8, 2.2)

        # ruler line
        ax.plot([-0.2, 10.5], [0, 0], color=CDK, lw=2.0,
                solid_capstyle='round', zorder=5)
        ax.text(10.7, 0, '→', color=CDK, fontsize=12, va='center')
        ax.text(-0.5, 0, 'Slit\ncentre', fontsize=7.5, color=CPURP,
                ha='right', va='center', fontweight='600')

        # positions: nodal at x = n*(L_scale), antinodal between
        L_scale = 1.6  # spacing unit

        # central antinode at 0
        ax.plot(0, 0, 'o', color=CG, ms=13, zorder=8,
                markeredgecolor='white', markeredgewidth=2)
        ax.text(0, 0.62, 'A₀', ha='center', fontsize=9,
                color=CG, fontweight='bold')
        ax.text(0, 0.24, 'Δr=0', ha='center', fontsize=6.5, color=CG)

        for n in range(1, nmax+1):
            xN = n * L_scale * 2        # nodal positions (symmetric each side shown on + axis)
            xA = (n - 0.5) * L_scale * 2  # antinodal positions

            # nodal (positive side)
            ax.plot(xN, 0, 'v', color=CRED, ms=10, zorder=8,
                    markeredgecolor='white', markeredgewidth=1.5)
            ax.text(xN, -0.60, f'N{n}', ha='center', fontsize=8.5,
                    color=CRED, fontweight='bold')
            ax.text(xN, -1.05, f'sinθ={n}λ/a', ha='center', fontsize=6.5, color=CRED)

            # antinodal (positive side), only if not too far
            ax.plot(xA, 0, 'o', color=CG, ms=10, zorder=8,
                    markeredgecolor='white', markeredgewidth=1.5)
            ax.text(xA, 0.58, f'A{n}', ha='center', fontsize=8.5,
                    color=CG, fontweight='bold')
            ax.text(xA, 0.20, f'sinθ≈{n-.5:.1f}λ/a', ha='center', fontsize=6.5, color=CG)

        # labels
        ax.text(5.0, 1.9,
                f'a = {int(a)} cm,  λ = {int(lam)} cm   →   '
                f'n_max = {nmax}   →   Nodal lines = {total_node}',
                ha='center', fontsize=9.5, fontweight='700', color=CDK,
                bbox=dict(boxstyle='round,pad=0.35', fc='#f1f5f9',
                          ec='#cbd5e1', lw=1.6))

        legend_N = mpatches.Patch(color=CRED, label='Node  ▼  (dark, destructive)')
        legend_A = mpatches.Patch(color=CG,   label='Antinode  ●  (bright, constructive)')
        ax.legend(handles=[legend_A, legend_N], fontsize=8,
                  loc='lower right', framealpha=0.95, edgecolor='#e2e8f0')

        fig.tight_layout(pad=0.4)
    return fig


@st.cache_data
def _fig_ref_table():
    """Quick-reference comparison table as figure."""
    with plt.rc_context(RC):
        fig, ax = plt.subplots(figsize=(9, 3.2))
        ax.set_facecolor(CBG)
        fig.patch.set_facecolor(CBG)
        ax.axis('off')

        rows = [
            ('Quantity',             'Formula',                    'Notes'),
            ('Node condition',       'a sinθ = nλ',                'n = ±1, ±2, … (NOT n=0)'),
            ('Max order (n_max)',    'n_max = floor(a / λ)',        'integer part of a/λ'),
            ('Total nodal lines',   '2 × n_max',                   'symmetric about centre'),
            ('Angle of nth node',   'sinθ_n = nλ / a',            'solve for θ'),
            ('Approx antinode',     'sinθ ≈ (n − ½)λ / a',        'between N(n−1) and Nn'),
        ]

        col_w = [0.28, 0.38, 0.34]
        col_x = [0.01, 0.29, 0.67]
        row_h = 1.0 / len(rows)

        for r_idx, row in enumerate(rows):
            y = 1.0 - r_idx * row_h
            bg = '#1e3a8a' if r_idx == 0 else ('#f8fafc' if r_idx % 2 == 0 else '#fff')
            fc = '#fff'    if r_idx == 0 else CDK
            fw = 'bold'
            ax.add_patch(Rectangle((0, y - row_h), 1, row_h,
                                   fc=bg, ec='#e2e8f0', lw=0.7,
                                   transform=ax.transAxes, clip_on=False))
            for c_idx, (cell, cx) in enumerate(zip(row, col_x)):
                ax.text(cx + 0.01, y - row_h/2, cell,
                        transform=ax.transAxes,
                        fontsize=8.5 if r_idx == 0 else 8.8,
                        va='center', ha='left',
                        color=fc if r_idx == 0 else (CB if c_idx == 1 else CDK),
                        fontweight='bold' if r_idx == 0 or c_idx == 1 else 'normal',
                        fontfamily='monospace' if c_idx == 1 and r_idx > 0 else 'sans-serif')

        ax.set_xlim(0, 1); ax.set_ylim(0, 1)
        fig.tight_layout(pad=0.3)
    return fig


# ── Main render function ──────────────────────────────────────────────────────

def render_diffraction():
    st.markdown(_CSS, unsafe_allow_html=True)
    st.markdown('<div class="dif-wrap">', unsafe_allow_html=True)

    # ── Title ─────────────────────────────────────────────────────────────────
    st.markdown("""
    <div class="dif-h1">🔬 Diffraction — Single-Slit & Double-Slit</div>
    """, unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════════════
    # 01 — What is Diffraction?
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown('<div class="dif-h2">01 — What is Diffraction?</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="dif-card">
      <div class="dif-grid">
        <div class="dif-info">
          <b>Definition</b><br>
          When a wave passes through a narrow slit or past an obstacle,
          it <b>bends and spreads</b> into the geometric shadow region.<br><br>
          <b>Key condition:</b> diffraction is significant when<br>
          &emsp;slit width <b>a ≈ λ</b>  (wavelength ~ slit size)<br><br>
          If a ≫ λ → almost no bending (ray-like)<br>
          If a ≪ λ → nearly circular spread (point source)
        </div>
        <div class="dif-info">
          <b>Huygens' Principle</b><br>
          Every point on a wavefront acts as a new point source of secondary waves.
          The slit lets through a strip of wavefront → each point inside the slit
          radiates outward → the secondary waves <b>interfere</b> to create a
          pattern of bright and dark bands on a screen.<br><br>
          <span class="dif-tag tag-blue">Diffraction</span>
          <span class="dif-tag tag-purp">Interference</span>
          are two sides of the same phenomenon.
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════════════
    # 02 — Single-Slit Geometry
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown('<div class="dif-h2">02 — Single-Slit: Geometry & Nodal Lines</div>',
                unsafe_allow_html=True)

    st.markdown("""
    <div class="dif-card">
      <div class="dif-card-title">Key formula — dark fringe (node) condition</div>
      <div class="dif-formula">a · sinθ = n · λ &emsp;&emsp; n = ±1, ±2, ±3, …</div>
      <div class="dif-grid" style="margin-top:12px">
        <div class="dif-hl">
          <b>a</b> = slit width (cm or m)<br>
          <b>θ</b> = angle from the central axis to the nodal line<br>
          <b>λ</b> = wavelength<br>
          <b>n</b> = order number &nbsp;(n = 1 is the 1st dark fringe, etc.)
        </div>
        <div class="dif-hl dif-hl-r">
          ⚠️ <b>n = 0 is NOT a node</b> — the centre is always the
          bright central maximum (A₀).<br><br>
          Nodes exist only for <b>n = ±1, ±2, ±3, …</b>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.image(_fig_geometry(), use_container_width=True)

    # ══════════════════════════════════════════════════════════════════════════
    # 03 — Counting Lines
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown('<div class="dif-h2">03 — Counting Nodal & Antinodal Lines</div>',
                unsafe_allow_html=True)
    st.markdown("""
    <div class="dif-card">
      <div class="dif-grid3">
        <div class="dif-info" style="border-left:4px solid #dc2626;">
          <b style="color:#dc2626">Maximum order</b><br><br>
          <code style="font-size:1rem">n_max = floor(a / λ)</code><br><br>
          Take the <b>integer part</b> of a/λ.<br>
          (sinθ cannot exceed 1, so n·λ/a ≤ 1 → n ≤ a/λ)
        </div>
        <div class="dif-info" style="border-left:4px solid #dc2626;">
          <b style="color:#dc2626">Total nodal lines</b><br><br>
          <code style="font-size:1rem">= 2 × n_max</code><br><br>
          One set on each side of centre.<br>
          e.g. n_max=3 → N1, N2, N3 per side → <b>6 nodal lines</b>
        </div>
        <div class="dif-info" style="border-left:4px solid #16a34a;">
          <b style="color:#16a34a">Antinodal lines</b><br><br>
          Central bright band = <b>A₀</b><br>
          Side bright bands: <b>A₁, A₂, …</b> appear <em>between</em> nodal lines<br>
          (between N(n−1) and Nn)
        </div>
      </div>

      <div style="margin-top:14px">
        <div class="dif-hl dif-hl-g" style="margin-bottom:8px">
          <b>Example:</b>&ensp; a = 6 cm, λ = 2 cm<br>
          &emsp;n_max = floor(6/2) = <b>3</b><br>
          &emsp;Nodal lines = 2 × 3 = <b>6 lines</b>&ensp; (N1, N2, N3 on each side)
        </div>
        <div class="dif-hl dif-hl-g">
          <b>Example:</b>&ensp; a = 8 cm, λ = 2.5 cm<br>
          &emsp;n_max = floor(8/2.5) = floor(3.2) = <b>3</b><br>
          &emsp;Nodal lines = 2 × 3 = <b>6 lines</b>&ensp;(not 6.4 — always round down)
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.image(_fig_pattern(), use_container_width=True)

    # ══════════════════════════════════════════════════════════════════════════
    # 04 — Finding the Angle
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown('<div class="dif-h2">04 — Finding the Angle of a Nodal Line</div>',
                unsafe_allow_html=True)
    st.markdown("""
    <div class="dif-card">
      <div class="dif-formula">sinθ_n = n · λ / a &emsp;→&emsp; θ_n = arcsin(nλ/a)</div>
      <div class="dif-grid" style="margin-top:12px">
        <div class="dif-hl">
          <b>Example — nth dark fringe angle:</b><br>
          a = 8 cm, λ = 2.5 cm, find θ₂<br><br>
          sinθ₂ = 2 × 2.5 / 8 = 5/8 = 0.625<br>
          θ₂ = arcsin(0.625) ≈ <b>38.7°</b>
        </div>
        <div class="dif-hl dif-hl-p">
          <b>Approximate antinodal angle:</b><br>
          A<sub>n</sub> lies <em>roughly</em> halfway between N<sub>n−1</sub> and N<sub>n</sub><br><br>
          sinθ_A ≈ (n − ½) · λ / a<br><br>
          e.g. A₁ between N₀(centre) and N₁:<br>
          sinθ ≈ 0.5 × 2.5/8 = 0.156 → θ ≈ 9°<br>
          <em style="font-size:.78rem">(not exact — just an approximation)</em>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════════════
    # 05 — Changing a or λ
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown('<div class="dif-h2">05 — Effect of Changing a or λ</div>',
                unsafe_allow_html=True)
    st.markdown("""
    <div class="dif-card">
      <div class="dif-formula">n_max = floor(a / λ) &emsp;→&emsp; n_new = floor(a_new / λ_new)</div>
      <div style="margin-top:10px" class="dif-hl dif-hl-g">
        <b>Worked example (Q65-type):</b><br>
        Original: 6 nodal lines → n_max = 3 → a/λ = 3<br>
        Change: a becomes 2a, frequency becomes f/3 → λ becomes 3λ<br><br>
        n_new = floor(2a / 3λ) = floor(⅔ × 3) = floor(2) = <b>2</b><br>
        New nodal lines = 2 × 2 = <b>4 lines</b>
      </div>
      <div style="margin-top:10px">
        <table style="width:100%;font-size:.83rem;border-collapse:collapse">
          <tr>
            <th style="background:#1e3a8a;color:#fff;padding:6px 10px;text-align:left">Change</th>
            <th style="background:#1e3a8a;color:#fff;padding:6px 10px;text-align:left">Effect on n_max</th>
            <th style="background:#1e3a8a;color:#fff;padding:6px 10px;text-align:left">Effect on pattern</th>
          </tr>
          <tr style="background:#f8fafc">
            <td style="padding:6px 10px;border-bottom:1px solid #e2e8f0">Wider slit (a↑)</td>
            <td style="padding:6px 10px;border-bottom:1px solid #e2e8f0">n_max ↑</td>
            <td style="padding:6px 10px;border-bottom:1px solid #e2e8f0">More nodal lines, narrower central max</td>
          </tr>
          <tr>
            <td style="padding:6px 10px;border-bottom:1px solid #e2e8f0">Narrower slit (a↓)</td>
            <td style="padding:6px 10px;border-bottom:1px solid #e2e8f0">n_max ↓</td>
            <td style="padding:6px 10px;border-bottom:1px solid #e2e8f0">Fewer lines, wider central max (more spreading)</td>
          </tr>
          <tr style="background:#f8fafc">
            <td style="padding:6px 10px;border-bottom:1px solid #e2e8f0">Longer λ (↑)</td>
            <td style="padding:6px 10px;border-bottom:1px solid #e2e8f0">n_max ↓</td>
            <td style="padding:6px 10px;border-bottom:1px solid #e2e8f0">Fewer lines, larger angles, more diffraction</td>
          </tr>
          <tr>
            <td style="padding:6px 10px">Shorter λ (↓)</td>
            <td style="padding:6px 10px">n_max ↑</td>
            <td style="padding:6px 10px">More lines, smaller angles, less diffraction</td>
          </tr>
        </table>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════════════
    # 06 — Double Slit (brief)
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown('<div class="dif-h2">06 — Double-Slit (Review)</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="dif-card">
      <div class="dif-card-title">Two point sources separated by d — same as interference</div>
      <div class="dif-grid">
        <div class="dif-hl dif-hl-g">
          <b style="color:#16a34a">Antinodal (constructive)</b><br>
          Δr = nλ &emsp; n = 0, 1, 2, …<br><br>
          n_max = floor(d / λ)<br>
          Total antinodal lines = <b>2·n_max + 1</b>
        </div>
        <div class="dif-hl dif-hl-r">
          <b style="color:#dc2626">Nodal (destructive)</b><br>
          Δr = (n − ½)λ &emsp; n = 1, 2, …<br><br>
          Total nodal lines = <b>2·n_max</b>
        </div>
      </div>
      <div class="dif-hl dif-hl-g" style="margin-top:10px">
        <b>Example (Q68):</b>&ensp; d = 8 cm, Δr = 4 cm → λ = 2 cm<br>
        n_max = floor(8/2) = 4<br>
        Antinodal: 2×4+1 = <b>9 lines</b> &emsp; Nodal: 2×4 = <b>8 lines</b>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════════════
    # REF — Formula Reference
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown('<div class="dif-h2">📋 Formula Reference</div>', unsafe_allow_html=True)
    st.image(_fig_ref_table(), use_container_width=True)

    st.markdown("""
    <div class="dif-card" style="margin-top:10px">
      <div class="dif-grid3">
        <div class="dif-info">
          <b>3-Step method</b><br>
          1. Find n_max = floor(a/λ)<br>
          2. Total nodal = 2 × n_max<br>
          3. Use sinθ = nλ/a for angles
        </div>
        <div class="dif-info">
          <b>Trap to avoid</b><br>
          Don't round a/λ up.<br>
          Always use <b>floor</b> (integer part).<br>
          e.g. a/λ = 3.9 → n_max = <b>3</b>, not 4
        </div>
        <div class="dif-info">
          <b>Double slit</b><br>
          Antinodal: 2·n_max + 1<br>
          Nodal: 2·n_max<br>
          where n_max = floor(d/λ)
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)   # close dif-wrap
