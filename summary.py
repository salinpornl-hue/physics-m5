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
@import url('https://fonts.googleapis.com/css2?family=Sarabun:wght@300;400;600;700&display=swap');
.sum-wrap { font-family: 'Sarabun', sans-serif; }

.hero {
    background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 55%, #2563eb 100%);
    border-radius: 16px;
    padding: 36px 32px 28px;
    color: #fff;
    margin-bottom: 28px;
}
.hero h1 { font-size: 1.9rem; font-weight: 800; margin: 0 0 6px; }
.hero p  { color: #93c5fd; margin: 0; font-size: .97rem; line-height: 1.55; }
.hero-meta { margin-top: 14px; display: flex; gap: 10px; flex-wrap: wrap; }
.hero-tag {
    background: rgba(255,255,255,0.13);
    border: 1px solid rgba(255,255,255,0.22);
    color: #e0f2fe;
    font-size: .72rem; font-weight: 600;
    padding: 3px 11px; border-radius: 20px;
}

.sh {
    font-size: 1.1rem; font-weight: 700; color: #0f172a;
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
.card p, .card li { font-size: .91rem; color: #374151; line-height: 1.75; }
.card ul { margin: 6px 0 0; padding-left: 18px; }

.rt { width:100%; border-collapse:collapse; font-size:.87rem; border-radius:10px; overflow:hidden; }
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

.step-row {
    display: flex; gap: 10px; align-items: stretch;
    margin: 14px 0;
}
.step-box {
    flex: 1;
    border-radius: 10px;
    padding: 14px 16px;
    font-size: .88rem;
}
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
            (0,      CG,   '#f0fdf4', 'คลื่นเสริมกัน (เฟสตรงกัน)',   '#bbf7d0'),
            (np.pi,  CRED, '#fff5f5', 'คลื่นหักล้างกัน (เฟสตรงข้าม)', '#fecaca'),
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
                    ax.set_title('คลื่นจาก S₁', fontsize=9, color=CB, fontweight='bold', pad=3)
                elif col == 1:
                    y, color = w2, CR
                    ax.set_title('คลื่นจาก S₂', fontsize=9, color=CR, fontweight='bold', pad=3)
                else:
                    y, color = res, rcol
                    ax.set_title('ผลรวม (ผิวน้ำ)', fontsize=9, color=rcol, fontweight='bold', pad=3)

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
                    label = f'แอมพลิจูด = {amax:.0f}A' if amax > 0.1 else 'แอมพลิจูด = 0\n(น้ำนิ่ง)'
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

        fig.suptitle('หลักการซ้อนทับของคลื่น ณ จุดคงที่บนผิวน้ำ',
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

        ax.set_title('ผลต่างเส้นทาง Δr = ระยะต่างที่คลื่นทั้งสองเดินทางมาถึงจุด P',
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
             'ปฏิบัพ — คลื่นเสริมกัน',
             r'$\Delta r = n\lambda$',
             r'$n = 0,\;1,\;2,\;3,\;\ldots$',
             'แอมพลิจูด = 2A',
             'สันคลื่น + สันคลื่น'),
            (CRED, '#fef2f2', '#fecaca',
             'บัพ — คลื่นหักล้างกัน',
             r'$\Delta r = \left(n - \tfrac{1}{2}\right)\lambda$',
             r'$n = 1,\;2,\;3,\;\ldots$',
             'แอมพลิจูด = 0',
             'สันคลื่น + ท้องคลื่น'),
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

        fig.suptitle('เงื่อนไขการแทรกสอด (แหล่งกำเนิดเฟสตรงกัน)',
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

        h1 = mpatches.Patch(color=CG,   label=f'แนวปฏิบัพ ({2*n_max+1} แนว)')
        h2 = mpatches.Patch(color=CRED, label=f'แนวบัพ ({2*n_max} แนว)',
                             fill=False, linestyle='--', edgecolor=CRED)
        l1 = mpatches.Patch(color=CB, fill=False, linewidth=1.4,
                             edgecolor=CB, label='หน้าคลื่นจาก S₁')
        l2 = mpatches.Patch(color=CR, fill=False, linewidth=1.4,
                             edgecolor=CR, label='หน้าคลื่นจาก S₂')
        ax.legend(handles=[l1, l2, h1, h2], fontsize=7.5,
                  loc='lower right', framealpha=0.92, edgecolor='#e2e8f0')

        ax.set_xlim(-9, 9); ax.set_ylim(-8.5, 8.5)
        ax.set_xlabel('x (cm)', fontsize=9, color=CGR)
        ax.set_ylabel('y (cm)', fontsize=9, color=CGR)
        ax.tick_params(labelsize=7.5)
        ax.set_title(f'd = {int(d)} cm,  λ = {int(lam)} cm  →  '
                     f'ปฏิบัพ: {2*n_max+1} แนว,  บัพ: {2*n_max} แนว',
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

        h1 = mpatches.Patch(color=CG,   label=f'แนวปฏิบัพ ({2*n_max+1} แนว)')
        h2 = mpatches.Patch(color=CRED, label=f'แนวบัพ ({2*n_max} แนว)',
                             fill=False, linestyle='--', edgecolor=CRED)
        ax.legend(handles=[h1, h2], fontsize=8.5, loc='lower right',
                  framealpha=0.95, edgecolor='#e2e8f0')

        ax.set_xlim(-20, 20); ax.set_ylim(-12, 12)
        ax.set_xlabel('x (cm)', fontsize=9)
        ax.set_ylabel('y (cm)', fontsize=9)
        ax.set_title(f'd = {int(d)} cm,  λ = {lam} cm  →  '
                     f'ปฏิบัพ {2*n_max+1} แนว,  บัพ {2*n_max} แนว',
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
        ax.text(5, -0.65, 'ตำแหน่งบนเส้น S₁S₂ (cm)',
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
                f'ปฏิบัพ {int(d/lam)*2+1} แนว,  บัพ {int(d/lam)*2} แนว',
                ha='center', fontsize=10, fontweight='700', color=CDK,
                bbox=dict(boxstyle='round,pad=0.35', fc='#f1f5f9',
                          ec='#cbd5e1', lw=1.6))

        h1 = mpatches.Patch(color=CG,   label='ปฏิบัพ (คลื่นเสริมกัน)')
        h2 = mpatches.Patch(color=CRED, label='บัพ (คลื่นหักล้างกัน)')
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
            (0,      'เฟสตรงกัน  (Δφ = 0)',     CG,   '#f0f7ff', '#f0fdf4', CG,
             'ปฏิบัพ\nแอมพลิจูด = 2A'),
            (np.pi,  'เฟสตรงข้าม  (Δφ = π)',    CRED, '#fff8f8', '#fff5f5', CRED,
             'บัพ\nแอมพลิจูด = 0'),
        ]
        row_labels = ['คลื่นจาก S₁', 'คลื่นจาก S₂', 'ผลรวม\n(ผิวน้ำ)']
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

        fig.suptitle('เปรียบเทียบ: แหล่งกำเนิดเฟสตรงกัน vs เฟสตรงข้าม  (Δr = 0)',
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
        from matplotlib.patches import Rectangle
        fig, ax = plt.subplots(figsize=(10, 5.5))
        ax.set_facecolor('#f0f7ff')
        fig.patch.set_facecolor('#f0f7ff')

        X_LEFT, X_RIGHT, Y_MAX = -5.5, 11.5, 4.8
        ax.set_xlim(X_LEFT - 0.3, X_RIGHT + 0.2)
        ax.set_ylim(-Y_MAX - 0.4, Y_MAX + 0.4)
        ax.set_aspect('equal')
        ax.axis('off')

        d = 2.0; lam = 0.6; n_max = 3
        s1 = np.array([0.0,  d/2])
        s2 = np.array([0.0, -d/2])
        gap = 0.25

        # incoming plane wave (left side)
        for xi in np.arange(X_LEFT + 0.3, -0.05, lam):
            ax.plot([xi, xi], [d/2 + gap, Y_MAX],
                    color=CB, lw=1.3, alpha=0.50, zorder=8)
            ax.plot([xi, xi], [-Y_MAX, -d/2 - gap],
                    color=CB, lw=1.3, alpha=0.50, zorder=8)

        ax.annotate('', xy=(-0.8, 0), xytext=(-3.5, 0),
                    arrowprops=dict(arrowstyle='->', color=CB, lw=2.0,
                                   mutation_scale=16), zorder=9)
        ax.text((X_LEFT+0)/2, 1.2, 'คลื่นหน้าตรง\nเคลื่อนที่เข้ามา',
                color=CB, fontsize=8.5, ha='center', va='bottom',
                fontweight='600', zorder=9)

        # barrier
        bw = 0.24
        for y0, y1 in [(-Y_MAX, -(d/2 + gap)),
                       (-(d/2 - gap), (d/2 - gap)),
                       ((d/2 + gap), Y_MAX)]:
            ax.add_patch(Rectangle((-bw, y0), 2*bw, y1-y0,
                                   fc='#475569', ec='none', alpha=0.90, zorder=6))
        ax.text(-bw-0.2, -Y_MAX+0.15, 'แผ่นกั้น', color='#475569',
                fontsize=7.5, ha='right', va='bottom', fontweight='600', zorder=9)

        # d annotation
        ax.annotate('', xy=(-1.1, s1[1]), xytext=(-1.1, s2[1]),
                    arrowprops=dict(arrowstyle='<->', color=CGR, lw=1.4))
        ax.text(-1.45, 0, 'd', fontsize=11, color=CDK,
                ha='center', va='center', fontweight='bold')

        # opening markers
        for src, col, lbl in [(s1, CB, 'O₁'), (s2, CR, 'O₂')]:
            ax.plot(*src, 'D', color=col, ms=9, zorder=10,
                    markeredgecolor='white', markeredgewidth=1.4)
            ax.text(0.5, src[1], lbl, color=col,
                    fontsize=8.5, va='center', fontweight='700', zorder=10)

        # circular wavefronts (right side)
        for src, col in [(s1, CB), (s2, CR)]:
            for n in range(1, 15):
                r     = n * lam
                alpha = max(0.05, 0.60 - n*0.04)
                lw_c  = 1.4 if n % 2 != 0 else 0.7
                ax.add_patch(plt.Circle(src, r, color=col, fill=False,
                                        lw=lw_c, alpha=alpha, zorder=2))

        # mask left side
        ax.add_patch(Rectangle((X_LEFT-0.4, -Y_MAX-0.5),
                                abs(X_LEFT)+0.4+bw, 2*(Y_MAX+0.5),
                                fc='#f0f7ff', ec='none', zorder=3))

        # antinodal lines
        R_MAX = 11.0
        for n in range(-n_max, n_max + 1):
            v = n * lam / d
            if abs(v) > 1: continue
            th  = np.arcsin(v)
            xe  = R_MAX * np.cos(th)
            ye  = R_MAX * np.sin(th)
            lw_a = 2.0 if n == 0 else 1.4
            ax.plot([0, xe], [0, ye], color=CG, lw=lw_a, alpha=0.9, zorder=4)
            lbl = 'A₀ (กลาง)' if n == 0 else f'A{abs(n)}'
            ha  = 'left' if xe > 0 else 'right'
            va  = ('bottom' if ye > 0.4 else 'top' if ye < -0.4 else 'center')
            ax.text(xe*1.04, ye*1.04, lbl, color=CG, fontsize=8,
                    fontweight='bold', ha=ha, va=va, zorder=5)

        # nodal lines
        for n in range(1, n_max + 1):
            for sign in [1, -1]:
                v = (n - 0.5) * lam / d
                if abs(v) > 1: continue
                th  = np.arcsin(sign * v)
                xe  = R_MAX * np.cos(th)
                ye  = R_MAX * np.sin(th)
                ax.plot([0, xe], [0, ye], color=CRED,
                        lw=1.0, ls='--', alpha=0.70, zorder=4)
                ha = 'left' if xe > 0 else 'right'
                va = 'bottom' if ye > 0.4 else ('top' if ye < -0.4 else 'center')
                ax.text(xe*1.04, ye*1.04, f'N{n}', color=CRED,
                        fontsize=7.5, ha=ha, va=va, zorder=5)

        # θ angle
        th1 = np.arcsin(lam / d)
        ax.add_patch(Arc((0,0), 2.5, 2.5, angle=0,
                         theta1=0, theta2=np.degrees(th1),
                         color='#7c3aed', lw=1.8, zorder=7))
        ax.text(1.5, 0.32, 'θ₁', fontsize=10, color='#7c3aed',
                fontweight='bold', zorder=8)

        # L arrow
        y_arr = -Y_MAX + 0.2
        ax.annotate('', xy=(X_RIGHT-0.4, y_arr), xytext=(0, y_arr),
                    arrowprops=dict(arrowstyle='<->', color=CGR, lw=1.2))
        ax.text((X_RIGHT-0.4)/2, y_arr-0.42,
                'L (ระยะไปยังจุดวัด)',
                ha='center', fontsize=8, color=CGR, zorder=8)

        ax.set_title('มุมมองจากด้านบน: คลื่นผ่านช่องสองช่องในแผ่นกั้น',
                     fontsize=9.5, color=CDK, pad=6, fontweight='700')
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
             'ขั้น 1',
             r'$\Delta r = |r_1 - r_2|$'),
            (3.80, '#065f46', '#f0fdf4',
             'ขั้น 2',
             r'$k = \Delta r \;/\; \lambda$'),
            (6.42, '#78350f', '#fefce8',
             'ขั้น 3',
             'k เป็นเลขจำนวนเต็ม\nหรือ ครึ่งจำนวนเต็ม?'),
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
            (2.28,  CG,   '#dcfce7', 'k = 0,1,2,…\n→ ปฏิบัพ'),
            (0.55,  CRED, '#fee2e2', 'k = ½,1½,…\n→ บัพ'),
        ]:
            ax.add_patch(FancyBboxPatch((7.56, yc-0.38), 1.85, 0.76,
                                        boxstyle='round,pad=0.06',
                                        fc=fc2, ec=col, lw=1.9))
            ax.text(8.44, yc, txt, ha='center', va='center',
                    fontsize=8.5, color=col, fontweight='700')

        ax.set_title('วิธีแก้โจทย์ 3 ขั้นตอน (ใช้ได้กับทุกโจทย์)',
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
  <h1>🌊 การแทรกสอดของคลื่นน้ำ</h1>
  <p>สรุปครบ ตั้งแต่หลักการพื้นฐานจนถึงการนับแนวและแก้โจทย์<br>
     เนื้อหาวิชาฟิสิกส์ ม.5 บทคลื่นกล</p>
  <div class="hero-meta">
    <span class="hero-tag">ฟิสิกส์ ม.5</span>
    <span class="hero-tag">คลื่นกล</span>
    <span class="hero-tag">การแทรกสอด</span>
  </div>
</div>
""", unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════════════
    # 01  แหล่งกำเนิดอาพันธ์คืออะไร?
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown('<p class="sh"><span class="pill">01</span>'
                'แหล่งกำเนิดอาพันธ์ (Coherent Sources)</p>',
                unsafe_allow_html=True)

    c1, c2 = st.columns([1, 1], gap="large")
    with c1:
        st.markdown("""
<div class="card cb">
<h4>🔵 แหล่งกำเนิดอาพันธ์คืออะไร?</h4>
<p>แหล่งกำเนิดคลื่นสองแหล่งที่มี:</p>
<ul>
<li><strong>ความถี่เท่ากัน</strong> ทั้งคู่</li>
<li><strong>ผลต่างเฟสคงที่</strong> ตลอดเวลา (ไม่เปลี่ยนแปลง)</li>
</ul>
<p>ในถาดคลื่น: ใช้แท่งสั่นสองแท่งติดกับมอเตอร์ตัวเดียวกัน</p>
</div>
""", unsafe_allow_html=True)
    with c2:
        st.markdown("""
<div class="card cs">
<h4>📋 สองกรณีหลัก</h4>
<ul>
<li><strong>เฟสตรงกัน</strong> (In-phase) — ทั้งคู่ออกสันคลื่นพร้อมกัน (Δφ = 0)</li>
<li><strong>เฟสตรงข้าม</strong> (Anti-phase) — หนึ่งออกสันขณะอีกออกท้อง (Δφ = π)</li>
</ul>
<p>โจทย์ส่วนใหญ่จะบอกว่า "เฟสตรงกัน" ถ้าไม่บอกให้ถือว่าเฟสตรงกัน</p>
</div>
""", unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════════════
    # 02  หลักการซ้อนทับ
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown('<hr class="div"><p class="sh"><span class="pill">02</span>'
                'หลักการซ้อนทับ — ทำไมจึงเกิดการแทรกสอด?</p>',
                unsafe_allow_html=True)

    _show("superposition",
          "แถวบน: สันคลื่น + สันคลื่น → แอมพลิจูด 2A (เสริมกัน)  |  "
          "แถวล่าง: สันคลื่น + ท้องคลื่น → ผลรวม = 0 (หักล้างกัน)")

    c1, c2 = st.columns([1, 1], gap="large")
    with c1:
        st.markdown("""
<div class="card cg">
<h4>✅ คลื่นเสริมกัน (Constructive)</h4>
<ul>
<li>สันคลื่นพบสันคลื่น หรือ ท้องพบท้อง</li>
<li>คลื่นสองขบวนมาถึงจุดเดียวกัน <strong>เฟสตรงกัน</strong></li>
<li>ผิวน้ำสั่นด้วยแอมพลิจูด = <strong>2A</strong> (สูงสุด)</li>
<li>จุดนี้เรียกว่า <strong>"ปฏิบัพ" (Antinode)</strong></li>
</ul>
</div>
""", unsafe_allow_html=True)
    with c2:
        st.markdown("""
<div class="card cr">
<h4>❌ คลื่นหักล้างกัน (Destructive)</h4>
<ul>
<li>สันคลื่นพบท้องคลื่น</li>
<li>คลื่นสองขบวนมาถึงจุดเดียวกัน <strong>เฟสตรงข้าม</strong></li>
<li>ผิวน้ำไม่สั่น แอมพลิจูด = <strong>0</strong></li>
<li>จุดนี้เรียกว่า <strong>"บัพ" (Node)</strong></li>
</ul>
</div>
""", unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════════════
    # 03  ผลต่างเส้นทาง Δr
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown('<hr class="div"><p class="sh"><span class="pill">03</span>'
                'ผลต่างเส้นทาง Δr — หัวใจสำคัญของการแทรกสอด</p>',
                unsafe_allow_html=True)

    c1, c2 = st.columns([1.3, 1], gap="large")
    with c1:
        _show("path_diff",
              "วงกลม = หน้าคลื่น (สันคลื่น)  |  เส้นโค้ง = คลื่นเดินทางตามเส้นทาง r₁ และ r₂ ไปยังจุด P")
    with c2:
        st.markdown("""
<div class="card cb">
<h4>📐 นิยาม</h4>
<p>ผลต่างเส้นทาง คือ <strong>ความต่างของระยะทาง</strong> ที่คลื่นแต่ละขบวนเดินทางมาถึงจุด P</p>
</div>
""", unsafe_allow_html=True)
        st.latex(r"\Delta r \;=\; |r_1 - r_2|")

        st.markdown("""
<div class="card cb" style="margin-top:12px">
<h4>🔑 ทำไม Δr จึงสำคัญ?</h4>
<ul>
<li>ถ้า Δr = nλ → คลื่นเดินทาง <em>ต่างกัน n รอบพอดี</em> → มาถึง <strong>เฟสตรงกัน</strong> → <span class="tg">ปฏิบัพ</span></li>
<li>ถ้า Δr = (n−½)λ → ต่างกันครึ่งรอบ → มาถึง <strong>เฟสตรงข้าม</strong> → <span class="tr">บัพ</span></li>
</ul>
</div>
""", unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════════════
    # 04  เงื่อนไข + รูปแบบการแทรกสอด
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown('<hr class="div"><p class="sh"><span class="pill">04</span>'
                'เงื่อนไขปฏิบัพและบัพ (แหล่งกำเนิดเฟสตรงกัน)</p>',
                unsafe_allow_html=True)

    _show("conditions")

    c1, c2 = st.columns(2, gap="large")
    with c1:
        st.markdown('<div class="card cg"><h4>✅ ปฏิบัพ (Antinode)</h4></div>',
                    unsafe_allow_html=True)
        st.latex(r"\Delta r = n\lambda \quad n = 0,\,1,\,2,\,3,\,\ldots")
        st.markdown("แอมพลิจูดผลรวม = **2A** (ผิวน้ำสั่นสูงสุด)")
    with c2:
        st.markdown('<div class="card cr"><h4>❌ บัพ (Node)</h4></div>',
                    unsafe_allow_html=True)
        st.latex(r"\Delta r = \left(n - \tfrac{1}{2}\right)\lambda \quad n = 1,\,2,\,3,\,\ldots")
        st.markdown("แอมพลิจูดผลรวม = **0** (ผิวน้ำนิ่ง)")

    # ══════════════════════════════════════════════════════════════════════════
    # 05  แบบแผนการแทรกสอด — มุมมองจากด้านบน
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown('<hr class="div"><p class="sh"><span class="pill">05</span>'
                'แบบแผนการแทรกสอด — มุมมองจากด้านบน</p>',
                unsafe_allow_html=True)

    c1, c2 = st.columns([1, 1], gap="large")
    with c1:
        _show("two_sources",
              "วงแข็ง = หน้าคลื่น  |  เส้นสีเขียว = แนวปฏิบัพ  |  เส้นประแดง = แนวบัพ")
    with c2:
        _show("pattern",
              "d = 10 cm, λ = 2.5 cm  |  ปฏิบัพ 9 แนว,  บัพ 8 แนว")

    st.markdown("""
<div class="card cb">
<h4>🗺️ วิธีอ่านแผนภาพวงกลม</h4>
<ul>
<li>วงสีฟ้า = สันคลื่นจาก S₁ &nbsp;|&nbsp; วงสีแดง = สันคลื่นจาก S₂</li>
<li>วงฟ้าพบวงฟ้า → <strong class="tg">สันพบสัน → ปฏิบัพ</strong></li>
<li>วงฟ้าพบวงแดง → <strong class="tr">สันพบท้อง → บัพ</strong></li>
<li>เชื่อมจุดปฏิบัพทุกจุดจะได้ <strong>แนวปฏิบัพ (เส้นสีเขียว)</strong></li>
<li>เชื่อมจุดบัพทุกจุดจะได้ <strong>แนวบัพ (เส้นประแดง)</strong></li>
</ul>
</div>
""", unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════════════
    # 06  การนับแนวปฏิบัพและบัพ
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown('<hr class="div"><p class="sh"><span class="pill">06</span>'
                'การนับแนวปฏิบัพและบัพ</p>',
                unsafe_allow_html=True)

    _show("ruler",
          "◆ ปฏิบัพ อยู่เหนือแกน  |  ▼ บัพ อยู่ใต้แกน  (d = 10 cm, λ = 2 cm)")

    c1, c2 = st.columns([1, 1.1], gap="large")
    with c1:
        st.markdown('<div class="card cb"><h4>หา n<sub>max</sub></h4></div>',
                    unsafe_allow_html=True)
        st.latex(r"n_{\max} = \left\lfloor \frac{d}{\lambda} \right\rfloor"
                 r"\quad\text{(เอาแค่ส่วนเต็ม)}")
        st.markdown("""
<div class="card cg" style="margin-top:10px">
<h4>นับจำนวนแนว</h4>
<ul>
<li>แนวปฏิบัพทั้งหมด = <strong>2n<sub>max</sub> + 1</strong></li>
<li>แนวบัพทั้งหมด = <strong>2n<sub>max</sub></strong></li>
</ul>
</div>
""", unsafe_allow_html=True)
    with c2:
        st.markdown("""
<table class="rt">
<thead><tr>
  <th>นับที่ไหน</th>
  <th class="tg">ปฏิบัพ</th>
  <th class="tr">บัพ</th>
</tr></thead>
<tbody>
<tr>
  <td>บนเส้น S₁S₂ ทั้งหมด</td>
  <td class="tg">2n₀ + 1</td>
  <td class="tr">2n₀</td>
</tr>
<tr>
  <td>ระหว่าง S₁ กับ S₂</td>
  <td class="tg">2n₀ − 1</td>
  <td class="tr">2(n₀ − 1)</td>
</tr>
</tbody>
</table>
<p style="font-size:.75rem;color:#64748b;margin-top:6px">
* ใช้ได้เมื่อ d หารด้วย λ ลงตัว
</p>
""", unsafe_allow_html=True)

    st.markdown("""
<div class="card cy">
<h4>📝 ตัวอย่าง</h4>
<p><strong>กำหนด:</strong> d = 12 cm,  λ = 4 cm  →  n₀ = 12/4 = <strong>3</strong></p>
<ul>
<li>ปฏิบัพทั้งหมด = 2×3 + 1 = <span class="tg">7 แนว</span> &nbsp;(A₀, A₁, A₂, A₃ ทั้งสองข้าง)</li>
<li>บัพทั้งหมด = 2×3 = <span class="tr">6 แนว</span> &nbsp;(N₁, N₂, N₃ ทั้งสองข้าง)</li>
<li>ระหว่าง S₁S₂: ปฏิบัพ = 2×3 − 1 = <span class="tg">5 แนว</span>,  บัพ = 2×(3−1) = <span class="tr">4 แนว</span></li>
</ul>
</div>
""", unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════════════
    # 07  วิธีแก้โจทย์ 3 ขั้นตอน
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown('<hr class="div"><p class="sh"><span class="pill">07</span>'
                'วิธีแก้โจทย์ 3 ขั้นตอน</p>',
                unsafe_allow_html=True)

    _show("flowchart")

    st.markdown("""
<div class="keytip">
💡 <strong>กฎเหล็ก:</strong> &nbsp; คำนวณ k = Δr ÷ λ &nbsp;—&nbsp;
ถ้า k เป็น <strong>จำนวนเต็ม</strong> → ปฏิบัพ &nbsp;|&nbsp;
ถ้า k ลงท้ายด้วย <strong>.5</strong> → บัพ
</div>
""", unsafe_allow_html=True)

    c1, c2 = st.columns(2, gap="large")
    with c1:
        st.markdown("""
<div class="card cy">
<h4>ตัวอย่างที่ 1</h4>
<p>d = 10 cm, λ = 2.5 cm  |  จุด A: r₁ = 12, r₂ = 17 cm</p>
<ul>
<li>Δr = |12 − 17| = <strong>5 cm</strong></li>
<li>k = 5 ÷ 2.5 = <strong>2.0</strong> ← จำนวนเต็ม</li>
<li>→ <span class="tg">ปฏิบัพ A₂</span></li>
</ul>
</div>
""", unsafe_allow_html=True)
    with c2:
        st.markdown("""
<div class="card cy">
<h4>ตัวอย่างที่ 2</h4>
<p>λ = 2.5 cm  |  จุด B: r₁ = 14.5, r₂ = 15.75 cm</p>
<ul>
<li>Δr = |14.5 − 15.75| = <strong>1.25 cm</strong></li>
<li>k = 1.25 ÷ 2.5 = <strong>0.5</strong> ← ลงท้าย .5</li>
<li>→ <span class="tr">บัพ N₁</span></li>
</ul>
</div>
""", unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════════════
    # 08  แหล่งกำเนิดเฟสตรงข้าม
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown('<hr class="div"><p class="sh"><span class="pill">08</span>'
                'กรณีพิเศษ: แหล่งกำเนิดเฟสตรงข้าม (Δφ = 180°)</p>',
                unsafe_allow_html=True)

    _show("antiphase",
          "ซ้าย: เฟสตรงกัน → Δr=0 คือ ปฏิบัพ  |  ขวา: เฟสตรงข้าม → Δr=0 คือ บัพ")

    c1, c2 = st.columns(2, gap="large")
    with c1:
        st.markdown("""
<div class="card cr">
<h4>⚠️ เงื่อนไขสลับกันทั้งหมด!</h4>
<p>แหล่งกำเนิดเฟสตรงข้ามมีเฟสต่างกันอยู่แล้ว 180° จึงทำให้เงื่อนไขสลับ</p>
</div>
""", unsafe_allow_html=True)
        st.markdown("""
<table class="rt">
<thead><tr><th>Δr</th><th>เฟสตรงกัน</th><th>เฟสตรงข้าม</th></tr></thead>
<tbody>
<tr><td>0, λ, 2λ …</td>
    <td class="tg">ปฏิบัพ</td><td class="tr">บัพ</td></tr>
<tr><td>λ/2, 3λ/2 …</td>
    <td class="tr">บัพ</td><td class="tg">ปฏิบัพ</td></tr>
</tbody>
</table>
""", unsafe_allow_html=True)
    with c2:
        st.markdown("""
<div class="card cy">
<h4>💡 เข้าใจง่ายๆ</h4>
<p>แหล่งเฟสตรงข้ามมีเฟสต่างกัน 180° อยู่แล้ว:</p>
<ul>
<li>Δr = 0 → บวกอีก 0° → รวม 180° → <span class="tr">บัพ</span></li>
<li>Δr = λ/2 → บวกอีก 180° → รวม 360° = 0° → <span class="tg">ปฏิบัพ</span></li>
</ul>
<p><strong>สรุป:</strong> เฟสตรงข้าม = เหมือนเฟสตรงกัน แต่สลับบัพกับปฏิบัพ</p>
</div>
""", unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════════════
    # 09  คลื่นผ่านช่องสองช่อง
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown('<hr class="div"><p class="sh"><span class="pill">09</span>'
                'คลื่นผ่านช่องสองช่องในแผ่นกั้น</p>',
                unsafe_allow_html=True)

    _show("barrier",
          "คลื่นหน้าตรงเลี้ยวเบนผ่านช่องทั้งสอง แล้วแทรกสอดกันในด้านขวา  |  θ₁ = มุมไปยังปฏิบัพลำดับที่ 1")

    c1, c2 = st.columns(2, gap="large")
    with c1:
        st.markdown('<div class="card cb"><h4>📐 สูตรสำคัญ</h4></div>',
                    unsafe_allow_html=True)
        st.markdown("**มุมปฏิบัพลำดับ n:**")
        st.latex(r"\sin\theta_n = \frac{n\lambda}{d}")
        st.markdown("**ระยะจากแนวกลาง (มุมน้อย):**")
        st.latex(r"x_n = \frac{n\lambda L}{d}")
        st.markdown("**ระยะห่างระหว่างปฏิบัพที่ติดกัน:**")
        st.latex(r"\Delta x = \frac{\lambda L}{d}")
        st.markdown("**มุมบัพลำดับ n:**")
        st.latex(r"\sin\theta_n = \frac{(n-\tfrac{1}{2})\lambda}{d}")
    with c2:
        st.markdown("""
<div class="card cg">
<h4>📝 ตัวอย่าง</h4>
<p>d = 4 cm, λ = 2 cm, L = 30 cm</p>
<ul>
<li>x₁ = (1 × 2 × 30) / 4 = <strong>15 cm</strong></li>
<li>x₂ = (2 × 2 × 30) / 4 = <strong>30 cm</strong></li>
<li>Δx = 2 × 30 / 4 = <strong>15 cm</strong></li>
</ul>
</div>
<div class="card cp" style="margin-top:10px">
<h4>⚠️ ข้อสังเกต</h4>
<ul>
<li>ช่องสองช่อง = แหล่งกำเนิดอาพันธ์สองแหล่ง เฟสตรงกัน</li>
<li>ยิ่ง d ใหญ่ ยิ่ง x น้อย (แนวปฏิบัพชิดกัน)</li>
<li>ยิ่ง λ ยาว ยิ่ง x มาก (แนวปฏิบัพห่างกัน)</li>
</ul>
</div>
""", unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════════════
    # REF  ตารางสรุปสูตร
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown('<hr class="div"><p class="sh"><span class="pill">REF</span>'
                'ตารางสรุปสูตรทั้งหมด</p>',
                unsafe_allow_html=True)

    st.markdown("""
<table class="rt">
<thead><tr>
  <th>ปริมาณ</th>
  <th class="tg">ปฏิบัพ (คลื่นเสริมกัน)</th>
  <th class="tr">บัพ (คลื่นหักล้างกัน)</th>
</tr></thead>
<tbody>
<tr>
  <td><strong>Δr — แหล่งเฟสตรงกัน</strong></td>
  <td class="tg">0, λ, 2λ, 3λ …</td>
  <td class="tr">λ/2, 3λ/2, 5λ/2 …</td>
</tr>
<tr>
  <td><strong>Δr — แหล่งเฟสตรงข้าม</strong></td>
  <td class="tg">λ/2, 3λ/2, 5λ/2 …</td>
  <td class="tr">0, λ, 2λ, 3λ …</td>
</tr>
<tr>
  <td><strong>จำนวนแนว (เฟสตรงกัน)</strong></td>
  <td class="tg">2n<sub>max</sub> + 1</td>
  <td class="tr">2n<sub>max</sub></td>
</tr>
<tr>
  <td><strong>มุมแนวลำดับ n</strong></td>
  <td class="tg">sin θ = nλ/d</td>
  <td class="tr">sin θ = (n−½)λ/d</td>
</tr>
<tr>
  <td><strong>ระยะจากแนวกลาง (L ห่าง)</strong></td>
  <td class="tg">x = nλL/d</td>
  <td class="tr">x = (n−½)λL/d</td>
</tr>
<tr>
  <td><strong>แอมพลิจูดผลรวม</strong></td>
  <td class="tg">2A</td>
  <td class="tr">0</td>
</tr>
</tbody>
</table>
""", unsafe_allow_html=True)

    st.markdown("""
<div class="keytip" style="margin-top:16px">
💡 <strong>จำไว้:</strong> &nbsp;
k = Δr ÷ λ &nbsp;—&nbsp;
k เป็น <strong>จำนวนเต็ม</strong> → ปฏิบัพ &nbsp;•&nbsp;
k ลงท้าย <strong>.5</strong> → บัพ &nbsp;•&nbsp;
ใช้ได้กับแหล่งกำเนิดเฟสตรงกันเท่านั้น
</div>
""", unsafe_allow_html=True)
