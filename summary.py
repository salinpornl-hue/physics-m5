"""
summary.py — สรุปเรื่อง "การแทรกสอดของคลื่น"
Thai text stays in Streamlit markdown. Matplotlib figures use English only.
"""
import streamlit as st
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# ── Try to use a Thai-compatible font for matplotlib ──────────────────────────
import matplotlib.font_manager as fm

_THAI_CANDIDATES = ['Tahoma', 'Arial Unicode MS', 'Browallia New',
                    'AngsanaUPC', 'Cordia New', 'FreeSans', 'DejaVu Sans']
_available = {f.name for f in fm.fontManager.ttflist}
_thai_font = next((f for f in _THAI_CANDIDATES if f in _available), 'DejaVu Sans')
plt.rcParams['font.family'] = _thai_font
plt.rcParams['axes.unicode_minus'] = False


# ─── CSS ──────────────────────────────────────────────────────────────────────
_CSS = """
<style>
.s-title  { font-size:2.1rem; font-weight:900; color:#1e3a8a;
            text-align:center; margin-bottom:2px; }
.s-sub    { font-size:1rem; color:#64748b; text-align:center; margin-bottom:20px; }
.s-h2     { font-size:1.4rem; font-weight:800; color:#1e3a8a; margin:8px 0 4px 0; }
.box-blue { background:#eff6ff; border-left:5px solid #2563eb;
            border-radius:8px; padding:14px 18px; margin:10px 0; }
.box-blue h4 { margin:0 0 6px 0; color:#1e40af; }
.box-green{ background:#f0fdf4; border:1px solid #86efac;
            border-radius:8px; padding:14px 18px; margin:10px 0; }
.box-warn { background:#fffbeb; border-left:5px solid #f59e0b;
            border-radius:8px; padding:12px 16px; margin:10px 0; }
.box-red  { background:#fef2f2; border-left:5px solid #dc2626;
            border-radius:8px; padding:14px 18px; margin:10px 0; }
.box-red h4 { margin:0 0 6px 0; color:#991b1b; }
</style>
"""


# ─── Figure helpers ───────────────────────────────────────────────────────────

def _show(func, caption=""):
    try:
        fig = func()
        st.pyplot(fig, use_container_width=True)
        if caption:
            st.caption(caption)
        plt.close(fig)
    except Exception as e:
        st.warning(f"ไม่สามารถแสดงรูปได้: {e}")


# ─── Figures (English labels only) ───────────────────────────────────────────

def _fig_ripple():
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.set_xlim(-8, 8); ax.set_ylim(-5, 5)
    ax.set_aspect('equal'); ax.axis('off')
    ax.set_facecolor('#f0f9ff')
    fig.patch.set_facecolor('#f0f9ff')

    lam = 2.0
    sources = [(-2.5, 0.0, '#2563eb', 'S₁'), (2.5, 0.0, '#dc2626', 'S₂')]
    for sx, sy, col, lbl in sources:
        for r in np.arange(lam/2, 9, lam/2):
            alpha = max(0.08, 0.7 - r/9)
            c = plt.Circle((sx, sy), r, color=col, fill=False, lw=1.2, alpha=alpha)
            ax.add_patch(c)
        ax.plot(sx, sy, 'o', color=col, ms=10, zorder=5)
        ax.text(sx, sy - 0.7, lbl, ha='center', fontsize=14,
                color=col, fontweight='bold')

    ax.text(0, 4.3, 'Two wave sources radiating outward',
            ha='center', fontsize=11, color='#374151',
            bbox=dict(boxstyle='round,pad=0.3', fc='white', ec='#cbd5e1', lw=1))
    fig.tight_layout()
    return fig


def _fig_constructive():
    fig, axes = plt.subplots(3, 1, figsize=(9, 5), sharex=True)
    fig.patch.set_facecolor('#f0fdf4')
    x = np.linspace(0, 4*np.pi, 500)

    data = [
        (np.sin(x),       '#2563eb', 'Wave 1'),
        (np.sin(x),       '#dc2626', 'Wave 2  (same phase)'),
        (2*np.sin(x),     '#16a34a', 'Result  =  Wave 1 + Wave 2'),
    ]
    for ax, (y, col, lbl) in zip(axes, data):
        ax.fill_between(x, y, alpha=0.18, color=col)
        ax.plot(x, y, color=col, lw=2.2)
        ax.axhline(0, color='k', lw=0.6)
        ax.set_ylabel(lbl, fontsize=9, color=col, fontweight='bold')
        ax.set_ylim(-2.5, 2.5); ax.set_yticks([])
        ax.spines[['top','right','bottom','left']].set_visible(False)

    axes[2].annotate('Amplitude = 2A  (maximum!)',
                     xy=(np.pi/2, 2), xytext=(np.pi/2 + 2.5, 2.3),
                     arrowprops=dict(arrowstyle='->', color='#16a34a', lw=1.8),
                     fontsize=10, color='#16a34a', fontweight='bold')
    axes[2].set_xlabel('Position  x', fontsize=10)
    fig.suptitle('CONSTRUCTIVE Interference  —  crests meet crests',
                 fontsize=12, fontweight='bold', color='#16a34a', y=1.01)
    fig.tight_layout()
    return fig


def _fig_destructive():
    fig, axes = plt.subplots(3, 1, figsize=(9, 5), sharex=True)
    fig.patch.set_facecolor('#fef2f2')
    x = np.linspace(0, 4*np.pi, 500)

    data = [
        (np.sin(x),        '#2563eb', 'Wave 1'),
        (-np.sin(x),       '#dc2626', 'Wave 2  (opposite phase)'),
        (np.zeros_like(x), '#6b7280', 'Result  =  0  (cancelled out!)'),
    ]
    for ax, (y, col, lbl) in zip(axes, data):
        ax.fill_between(x, y, alpha=0.18, color=col)
        ax.plot(x, y, color=col, lw=2.2)
        ax.axhline(0, color='k', lw=0.6)
        ax.set_ylabel(lbl, fontsize=9, color=col, fontweight='bold')
        ax.set_ylim(-2.5, 2.5); ax.set_yticks([])
        ax.spines[['top','right','bottom','left']].set_visible(False)

    axes[2].set_xlabel('Position  x', fontsize=10)
    fig.suptitle('DESTRUCTIVE Interference  —  crests meet troughs',
                 fontsize=12, fontweight='bold', color='#dc2626', y=1.01)
    fig.tight_layout()
    return fig


def _fig_path_diff():
    fig, ax = plt.subplots(figsize=(7, 4.8))
    ax.set_xlim(-1, 9.5); ax.set_ylim(-0.5, 5.5)
    ax.set_aspect('equal'); ax.axis('off')
    fig.patch.set_facecolor('#fefce8')
    ax.set_facecolor('#fefce8')

    s1 = np.array([0.0, 4.2])
    s2 = np.array([0.0, 0.5])
    P  = np.array([7.5, 2.8])

    for src, col, lbl in [(s1,'#2563eb','S₁'), (s2,'#dc2626','S₂')]:
        ax.plot(*src, 'o', color=col, ms=13, zorder=5)
        ax.text(src[0]-0.35, src[1], lbl, ha='right', fontsize=14,
                color=col, fontweight='bold')

    ax.plot(*P, '^', color='#16a34a', ms=13, zorder=5)
    ax.text(P[0]+0.2, P[1]+0.15, 'P', fontsize=14,
            color='#16a34a', fontweight='bold')

    r1 = np.linalg.norm(P - s1)
    r2 = np.linalg.norm(P - s2)
    ax.plot([s1[0], P[0]], [s1[1], P[1]], '#2563eb', lw=2, ls='--', alpha=0.8)
    ax.plot([s2[0], P[0]], [s2[1], P[1]], '#dc2626', lw=2, ls='--', alpha=0.8)

    mid1 = (s1 + P) / 2
    mid2 = (s2 + P) / 2
    ang1 = np.degrees(np.arctan2(P[1]-s1[1], P[0]-s1[0]))
    ang2 = np.degrees(np.arctan2(P[1]-s2[1], P[0]-s2[0]))
    ax.text(mid1[0]-0.2, mid1[1]+0.25, f'r₁ = {r1:.1f}',
            fontsize=10, color='#2563eb', rotation=ang1, ha='center')
    ax.text(mid2[0]+0.2, mid2[1]-0.35, f'r₂ = {r2:.1f}',
            fontsize=10, color='#dc2626', rotation=ang2, ha='center')

    dr = abs(r2 - r1)
    ax.text(4.5, 5.2,
            f'Δr  =  |r₂ − r₁|  =  {dr:.1f}  cm',
            fontsize=12, ha='center', fontweight='bold', color='#92400e',
            bbox=dict(boxstyle='round,pad=0.4', fc='#fef3c7', ec='#f59e0b', lw=2))

    ax.text(4.5, -0.3, 'PATH DIFFERENCE  determines  constructive or destructive',
            ha='center', fontsize=9, color='#6b7280', style='italic')
    fig.tight_layout()
    return fig


def _fig_formula_summary():
    fig, axes = plt.subplots(1, 2, figsize=(10, 3.5))
    fig.patch.set_facecolor('#f8fafc')

    configs = [
        ('#16a34a', '#dcfce7', 'CONSTRUCTIVE (Antinode)',
         [r'$\Delta r = n\lambda$',
          r'$n = 0,\,1,\,2,\,3,\,\ldots$',
          '',
          'Amplitude = 2A  (MAX)'],
        ),
        ('#dc2626', '#fee2e2', 'DESTRUCTIVE (Node)',
         [r'$\Delta r = \left(n-\tfrac{1}{2}\right)\lambda$',
          r'$n = 1,\,2,\,3,\,\ldots$',
          '',
          'Amplitude = 0  (MIN)'],
        ),
    ]

    for ax, (col, fc, title, lines) in zip(axes, configs):
        ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis('off')
        ax.set_facecolor(fc)
        rect = mpatches.FancyBboxPatch((0.02, 0.02), 0.96, 0.96,
                                       boxstyle='round,pad=0.02',
                                       fc=fc, ec=col, lw=2.5,
                                       transform=ax.transAxes, clip_on=False)
        ax.add_patch(rect)
        ax.text(0.5, 0.90, title, transform=ax.transAxes,
                ha='center', va='top', fontsize=11.5, fontweight='bold', color=col)
        for k, line in enumerate(lines):
            ax.text(0.5, 0.72 - k*0.15, line, transform=ax.transAxes,
                    ha='center', va='top', fontsize=11)

    fig.suptitle('Interference Conditions  (in-phase sources)',
                 fontsize=12, fontweight='bold', y=1.02)
    fig.tight_layout()
    return fig


def _fig_pattern():
    fig, ax = plt.subplots(figsize=(9, 5.5))
    fig.patch.set_facecolor('#f8fafc')
    d, lam = 10.0, 2.5
    n_max = int(d / lam)
    s1, s2 = np.array([0.0,  d/2]), np.array([0.0, -d/2])

    for src, col, lbl in [(s1,'#2563eb','S₁'),(s2,'#dc2626','S₂')]:
        ax.plot(*src, 'o', color=col, ms=10, zorder=5)
        ax.text(src[0]-0.4, src[1], lbl, ha='right', fontsize=11,
                color=col, fontweight='bold')

    r_max = 28
    for n in range(-n_max, n_max+1):
        val = n * lam / d
        if abs(val) <= 1:
            th = np.arcsin(val)
            ax.plot([0, r_max*np.cos(th)], [0, r_max*np.sin(th)],
                    '#16a34a', lw=2.2, alpha=0.85, zorder=3)
            lbl = f'A{abs(n)}' if n != 0 else 'A₀'
            ax.text(r_max*np.cos(th)*1.05, r_max*np.sin(th)*1.05,
                    lbl, fontsize=8.5, color='#16a34a',
                    ha='center', fontweight='bold')

    for n in range(1, n_max+1):
        for sign in [1, -1]:
            val = (n - 0.5) * lam / d
            if abs(val) <= 1:
                th = np.arcsin(sign * val)
                ax.plot([0, r_max*np.cos(th)], [0, r_max*np.sin(th)],
                        '#dc2626', lw=1.3, ls='--', alpha=0.7, zorder=2)
                ax.text(r_max*np.cos(th)*1.05, r_max*np.sin(th)*1.05,
                        f'N{n}', fontsize=8, color='#dc2626', ha='center')

    anti_p = mpatches.Patch(color='#16a34a', label='Antinodal lines (constructive)')
    node_p = mpatches.Patch(color='#dc2626', label='Nodal lines (destructive)',
                             fill=False, linestyle='--', edgecolor='#dc2626')
    ax.legend(handles=[anti_p, node_p], loc='lower right', fontsize=9.5)
    ax.set_xlim(-3, 32); ax.set_ylim(-12.5, 12.5)
    ax.set_xlabel('x  (cm)', fontsize=10)
    ax.set_title(f'd = {int(d)} cm,  λ = {lam} cm\n'
                 f'Antinodal lines = {2*n_max+1},  Nodal lines = {2*n_max}',
                 fontsize=10)
    ax.axhline(0, color='gray', lw=0.5, ls=':')
    ax.set_facecolor('#f8fafc')
    fig.tight_layout()
    return fig


def _fig_steps():
    """3-step method diagram."""
    fig, ax = plt.subplots(figsize=(9, 2.8))
    ax.axis('off')
    fig.patch.set_facecolor('#fffbeb')
    ax.set_facecolor('#fffbeb')

    steps = [
        ('Step 1', r'$\Delta r = |r_1 - r_2|$', '#6366f1'),
        ('Step 2', r'$k = \Delta r \,/\, \lambda$',  '#0891b2'),
        ('Step 3', 'Check k', '#374151'),
    ]
    outcomes = [
        ('k = integer', 'Antinode\n(constructive)', '#16a34a', '#dcfce7'),
        ('k ends in .5', 'Node\n(destructive)',    '#dc2626', '#fee2e2'),
    ]

    for i, (title, formula, col) in enumerate(steps):
        x = 0.12 + i * 0.27
        rect = mpatches.FancyBboxPatch((x-0.1, 0.08), 0.2, 0.84,
                                       boxstyle='round,pad=0.02', fc='white',
                                       ec=col, lw=2.2,
                                       transform=ax.transAxes, clip_on=False)
        ax.add_patch(rect)
        ax.text(x, 0.85, title, transform=ax.transAxes,
                ha='center', va='top', fontsize=10, color=col, fontweight='bold')
        ax.text(x, 0.52, formula, transform=ax.transAxes,
                ha='center', va='top', fontsize=11)
        if i < 2:
            ax.annotate('', xy=(x+0.115, 0.5), xytext=(x+0.085, 0.5),
                        xycoords='axes fraction', textcoords='axes fraction',
                        arrowprops=dict(arrowstyle='->', color='gray', lw=2.2))

    for j, (cond, result, col, fc) in enumerate(outcomes):
        xo = 0.72 + j * 0.15
        rect = mpatches.FancyBboxPatch((xo-0.065, 0.08), 0.13, 0.84,
                                       boxstyle='round,pad=0.02', fc=fc,
                                       ec=col, lw=2,
                                       transform=ax.transAxes, clip_on=False)
        ax.add_patch(rect)
        ax.text(xo, 0.85, cond, transform=ax.transAxes,
                ha='center', va='top', fontsize=9, color=col, fontweight='bold')
        ax.text(xo, 0.55, result, transform=ax.transAxes,
                ha='center', va='top', fontsize=9.5, color=col, fontweight='bold')

    ax.annotate('', xy=(0.655, 0.5), xytext=(0.625, 0.5),
                xycoords='axes fraction', textcoords='axes fraction',
                arrowprops=dict(arrowstyle='->', color='gray', lw=2.2))

    ax.set_title('3-Step Method  —  works for every problem!',
                 fontsize=11, fontweight='bold', pad=6)
    fig.tight_layout()
    return fig


def _fig_antiphase_table():
    fig, ax = plt.subplots(figsize=(8, 2.6))
    ax.axis('off')
    fig.patch.set_facecolor('#f8fafc')

    cols_h = ['Δr', 'In-phase sources', 'Anti-phase sources']
    rows = [
        ['0, λ, 2λ, …', 'Antinode (Constructive)', 'Node (Destructive)'],
        ['λ/2, 3λ/2, …', 'Node (Destructive)',    'Antinode (Constructive)'],
    ]
    cell_colors = [
        ['#f1f5f9', '#dcfce7', '#fee2e2'],
        ['#f1f5f9', '#fee2e2', '#dcfce7'],
    ]
    table = ax.table(
        cellText=rows,
        colLabels=cols_h,
        cellLoc='center',
        loc='center',
        cellColours=cell_colors,
    )
    table.auto_set_font_size(False)
    table.set_fontsize(10.5)
    table.scale(1, 2.4)
    for (r, c), cell in table.get_celld().items():
        cell.set_edgecolor('#cbd5e1')
        if r == 0:
            cell.set_facecolor('#1e3a8a')
            cell.set_text_props(color='white', fontweight='bold')

    ax.set_title('When sources are anti-phase  —  conditions SWAP!',
                 fontsize=11, fontweight='bold', pad=10)
    fig.tight_layout()
    return fig


def _fig_double_slit():
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.set_xlim(-1, 9); ax.set_ylim(-3, 3)
    ax.set_facecolor('#f0f9ff')
    fig.patch.set_facecolor('#f0f9ff')

    # Sources
    for sy, col, lbl in [(0.5,'#2563eb','S₁'),(-0.5,'#dc2626','S₂')]:
        ax.plot(0, sy, 'o', color=col, ms=10, zorder=5)
        ax.text(-0.15, sy, lbl, ha='right', fontsize=12,
                color=col, fontweight='bold')

    # Screen
    ax.plot([7.5, 7.5], [-2.8, 2.8], 'k-', lw=4)

    # Central line
    ax.plot([0, 7.5], [0, 0], 'gray', lw=0.8, ls=':', alpha=0.7)

    # Antinodal lines at angles
    d, lam = 1.0, 0.3
    for n in range(-3, 4):
        val = n * lam / d
        if abs(val) < 1:
            th = np.arcsin(val)
            xe, ye = 7.5, 7.5 * np.tan(th)
            if abs(ye) <= 2.8:
                ax.plot([0, xe], [0, ye], '#16a34a', lw=1.5, alpha=0.8)
                ax.plot(xe, ye, 'g^', ms=7, zorder=5)
                ax.text(xe+0.15, ye, f'n={n}', fontsize=8, color='#16a34a')

    # Labels
    ax.annotate('', xy=(7.5, 2), xytext=(0, 0),
                arrowprops=dict(arrowstyle='->', color='#9333ea', lw=1.8, ls='dashed'))
    ax.text(3.5, 1.2, r'$\theta$', fontsize=14, color='#9333ea')

    ax.text(3.8, -2.6,
            r'$\sin\theta = n\lambda / d$',
            fontsize=12, ha='center', color='#1e3a8a', fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.3', fc='white', ec='#2563eb', lw=1.5))

    ax.set_title('Double-slit interference  —  antinodal directions',
                 fontsize=10, fontweight='bold')
    ax.axis('off')
    fig.tight_layout()
    return fig


def _fig_count_guide():
    """Visual showing how to count on the S1S2 line."""
    fig, ax = plt.subplots(figsize=(9, 2.8))
    ax.set_xlim(-0.5, 10.5); ax.set_ylim(-1.8, 2.0)
    ax.axis('off')
    fig.patch.set_facecolor('#f0fdf4')
    ax.set_facecolor('#f0fdf4')

    # S1 at 0, S2 at 10  (d=10, lam=2)
    ax.plot([0, 10], [0, 0], 'k-', lw=2.5)
    for xp, col, lbl in [(0,'#2563eb','S₁'),(10,'#dc2626','S₂')]:
        ax.plot(xp, 0, 'o', color=col, ms=13, zorder=5)
        ax.text(xp, -0.5, lbl, ha='center', fontsize=11,
                color=col, fontweight='bold')

    # Antinodes (green diamond) — Δr even multiples of λ=2
    for dr, x_list in [
        (0,  [5]),
        (2,  [4, 6]),
        (4,  [3, 7]),
        (6,  [2, 8]),
        (8,  [1, 9]),
        (10, [0, 10]),
    ]:
        for xp in x_list:
            ax.plot(xp, 0, 'D', color='#16a34a', ms=9, zorder=6)
            ax.text(xp, 0.45, f'Δr={dr}', ha='center',
                    fontsize=7.5, color='#16a34a', fontweight='bold')

    # Nodes (red triangle) — Δr odd multiples of λ/2=1
    for dr in [1, 3, 5, 7, 9]:
        for xp in [(10+dr)/2, (10-dr)/2]:
            ax.plot(xp, 0, 'v', color='#dc2626', ms=8, zorder=6)
            ax.text(xp, -1.1, f'Δr={dr}', ha='center',
                    fontsize=7.5, color='#dc2626')

    ax.text(5, 1.7,
            'd = 10 cm,  λ = 2 cm  →  Antinodes (green ◆) = 11,  Nodes (red ▼) = 10',
            ha='center', fontsize=9, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.25', fc='white', ec='#86efac'))
    fig.tight_layout()
    return fig


# ─── Main render ──────────────────────────────────────────────────────────────

def render_summary():
    st.markdown(_CSS, unsafe_allow_html=True)

    st.markdown('<div class="s-title">🌊 การแทรกสอดของคลื่น</div>', unsafe_allow_html=True)
    st.markdown('<div class="s-sub">Wave Interference — อ่านแล้วเข้าใจได้ทันที!</div>',
                unsafe_allow_html=True)

    # ── 1. คืออะไร ──────────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("## 1️⃣ การแทรกสอดคืออะไร?")

    col1, col2 = st.columns([1, 1], gap="large")
    with col1:
        st.markdown("""
<div class="box-blue">
<h4>🔑 ความหมายง่ายๆ</h4>

**การแทรกสอด (Interference)** คือเมื่อ **คลื่น 2 ขบวนมาพบกัน** แล้วรวมกัน

- **ยอดชนยอด** → เสริมกัน 🟢 (แอมพลิจูดสูงขึ้น)
- **ยอดชนราง** → หักล้างกัน 🔴 (แอมพลิจูดลดลง หรือเป็น 0)

> 💡 เหมือนโยนก้อนหิน 2 ก้อนลงสระพร้อมกัน — บางจุดคลื่นสูงมาก บางจุดผิวน้ำนิ่งสนิท!
</div>
""", unsafe_allow_html=True)

    with col2:
        _show(_fig_ripple,
              "คลื่นจาก S₁ (น้ำเงิน) และ S₂ (แดง) แผ่ออกมาพบกัน")

    # ── 2. เสริม vs หักล้าง ──────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("## 2️⃣ เสริมกัน vs หักล้างกัน — ดูคลื่นจริง")

    c1, c2 = st.columns(2, gap="medium")
    with c1:
        _show(_fig_constructive,
              "เฟสตรงกัน → ยอดชนยอด → แอมพลิจูดเป็น 2 เท่า")
    with c2:
        _show(_fig_destructive,
              "เฟสตรงข้าม → ยอดชนราง → ผลรวม = 0")

    st.markdown("""
<div class="box-warn">

⚠️ <strong>จำไว้!</strong> คลื่นสองขบวนผ่านกันแล้วต่างก็เดินทางต่อไปเหมือนเดิม
การแทรกสอดเป็นแค่ผลชั่วคราว <em>ตรงจุดที่พบกัน</em>
</div>
""", unsafe_allow_html=True)

    # ── 3. ผลต่างระยะทาง ────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("## 3️⃣ ผลต่างระยะทาง (Δr) — กุญแจสำคัญ!")

    _show(_fig_path_diff,
          "Δr = ผลต่างระยะทางจากแหล่งกำเนิดสองแหล่งมายังจุด P")

    st.markdown("""
<div class="box-blue">
<h4>📏 ผลต่างระยะทาง (Path Difference)</h4>
</div>
""", unsafe_allow_html=True)

    st.latex(r"\Delta r = |r_1 - r_2|")

    st.markdown("""
- $r_1$ = ระยะจาก **S₁** ถึงจุด P
- $r_2$ = ระยะจาก **S₂** ถึงจุด P
- **Δr ใกล้จำนวนเต็มของ λ → เสริมกัน** (ปฏิบัพ)
- **Δr ใกล้ครึ่งหนึ่งของ λ → หักล้างกัน** (บัพ)
""")

    # ── 4. สูตรเงื่อนไข ─────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("## 4️⃣ สูตรเงื่อนไข (แหล่งกำเนิดเฟสตรงกัน)")

    _show(_fig_formula_summary)

    col_a, col_b = st.columns(2, gap="large")
    with col_a:
        st.markdown("""
<div class="box-green">
<strong>✅ ปฏิบัพ (Antinode) — เสริมกัน</strong>
</div>
""", unsafe_allow_html=True)
        st.latex(r"\Delta r = n\lambda \quad (n = 0,1,2,3,\ldots)")
        st.markdown("แอมพลิจูด = **2A** (สูงสุด)")

    with col_b:
        st.markdown("""
<div class="box-red">
<h4>❌ บัพ (Node) — หักล้างกัน</h4>
</div>
""", unsafe_allow_html=True)
        st.latex(r"\Delta r = \left(n - \frac{1}{2}\right)\lambda \quad (n = 1,2,3,\ldots)")
        st.markdown("แอมพลิจูด = **0** (เป็นศูนย์)")

    # ── 5. วิธีจำ 3 ขั้น ────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("## 5️⃣ วิธีทำโจทย์ — 3 ขั้นตอน ไม่ผิดพลาด!")

    _show(_fig_steps)

    st.markdown("""
<div class="box-green">

**🧮 ตัวอย่าง:** S₁ และ S₂ ให้คลื่น λ = 4 cm
จุด A ห่างจาก S₁ = 12 cm, ห่างจาก S₂ = 18 cm

**ขั้น 1:** Δr = 18 − 12 = **8 cm**

**ขั้น 2:** k = 8 ÷ 4 = **2.0**

**ขั้น 3:** k = 2.0 เป็นจำนวนเต็ม → จุด A อยู่บน **ปฏิบัพลำดับที่ 2** ✅
</div>
""", unsafe_allow_html=True)

    st.markdown("""
<div class="box-green">

**🧮 ตัวอย่างที่ 2:** λ = 4 cm, Δr = 6 cm

**ขั้น 2:** k = 6 ÷ 4 = **1.5**

**ขั้น 3:** k ลงท้าย .5 → **บัพลำดับที่ 2** ❌ (หักล้าง)
</div>
""", unsafe_allow_html=True)

    # ── 6. รูปแบบการแทรกสอดทั้งหมด ─────────────────────────────────────────
    st.markdown("---")
    st.markdown("## 6️⃣ รูปแบบการแทรกสอดทั้งหมด (Interference Pattern)")

    _show(_fig_pattern,
          "เส้นสีเขียว = แนวปฏิบัพ (เสริมกัน), เส้นประสีแดง = แนวบัพ (หักล้างกัน)")

    # ── 7. นับจำนวนแนว ──────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("## 7️⃣ นับจำนวนแนว — ใช้สูตรนี้")

    _show(_fig_count_guide,
          "ตัวอย่าง d = 10 cm, λ = 2 cm — นับตำแหน่งบัพและปฏิบัพบนเส้น S₁S₂")

    st.markdown("""
<div class="box-blue">
<h4>🔢 สูตรนับจำนวนแนว (เฟสตรงกัน)</h4>

หา $n_{max}$ ก่อน:
</div>
""", unsafe_allow_html=True)

    st.latex(r"n_{max} = \left\lfloor \frac{d}{\lambda} \right\rfloor \quad \text{(เอาแค่จำนวนเต็ม)}")

    col_c, col_d = st.columns(2)
    with col_c:
        st.markdown("**จำนวนแนวปฏิบัพทั้งหมด:**")
        st.latex(r"2n_{max} + 1")
    with col_d:
        st.markdown("**จำนวนแนวบัพทั้งหมด:**")
        st.latex(r"2n_{max}")

    st.markdown("""
<div class="box-green">

**ตัวอย่าง:** d = 10 cm, λ = 2.5 cm

$n_{max} = \lfloor 10/2.5 \rfloor = 4$

แนวปฏิบัพ = 2×4+1 = **9 แนว**, แนวบัพ = 2×4 = **8 แนว**
</div>
""", unsafe_allow_html=True)

    # ── 8. นับบน vs ระหว่าง ──────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("## 8️⃣ นับ 'บนแนว S₁S₂' vs 'ระหว่าง S₁S₂'")

    st.markdown("""
| | บนแนว S₁S₂ (รวม S₁ และ S₂) | ระหว่าง S₁S₂ (ไม่รวม S₁ S₂) |
|---|---|---|
| **ปฏิบัพ** | $2n_0 + 1$ | $2n_0 - 1$ |
| **บัพ** | $2n_0$ | $2(n_0 - 1)$ |

*(ใช้เมื่อ d หารด้วย λ ได้ลงตัวพอดี คือ $d = n_0 \\lambda$)*
""")

    st.markdown("""
<div class="box-warn">

⚠️ ถ้า $d / \\lambda$ <strong>ไม่ลงตัว</strong> ให้นับตามค่าจริงโดยเปรียบเทียบ Δr ≤ d
</div>
""", unsafe_allow_html=True)

    # ── 9. เฟสตรงข้าม ────────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("## 9️⃣ กรณีพิเศษ: แหล่งกำเนิดเฟสตรงข้าม (Anti-phase)")

    _show(_fig_antiphase_table)

    st.markdown("""
<div class="box-warn">

⚠️ <strong>เฟสตรงข้าม = เงื่อนไขสลับกันทั้งหมด!</strong>

- เมื่อ Δr = 0: คลื่นมาถึงพร้อมกัน แต่เฟสต่างกัน 180° อยู่แล้ว → **หักล้าง (บัพ)**
- เมื่อ Δr = λ/2: เฟสห่าง 180° + เพิ่มอีก 180° = 360° → **เสริม (ปฏิบัพ)**
</div>
""", unsafe_allow_html=True)

    # ── 10. ช่องสลิตคู่ ──────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("## 🔟 การแทรกสอดในทิศมุม θ (Double Slit)")

    _show(_fig_double_slit, "เส้นสีเขียวคือแนวปฏิบัพ — แต่ละเส้นสอดคล้องกับค่า n หนึ่งค่า")

    col_e, col_f = st.columns(2, gap="large")
    with col_e:
        st.markdown("**สูตรมุมปฏิบัพลำดับที่ n:**")
        st.latex(r"\sin\theta = \frac{n\lambda}{d}")
        st.markdown("**ระยะบนฉากที่ห่าง L (θ เล็ก):**")
        st.latex(r"x = \frac{n\lambda L}{d}")

    with col_f:
        st.markdown("""
<div class="box-green">

**ตัวอย่าง:** d = 10 cm, λ = 1 cm, L = 60 cm

ปฏิบัพที่ 1 (n = 1):

$x = (1 \\times 1 \\times 60)/10 = 6$ cm

ปฏิบัพที่ 2 (n = 2):

$x = (2 \\times 1 \\times 60)/10 = 12$ cm
</div>
""", unsafe_allow_html=True)

    # ── สรุปรวม ──────────────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("## 🗂️ ตารางสรุปรวม — ดูรวดเดียวจบ!")

    st.markdown("""
| สถานการณ์ | เงื่อนไขปฏิบัพ | เงื่อนไขบัพ |
|---|---|---|
| เฟสตรงกัน | $\\Delta r = 0, \\lambda, 2\\lambda, \\ldots$ | $\\Delta r = \\tfrac{\\lambda}{2}, \\tfrac{3\\lambda}{2}, \\ldots$ |
| เฟสตรงข้าม | $\\Delta r = \\tfrac{\\lambda}{2}, \\tfrac{3\\lambda}{2}, \\ldots$ | $\\Delta r = 0, \\lambda, 2\\lambda, \\ldots$ |
| แนวปฏิบัพทั้งหมด | $2n_{max}+1$ แนว | — |
| แนวบัพทั้งหมด | — | $2n_{max}$ แนว |
| มุม θ บนฉาก | $\\sin\\theta = n\\lambda/d$ | $\\sin\\theta = (n-\\tfrac{1}{2})\\lambda/d$ |
| ระยะ x บนฉาก | $x = n\\lambda L/d$ | — |
""")

    st.success("""
💪 **เคล็ดลับสุดท้าย:**
ทุกข้อเริ่มจาก **หา Δr** → **หารด้วย λ** → **ดูว่าได้จำนวนเต็มหรือ .5** → ตอบได้เลย!

🎉 ลองไปทำโจทย์ในแท็บ **📚 แบบฝึกหัด** ได้เลย!
""")
