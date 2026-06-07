"""
summary_standing_waves.py — Standing Waves & Resonance summary (English)
Style mirrors summary.py
"""
import io as _io
import streamlit as st
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import matplotlib.font_manager as fm

# ── Font ──────────────────────────────────────────────────────────────────────
_THAI  = ['Tahoma', 'Arial Unicode MS', 'Browallia New', 'DejaVu Sans']
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
CP   = '#7c3aed'
CY   = '#d97706'

# ── CSS (same tokens as summary.py) ──────────────────────────────────────────
_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');
.sw-wrap { font-family: 'Inter', sans-serif; }

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
def _cached_fig_png(key: str) -> bytes:
    _map = {
        "formation":    _fig_formation,
        "harmonics":    _fig_harmonics,
        "one_end":      _fig_one_end,
        "speed_table":  _fig_speed_table,
    }
    fig = _map[key]()
    buf = _io.BytesIO()
    fig.savefig(buf, format="png", dpi=110, bbox_inches="tight")
    buf.seek(0)
    plt.close(fig)
    return buf.getvalue()


def _show(key: str, cap: str = ""):
    try:
        png = _cached_fig_png(key)
        st.image(png, use_container_width=True)
        if cap:
            st.markdown(f'<p class="cap">{cap}</p>', unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Figure error ({key}): {e}")


# ═══════════════════════════════════════════════════════════════════════════════
#  FIGURE 1 — Standing wave formation (two travelling waves → standing wave)
# ═══════════════════════════════════════════════════════════════════════════════
def _fig_formation():
    with plt.rc_context(RC):
        fig, axes = plt.subplots(3, 1, figsize=(10, 6.0),
                                 gridspec_kw={'hspace': 0.55})
        fig.patch.set_facecolor(CBG)
        x = np.linspace(0, 4, 800)
        t_vals = [0, 0.125, 0.25]   # fractions of T

        configs = [
            (CB,   r'Wave 1 →   $y_1 = A\sin(kx - \omega t)$',   +1),
            (CR,   r'Wave 2 ←   $y_2 = A\sin(kx + \omega t)$',   -1),
            (CG,   r'Standing wave:   $y = 2A\sin(kx)\cos(\omega t)$', 0),
        ]
        linestyles = ['-', '--', '-.']
        time_labels = ['t = 0', 't = T/8', 't = T/4']
        alpha_vals  = [1.0, 0.55, 0.28]

        for row, (col, title, direction) in enumerate(configs):
            ax = axes[row]
            ax.set_facecolor('#f8fafc' if row < 2 else '#f0fdf4')
            for ti, (t, ls, alp) in enumerate(zip(t_vals, linestyles, alpha_vals)):
                phi = 2 * np.pi * t
                if row == 0:
                    y = np.sin(2*np.pi*x - phi)
                elif row == 1:
                    y = np.sin(2*np.pi*x + phi)
                else:
                    y = 2 * np.sin(2*np.pi*x) * np.cos(phi)

                ax.plot(x, y, color=col, lw=2.2 if ti == 0 else 1.2,
                        ls=ls, alpha=alp,
                        label=time_labels[ti] if row == 2 else None)

            if row == 2:
                # shade envelope
                env = 2 * np.abs(np.sin(2*np.pi*x))
                ax.fill_between(x,  env, -env, color=CG, alpha=0.07)
                ax.plot(x,  env, color=CG, lw=0.9, ls=':', alpha=0.5)
                ax.plot(x, -env, color=CG, lw=0.9, ls=':', alpha=0.5)

                # mark nodes and antinodes
                nodes     = np.arange(0, 4.01, 0.5)
                antinodes = np.arange(0.25, 4.01, 0.5)
                for xn in nodes:
                    ax.axvline(xn, color='#94a3b8', lw=0.7, ls=':', alpha=0.5)
                    ax.text(xn, -2.55, 'N', ha='center', fontsize=7, color=CGR)
                for xa in antinodes:
                    ax.plot(xa, 0, 'D', color=CG, ms=5, zorder=5)
                    ax.text(xa, 2.55, 'AN', ha='center', fontsize=7,
                            color=CG, fontweight='bold')

                ax.legend(fontsize=8, loc='upper right',
                          framealpha=0.9, edgecolor='#e2e8f0')

            ax.axhline(0, color='#94a3b8', lw=0.7, ls=':')
            ax.set_xlim(0, 4); ax.set_ylim(-2.8, 2.8)
            ax.set_xticks(np.arange(0, 4.5, 0.5))
            ax.set_xticklabels([f'{v:.1f}λ' if v != int(v) else f'{int(v)}λ'
                                 for v in np.arange(0, 4.5, 0.5)], fontsize=8)
            ax.set_yticks([-2, -1, 0, 1, 2])
            ax.set_yticklabels(['-2A', '-A', '0', '+A', '+2A'], fontsize=8)
            ax.set_title(title, fontsize=9.5, color=col, fontweight='700', pad=4)
            ax.spines[['top', 'right']].set_visible(False)

        fig.suptitle('How a Standing Wave Forms: Two Identical Waves Travelling in Opposite Directions',
                     fontsize=11, fontweight='bold', color=CDK, y=1.01)
        fig.tight_layout()
    return fig


# ═══════════════════════════════════════════════════════════════════════════════
#  FIGURE 2 — Harmonics on a string (both ends fixed), n = 1–4
# ═══════════════════════════════════════════════════════════════════════════════
def _fig_harmonics():
    with plt.rc_context(RC):
        fig, axes = plt.subplots(4, 1, figsize=(10, 7.5),
                                 gridspec_kw={'hspace': 0.70})
        fig.patch.set_facecolor(CBG)
        x = np.linspace(0, 1, 800)

        colors = [CB, CG, CP, CY]
        for n, (ax, col) in enumerate(zip(axes, colors), start=1):
            y = np.sin(n * np.pi * x)

            ax.set_facecolor('#f8fafc')
            ax.fill_between(x,  y, 0, where=(y >= 0), color=col, alpha=0.18)
            ax.fill_between(x,  y, 0, where=(y <  0), color=col, alpha=0.09)
            ax.plot(x, y,  color=col, lw=2.8, solid_capstyle='round')
            ax.plot(x, -y, color=col, lw=1.0, ls='--', alpha=0.35)
            ax.axhline(0, color='#94a3b8', lw=0.8, ls=':')

            # Nodes
            node_xs = [i / n for i in range(n + 1)]
            for xn in node_xs:
                ax.plot(xn, 0, 'o', color='#475569', ms=8, zorder=6,
                        markeredgecolor='white', markeredgewidth=1.4)
                ax.text(xn, -1.45, 'N', ha='center', fontsize=7.5,
                        color=CGR, fontweight='600')

            # Antinodes
            anti_xs = [(2*i - 1) / (2*n) for i in range(1, n + 1)]
            for xa in anti_xs:
                ax.plot(xa, np.sin(n * np.pi * xa), 'D',
                        color=col, ms=7, zorder=6,
                        markeredgecolor='white', markeredgewidth=1.2)

            # Labels right side
            loops = n
            lam_n = f'λ = 2L/{n}' if n > 1 else 'λ = 2L'
            f_n   = f'f = {n}f₁' if n > 1 else 'f = f₁  (fundamental)'
            overtone = (f'{n-1}st overtone' if n == 2 else
                        f'{n-1}nd overtone' if n == 3 else
                        f'{n-1}rd overtone' if n == 4 else '')
            harmonic_name = (f'Harmonic {n}'
                             + (f' — {overtone}' if overtone else ''))

            ax.set_xlim(-0.04, 1.30)
            ax.set_ylim(-1.7, 1.7)
            ax.axis('off')

            # String endpoints
            for xe in [0, 1]:
                ax.plot(xe, 0, 's', color=CDK, ms=10, zorder=7,
                        markeredgecolor='white', markeredgewidth=1.5)

            # Annotations right
            ax.text(1.05, 0.55, harmonic_name, fontsize=9, color=col,
                    fontweight='800', va='center')
            ax.text(1.05, 0.10, f'  {lam_n}', fontsize=8.5, color=CDK, va='center')
            ax.text(1.05,-0.32, f'  {f_n}',   fontsize=8.5, color=CDK, va='center')
            ax.text(1.05,-0.72, f'  Loops: {loops}  |  Nodes: {n+1}  |  Antinodes: {n}',
                    fontsize=7.5, color=CGR, va='center')

            # L arrow below
            ax.annotate('', xy=(1, -1.30), xytext=(0, -1.30),
                        arrowprops=dict(arrowstyle='<->', color=CGR, lw=1.2))
            ax.text(0.5, -1.55, 'L', ha='center', fontsize=8.5,
                    color=CGR, fontweight='700')

        axes[0].set_title('Standing Waves on a String — Both Ends Fixed',
                          fontsize=11, fontweight='bold', color=CDK, pad=6)
        fig.tight_layout()
    return fig


# ═══════════════════════════════════════════════════════════════════════════════
#  FIGURE 3 — One end fixed, one end free  (odd harmonics only)
# ═══════════════════════════════════════════════════════════════════════════════
def _fig_one_end():
    with plt.rc_context(RC):
        fig, axes = plt.subplots(4, 1, figsize=(10, 7.5),
                                 gridspec_kw={'hspace': 0.70})
        fig.patch.set_facecolor(CBG)
        x = np.linspace(0, 1, 800)
        colors = [CB, CG, CP, CY]
        odd_ns = [1, 3, 5, 7]

        for idx, (ax, col, n) in enumerate(zip(axes, colors, odd_ns)):
            # y = sin((2n-1)πx/2) but using quarter-wave: y=sin(n_eff * π/2 * x/L)
            # For n-th odd harmonic: f_n = (2k-1)f1, k=1,2,3,4
            k  = idx + 1
            y  = np.sin((2*k - 1) * np.pi / 2 * x)

            ax.set_facecolor('#f8fafc')
            ax.fill_between(x,  y, 0, where=(y >= 0), color=col, alpha=0.18)
            ax.fill_between(x,  y, 0, where=(y <  0), color=col, alpha=0.09)
            ax.plot(x, y,  color=col, lw=2.8, solid_capstyle='round')
            ax.plot(x, -y, color=col, lw=1.0, ls='--', alpha=0.35)
            ax.axhline(0, color='#94a3b8', lw=0.8, ls=':')

            # Fixed end node (x=0)
            ax.plot(0, 0, 's', color=CDK, ms=10, zorder=7,
                    markeredgecolor='white', markeredgewidth=1.5)
            ax.text(0, -1.45, 'N', ha='center', fontsize=7.5,
                    color=CGR, fontweight='600')

            # Free end antinode (x=1)
            ax.plot(1, y[-1], 'D', color=col, ms=9, zorder=7,
                    markeredgecolor='white', markeredgewidth=1.4)
            ax.text(1.0, 1.45, 'AN', ha='center', fontsize=7.5,
                    color=col, fontweight='700')

            # Interior nodes
            n_nodes_interior = k - 1
            for i in range(1, k):
                xn = 2*i / (2*k - 1)
                ax.plot(xn, 0, 'o', color='#475569', ms=8, zorder=6,
                        markeredgecolor='white', markeredgewidth=1.4)
                ax.text(xn, -1.45, 'N', ha='center', fontsize=7.5,
                        color=CGR, fontweight='600')

            lam_str = f'λ = 4L/{2*k-1}' if k > 1 else 'λ = 4L'
            f_str   = f'f = {2*k-1}f₁' if k > 1 else 'f = f₁  (fundamental)'
            name    = (f'{2*k-1}th Harmonic' if k > 1 else '1st Harmonic (fundamental)')

            ax.set_xlim(-0.06, 1.30)
            ax.set_ylim(-1.7, 1.7)
            ax.axis('off')

            ax.text(1.05, 0.55, name,   fontsize=9, color=col, fontweight='800', va='center')
            ax.text(1.05, 0.10, f'  {lam_str}', fontsize=8.5, color=CDK, va='center')
            ax.text(1.05,-0.32, f'  {f_str}',   fontsize=8.5, color=CDK, va='center')
            ax.text(1.05,-0.72,
                    f'  Nodes: {k}  |  Antinodes: {k}',
                    fontsize=7.5, color=CGR, va='center')

            ax.annotate('', xy=(1, -1.30), xytext=(0, -1.30),
                        arrowprops=dict(arrowstyle='<->', color=CGR, lw=1.2))
            ax.text(0.5, -1.55, 'L', ha='center', fontsize=8.5,
                    color=CGR, fontweight='700')

            # Wall indicator
            ax.add_patch(FancyBboxPatch((-0.055, -0.5), 0.04, 1.0,
                                        boxstyle='square,pad=0',
                                        fc='#475569', ec='none', alpha=0.8))

        axes[0].set_title('Standing Waves — One End Fixed, One End Free  (Odd Harmonics Only)',
                          fontsize=11, fontweight='bold', color=CDK, pad=6)
        fig.tight_layout()
    return fig


# ═══════════════════════════════════════════════════════════════════════════════
#  FIGURE 4 — Wave speed on a string: effect of tension & density
# ═══════════════════════════════════════════════════════════════════════════════
def _fig_speed_table():
    with plt.rc_context(RC):
        fig, axes = plt.subplots(1, 2, figsize=(10, 3.8),
                                 gridspec_kw={'wspace': 0.40})
        fig.patch.set_facecolor(CBG)

        # Left: v vs T at fixed μ
        ax = axes[0]
        ax.set_facecolor('#f0f6ff')
        T_vals = np.linspace(0, 160, 300)
        mu = 0.01  # kg/m
        v  = np.sqrt(T_vals / mu)
        ax.plot(T_vals, v, color=CB, lw=2.6)
        ax.fill_between(T_vals, v, alpha=0.10, color=CB)
        ax.set_xlabel('Tension  T  (N)', fontsize=9.5, color=CDK)
        ax.set_ylabel('Wave speed  v  (m/s)', fontsize=9.5, color=CDK)
        ax.set_title(r'v vs T  (μ fixed)', fontsize=10, color=CB, fontweight='700')
        ax.spines[['top', 'right']].set_visible(False)
        ax.tick_params(labelsize=8.5)
        ax.set_xlim(0, 160); ax.set_ylim(0)
        # annotation
        ax.text(100, 60, r'$v = \sqrt{T/\mu}$',
                fontsize=13, color=CB, fontweight='700')
        ax.text(100, 30, 'v ∝ √T', fontsize=9.5, color=CGR)

        # Right: v vs μ at fixed T
        ax2 = axes[1]
        ax2.set_facecolor('#f0fdf4')
        mu_vals = np.linspace(0.001, 0.04, 300)
        T_fixed = 40.0  # N
        v2 = np.sqrt(T_fixed / mu_vals)
        ax2.plot(mu_vals * 1000, v2, color=CG, lw=2.6)
        ax2.fill_between(mu_vals * 1000, v2, alpha=0.10, color=CG)
        ax2.set_xlabel('Linear density  μ  (g/m)', fontsize=9.5, color=CDK)
        ax2.set_ylabel('Wave speed  v  (m/s)', fontsize=9.5, color=CDK)
        ax2.set_title(r'v vs μ  (T fixed)', fontsize=10, color=CG, fontweight='700')
        ax2.spines[['top', 'right']].set_visible(False)
        ax2.tick_params(labelsize=8.5)
        ax2.set_xlim(1, 40); ax2.set_ylim(0)
        ax2.text(22, 120, r'$v = \sqrt{T/\mu}$',
                 fontsize=13, color=CG, fontweight='700')
        ax2.text(22, 55, 'v ∝ 1/√μ', fontsize=9.5, color=CGR)

        fig.suptitle('Wave Speed on a String', fontsize=11,
                     fontweight='bold', color=CDK)
        fig.tight_layout()
    return fig


# ═══════════════════════════════════════════════════════════════════════════════
#  MAIN RENDER
# ═══════════════════════════════════════════════════════════════════════════════
def render_standing_waves():
    st.markdown(_CSS, unsafe_allow_html=True)

    # ── Hero ──────────────────────────────────────────────────────────────────
    st.markdown("""
<div class="hero">
  <h1>🎵 Standing Waves &amp; Resonance</h1>
  <p>From wave superposition to string harmonics and resonance conditions.<br>
     Physics · Grade 11 · Mechanical Waves</p>
  <div class="hero-meta">
    <span class="hero-tag">Standing Waves</span>
    <span class="hero-tag">Resonance</span>
    <span class="hero-tag">String Harmonics</span>
    <span class="hero-tag">Wave Speed</span>
  </div>
</div>
""", unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════════════
    # 01  What is a Standing Wave?
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown('<p class="sh"><span class="pill">01</span>What is a Standing Wave?</p>',
                unsafe_allow_html=True)

    c1, c2 = st.columns([1, 1], gap="large")
    with c1:
        st.markdown("""
<div class="card cb">
<h4>📖 Definition</h4>
<p>A <strong>standing wave</strong> is formed when two identical waves
travel in <strong>opposite directions</strong> through the same medium and superpose.</p>
<ul>
  <li>Same amplitude <em>A</em>, same frequency <em>f</em>, same wavelength <em>λ</em></li>
  <li>The wave pattern appears to <strong>stand still</strong> — it does not move left or right</li>
  <li>Certain points are always at rest (<strong>nodes</strong>),
      others oscillate with maximum amplitude (<strong>antinodes</strong>)</li>
</ul>
</div>
""", unsafe_allow_html=True)
    with c2:
        st.markdown("""
<div class="card cs">
<h4>⚡ Key Equation</h4>
<p>Superposing two travelling waves:</p>
</div>
""", unsafe_allow_html=True)
        st.latex(r"y_1 = A\sin(kx - \omega t)")
        st.latex(r"y_2 = A\sin(kx + \omega t)")
        st.markdown('<div class="card cg" style="margin-top:6px">'
                    '<h4>Result — Standing Wave</h4></div>',
                    unsafe_allow_html=True)
        st.latex(r"y = 2A\sin(kx)\cos(\omega t)")
        st.markdown("""
<div class="card cs" style="margin-top:6px">
<p><em>Space</em> part sin(kx) → fixes node/antinode positions<br>
   <em>Time</em> part cos(ωt) → whole string oscillates in phase</p>
</div>
""", unsafe_allow_html=True)

    _show("formation",
          "Top two rows: travelling waves moving in opposite directions  |  "
          "Bottom: resulting standing wave with envelope (dashed) and three time snapshots  |  "
          "N = node · AN = antinode")

    # ══════════════════════════════════════════════════════════════════════════
    # 02  Nodes & Antinodes
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown('<hr class="div"><p class="sh"><span class="pill">02</span>'
                'Nodes &amp; Antinodes</p>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1, 1, 1], gap="large")
    with c1:
        st.markdown("""
<div class="card cr">
<h4>❌ Node (N)</h4>
<ul>
  <li>Point of <strong>zero displacement</strong> at all times</li>
  <li>sin(kx) = 0  →  kx = nπ</li>
  <li>Position: x = nλ/2  (n = 0, 1, 2 …)</li>
  <li>Amplitude = <strong>0</strong></li>
</ul>
</div>
""", unsafe_allow_html=True)
    with c2:
        st.markdown("""
<div class="card cg">
<h4>✅ Antinode (AN)</h4>
<ul>
  <li>Point of <strong>maximum displacement</strong></li>
  <li>|sin(kx)| = 1  →  kx = (n − ½)π</li>
  <li>Position: x = (2n−1)λ/4</li>
  <li>Amplitude = <strong>2A</strong></li>
</ul>
</div>
""", unsafe_allow_html=True)
    with c3:
        st.markdown("""
<div class="card cb">
<h4>📏 Spacing Rules</h4>
<ul>
  <li>Adjacent nodes: <strong>λ/2</strong> apart</li>
  <li>Adjacent antinodes: <strong>λ/2</strong> apart</li>
  <li>Node → nearest antinode: <strong>λ/4</strong></li>
  <li># loops = # antinodes = harmonic number <em>n</em></li>
</ul>
</div>
""", unsafe_allow_html=True)

    st.markdown("""
<div class="keytip">
💡 <strong>Quick check:</strong>&nbsp;
If the distance between two adjacent nodes is measured as <em>d</em>,
then <strong>λ = 2d</strong>.
&nbsp;|&nbsp;
All points between two adjacent nodes oscillate <strong>in phase</strong>
with each other but <strong>out of phase</strong> with the next segment.
</div>
""", unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════════════
    # 03  Both Ends Fixed
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown('<hr class="div"><p class="sh"><span class="pill">03</span>'
                'String Fixed at Both Ends — Harmonics</p>',
                unsafe_allow_html=True)

    c1, c2 = st.columns([1.6, 1], gap="large")
    with c1:
        _show("harmonics",
              "■ = fixed node (wall)  ◆ = antinode  ○ = interior node  "
              "| Dashed line = mirror image of the wave")
    with c2:
        st.markdown("""
<div class="card cb">
<h4>🔒 Boundary Condition</h4>
<p>Both ends are <strong>fixed → nodes</strong> at x = 0 and x = L.</p>
</div>
""", unsafe_allow_html=True)
        st.latex(r"L = n\,\frac{\lambda}{2} \quad n = 1, 2, 3, \ldots")
        st.markdown("""
<div class="card cg" style="margin-top:10px">
<h4>Allowed Wavelengths</h4>
</div>
""", unsafe_allow_html=True)
        st.latex(r"\lambda_n = \frac{2L}{n}")
        st.markdown("""
<div class="card cp" style="margin-top:10px">
<h4>Resonant Frequencies</h4>
</div>
""", unsafe_allow_html=True)
        st.latex(r"f_n = n\,\frac{v}{2L} = n\,f_1")
        st.markdown("""
<div class="card cs" style="margin-top:10px">
<p>
<strong>f₁</strong> = fundamental (1st harmonic)<br>
<strong>f₂ = 2f₁</strong> = 1st overtone (2nd harmonic)<br>
<strong>f₃ = 3f₁</strong> = 2nd overtone (3rd harmonic)<br>
<em>All harmonics</em> (odd + even) are present.
</p>
</div>
""", unsafe_allow_html=True)

    st.markdown("""
<table class="rt">
<thead><tr>
  <th>Harmonic n</th>
  <th>Name</th>
  <th>Loops</th>
  <th>Nodes</th>
  <th>Antinodes</th>
  <th>λ</th>
  <th>f</th>
</tr></thead>
<tbody>
<tr><td>1</td><td>Fundamental</td><td>1</td><td>2</td><td>1</td>
    <td>2L</td><td class="tg">f₁</td></tr>
<tr><td>2</td><td>1st Overtone</td><td>2</td><td>3</td><td>2</td>
    <td>L</td><td class="tg">2f₁</td></tr>
<tr><td>3</td><td>2nd Overtone</td><td>3</td><td>4</td><td>3</td>
    <td>2L/3</td><td class="tg">3f₁</td></tr>
<tr><td>4</td><td>3rd Overtone</td><td>4</td><td>5</td><td>4</td>
    <td>L/2</td><td class="tg">4f₁</td></tr>
<tr><td>n</td><td>—</td><td>n</td><td>n+1</td><td>n</td>
    <td>2L/n</td><td class="tg">nf₁</td></tr>
</tbody>
</table>
""", unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════════════
    # 04  One End Fixed
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown('<hr class="div"><p class="sh"><span class="pill">04</span>'
                'String Fixed at One End, Free at the Other</p>',
                unsafe_allow_html=True)

    c1, c2 = st.columns([1.6, 1], gap="large")
    with c1:
        _show("one_end",
              "■ = fixed node (wall)  ◆ = free antinode  ○ = interior node  "
              "| Only odd harmonics exist")
    with c2:
        st.markdown("""
<div class="card cr">
<h4>🔒🔓 Boundary Condition</h4>
<p>Fixed end → <strong>node</strong>.&nbsp;
Free end → <strong>antinode</strong>.</p>
</div>
""", unsafe_allow_html=True)
        st.latex(r"L = (2n-1)\,\frac{\lambda}{4} \quad n = 1, 2, 3, \ldots")
        st.markdown("""
<div class="card cy" style="margin-top:10px">
<h4>Allowed Wavelengths</h4>
</div>
""", unsafe_allow_html=True)
        st.latex(r"\lambda_n = \frac{4L}{2n-1}")
        st.markdown("""
<div class="card cp" style="margin-top:10px">
<h4>Resonant Frequencies</h4>
</div>
""", unsafe_allow_html=True)
        st.latex(r"f_n = (2n-1)\,\frac{v}{4L} = (2n-1)\,f_1")
        st.markdown("""
<div class="card cs" style="margin-top:10px">
<p>
Only <strong>odd harmonics</strong> exist: f₁, 3f₁, 5f₁, 7f₁ …<br>
Even harmonics are <em>absent</em>.
</p>
</div>
""", unsafe_allow_html=True)

    st.markdown("""
<table class="rt">
<thead><tr>
  <th>n</th>
  <th>Harmonic</th>
  <th>Nodes</th>
  <th>Antinodes</th>
  <th>λ</th>
  <th>f</th>
</tr></thead>
<tbody>
<tr><td>1</td><td>1st (fundamental)</td><td>1</td><td>1</td>
    <td>4L</td><td class="tg">f₁</td></tr>
<tr><td>2</td><td>3rd</td><td>2</td><td>2</td>
    <td>4L/3</td><td class="tg">3f₁</td></tr>
<tr><td>3</td><td>5th</td><td>3</td><td>3</td>
    <td>4L/5</td><td class="tg">5f₁</td></tr>
<tr><td>4</td><td>7th</td><td>4</td><td>4</td>
    <td>4L/7</td><td class="tg">7f₁</td></tr>
<tr><td>n</td><td>(2n−1)th</td><td>n</td><td>n</td>
    <td>4L/(2n−1)</td><td class="tg">(2n−1)f₁</td></tr>
</tbody>
</table>
""", unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════════════
    # 05  Wave speed on a string
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown('<hr class="div"><p class="sh"><span class="pill">05</span>'
                'Wave Speed on a String</p>', unsafe_allow_html=True)

    c1, c2 = st.columns([1, 1.4], gap="large")
    with c1:
        st.markdown("""
<div class="card cb">
<h4>📐 Formula</h4>
</div>
""", unsafe_allow_html=True)
        st.latex(r"v = \sqrt{\frac{T}{\mu}}")
        st.markdown("""
<div class="card cs" style="margin-top:10px">
<h4>Variables</h4>
<ul>
  <li><strong>v</strong> — wave speed (m/s)</li>
  <li><strong>T</strong> — tension in the string (N)</li>
  <li><strong>μ</strong> — linear mass density (kg/m)
      = mass ÷ length = m/L</li>
</ul>
</div>
<div class="card cy" style="margin-top:10px">
<h4>Proportionality</h4>
<ul>
  <li>v ∝ √T &nbsp;(double T → v increases by √2)</li>
  <li>v ∝ 1/√μ &nbsp;(heavier string → slower wave)</li>
</ul>
</div>
""", unsafe_allow_html=True)
    with c2:
        _show("speed_table",
              "Left: wave speed increases with tension (fixed μ)  |  "
              "Right: wave speed decreases with linear density (fixed T)")

    # ══════════════════════════════════════════════════════════════════════════
    # 06  Resonance
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown('<hr class="div"><p class="sh"><span class="pill">06</span>'
                'Resonance</p>', unsafe_allow_html=True)

    c1, c2 = st.columns([1, 1], gap="large")
    with c1:
        st.markdown("""
<div class="card cg">
<h4>🎯 Definition</h4>
<p><strong>Resonance</strong> occurs when the driving frequency matches
one of the system's <strong>natural (resonant) frequencies</strong>.</p>
<ul>
  <li>Energy transfer from driver to string is maximised</li>
  <li>Amplitude of oscillation grows to a large value</li>
  <li>A clear, stable standing wave pattern appears</li>
</ul>
</div>
""", unsafe_allow_html=True)
        st.markdown("""
<div class="card cb" style="margin-top:10px">
<h4>⚙️ Condition</h4>
</div>
""", unsafe_allow_html=True)
        st.latex(r"f_{\text{drive}} = f_n = n\,\frac{v}{2L}")
        st.markdown("""
<div class="card cs" style="margin-top:10px">
<p>Equivalently: the string length must be an exact
<strong>integer number of half-wavelengths</strong>:</p>
</div>
""", unsafe_allow_html=True)
        st.latex(r"L = n\,\frac{\lambda}{2}")
    with c2:
        st.markdown("""
<div class="card cy">
<h4>🔢 Identifying the Harmonic from a Problem</h4>
<ul>
  <li>Given f and v → find n: &nbsp;<strong>n = 2Lf / v</strong></li>
  <li>If n is an integer → resonance is occurring</li>
  <li>n = 1 → fundamental; n = 2 → 1st overtone …</li>
</ul>
</div>
<div class="card cp" style="margin-top:10px">
<h4>💡 Worked Example</h4>
<p>String: L = 1.25 m, v = 160 m/s<br>
What frequencies produce resonance?</p>
<ul>
  <li>f₁ = v / 2L = 160 / 2.5 = <strong>64 Hz</strong></li>
  <li>f₂ = 2 × 64 = <strong>128 Hz</strong></li>
  <li>f₃ = 3 × 64 = <strong>192 Hz</strong></li>
  <li>fₙ = n × 64 Hz &nbsp;(n = 1, 2, 3 …)</li>
</ul>
</div>
""", unsafe_allow_html=True)

    st.markdown("""
<div class="keytip">
💡 <strong>Exam tip:</strong>&nbsp;
When a problem says "resonance occurs in the n<sup>th</sup> mode",
it means n loops (both-ends fixed) or the (2n−1)<sup>th</sup> harmonic (one-end fixed).
&nbsp;—&nbsp;
Always draw the wave shape first to count loops!
</div>
""", unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════════════
    # REF  Formula Reference Table
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown('<hr class="div"><p class="sh"><span class="pill">REF</span>'
                'Formula Reference</p>', unsafe_allow_html=True)

    st.markdown("""
<table class="rt">
<thead><tr>
  <th>Quantity</th>
  <th>Both Ends Fixed</th>
  <th>One End Fixed</th>
</tr></thead>
<tbody>
<tr>
  <td><strong>Boundary</strong></td>
  <td>Node — Node</td>
  <td>Node — Antinode</td>
</tr>
<tr>
  <td><strong>Length condition</strong></td>
  <td class="tg">L = nλ/2</td>
  <td class="tg">L = (2n−1)λ/4</td>
</tr>
<tr>
  <td><strong>Allowed λ</strong></td>
  <td>λₙ = 2L/n</td>
  <td>λₙ = 4L/(2n−1)</td>
</tr>
<tr>
  <td><strong>Resonant f</strong></td>
  <td>fₙ = nv/2L = nf₁</td>
  <td>fₙ = (2n−1)v/4L = (2n−1)f₁</td>
</tr>
<tr>
  <td><strong>Harmonics present</strong></td>
  <td>All: 1st, 2nd, 3rd …</td>
  <td>Odd only: 1st, 3rd, 5th …</td>
</tr>
<tr>
  <td><strong>Nodes (both ends)</strong></td>
  <td>n + 1</td>
  <td>n</td>
</tr>
<tr>
  <td><strong>Antinodes</strong></td>
  <td>n</td>
  <td>n</td>
</tr>
<tr>
  <td><strong>Wave speed</strong></td>
  <td colspan="2">v = √(T/μ) &nbsp;—&nbsp; v = fλ</td>
</tr>
<tr>
  <td><strong>Node spacing</strong></td>
  <td colspan="2">λ/2 &nbsp;between adjacent nodes</td>
</tr>
</tbody>
</table>
""", unsafe_allow_html=True)

    st.markdown("""
<div class="keytip" style="margin-top:16px">
💡 <strong>Remember:</strong>&nbsp;
<strong>v = fλ</strong> always holds.&nbsp;
Frequency does <em>not</em> change when a wave crosses a boundary —
only v and λ change.&nbsp;
Increasing tension → higher v → higher f for the same string length.
</div>
""", unsafe_allow_html=True)
