"""
summary.py — สรุปการแทรกสอดของคลื่นน้ำ ม.5
"""
import io as _io
import streamlit as st
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Arc

import matplotlib.font_manager as fm

# ── Font ─────────────────────────────────────────────────────────────────────
_THAI = ['Tahoma', 'Arial Unicode MS', 'Browallia New',
         'AngsanaUPC', 'Cordia New', 'FreeSans']
_avail = {f.name for f in fm.fontManager.ttflist}
_font  = next((f for f in _THAI if f in _avail), 'DejaVu Sans')

RC = {
    'font.family': _font,
    'axes.unicode_minus': False,
    'figure.dpi': 110,
    'savefig.bbox': 'tight',
}

CB   = '#1d4ed8'
CR   = '#b91c1c'
CG   = '#16a34a'
CRED = '#dc2626'
CGR  = '#475569'
CDK  = '#0f172a'
CBG  = '#ffffff'

# ── CSS ───────────────────────────────────────────────────────────────────────
_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');

.hero {
    background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 55%, #2563eb 100%);
    border-radius: 16px;
    padding: 36px 32px 28px;
    color: #fff;
    margin-bottom: 28px;
}
.hero h1 { font-size: 1.9rem; font-weight: 800; margin: 0 0 6px; }
.hero p  { color: #93c5fd; margin: 0; font-size: .97rem; line-height: 1.6; }
.hero-meta { margin-top: 14px; display: flex; gap: 10px; flex-wrap: wrap; }
.hero-tag {
    background: rgba(255,255,255,0.13);
    border: 1px solid rgba(255,255,255,0.22);
    color: #e0f2fe;
    font-size: .72rem; font-weight: 600;
    padding: 3px 11px; border-radius: 20px;
}

.sh {
    font-size: 1.05rem; font-weight: 700; color: #0f172a;
    padding: 9px 0 9px 14px;
    margin: 28px 0 14px;
    border-left: 4px solid #2563eb;
    background: linear-gradient(to right, #eff6ff, transparent);
    border-radius: 0 8px 8px 0;
}
.pill {
    display: inline-block;
    background: #2563eb; color: #fff;
    font-size: .63rem; font-weight: 700;
    padding: 2px 8px; border-radius: 12px;
    letter-spacing: .04em; text-transform: uppercase;
    margin-right: 9px; vertical-align: middle;
    position: relative; top: -1px;
}

.card {
    background: #fff;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 16px 18px;
    margin: 8px 0;
    box-shadow: 0 1px 4px rgba(0,0,0,.05);
}
.cb { border-left: 4px solid #3b82f6; }
.cg { border-left: 4px solid #16a34a; }
.cr { border-left: 4px solid #dc2626; }
.cy { border-left: 4px solid #d97706; }
.cs { border-left: 4px solid #94a3b8; }
.cp { border-left: 4px solid #7c3aed; }
.card h4 { margin: 0 0 8px; font-size: .9rem; font-weight: 700; color: #0f172a; }
.card p, .card li { font-size: .91rem; color: #374151; line-height: 1.8; }
.card ul { margin: 6px 0 0; padding-left: 18px; }

.rt { width:100%; border-collapse:collapse; font-size:.87rem;
      border-radius:10px; overflow:hidden; }
.rt thead tr { background: linear-gradient(135deg,#1e3a8a,#2563eb); }
.rt th { color:#fff; padding:9px 13px; text-align:center; font-weight:600; }
.rt td { padding:8px 13px; text-align:center; border-bottom:1px solid #e2e8f0; }
.rt tr:last-child td { border-bottom:none; }
.rt tr:nth-child(even) td { background:#f8fafc; }
.tg { color:#15803d; font-weight:700; }
.tr { color:#dc2626; font-weight:700; }

.cap {
    font-size:.76rem; color:#64748b; text-align:center;
    margin:-2px 0 10px; font-style:italic;
    padding:4px 14px; background:#f8fafc;
    border-radius: 0 0 8px 8px;
}
.keytip {
    background: linear-gradient(135deg,#fef3c7,#fde68a);
    border: 1.5px solid #f59e0b;
    border-radius: 10px;
    padding: 13px 16px;
    font-size: .91rem; color: #78350f; margin: 14px 0;
}
.keytip strong { color: #92400e; }
hr.div { border:none; border-top:1px solid #e2e8f0; margin:24px 0; }
</style>
"""

# ── Figure cache ──────────────────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def _cached_fig_png(func_name: str) -> bytes:
    _funcs = {
        "superposition":   _fig_superposition,
        "path_diff":       _fig_path_diff,
        "conditions":      _fig_conditions,
        "two_sources":     _fig_two_sources,
        "pattern":         _fig_pattern,
        "ruler":           _fig_ruler,
        "antiphase":       _fig_antiphase,
        "barrier":         _fig_barrier,
        "flowchart":       _fig_flowchart,
    }
    fig = _funcs[func_name]()
    buf = _io.BytesIO()
    fig.savefig(buf, format="png", dpi=110, bbox_inches="tight")
    buf.seek(0)
    plt.close(fig)
    return buf.getvalue()


def _show(func_name: str, cap: str = ""):
    try:
        png = _cached_fig_png(func_name)
        st.image(png, use_container_width=True)
        if cap:
            st.markdown(f'<p class="cap">{cap}</p>', unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Figure error ({func_name}): {e}")


# ═══════════════════════════════════════════════════════════════════════════════
#  FIGURE 1 — การซ้อนทับของคลื่น: constructive vs destructive
# ═══════════════════════════════════════════════════════════════════════════════
def _fig_superposition():
    with plt.rc_context(RC):
        fig, axes = plt.subplots(2, 3, figsize=(10, 5.2),
                                 gridspec_kw={'hspace': 0.65, 'wspace': 0.30})
        fig.patch.set_facecolor(CBG)
        x = np.linspace(0, 2, 500)

        configs = [
            (0,      CG,   '#f0fdf4', 'In-phase  (Δφ = 0)',   '#bbf7d0'),
            (np.pi,  CRED, '#fff5f5', 'Anti-phase  (Δφ = π)', '#fecaca'),
        ]
        for row, (dphi, rcol, rbg, row_title, rfill) in enumerate(configs):
            w1  = np.sin(2 * np.pi * x)
            w2  = np.sin(2 * np.pi * x + dphi)
            res = w1 + w2

            for col in range(3):
                ax = axes[row, col]
                ax.set_facecolor(rbg)
                if col == 0:
                    y, color = w1, CB
                    ax.set_title('Wave from S₁', fontsize=9, color=CB, fontweight='bold', pad=3)
                elif col == 1:
                    y, color = w2, CR
                    ax.set_title('Wave from S₂', fontsize=9, color=CR, fontweight='bold', pad=3)
                else:
                    y, color = res, rcol
                    ax.set_title('Resultant (surface)', fontsize=9, color=rcol, fontweight='bold', pad=3)

                ax.fill_between(x, y, 0, where=(y >= 0), color=rfill, alpha=0.6)
                ax.fill_between(x, y, 0, where=(y < 0),  color=rfill, alpha=0.25)
                ax.plot(x, y, color=color, lw=2.2)
                ax.axhline(0, color='#94a3b8', lw=0.7, ls=':')
                ax.set_xlim(0, 2); ax.set_ylim(-2.5, 2.5)
                ax.set_xticks([0, 0.5, 1, 1.5, 2])
                ax.set_xticklabels(['0', 'λ/2', 'λ', '3λ/2', '2λ'], fontsize=7.5)
                ax.set_yticks([-2, -1, 0, 1, 2])
                ax.set_yticklabels(['-2A', '-A', '0', '+A', '+2A'], fontsize=7.5)
                ax.spines[['top', 'right']].set_visible(False)

                if col == 2:
                    amax = np.max(np.abs(res))
                    label = f'Amplitude = {amax:.0f}A' if amax > 0.1 else 'Amplitude = 0\n(still water)'
                    ax.text(0.97, 0.92, label, transform=ax.transAxes,
                            ha='right', va='top', fontsize=8.5,
                            fontweight='bold', color=rcol,
                            bbox=dict(boxstyle='round,pad=0.3',
                                      fc='#f0fdf4' if rcol == CG else '#fef2f2',
                                      ec=rcol, lw=1.5))

            axes[row, 0].set_ylabel(row_title, fontsize=8.5,
                                    color=rcol, fontweight='800', labelpad=5)

        # เครื่องหมาย + และ =
        for row in range(2):
            y_pos = 0.76 - row * 0.44
            fig.text(0.368, y_pos, '+', ha='center', va='center',
                     fontsize=16, color=CGR, fontweight='bold')
            fig.text(0.638, y_pos, '=', ha='center', va='center',
                     fontsize=16, color=configs[row][1], fontweight='bold')

        fig.suptitle('Superposition Principle — fixed point on the water surface',
                     fontsize=11, fontweight='bold', color=CDK, y=1.01)
        fig.tight_layout()
    return fig


# ═══════════════════════════════════════════════════════════════════════════════
#  FIGURE 2 — ผลต่างเส้นทาง Δr geometry
# ═══════════════════════════════════════════════════════════════════════════════
def _fig_path_diff():
    with plt.rc_context(RC):
        fig, ax = plt.subplots(figsize=(8, 5.0))
        ax.set_facecolor('#f0f6ff')
        fig.patch.set_facecolor('#f0f6ff')
        ax.axis('off')
        ax.set_xlim(-1.0, 10.5)
        ax.set_ylim(-0.5, 6.0)

        s1  = np.array([0.5, 4.8])
        s2  = np.array([0.5, 0.8])
        P   = np.array([8.5, 3.0])
        lam = 1.2
        r1  = np.linalg.norm(P - s1)
        r2  = np.linalg.norm(P - s2)
        dr  = abs(r1 - r2)

        # วงหน้าคลื่นจาก S1, S2
        for src, col in [(s1, CB), (s2, CR)]:
            for n in range(1, 8):
                r     = n * lam
                alpha = max(0.06, 0.50 - n * 0.06)
                lw_r  = 1.4 if n % 2 != 0 else 0.8
                c = plt.Circle(src, r, color=col, fill=False,
                               lw=lw_r, alpha=alpha, zorder=2)
                ax.add_patch(c)

        # เส้นประตามเส้นทาง
        ax.plot([s1[0], P[0]], [s1[1], P[1]], '--', color=CB, lw=1.0, alpha=0.4, zorder=3)
        ax.plot([s2[0], P[0]], [s2[1], P[1]], '--', color=CR, lw=1.0, alpha=0.4, zorder=3)

        # วาดคลื่นไซน์ตามเส้นทาง
        def draw_wave(src, dst, lam, color, amp=0.22, lw=2.2):
            vec  = dst - src
            dist = np.linalg.norm(vec)
            u    = vec / dist
            n    = np.array([-u[1], u[0]])
            t    = np.linspace(0, dist, 500)
            osc  = amp * np.sin(2 * np.pi * t / lam)
            pts  = np.array([src + t[i]*u + osc[i]*n for i in range(500)])
            ax.plot(pts[:,0], pts[:,1], color=color, lw=lw,
                    solid_capstyle='round', zorder=5)

        draw_wave(s1, P, lam, CB)
        draw_wave(s2, P, lam, CR)

        # Source markers
        for src, col, lbl in [(s1, CB, 'S₁'), (s2, CR, 'S₂')]:
            ax.plot(*src, 'o', color=col, ms=12, zorder=7,
                    markeredgecolor='white', markeredgewidth=1.6)
            ax.text(src[0]-0.35, src[1], lbl, color=col,
                    fontsize=12, fontweight='bold', ha='right', va='center')

        # P marker
        ax.plot(*P, 's', color=CG, ms=12, zorder=7,
                markeredgecolor='white', markeredgewidth=1.6)
        ax.text(P[0]+0.22, P[1]+0.22, 'P', color=CG,
                fontsize=13, fontweight='bold')

        # label r1, r2
        def label_path(src, dst, txt, color, side=1):
            vec  = dst - src
            dist = np.linalg.norm(vec)
            u    = vec / dist
            n    = np.array([-u[1], u[0]])
            mid  = src + 0.50 * vec
            off  = mid + side * 0.50 * n
            ang  = np.degrees(np.arctan2(vec[1], vec[0]))
            ax.text(off[0], off[1], txt, color=color, fontsize=9,
                    rotation=ang, ha='center', va='center', fontweight='700',
                    bbox=dict(fc='#f0f6ff', ec='none', pad=1.5, alpha=0.85),
                    zorder=8)

        label_path(s1, P, f'r₁ = {r1:.1f} cm', CB, side=+1)
        label_path(s2, P, f'r₂ = {r2:.1f} cm', CR, side=-1)

        # d annotation
        ax.annotate('', xy=(s1[0]-0.35, s1[1]),
                    xytext=(s1[0]-0.35, s2[1]),
                    arrowprops=dict(arrowstyle='<->', color=CGR, lw=1.3))
        ax.text(s1[0]-0.65, (s1[1]+s2[1])/2,
                f'd={abs(s1[1]-s2[1]):.1f}', color=CGR,
                fontsize=8, ha='right', va='center')

        # Δr callout
        ax.text(4.8, 5.70,
                f'Δr = |r₁ − r₂| = {dr:.2f} cm',
                fontsize=12, ha='center', fontweight='bold', color='#78350f',
                bbox=dict(boxstyle='round,pad=0.45', fc='#fef3c7',
                          ec='#f59e0b', lw=2.0), zorder=9)

        ax.set_title('Path difference Δr = difference in distance from S₁ and S₂ to point P',
                     fontsize=9.5, color=CDK, pad=6)
        fig.tight_layout(pad=0.5)
    return fig


# ═══════════════════════════════════════════════════════════════════════════════
#  FIGURE 3 — เงื่อนไขปฏิบัพและบัพ (2 panels)
# ═══════════════════════════════════════════════════════════════════════════════
def _fig_conditions():
    with plt.rc_context(RC):
        fig, axes = plt.subplots(1, 2, figsize=(9, 3.4))
        fig.patch.set_facecolor(CBG)

        panels = [
            (CG,   '#f0fdf4', '#bbf7d0',
             'Antinode — Constructive',
             r'$\Delta r = n\lambda$',
             r'$n = 0,\;1,\;2,\;3,\;\ldots$',
             'Amplitude = 2A',
             'crest + crest'),
            (CRED, '#fef2f2', '#fecaca',
             'Node — Destructive',
             r'$\Delta r = \left(n - \tfrac{1}{2}\right)\lambda$',
             r'$n = 1,\;2,\;3,\;\ldots$',
             'Amplitude = 0',
             'crest + trough'),
        ]
        for ax, (col, fc, hc, title, f1, f2, result, sub) in zip(axes, panels):
            ax.set_facecolor(fc)
            ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis('off')
            for sp in ['top','bottom','left','right']:
                ax.spines[sp].set_visible(True)
                ax.spines[sp].set_edgecolor(col)
                ax.spines[sp].set_linewidth(2.2)

            hbar = FancyBboxPatch((0, 0.82), 1, 0.18, boxstyle='square',
                                  fc=hc, ec='none',
                                  transform=ax.transAxes, clip_on=False)
            ax.add_patch(hbar)
            ax.text(0.5, 0.91, title, transform=ax.transAxes,
                    ha='center', va='center', fontsize=10,
                    fontweight='800', color=col)

            ax.text(0.5, 0.64, f1, transform=ax.transAxes,
                    ha='center', va='center', fontsize=14)
            ax.text(0.5, 0.44, f2, transform=ax.transAxes,
                    ha='center', va='center', fontsize=10.5)
            ax.text(0.5, 0.25, result, transform=ax.transAxes,
                    ha='center', va='center', fontsize=11,
                    fontweight='800', color=col)
            ax.text(0.5, 0.09, f'({sub})', transform=ax.transAxes,
                    ha='center', va='center', fontsize=8.5,
                    color=col, style='italic')

        fig.suptitle('Interference Conditions  (in-phase sources)',
                     fontsize=10, color=CGR, y=1.02)
        fig.tight_layout(pad=0.8)
    return fig


# ═══════════════════════════════════════════════════════════════════════════════
#  FIGURE 4 — แบบแผนการแทรกสอด (top view + lines)
# ═══════════════════════════════════════════════════════════════════════════════
def _fig_two_sources():
    with plt.rc_context(RC):
        fig, ax = plt.subplots(figsize=(7, 5.5))
        ax.set_aspect('equal')
        ax.set_facecolor('#f0f7ff')
        fig.patch.set_facecolor('#f0f7ff')

        lam   = 2.0
        s1    = np.array([0.0,  2.5])
        s2    = np.array([0.0, -2.5])
        d     = np.linalg.norm(s1 - s2)
        R_MAX = 8.0
        n_rings = int(R_MAX / lam) + 1

        for n in range(1, n_rings + 1):
            for src, col in [(s1, CB), (s2, CR)]:
                ax.add_patch(plt.Circle(src, n*lam, color=col, fill=False,
                                        lw=1.5, alpha=0.65, zorder=3))
                ax.add_patch(plt.Circle(src, (n-0.5)*lam, color=col, fill=False,
                                        lw=0.6, alpha=0.25, ls='--', zorder=2))

        n_max = int(d / lam)

        # antinodal lines
        for n in range(-n_max, n_max + 1):
            v = n * lam / d
            if abs(v) > 1: continue
            th   = np.arcsin(v)
            cos_ = np.cos(th); sin_ = np.sin(th)
            ax.plot([-R_MAX*cos_, R_MAX*cos_], [-R_MAX*sin_, R_MAX*sin_],
                    color=CG, lw=2.2 if n==0 else 1.5, alpha=0.9, zorder=4)
            lbl = 'A₀' if n == 0 else f'A{abs(n)}'
            ax.text(R_MAX*cos_*1.05, R_MAX*sin_*1.05, lbl,
                    color=CG, fontsize=8, fontweight='bold',
                    ha='center', va='center')
            if n != 0:
                ax.text(-R_MAX*cos_*1.05, -R_MAX*sin_*1.05, lbl,
                        color=CG, fontsize=8, fontweight='bold',
                        ha='center', va='center')

        # nodal lines
        for n in range(1, n_max + 1):
            for sign in [1, -1]:
                v = (n - 0.5) * lam / d
                if abs(v) > 1: continue
                th   = np.arcsin(sign * v)
                cos_ = np.cos(th); sin_ = np.sin(th)
                ax.plot([-R_MAX*cos_, R_MAX*cos_], [-R_MAX*sin_, R_MAX*sin_],
                        color=CRED, lw=1.0, ls='--', alpha=0.7, zorder=4)
                ax.text(R_MAX*cos_*1.05, R_MAX*sin_*1.05, f'N{n}',
                        color=CRED, fontsize=7.5, ha='center', va='center')
                ax.text(-R_MAX*cos_*1.05, -R_MAX*sin_*1.05, f'N{n}',
                        color=CRED, fontsize=7.5, ha='center', va='center')

        # Sources
        for src, col, lbl in [(s1, CB, 'S₁'), (s2, CR, 'S₂')]:
            ax.plot(*src, 'o', color=col, ms=11, zorder=8,
                    markeredgecolor='white', markeredgewidth=1.6)
            ax.text(src[0]-0.4, src[1], lbl, color=col,
                    fontsize=12, fontweight='bold', ha='right', va='center')

        # d annotation
        ax.annotate('', xy=(-0.55, s1[1]), xytext=(-0.55, s2[1]),
                    arrowprops=dict(arrowstyle='<->', color=CGR, lw=1.3))
        ax.text(-0.85, 0, f'd={int(d)}cm', color=CGR,
                fontsize=8.5, ha='center', va='center', rotation=90)

        h1 = mpatches.Patch(color=CG,   label=f'Antinodal lines ({2*n_max+1})')
        h2 = mpatches.Patch(color=CRED, label=f'Nodal lines ({2*n_max})',
                             fill=False, linestyle='--', edgecolor=CRED)
        l1 = mpatches.Patch(color=CB, fill=False, linewidth=1.4,
                             edgecolor=CB, label='Wavefront from S₁')
        l2 = mpatches.Patch(color=CR, fill=False, linewidth=1.4,
                             edgecolor=CR, label='Wavefront from S₂')
        ax.legend(handles=[l1, l2, h1, h2], fontsize=7.5,
                  loc='lower right', framealpha=0.92, edgecolor='#e2e8f0')

        ax.set_xlim(-9, 9); ax.set_ylim(-8.5, 8.5)
        ax.set_xlabel('x (cm)', fontsize=9, color=CGR)
        ax.set_ylabel('y (cm)', fontsize=9, color=CGR)
        ax.tick_params(labelsize=7.5)
        ax.set_title(f'd = {int(d)} cm,  λ = {int(lam)} cm  →  '
                     f'Antinodal: {2*n_max+1} lines,  Nodal: {2*n_max} lines',
                     fontsize=9, color=CDK, pad=5)
        ax.spines[['top','right']].set_visible(False)
        fig.tight_layout()
    return fig


# ═══════════════════════════════════════════════════════════════════════════════
#  FIGURE 5 — แนวปฏิบัพ/บัพ แบบเต็ม (full pattern)
# ═══════════════════════════════════════════════════════════════════════════════
def _fig_pattern():
    with plt.rc_context(RC):
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.set_facecolor('#f8fafc')
        fig.patch.set_facecolor('#f8fafc')
        ax.set_aspect('equal')

        d   = 10.0; lam = 2.5
        s1  = np.array([0.0,  d/2])
        s2  = np.array([0.0, -d/2])
        n_max = int(d / lam)
        R_MAX = 18

        for src, col in [(s1, CB), (s2, CR)]:
            for n in range(1, 9):
                ax.add_patch(plt.Circle(src, n*lam, color=col, fill=False,
                                        lw=0.8, alpha=0.16, zorder=1))

        for n in range(-n_max, n_max + 1):
            v = n * lam / d
            if abs(v) > 1: continue
            th   = np.arcsin(v)
            cos_ = np.cos(th); sin_ = np.sin(th)
            ax.plot([-R_MAX*cos_, R_MAX*cos_], [-R_MAX*sin_, R_MAX*sin_],
                    color=CG, lw=2.2 if n==0 else 1.6, alpha=0.9, zorder=4)
            lbl = 'A₀' if n == 0 else f'A{abs(n)}'
            ax.text(R_MAX*cos_*1.04, R_MAX*sin_*1.04, lbl,
                    color=CG, fontsize=8.5, fontweight='bold',
                    ha='center', va='center')
            if n != 0:
                ax.text(-R_MAX*cos_*1.04, -R_MAX*sin_*1.04, lbl,
                        color=CG, fontsize=8.5, fontweight='bold',
                        ha='center', va='center')

        for n in range(1, n_max + 1):
            for sign in [1, -1]:
                v = (n - 0.5) * lam / d
                if abs(v) > 1: continue
                th   = np.arcsin(sign * v)
                cos_ = np.cos(th); sin_ = np.sin(th)
                ax.plot([-R_MAX*cos_, R_MAX*cos_], [-R_MAX*sin_, R_MAX*sin_],
                        color=CRED, lw=1.2, ls='--', alpha=0.75, zorder=3)
                ax.text(R_MAX*cos_*1.04, R_MAX*sin_*1.04, f'N{n}',
                        color=CRED, fontsize=8, ha='center', va='center')
                ax.text(-R_MAX*cos_*1.04, -R_MAX*sin_*1.04, f'N{n}',
                        color=CRED, fontsize=8, ha='center', va='center')

        for src, col, lbl in [(s1, CB, 'S₁'), (s2, CR, 'S₂')]:
            ax.plot(*src, 'o', color=col, ms=11, zorder=8,
                    markeredgecolor='white', markeredgewidth=1.8)
            ax.text(src[0]-0.55, src[1], lbl, color=col,
                    fontsize=11, fontweight='bold', va='center')

        ax.annotate('', xy=(-0.65, s1[1]), xytext=(-0.65, s2[1]),
                    arrowprops=dict(arrowstyle='<->', color=CGR, lw=1.4))
        ax.text(-1.25, 0, f'd={int(d)} cm', color=CGR,
                fontsize=8, ha='center', va='center', rotation=90)
        ax.axhline(0, color=CGR, lw=0.7, ls=':', alpha=0.5)

        h1 = mpatches.Patch(color=CG,   label=f'Antinodal lines ({2*n_max+1})')
        h2 = mpatches.Patch(color=CRED, label=f'Nodal lines ({2*n_max})',
                             fill=False, linestyle='--', edgecolor=CRED)
        ax.legend(handles=[h1, h2], fontsize=8.5, loc='lower right',
                  framealpha=0.95, edgecolor='#e2e8f0')

        ax.set_xlim(-20, 20); ax.set_ylim(-12, 12)
        ax.set_xlabel('x (cm)', fontsize=9)
        ax.set_ylabel('y (cm)', fontsize=9)
        ax.set_title(f'd = {int(d)} cm,  λ = {lam} cm  →  '
                     f'Antinodal {2*n_max+1} lines,  Nodal {2*n_max} lines',
                     fontsize=9.5, fontweight='600', color=CDK)
        ax.spines[['top','right']].set_visible(False)
        fig.tight_layout()
    return fig


# ═══════════════════════════════════════════════════════════════════════════════
#  FIGURE 6 — ไม้บรรทัด S1S2 แสดงตำแหน่งบัพ/ปฏิบัพ
# ═══════════════════════════════════════════════════════════════════════════════
def _fig_ruler():
    with plt.rc_context(RC):
        fig, ax = plt.subplots(figsize=(10, 4.2))
        ax.set_facecolor(CBG)
        fig.patch.set_facecolor(CBG)
        d = 10.0; lam = 2.0
        ax.set_xlim(-0.6, 11.5); ax.set_ylim(-2.8, 3.0)
        ax.axis('off')

        ax.plot([-0.1, 10.3], [0, 0], color=CDK, lw=2.2,
                solid_capstyle='round', zorder=5)

        for xi in range(0, 11):
            ax.plot([xi, xi], [-0.16, 0.16], color=CGR, lw=0.9)
            ax.text(xi, -0.36, str(xi), ha='center', fontsize=7.5, color=CGR)
        ax.text(5, -0.65, 'Position along S₁S₂ (cm)',
                ha='center', fontsize=8.5, color=CGR)

        for xp, col, lbl in [(0, CB, 'S₁'), (10, CR, 'S₂')]:
            ax.plot(xp, 0, 'o', color=col, ms=14, zorder=7,
                    markeredgecolor='white', markeredgewidth=2)
            ax.text(xp, 0.50, lbl, ha='center', fontsize=11,
                    color=col, fontweight='bold')

        for xi in np.arange(0.0, d + 0.001, 0.5):
            r1 = xi; r2 = d - xi; dr = abs(r1 - r2)
            k  = dr / lam
            is_anti = abs(k - round(k)) < 0.01
            is_node = abs((k + 0.5) - round(k + 0.5)) < 0.01

            if is_anti:
                n = int(round(k))
                ax.plot(xi, 0, 'D', color=CG, ms=10, zorder=8,
                        markeredgecolor='white', markeredgewidth=1.3)
                ax.text(xi, 1.05, f'A{n}', ha='center', fontsize=8,
                        color=CG, fontweight='bold')
                ax.text(xi, 0.58, f'Δr={int(dr)}λ' if dr > 0 else 'Δr=0',
                        ha='center', fontsize=6.5, color=CG)
                ax.plot([xi, xi], [0.15, 0.52], color=CG, lw=0.7, alpha=0.5)

            elif is_node:
                n = int(round(k + 0.5))
                ax.plot(xi, 0, 'v', color=CRED, ms=9, zorder=8,
                        markeredgecolor='white', markeredgewidth=1.3)
                ax.text(xi, -1.05, f'N{n}', ha='center', fontsize=8,
                        color=CRED, fontweight='bold')
                ax.text(xi, -1.55, f'Δr={int(dr*2)//2}·λ/2',
                        ha='center', fontsize=6.5, color=CRED)
                ax.plot([xi, xi], [-0.15, -0.52], color=CRED, lw=0.7, alpha=0.5)

        ax.text(5.0, 2.70,
                f'd = {int(d)} cm,  λ = {int(lam)} cm  →  '
                f'Antinodal {int(d/lam)*2+1} lines,  Nodal {int(d/lam)*2} lines',
                ha='center', fontsize=10, fontweight='700', color=CDK,
                bbox=dict(boxstyle='round,pad=0.35', fc='#f1f5f9',
                          ec='#cbd5e1', lw=1.6))

        h1 = mpatches.Patch(color=CG,   label='Antinode (constructive)')
        h2 = mpatches.Patch(color=CRED, label='Node (destructive)')
        ax.legend(handles=[h1, h2], fontsize=8.5,
                  loc='upper left', framealpha=0.95, edgecolor='#e2e8f0')
        fig.tight_layout()
    return fig


# ═══════════════════════════════════════════════════════════════════════════════
#  FIGURE 7 — แหล่งกำเนิดเฟสตรงข้าม (in-phase vs anti-phase)
# ═══════════════════════════════════════════════════════════════════════════════
def _fig_antiphase():
    with plt.rc_context(RC):
        from matplotlib.gridspec import GridSpec
        fig = plt.figure(figsize=(10, 6.5))
        fig.patch.set_facecolor(CBG)
        gs = GridSpec(3, 2, figure=fig,
                      hspace=0.55, wspace=0.32,
                      left=0.12, right=0.97, top=0.88, bottom=0.07)

        x = np.linspace(0, 2, 500)
        col_cfgs = [
            (0,      'In-phase  (Δφ = 0)',      CG,   '#f0f7ff', '#f0fdf4', CG,
             'Antinode\nAmplitude = 2A'),
            (np.pi,  'Anti-phase  (Δφ = π)',   CRED, '#fff8f8', '#fff5f5', CRED,
             'Node\nAmplitude = 0'),
        ]
        row_labels = ['Wave from S₁', 'Wave from S₂', 'Resultant\n(surface)']
        row_colors = [CB, CR, CGR]

        for col_i, (src_phase, col_title, title_col,
                    bg_wave, bg_res, rcol, outcome) in enumerate(col_cfgs):
            w1  = np.sin(2*np.pi*x)
            w2  = np.sin(2*np.pi*x + src_phase)
            res = w1 + w2
            waves = [w1, w2, res]
            wcolors = [CB, CR, rcol]

            for row_i, (y, wc) in enumerate(zip(waves, wcolors)):
                ax = fig.add_subplot(gs[row_i, col_i])
                bg = bg_res if row_i == 2 else bg_wave
                ax.set_facecolor(bg)

                if row_i == 0:
                    ax.set_title(col_title, fontsize=9.5,
                                 color=title_col, fontweight='800', pad=6)

                fill_c = ('#bbf7d0' if (row_i==2 and rcol==CG) else
                          '#fecaca' if (row_i==2 and rcol==CRED) else '#dbeafe')
                ax.fill_between(x, y, 0, where=(y>=0), color=fill_c, alpha=0.5)
                ax.fill_between(x, y, 0, where=(y<0),  color=fill_c, alpha=0.2)
                ax.plot(x, y, color=wc, lw=2.4, solid_capstyle='round')
                ax.axhline(0, color='#94a3b8', lw=0.8, ls=':', zorder=1)

                amax = np.max(np.abs(y))
                if amax > 0.05:
                    ax.axhline( amax, color=wc, lw=0.9, ls='--', alpha=0.35)
                    ax.axhline(-amax, color=wc, lw=0.9, ls='--', alpha=0.35)

                ax.set_xlim(0, 2); ax.set_ylim(-2.6, 2.6)
                ax.set_xticks([0, 0.5, 1.0, 1.5, 2.0])
                ax.set_xticklabels(['0','λ/2','λ','3λ/2','2λ'], fontsize=8)
                ax.set_yticks([-2, -1, 0, 1, 2])
                ax.set_yticklabels(['-2A','-A','0','+A','+2A'], fontsize=8)
                ax.spines[['top','right']].set_visible(False)

                if col_i == 0:
                    ax.set_ylabel(row_labels[row_i], color=row_colors[row_i],
                                  fontsize=9, fontweight='700', labelpad=6)

                if row_i == 2:
                    badge_fc = '#dcfce7' if rcol==CG else '#fee2e2'
                    ax.text(0.97, 0.08, outcome,
                            transform=ax.transAxes, ha='right', va='bottom',
                            fontsize=9.5, fontweight='900', color=rcol,
                            bbox=dict(boxstyle='round,pad=0.3',
                                      fc=badge_fc, ec=rcol, lw=2.0))

        fig.suptitle('In-phase vs Anti-phase Sources  (Δr = 0)',
                     fontsize=11, fontweight='bold', color=CDK, y=0.96)
        fig.add_artist(plt.Line2D([0.545, 0.545], [0.06, 0.92],
                                  transform=fig.transFigure,
                                  color='#e2e8f0', lw=1.5, ls='--'))
    return fig


# ═══════════════════════════════════════════════════════════════════════════════
#  FIGURE 8 — คลื่นผ่านช่องสองช่องในแผ่นกั้น (top view)
# ═══════════════════════════════════════════════════════════════════════════════
def _fig_barrier():
    with plt.rc_context(RC):
        from matplotlib.patches import Rectangle, FancyArrowPatch
        fig, ax = plt.subplots(figsize=(10, 5.8))
        ax.set_facecolor('#f0f7ff')
        fig.patch.set_facecolor('#f0f7ff')

        # ── coordinate layout ──────────────────────────────────────────
        X_BARRIER = 0.0
        X_SCREEN  = 8.5
        X_LEFT    = -4.5
        Y_MAX     = 4.2

        d   = 2.4   # slit separation
        lam = 0.6
        n_max = 3
        slit_gap = 0.20   # half-width of slit opening

        s1 = np.array([X_BARRIER, +d/2])
        s2 = np.array([X_BARRIER, -d/2])

        ax.set_xlim(X_LEFT - 0.2, X_SCREEN + 1.6)
        ax.set_ylim(-Y_MAX - 0.3, Y_MAX + 0.5)
        ax.set_aspect('equal')
        ax.axis('off')

        # ── incoming plane wavefronts (left of barrier) ────────────────
        for xi in np.arange(X_LEFT + 0.3, X_BARRIER - 0.05, lam):
            ax.plot([xi, xi], [+d/2 + slit_gap, Y_MAX],
                    color=CB, lw=1.2, alpha=0.45, zorder=2)
            ax.plot([xi, xi], [-Y_MAX, -d/2 - slit_gap],
                    color=CB, lw=1.2, alpha=0.45, zorder=2)

        # arrow + label for plane wave
        ax.annotate('', xy=(X_BARRIER - 0.6, 0), xytext=(X_LEFT + 0.4, 0),
                    arrowprops=dict(arrowstyle='->', color=CB, lw=2.0,
                                   mutation_scale=18), zorder=9)
        ax.text(X_LEFT + 0.1, 0.75, 'Plane wave\nentering',
                color=CB, fontsize=8.5, ha='left', va='bottom',
                fontweight='600', zorder=9)

        # ── barrier ────────────────────────────────────────────────────
        bw = 0.22
        barrier_segs = [
            (-Y_MAX,          -d/2 - slit_gap),
            (-d/2 + slit_gap,  d/2 - slit_gap),   # mid block (between slits)
            ( d/2 + slit_gap,  Y_MAX),
        ]
        for y0, y1 in barrier_segs:
            ax.add_patch(Rectangle((X_BARRIER - bw, y0), 2*bw, y1 - y0,
                                   fc='#475569', ec='none', alpha=0.88, zorder=6))
        ax.text(X_BARRIER - bw - 0.15, -Y_MAX + 0.1, 'Barrier',
                color='#475569', fontsize=7.5, ha='right', va='bottom',
                fontweight='700', zorder=9)

        # ── slit markers (S₁ and S₂) ────────────────────────────────
        for src, col, lbl in [(s1, CB, 'S₁'), (s2, CR, 'S₂')]:
            ax.plot(*src, 'D', color=col, ms=9, zorder=10,
                    markeredgecolor='white', markeredgewidth=1.5)
            ax.text(src[0] + 0.38, src[1], lbl, color=col,
                    fontsize=9, va='center', fontweight='700', zorder=10)

        # ── d annotation ───────────────────────────────────────────────
        x_ann = X_BARRIER - 1.0
        ax.annotate('', xy=(x_ann, s1[1]), xytext=(x_ann, s2[1]),
                    arrowprops=dict(arrowstyle='<->', color=CGR, lw=1.4))
        ax.text(x_ann - 0.25, 0, 'd', fontsize=12, color=CDK,
                ha='center', va='center', fontweight='bold')

        # ── circular wavefronts from each slit ────────────────────────
        for src, col in [(s1, CB), (s2, CR)]:
            for n in range(1, 18):
                r     = n * lam
                alpha = max(0.05, 0.55 - n * 0.035)
                lw_c  = 1.3 if n % 2 != 0 else 0.6
                circ = plt.Circle(src, r, color=col, fill=False,
                                  lw=lw_c, alpha=alpha, zorder=2)
                ax.add_patch(circ)

        # mask — hide wavefronts left of barrier
        ax.add_patch(Rectangle((X_LEFT - 0.5, -Y_MAX - 0.5),
                                abs(X_LEFT) + 0.5 + bw, 2*(Y_MAX + 0.5),
                                fc='#f0f7ff', ec='none', zorder=3))

        # ── screen ─────────────────────────────────────────────────────
        ax.plot([X_SCREEN, X_SCREEN], [-Y_MAX, Y_MAX],
                color='#1e293b', lw=3.5, zorder=6, solid_capstyle='round')
        ax.text(X_SCREEN + 0.12, Y_MAX - 0.1, 'Screen',
                color='#1e293b', fontsize=8, va='top', fontweight='600')

        # ── antinodal lines → label at screen ─────────────────────────
        for n in range(-n_max, n_max + 1):
            v = n * lam / d
            if abs(v) > 1: continue
            th   = np.arcsin(v)
            y_sc = X_SCREEN * np.tan(th)
            if abs(y_sc) > Y_MAX + 0.2: continue
            lw_a  = 2.2 if n == 0 else 1.6
            ax.plot([X_BARRIER, X_SCREEN], [0, y_sc],
                    color=CG, lw=lw_a, alpha=0.85, zorder=4)
            ax.plot(X_SCREEN, y_sc, 'o', color=CG, ms=6, zorder=7,
                    markeredgecolor='white', markeredgewidth=1.2)
            lbl = 'A₀  (central max)' if n == 0 else f'A{abs(n)}'
            va  = 'bottom' if y_sc > 0.3 else ('top' if y_sc < -0.3 else 'center')
            ax.text(X_SCREEN + 0.18, y_sc, lbl,
                    color=CG, fontsize=8, fontweight='bold',
                    va=va, ha='left', zorder=8)

        # ── nodal lines → label at screen ─────────────────────────────
        for n in range(1, n_max + 1):
            for sign in [1, -1]:
                v = (n - 0.5) * lam / d
                if abs(v) > 1: continue
                th   = np.arcsin(sign * v)
                y_sc = X_SCREEN * np.tan(th)
                if abs(y_sc) > Y_MAX + 0.2: continue
                ax.plot([X_BARRIER, X_SCREEN], [0, y_sc],
                        color=CRED, lw=1.1, ls='--', alpha=0.65, zorder=4)
                ax.plot(X_SCREEN, y_sc, 'x', color=CRED, ms=5,
                        markeredgewidth=1.5, zorder=7)
                va = 'bottom' if y_sc > 0.3 else ('top' if y_sc < -0.3 else 'center')
                ax.text(X_SCREEN + 0.18, y_sc, f'N{n}',
                        color=CRED, fontsize=7.5,
                        va=va, ha='left', zorder=8)

        # ── θ₁ angle arc ───────────────────────────────────────────────
        th1 = np.arcsin(lam / d)
        ax.add_patch(Arc((X_BARRIER, 0), 2.8, 2.8, angle=0,
                         theta1=0, theta2=np.degrees(th1),
                         color='#7c3aed', lw=1.8, zorder=7))
        ax.text(X_BARRIER + 1.7, 0.30, 'θ₁', fontsize=10,
                color='#7c3aed', fontweight='bold', zorder=8)

        # ── L annotation (barrier → screen) ───────────────────────────
        y_arr = -Y_MAX + 0.05
        ax.annotate('', xy=(X_SCREEN, y_arr), xytext=(X_BARRIER, y_arr),
                    arrowprops=dict(arrowstyle='<->', color=CGR, lw=1.2,
                                   mutation_scale=12))
        ax.text((X_BARRIER + X_SCREEN) / 2, y_arr - 0.42,
                'L  (distance to screen)',
                ha='center', fontsize=8, color=CGR)

        # ── legend ─────────────────────────────────────────────────────
        import matplotlib.patches as mpatches
        import matplotlib.lines as mlines
        leg_A = mlines.Line2D([], [], color=CG,   lw=2, label='Antinodal line (constructive)')
        leg_N = mlines.Line2D([], [], color=CRED, lw=1.2, ls='--', label='Nodal line (destructive)')
        ax.legend(handles=[leg_A, leg_N], fontsize=7.5,
                  loc='upper left', framealpha=0.92, edgecolor='#e2e8f0')

        ax.set_title('Top view — double-slit interference',
                     fontsize=10, color=CDK, pad=6, fontweight='700')
        fig.tight_layout(pad=0.4)
    return fig


# ═══════════════════════════════════════════════════════════════════════════════
#  FIGURE 9 — flowchart 3 ขั้นตอน
# ═══════════════════════════════════════════════════════════════════════════════
def _fig_flowchart():
    with plt.rc_context(RC):
        fig, ax = plt.subplots(figsize=(9.5, 2.8))
        ax.axis('off')
        ax.set_facecolor(CBG)
        fig.patch.set_facecolor(CBG)
        ax.set_xlim(0, 9.5); ax.set_ylim(0, 2.8)

        steps = [
            (1.18, '#1e3a8a', '#eff6ff',
             'Step 1',
             r'$\Delta r = |r_1 - r_2|$'),
            (3.80, '#065f46', '#f0fdf4',
             'Step 2',
             r'$k = \Delta r \;/\; \lambda$'),
            (6.42, '#78350f', '#fefce8',
             'Step 3',
             'Is k a whole\nnumber or n − ½?'),
        ]
        for xc, bc, fc, title, body in steps:
            ax.add_patch(FancyBboxPatch((xc-1.05, 0.38), 2.10, 2.06,
                                        boxstyle='round,pad=0.08',
                                        fc=fc, ec=bc, lw=2.2))
            ax.text(xc, 2.30, title, ha='center', va='center',
                    fontsize=9, fontweight='800', color=bc)
            ax.text(xc, 1.42, body, ha='center', va='center', fontsize=11)

        for xa in [2.25, 4.87]:
            ax.annotate('', xy=(xa+0.48, 1.42), xytext=(xa, 1.42),
                        arrowprops=dict(arrowstyle='->',
                                        color='#94a3b8', lw=2.0))

        ax.annotate('', xy=(7.53, 2.22), xytext=(7.47, 1.42),
                    arrowprops=dict(arrowstyle='->', color=CG, lw=1.8))
        ax.annotate('', xy=(7.53, 0.60), xytext=(7.47, 1.42),
                    arrowprops=dict(arrowstyle='->', color=CRED, lw=1.8))

        for yc, col, fc2, txt in [
            (2.28,  CG,   '#dcfce7', 'k = 0,1,2,…\n→ Antinode'),
            (0.55,  CRED, '#fee2e2', 'k = ½,1½,…\n→ Node'),
        ]:
            ax.add_patch(FancyBboxPatch((7.56, yc-0.38), 1.85, 0.76,
                                        boxstyle='round,pad=0.06',
                                        fc=fc2, ec=col, lw=1.9))
            ax.text(8.44, yc, txt, ha='center', va='center',
                    fontsize=8.5, color=col, fontweight='700')

        ax.set_title('3-Step method — works for every interference problem',
                     fontsize=9.5, color=CGR, pad=4)
        fig.tight_layout(pad=0.3)
    return fig


# ═══════════════════════════════════════════════════════════════════════════════
#  MAIN RENDER
# ═══════════════════════════════════════════════════════════════════════════════
def render_summary():
    st.markdown(_CSS, unsafe_allow_html=True)

    # ── Hero ──────────────────────────────────────────────────────────────────
    st.markdown("""
<div class="hero">
  <h1>🌊 Wave Interference</h1>
  <p>Coherent sources · superposition · path difference · counting lines · double-slit geometry<br>
     Physics · Grade 11 · Mechanical Waves</p>
  <div class="hero-meta">
    <span class="hero-tag">Coherent Sources</span>
    <span class="hero-tag">Path Difference</span>
    <span class="hero-tag">Antinodes &amp; Nodes</span>
    <span class="hero-tag">Double Slit</span>
  </div>
</div>
""", unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════════════
    # 01  Coherent Sources
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown('<p class="sh"><span class="pill">01</span>Coherent Sources</p>',
                unsafe_allow_html=True)

    c1, c2 = st.columns(2, gap="large")
    with c1:
        st.markdown("""
<div class="card cb">
<h4>📖 Definition</h4>
<p>Two sources are <strong>coherent</strong> when they share:</p>
<ul>
  <li>The <strong>same frequency</strong></li>
  <li>A <strong>constant phase difference</strong> (does not drift over time)</li>
</ul>
<p>In practice: two prongs on the same motor in a ripple tank, or two slits illuminated by one source.</p>
</div>
""", unsafe_allow_html=True)
    with c2:
        st.markdown("""
<div class="card cs">
<h4>⚡ Two Cases</h4>
<ul>
  <li><strong>In-phase</strong> (Δφ = 0) — crests leave both sources simultaneously</li>
  <li><strong>Anti-phase</strong> (Δφ = π) — one emits a crest while the other emits a trough</li>
</ul>
<p>Most problems say "in-phase." If unspecified, assume in-phase.</p>
</div>
""", unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════════════
    # 02  Superposition
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown('<hr class="div"><p class="sh"><span class="pill">02</span>'
                'Superposition Principle</p>', unsafe_allow_html=True)

    _show("superposition",
          "Top: crest + crest → 2A (constructive)  |  Bottom: crest + trough → 0 (destructive)")

    c1, c2 = st.columns(2, gap="large")
    with c1:
        st.markdown("""
<div class="card cg">
<h4>✅ Constructive — Antinode</h4>
<ul>
  <li>Crest meets crest  <em>or</em>  trough meets trough</li>
  <li>Waves arrive <strong>in phase</strong></li>
  <li>Resultant amplitude = <strong>2A</strong>  (maximum)</li>
</ul>
</div>
""", unsafe_allow_html=True)
    with c2:
        st.markdown("""
<div class="card cr">
<h4>❌ Destructive — Node</h4>
<ul>
  <li>Crest meets trough</li>
  <li>Waves arrive <strong>180° out of phase</strong></li>
  <li>Resultant amplitude = <strong>0</strong>  (surface still)</li>
</ul>
</div>
""", unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════════════
    # 03  Path Difference
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown('<hr class="div"><p class="sh"><span class="pill">03</span>'
                'Path Difference  Δr</p>', unsafe_allow_html=True)

    c1, c2 = st.columns([1.4, 1], gap="large")
    with c1:
        _show("path_diff",
              "Rings = wavefronts (crests)  ·  Curves = actual wave paths r₁ and r₂ to point P")
    with c2:
        st.markdown("""
<div class="card cb">
<h4>📐 What is Δr?</h4>
<p>The <strong>difference in distance</strong> each wave travels to reach point P.</p>
</div>
""", unsafe_allow_html=True)
        st.latex(r"\Delta r = |r_1 - r_2|")
        st.markdown("""
<div class="card cg" style="margin-top:10px">
<h4>✅ Antinode condition</h4>
<p>Waves travel exactly <em>n whole wavelengths</em> apart → arrive in phase.</p>
</div>
""", unsafe_allow_html=True)
        st.latex(r"\Delta r = n\lambda \quad (n = 0,1,2,\ldots)")
        st.markdown("""
<div class="card cr" style="margin-top:10px">
<h4>❌ Node condition</h4>
<p>Waves travel a <em>half-wavelength</em> extra → arrive 180° out of phase.</p>
</div>
""", unsafe_allow_html=True)
        st.latex(r"\Delta r = \!\left(n-\tfrac{1}{2}\right)\lambda \quad (n = 1,2,3,\ldots)")

    # ══════════════════════════════════════════════════════════════════════════
    # 04  Interference Pattern
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown('<hr class="div"><p class="sh"><span class="pill">04</span>'
                'Interference Pattern — Top View</p>', unsafe_allow_html=True)

    _show("conditions",
          "Left panel: antinodal condition  ·  Right panel: nodal condition  (in-phase sources)")

    c1, c2 = st.columns(2, gap="large")
    with c1:
        _show("two_sources",
              "Solid green = antinodal lines  ·  Dashed red = nodal lines  ·  d = 5 cm, λ = 2 cm")
    with c2:
        _show("pattern",
              "d = 10 cm, λ = 2.5 cm  →  9 antinodal lines, 8 nodal lines")

    st.markdown("""
<div class="card cb">
<h4>🗺️ Reading the Diagram</h4>
<ul>
  <li><strong>Blue rings</strong> = crests from S₁ &nbsp;·&nbsp; <strong>Red rings</strong> = crests from S₂</li>
  <li>Blue meets blue → crest + crest → <span class="tg"><strong>Antinode</strong></span></li>
  <li>Blue meets red &nbsp;→ crest + trough → <span class="tr"><strong>Node</strong></span></li>
  <li>Connecting all antinodes gives a <strong>solid antinodal line</strong> (hyperbola)</li>
  <li>Connecting all nodes gives a <strong>dashed nodal line</strong></li>
</ul>
</div>
""", unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════════════
    # 05  Counting Lines
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown('<hr class="div"><p class="sh"><span class="pill">05</span>'
                'Counting Antinodal &amp; Nodal Lines</p>', unsafe_allow_html=True)

    _show("ruler",
          "◆ antinodal positions above axis  ·  ▼ nodal positions below axis  "
          "(d = 10 cm, λ = 2 cm  →  n₀ = 5)")

    c1, c2 = st.columns([1, 1.1], gap="large")
    with c1:
        st.markdown("""
<div class="card cb">
<h4>Step 1 — Find n₀</h4>
</div>
""", unsafe_allow_html=True)
        st.latex(r"n_0 = \left\lfloor \frac{d}{\lambda} \right\rfloor"
                 r"\quad \text{(take integer part)}")
        st.markdown("""
<div class="card cg" style="margin-top:10px">
<h4>Step 2 — Count</h4>
<ul>
  <li>Antinodal lines total = <strong>2n₀ + 1</strong></li>
  <li>Nodal lines total &nbsp;&nbsp;&nbsp;&nbsp;= <strong>2n₀</strong></li>
</ul>
</div>
<div class="card cy" style="margin-top:10px">
<h4>📝 Example</h4>
<p>d = 12 cm, λ = 4 cm &nbsp;→&nbsp; n₀ = <strong>3</strong></p>
<ul>
  <li>Antinodal lines = 2×3 + 1 = <span class="tg">7</span></li>
  <li>Nodal lines &nbsp;&nbsp;&nbsp;&nbsp;= 2×3 &nbsp;&nbsp;&nbsp;&nbsp;= <span class="tr">6</span></li>
</ul>
</div>
""", unsafe_allow_html=True)
    with c2:
        st.markdown("""
<table class="rt">
<thead><tr>
  <th>Region</th>
  <th class="tg">Antinodal</th>
  <th class="tr">Nodal</th>
</tr></thead>
<tbody>
<tr>
  <td>Entire S₁S₂ line</td>
  <td class="tg">2n₀ + 1</td>
  <td class="tr">2n₀</td>
</tr>
<tr>
  <td>Between S₁ and S₂ only</td>
  <td class="tg">2n₀ − 1</td>
  <td class="tr">2n₀ − 2</td>
</tr>
</tbody>
</table>
<p style="font-size:.78rem;color:#64748b;margin-top:8px">
  ※ Valid when d/λ is a whole number.
  If d/λ has a remainder, count carefully using Δr conditions.
</p>
<div class="card cp" style="margin-top:14px">
<h4>⚠️ Quick Check</h4>
<ul>
  <li>The central line (Δr = 0) is <strong>always an antinode</strong> for in-phase sources</li>
  <li>Antinodal and nodal lines <strong>alternate</strong> outward from centre</li>
  <li>Label: A₀ (centre), A₁, A₂ … and N₁, N₂ …</li>
</ul>
</div>
""", unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════════════
    # 06  3-Step Method
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown('<hr class="div"><p class="sh"><span class="pill">06</span>'
                '3-Step Problem Method</p>', unsafe_allow_html=True)

    _show("flowchart")

    st.markdown("""
<div class="keytip">
💡 <strong>Golden rule:</strong>&nbsp;
Compute  k = Δr ÷ λ &nbsp;—&nbsp;
k whole number → <strong>Antinode</strong> &nbsp;·&nbsp;
k ends in .5 → <strong>Node</strong>
</div>
""", unsafe_allow_html=True)

    c1, c2 = st.columns(2, gap="large")
    with c1:
        st.markdown("""
<div class="card cy">
<h4>Example A — identify the line</h4>
<p>λ = 2.5 cm &nbsp;·&nbsp; r₁ = 12 cm, r₂ = 17 cm</p>
<ul>
  <li>Δr = |12 − 17| = <strong>5 cm</strong></li>
  <li>k = 5 ÷ 2.5 = <strong>2.0</strong> &nbsp;(integer)</li>
  <li>→ <span class="tg">Antinode A₂</span></li>
</ul>
</div>
""", unsafe_allow_html=True)
    with c2:
        st.markdown("""
<div class="card cy">
<h4>Example B — identify the line</h4>
<p>λ = 2.5 cm &nbsp;·&nbsp; r₁ = 14.5 cm, r₂ = 15.75 cm</p>
<ul>
  <li>Δr = |14.5 − 15.75| = <strong>1.25 cm</strong></li>
  <li>k = 1.25 ÷ 2.5 = <strong>0.5</strong> &nbsp;(ends in .5)</li>
  <li>→ <span class="tr">Node N₁</span></li>
</ul>
</div>
""", unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════════════
    # 07  Anti-phase Sources
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown('<hr class="div"><p class="sh"><span class="pill">07</span>'
                'Anti-phase Sources  (Δφ = 180°)</p>', unsafe_allow_html=True)

    _show("antiphase",
          "Left: in-phase → Δr = 0 gives Antinode  ·  Right: anti-phase → Δr = 0 gives Node")

    c1, c2 = st.columns(2, gap="large")
    with c1:
        st.markdown("""
<div class="card cr">
<h4>⚠️ Conditions Are Swapped</h4>
<p>Anti-phase sources start 180° apart, so every Δr condition flips.</p>
</div>
""", unsafe_allow_html=True)
        st.markdown("""
<table class="rt">
<thead>
  <tr><th>Δr</th><th>In-phase</th><th>Anti-phase</th></tr>
</thead>
<tbody>
  <tr><td>0, λ, 2λ …</td>
      <td class="tg">Antinode</td><td class="tr">Node</td></tr>
  <tr><td>½λ, 1½λ …</td>
      <td class="tr">Node</td><td class="tg">Antinode</td></tr>
</tbody>
</table>
""", unsafe_allow_html=True)
    with c2:
        st.markdown("""
<div class="card cy">
<h4>💡 Intuition</h4>
<p>The source phase shift of 180° acts like an extra Δr = λ/2:</p>
<ul>
  <li>Δr = 0 → phase gap from path = 0° → add 180° from source → total <strong>180°</strong> → <span class="tr">Node</span></li>
  <li>Δr = λ/2 → phase gap = 180° → add 180° → total <strong>360° = 0°</strong> → <span class="tg">Antinode</span></li>
</ul>
<p><strong>Shortcut:</strong> treat anti-phase like in-phase but swap every label.</p>
</div>
""", unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════════════
    # 08  Double-Slit Geometry
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown('<hr class="div"><p class="sh"><span class="pill">08</span>'
                'Double-Slit Geometry</p>', unsafe_allow_html=True)

    _show("barrier",
          "Plane wave diffracts through both slits then interferes  ·  "
          "d = slit separation  ·  L = distance to screen  ·  θ₁ = angle to 1st antinode")

    c1, c2 = st.columns([1, 1], gap="large")
    with c1:
        st.markdown('<div class="card cb"><h4>📐 Formulae</h4></div>',
                    unsafe_allow_html=True)
        st.markdown("**n-th antinodal angle:**")
        st.latex(r"\sin\theta_n = \frac{n\lambda}{d}")
        st.markdown("**n-th antinodal position on screen:**")
        st.latex(r"x_n = \frac{n\lambda L}{d}")
        st.markdown("**Fringe spacing  Δx:**")
        st.latex(r"\Delta x = \frac{\lambda L}{d}")
        st.markdown("**n-th nodal angle:**")
        st.latex(r"\sin\theta_n = \frac{(n-\tfrac{1}{2})\lambda}{d}")
    with c2:
        st.markdown("""
<div class="card cg">
<h4>📝 Worked Example</h4>
<p>d = 4 cm &nbsp;·&nbsp; λ = 2 cm &nbsp;·&nbsp; L = 30 cm</p>
<ul>
  <li>x₁ = 1 × 2 × 30 / 4 = <strong>15 cm</strong></li>
  <li>x₂ = 2 × 2 × 30 / 4 = <strong>30 cm</strong></li>
  <li>Δx = 2 × 30 / 4 = <strong>15 cm</strong> (constant)</li>
</ul>
</div>
<div class="card cs" style="margin-top:10px">
<h4>Trends</h4>
<ul>
  <li>d ↑ → Δx ↓ (fringes closer)</li>
  <li>λ ↑ → Δx ↑ (fringes wider)</li>
  <li>L ↑ → Δx ↑ (fringes wider)</li>
</ul>
</div>
""", unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════════════
    # REF
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown('<hr class="div"><p class="sh"><span class="pill">REF</span>'
                'Formula Reference</p>', unsafe_allow_html=True)

    st.markdown("""
<table class="rt">
<thead><tr>
  <th>Quantity</th>
  <th class="tg">Antinode (constructive)</th>
  <th class="tr">Node (destructive)</th>
</tr></thead>
<tbody>
<tr>
  <td><strong>Δr — in-phase</strong></td>
  <td class="tg">0, λ, 2λ, 3λ …</td>
  <td class="tr">½λ, 1½λ, 2½λ …</td>
</tr>
<tr>
  <td><strong>Δr — anti-phase</strong></td>
  <td class="tg">½λ, 1½λ, 2½λ …</td>
  <td class="tr">0, λ, 2λ, 3λ …</td>
</tr>
<tr>
  <td><strong>Total lines (in-phase)</strong></td>
  <td class="tg">2n₀ + 1</td>
  <td class="tr">2n₀</td>
</tr>
<tr>
  <td><strong>Between S₁ S₂ (in-phase)</strong></td>
  <td class="tg">2n₀ − 1</td>
  <td class="tr">2n₀ − 2</td>
</tr>
<tr>
  <td><strong>Angle to n-th line</strong></td>
  <td class="tg">sin θ = nλ/d</td>
  <td class="tr">sin θ = (n−½)λ/d</td>
</tr>
<tr>
  <td><strong>Screen position (small θ)</strong></td>
  <td class="tg">xₙ = nλL/d</td>
  <td class="tr">xₙ = (n−½)λL/d</td>
</tr>
<tr>
  <td><strong>Resultant amplitude</strong></td>
  <td class="tg">2A</td>
  <td class="tr">0</td>
</tr>
</tbody>
</table>
""", unsafe_allow_html=True)

    st.markdown("""
<div class="keytip" style="margin-top:16px">
💡 <strong>Remember:</strong>&nbsp;
k = Δr ÷ λ &nbsp;·&nbsp;
k = integer → <strong>Antinode</strong> &nbsp;·&nbsp;
k = n − ½ → <strong>Node</strong> &nbsp;·&nbsp;
Anti-phase sources: swap every label.
</div>
""", unsafe_allow_html=True)
