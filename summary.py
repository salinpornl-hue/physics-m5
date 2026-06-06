"""
summary.py — สรุปเรื่อง "การแทรกสอดของคลื่น" แบบเข้าใจง่าย
แสดงผ่าน st.markdown + matplotlib figures
"""
import streamlit as st
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch


# ─── helpers ──────────────────────────────────────────────────────────────────

def _fig(func):
    """Call func() → return fig safely."""
    try:
        return func()
    except Exception as e:
        st.warning(f"[รูปไม่แสดง: {e}]")
        return None


def _show(func, caption=""):
    fig = _fig(func)
    if fig:
        st.pyplot(fig, use_container_width=True)
        if caption:
            st.caption(caption)
        plt.close(fig)


# ─── figures ──────────────────────────────────────────────────────────────────

def _fig_ripple():
    """Two circular wave sources, ripple pattern."""
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.set_xlim(-8, 8); ax.set_ylim(-5, 5)
    ax.set_aspect('equal'); ax.axis('off')

    lam = 2.0
    s1, s2 = np.array([-2.5, 0.0]), np.array([2.5, 0.0])

    for src, col in [(s1, '#2563eb'), (s2, '#dc2626')]:
        for r in np.arange(lam/2, 9, lam/2):
            circle = plt.Circle(src, r, color=col, fill=False,
                                lw=1.0, alpha=max(0.1, 1-r/9))
            ax.add_patch(circle)
        ax.plot(*src, 'o', color=col, ms=8, zorder=5)

    ax.text(-2.5, -0.5, '$S_1$', ha='center', fontsize=13, color='#2563eb', fontweight='bold')
    ax.text( 2.5, -0.5, '$S_2$', ha='center', fontsize=13, color='#dc2626', fontweight='bold')
    ax.set_title('คลื่นจากแหล่งกำเนิด 2 แหล่งแผ่ออกมาพบกัน', fontsize=12)
    fig.tight_layout()
    return fig


def _fig_constructive():
    """Two waves adding up — constructive."""
    fig, axes = plt.subplots(3, 1, figsize=(9, 5), sharex=True)
    x = np.linspace(0, 4*np.pi, 400)
    A = 1.0
    y1 = A * np.sin(x)
    y2 = A * np.sin(x)
    ysum = y1 + y2

    axes[0].plot(x, y1, '#2563eb', lw=2)
    axes[0].axhline(0, color='k', lw=0.6)
    axes[0].set_ylabel('คลื่น 1', fontsize=10)
    axes[0].set_ylim(-2.5, 2.5); axes[0].set_yticks([])

    axes[1].plot(x, y2, '#dc2626', lw=2)
    axes[1].axhline(0, color='k', lw=0.6)
    axes[1].set_ylabel('คลื่น 2', fontsize=10)
    axes[1].set_ylim(-2.5, 2.5); axes[1].set_yticks([])

    axes[2].fill_between(x, ysum, alpha=0.25, color='#16a34a')
    axes[2].plot(x, ysum, '#16a34a', lw=3)
    axes[2].axhline(0, color='k', lw=0.6)
    axes[2].set_ylabel('ผลรวม', fontsize=10)
    axes[2].set_ylim(-2.5, 2.5); axes[2].set_yticks([-2, 0, 2])
    axes[2].set_xlabel('ตำแหน่ง', fontsize=10)

    axes[2].annotate('แอมพลิจูดเป็น 2 เท่า!', xy=(np.pi/2, 2), xytext=(np.pi/2+2, 2.2),
                     arrowprops=dict(arrowstyle='->', color='green', lw=1.5),
                     fontsize=10, color='green', fontweight='bold')

    fig.suptitle('การแทรกสอดแบบเสริมกัน (Constructive) 🟢', fontsize=13, fontweight='bold', color='#16a34a')
    fig.tight_layout()
    return fig


def _fig_destructive():
    """Two waves cancelling — destructive."""
    fig, axes = plt.subplots(3, 1, figsize=(9, 5), sharex=True)
    x = np.linspace(0, 4*np.pi, 400)
    A = 1.0
    y1 =  A * np.sin(x)
    y2 = -A * np.sin(x)   # phase diff = π
    ysum = y1 + y2

    axes[0].plot(x, y1, '#2563eb', lw=2)
    axes[0].axhline(0, color='k', lw=0.6)
    axes[0].set_ylabel('คลื่น 1', fontsize=10)
    axes[0].set_ylim(-2.5, 2.5); axes[0].set_yticks([])

    axes[1].plot(x, y2, '#dc2626', lw=2)
    axes[1].axhline(0, color='k', lw=0.6)
    axes[1].set_ylabel('คลื่น 2', fontsize=10)
    axes[1].set_ylim(-2.5, 2.5); axes[1].set_yticks([])
    axes[1].annotate('(เฟสตรงข้ามกัน)', (np.pi, -1), fontsize=9,
                     color='#dc2626', ha='center', xytext=(np.pi, -2.2),
                     arrowprops=dict(arrowstyle='->', color='#dc2626', lw=1))

    axes[2].fill_between(x, ysum, alpha=0.25, color='#6b7280')
    axes[2].plot(x, ysum, '#6b7280', lw=3)
    axes[2].axhline(0, color='k', lw=1.5, ls='--')
    axes[2].set_ylabel('ผลรวม = 0', fontsize=10)
    axes[2].set_ylim(-2.5, 2.5); axes[2].set_yticks([-2, 0, 2])
    axes[2].set_xlabel('ตำแหน่ง', fontsize=10)
    axes[2].text(2*np.pi, 0.3, 'หักล้างกันหมด!', fontsize=11,
                 color='gray', fontweight='bold', ha='center')

    fig.suptitle('การแทรกสอดแบบหักล้างกัน (Destructive) 🔴', fontsize=13, fontweight='bold', color='#dc2626')
    fig.tight_layout()
    return fig


def _fig_path_diff():
    """Path difference diagram — two sources S1 S2, point P."""
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.set_xlim(-1, 9); ax.set_ylim(-1, 6)
    ax.set_aspect('equal'); ax.axis('off')

    s1 = np.array([0.0, 4.0])
    s2 = np.array([0.0, 0.0])
    P  = np.array([7.0, 2.5])

    # draw sources
    ax.plot(*s1, 'o', color='#2563eb', ms=12, zorder=5)
    ax.plot(*s2, 'o', color='#dc2626', ms=12, zorder=5)
    ax.text(s1[0]-0.4, s1[1], '$S_1$', ha='right', fontsize=14,
            color='#2563eb', fontweight='bold')
    ax.text(s2[0]-0.4, s2[1], '$S_2$', ha='right', fontsize=14,
            color='#dc2626', fontweight='bold')

    # draw P
    ax.plot(*P, '^', color='#16a34a', ms=12, zorder=5)
    ax.text(P[0]+0.2, P[1]+0.15, 'P', fontsize=14,
            color='#16a34a', fontweight='bold')

    # lines
    ax.plot([s1[0], P[0]], [s1[1], P[1]], '#2563eb', lw=2, ls='--')
    ax.plot([s2[0], P[0]], [s2[1], P[1]], '#dc2626', lw=2, ls='--')

    # distance labels
    mid1 = (s1 + P) / 2
    mid2 = (s2 + P) / 2
    r1 = np.linalg.norm(P - s1)
    r2 = np.linalg.norm(P - s2)
    ax.text(mid1[0]-0.3, mid1[1]+0.25, f'$r_1={r1:.1f}$', fontsize=11,
            color='#2563eb', rotation=np.degrees(np.arctan2(P[1]-s1[1], P[0]-s1[0])))
    ax.text(mid2[0]+0.1, mid2[1]-0.35, f'$r_2={r2:.1f}$', fontsize=11,
            color='#dc2626', rotation=np.degrees(np.arctan2(P[1]-s2[1], P[0]-s2[0])))

    dr = abs(r2 - r1)
    ax.text(4.5, 5.2,
            f'ผลต่างระยะทาง  $\\Delta r = |r_2 - r_1| = {dr:.1f}$',
            fontsize=12, ha='center',
            bbox=dict(boxstyle='round,pad=0.4', fc='#fef3c7', ec='orange', lw=1.5))

    fig.suptitle('ผลต่างระยะทาง (Path Difference) คือหัวใจสำคัญ!', fontsize=12, fontweight='bold')
    fig.tight_layout()
    return fig


def _fig_interference_pattern():
    """Full interference pattern with labeled antinodal/nodal lines."""
    fig, ax = plt.subplots(figsize=(9, 6))
    d, lam = 10.0, 2.5
    n_max = int(d / lam)   # = 4

    s1 = np.array([0.0,  d/2])
    s2 = np.array([0.0, -d/2])
    ax.plot(*s1, 'o', color='#2563eb', ms=10, zorder=5)
    ax.plot(*s2, 's', color='#dc2626', ms=10, zorder=5)
    ax.text(s1[0]-0.5, s1[1], '$S_1$', ha='right', fontsize=12, color='#2563eb', fontweight='bold')
    ax.text(s2[0]-0.5, s2[1], '$S_2$', ha='right', fontsize=12, color='#dc2626', fontweight='bold')

    r_max = 28

    # Antinodal lines (constructive)
    for n in range(-n_max, n_max+1):
        val = n * lam / d
        if abs(val) <= 1:
            th = np.arcsin(val)
            xe, ye = r_max*np.cos(th), r_max*np.sin(th)
            ax.plot([0, xe], [0, ye], '#16a34a', lw=2.0, alpha=0.85)
            label = f'A{abs(n)}' if n != 0 else 'A₀\n(กลาง)'
            ax.text(xe*1.05, ye*1.05, label, fontsize=8,
                    color='#16a34a', ha='center', fontweight='bold')

    # Nodal lines (destructive)
    for n in range(1, n_max+1):
        for sign in [1, -1]:
            val = (n - 0.5) * lam / d
            if abs(val) <= 1:
                th = np.arcsin(sign * val)
                xe, ye = r_max*np.cos(th), r_max*np.sin(th)
                ax.plot([0, xe], [0, ye], '#dc2626', lw=1.2,
                        ls='--', alpha=0.7)
                ax.text(xe*1.05, ye*1.05, f'N{n}', fontsize=8,
                        color='#dc2626', ha='center')

    # Legend patches
    anti = mpatches.Patch(color='#16a34a', label='แนวปฏิบัพ (เสริมกัน)')
    node = mpatches.Patch(color='#dc2626', label='แนวบัพ (หักล้างกัน)', linestyle='--', fill=False,
                          edgecolor='#dc2626')
    ax.legend(handles=[anti, node], loc='lower right', fontsize=10)

    ax.set_xlim(-3, 31); ax.set_ylim(-12, 12)
    ax.set_xlabel('ระยะห่างจากแหล่งกำเนิด (cm)', fontsize=10)
    ax.set_title('รูปแบบการแทรกสอด: d=10cm, λ=2.5cm\n'
                 '(เส้นสีเขียว=ปฏิบัพ, เส้นประสีแดง=บัพ)', fontsize=11)
    ax.axhline(0, color='gray', lw=0.5, ls=':')
    fig.tight_layout()
    return fig


def _fig_node_count():
    """Visual guide for counting antinodes/nodes on S1S2 line."""
    fig, ax = plt.subplots(figsize=(9, 3))
    ax.set_xlim(-0.5, 11); ax.set_ylim(-1.5, 2)
    ax.axis('off')

    d, lam = 10.0, 2.0
    n0 = int(d / lam)   # 5

    # S1 at x=0, S2 at x=10
    ax.plot(0,  0, 'o', color='#2563eb', ms=14, zorder=5)
    ax.plot(10, 0, 's', color='#dc2626', ms=14, zorder=5)
    ax.text(0,  -0.55, '$S_1$', ha='center', fontsize=12, color='#2563eb', fontweight='bold')
    ax.text(10, -0.55, '$S_2$', ha='right',  fontsize=12, color='#dc2626', fontweight='bold')

    # line
    ax.plot([0, 10], [0, 0], 'k-', lw=2)

    # Antinodes: Δr = 0,2,4,6,8,10  → x positions
    antinodes_x = [5, 4, 6, 3, 7, 2, 8, 1, 9, 0, 10]
    dr_vals      = [0, 2, 2, 4, 4, 6, 6, 8, 8, 10, 10]
    for x, dr in zip(antinodes_x, dr_vals):
        ax.plot(x, 0, 'D', color='#16a34a', ms=10, zorder=6)
        ax.text(x, 0.55, f'Δr={dr}', ha='center', fontsize=7.5,
                color='#16a34a', fontweight='bold')

    # Nodes: Δr = 1,3,5,7,9
    for dr in [1, 3, 5, 7, 9]:
        for x in [(10+dr)/2, (10-dr)/2]:
            ax.plot(x, 0, 'v', color='#dc2626', ms=9, zorder=6)
            ax.text(x, -1.05, f'Δr={dr}', ha='center', fontsize=7.5, color='#dc2626')

    ax.text(5, 1.6,
            f'd={int(d)} cm, λ={int(lam)} cm  →  นับ Δr/λ: จำนวนเต็ม=ปฏิบัพ ■, ทศนิยม .5=บัพ ▼',
            ha='center', fontsize=9,
            bbox=dict(boxstyle='round,pad=0.3', fc='#fffbeb', ec='orange'))

    fig.tight_layout()
    return fig


def _fig_formula_card():
    """Visual formula summary card."""
    fig, ax = plt.subplots(figsize=(9, 4.5))
    ax.axis('off')

    # Two boxes side by side
    for xc, color, fc, title, lines in [
        (0.25, '#16a34a', '#dcfce7',
         '✅ เสริมกัน (ปฏิบัพ)',
         [r'$\Delta r = 0,\ \lambda,\ 2\lambda,\ 3\lambda,\ \ldots$',
          r'$\Delta r = n\lambda \quad (n = 0,1,2,\ldots)$',
          '',
          r'เฟสตรงกัน → ยอดชนยอด',
          r'แอมพลิจูด = $2A$ (สูงสุด)']),
        (0.75, '#dc2626', '#fee2e2',
         '❌ หักล้างกัน (บัพ)',
         [r'$\Delta r = \tfrac{\lambda}{2},\ \tfrac{3\lambda}{2},\ \tfrac{5\lambda}{2},\ \ldots$',
          r'$\Delta r = (n-\tfrac{1}{2})\lambda \quad (n = 1,2,\ldots)$',
          '',
          r'เฟสตรงข้าม → ยอดชนราง',
          r'แอมพลิจูด = $0$ (เป็นศูนย์)']),
    ]:
        rect = mpatches.FancyBboxPatch((xc-0.22, 0.05), 0.44, 0.9,
                                       boxstyle='round,pad=0.02',
                                       fc=fc, ec=color, lw=2,
                                       transform=ax.transAxes, clip_on=False)
        ax.add_patch(rect)
        ax.text(xc, 0.88, title, transform=ax.transAxes,
                ha='center', va='top', fontsize=12, fontweight='bold', color=color)
        for i, line in enumerate(lines):
            ax.text(xc, 0.75 - i*0.13, line, transform=ax.transAxes,
                    ha='center', va='top', fontsize=10.5)

    ax.text(0.5, 0.98, '📋 สรุปสูตร: เงื่อนไขการแทรกสอด (เฟสตรงกัน)',
            transform=ax.transAxes, ha='center', va='top',
            fontsize=13, fontweight='bold')
    fig.tight_layout()
    return fig


def _fig_mnemonic():
    """Simple mnemonic: divide Δr by λ → integer=antinode, half=node."""
    fig, ax = plt.subplots(figsize=(8, 3))
    ax.axis('off')

    steps = [
        ('① คำนวณ\nผลต่างระยะทาง', r'$\Delta r = |r_1 - r_2|$', '#6366f1'),
        ('② หารด้วย\nความยาวคลื่น', r'$k = \Delta r \div \lambda$', '#0891b2'),
        ('③ ดูผลลัพธ์\n', '', '#374151'),
    ]
    for i, (label, formula, color) in enumerate(steps):
        x = 0.13 + i * 0.32
        rect = mpatches.FancyBboxPatch((x-0.11, 0.1), 0.22, 0.8,
                                       boxstyle='round,pad=0.02',
                                       fc='white', ec=color, lw=2,
                                       transform=ax.transAxes, clip_on=False)
        ax.add_patch(rect)
        ax.text(x, 0.78, label, transform=ax.transAxes,
                ha='center', va='top', fontsize=10, color=color, fontweight='bold')
        ax.text(x, 0.42, formula, transform=ax.transAxes,
                ha='center', va='top', fontsize=11)
        if i < 2:
            ax.annotate('', xy=(x+0.12, 0.5), xytext=(x+0.085, 0.5),
                        xycoords='axes fraction', textcoords='axes fraction',
                        arrowprops=dict(arrowstyle='->', color='gray', lw=2))

    # Step 3 result boxes
    for xr, label, col, fc in [
        (0.69, 'จำนวนเต็ม\n→ ปฏิบัพ (เสริม)', '#16a34a', '#dcfce7'),
        (0.87, 'ลงท้าย .5\n→ บัพ (หักล้าง)', '#dc2626', '#fee2e2'),
    ]:
        rect = mpatches.FancyBboxPatch((xr-0.09, 0.1), 0.18, 0.8,
                                       boxstyle='round,pad=0.02',
                                       fc=fc, ec=col, lw=1.5,
                                       transform=ax.transAxes, clip_on=False)
        ax.add_patch(rect)
        ax.text(xr, 0.62, label, transform=ax.transAxes,
                ha='center', va='top', fontsize=9.5, color=col, fontweight='bold')

    ax.annotate('', xy=(0.60, 0.5), xytext=(0.565, 0.5),
                xycoords='axes fraction', textcoords='axes fraction',
                arrowprops=dict(arrowstyle='->', color='gray', lw=2))

    ax.set_title('⚡ วิธีจำแบบง่าย — ทำ 3 ขั้น แล้วตอบได้เลย!',
                 fontsize=12, fontweight='bold', pad=8)
    fig.tight_layout()
    return fig


def _fig_antiphase():
    """Antiphase sources: conditions swap."""
    fig, ax = plt.subplots(figsize=(7, 3.5))
    ax.axis('off')

    rows = [
        ('ผลต่าง Δr', 'เฟสตรงกัน (ปกติ)', 'เฟสตรงข้าม (สลับ)'),
        ('0, λ, 2λ, …',    '✅ ปฏิบัพ', '❌ บัพ'),
        ('λ/2, 3λ/2, …',  '❌ บัพ',    '✅ ปฏิบัพ'),
    ]
    col_colors = [['#e2e8f0']*3,
                  ['#f8fafc', '#dcfce7', '#fee2e2'],
                  ['#f8fafc', '#fee2e2', '#dcfce7']]
    table = ax.table(cellText=rows, cellLoc='center', loc='center',
                     cellColours=col_colors)
    table.auto_set_font_size(False)
    table.set_fontsize(11)
    table.scale(1, 2.5)

    ax.set_title('📌 เมื่อแหล่งกำเนิดเฟสตรงข้ามกัน — เงื่อนไขสลับกัน!',
                 fontsize=12, fontweight='bold', pad=14)
    fig.tight_layout()
    return fig


# ─── main render function ──────────────────────────────────────────────────────

def render_summary():
    st.markdown("""
<style>
.sum-header {
    font-size: 2rem; font-weight: 800; color: #1e3a8a;
    text-align: center; margin-bottom: 4px;
}
.sum-sub {
    font-size: 1rem; color: #64748b;
    text-align: center; margin-bottom: 24px;
}
.concept-box {
    background: #eff6ff;
    border-left: 5px solid #2563eb;
    border-radius: 8px;
    padding: 14px 18px;
    margin: 12px 0;
}
.concept-box h4 { margin: 0 0 6px 0; color: #1e40af; }
.warn-box {
    background: #fffbeb;
    border-left: 5px solid #f59e0b;
    border-radius: 8px;
    padding: 12px 16px;
    margin: 12px 0;
}
.example-box {
    background: #f0fdf4;
    border: 1px solid #86efac;
    border-radius: 8px;
    padding: 14px 18px;
    margin: 12px 0;
}
</style>
""", unsafe_allow_html=True)

    st.markdown('<div class="sum-header">🌊 การแทรกสอดของคลื่น</div>', unsafe_allow_html=True)
    st.markdown('<div class="sum-sub">Wave Interference — อ่านแล้วเข้าใจได้เลย!</div>', unsafe_allow_html=True)

    # ── Section 1: คืออะไร
    st.markdown("---")
    st.markdown("## 1️⃣ การแทรกสอดคืออะไร?")

    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("""
<div class="concept-box">
<h4>🔑 นิยามง่ายๆ</h4>

**การแทรกสอด** คือปรากฏการณ์ที่คลื่น **2 ขบวนมาพบกัน** แล้วรวมกัน

- ถ้ายอดมาชนยอด → **เสริมกัน** (แอมพลิจูดสูงขึ้น)
- ถ้ายอดมาชนราง → **หักล้างกัน** (แอมพลิจูดลดลง หรือเป็นศูนย์)

> 💡 คิดเหมือนเพื่อน 2 คนโยนก้อนหินลงสระ
> คลื่นจากทั้งสองมาเจอกัน — บางจุดคลื่นสูงมาก บางจุดเงียบ!
</div>
""", unsafe_allow_html=True)

    with col2:
        _show(_fig_ripple, "คลื่นจาก S₁ (สีน้ำเงิน) และ S₂ (สีแดง) แผ่ออกมาพบกัน")

    # ── Section 2: เสริม vs หักล้าง
    st.markdown("---")
    st.markdown("## 2️⃣ เสริมกัน vs หักล้างกัน")

    c1, c2 = st.columns(2)
    with c1:
        _show(_fig_constructive, "คลื่นสองขบวนเฟสตรงกัน → รวมกันได้แอมพลิจูดเป็น 2 เท่า")
    with c2:
        _show(_fig_destructive, "คลื่นสองขบวนเฟสตรงข้ามกัน → หักล้างกันจนเป็นศูนย์")

    st.markdown("""
<div class="warn-box">
⚠️ <strong>จำไว้!</strong> คลื่นสองขบวนผ่านกันแล้ว ต่างก็เดินทางต่อเหมือนไม่มีอะไรเกิดขึ้น
การแทรกสอดเป็นแค่ผลชั่วคราวตรงจุดที่พบกัน
</div>
""", unsafe_allow_html=True)

    # ── Section 3: ผลต่างระยะทาง
    st.markdown("---")
    st.markdown("## 3️⃣ ผลต่างระยะทาง (Δr) — กุญแจสำคัญ!")

    _show(_fig_path_diff,
          "ผลต่างระยะทาง Δr = ระยะห่างจากแหล่งกำเนิดสองแหล่งมายังจุด P ที่ต่างกัน")

    st.markdown("""
<div class="concept-box">
<h4>📏 ผลต่างระยะทาง (Path Difference)</h4>

$$\\Delta r = |r_1 - r_2|$$

- $r_1$ = ระยะจาก **S₁** ถึงจุด P
- $r_2$ = ระยะจาก **S₂** ถึงจุด P

**ยิ่ง Δr ใกล้จำนวนเต็มของ λ → ยิ่งเสริมกัน**
**ยิ่ง Δr ใกล้ครึ่งหนึ่งของ λ → ยิ่งหักล้างกัน**
</div>
""", unsafe_allow_html=True)

    # ── Section 4: สูตรเงื่อนไข
    st.markdown("---")
    st.markdown("## 4️⃣ สูตรเงื่อนไข (เฟสตรงกัน)")

    _show(_fig_formula_card)

    st.markdown("""
<div class="example-box">

**🧮 ตัวอย่าง:** S₁S₂ ให้คลื่น λ = 4 cm, จุด A ห่างจาก S₁ = 12 cm, ห่างจาก S₂ = 18 cm

$$\\Delta r = 18 - 12 = 6 \\text{ cm}$$

$$\\frac{\\Delta r}{\\lambda} = \\frac{6}{4} = 1.5$$

ลงท้ายด้วย **.5** → จุด A อยู่บน**บัพ** (หักล้างกัน) ลำดับที่ 2 ✅
</div>
""", unsafe_allow_html=True)

    # ── Section 5: วิธีจำ
    st.markdown("---")
    st.markdown("## 5️⃣ วิธีจำ — 3 ขั้นตอน")

    _show(_fig_mnemonic)

    st.markdown("""
<div class="example-box">

**🧮 ลองทำ:** จุด B: r₁ = 20 cm, r₂ = 28 cm, λ = 4 cm

**ขั้น 1:** Δr = 28 − 20 = **8 cm**

**ขั้น 2:** k = 8 ÷ 4 = **2.0**

**ขั้น 3:** เป็นจำนวนเต็ม → **ปฏิบัพลำดับที่ 2** 🎉
</div>
""", unsafe_allow_html=True)

    # ── Section 6: รูปแบบการแทรกสอด
    st.markdown("---")
    st.markdown("## 6️⃣ รูปแบบการแทรกสอดทั้งหมด")

    _show(_fig_interference_pattern,
          "แนวปฏิบัพ (เส้นสีเขียว) และแนวบัพ (เส้นประสีแดง) ที่เกิดขึ้น")

    st.markdown("""
<div class="concept-box">
<h4>🔢 วิธีนับจำนวนแนว (เฟสตรงกัน)</h4>

หา $n_{max} = \\left\\lfloor \\dfrac{d}{\\lambda} \\right\\rfloor$ (เอาแค่จำนวนเต็ม)

| สิ่งที่นับ | สูตร |
|-----------|------|
| แนวปฏิบัพทั้งหมด | $2n_{max} + 1$ |
| แนวบัพทั้งหมด | $2n_{max}$ |

**ตัวอย่าง:** d = 10 cm, λ = 2.5 cm → n_max = 4

แนวปฏิบัพ = 2×4+1 = **9 แนว**, แนวบัพ = 2×4 = **8 แนว**
</div>
""", unsafe_allow_html=True)

    _show(_fig_node_count,
          "ตัวอย่างการนับตำแหน่งบัพและปฏิบัพบนเส้น S₁S₂ (d=10cm, λ=2cm)")

    # ── Section 7: กรณีบนแนว S1S2
    st.markdown("---")
    st.markdown("## 7️⃣ นับเฉพาะ บน/ระหว่าง เส้น S₁S₂")

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("""
**📍 บนแนวเส้น S₁S₂ (รวม S₁ และ S₂)**

$$\\text{ปฏิบัพ} = 2n_0 + 1$$
$$\\text{บัพ} = 2n_0$$

โดย $n_0 = \\left\\lfloor \\dfrac{d}{\\lambda} \\right\\rfloor$
""")
    with col_b:
        st.markdown("""
**📍 ระหว่าง S₁S₂ (ไม่รวม S₁ และ S₂)**

$$\\text{ปฏิบัพ} = 2n_0 - 1 \\quad \\text{(ถ้า } d=n_0\\lambda\\text{)}$$
$$\\text{บัพ} = 2(n_0 - 1) \\quad \\text{(กรณีเดียวกัน)}$$

⚠️ ถ้า d ไม่ใช่จำนวนเต็มของ λ ให้นับตามจริง
""")

    # ── Section 8: เฟสตรงข้าม
    st.markdown("---")
    st.markdown("## 8️⃣ กรณีพิเศษ: แหล่งกำเนิดเฟสตรงข้ามกัน")

    _show(_fig_antiphase)

    st.markdown("""
<div class="warn-box">
⚠️ <strong>เฟสตรงข้าม = เงื่อนไขสลับกัน!</strong><br>
เมื่อ Δr = 0 → คลื่นมาถึงพร้อมกัน แต่เฟสต่างกัน 180° → <strong>หักล้าง (บัพ)</strong><br>
เมื่อ Δr = λ/2 → เฟสต่างกัน 180° + 180° = 360° → <strong>เสริม (ปฏิบัพ)</strong>
</div>
""", unsafe_allow_html=True)

    # ── Section 9: Double-slit (มุม θ)
    st.markdown("---")
    st.markdown("## 9️⃣ ปฏิบัพในทิศมุม θ (Double Slit)")

    col_f, col_ex = st.columns([1, 1])
    with col_f:
        st.markdown("""
<div class="concept-box">
<h4>📐 สูตร</h4>

$$\\sin\\theta = \\frac{n\\lambda}{d}$$

- $n$ = ลำดับปฏิบัพ (0, 1, 2, …)
- $d$ = ระยะห่างแหล่งกำเนิด
- $\\lambda$ = ความยาวคลื่น

**ถ้าฉากอยู่ห่าง L (และ θ เล็ก):**
$$x = \\frac{n\\lambda L}{d}$$
</div>
""", unsafe_allow_html=True)

    with col_ex:
        st.markdown("""
<div class="example-box">

**🧮 ตัวอย่าง:** d = 10 cm, λ = 1 cm, L = 60 cm

ปฏิบัพที่ 1 (n=1):
$$x = \\frac{1 \\times 1 \\times 60}{10} = 6 \\text{ cm}$$

ปฏิบัพที่ 2 (n=2):
$$x = \\frac{2 \\times 1 \\times 60}{10} = 12 \\text{ cm}$$
</div>
""", unsafe_allow_html=True)

    # ── Section 10: สรุปทุกอย่าง
    st.markdown("---")
    st.markdown("## 🗂️ สรุปรวม — ดูรวดเดียวจบ")

    st.markdown("""
| สถานการณ์ | เงื่อนไขปฏิบัพ | เงื่อนไขบัพ |
|-----------|----------------|------------|
| เฟสตรงกัน | Δr = 0, λ, 2λ, … | Δr = λ/2, 3λ/2, … |
| เฟสตรงข้าม | Δr = λ/2, 3λ/2, … | Δr = 0, λ, 2λ, … |
| จำนวนแนวปฏิบัพ | $2n_{max}+1$ แนว | — |
| จำนวนแนวบัพ | — | $2n_{max}$ แนว |
| ปฏิบัพทิศ θ | $\\sin\\theta = n\\lambda/d$ | $\\sin\\theta = (n-½)\\lambda/d$ |
| ระยะบนฉาก | $x = n\\lambda L/d$ | — |

> 💪 **เคล็ดลับสุดท้าย:** ทุกข้อเริ่มจาก Δr → หารด้วย λ → ดูตัวเลข → ตอบได้เลย!
""")

    st.success("🎉 เข้าใจแล้ว! ลองไปทำโจทย์ในแท็บ 📚 แบบฝึกหัด ได้เลย")
