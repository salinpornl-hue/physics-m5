"""
summary.py — สรุปการแทรกสอดของคลื่น (Professional Edition)
All Thai text in Streamlit markdown. Matplotlib figures use English-only labels.
"""
import streamlit as st
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.gridspec as gridspec
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.font_manager as fm

# ── Font configuration ────────────────────────────────────────────────────────
_THAI_CANDIDATES = ['Tahoma', 'Arial Unicode MS', 'Browallia New',
                    'AngsanaUPC', 'Cordia New', 'FreeSans']
_available = {f.name for f in fm.fontManager.ttflist}
_thai_font = next((f for f in _THAI_CANDIDATES if f in _available), 'DejaVu Sans')

STYLE = {
    'font.family':        _thai_font,
    'axes.unicode_minus': False,
    'axes.spines.top':    False,
    'axes.spines.right':  False,
    'axes.linewidth':     0.8,
    'xtick.direction':    'out',
    'ytick.direction':    'out',
    'xtick.major.size':   4,
    'ytick.major.size':   4,
    'figure.dpi':         130,
    'savefig.bbox':       'tight',
}

# Palette
C1   = '#1e40af'   # blue  — source 1
C2   = '#b91c1c'   # red   — source 2
CPOS = '#15803d'   # green — constructive
CNEG = '#dc2626'   # red   — destructive
CGRAY= '#64748b'
CDARK= '#0f172a'
CBGF = '#f8fafc'   # figure bg

# ── CSS ───────────────────────────────────────────────────────────────────────
_CSS = """
<style>
.pro-hero {
    background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 60%, #1d4ed8 100%);
    border-radius: 16px;
    padding: 40px 36px 32px;
    margin-bottom: 32px;
    color: white;
}
.pro-hero h1 {
    font-size: 2.2rem; font-weight: 800; margin: 0 0 6px 0;
    letter-spacing: -0.5px;
}
.pro-hero p { font-size: 1.05rem; color: #93c5fd; margin: 0; }

.sec-head {
    font-size: 1.25rem; font-weight: 700; color: #0f172a;
    border-bottom: 2px solid #3b82f6;
    padding-bottom: 6px; margin: 32px 0 16px 0;
    letter-spacing: -0.2px;
}
.pill {
    display: inline-block;
    background: #eff6ff; color: #1d4ed8;
    font-size: 0.72rem; font-weight: 700;
    padding: 2px 9px; border-radius: 20px;
    letter-spacing: 0.5px; text-transform: uppercase;
    margin-right: 8px; vertical-align: middle;
}
.card {
    background: #fff; border: 1px solid #e2e8f0;
    border-radius: 12px; padding: 20px 22px; margin: 12px 0;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
}
.card-blue  { border-left: 4px solid #3b82f6; }
.card-green { border-left: 4px solid #16a34a; }
.card-red   { border-left: 4px solid #dc2626; }
.card-amber { border-left: 4px solid #d97706; }
.card-gray  { border-left: 4px solid #94a3b8; }
.card h4    { margin: 0 0 8px 0; font-size: 0.9rem;
              font-weight: 700; letter-spacing: 0.2px; }
.card p, .card li { font-size: 0.93rem; color: #374151; line-height: 1.7; }
.card ul    { margin: 6px 0 0 0; padding-left: 18px; }

.rule-table { width: 100%; border-collapse: collapse; font-size: 0.88rem; }
.rule-table th {
    background: #1e3a8a; color: white;
    padding: 9px 14px; text-align: center; font-weight: 600;
}
.rule-table td {
    padding: 9px 14px; text-align: center;
    border-bottom: 1px solid #e2e8f0;
}
.rule-table tr:nth-child(even) td { background: #f8fafc; }
.t-green { color: #15803d; font-weight: 700; }
.t-red   { color: #dc2626; font-weight: 700; }
.t-blue  { color: #1d4ed8; font-weight: 700; }

.caption-sm {
    font-size: 0.8rem; color: #64748b; text-align: center;
    margin-top: -8px; margin-bottom: 16px;
    font-style: italic;
}
.divider { border: none; border-top: 1px solid #e2e8f0; margin: 28px 0; }
</style>
"""


# ── Shared figure setup ───────────────────────────────────────────────────────
def _show(func, caption=""):
    with plt.rc_context(STYLE):
        try:
            fig = func()
            st.pyplot(fig, use_container_width=True)
            if caption:
                st.markdown(f'<p class="caption-sm">{caption}</p>',
                            unsafe_allow_html=True)
            plt.close(fig)
        except Exception as e:
            st.warning(f"Figure error: {e}")


# ═══════════════════════════════════════════════════════════════════════════════
#  FIGURES
# ═══════════════════════════════════════════════════════════════════════════════

def _fig_interference_map():
    """Ripple-tank top-view: realistic water surface interference map."""
    with plt.rc_context(STYLE):
        fig, ax = plt.subplots(figsize=(9, 6))
        # Water-surface colour: dark teal deep → bright cyan crest
        water_cmap = LinearSegmentedColormap.from_list(
            'water', ['#0a1628', '#0c3060', '#0e5fa0', '#3daee9',
                      '#9dd9f5', '#e8f7ff', '#ffffff'])
        fig.patch.set_facecolor('#0a1628')
        ax.set_facecolor('#0a1628')

        d = 4.0; lam = 2.0
        s1 = np.array([0.0,  d/2])
        s2 = np.array([0.0, -d/2])

        xv = np.linspace(-9, 9, 800)
        yv = np.linspace(-9, 9, 800)
        X, Y = np.meshgrid(xv, yv)
        R1 = np.sqrt((X - s1[0])**2 + (Y - s1[1])**2) + 1e-9
        R2 = np.sqrt((X - s2[0])**2 + (Y - s2[1])**2) + 1e-9

        # Realistic wave amplitude: two circular waves with 1/√r decay
        t = 0.0
        omega = 2 * np.pi
        amp1 = np.sin(2*np.pi*R1/lam - omega*t) / np.sqrt(R1 + 0.5)
        amp2 = np.sin(2*np.pi*R2/lam - omega*t) / np.sqrt(R2 + 0.5)
        surface = amp1 + amp2
        # Normalise to [0,1] for display
        surface_norm = (surface - surface.min()) / (surface.max() - surface.min())

        im = ax.imshow(surface_norm, origin='lower', aspect='equal',
                       cmap=water_cmap,
                       extent=[xv[0], xv[-1], yv[0], yv[-1]],
                       vmin=0, vmax=1, interpolation='bilinear')

        cb = fig.colorbar(im, ax=ax, fraction=0.032, pad=0.015)
        cb.set_label('Water surface height\n(bright = crest,  dark = trough)',
                     fontsize=8.5, color='#94a3b8')
        cb.ax.yaxis.set_tick_params(color='#94a3b8', labelcolor='#94a3b8')
        cb.set_ticks([0, 0.5, 1])
        cb.set_ticklabels(['Trough', 'Still', 'Crest'])

        # Source markers with ripple halos
        for src, col, lbl in [(s1, '#facc15', 'S₁'), (s2, '#fb923c', 'S₂')]:
            for r_h in [0.35, 0.65]:
                circle = plt.Circle(src, r_h, color=col, fill=False,
                                    lw=1.2, alpha=0.5, zorder=5)
                ax.add_patch(circle)
            ax.plot(*src, 'o', color=col, ms=11, zorder=7,
                    markeredgecolor='white', markeredgewidth=1.5)
            ax.text(src[0], src[1] - 0.75, lbl, color=col,
                    fontsize=12, fontweight='bold', ha='center', va='top')

        # Antinodal direction arrows
        n_max = int(d / lam)
        for n in range(-n_max, n_max + 1):
            v = n * lam / d
            if abs(v) < 1:
                th = np.arcsin(v)
                xe = 8.5 * np.cos(th); ye = 8.5 * np.sin(th)
                if abs(ye) < 8.7:
                    lbl = 'A₀\n(central)' if n == 0 else f'A{abs(n)}'
                    ax.text(xe * 1.05, ye * 1.05, lbl, color='#facc15',
                            fontsize=7.5, va='center', ha='center',
                            fontweight='bold')

        ax.set_xlabel('x  (cm)', color='#94a3b8', fontsize=10)
        ax.set_ylabel('y  (cm)', color='#94a3b8', fontsize=10)
        ax.tick_params(colors='#94a3b8', labelsize=8)
        for sp in ax.spines.values():
            sp.set_color('#334155')
        ax.set_title(
            'Ripple tank  —  top-view water surface  '
            f'(d = {int(d)} cm,  λ = {int(lam)} cm)',
            fontsize=10, color='#94a3b8', pad=8, fontweight='600')
        fig.tight_layout()
    return fig


def _fig_superposition():
    """Water surface displacement: constructive & destructive superposition."""
    with plt.rc_context(STYLE):
        fig = plt.figure(figsize=(11, 6.5))
        fig.patch.set_facecolor(CBGF)

        # Water-like colour map for 2-D snapshots
        water_cmap = LinearSegmentedColormap.from_list(
            'wt', ['#0c3060', '#3daee9', '#e8f7ff', '#ffffff',
                   '#e8f7ff', '#3daee9', '#0c3060'])

        x = np.linspace(0, 4 * np.pi, 600)
        configs = [
            (0,     'CONSTRUCTIVE  (Δφ = 0)',   CPOS, '#f0fdf4'),
            (np.pi, 'DESTRUCTIVE   (Δφ = π)', CNEG, '#fff5f5'),
        ]

        gs = fig.add_gridspec(2, 4, hspace=0.62, wspace=0.28,
                              width_ratios=[1, 1, 1, 0.05])

        for row, (dphi, row_lbl, rcol, rbg) in enumerate(configs):
            w1  = np.sin(x)
            w2  = np.sin(x + dphi)
            res = w1 + w2

            labels = ['Wave 1  (from S₁)', 'Wave 2  (from S₂)', 'Resultant  (water surface)']
            waves  = [w1, w2, res]
            cols_c = [C1, C2, rcol]

            for col, (y, col_c, lbl) in enumerate(zip(waves, labels, cols_c)):
                ax = fig.add_subplot(gs[row, col])
                ax.set_facecolor(rbg)

                # Shaded fill mimicking water surface depth
                ax.fill_between(x, y, 0,
                                where=(y > 0), alpha=0.22,
                                color='#7dd3fc', label='Crest')
                ax.fill_between(x, y, 0,
                                where=(y < 0), alpha=0.22,
                                color='#1e40af', label='Trough')
                ax.plot(x, y, color=col_c, lw=2.2)
                ax.axhline(0, color='#94a3b8', lw=0.8, ls=':')

                # Still-water reference
                ax.axhline(0, color='#94a3b8', lw=0.6, ls=':')

                ax.set_xlim(0, 4*np.pi)
                ax.set_ylim(-2.6, 2.6)
                ax.set_xticks(np.arange(0, 4.5*np.pi, np.pi))
                ax.set_xticklabels(['0', 'λ', '2λ', '3λ', '4λ'], fontsize=8)
                ax.set_yticks([-2, -1, 0, 1, 2])
                ax.set_yticklabels(['-2A', '-A', '0', '+A', '+2A'], fontsize=8)
                ax.set_xlabel('Distance along water surface', fontsize=8, color=CGRAY)
                ax.set_ylabel('Water surface\ndisplacement', fontsize=8,
                              color=CGRAY)
                ax.set_title(lbl, fontsize=9, fontweight='bold',
                             color=col_c, pad=4)

                # Amplitude callout on resultant
                if col == 2 and abs(res).max() > 0.1:
                    pidx = np.argmax(abs(res))
                    amax = abs(res).max()
                    ax.annotate(
                        f' Surface height\n = {amax:.0f}A',
                        xy=(x[pidx], res[pidx]),
                        xytext=(x[pidx] + 1.6, res[pidx] * 0.5),
                        fontsize=8, color=rcol, fontweight='bold',
                        arrowprops=dict(arrowstyle='->', color=rcol, lw=1.5),
                    )
                    if abs(res).max() < 0.05:
                        ax.text(np.pi * 2, 0.3, 'Flat surface\n(no wave)',
                                ha='center', fontsize=9, color=CNEG,
                                fontweight='bold')

                if col == 0:
                    ax.set_ylabel(row_lbl + '\n\nSurface\ndisplacement',
                                  fontsize=8, color=rcol,
                                  fontweight='700', labelpad=6)

        fig.suptitle('Water surface displacement — Superposition at a fixed moment',
                     fontsize=11, fontweight='bold', color=CDARK, y=1.01)
    return fig


def _fig_path_difference():
    """Top-view ripple tank with two point sources and path difference."""
    with plt.rc_context(STYLE):
        fig, ax = plt.subplots(figsize=(9, 6.2))

        # --- Water background using interference pattern ---
        d = 4.4; lam = 1.4
        s1 = np.array([1.5, 5.2])
        s2 = np.array([1.5, 0.8])
        P  = np.array([8.8, 3.4])
        r1 = np.linalg.norm(P - s1)
        r2 = np.linalg.norm(P - s2)
        dr = abs(r1 - r2)

        xv = np.linspace(-0.5, 10.5, 700)
        yv = np.linspace(-0.5, 6.5, 700)
        X, Y = np.meshgrid(xv, yv)
        R1g = np.sqrt((X - s1[0])**2 + (Y - s1[1])**2) + 1e-9
        R2g = np.sqrt((X - s2[0])**2 + (Y - s2[1])**2) + 1e-9
        surf = (np.sin(2*np.pi*R1g/lam) / np.sqrt(R1g + 0.5) +
                np.sin(2*np.pi*R2g/lam) / np.sqrt(R2g + 0.5))
        surf_n = (surf - surf.min()) / (surf.max() - surf.min())

        water_cmap = LinearSegmentedColormap.from_list(
            'wt2', ['#082844', '#0c4a80', '#1e7fc0', '#6ec6f0',
                    '#d4f0fb', '#ffffff', '#d4f0fb', '#6ec6f0',
                    '#1e7fc0', '#0c4a80', '#082844'])
        ax.imshow(surf_n, origin='lower', aspect='auto',
                  cmap=water_cmap, extent=[xv[0], xv[-1], yv[0], yv[-1]],
                  vmin=0, vmax=1, alpha=0.55, interpolation='bilinear')
        ax.set_facecolor('#0c3060')
        fig.patch.set_facecolor('#0c3060')

        # Circular wavefront rings (crisp on top of background)
        for src, col in [(s1, '#facc15'), (s2, '#fb923c')]:
            for r in np.arange(lam, 8.5, lam):
                alpha = max(0.08, 0.7 - r / 9)
                lw_r  = max(0.6, 1.6 - r / 7)
                c = plt.Circle(src, r, color=col, fill=False,
                               lw=lw_r, alpha=alpha, zorder=3)
                ax.add_patch(c)

        # Path lines S→P
        for src, col in [(s1, '#facc15'), (s2, '#fb923c')]:
            ax.plot([src[0], P[0]], [src[1], P[1]],
                    color=col, lw=2.2, ls='--', alpha=0.95, zorder=5)

        # Sources
        for src, col, lbl in [(s1, '#facc15', 'S₁'),
                               (s2, '#fb923c', 'S₂')]:
            ax.plot(*src, 'o', color=col, ms=14, zorder=7,
                    markeredgecolor='white', markeredgewidth=1.8)
            ax.text(src[0] - 0.45, src[1], lbl, ha='right', fontsize=14,
                    color=col, fontweight='bold', va='center')

        # Point P (observation point on water surface)
        ax.plot(*P, 's', color='#4ade80', ms=13, zorder=7,
                markeredgecolor='white', markeredgewidth=1.5)
        ax.text(P[0]+0.28, P[1]+0.28, 'P', fontsize=14,
                color='#4ade80', fontweight='bold')

        # r₁ and r₂ labels
        for src, col, lbl, sign in [
            (s1, '#facc15', f'r₁ = {r1:.2f} cm', +1),
            (s2, '#fb923c', f'r₂ = {r2:.2f} cm', -1),
        ]:
            mid = (src + P) / 2
            ang = np.degrees(np.arctan2(P[1]-src[1], P[0]-src[0]))
            ax.text(mid[0] + sign*0.0, mid[1] + sign*0.32, lbl,
                    fontsize=10, color=col, rotation=ang, ha='center',
                    fontweight='700',
                    bbox=dict(fc='#0c3060', ec='none', pad=1.5, alpha=0.7))

        # Δr callout
        ax.text(5.0, 6.35,
                f'Δr  =  |r₁ − r₂|  =  {dr:.2f} cm',
                fontsize=13, ha='center', fontweight='bold', color='#fef08a',
                bbox=dict(boxstyle='round,pad=0.5', fc='#713f12',
                          ec='#fbbf24', lw=2.2))

        ax.text(0.0, -0.35,
                'Top-view ripple tank  —  each ring = one wavelength  (λ = 1.4 cm)',
                fontsize=8.5, color='#94a3b8', style='italic')

        ax.set_xlim(-0.5, 10.5); ax.set_ylim(-0.5, 6.5)
        ax.set_xlabel('x  (cm)', color='#94a3b8', fontsize=10)
        ax.set_ylabel('y  (cm)', color='#94a3b8', fontsize=10)
        ax.tick_params(colors='#94a3b8', labelsize=8)
        for sp in ax.spines.values():
            sp.set_color('#334155')
        fig.tight_layout(pad=0.5)
    return fig


def _fig_condition_panels():
    """Two clean formula panels: constructive / destructive."""
    with plt.rc_context(STYLE):
        fig, axes = plt.subplots(1, 2, figsize=(10, 3.8))
        fig.patch.set_facecolor(CBGF)

        panels = [
            (CPOS, '#f0fdf4', '#bbf7d0',
             'CONSTRUCTIVE  (Antinode)',
             [r'$\Delta r = n\lambda$',
              r'$n = 0,\ 1,\ 2,\ 3,\ \ldots$',
              'Amplitude  =  2A  (maximum)'],
             'Crests meet crests'),
            (CNEG, '#fef2f2', '#fecaca',
             'DESTRUCTIVE  (Node)',
             [r'$\Delta r = \!\left(n - \tfrac{1}{2}\right)\!\lambda$',
              r'$n = 1,\ 2,\ 3,\ \ldots$',
              'Amplitude  =  0  (cancelled)'],
             'Crests meet troughs'),
        ]
        for ax, (col, fc, hc, title, lines, sub) in zip(axes, panels):
            ax.set_facecolor(fc)
            ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis('off')

            bar = FancyBboxPatch((0, 0.82), 1, 0.18, transform=ax.transAxes,
                                  boxstyle='square', fc=hc, ec='none',
                                  clip_on=False)
            ax.add_patch(bar)
            ax.text(0.5, 0.91, title, transform=ax.transAxes,
                    ha='center', va='center', fontsize=10.5,
                    fontweight='800', color=col)
            ax.text(0.5, 0.74, f'({sub})', transform=ax.transAxes,
                    ha='center', va='top', fontsize=8.5,
                    color=col, style='italic')
            for k, line in enumerate(lines):
                ax.text(0.5, 0.57 - k * 0.185, line, transform=ax.transAxes,
                        ha='center', va='top', fontsize=11.5)

            for spine_name in ['top', 'bottom', 'left', 'right']:
                ax.spines[spine_name].set_visible(True)
                ax.spines[spine_name].set_edgecolor(col)
                ax.spines[spine_name].set_linewidth(2.2)

        fig.suptitle('Interference conditions  (in-phase sources)',
                     fontsize=10.5, color=CGRAY, y=1.01)
        fig.tight_layout(pad=0.8)
    return fig


def _fig_interference_pattern():
    """Full ripple-tank view with antinodal/nodal lines overlaid."""
    with plt.rc_context(STYLE):
        fig, ax = plt.subplots(figsize=(10, 7))

        d = 12.0; lam = 3.0
        s1 = np.array([0.0,  d/2])
        s2 = np.array([0.0, -d/2])
        n_max = int(d / lam)

        # Water surface render
        xv = np.linspace(0.01, 28, 700)
        yv = np.linspace(-15, 15, 700)
        X, Y = np.meshgrid(xv, yv)
        R1 = np.sqrt((X - s1[0])**2 + (Y - s1[1])**2) + 1e-9
        R2 = np.sqrt((X - s2[0])**2 + (Y - s2[1])**2) + 1e-9
        surf = (np.sin(2*np.pi*R1/lam) / np.sqrt(R1 + 1) +
                np.sin(2*np.pi*R2/lam) / np.sqrt(R2 + 1))
        surf_n = (surf - surf.min()) / (surf.max() - surf.min())

        water_cmap = LinearSegmentedColormap.from_list(
            'wt3', ['#061628', '#0a3060', '#1464a8', '#4da8d8',
                    '#b8e4f5', '#ffffff', '#b8e4f5', '#4da8d8',
                    '#1464a8', '#0a3060', '#061628'])
        ax.imshow(surf_n, origin='lower', aspect='auto',
                  cmap=water_cmap,
                  extent=[xv[0], xv[-1], yv[0], yv[-1]],
                  vmin=0, vmax=1, interpolation='bilinear', zorder=1)
        ax.set_facecolor('#061628')
        fig.patch.set_facecolor('#061628')

        # Antinodal direction lines (bright green)
        r_max = 26
        for n in range(-n_max, n_max + 1):
            v = n * lam / d
            if abs(v) <= 1:
                th = np.arcsin(v)
                xe = r_max * np.cos(th)
                ye = r_max * np.sin(th)
                lw = 2.5 if n == 0 else 1.8
                ax.plot([0, xe], [0, ye], color='#4ade80',
                        lw=lw, alpha=0.92, zorder=3)
                lbl = 'A₀\n(central)' if n == 0 else f'A{abs(n)}'
                ax.text(xe * 1.035, ye * 1.035, lbl, fontsize=8,
                        color='#4ade80', fontweight='bold', ha='center',
                        va='center')

        # Nodal lines (dashed red-orange)
        for n in range(1, n_max + 1):
            for sign in [1, -1]:
                v = (n - 0.5) * lam / d
                if abs(v) <= 1:
                    th = np.arcsin(sign * v)
                    xe = r_max * np.cos(th)
                    ye = r_max * np.sin(th)
                    ax.plot([0, xe], [0, ye], color='#f87171',
                            lw=1.4, ls='--', alpha=0.80, zorder=3)
                    ax.text(xe * 1.035, ye * 1.035, f'N{n}',
                            fontsize=7.5, color='#f87171',
                            ha='center', va='center')

        # Sources (vibrating dippers on water surface)
        for src, col, lbl in [(s1, '#facc15', 'S₁'), (s2, '#fb923c', 'S₂')]:
            for rh in [0.6, 1.2]:
                ax.add_patch(plt.Circle(src, rh, color=col,
                                        fill=False, lw=1.0,
                                        alpha=0.5, zorder=4))
            ax.plot(*src, 'o', color=col, ms=13, zorder=6,
                    markeredgecolor='white', markeredgewidth=1.8)
            ax.text(src[0] - 1.0, src[1], lbl, fontsize=13,
                    color=col, fontweight='bold', va='center')

        # d annotation
        ax.annotate('', xy=(s1[0]-1.8, s1[1]), xytext=(s1[0]-1.8, s2[1]),
                    arrowprops=dict(arrowstyle='<->',
                                   color='#94a3b8', lw=1.5))
        ax.text(s1[0]-2.4, 0, f'd = {int(d)} cm',
                fontsize=9, color='#94a3b8', va='center', rotation=90,
                ha='center')

        # Central axis
        ax.axhline(0, color='#94a3b8', lw=0.8, ls=':', alpha=0.6)

        # Legend
        ap = mpatches.Patch(color='#4ade80',
                             label=f'Antinodal lines  ({2*n_max+1} total)')
        np2 = mpatches.Patch(color='#f87171',
                              label=f'Nodal lines  ({2*n_max} total)',
                              fill=False, linestyle='--',
                              edgecolor='#f87171')
        ax.legend(handles=[ap, np2], fontsize=9, loc='lower right',
                  framealpha=0.85, facecolor='#0a1e38',
                  edgecolor='#334155', labelcolor='white')

        ax.set_xlim(-3.5, 29); ax.set_ylim(-15.5, 15.5)
        ax.set_xlabel('x  (cm)', color='#94a3b8', fontsize=10)
        ax.set_ylabel('y  (cm)', color='#94a3b8', fontsize=10)
        ax.tick_params(colors='#94a3b8', labelsize=8)
        for sp in ax.spines.values():
            sp.set_color('#334155')
        ax.set_title(
            f'Ripple tank — top view  '
            f'(d = {int(d)} cm,  λ = {int(lam)} cm)',
            fontsize=10.5, color='#94a3b8', pad=8, fontweight='600')
        fig.tight_layout()
    return fig


def _fig_line_count():
    """Ruler diagram: Δr at every position along S₁S₂."""
    with plt.rc_context(STYLE):
        fig, ax = plt.subplots(figsize=(11, 4.5))
        fig.patch.set_facecolor(CBGF); ax.set_facecolor(CBGF)

        d = 10.0; lam = 2.0
        ax.set_xlim(-0.8, 11.6); ax.set_ylim(-3.2, 3.5)
        ax.axis('off')

        # Main axis
        ax.plot([-0.3, 10.8], [0, 0], 'k-', lw=2.5, zorder=4, solid_capstyle='round')

        # Tick marks
        for xi in range(0, 11):
            ax.plot([xi, xi], [-0.2, 0.2], 'k-', lw=1.0)
            ax.text(xi, -0.42, f'{xi}', ha='center', fontsize=7.5, color=CGRAY)
        ax.text(5, -0.72, 'Position along S₁S₂  (cm)',
                ha='center', fontsize=9, color=CGRAY)

        # Sources
        for xp, col, lbl in [(0, C1, 'S₁'), (10, C2, 'S₂')]:
            ax.plot(xp, 0, 'o', color=col, ms=15, zorder=6,
                    markeredgecolor='white', markeredgewidth=1.5)
            ax.text(xp, 0.52, lbl, ha='center', fontsize=11,
                    color=col, fontweight='bold')

        # Antinodes and nodes
        for xi in np.arange(0, d + 0.001, 0.5):
            r1 = xi; r2 = d - xi
            dr = abs(r1 - r2)
            k  = dr / lam
            is_anti = abs(k - round(k)) < 0.01
            is_node = abs((k + 0.5) - round(k + 0.5)) < 0.01

            if is_anti:
                n_lbl = int(round(k))
                ax.plot(xi, 0, 'D', color=CPOS, ms=12, zorder=7,
                        markeredgecolor='white', markeredgewidth=1.2)
                ax.text(xi, 1.1, f'A{n_lbl}', ha='center', fontsize=8,
                        color=CPOS, fontweight='bold')
                ax.text(xi, 0.62, f'Δr={int(dr)}', ha='center',
                        fontsize=7, color=CPOS)
            elif is_node:
                n_lbl = int(round(k + 0.5))
                ax.plot(xi, 0, 'v', color=CNEG, ms=10, zorder=7,
                        markeredgecolor='white', markeredgewidth=1.2)
                ax.text(xi, -1.1, f'N{n_lbl}', ha='center', fontsize=8,
                        color=CNEG, fontweight='bold')
                ax.text(xi, -1.6, f'Δr={int(dr)}', ha='center',
                        fontsize=7, color=CNEG)

        # Legend
        ap = mpatches.Patch(color=CPOS, label='Antinode  ◆  (constructive)')
        np2 = mpatches.Patch(color=CNEG, label='Node  ▼  (destructive)')
        ax.legend(handles=[ap, np2], fontsize=9, loc='upper right',
                  framealpha=0.95, edgecolor='#e2e8f0',
                  bbox_to_anchor=(1.05, 3.3))

        ax.text(5.0, 3.35,
                f'd = {int(d)} cm,  λ = {int(lam)} cm'
                f'   →   Antinodes = {int(d/lam)*2+1},  Nodes = {int(d/lam)*2}',
                ha='center', fontsize=10.5, fontweight='700', color=CDARK,
                bbox=dict(boxstyle='round,pad=0.4', fc='white',
                          ec='#cbd5e1', lw=1.8))
        fig.tight_layout()
    return fig


def _fig_antiphase():
    """2×2 grid: in-phase/anti-phase × Δr=0/Δr=λ/2."""
    with plt.rc_context(STYLE):
        fig, axes = plt.subplots(2, 2, figsize=(10, 5.5),
                                 gridspec_kw={'hspace': 0.58, 'wspace': 0.28})
        fig.patch.set_facecolor(CBGF)

        x = np.linspace(0, 4 * np.pi, 500)
        configs = [
            (0, 0, 0,      0,      'In-phase,  Δr = 0',       'ANTINODE', CPOS),
            (0, 1, np.pi,  0,      'In-phase,  Δr = λ/2', 'NODE',     CNEG),
            (1, 0, 0,      np.pi,  'Anti-phase, Δr = 0',       'NODE',     CNEG),
            (1, 1, np.pi,  np.pi,  'Anti-phase, Δr = λ/2','ANTINODE', CPOS),
        ]
        for (r, c, extra, src_phase, lbl, result, rcol) in configs:
            ax = axes[r][c]
            w1 = np.sin(x)
            w2 = np.sin(x + src_phase + extra)
            res = w1 + w2
            fc = '#f0fdf4' if rcol == CPOS else '#fff5f5'
            ax.set_facecolor(fc)
            ax.plot(x, w1, color=C1, lw=1.5, alpha=0.65, label='Wave 1')
            ax.plot(x, w2, color=C2, lw=1.5, alpha=0.65, label='Wave 2')
            ax.fill_between(x, res, alpha=0.22, color=rcol)
            ax.plot(x, res, color=rcol, lw=2.5, label='Resultant')
            ax.axhline(0, color='#94a3b8', lw=0.6, ls=':')
            ax.set_ylim(-2.5, 2.5); ax.set_yticks([-2, 0, 2])
            ax.set_yticklabels(['-2A', '0', '2A'], fontsize=7.5)
            ax.set_xticks([])
            ax.set_title(lbl, fontsize=8.5, fontweight='600', pad=4)
            ax.text(0.97, 0.93, f'→ {result}', transform=ax.transAxes,
                    ha='right', va='top', fontsize=9, fontweight='800',
                    color=rcol,
                    bbox=dict(boxstyle='round,pad=0.25', fc='white',
                              ec=rcol, lw=1.5))
            if r == 0 and c == 0:
                ax.legend(fontsize=7.5, loc='lower right',
                          framealpha=0.92, edgecolor='#e2e8f0')

        axes[0][0].set_ylabel('In-phase sources', fontsize=9,
                               color=CGRAY, fontweight='600')
        axes[1][0].set_ylabel('Anti-phase sources', fontsize=9,
                               color=CGRAY, fontweight='600')
        fig.suptitle('Phase reversal: in-phase vs anti-phase sources',
                     fontsize=11, fontweight='bold', y=1.01)
        fig.tight_layout()
    return fig


def _fig_double_slit_geometry():
    """Water wave passing through two openings in a barrier — top view."""
    with plt.rc_context(STYLE):
        fig, ax = plt.subplots(figsize=(10, 6.5))

        d = 1.0; lam = 0.30; L = 10.5
        s1 = np.array([0.0,  d/2])
        s2 = np.array([0.0, -d/2])

        # --- Water surface beyond barrier ---
        xv = np.linspace(0.01, 12, 700)
        yv = np.linspace(-5.2, 5.2, 700)
        X, Y = np.meshgrid(xv, yv)
        R1 = np.sqrt((X - s1[0])**2 + (Y - s1[1])**2) + 1e-9
        R2 = np.sqrt((X - s2[0])**2 + (Y - s2[1])**2) + 1e-9
        surf = (np.sin(2*np.pi*R1/lam) / np.sqrt(R1 + 0.4) +
                np.sin(2*np.pi*R2/lam) / np.sqrt(R2 + 0.4))
        surf_n = (surf - surf.min()) / (surf.max() - surf.min())

        water_cmap = LinearSegmentedColormap.from_list(
            'wt4', ['#061628', '#0b3668', '#1972b8', '#55b4e0',
                    '#c0e8f8', '#ffffff', '#c0e8f8', '#55b4e0',
                    '#1972b8', '#0b3668', '#061628'])
        ax.imshow(surf_n, origin='lower', aspect='auto',
                  cmap=water_cmap,
                  extent=[xv[0], xv[-1], yv[0], yv[-1]],
                  vmin=0, vmax=1, interpolation='bilinear', zorder=1)
        ax.set_facecolor('#061628')
        fig.patch.set_facecolor('#061628')

        # --- Left side (incident plane wave, darker) ---
        ax.fill_between([-2.5, 0], [-5.2, -5.2], [5.2, 5.2],
                        color='#040e1e', alpha=0.80, zorder=2)

        # Incoming plane wavefronts
        for xi in np.arange(-2.2, 0, lam):
            ax.plot([xi, xi], [-4.8, 4.8], color='#60a5fa',
                    lw=1.2, alpha=0.5, zorder=3)

        # Incoming wave label
        ax.text(-1.25, 4.5, 'Incoming\nplane wave',
                color='#93c5fd', fontsize=9, ha='center', fontweight='600',
                zorder=4)
        ax.annotate('', xy=(-0.35, 0), xytext=(-1.5, 0),
                    arrowprops=dict(arrowstyle='->', color='#60a5fa',
                                   lw=2.2), zorder=4)

        # --- Barrier ---
        barrier_x = [-0.18, 0.18]
        gap_half   = d / 2
        for y_seg in [(-5.2, -(gap_half + d/2 + 0.05)),
                      (-gap_half + 0.0, gap_half - 0.0),
                      (gap_half + d/2 + 0.05, 5.2)]:
            # solid barrier regions — the two gap_half-sized openings are left clear
            pass
        # Proper barrier: two gaps at ±d/2
        gap = d * 0.5   # half-gap size visually
        for yseg_bot, yseg_top in [
            (-5.2,            -(gap_half + gap * 0.1)),
            (-(gap_half - gap * 0.1), gap_half - gap * 0.1),
            (gap_half + gap * 0.1, 5.2),
        ]:
            ax.fill_between(barrier_x, yseg_bot, yseg_top,
                            color='#64748b', alpha=0.97, zorder=5)
        # Openings highlight
        for yc in [s1[1], s2[1]]:
            ax.fill_between(barrier_x, yc - gap*0.1, yc + gap*0.1,
                            color='#0f172a', alpha=0.0, zorder=6)
        # Barrier label
        ax.text(-0.65, -4.5, 'Barrier\n(แผ่นกั้นน้ำ)',
                color='#94a3b8', fontsize=8.5, ha='center',
                va='bottom', rotation=90, zorder=6)

        # Opening markers
        for src, col, lbl in [(s1, '#facc15', 'O₁  (upper opening)'),
                               (s2, '#fb923c', 'O₂  (lower opening)')]:
            ax.plot(*src, 'D', color=col, ms=10, zorder=8,
                    markeredgecolor='white', markeredgewidth=1.5)
            ax.text(0.35, src[1], lbl, color=col, fontsize=8.5,
                    va='center', fontweight='600', zorder=8)

        # d annotation
        ax.annotate('', xy=(-0.85, s1[1]), xytext=(-0.85, s2[1]),
                    arrowprops=dict(arrowstyle='<->', color='#94a3b8', lw=1.5),
                    zorder=6)
        ax.text(-1.25, 0, 'd', fontsize=13, color='#e2e8f0',
                ha='center', va='center', fontweight='bold', zorder=6)

        # Central axis
        ax.plot([0, 11.5], [0, 0], color='#94a3b8',
                lw=0.9, ls=':', alpha=0.7, zorder=4)

        # Antinodal direction arrows + n labels
        for n in range(-3, 4):
            v = n * lam / d
            if abs(v) < 1:
                th = np.arcsin(v)
                ye = L * np.tan(th)
                if abs(ye) <= 4.8:
                    lw = 2.2 if n == 0 else 1.4
                    al = 1.0 if n == 0 else 0.75
                    ax.plot([0, L], [0, ye], color='#4ade80',
                            lw=lw, alpha=al, zorder=4)
                    ax.plot(L, ye, 'o', color='#4ade80', ms=9,
                            markeredgecolor='white', markeredgewidth=1.2,
                            zorder=6)
                    ax.text(L + 0.3, ye, f'n = {n}',
                            color='#4ade80', fontsize=8.5, va='center',
                            fontweight='600', zorder=6)

        # θ arc for n=1
        th1 = np.arcsin(lam / d)
        ye1 = L * np.tan(th1)
        arc = mpatches.Arc((0, 0), 3.0, 3.0, angle=0,
                           theta1=0, theta2=np.degrees(th1),
                           color='#c084fc', lw=2.0, zorder=5)
        ax.add_patch(arc)
        ax.text(1.65, 0.45, 'θ', fontsize=14, color='#c084fc',
                fontweight='bold', zorder=6)

        # x arrow (vertical)
        ax.annotate('', xy=(L + 0.2, ye1), xytext=(L + 0.2, 0),
                    arrowprops=dict(arrowstyle='<->', color='#fbbf24', lw=1.5),
                    zorder=6)
        ax.text(L + 0.7, ye1 / 2, 'x', fontsize=13, color='#fbbf24',
                va='center', fontweight='bold', zorder=6)

        # L arrow (horizontal)
        ax.annotate('', xy=(L, -5.05), xytext=(0, -5.05),
                    arrowprops=dict(arrowstyle='<->', color='#94a3b8', lw=1.4),
                    zorder=6)
        ax.text(L / 2, -5.25, 'L  (distance from barrier)',
                ha='center', fontsize=8.5, color='#94a3b8', zorder=6)

        # Formula box
        ax.text(5.5, 5.1,
                r'$\sin\theta = n\lambda / d$'
                r'   →   '
                r'$x = n\lambda L / d$   (small  $\theta$)',
                fontsize=11, ha='center', color='white', fontweight='700',
                bbox=dict(boxstyle='round,pad=0.5', fc='#1e3a8a',
                          ec='#60a5fa', lw=2.0), zorder=7)

        ax.set_xlim(-2.5, 12); ax.set_ylim(-5.4, 5.4)
        ax.set_xlabel('x  (cm)', color='#94a3b8', fontsize=10)
        ax.set_ylabel('y  (cm)', color='#94a3b8', fontsize=10)
        ax.tick_params(colors='#94a3b8', labelsize=8)
        for sp in ax.spines.values():
            sp.set_color('#334155')
        ax.set_title(
            'Water waves passing through two openings — top view\n'
            'Bright green lines = antinodal directions (constructive interference)',
            fontsize=10, color='#94a3b8', pad=8, fontweight='600')
        fig.tight_layout(pad=0.4)
    return fig


def _fig_method_flowchart():
    """Professional 3-step flowchart."""
    with plt.rc_context(STYLE):
        fig, ax = plt.subplots(figsize=(10, 3.2))
        ax.axis('off')
        fig.patch.set_facecolor(CBGF); ax.set_facecolor(CBGF)
        ax.set_xlim(0, 10); ax.set_ylim(0, 3.2)

        steps = [
            (1.25, '#1e3a8a', '#eff6ff',
             'Step 1',
             'Compute\npath difference',
             r'$\Delta r = |r_1 - r_2|$'),
            (4.00, '#065f46', '#f0fdf4',
             'Step 2',
             'Find ratio k',
             r'$k = \Delta r \;/\; \lambda$'),
            (6.75, '#92400e', '#fefce8',
             'Step 3',
             'Classify k',
             'integer  or  half-integer?'),
        ]
        for xc, bc, fc, step_lbl, desc, formula in steps:
            box = FancyBboxPatch((xc-1.05, 0.5), 2.1, 2.2,
                                  boxstyle='round,pad=0.09',
                                  fc=fc, ec=bc, lw=2.4,
                                  transform=ax.transData)
            ax.add_patch(box)
            ax.text(xc, 2.52, step_lbl, ha='center', va='center',
                    fontsize=9, fontweight='800', color=bc)
            ax.text(xc, 1.98, desc, ha='center', va='center',
                    fontsize=8.8, color='#374151')
            ax.text(xc, 1.35, formula, ha='center', va='center',
                    fontsize=10.5)

        # Arrows between steps
        for xarr in [2.32, 5.07]:
            ax.annotate('', xy=(xarr + 0.61, 1.6), xytext=(xarr, 1.6),
                        arrowprops=dict(arrowstyle='->', color='#94a3b8', lw=2.0))

        # Outcome branches
        ax.annotate('', xy=(7.87, 2.3), xytext=(7.82, 1.6),
                    arrowprops=dict(arrowstyle='->', color=CPOS, lw=1.8))
        ax.annotate('', xy=(7.87, 0.9), xytext=(7.82, 1.6),
                    arrowprops=dict(arrowstyle='->', color=CNEG, lw=1.8))

        for yc, col, fc, txt in [
            (2.40, CPOS, '#dcfce7', 'k = 0, 1, 2, …\n→ ANTINODE'),
            (0.80, CNEG, '#fee2e2', 'k = ½, 1½, 2½, …\n→  NODE'),
        ]:
            box = FancyBboxPatch((7.9, yc-0.42), 2.0, 0.84,
                                  boxstyle='round,pad=0.07',
                                  fc=fc, ec=col, lw=2.0,
                                  transform=ax.transData)
            ax.add_patch(box)
            ax.text(8.9, yc, txt, ha='center', va='center',
                    fontsize=8.5, color=col, fontweight='700')

        ax.set_title('3-Step Method  —  applicable to every interference problem',
                     fontsize=10.5, color=CGRAY, pad=6)
        fig.tight_layout(pad=0.5)
    return fig


# ═══════════════════════════════════════════════════════════════════════════════
#  MAIN RENDER
# ═══════════════════════════════════════════════════════════════════════════════

def render_summary():
    st.markdown(_CSS, unsafe_allow_html=True)

    # Hero
    st.markdown("""
<div class="pro-hero">
  <h1>การแทรกสอดของคลื่นน้ำ</h1>
  <p>Water Wave Interference &nbsp;&middot;&nbsp; สรุปครบ พร้อมสูตร พร้อมรูปภาพจากถาดคลื่น (Ripple Tank)</p>
</div>
""", unsafe_allow_html=True)

    # ── 01 หลักการซ้อนทับ ────────────────────────────────────────────────────
    st.markdown('<p class="sec-head"><span class="pill">01</span>หลักการซ้อนทับ  (Superposition Principle)</p>',
                unsafe_allow_html=True)

    c1, c2 = st.columns([1.05, 1], gap="large")
    with c1:
        st.markdown("""
<div class="card card-blue">
<h4>ความหมาย</h4>
<p>เมื่อ<strong>คลื่นน้ำสองขบวน</strong>เดินทางมาพบกันบนผิวน้ำ
ระดับน้ำ ณ จุดนั้นเท่ากับ<strong>ผลรวมของความสูงผิวน้ำจากแต่ละขบวน</strong></p>
<ul>
<li>ยอดคลื่นพบยอดคลื่น → <strong class="t-green">ผิวน้ำสูงเป็น 2 เท่า</strong> (เสริมกัน)</li>
<li>ยอดคลื่นพบรางคลื่น → <strong class="t-red">ผิวน้ำนิ่ง = ระดับปกติ</strong> (หักล้างกัน)</li>
</ul>
</div>
<div class="card card-gray" style="margin-top:10px">
<h4>แหล่งกำเนิดในถาดคลื่น (Ripple Tank)</h4>
<p>ใช้ <strong>แท่งสั่น (dipper) สองอัน</strong> ความถี่เท่ากัน สั่นพร้อมกัน
สร้างคลื่นวงกลมสองชุดที่แผ่ออกมาบนผิวน้ำและเกิดการแทรกสอดกัน</p>
</div>
""", unsafe_allow_html=True)
    with c2:
        _show(_fig_superposition,
              "บน: ยอดพบยอด → ผิวน้ำสูง 2A &nbsp;|&nbsp; ล่าง: ยอดพบราง → ผิวน้ำนิ่ง (สุทธิ = 0)")

    # ── 02 ผลต่างระยะทาง ─────────────────────────────────────────────────────
    st.markdown('<hr class="divider"><p class="sec-head"><span class="pill">02</span>ผลต่างระยะทาง  (Path Difference  Δr)</p>',
                unsafe_allow_html=True)

    c1, c2 = st.columns([1, 1.05], gap="large")
    with c1:
        _show(_fig_path_difference,
              "วงกลมแต่ละวงแทนหนึ่งความยาวคลื่น — Δr คือส่วนต่างของระยะที่คลื่นทั้งสองเดินทาง")
    with c2:
        st.markdown('<div class="card card-blue"><h4>นิยาม</h4></div>',
                    unsafe_allow_html=True)
        st.latex(r"\Delta r \;=\; |r_1 - r_2|")
        st.markdown("""
<div class="card card-blue" style="margin-top:12px">
<h4>ทำไม Δr ถึงสำคัญ?</h4>
<p>Δr บอกว่าคลื่นสองขบวนใช้เส้นทางต่างกันเท่าไร
ซึ่งทำให้เฟสต่างกันตาม</p>
<ul>
<li>Δr = nλ &nbsp;&rarr;&nbsp; เฟสตรงกัน &rarr;&nbsp; <strong class="t-green">เสริม</strong></li>
<li>Δr = (n&minus;&frac12;)λ &nbsp;&rarr;&nbsp; เฟสต่าง 180&deg; &rarr;&nbsp; <strong class="t-red">หักล้าง</strong></li>
</ul>
</div>
""", unsafe_allow_html=True)

    # ── 03 เงื่อนไข ──────────────────────────────────────────────────────────
    st.markdown('<hr class="divider"><p class="sec-head"><span class="pill">03</span>เงื่อนไขปฏิบัพและบัพ  (แหล่งกำเนิดเฟสตรงกัน)</p>',
                unsafe_allow_html=True)

    _show(_fig_condition_panels)

    c1, c2 = st.columns(2, gap="large")
    with c1:
        st.markdown('<div class="card card-green"><h4>ปฏิบัพ (Antinode) — เสริมกัน</h4></div>',
                    unsafe_allow_html=True)
        st.latex(r"\Delta r = n\lambda \qquad n = 0,\,1,\,2,\,\ldots")
        st.markdown("แอมพลิจูด = **2A** &nbsp;(สูงสุด)")
    with c2:
        st.markdown('<div class="card card-red"><h4>บัพ (Node) — หักล้างกัน</h4></div>',
                    unsafe_allow_html=True)
        st.latex(r"\Delta r = \!\left(n - \tfrac{1}{2}\right)\!\lambda \qquad n = 1,\,2,\,3,\,\ldots")
        st.markdown("แอมพลิจูด = **0**")

    # ── 04 วิธีทำโจทย์ ───────────────────────────────────────────────────────
    st.markdown('<hr class="divider"><p class="sec-head"><span class="pill">04</span>วิธีทำโจทย์ — 3 ขั้นตอน</p>',
                unsafe_allow_html=True)

    _show(_fig_method_flowchart)

    c1, c2 = st.columns(2, gap="large")
    with c1:
        st.markdown("""
<div class="card card-amber">
<h4>ตัวอย่างที่ 1</h4>
<p>S₁ S₂ ให้คลื่น λ = 4 cm &nbsp;·&nbsp; r₁ = 22 cm, r₂ = 14 cm</p>
<ul>
<li>Δr = |22 &minus; 14| = <strong>8 cm</strong></li>
<li>k = 8 ÷ 4 = <strong>2.0</strong>  (จำนวนเต็ม)</li>
<li>&rarr; <strong class="t-green">ปฏิบัพ A₂</strong></li>
</ul>
</div>
""", unsafe_allow_html=True)
    with c2:
        st.markdown("""
<div class="card card-amber">
<h4>ตัวอย่างที่ 2</h4>
<p>λ = 6 cm &nbsp;·&nbsp; Δr = 9 cm</p>
<ul>
<li>k = 9 ÷ 6 = <strong>1.5</strong>  (ลงท้าย .5)</li>
<li>&rarr; <strong class="t-red">บัพ N₂</strong></li>
</ul>
</div>
""", unsafe_allow_html=True)

    # ── 05 Interference Pattern ───────────────────────────────────────────────
    st.markdown('<hr class="divider"><p class="sec-head"><span class="pill">05</span>รูปแบบการแทรกสอด  (Interference Pattern)</p>',
                unsafe_allow_html=True)

    _show(_fig_interference_map,
          "แผนที่ความเข้มจริง — แถบสว่างคือแนวปฏิบัพ, แถบมืดคือแนวบัพ  (d = 4 cm, λ = 2 cm)")
    _show(_fig_interference_pattern,
          "แนวปฏิบัพ (สีเขียว) และแนวบัพ (เส้นประสีแดง)  (d = 12 cm, λ = 3 cm)")

    # ── 06 การนับแนว ─────────────────────────────────────────────────────────
    st.markdown('<hr class="divider"><p class="sec-head"><span class="pill">06</span>การนับจำนวนแนวปฏิบัพและบัพ</p>',
                unsafe_allow_html=True)

    _show(_fig_line_count,
          "ตำแหน่งปฏิบัพ ◆ และบัพ ▼ ทุกจุดบนเส้น S₁S₂  (d = 10 cm, λ = 2 cm)")

    st.markdown('<div class="card card-blue"><h4>หา n<sub>max</sub> ก่อน</h4></div>',
                unsafe_allow_html=True)
    st.latex(r"n_{\max} = \left\lfloor \frac{d}{\lambda} \right\rfloor")

    c1, c2 = st.columns(2, gap="large")
    with c1:
        st.markdown("**จำนวนแนวปฏิบัพ (รวม A₀):**")
        st.latex(r"2\,n_{\max} + 1")
    with c2:
        st.markdown("**จำนวนแนวบัพ:**")
        st.latex(r"2\,n_{\max}")

    st.markdown("""
<table class="rule-table">
<thead><tr>
  <th>สิ่งที่นับ</th>
  <th>บนแนว S₁S₂ (รวม S₁, S₂)</th>
  <th>ระหว่าง S₁S₂ (ไม่รวม S₁, S₂)</th>
</tr></thead>
<tbody>
<tr><td><strong>ปฏิบัพ</strong></td>
    <td class="t-green">2n₀ + 1</td>
    <td class="t-green">2n₀ &minus; 1</td></tr>
<tr><td><strong>บัพ</strong></td>
    <td class="t-red">2n₀</td>
    <td class="t-red">2(n₀ &minus; 1)</td></tr>
</tbody>
</table>
<p style="font-size:0.8rem;color:#64748b;margin-top:6px">
* ใช้เมื่อ d = n₀λ (หารลงตัว) &nbsp;|&nbsp; ถ้าไม่ลงตัว ให้ใช้ n<sub>max</sub> ข้างบนแทน
</p>
""", unsafe_allow_html=True)

    # ── 07 เฟสตรงข้าม ────────────────────────────────────────────────────────
    st.markdown('<hr class="divider"><p class="sec-head"><span class="pill">07</span>กรณีพิเศษ: แหล่งกำเนิดเฟสตรงข้าม  (Anti-phase)</p>',
                unsafe_allow_html=True)

    c1, c2 = st.columns([1.1, 1], gap="large")
    with c1:
        _show(_fig_antiphase,
              "เปรียบเทียบผลลัพธ์ที่ Δr = 0 และ λ/2 สำหรับทั้งสองกรณี")
    with c2:
        st.markdown("""
<div class="card card-red">
<h4>เงื่อนไขสลับทั้งหมด!</h4>
<p>เมื่อแหล่งกำเนิดเฟสต่างกัน 180° เงื่อนไขปฏิบัพ-บัพ <strong>สลับกันทั้งหมด</strong></p>
</div>
""", unsafe_allow_html=True)
        st.markdown("""
<table class="rule-table">
<thead><tr><th>Δr</th><th>เฟสตรงกัน</th><th>เฟสตรงข้าม</th></tr></thead>
<tbody>
<tr><td>0, λ, 2λ, …</td>
    <td class="t-green">ปฏิบัพ</td>
    <td class="t-red">บัพ</td></tr>
<tr><td>λ/2, 3λ/2, …</td>
    <td class="t-red">บัพ</td>
    <td class="t-green">ปฏิบัพ</td></tr>
</tbody>
</table>
""", unsafe_allow_html=True)
        st.markdown("""
<div class="card card-amber" style="margin-top:10px">
<h4>อธิบายเหตุผล</h4>
<p>แหล่งกำเนิดเฟสตรงข้ามส่งคลื่นต่างกัน 180° อยู่แล้ว
เมื่อ Δr = 0 เฟสรวม = 180° &rarr; หักล้าง
เมื่อ Δr = λ/2 เฟสเพิ่ม 180° รวม = 360° = 0° &rarr; เสริม</p>
</div>
""", unsafe_allow_html=True)

    # ── 08 Two-opening barrier ────────────────────────────────────────────────
    st.markdown('<hr class="divider"><p class="sec-head"><span class="pill">08</span>คลื่นน้ำผ่านช่องเปิดคู่ในแผ่นกั้น</p>',
                unsafe_allow_html=True)

    _show(_fig_double_slit_geometry,
          "มองจากด้านบน — คลื่นน้ำแผ่ผ่านช่องเปิด O₁ และ O₂ แล้วเกิดการแทรกสอดกัน")

    c1, c2 = st.columns(2, gap="large")
    with c1:
        st.markdown("**มุมแนวปฏิบัพลำดับที่ n ทำกับแนวตั้งฉาก:**")
        st.latex(r"\sin\theta_n = \frac{n\lambda}{d}")
        st.markdown("**ระยะวัดตามแนวขวาง ห่างจากแกนกลาง (θ เล็ก):**")
        st.latex(r"x_n = \frac{n\lambda L}{d}")
        st.markdown("**ระยะห่างระหว่างแนวปฏิบัพสองแนวติดกัน:**")
        st.latex(r"\Delta x = \frac{\lambda L}{d}")
    with c2:
        st.markdown("""
<div class="card card-green">
<h4>ตัวอย่าง (คลื่นน้ำ)</h4>
<p>ช่องเปิดสองช่อง ห่างกัน d = 4 cm<br>
λ = 2 cm, วัดระยะที่ L = 30 cm</p>
<ul>
<li>x₁ = (1 × 2 × 30) / 4 = <strong>15 cm</strong></li>
<li>x₂ = (2 × 2 × 30) / 4 = <strong>30 cm</strong></li>
<li>Δx = (2 × 30) / 4 = <strong>15 cm</strong></li>
</ul>
</div>
<div class="card card-red" style="margin-top:10px">
<h4>มุมแนวบัพลำดับที่ n:</h4>
</div>
""", unsafe_allow_html=True)
        st.latex(r"\sin\theta_n = \frac{(n-\tfrac{1}{2})\lambda}{d}")

    # ── ตารางสรุป ─────────────────────────────────────────────────────────────
    st.markdown('<hr class="divider"><p class="sec-head"><span class="pill">สรุป</span>ตารางสูตรครบ</p>',
                unsafe_allow_html=True)

    st.markdown("""
<table class="rule-table">
<thead><tr>
  <th>หัวข้อ</th>
  <th>ปฏิบัพ (Constructive)</th>
  <th>บัพ (Destructive)</th>
</tr></thead>
<tbody>
<tr><td><strong>เงื่อนไข Δr (เฟสตรงกัน)</strong></td>
    <td class="t-green">Δr = 0, λ, 2λ, …</td>
    <td class="t-red">Δr = λ/2, 3λ/2, …</td></tr>
<tr><td><strong>เงื่อนไข Δr (เฟสตรงข้าม)</strong></td>
    <td class="t-green">Δr = λ/2, 3λ/2, …</td>
    <td class="t-red">Δr = 0, λ, 2λ, …</td></tr>
<tr><td><strong>จำนวนแนว (ทั่วระนาบ)</strong></td>
    <td class="t-green">2n<sub>max</sub> + 1</td>
    <td class="t-red">2n<sub>max</sub></td></tr>
<tr><td><strong>มุมบนฉาก</strong></td>
    <td class="t-green">sin θ = nλ / d</td>
    <td class="t-red">sin θ = (n&minus;½)λ / d</td></tr>
<tr><td><strong>ระยะบนฉาก (θ เล็ก)</strong></td>
    <td class="t-green">x = nλL / d</td>
    <td class="t-red">x = (n&minus;½)λL / d</td></tr>
<tr><td><strong>แอมพลิจูดผลลัพธ์</strong></td>
    <td class="t-green">2A</td>
    <td class="t-red">0</td></tr>
</tbody>
</table>
""", unsafe_allow_html=True)

    st.info(
        "**เคล็ดลับ:** ทุกโจทย์เริ่มจาก หา Δr → หารด้วย λ → "
        "ดูว่าได้จำนวนเต็มหรือครึ่งจำนวนเต็ม → ตอบได้ทันที"
    )
