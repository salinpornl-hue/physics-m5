"""
summary.py  —  Water Wave Interference Summary  (Grade 11)
Circular-wavefront style.  All text in English.
"""
import streamlit as st
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Arc, FancyArrowPatch
import matplotlib.font_manager as fm

# ── Font ─────────────────────────────────────────────────────────────────────
_THAI = ['Tahoma', 'Arial Unicode MS', 'Browallia New',
         'AngsanaUPC', 'Cordia New', 'FreeSans']
_avail = {f.name for f in fm.fontManager.ttflist}
_font  = next((f for f in _THAI if f in _avail), 'DejaVu Sans')

RC = {
    'font.family': _font,
    'axes.unicode_minus': False,
    'figure.dpi': 130,
    'savefig.bbox': 'tight',
}

# Colour palette
CB   = '#1d4ed8'   # blue  (S1)
CR   = '#b91c1c'   # red   (S2)
CG   = '#16a34a'   # green (constructive / antinode)
CRED = '#dc2626'   # red   (destructive / node)
CGR  = '#475569'   # slate
CDK  = '#0f172a'
CBG  = '#ffffff'

# ── CSS ───────────────────────────────────────────────────────────────────────
_CSS = """
<style>
.hero{background:linear-gradient(135deg,#0f172a,#1e3a8a,#2563eb);
      border-radius:14px;padding:36px 32px 28px;color:#fff;margin-bottom:28px}
.hero h1{font-size:2rem;font-weight:800;margin:0 0 4px}
.hero p{color:#93c5fd;margin:0;font-size:.98rem}
.sh{font-size:1.18rem;font-weight:700;color:#0f172a;
    border-bottom:2.5px solid #2563eb;padding-bottom:5px;margin:28px 0 14px}
.pill{display:inline-block;background:#dbeafe;color:#1d4ed8;
      font-size:.68rem;font-weight:700;padding:2px 9px;border-radius:20px;
      letter-spacing:.5px;text-transform:uppercase;margin-right:8px;vertical-align:middle}
.card{background:#fff;border:1px solid #e2e8f0;border-radius:10px;
      padding:18px 20px;margin:10px 0;box-shadow:0 1px 3px rgba(0,0,0,.06)}
.cb{border-left:4px solid #3b82f6}.cg{border-left:4px solid #16a34a}
.cr{border-left:4px solid #dc2626}.cy{border-left:4px solid #d97706}
.cs{border-left:4px solid #94a3b8}
.card h4{margin:0 0 7px;font-size:.88rem;font-weight:700}
.card p,.card li{font-size:.91rem;color:#374151;line-height:1.7}
.card ul{margin:5px 0 0;padding-left:17px}
.rt{width:100%;border-collapse:collapse;font-size:.88rem}
.rt th{background:#1e3a8a;color:#fff;padding:8px 13px;text-align:center;font-weight:600}
.rt td{padding:8px 13px;text-align:center;border-bottom:1px solid #e2e8f0}
.rt tr:nth-child(even) td{background:#f8fafc}
.tg{color:#15803d;font-weight:700}.tr{color:#dc2626;font-weight:700}
.cap{font-size:.79rem;color:#64748b;text-align:center;margin:-6px 0 14px;font-style:italic}
hr.div{border:none;border-top:1px solid #e2e8f0;margin:26px 0}
</style>
"""


# ── Helper ────────────────────────────────────────────────────────────────────
def _show(func, cap=""):
    with plt.rc_context(RC):
        try:
            fig = func()
            st.pyplot(fig, use_container_width=True)
            if cap:
                st.markdown(f'<p class="cap">{cap}</p>', unsafe_allow_html=True)
            plt.close(fig)
        except Exception as e:
            st.error(f"Figure error: {e}")


# ═══════════════════════════════════════════════════════════════════════════════
#  FIGURE 1 — Two sources + circular wavefronts (crest rings)
# ═══════════════════════════════════════════════════════════════════════════════
def _fig_two_sources():
    """Two point sources with solid crest rings, marking constructive/destructive points."""
    with plt.rc_context(RC):
        fig, ax = plt.subplots(figsize=(7.5, 5.8))
        ax.set_aspect('equal')
        ax.set_facecolor('#f0f7ff')
        fig.patch.set_facecolor('#f0f7ff')

        lam = 2.0
        s1 = np.array([0.0,  2.5])
        s2 = np.array([0.0, -2.5])
        R_MAX = 8.5

        # Draw crest rings: every full λ from each source
        n_rings = int(R_MAX / lam) + 1
        for n in range(1, n_rings + 1):
            r = n * lam
            for src, col in [(s1, CB), (s2, CR)]:
                c = plt.Circle(src, r, color=col, fill=False,
                               lw=1.6, alpha=0.7, zorder=3)
                ax.add_patch(c)
            # half-wavelength (trough) rings — thin dashed
            r2 = (n - 0.5) * lam
            for src, col in [(s1, CB), (s2, CR)]:
                c = plt.Circle(src, r2, color=col, fill=False,
                               lw=0.7, alpha=0.3, ls='--', zorder=2)
                ax.add_patch(c)

        # Mark constructive points (Δr = nλ) in the right half
        xv = np.linspace(0.1, 8.2, 400)
        yv = np.linspace(-8, 8, 400)
        X, Y = np.meshgrid(xv, yv)
        R1 = np.sqrt((X - s1[0])**2 + (Y - s1[1])**2)
        R2 = np.sqrt((X - s2[0])**2 + (Y - s2[1])**2)
        DR = np.abs(R1 - R2)
        k  = DR / lam

        # Shade antinodal bands
        for n in range(0, int(R_MAX / lam) + 1):
            mask = np.abs(k - n) < 0.08
            ax.contourf(X, Y, mask.astype(float), levels=[0.5, 1.5],
                        colors=[CG], alpha=0.13, zorder=1)

        # Shade nodal bands
        for n in range(1, int(R_MAX / lam) + 1):
            mask = np.abs(k - (n - 0.5)) < 0.08
            ax.contourf(X, Y, mask.astype(float), levels=[0.5, 1.5],
                        colors=[CRED], alpha=0.10, zorder=1)

        # Antinodal lines (right half)
        d = np.linalg.norm(s1 - s2)
        n_max = int(d / lam)
        for n in range(-n_max, n_max + 1):
            v = n * lam / d
            if abs(v) <= 1:
                th = np.arcsin(v)
                xe = R_MAX * np.cos(th); ye = R_MAX * np.sin(th)
                ax.plot([0, xe], [0, ye], color=CG,
                        lw=2.0 if n == 0 else 1.3,
                        alpha=0.85, zorder=4)
                lbl = 'A₀' if n == 0 else f'A{abs(n)}'
                ax.text(xe * 1.04, ye * 1.04, lbl,
                        color=CG, fontsize=8.5, fontweight='bold',
                        ha='center', va='center')

        # Nodal lines (right half)
        for n in range(1, n_max + 1):
            for sign in [1, -1]:
                v = (n - 0.5) * lam / d
                if abs(v) <= 1:
                    th = np.arcsin(sign * v)
                    xe = R_MAX * np.cos(th); ye = R_MAX * np.sin(th)
                    ax.plot([0, xe], [0, ye], color=CRED,
                            lw=1.0, ls='--', alpha=0.75, zorder=4)
                    ax.text(xe * 1.04, ye * 1.04, f'N{n}',
                            color=CRED, fontsize=7.5,
                            ha='center', va='center')

        # Sources
        for src, col, lbl in [(s1, CB, 'S₁'), (s2, CR, 'S₂')]:
            ax.plot(*src, 'o', color=col, ms=13, zorder=8,
                    markeredgecolor='white', markeredgewidth=1.8)
            ax.text(src[0] - 0.45, src[1], lbl,
                    color=col, fontsize=13, fontweight='bold',
                    ha='right', va='center')

        # d annotation
        ax.annotate('', xy=(-0.6, s1[1]), xytext=(-0.6, s2[1]),
                    arrowprops=dict(arrowstyle='<->', color=CGR, lw=1.5))
        ax.text(-0.95, 0, f'd = {int(d)} cm', color=CGR,
                fontsize=9, ha='center', va='center', rotation=90)

        # λ annotation (one ring)
        ax.annotate('', xy=(0, s1[1] + lam), xytext=(0, s1[1]),
                    arrowprops=dict(arrowstyle='<->', color=CB, lw=1.4))
        ax.text(0.35, s1[1] + lam/2, f'λ={int(lam)} cm',
                color=CB, fontsize=8.5, va='center')

        # Legend
        ap = mpatches.Patch(color=CG, alpha=0.7,
                             label='Antinodal band (constructive)')
        np_ = mpatches.Patch(color=CRED, alpha=0.7,
                              label='Nodal band (destructive)')
        l1  = mpatches.Patch(color=CB, label='Crest rings from S₁', fill=False,
                              linewidth=1.6, edgecolor=CB)
        l2  = mpatches.Patch(color=CR, label='Crest rings from S₂', fill=False,
                              linewidth=1.6, edgecolor=CR)
        ax.legend(handles=[l1, l2, ap, np_], fontsize=8,
                  loc='lower right', framealpha=0.92,
                  edgecolor='#e2e8f0')

        ax.set_xlim(-1.2, 9); ax.set_ylim(-8.5, 8.5)
        ax.set_xlabel('x  (cm)', fontsize=10, color=CGR)
        ax.set_ylabel('y  (cm)', fontsize=10, color=CGR)
        ax.tick_params(labelsize=8, color=CGR)
        ax.set_title(
            f'Two coherent sources  (d = {int(d)} cm,  λ = {int(lam)} cm)\n'
            f'Solid rings = crests  |  Antinodal lines: {2*n_max+1}  |  Nodal lines: {2*n_max}',
            fontsize=9.5, color=CDK, pad=6)
        fig.tight_layout()
    return fig


# ═══════════════════════════════════════════════════════════════════════════════
#  FIGURE 2 — Wave superposition: constructive vs destructive
# ═══════════════════════════════════════════════════════════════════════════════
def _fig_superposition():
    """4-panel: show each wave + resultant for constructive & destructive."""
    with plt.rc_context(RC):
        fig, axes = plt.subplots(2, 3, figsize=(11, 5.8),
                                 gridspec_kw={'hspace': 0.72, 'wspace': 0.22})
        fig.patch.set_facecolor(CBG)
        x = np.linspace(0, 2, 500)   # 2 wavelengths

        rows = [
            # (phase_diff, title, result_col, bg)
            (0,      'CONSTRUCTIVE  (in-phase,  Δr = nλ)',      CG,   '#f0fdf4'),
            (np.pi,  'DESTRUCTIVE  (anti-phase,  Δr = (n−½)λ)', CRED, '#fff5f5'),
        ]
        col_cfg = [
            (CB,   'Wave 1  (from S₁)'),
            (CR,   'Wave 2  (from S₂)'),
        ]

        for row, (dphi, row_title, rcol, rbg) in enumerate(rows):
            w1  = np.sin(2 * np.pi * x)
            w2  = np.sin(2 * np.pi * x + dphi)
            res = w1 + w2

            for col in range(3):
                ax = axes[row, col]
                ax.set_facecolor(rbg)

                if col < 2:
                    y      = w1 if col == 0 else w2
                    color  = col_cfg[col][0]
                    label  = col_cfg[col][1]
                    # crest fill
                    ax.fill_between(x, y, 0, where=(y >= 0),
                                    color='#bfdbfe', alpha=0.55)
                    ax.fill_between(x, y, 0, where=(y < 0),
                                    color='#dbeafe', alpha=0.30)
                    ax.plot(x, y, color=color, lw=2.4)
                    ax.set_title(label, fontsize=9.5, color=color,
                                 fontweight='bold', pad=4)
                else:
                    # Resultant
                    ax.fill_between(x, res, 0, where=(res >= 0),
                                    color='#bbf7d0' if rcol == CG else '#fecaca',
                                    alpha=0.55)
                    ax.fill_between(x, res, 0, where=(res < 0),
                                    color='#d1fae5' if rcol == CG else '#fee2e2',
                                    alpha=0.30)
                    ax.plot(x, res, color=rcol, lw=3.0)
                    ax.set_title('Resultant  (water surface)',
                                 fontsize=9.5, color=rcol,
                                 fontweight='bold', pad=4)

                    # Amplitude annotation
                    amax = np.max(np.abs(res))
                    if amax > 0.05:
                        pk = np.argmax(np.abs(res))
                        ax.annotate(
                            f'  {amax:.0f}A',
                            xy=(x[pk], res[pk]),
                            xytext=(x[pk] + 0.25, res[pk] * 0.7),
                            fontsize=11, color=rcol, fontweight='black',
                            arrowprops=dict(arrowstyle='->', color=rcol, lw=1.8))
                    else:
                        ax.text(1.0, 0.25, 'Amplitude = 0\n(water is still)',
                                ha='center', fontsize=9.5, color=CRED,
                                fontweight='bold')

                ax.axhline(0, color='#94a3b8', lw=0.8, ls=':')
                ax.set_xlim(0, 2); ax.set_ylim(-2.4, 2.4)
                ax.set_xticks([0, 0.5, 1, 1.5, 2])
                ax.set_xticklabels(['0', 'λ/2', 'λ', '3λ/2', '2λ'],
                                   fontsize=8)
                ax.set_yticks([-2, -1, 0, 1, 2])
                ax.set_yticklabels(['-2A', '-A', '0', '+A', '+2A'],
                                   fontsize=8)
                ax.spines[['top', 'right']].set_visible(False)

            # Row label
            axes[row, 0].set_ylabel(row_title, fontsize=9,
                                    color=rcol, fontweight='800',
                                    labelpad=5)

        # + sign between panels
        for row in range(2):
            for mid_x in [0.355, 0.625]:
                fig.text(mid_x, 0.74 - row * 0.43, '+',
                         ha='center', va='center',
                         fontsize=18, color=CGR, fontweight='bold')
            fig.text(0.623 + 0.008, 0.74 - 0 * 0.43, '=',
                     ha='center', va='center',
                     fontsize=18, color=CG, fontweight='bold')
            fig.text(0.623 + 0.008, 0.74 - 1 * 0.43, '=',
                     ha='center', va='center',
                     fontsize=18, color=CRED, fontweight='bold')

        fig.suptitle(
            'Wave Superposition at a fixed point on the water surface',
            fontsize=11, fontweight='bold', color=CDK, y=1.01)
        fig.tight_layout()
    return fig


# ═══════════════════════════════════════════════════════════════════════════════
#  FIGURE 3 — Path difference geometry
# ═══════════════════════════════════════════════════════════════════════════════
def _draw_wave_along_path(ax, src, dst, lam, color, amp=0.28,
                          lw=2.4, zorder=5, phase=0.0):
    """Draw a sine wave travelling from src → dst along the straight path."""
    vec   = dst - src
    dist  = np.linalg.norm(vec)
    uhat  = vec / dist                        # unit tangent
    nhat  = np.array([-uhat[1], uhat[0]])     # unit normal (perpendicular)

    n_pts = 600
    t     = np.linspace(0.0, dist, n_pts)
    osc   = amp * np.sin(2 * np.pi * t / lam + phase)

    pts   = np.array([src + t[i] * uhat + osc[i] * nhat
                      for i in range(n_pts)])
    ax.plot(pts[:, 0], pts[:, 1], color=color, lw=lw,
            solid_capstyle='round', zorder=zorder)


def _fig_path_diff():
    """Geometric diagram with sine waves drawn along r₁ and r₂."""
    with plt.rc_context(RC):
        fig, ax = plt.subplots(figsize=(9, 5.8))
        ax.set_facecolor('#f0f6ff')
        fig.patch.set_facecolor('#f0f6ff')
        ax.axis('off')

        s1 = np.array([0.5, 4.8])
        s2 = np.array([0.5, 0.8])
        P  = np.array([8.8, 3.0])
        lam = 1.2
        r1 = np.linalg.norm(P - s1)
        r2 = np.linalg.norm(P - s2)
        dr = abs(r1 - r2)

        # ── Circular wavefront rings (faint background) ──────────────────
        for src, col in [(s1, CB), (s2, CR)]:
            for n in range(1, 8):
                r = n * lam
                alpha = max(0.07, 0.55 - n * 0.06)
                lw_r  = 1.5 if n % 2 != 0 else 0.9
                c = plt.Circle(src, r, color=col, fill=False,
                               lw=lw_r, alpha=alpha, zorder=2)
                ax.add_patch(c)

        # ── Dashed centre-line along each path ───────────────────────────
        ax.plot([s1[0], P[0]], [s1[1], P[1]], '--',
                color=CB, lw=1.2, alpha=0.45, zorder=3)
        ax.plot([s2[0], P[0]], [s2[1], P[1]], '--',
                color=CR, lw=1.2, alpha=0.45, zorder=3)

        # ── Sine waves along each path ────────────────────────────────────
        _draw_wave_along_path(ax, s1, P, lam, color=CB,
                              amp=0.30, lw=2.6, zorder=5, phase=0.0)
        _draw_wave_along_path(ax, s2, P, lam, color=CR,
                              amp=0.30, lw=2.6, zorder=5, phase=0.0)

        # Source markers
        for src, col, lbl in [(s1, CB, 'S₁'), (s2, CR, 'S₂')]:
            ax.plot(*src, 'o', color=col, ms=14, zorder=7,
                    markeredgecolor='white', markeredgewidth=1.8)
            ax.text(src[0] - 0.4, src[1], lbl,
                    color=col, fontsize=14, fontweight='bold',
                    ha='right', va='center')

        # P marker
        ax.plot(*P, 's', color=CG, ms=13, zorder=7,
                markeredgecolor='white', markeredgewidth=1.8)
        ax.text(P[0] + 0.25, P[1] + 0.22, 'P',
                color=CG, fontsize=14, fontweight='bold')

        # ── r₁ and r₂ labels (offset perpendicular to path) ─────────────
        def _label_path(src, dst, txt, color, side=1):
            """side=+1 above, side=-1 below relative to path normal."""
            vec  = dst - src
            dist = np.linalg.norm(vec)
            uhat = vec / dist
            nhat = np.array([-uhat[1], uhat[0]])  # perpendicular
            mid  = src + 0.52 * vec               # 52% along the path
            off  = mid + side * 0.55 * nhat       # shift perpendicular
            ang  = np.degrees(np.arctan2(vec[1], vec[0]))
            ax.text(off[0], off[1], txt,
                    color=color, fontsize=10, rotation=ang,
                    ha='center', va='center', fontweight='700',
                    bbox=dict(fc='#f0f6ff', ec='none', pad=2, alpha=0.8),
                    zorder=8)

        _label_path(s1, P, f'r₁ = {r1:.1f} cm', CB,  side=+1)
        _label_path(s2, P, f'r₂ = {r2:.1f} cm', CR,  side=-1)

        # ── d annotation ─────────────────────────────────────────────────
        ax.annotate('', xy=(s1[0]-0.4, s1[1]),
                    xytext=(s1[0]-0.4, s2[1]),
                    arrowprops=dict(arrowstyle='<->', color=CGR, lw=1.4))
        ax.text(s1[0]-0.75, (s1[1]+s2[1])/2,
                f'd = {abs(s1[1]-s2[1]):.1f} cm',
                color=CGR, fontsize=8.5, ha='right', va='center')

        # ── λ label on first ring from S₁ ────────────────────────────────
        ax.annotate('', xy=(s1[0], s1[1]+lam), xytext=(s1[0], s1[1]),
                    arrowprops=dict(arrowstyle='<->', color=CB, lw=1.3),
                    zorder=6)
        ax.text(s1[0]+0.35, s1[1]+lam*0.5, f'λ={lam:.1f}cm',
                color=CB, fontsize=8, va='center', zorder=8)

        # ── Δr callout box ────────────────────────────────────────────────
        ax.text(4.8, 6.02,
                f'Δr  =  |r₁ − r₂|  =  {dr:.2f} cm',
                fontsize=13, ha='center', fontweight='bold',
                color='#78350f',
                bbox=dict(boxstyle='round,pad=0.5', fc='#fef3c7',
                          ec='#f59e0b', lw=2.2), zorder=9)

        ax.text(0.5, -0.22,
                'Top view — rings = wave crests,  wavy lines = waves travelling along each path',
                fontsize=8.5, color=CGR, style='italic')
        ax.set_xlim(-0.8, 10.8); ax.set_ylim(-0.3, 6.2)
        fig.tight_layout(pad=0.5)
    return fig


# ═══════════════════════════════════════════════════════════════════════════════
#  FIGURE 4 — Condition summary panels
# ═══════════════════════════════════════════════════════════════════════════════
def _fig_conditions():
    """Two clean panels: constructive / destructive conditions."""
    with plt.rc_context(RC):
        fig, axes = plt.subplots(1, 2, figsize=(10, 3.6))
        fig.patch.set_facecolor(CBG)

        panels = [
            (CG,   '#f0fdf4', '#bbf7d0',
             'CONSTRUCTIVE  (Antinode)',
             r'$\Delta r = n\lambda$',
             r'$n = 0,\;1,\;2,\;3,\;\ldots$',
             'Amplitude = 2A',
             'Crest meets crest'),
            (CRED, '#fef2f2', '#fecaca',
             'DESTRUCTIVE  (Node)',
             r'$\Delta r = (n - \frac{1}{2})\,\lambda$',
             r'$n = 1,\;2,\;3,\;\ldots$',
             'Amplitude = 0',
             'Crest meets trough'),
        ]
        for ax, (col, fc, hc, title, f1, f2, result, sub) in zip(axes, panels):
            ax.set_facecolor(fc)
            ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis('off')
            for sp in ['top','bottom','left','right']:
                ax.spines[sp].set_visible(True)
                ax.spines[sp].set_edgecolor(col)
                ax.spines[sp].set_linewidth(2.5)

            # Header bar
            hbar = FancyBboxPatch((0,0.83), 1, 0.17, boxstyle='square',
                                   fc=hc, ec='none',
                                   transform=ax.transAxes, clip_on=False)
            ax.add_patch(hbar)
            ax.text(0.5, 0.915, title, transform=ax.transAxes,
                    ha='center', va='center', fontsize=10.5,
                    fontweight='800', color=col)

            # Formula lines
            ax.text(0.5, 0.66, f1, transform=ax.transAxes,
                    ha='center', va='center', fontsize=14)
            ax.text(0.5, 0.45, f2, transform=ax.transAxes,
                    ha='center', va='center', fontsize=11)
            ax.text(0.5, 0.24, result, transform=ax.transAxes,
                    ha='center', va='center', fontsize=12,
                    fontweight='800', color=col)
            ax.text(0.5, 0.08, f'({sub})', transform=ax.transAxes,
                    ha='center', va='center', fontsize=9,
                    color=col, style='italic')

        fig.suptitle('Conditions for in-phase coherent sources',
                     fontsize=10.5, color=CGR, y=1.02)
        fig.tight_layout(pad=0.9)
    return fig


# ═══════════════════════════════════════════════════════════════════════════════
#  FIGURE 5 — Antinodal/nodal lines: top-view line diagram
# ═══════════════════════════════════════════════════════════════════════════════
def _fig_pattern():
    """Clean top-view line diagram: antinodal and nodal line directions."""
    with plt.rc_context(RC):
        fig, ax = plt.subplots(figsize=(9.5, 7))
        ax.set_facecolor('#f8fafc')
        fig.patch.set_facecolor('#f8fafc')
        ax.set_aspect('equal')

        d = 10.0; lam = 2.5
        s1 = np.array([0.0,  d/2])
        s2 = np.array([0.0, -d/2])
        n_max = int(d / lam)   # = 4
        R_MAX = 20

        # Light wavefront rings in background
        for src, col in [(s1, CB), (s2, CR)]:
            for n in range(1, 10):
                r = n * lam
                c = plt.Circle(src, r, color=col, fill=False,
                               lw=0.8, alpha=0.18, zorder=1)
                ax.add_patch(c)

        # Antinodal lines (solid green)
        for n in range(-n_max, n_max + 1):
            v = n * lam / d
            if abs(v) <= 1:
                th = np.arcsin(v)
                for sign in [1, -1]:
                    xe = sign * R_MAX * np.cos(th)
                    ye = R_MAX * np.sin(th) * sign
                    ax.plot([0, sign * R_MAX * np.cos(th)],
                            [0, R_MAX * np.sin(th)],
                            color=CG,
                            lw=2.5 if n == 0 else 1.8,
                            alpha=1.0 if n == 0 else 0.85,
                            solid_capstyle='round', zorder=4)
                    break  # draw one direction, mirror below

        # Re-draw properly both directions
        ax.cla()
        ax.set_facecolor('#f8fafc')
        ax.set_aspect('equal')
        for src, col in [(s1, CB), (s2, CR)]:
            for n in range(1, 10):
                r = n * lam
                c = plt.Circle(src, r, color=col, fill=False,
                               lw=0.9, alpha=0.18, zorder=1)
                ax.add_patch(c)

        for n in range(-n_max, n_max + 1):
            v = n * lam / d
            if abs(v) <= 1:
                th = np.arcsin(v)
                cos_t = np.cos(th); sin_t = np.sin(th)
                # Full line through origin in both directions
                ax.plot([-R_MAX * cos_t, R_MAX * cos_t],
                        [-R_MAX * sin_t, R_MAX * sin_t],
                        color=CG,
                        lw=2.6 if n == 0 else 1.9,
                        alpha=1.0 if n == 0 else 0.85,
                        solid_capstyle='round', zorder=4)
                lbl = 'A₀' if n == 0 else f'A{abs(n)}'
                ax.text(R_MAX * cos_t * 1.04, R_MAX * sin_t * 1.04,
                        lbl, color=CG, fontsize=9,
                        fontweight='bold', ha='center', va='center')
                if n != 0:
                    ax.text(-R_MAX * cos_t * 1.04, -R_MAX * sin_t * 1.04,
                            lbl, color=CG, fontsize=9,
                            fontweight='bold', ha='center', va='center')

        # Nodal lines (dashed red)
        for n in range(1, n_max + 1):
            for sign in [1, -1]:
                v = (n - 0.5) * lam / d
                if abs(v) <= 1:
                    th = np.arcsin(sign * v)
                    cos_t = np.cos(th); sin_t = np.sin(th)
                    ax.plot([-R_MAX * cos_t, R_MAX * cos_t],
                            [-R_MAX * sin_t, R_MAX * sin_t],
                            color=CRED, lw=1.3, ls='--',
                            alpha=0.75, zorder=3)
                    ax.text(R_MAX * cos_t * 1.04, R_MAX * sin_t * 1.04,
                            f'N{n}', color=CRED, fontsize=8,
                            ha='center', va='center')
                    ax.text(-R_MAX * cos_t * 1.04, -R_MAX * sin_t * 1.04,
                            f'N{n}', color=CRED, fontsize=8,
                            ha='center', va='center')

        # Sources
        for src, col, lbl in [(s1, CB, 'S₁'), (s2, CR, 'S₂')]:
            ax.plot(*src, 'o', color=col, ms=13, zorder=8,
                    markeredgecolor='white', markeredgewidth=2)
            ax.text(src[0] - 0.6, src[1], lbl, color=col,
                    fontsize=12, fontweight='bold', va='center')

        # d annotation
        ax.annotate('', xy=(-0.7, s1[1]), xytext=(-0.7, s2[1]),
                    arrowprops=dict(arrowstyle='<->', color=CGR, lw=1.5))
        ax.text(-1.3, 0, f'd = {int(d)} cm', color=CGR,
                fontsize=9, ha='center', va='center', rotation=90)
        ax.axhline(0, color=CGR, lw=0.8, ls=':', alpha=0.6)

        # Legend
        h1 = mpatches.Patch(color=CG,   label=f'Antinodal lines  ({2*n_max+1} lines)')
        h2 = mpatches.Patch(color=CRED, label=f'Nodal lines  ({2*n_max} lines)',
                             fill=False, linestyle='--', edgecolor=CRED)
        ax.legend(handles=[h1, h2], fontsize=9, loc='lower right',
                  framealpha=0.95, edgecolor='#e2e8f0')

        ax.set_xlim(-22, 22); ax.set_ylim(-13.5, 13.5)
        ax.set_xlabel('x  (cm)', fontsize=10)
        ax.set_ylabel('y  (cm)', fontsize=10)
        ax.set_title(
            f'd = {int(d)} cm,  λ = {int(lam)} cm   →   '
            f'Antinodal lines: {2*n_max+1}   |   Nodal lines: {2*n_max}',
            fontsize=10, fontweight='600', color=CDK)
        ax.spines[['top','right']].set_visible(False)
        fig.tight_layout()
    return fig


# ═══════════════════════════════════════════════════════════════════════════════
#  FIGURE 6 — S1S2 ruler showing Δr at every position
# ═══════════════════════════════════════════════════════════════════════════════
def _fig_ruler():
    """Precise ruler: antinode / node positions on the S1S2 line."""
    with plt.rc_context(RC):
        fig, ax = plt.subplots(figsize=(12, 4.8))
        ax.set_facecolor(CBG)
        fig.patch.set_facecolor(CBG)
        d = 10.0; lam = 2.0
        ax.set_xlim(-0.8, 11.8); ax.set_ylim(-3.0, 3.2)
        ax.axis('off')

        # S1S2 axis line
        ax.plot([-0.2, 10.5], [0, 0], color=CDK, lw=2.5,
                solid_capstyle='round', zorder=5)

        # Tick marks
        for xi in range(0, 11):
            ax.plot([xi, xi], [-0.18, 0.18], color=CGR, lw=0.9)
            ax.text(xi, -0.38, str(xi), ha='center', fontsize=8, color=CGR)
        ax.text(5, -0.68, 'Position along S₁S₂  (cm)',
                ha='center', fontsize=9, color=CGR)

        # Sources
        for xp, col, lbl in [(0, CB, 'S₁'), (10, CR, 'S₂')]:
            ax.plot(xp, 0, 'o', color=col, ms=16, zorder=7,
                    markeredgecolor='white', markeredgewidth=2)
            ax.text(xp, 0.55, lbl, ha='center', fontsize=12,
                    color=col, fontweight='bold')

        # Plot every half-lambda position
        for xi in np.arange(0.0, d + 0.001, 0.5):
            r1 = xi; r2 = d - xi; dr = abs(r1 - r2)
            k  = dr / lam
            is_anti = abs(k - round(k)) < 0.01
            is_node = abs((k + 0.5) - round(k + 0.5)) < 0.01

            if is_anti:
                n = int(round(k))
                ax.plot(xi, 0, 'D', color=CG, ms=12, zorder=8,
                        markeredgecolor='white', markeredgewidth=1.5)
                ax.text(xi, 1.15, f'A{n}', ha='center', fontsize=8,
                        color=CG, fontweight='bold')
                ax.text(xi, 0.65, f'Δr={int(dr)}',
                        ha='center', fontsize=7, color=CG)
                ax.plot([xi, xi], [0.17, 0.60], color=CG,
                        lw=0.8, alpha=0.5)

            elif is_node:
                n = int(round(k + 0.5))
                ax.plot(xi, 0, 'v', color=CRED, ms=11, zorder=8,
                        markeredgecolor='white', markeredgewidth=1.5)
                ax.text(xi, -1.12, f'N{n}', ha='center', fontsize=8,
                        color=CRED, fontweight='bold')
                ax.text(xi, -1.65, f'Δr={int(dr)}',
                        ha='center', fontsize=7, color=CRED)
                ax.plot([xi, xi], [-0.17, -0.60], color=CRED,
                        lw=0.8, alpha=0.5)

        # Header text
        ax.text(5.0, 2.85,
                f'd = {int(d)} cm,  λ = {int(lam)} cm   '
                f'→   Antinodes = {int(d/lam)*2+1},  Nodes = {int(d/lam)*2}',
                ha='center', fontsize=11, fontweight='700', color=CDK,
                bbox=dict(boxstyle='round,pad=0.4', fc='#f1f5f9',
                          ec='#cbd5e1', lw=1.8))
        # Legend inside axes (no bbox_to_anchor)
        h1 = mpatches.Patch(color=CG,   label='Antinode  (constructive)')
        h2 = mpatches.Patch(color=CRED, label='Node  (destructive)')
        ax.legend(handles=[h1, h2], fontsize=9,
                  loc='upper left',
                  framealpha=0.95, edgecolor='#e2e8f0')
        fig.tight_layout()
    return fig


# ═══════════════════════════════════════════════════════════════════════════════
#  FIGURE 7 — Phase comparison: in-phase vs anti-phase (3-row × 2-col)
# ═══════════════════════════════════════════════════════════════════════════════
def _fig_antiphase_waves():
    """
    Clear 3-row × 2-col comparison:
      Left  col = In-phase sources  (Δφ = 0)
      Right col = Anti-phase sources (Δφ = π)
      Row 1 = Wave from S₁
      Row 2 = Wave from S₂
      Row 3 = Resultant  (what the water surface looks like)
    """
    with plt.rc_context(RC):
        fig = plt.figure(figsize=(11, 7.5))
        fig.patch.set_facecolor(CBG)

        # GridSpec: 3 rows, 2 cols + left margin col for row labels
        from matplotlib.gridspec import GridSpec
        gs = GridSpec(3, 2, figure=fig,
                      hspace=0.55, wspace=0.30,
                      left=0.13, right=0.97, top=0.90, bottom=0.07)

        x = np.linspace(0, 2, 600)  # 2 wavelengths

        col_configs = [
            # (source_phase, col_title, col_title_col, bg_waves, bg_result,
            #  result_col, outcome_lbl)
            (0,      'IN-PHASE sources\n(delta-phi = 0)',
             CG,   '#f0f7ff', '#f0fdf4', CG,   'ANTINODE\nAmplitude = 2A'),
            (np.pi, 'ANTI-PHASE sources\n(delta-phi = pi)',
             CRED, '#fff8f8', '#fff5f5', CRED, 'NODE\nAmplitude = 0'),
        ]

        row_labels  = ['Wave from S₁', 'Wave from S₂', 'Resultant\n(water surface)']
        row_colors  = [CB, CR, CGR]

        for col_i, (src_phase, col_title, title_col,
                    bg_wave, bg_res, rcol, outcome) in enumerate(col_configs):

            w1  = np.sin(2 * np.pi * x)
            w2  = np.sin(2 * np.pi * x + src_phase)
            res = w1 + w2
            waves = [w1, w2, res]
            wave_cols = [CB, CR, rcol]

            for row_i, (y, wc) in enumerate(zip(waves, wave_cols)):
                ax = fig.add_subplot(gs[row_i, col_i])
                bg = bg_res if row_i == 2 else bg_wave
                ax.set_facecolor(bg)
                # Column title sits on the first-row axes (no separate axes needed)
                if row_i == 0:
                    ax.set_title(col_title, fontsize=10.5,
                                 color=title_col, fontweight='800', pad=8)

                # Fill crest/trough
                fill_c = '#bbf7d0' if (row_i == 2 and rcol == CG) else \
                         '#fecaca' if (row_i == 2 and rcol == CRED) else '#dbeafe'
                ax.fill_between(x, y, 0, where=(y >= 0),
                                color=fill_c, alpha=0.50)
                ax.fill_between(x, y, 0, where=(y < 0),
                                color=fill_c, alpha=0.20)

                ax.plot(x, y, color=wc, lw=2.6, solid_capstyle='round')
                ax.axhline(0, color='#94a3b8', lw=0.9, ls=':', zorder=1)

                # Amplitude dashed lines
                amax = np.max(np.abs(y))
                if amax > 0.05:
                    ax.axhline( amax, color=wc, lw=1.0, ls='--', alpha=0.4)
                    ax.axhline(-amax, color=wc, lw=1.0, ls='--', alpha=0.4)

                ax.set_xlim(0, 2); ax.set_ylim(-2.6, 2.6)
                ax.set_xticks([0, 0.5, 1.0, 1.5, 2.0])
                ax.set_xticklabels(['0','λ/2','λ','3λ/2','2λ'], fontsize=8.5)
                ax.set_yticks([-2, -1, 0, 1, 2])
                ax.set_yticklabels(['-2A','-A','0','+A','+2A'], fontsize=8.5)
                ax.spines[['top','right']].set_visible(False)

                # Amplitude label on y-axis right side
                if amax > 0.05:
                    ax.text(2.05, amax, f'{amax:.0f}A',
                            color=wc, fontsize=9, va='center',
                            fontweight='bold')

                # Row label (left side, only for left column)
                if col_i == 0:
                    ax.set_ylabel(row_labels[row_i],
                                  color=row_colors[row_i],
                                  fontsize=9.5, fontweight='700',
                                  labelpad=8)

                # Result badge (bottom-right of resultant row)
                if row_i == 2:
                    badge_fc  = '#dcfce7' if rcol == CG else '#fee2e2'
                    ax.text(0.97, 0.08, outcome,
                            transform=ax.transAxes,
                            ha='right', va='bottom',
                            fontsize=10, fontweight='900',
                            color=rcol,
                            bbox=dict(boxstyle='round,pad=0.35',
                                      fc=badge_fc, ec=rcol, lw=2.2))
                    # Flat-surface note for anti-phase
                    if rcol == CRED and amax < 0.05:
                        ax.text(1.0, 0.6, 'Water surface\nstays flat',
                                transform=ax.transAxes,
                                ha='center', va='center',
                                fontsize=11, color=CRED,
                                fontweight='bold')

            # (column title already set on row 0 axes above)

        # Grand title
        fig.suptitle(
            'In-phase vs Anti-phase Sources  (Δr = 0 at point P)',
            fontsize=12, fontweight='bold', color=CDK, y=0.97)

        # Vertical divider
        fig.add_artist(
            plt.Line2D([0.545, 0.545], [0.05, 0.93],
                       transform=fig.transFigure,
                       color='#e2e8f0', lw=1.5, ls='--'))
    return fig


# ═══════════════════════════════════════════════════════════════════════════════
#  FIGURE 8 — Two openings in barrier (top view, line diagram only)
# ═══════════════════════════════════════════════════════════════════════════════
def _fig_barrier():
    """Top-view line diagram: plane wave → barrier with 2 openings → interference."""
    with plt.rc_context(RC):
        fig, ax = plt.subplots(figsize=(10, 6.5))
        ax.set_facecolor('#f0f7ff')
        fig.patch.set_facecolor('#f0f7ff')
        ax.set_xlim(-4.5, 13); ax.set_ylim(-5.5, 5.5)
        ax.set_aspect('equal')
        ax.axis('off')

        d = 2.0; lam = 0.6
        s1 = np.array([0.0,  d/2])
        s2 = np.array([0.0, -d/2])
        n_max = 3

        # ── Left: incoming plane wave ──
        for xi in np.arange(-4, 0, lam):
            ax.plot([xi, xi], [-5.2, -d/2 - 0.15], color=CB,
                    lw=1.5, alpha=0.5, solid_capstyle='round', zorder=7)
            ax.plot([xi, xi], [d/2 + 0.15, 5.2], color=CB,
                    lw=1.5, alpha=0.5, solid_capstyle='round', zorder=7)

        ax.annotate('', xy=(-0.5, 0), xytext=(-2.5, 0),
                    arrowprops=dict(arrowstyle='->', color=CB,
                                   lw=2.5, mutation_scale=16),
                    zorder=8)
        ax.text(-2.8, 0.6, 'Incoming\nplane wave', color=CB,
                fontsize=9, ha='center', fontweight='600', zorder=8)

        # ── Barrier ──
        gap = 0.25
        for y0, y1 in [(-5.5, -(d/2 + gap)),
                       (-(d/2 - gap), (d/2 - gap)),
                       ((d/2 + gap), 5.5)]:
            ax.fill_between([-0.22, 0.22], y0, y1,
                            color='#475569', alpha=0.92, zorder=5)
        ax.text(-0.9, -4.5, 'Barrier', color='#475569',
                fontsize=9, ha='center', va='top', rotation=90)

        # Openings
        for src, col, lbl in [(s1, CB, 'O₁'), (s2, CR, 'O₂')]:
            ax.plot(*src, 'D', color=col, ms=10, zorder=8,
                    markeredgecolor='white', markeredgewidth=1.5)
            ax.text(0.45, src[1], lbl, color=col,
                    fontsize=9.5, va='center', fontweight='700', zorder=8)

        # d annotation
        ax.annotate('', xy=(-0.7, s1[1]), xytext=(-0.7, s2[1]),
                    arrowprops=dict(arrowstyle='<->', color=CGR, lw=1.4))
        ax.text(-1.05, 0, 'd', fontsize=13, color=CDK,
                ha='center', va='center', fontweight='bold')

        # ── Right: circular wavefronts from O1 and O2 ──
        for src, col in [(s1, CB), (s2, CR)]:
            for n in range(1, 14):
                r = n * lam
                c = plt.Circle(src, r, color=col, fill=False,
                               lw=1.6 if n % 2 != 0 else 0.8,
                               alpha=max(0.06, 0.65 - n * 0.04),
                               zorder=2)
                ax.add_patch(c)
        # Clip circular rings to x > 0 using a mask rectangle (below text zorder)
        from matplotlib.patches import Rectangle
        mask = Rectangle((-4.5, -5.5), 4.5, 11,
                         fc='#f0f7ff', ec='none', zorder=3)
        ax.add_patch(mask)

        # ── Antinodal lines ──
        R_MAX = 12
        for n in range(-n_max, n_max + 1):
            v = n * lam / d
            if abs(v) <= 1:
                th = np.arcsin(v)
                xe = R_MAX * np.cos(th); ye = R_MAX * np.sin(th)
                ax.plot([0, xe], [0, ye], color=CG,
                        lw=2.2 if n == 0 else 1.5, alpha=0.9, zorder=4)
                lbl = 'A₀\n(central)' if n == 0 else f'A{abs(n)}'
                ax.text(xe * 1.04, ye * 1.04, lbl, color=CG,
                        fontsize=8.5, ha='center', va='center',
                        fontweight='bold')

        # Nodal lines
        for n in range(1, n_max + 1):
            for sign in [1, -1]:
                v = (n - 0.5) * lam / d
                if abs(v) <= 1:
                    th = np.arcsin(sign * v)
                    xe = R_MAX * np.cos(th); ye = R_MAX * np.sin(th)
                    ax.plot([0, xe], [0, ye], color=CRED,
                            lw=1.2, ls='--', alpha=0.7, zorder=3)
                    ax.text(xe * 1.04, ye * 1.04, f'N{n}',
                            color=CRED, fontsize=8, ha='center', va='center')

        # θ arc for n=1
        th1 = np.arcsin(lam / d)
        arc = Arc((0, 0), 3.0, 3.0, angle=0,
                  theta1=0, theta2=np.degrees(th1),
                  color='#9333ea', lw=2.0, zorder=5)
        ax.add_patch(arc)
        ax.text(1.6, 0.42, 'θ', fontsize=14, color='#9333ea',
                fontweight='bold', zorder=6)

        # L arrow
        ax.annotate('', xy=(10, -5.3), xytext=(0, -5.3),
                    arrowprops=dict(arrowstyle='<->', color=CGR, lw=1.4))
        ax.text(5, -5.55, 'L  (distance from barrier)',
                ha='center', fontsize=9, color=CGR)

        # Formula box — placed inside the upper-right area of the plot
        ax.text(6.5, 4.5,
                r'$\sin\theta_n = \dfrac{n\lambda}{d}$'
                '     '
                r'$x_n = \dfrac{n\lambda L}{d}$',
                fontsize=10.5, ha='center', fontweight='700', color=CDK,
                bbox=dict(boxstyle='round,pad=0.5', fc='white',
                          ec='#2563eb', lw=2.0), zorder=7)

        ax.set_title(
            'Water wave — two openings in a barrier  (top view)',
            fontsize=10, color=CDK, pad=6, fontweight='600')
        fig.tight_layout(pad=0.4)
    return fig


# ═══════════════════════════════════════════════════════════════════════════════
#  FIGURE 9 — Linked: ring pattern + wave superposition at A / N points
# ═══════════════════════════════════════════════════════════════════════════════
def _draw_wave_cos(ax, src, dst, lam, color,
                   amp=0.23, lw=2.4, zorder=5, alpha=1.0):
    """Cosine wave along src→dst: starts at CREST (+amp) at the source."""
    vec  = np.asarray(dst) - np.asarray(src)
    dist = np.linalg.norm(vec)
    uhat = vec / dist
    nhat = np.array([-uhat[1], uhat[0]])
    t    = np.linspace(0.0, dist, 600)
    osc  = amp * np.cos(2 * np.pi * t / lam)
    pts  = (np.asarray(src)
            + np.outer(t, uhat)
            + np.outer(osc, nhat))
    ax.plot(pts[:, 0], pts[:, 1], color=color, lw=lw, alpha=alpha,
            solid_capstyle='round', zorder=zorder)


def _fig_interference_linked():
    """
    Composite figure linking the interference pattern to wave superposition.
    Left: top-view ring diagram with A₁ and N₁ lines + two example points.
    Right: 3-row wave panels (W1 / W2 / Resultant) for each point.
    """
    with plt.rc_context(RC):
        from matplotlib.gridspec import GridSpec
        fig = plt.figure(figsize=(14, 8.0))
        outer = GridSpec(1, 2, figure=fig,
                         width_ratios=[1.55, 1],
                         wspace=0.28,
                         left=0.03, right=0.98,
                         top=0.91, bottom=0.05)

        ax_map = fig.add_subplot(outer[0])

        # right side: 2 × 3 sub-grid (2 points × 3 wave rows each)
        inner = outer[1].subgridspec(2, 1, hspace=0.55)
        gA    = inner[0].subgridspec(3, 1, hspace=0.05)
        gN    = inner[1].subgridspec(3, 1, hspace=0.05)
        axA   = [fig.add_subplot(gA[i]) for i in range(3)]  # antinode rows
        axN   = [fig.add_subplot(gN[i]) for i in range(3)]  # node rows

        # ── parameters ──────────────────────────────────────────────────────
        d   = 6.0
        lam = 2.0
        s1  = np.array([0.0,  d / 2])   # S₁ at top
        s2  = np.array([0.0, -d / 2])   # S₂ at bottom
        n_max = int(d / lam)            # = 3

        # Exact geometry (derived analytically):
        # P on A₁: r₁=6=3λ, r₂=8=4λ, Δr=2=λ  → Antinode A₁
        P_A  = np.array([np.sqrt(320.0 / 9.0), 7.0 / 3.0])
        r1_A, r2_A = 6.0, 8.0

        # Q on N₁: r₁=7=3.5λ, r₂=8=4λ, Δr=1=λ/2 → Node N₁
        P_N  = np.array([np.sqrt(735.0 / 16.0), 1.25])
        r1_N, r2_N = 7.0, 8.0

        # ── MAP PANEL ────────────────────────────────────────────────────────
        ax_map.set_facecolor('#f0f6ff')
        ax_map.set_aspect('equal')
        ax_map.spines[['top', 'right']].set_visible(False)

        # Faint wavefront rings
        for src, col in [(s1, CB), (s2, CR)]:
            for n in range(1, 7):
                r     = n * lam
                alpha = max(0.06, 0.48 - n * 0.06)
                c     = plt.Circle(src, r, color=col, fill=False,
                                   lw=1.2, alpha=alpha, zorder=1)
                ax_map.add_patch(c)

        # Antinodal lines (green solid)
        for n in range(-n_max, n_max + 1):
            v = n * lam / d
            if abs(v) > 1:
                continue
            th = np.arcsin(v)
            R  = 9.5
            xe = R * np.cos(th); ye = R * np.sin(th)
            lw_an = 2.5 if n == 0 else 1.7
            ax_map.plot([0, xe],  [0, ye],  color=CG, lw=lw_an,
                        alpha=0.75, solid_capstyle='round', zorder=3)
            ax_map.plot([0, -xe], [0, -ye], color=CG, lw=lw_an,
                        alpha=0.75, solid_capstyle='round', zorder=3)
            lbl = 'A₀' if n == 0 else f'A{abs(n)}'
            ax_map.text( xe * 1.06,  ye * 1.06, lbl,
                        color=CG, fontsize=8.5, fontweight='bold', ha='center')
            ax_map.text(-xe * 1.06, -ye * 1.06, lbl,
                        color=CG, fontsize=8.5, fontweight='bold', ha='center')

        # Nodal lines (red dashed)
        for n in range(1, n_max + 1):
            for sign in [1, -1]:
                v = (n - 0.5) * lam / d
                if abs(v) > 1:
                    continue
                th = np.arcsin(sign * v)
                R  = 9.5
                xe = R * np.cos(th); ye = R * np.sin(th)
                ax_map.plot([0, xe],  [0, ye],  color=CRED, lw=1.2,
                            ls='--', alpha=0.65, zorder=3)
                ax_map.plot([0, -xe], [0, -ye], color=CRED, lw=1.2,
                            ls='--', alpha=0.65, zorder=3)
                ax_map.text( xe * 1.06,  ye * 1.06, f'N{n}',
                            color=CRED, fontsize=7.5, ha='center')
                ax_map.text(-xe * 1.06, -ye * 1.06, f'N{n}',
                            color=CRED, fontsize=7.5, ha='center')

        # Cosine waves from S₁ and S₂ to P_A (full opacity, bold)
        _draw_wave_cos(ax_map, s1, P_A, lam, CB,  amp=0.26, lw=2.7, zorder=5)
        _draw_wave_cos(ax_map, s2, P_A, lam, CR,  amp=0.26, lw=2.7, zorder=5)
        # Cosine waves to P_N (slightly lighter)
        _draw_wave_cos(ax_map, s1, P_N, lam, CB,  amp=0.22, lw=2.2,
                       zorder=5, alpha=0.7)
        _draw_wave_cos(ax_map, s2, P_N, lam, CR,  amp=0.22, lw=2.2,
                       zorder=5, alpha=0.7)

        # Centre-line dashes (very faint)
        for pa in [P_A, P_N]:
            ax_map.plot([s1[0], pa[0]], [s1[1], pa[1]],
                        '--', color=CB, lw=0.9, alpha=0.25, zorder=2)
            ax_map.plot([s2[0], pa[0]], [s2[1], pa[1]],
                        '--', color=CR, lw=0.9, alpha=0.25, zorder=2)

        # Phase-alignment badges at P_A and P_N
        # P_A: both arrive at CREST (cos=+1) → double crest badge
        ax_map.plot(*P_A, 'D', color=CG, ms=16, zorder=9,
                    markeredgecolor='white', markeredgewidth=2.0)
        ax_map.text(P_A[0] + 0.28, P_A[1] + 0.38,
                    'P  (Antinode A₁)\nr₁=3λ  r₂=4λ  Δr=λ',
                    color=CG, fontsize=8.5, fontweight='bold',
                    va='bottom', zorder=10)

        # P_N: crest meets trough → X badge
        ax_map.plot(*P_N, 'v', color=CRED, ms=15, zorder=9,
                    markeredgecolor='white', markeredgewidth=2.0)
        ax_map.text(P_N[0] + 0.28, P_N[1] - 0.55,
                    'Q  (Node N₁)\nr₁=3.5λ  r₂=4λ  Δr=λ/2',
                    color=CRED, fontsize=8.5, fontweight='bold',
                    va='top', zorder=10)

        # Sources
        for src, col, lbl in [(s1, CB, 'S₁'), (s2, CR, 'S₂')]:
            ax_map.plot(*src, 'o', color=col, ms=14, zorder=8,
                        markeredgecolor='white', markeredgewidth=2.0)
            ax_map.text(src[0] - 0.42, src[1], lbl,
                        color=col, fontsize=13, fontweight='bold',
                        ha='right', va='center')

        ax_map.set_xlim(-1.2, 11.0)
        ax_map.set_ylim(-5.6, 5.8)
        ax_map.set_xlabel('x  (cm)', fontsize=10, labelpad=4)
        ax_map.set_ylabel('y  (cm)', fontsize=10, labelpad=4)
        ax_map.set_title('Top view  (d = 6 cm, λ = 2 cm)',
                         fontsize=10, color=CGR, pad=6)

        # ── WAVE PANELS ──────────────────────────────────────────────────────
        T  = np.linspace(0, 2, 500)   # 2 periods

        # ── Antinode A₁ ──
        # W1: cos(ωt)  [r₁=3λ → phase = cos(6π) = +1 → same as cos(0)]
        # W2: cos(ωt)  [r₂=4λ → phase = cos(8π) = +1]
        wA1  = np.cos(2 * np.pi * T)
        wA2  = np.cos(2 * np.pi * T)
        wAr  = wA1 + wA2

        wave_data_A = [
            (wA1, CB,   'W₁  (from S₁,  r₁ = 3λ)'),
            (wA2, CR,   'W₂  (from S₂,  r₂ = 4λ)'),
            (wAr, CG,   'Resultant  =  2A'),
        ]
        # (ticks, labels, ylim) for each of the 3 rows
        _spec_A = [
            ([-1, 0, 1], ['-A', '0', 'A'],   (-1.35, 1.35)),
            ([-1, 0, 1], ['-A', '0', 'A'],   (-1.35, 1.35)),
            ([-2, 0, 2], ['-2A', '0', '2A'], (-2.50, 2.50)),
        ]

        # Header for antinode block
        axA[0].set_facecolor('#ecfdf5')
        axA[0].text(0.5, 1.18,
                    'At  P  →  ANTINODE A₁    (Δr = λ,  in-phase)',
                    transform=axA[0].transAxes,
                    ha='center', va='bottom', fontsize=9.5,
                    fontweight='800', color=CG)

        for ax_w, (w, col, lbl), (tks, tkl, ylim) in zip(axA, wave_data_A, _spec_A):
            ax_w.set_facecolor('#ecfdf5' if col != CG else '#dcfce7')
            ax_w.axhline(0, color='#94a3b8', lw=0.8, ls=':')
            ax_w.plot(T, w, color=col, lw=2.2)
            ax_w.fill_between(T, 0, w, color=col, alpha=0.12)
            ax_w.set_xlim(0, 2); ax_w.set_ylim(*ylim)
            ax_w.set_xticks([])
            ax_w.set_yticks(tks)
            ax_w.set_yticklabels(tkl, fontsize=7)
            ax_w.text(0.01, 0.82, lbl, transform=ax_w.transAxes,
                      fontsize=8, color=col, fontweight='700',
                      va='center')
            for sp in ['top', 'right', 'bottom']:
                ax_w.spines[sp].set_visible(False)
            ax_w.spines['left'].set_color('#cbd5e1')

        axA[2].set_xticks([0, 0.5, 1.0, 1.5, 2.0])
        axA[2].set_xticklabels(['0', 'T/2', 'T', '3T/2', '2T'], fontsize=7)
        # Highlight crest-meets-crest at t=0
        for ax_w in axA[:2]:
            ax_w.axvline(0, color='#f59e0b', lw=2.0, ls='--', alpha=0.9, zorder=5)
            ax_w.axvline(1, color='#f59e0b', lw=2.0, ls='--', alpha=0.9, zorder=5)
        axA[0].text(0.04, 1.0, 'crest', transform=axA[0].transAxes,
                    fontsize=7, color='#d97706', fontweight='bold')

        # ── Node N₁ ──
        # W1: -cos(ωt)  [r₁=3.5λ → cos(7π) = -1 → arrives at TROUGH]
        # W2: cos(ωt)   [r₂=4λ  → cos(8π) = +1 → arrives at CREST]
        wN1  = -np.cos(2 * np.pi * T)
        wN2  =  np.cos(2 * np.pi * T)
        wNr  = wN1 + wN2   # = 0 always

        wave_data_N = [
            (wN1, CB,   'W₁  (from S₁,  r₁ = 3.5λ)'),
            (wN2, CR,   'W₂  (from S₂,  r₂ = 4λ)'),
            (wNr, '#94a3b8', 'Resultant  =  0'),
        ]
        _spec_N = [
            ([-1, 0, 1], ['-A', '0', 'A'],  (-1.35, 1.35)),
            ([-1, 0, 1], ['-A', '0', 'A'],  (-1.35, 1.35)),
            ([0],        ['0'],             (-1.35, 1.35)),   # flat zero
        ]

        axN[0].set_facecolor('#fff1f2')
        axN[0].text(0.5, 1.18,
                    'At  Q  →  NODE N₁    (Δr = λ/2,  anti-phase)',
                    transform=axN[0].transAxes,
                    ha='center', va='bottom', fontsize=9.5,
                    fontweight='800', color=CRED)

        for ax_w, (w, col, lbl), (tks, tkl, ylim) in zip(axN, wave_data_N, _spec_N):
            bg = '#fff1f2' if col != '#94a3b8' else '#f1f5f9'
            ax_w.set_facecolor(bg)
            ax_w.axhline(0, color='#94a3b8', lw=0.8, ls=':')
            ax_w.plot(T, w, color=col, lw=2.2)
            ax_w.fill_between(T, 0, w, color=col, alpha=0.12)
            ax_w.set_xlim(0, 2); ax_w.set_ylim(*ylim)
            ax_w.set_xticks([])
            ax_w.set_yticks(tks)
            ax_w.set_yticklabels(tkl, fontsize=7)
            ax_w.text(0.01, 0.82, lbl, transform=ax_w.transAxes,
                      fontsize=8, color=col, fontweight='700',
                      va='center')
            for sp in ['top', 'right', 'bottom']:
                ax_w.spines[sp].set_visible(False)
            ax_w.spines['left'].set_color('#cbd5e1')

        axN[2].set_xticks([0, 0.5, 1.0, 1.5, 2.0])
        axN[2].set_xticklabels(['0', 'T/2', 'T', '3T/2', '2T'], fontsize=7)
        # Highlight crest-meets-trough at t=0
        axN[0].axvline(0, color='#f59e0b', lw=2.0, ls='--', alpha=0.9, zorder=5)
        axN[1].axvline(0, color='#f59e0b', lw=2.0, ls='--', alpha=0.9, zorder=5)
        axN[0].text(0.04, 0.08, 'trough', transform=axN[0].transAxes,
                    fontsize=7, color='#d97706', fontweight='bold')
        axN[1].text(0.04, 1.0, 'crest', transform=axN[1].transAxes,
                    fontsize=7, color='#d97706', fontweight='bold')

        # Zero-line label for resultant
        axN[2].text(0.5, 0.55, 'amplitude = 0',
                    transform=axN[2].transAxes,
                    ha='center', fontsize=9, color='#64748b',
                    fontweight='bold')

        fig.suptitle(
            'Why is this an Antinode?  Why is that a Node?'
            '  —  Follow the waves!',
            fontsize=12, fontweight='bold', color=CDK, y=0.96)

    return fig


# ═══════════════════════════════════════════════════════════════════════════════
#  FIGURE 10 — 3-step flowchart
# ═══════════════════════════════════════════════════════════════════════════════
def _fig_flowchart():
    with plt.rc_context(RC):
        fig, ax = plt.subplots(figsize=(10, 3.0))
        ax.axis('off')
        ax.set_facecolor(CBG)
        fig.patch.set_facecolor(CBG)
        ax.set_xlim(0, 10); ax.set_ylim(0, 3.0)

        steps = [
            (1.25, '#1e3a8a', '#eff6ff',
             'Step 1',
             r'$\Delta r = |r_1 - r_2|$'),
            (4.00, '#065f46', '#f0fdf4',
             'Step 2',
             r'$k = \Delta r \;/\; \lambda$'),
            (6.75, '#78350f', '#fefce8',
             'Step 3',
             'Is k integer or half-integer?'),
        ]
        for xc, bc, fc, title, body in steps:
            box = FancyBboxPatch((xc-1.08, 0.45), 2.16, 2.1,
                                  boxstyle='round,pad=0.09',
                                  fc=fc, ec=bc, lw=2.4)
            ax.add_patch(box)
            ax.text(xc, 2.38, title, ha='center', va='center',
                    fontsize=9.5, fontweight='800', color=bc)
            ax.text(xc, 1.5, body, ha='center', va='center',
                    fontsize=11.5)

        # Arrows
        for xa in [2.35, 5.10]:
            ax.annotate('', xy=(xa+0.57, 1.5), xytext=(xa, 1.5),
                        arrowprops=dict(arrowstyle='->',
                                        color='#94a3b8', lw=2.2))

        # Branch from Step 3
        ax.annotate('', xy=(7.93, 2.35), xytext=(7.85, 1.5),
                    arrowprops=dict(arrowstyle='->', color=CG, lw=1.9))
        ax.annotate('', xy=(7.93, 0.65), xytext=(7.85, 1.5),
                    arrowprops=dict(arrowstyle='->', color=CRED, lw=1.9))

        for yc, col, fc2, txt in [
            (2.4,  CG,   '#dcfce7', 'k = 0,1,2,…\n→ ANTINODE'),
            (0.60, CRED, '#fee2e2', 'k = ½,1½,…\n→  NODE'),
        ]:
            box = FancyBboxPatch((7.96, yc - 0.40), 1.96, 0.80,
                                  boxstyle='round,pad=0.07',
                                  fc=fc2, ec=col, lw=2.0)
            ax.add_patch(box)
            ax.text(8.94, yc, txt, ha='center', va='center',
                    fontsize=8.8, color=col, fontweight='700')

        ax.set_title('3-Step Method — for every interference problem',
                     fontsize=10.5, color=CGR, pad=5)
        fig.tight_layout(pad=0.4)
    return fig


# ═══════════════════════════════════════════════════════════════════════════════
#  MAIN RENDER
# ═══════════════════════════════════════════════════════════════════════════════
def render_summary():
    st.markdown(_CSS, unsafe_allow_html=True)

    # ── Hero ──────────────────────────────────────────────────────────────────
    st.markdown("""
<div class="hero">
  <h1>Water Wave Interference</h1>
  <p>Complete Summary &nbsp;&middot;&nbsp; Formulas, Diagrams &amp; Worked Examples</p>
</div>
""", unsafe_allow_html=True)

    # ─────────────────────────────────────────────────────────────────────────
    # 01  SUPERPOSITION PRINCIPLE
    # ─────────────────────────────────────────────────────────────────────────
    st.markdown('<p class="sh"><span class="pill">01</span>'
                'Superposition Principle — How Does Interference Arise?</p>',
                unsafe_allow_html=True)

    c1, c2 = st.columns([1, 1.1], gap="large")
    with c1:
        st.markdown("""
<div class="card cb">
<h4>Superposition Principle</h4>
<p>When two water waves meet, the water-surface displacement at that point
equals the <strong>algebraic sum</strong> of the two individual displacements.</p>
<ul>
<li><strong>Crest + Crest</strong> &rarr; surface rises to <em>2&times; amplitude</em> (constructive)</li>
<li><strong>Crest + Trough</strong> &rarr; surface stays flat, amplitude = 0 (destructive)</li>
</ul>
</div>
<div class="card cs" style="margin-top:10px">
<h4>Source Requirements</h4>
<p>Sources must be <strong>coherent</strong> &mdash;<br>
same frequency &amp; constant phase difference.<br>
In the ripple tank: two dippers on the <em>same vibrating bar</em>.</p>
</div>
""", unsafe_allow_html=True)
    with c2:
        _show(_fig_superposition,
              "Top: crest meets crest &rarr; 2A (constructive) &nbsp;|&nbsp; "
              "Bottom: crest meets trough &rarr; net = 0 (destructive)")

    # ─────────────────────────────────────────────────────────────────────────
    # 02  INTERFERENCE PATTERN — TOP VIEW
    # ─────────────────────────────────────────────────────────────────────────
    st.markdown('<hr class="div"><p class="sh"><span class="pill">02</span>'
                'Interference Pattern — Top View</p>',
                unsafe_allow_html=True)

    _show(_fig_two_sources,
          "Blue rings = crests from S&#x2081; &nbsp;|&nbsp; "
          "Red rings = crests from S&#x2082; &nbsp;|&nbsp; "
          "Green band = constructive (antinode) &nbsp;|&nbsp; "
          "Red band = destructive (node)")

    st.markdown("""
<div class="card cb">
<h4>How to Read This Diagram</h4>
<ul>
<li><strong>Blue rings</strong> = wave crests radiating from S&#x2081;</li>
<li><strong>Red rings</strong> = wave crests radiating from S&#x2082;</li>
<li>Where blue + blue rings cross &rarr; <strong class="tg">crest meets crest &rarr; ANTINODE</strong></li>
<li>Where blue + red rings cross &rarr; <strong class="tr">crest meets trough &rarr; NODE</strong></li>
<li>Green solid line through all antinodes &rarr; <strong>antinodal line</strong></li>
<li>Red dashed line through all nodes &rarr; <strong>nodal line</strong></li>
</ul>
</div>
""", unsafe_allow_html=True)

    # ─────────────────────────────────────────────────────────────────────────
    # 03  PATH DIFFERENCE  Δr
    # ─────────────────────────────────────────────────────────────────────────
    st.markdown('<hr class="div"><p class="sh"><span class="pill">03</span>'
                'Path Difference &Delta;r</p>',
                unsafe_allow_html=True)

    c1, c2 = st.columns([1.1, 1], gap="large")
    with c1:
        _show(_fig_path_diff,
              "Rings = wave crests &nbsp;|&nbsp; "
              "Wavy lines = waves travelling along each path from S&#x2081; and S&#x2082; to P")
    with c2:
        st.markdown('<div class="card cb"><h4>Definition</h4></div>',
                    unsafe_allow_html=True)
        st.latex(r"\Delta r \;=\; |r_1 - r_2|")
        st.markdown("""
<div class="card cb" style="margin-top:12px">
<h4>Why Does &Delta;r Matter?</h4>
<p>Wave from S&#x2081; travels distance r&#x2081;. &nbsp;Wave from S&#x2082; travels r&#x2082;.<br>
If &Delta;r = n&lambda; &rarr; difference is exactly <em>n whole cycles</em>
&rarr; both arrive at P <strong>in phase</strong> &rarr;
<strong class="tg">constructive</strong><br>
If &Delta;r = (n&minus;&frac12;)&lambda; &rarr; half-cycle offset
&rarr; arrive <strong>180&deg; out of phase</strong> &rarr;
<strong class="tr">destructive</strong></p>
</div>
""", unsafe_allow_html=True)

    # ─────────────────────────────────────────────────────────────────────────
    # 04  CONDITIONS FOR ANTINODES AND NODES
    # ─────────────────────────────────────────────────────────────────────────
    st.markdown('<hr class="div"><p class="sh"><span class="pill">04</span>'
                'Conditions for Antinodes and Nodes</p>',
                unsafe_allow_html=True)

    _show(_fig_conditions)

    c1, c2 = st.columns(2, gap="large")
    with c1:
        st.markdown('<div class="card cg"><h4>Antinode (Constructive Interference)</h4></div>',
                    unsafe_allow_html=True)
        st.latex(r"\Delta r = n\lambda \qquad n = 0,\,1,\,2,\,3,\,\ldots")
        st.markdown("Resultant amplitude = **2A** &nbsp;(maximum)")
    with c2:
        st.markdown('<div class="card cr"><h4>Node (Destructive Interference)</h4></div>',
                    unsafe_allow_html=True)
        st.latex(r"\Delta r = \left(n - \tfrac{1}{2}\right)\lambda \qquad n = 1,\,2,\,3,\,\ldots")
        st.markdown("Resultant amplitude = **0** &nbsp;(water surface stays flat)")

    # ─────────────────────────────────────────────────────────────────────────
    # 04b  WHY IS THIS AN ANTINODE? WHY IS THAT A NODE?
    # ─────────────────────────────────────────────────────────────────────────
    st.markdown('<hr class="div"><p class="sh"><span class="pill">04b</span>'
                'Why Is This Point an Antinode? Why Is That One a Node?'
                ' &mdash; Follow the Waves!</p>',
                unsafe_allow_html=True)

    st.markdown("""
<div class="card cb">
<h4>Track the Arrival Phase of Each Wave</h4>
<p>Each wave travels a different distance (r&#x2081; or r&#x2082;) before reaching the point.<br>
If r = n&lambda; &rarr; exactly <em>n full cycles</em> &rarr;
<strong>arrives back at CREST</strong> (same phase as when it left the source).<br>
If r = (n + &frac12;)&lambda; &rarr; half-cycle leftover &rarr;
<strong>arrives at TROUGH</strong> (opposite phase).</p>
</div>
""", unsafe_allow_html=True)

    _show(_fig_interference_linked,
          "Left: interference map &mdash; antinodal lines A (green solid) and nodal lines N (red dashed), "
          "with example points P (&diams;) on A&#x2081; and Q (&triangledown;) on N&#x2081;. &nbsp;|&nbsp; "
          "Right: wave graphs W&#x2081; + W&#x2082; = Resultant at each point. "
          "Orange dashed lines mark t = 0 (when sources emit a crest).")

    c1, c2 = st.columns(2, gap="large")
    with c1:
        st.markdown("""
<div class="card cg">
<h4>Point P on Antinode A&#x2081;</h4>
<ul>
<li>r&#x2081; = 6 cm = 3&lambda; &rarr; 3 full cycles &rarr; arrives as <strong>CREST</strong></li>
<li>r&#x2082; = 8 cm = 4&lambda; &rarr; 4 full cycles &rarr; arrives as <strong>CREST</strong></li>
<li>&Delta;r = 2 cm = <strong>1&lambda;</strong> &rarr; crest meets crest</li>
<li>Resultant amplitude = <strong class="tg">2A</strong></li>
</ul>
</div>
""", unsafe_allow_html=True)
    with c2:
        st.markdown("""
<div class="card cr">
<h4>Point Q on Node N&#x2081;</h4>
<ul>
<li>r&#x2081; = 7 cm = 3.5&lambda; &rarr; 3.5 cycles &rarr; arrives as <strong>TROUGH</strong></li>
<li>r&#x2082; = 8 cm = 4&lambda; &nbsp;&rarr; 4 full cycles &rarr; arrives as <strong>CREST</strong></li>
<li>&Delta;r = 1 cm = <strong>&lambda;/2</strong> &rarr; crest meets trough</li>
<li>Resultant amplitude = <strong class="tr">0</strong></li>
</ul>
</div>
""", unsafe_allow_html=True)

    # ─────────────────────────────────────────────────────────────────────────
    # 05  PROBLEM-SOLVING METHOD
    # ─────────────────────────────────────────────────────────────────────────
    st.markdown('<hr class="div"><p class="sh"><span class="pill">05</span>'
                'Problem-Solving Method &mdash; 3 Steps</p>',
                unsafe_allow_html=True)

    _show(_fig_flowchart)

    c1, c2 = st.columns(2, gap="large")
    with c1:
        st.markdown("""
<div class="card cy">
<h4>Worked Example 1 &nbsp;(Q43)</h4>
<p>d = 10 cm, &lambda; = 2.5 cm<br>
Point A: r&#x2081; = 12 cm, r&#x2082; = 17 cm</p>
<ul>
<li>&Delta;r = |12 &minus; 17| = <strong>5 cm</strong></li>
<li>k = 5 &div; 2.5 = <strong>2.0</strong> &nbsp;(integer)</li>
<li>&rarr; <strong class="tg">Antinode A&#x2082;</strong></li>
</ul>
</div>
""", unsafe_allow_html=True)
    with c2:
        st.markdown("""
<div class="card cy">
<h4>Worked Example 2 &nbsp;(Q43)</h4>
<p>&lambda; = 2.5 cm<br>
Point B: r&#x2081; = 14.5 cm, r&#x2082; = 15.75 cm</p>
<ul>
<li>&Delta;r = |14.5 &minus; 15.75| = <strong>1.25 cm</strong></li>
<li>k = 1.25 &div; 2.5 = <strong>0.5</strong> &nbsp;(ends in .5)</li>
<li>&rarr; <strong class="tr">Node N&#x2081;</strong></li>
</ul>
</div>
""", unsafe_allow_html=True)

    # ─────────────────────────────────────────────────────────────────────────
    # 06  FULL INTERFERENCE PATTERN
    # ─────────────────────────────────────────────────────────────────────────
    st.markdown('<hr class="div"><p class="sh"><span class="pill">06</span>'
                'Full Interference Pattern</p>',
                unsafe_allow_html=True)

    _show(_fig_pattern,
          "Green solid lines = antinodal lines (constructive) &nbsp;|&nbsp; "
          "Red dashed lines = nodal lines (destructive)")

    # ─────────────────────────────────────────────────────────────────────────
    # 07  COUNTING ANTINODAL AND NODAL LINES
    # ─────────────────────────────────────────────────────────────────────────
    st.markdown('<hr class="div"><p class="sh"><span class="pill">07</span>'
                'Counting Antinodal and Nodal Lines</p>',
                unsafe_allow_html=True)

    _show(_fig_ruler,
          "Antinodes (&diams;) and nodes (&triangledown;) along the S&#x2081;S&#x2082; axis "
          "&nbsp;(d = 10 cm, &lambda; = 2 cm)")

    st.markdown('<div class="card cb"><h4>Formula &mdash; Find n<sub>max</sub> First</h4></div>',
                unsafe_allow_html=True)
    st.latex(r"n_{\max} = \left\lfloor \frac{d}{\lambda} \right\rfloor "
             r"\quad \text{(integer part only — drop any remainder)}")

    c1, c2 = st.columns(2, gap="large")
    with c1:
        st.markdown("**Total antinodal lines (including A&#x2080;):**")
        st.latex(r"2\,n_{\max} + 1")
    with c2:
        st.markdown("**Total nodal lines:**")
        st.latex(r"2\,n_{\max}")

    st.markdown("""
<table class="rt">
<thead><tr>
  <th>What to count</th>
  <th>On the S&#x2081;S&#x2082; axis (includes S&#x2081;, S&#x2082;)</th>
  <th>Between S&#x2081; and S&#x2082; (excludes endpoints)</th>
</tr></thead>
<tbody>
<tr><td><strong>Antinodes</strong></td>
    <td class="tg">2n&#x2080; + 1</td>
    <td class="tg">2n&#x2080; &minus; 1</td></tr>
<tr><td><strong>Nodes</strong></td>
    <td class="tr">2n&#x2080;</td>
    <td class="tr">2(n&#x2080; &minus; 1)</td></tr>
</tbody>
</table>
<p style="font-size:.8rem;color:#64748b;margin-top:5px">
* Valid when d is an exact multiple of &lambda;, i.e. d = n&#x2080;&lambda;
</p>
""", unsafe_allow_html=True)

    st.markdown("""
<div class="card cy">
<h4>Worked Examples &nbsp;(Q44 &amp; Q45)</h4>
<p>d = 12 cm, &lambda; = 4 cm &nbsp;&rarr;&nbsp; n&#x2080; = 12/4 = <strong>3</strong></p>
<ul>
<li>Total antinodal lines = 2&times;3 + 1 = <strong class="tg">7 lines</strong></li>
<li>Total nodal lines = 2&times;3 = <strong class="tr">6 lines</strong></li>
</ul>
<hr style="border:none;border-top:1px solid #e2e8f0;margin:10px 0">
<p>d = 25 cm, &lambda; = 5 cm &nbsp;&rarr;&nbsp; n&#x2080; = 5</p>
<ul>
<li>Antinodes on S&#x2081;S&#x2082; = 2&times;5 + 1 = <strong class="tg">11</strong>
&nbsp;|&nbsp; between S&#x2081;S&#x2082; = 2&times;5 &minus; 1 = <strong class="tg">9</strong></li>
<li>Nodes on S&#x2081;S&#x2082; = 2&times;5 = <strong class="tr">10</strong>
&nbsp;|&nbsp; between S&#x2081;S&#x2082; = 2(5 &minus; 1) = <strong class="tr">8</strong></li>
</ul>
</div>
""", unsafe_allow_html=True)

    # ─────────────────────────────────────────────────────────────────────────
    # 08  ANTI-PHASE SOURCES
    # ─────────────────────────────────────────────────────────────────────────
    st.markdown('<hr class="div"><p class="sh"><span class="pill">08</span>'
                'Special Case: Anti-Phase Sources (&Delta;&phi; = 180&deg;)</p>',
                unsafe_allow_html=True)

    _show(_fig_antiphase_waves,
          "Left: in-phase sources &rarr; antinode (amplitude 2A) at &Delta;r = 0 &nbsp;|&nbsp; "
          "Right: anti-phase sources &rarr; node (amplitude 0) at &Delta;r = 0")

    c1, c2 = st.columns(2, gap="large")
    with c1:
        st.markdown("""
<div class="card cr">
<h4>All Conditions Swap!</h4>
<p>When sources are 180&deg; out of phase, the antinode/node conditions
<strong>reverse completely</strong>.</p>
</div>
""", unsafe_allow_html=True)
        st.markdown("""
<table class="rt">
<thead><tr><th>&Delta;r</th><th>In-phase sources</th><th>Anti-phase sources</th></tr></thead>
<tbody>
<tr><td>0, &lambda;, 2&lambda;, &hellip;</td>
    <td class="tg">Antinode</td>
    <td class="tr">Node</td></tr>
<tr><td>&lambda;/2, 3&lambda;/2, &hellip;</td>
    <td class="tr">Node</td>
    <td class="tg">Antinode</td></tr>
</tbody>
</table>
""", unsafe_allow_html=True)
    with c2:
        st.markdown("""
<div class="card cy">
<h4>Why?</h4>
<p>Anti-phase sources already have a built-in 180&deg; phase difference.<br>
&Delta;r = 0 &rarr; adds 0&deg; &rarr; total = 180&deg;
&rarr; <strong class="tr">Node</strong><br>
&Delta;r = &lambda;/2 &rarr; adds 180&deg; &rarr; total = 360&deg; = 0&deg;
&rarr; <strong class="tg">Antinode</strong></p>
</div>
""", unsafe_allow_html=True)

    # ─────────────────────────────────────────────────────────────────────────
    # 09  TWO OPENINGS IN A BARRIER
    # ─────────────────────────────────────────────────────────────────────────
    st.markdown('<hr class="div"><p class="sh"><span class="pill">09</span>'
                'Water Wave Through Two Openings in a Barrier</p>',
                unsafe_allow_html=True)

    _show(_fig_barrier,
          "Plane wave passes through openings O&#x2081; and O&#x2082;, "
          "diffracts into circular waves, and produces an interference pattern to the right.")

    c1, c2 = st.columns(2, gap="large")
    with c1:
        st.markdown("**Antinodal angle at order n:**")
        st.latex(r"\sin\theta_n = \frac{n\lambda}{d}")
        st.markdown("**Distance from centre line (small-angle approx.):**")
        st.latex(r"x_n = \frac{n\lambda L}{d}")
        st.markdown("**Spacing between adjacent antinodal lines:**")
        st.latex(r"\Delta x = \frac{\lambda L}{d}")
    with c2:
        st.markdown("""
<div class="card cg">
<h4>Worked Example &nbsp;(Q50)</h4>
<p>d = 4 cm, &lambda; = 2 cm, L = 30 cm</p>
<ul>
<li>x&#x2081; = (1 &times; 2 &times; 30) / 4 = <strong>15 cm</strong></li>
<li>x&#x2082; = (2 &times; 2 &times; 30) / 4 = <strong>30 cm</strong></li>
<li>&Delta;x = (2 &times; 30) / 4 = <strong>15 cm</strong></li>
</ul>
</div>
<div class="card cr" style="margin-top:10px">
<h4>Nodal angle at order n:</h4>
</div>
""", unsafe_allow_html=True)
        st.latex(r"\sin\theta_n = \frac{(n-\tfrac{1}{2})\lambda}{d}")

    # ─────────────────────────────────────────────────────────────────────────
    # REFERENCE TABLE
    # ─────────────────────────────────────────────────────────────────────────
    st.markdown('<hr class="div"><p class="sh"><span class="pill">REF</span>'
                'Complete Formula Reference</p>',
                unsafe_allow_html=True)

    st.markdown("""
<table class="rt">
<thead><tr>
  <th>Quantity</th>
  <th>Antinode (Constructive)</th>
  <th>Node (Destructive)</th>
</tr></thead>
<tbody>
<tr><td><strong>&Delta;r condition (in-phase sources)</strong></td>
    <td class="tg">&Delta;r = 0, &lambda;, 2&lambda;, &hellip;</td>
    <td class="tr">&Delta;r = &lambda;/2, 3&lambda;/2, &hellip;</td></tr>
<tr><td><strong>&Delta;r condition (anti-phase sources)</strong></td>
    <td class="tg">&Delta;r = &lambda;/2, 3&lambda;/2, &hellip;</td>
    <td class="tr">&Delta;r = 0, &lambda;, 2&lambda;, &hellip;</td></tr>
<tr><td><strong>No. of lines (in-phase)</strong></td>
    <td class="tg">2n<sub>max</sub> + 1</td>
    <td class="tr">2n<sub>max</sub></td></tr>
<tr><td><strong>Angle of n-th line</strong></td>
    <td class="tg">sin &theta; = n&lambda;/d</td>
    <td class="tr">sin &theta; = (n&minus;&frac12;)&lambda;/d</td></tr>
<tr><td><strong>Distance on screen (small &theta;)</strong></td>
    <td class="tg">x = n&lambda;L/d</td>
    <td class="tr">x = (n&minus;&frac12;)&lambda;L/d</td></tr>
<tr><td><strong>Resultant amplitude</strong></td>
    <td class="tg">2A</td>
    <td class="tr">0</td></tr>
</tbody>
</table>
""", unsafe_allow_html=True)

    st.info(
        "**Key tip:** For every interference problem: "
        "find Δr → divide by λ → "
        "integer result = **Antinode** / result ending in .5 = **Node**"
    )
