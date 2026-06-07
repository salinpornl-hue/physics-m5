"""
summary_diffraction.py — Single-Slit & Double-Slit Diffraction summary
"""
import io as _io
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Arc, Rectangle, FancyArrowPatch
import streamlit as st

# ── helpers ───────────────────────────────────────────────────────────────────
def _png(fig, dpi=145) -> bytes:
    buf = _io.BytesIO()
    fig.savefig(buf, format="png", dpi=dpi, bbox_inches="tight",
                facecolor=fig.get_facecolor())
    buf.seek(0)
    plt.close(fig)
    return buf.getvalue()

# ── palette ───────────────────────────────────────────────────────────────────
CB   = '#2563eb'
CG   = '#16a34a'
CR   = '#dc2626'
CY   = '#d97706'
CP   = '#7c3aed'
CGR  = '#64748b'
CDK  = '#0f172a'
CBG  = '#f8fafc'
CBGL = '#eff6ff'

RC = {
    'font.family': 'DejaVu Sans',
    'axes.unicode_minus': False,
    'text.color': CDK,
}

# ── CSS ───────────────────────────────────────────────────────────────────────
_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');

.dif-wrap { font-family:'Inter',sans-serif; color:#0f172a; }

.hero-dif {
  background: linear-gradient(135deg, #0f172a 0%, #1e3a5f 50%, #1d4ed8 100%);
  border-radius:16px; padding:32px 28px 24px; color:#fff; margin-bottom:24px;
}
.hero-dif h1 { font-size:1.85rem; font-weight:800; margin:0 0 6px; }
.hero-dif p  { font-size:.95rem; opacity:.85; margin:0; }

.dif-h2 {
  font-size:1.05rem; font-weight:700; color:#1e40af;
  border-left:4px solid #2563eb; padding-left:10px;
  margin:24px 0 12px;
}

.dif-card {
  background:#fff; border:1px solid #e2e8f0; border-radius:12px;
  padding:18px 20px 14px; margin-bottom:14px;
  box-shadow:0 1px 4px rgba(0,0,0,.05);
}
.dif-card-title {
  font-size:.82rem; font-weight:700; text-transform:uppercase;
  letter-spacing:.06em; color:#64748b; margin-bottom:10px;
}

.dif-formula {
  background:#f1f5f9; border-left:4px solid #2563eb;
  border-radius:0 8px 8px 0; padding:11px 18px;
  font-size:1.08rem; font-weight:700; color:#1e3a8a;
  margin:8px 0; font-family:'Courier New',monospace;
}
.dif-formula2 {
  background:#fdf4ff; border-left:4px solid #7c3aed;
  border-radius:0 8px 8px 0; padding:11px 18px;
  font-size:1.08rem; font-weight:700; color:#5b21b6;
  margin:8px 0; font-family:'Courier New',monospace;
}

.dif-grid  { display:grid; grid-template-columns:1fr 1fr; gap:14px; }
.dif-grid3 { display:grid; grid-template-columns:1fr 1fr 1fr; gap:12px; }

.dif-info {
  background:#f8fafc; border:1px solid #e2e8f0; border-radius:9px;
  padding:12px 15px; font-size:.84rem; line-height:1.75;
}

.dif-hl   { background:#eff6ff; border:1.5px solid #93c5fd; border-radius:9px;
            padding:11px 16px; margin:8px 0; font-size:.87rem; line-height:1.8; }
.dif-hl-g { background:#f0fdf4; border-color:#86efac; }
.dif-hl-r { background:#fff5f5; border-color:#fca5a5; }
.dif-hl-p { background:#f5f3ff; border-color:#c4b5fd; }
.dif-hl-y { background:#fffbeb; border-color:#fcd34d; }

.dif-tag  { display:inline-block; font-size:.72rem; font-weight:700;
            border-radius:6px; padding:2px 9px; margin:2px 4px 2px 0; }
.tag-blue { background:#dbeafe; color:#1d4ed8; }
.tag-red  { background:#fee2e2; color:#b91c1c; }
.tag-green{ background:#dcfce7; color:#15803d; }
.tag-purp { background:#ede9fe; color:#6d28d9; }
.tag-amb  { background:#fef3c7; color:#92400e; }

.dif-step {
  display:flex; align-items:flex-start; gap:12px;
  background:#f8fafc; border-radius:9px; padding:10px 14px;
  margin:7px 0; font-size:.86rem; line-height:1.7;
}
.dif-step-num {
  background:#2563eb; color:#fff; border-radius:50%;
  min-width:26px; height:26px; display:flex;
  align-items:center; justify-content:center;
  font-weight:800; font-size:.85rem; flex-shrink:0;
}

.ref-table { width:100%; border-collapse:collapse; font-size:.83rem; margin-top:8px; }
.ref-table th {
  background:#1e3a8a; color:#fff; padding:8px 12px;
  text-align:left; font-weight:700;
}
.ref-table td { padding:7px 12px; border-bottom:1px solid #e2e8f0; }
.ref-table tr:nth-child(even) td { background:#f8fafc; }
.ref-table code { font-family:'Courier New',monospace; font-weight:700;
                  color:#1d4ed8; font-size:.92rem; }
</style>
"""


# ═══════════════════════════════════════════════════════════════════════════════
#  FIGURE 1 — Experiment setup (2 panels: full setup + path difference)
# ═══════════════════════════════════════════════════════════════════════════════
@st.cache_data
def _fig_setup():
    with plt.rc_context(RC):
        fig, axes = plt.subplots(1, 2, figsize=(13, 5.4),
                                 gridspec_kw={'width_ratios': [3, 2]})
        fig.patch.set_facecolor(CBG)
        fig.subplots_adjust(left=0.01, right=0.99, top=0.90, bottom=0.06, wspace=0.06)

        # ── LEFT: full experiment setup ───────────────────────────────────────
        ax = axes[0]
        ax.set_facecolor(CBGL)
        ax.axis('off')

        a = 3.0; lam = 1.0
        X_SC = 8.5; Y_MAX = 4.0; X_MIN = -3.8
        ax.set_xlim(X_MIN, X_SC + 2.6)
        ax.set_ylim(-Y_MAX - 0.2, Y_MAX + 0.5)

        # incoming wavefronts
        for xi in np.arange(X_MIN + 0.3, -0.35, 0.9):
            ax.plot([xi, xi], [-Y_MAX, -a/2 - 0.18], color=CB, lw=0.9, alpha=0.30)
            ax.plot([xi, xi], [ a/2 + 0.18,  Y_MAX], color=CB, lw=0.9, alpha=0.30)
        ax.annotate('', xy=(-0.7, 0), xytext=(-2.3, 0),
                    arrowprops=dict(arrowstyle='->', color=CB, lw=2.2, mutation_scale=18))
        ax.text(X_MIN + 0.2, 0.65, 'Plane wave →', color=CB, fontsize=8.5, fontweight='700')

        # barrier
        bw = 0.22
        for y0, y1 in [(-Y_MAX - 0.2, -a/2), (a/2, Y_MAX + 0.2)]:
            ax.add_patch(Rectangle((-bw, y0), 2*bw, y1 - y0,
                                   fc='#334155', ec='none', zorder=6))
        ax.text(-bw - 0.12, -Y_MAX + 0.05, 'Barrier', color='#334155',
                fontsize=7.5, ha='right', va='bottom', fontweight='700')

        # slit edges
        ax.plot(0,  a/2, 'D', color=CB, ms=9, zorder=10,
                markeredgecolor='white', markeredgewidth=1.6)
        ax.plot(0, -a/2, 'D', color=CB, ms=9, zorder=10,
                markeredgecolor='white', markeredgewidth=1.6)

        # slit width annotation
        ax.annotate('', xy=(-1.3, a/2), xytext=(-1.3, -a/2),
                    arrowprops=dict(arrowstyle='<->', color=CDK, lw=1.5,
                                   mutation_scale=10))
        ax.text(-1.65, 0, 'a', fontsize=15, color=CDK,
                ha='center', va='center', fontweight='bold')

        # screen
        ax.plot([X_SC]*2, [-Y_MAX, Y_MAX], color='#1e293b', lw=4.5, zorder=6,
                solid_capstyle='round')
        ax.text(X_SC + 0.12, Y_MAX + 0.2, 'Screen', color='#1e293b',
                fontsize=8.5, fontweight='700', va='top')

        # intensity bars on screen
        theta_arr = np.linspace(-88, 88, 2000) * np.pi / 180
        sin_arr   = np.sin(theta_arr)
        beta      = np.pi * a * sin_arr / lam
        I_arr     = np.where(np.abs(beta) < 1e-10, 1.0, (np.sin(beta)/beta)**2)
        y_arr     = X_SC * np.tan(theta_arr)
        for i in range(len(theta_arr) - 1):
            y1s, y2s = y_arr[i], y_arr[i+1]
            if max(abs(y1s), abs(y2s)) > Y_MAX - 0.08:
                continue
            Iavg = (I_arr[i] + I_arr[i+1]) / 2
            if Iavg < 0.008:
                continue
            g = Iavg ** 0.55
            ax.fill_between([X_SC + 0.06, X_SC + 0.42],
                            [y1s, y1s], [y2s, y2s],
                            color=(g, g*0.95, 0.25*g), alpha=0.95, linewidth=0, zorder=5)

        # dark fringe rays
        for n in range(1, int(a/lam) + 1):
            sin_n = n * lam / a
            if sin_n >= 1.0:
                break
            th = np.arcsin(sin_n)
            for sgn in [1, -1]:
                ye = X_SC * np.tan(sgn * th)
                if abs(ye) > Y_MAX:
                    continue
                ax.plot([0, X_SC], [0, ye], color=CR, lw=1.3, ls='--',
                        alpha=0.75, zorder=4)
                ax.plot(X_SC, ye, 'x', color=CR, ms=8,
                        markeredgewidth=2.2, zorder=7)
                if sgn > 0:
                    ax.text(X_SC + 0.55, ye, f'N{n}', color=CR,
                            fontsize=9, va='center', fontweight='800')

        # central max ray
        ax.plot([0, X_SC], [0, 0], color=CG, lw=2.4, alpha=0.88, zorder=4)
        ax.plot(X_SC, 0, 'o', color=CG, ms=11, zorder=8,
                markeredgecolor='white', markeredgewidth=2)
        ax.text(X_SC + 0.55, 0.42, 'A₀', color=CG, fontsize=10.5,
                fontweight='900', va='center')

        # θ₁ arc
        th1 = np.arcsin(lam / a)
        ax.add_patch(Arc((0, 0), 3.0, 3.0, angle=0, theta1=0,
                         theta2=np.degrees(th1), color=CP, lw=2.2, zorder=7))
        ax.text(1.75, 0.44, 'θ₁', fontsize=12, color=CP, fontweight='bold')

        # L distance
        yL = -Y_MAX + 0.25
        ax.annotate('', xy=(X_SC, yL), xytext=(0, yL),
                    arrowprops=dict(arrowstyle='<->', color=CGR, lw=1.2,
                                   mutation_scale=9))
        ax.text(X_SC/2, yL - 0.5, 'L  (slit-to-screen distance)',
                ha='center', fontsize=8, color=CGR)

        ax.set_title('Experiment setup — a = 3λ → n_max = 3 → 6 dark fringes',
                     fontsize=10, color=CDK, fontweight='700', pad=5)

        # ── RIGHT: path difference geometry ──────────────────────────────────
        ax2 = axes[1]
        ax2.set_facecolor('#fffbeb')
        ax2.axis('off')
        ax2.set_xlim(-2.2, 8.0)
        ax2.set_ylim(-4.8, 4.8)

        slit_h = 2.5      # half-slit height in display coords
        theta_pd = np.arcsin(0.5)   # sinθ = 0.5, nice round example

        # slit visual
        ax2.plot([0, 0], [-slit_h, slit_h], color='#334155', lw=4.5, zorder=5,
                 solid_capstyle='round')
        ax2.plot(0,  slit_h, 'D', color=CB, ms=10, zorder=8,
                 markeredgecolor='white', markeredgewidth=1.8)
        ax2.plot(0, -slit_h, 'D', color=CB, ms=10, zorder=8,
                 markeredgecolor='white', markeredgewidth=1.8)
        ax2.plot(0, 0, 's', color=CP, ms=8, zorder=8,
                 markeredgecolor='white', markeredgewidth=1.4)

        ax2.text(-0.35,  slit_h, '+a/2\n(top)', color=CB, fontsize=8,
                 ha='right', va='center')
        ax2.text(-0.35,  0,      'centre', color=CP, fontsize=8,
                 ha='right', va='center')
        ax2.text(-0.35, -slit_h, '−a/2\n(bot)', color=CB, fontsize=8,
                 ha='right', va='center')

        # width brace
        ax2.annotate('', xy=(-1.5, slit_h), xytext=(-1.5, -slit_h),
                     arrowprops=dict(arrowstyle='<->', color=CDK, lw=1.5,
                                    mutation_scale=9))
        ax2.text(-1.9, 0, 'a', fontsize=15, color=CDK,
                 ha='center', va='center', fontweight='bold')

        # parallel rays at angle θ (far-field)
        ray_len = 6.2
        dx = ray_len * np.cos(theta_pd)
        dy = ray_len * np.sin(theta_pd)

        for y_start, col, lw in [(slit_h, CR, 2.0), (-slit_h, CR, 2.0), (0, CG, 1.5)]:
            ax2.annotate('', xy=(dx, y_start + dy), xytext=(0, y_start),
                         arrowprops=dict(arrowstyle='->', color=col, lw=lw,
                                         mutation_scale=13,
                                         alpha=0.9 if col == CR else 0.55))

        # path-difference construction
        P_top = np.array([0.0, slit_h])
        P_bot = np.array([0.0, -slit_h])
        ray_dir = np.array([np.cos(theta_pd), np.sin(theta_pd)])
        t_foot  = np.dot(P_top - P_bot, ray_dir)
        foot    = P_bot + t_foot * ray_dir

        # perpendicular dashed line
        ax2.plot([P_top[0], foot[0]], [P_top[1], foot[1]],
                 color=CY, lw=2.2, ls=':', zorder=6)

        # Δr arrow along bottom ray from origin to foot
        ax2.annotate('', xy=tuple(foot), xytext=tuple(P_bot),
                     arrowprops=dict(arrowstyle='<->', color=CY, lw=2.2,
                                     mutation_scale=10))
        mid = (P_bot + foot) / 2
        ax2.text(mid[0] + 0.25, mid[1] - 0.6,
                 'Δr = a · sinθ', color=CY, fontsize=10,
                 fontweight='800', ha='left')

        # right-angle mark at foot
        eps = 0.22
        perp = np.array([-ray_dir[1], ray_dir[0]])
        c1 = foot + eps * perp
        c2 = foot + eps * perp - eps * ray_dir
        c3 = foot - eps * ray_dir
        ax2.plot([c1[0], c2[0], c3[0]], [c1[1], c2[1], c3[1]],
                 color=CY, lw=1.2, zorder=6)

        # θ arc
        arc_r = 1.7
        ax2.add_patch(Arc((0, -slit_h), arc_r*2, arc_r*2, angle=0,
                          theta1=0, theta2=np.degrees(theta_pd),
                          color=CP, lw=2.2, zorder=7))
        ax2.text(1.5, -slit_h + 0.6, 'θ', fontsize=14, color=CP, fontweight='bold')

        # condition box
        ax2.text(4.1, -3.5,
                 'Dark fringe:\na · sinθ = nλ\n(destructive)\nn = 1, 2, 3, …',
                 fontsize=10, color=CR, fontweight='800', ha='center', va='center',
                 bbox=dict(boxstyle='round,pad=0.55', fc='#fff5f5', ec=CR, lw=2.0))

        ax2.set_title('Path difference — why dark fringes form',
                      fontsize=10, color=CDK, fontweight='700', pad=5)

        return _png(fig)


# ═══════════════════════════════════════════════════════════════════════════════
#  FIGURE 2 — sinc² Intensity Pattern
# ═══════════════════════════════════════════════════════════════════════════════
@st.cache_data
def _fig_intensity(a_lam: float = 3.0):
    """Two-row: fringe bar image (top) + sinc² curve with labels (bottom)."""
    nmax = int(a_lam)
    with plt.rc_context(RC):
        fig = plt.figure(figsize=(12, 6.5), facecolor=CBG)
        fig.patch.set_facecolor(CBG)
        gs = fig.add_gridspec(2, 1, height_ratios=[0.75, 3.5], hspace=0.04,
                              left=0.07, right=0.97, top=0.90, bottom=0.11)
        ax_bar = fig.add_subplot(gs[0])
        ax_int = fig.add_subplot(gs[1], sharex=ax_bar)

        # compute sinc²
        theta_deg = np.linspace(-88, 88, 8000)
        sin_t = np.sin(np.radians(theta_deg))
        beta  = np.pi * a_lam * sin_t
        I     = np.where(np.abs(beta) < 1e-10, 1.0, (np.sin(beta)/beta)**2)

        # ── top: visual fringe bars ───────────────────────────────────────────
        ax_bar.set_facecolor('#0a0a14')
        for i in range(len(theta_deg) - 1):
            Iavg = (I[i] + I[i+1]) / 2
            if Iavg < 0.006:
                continue
            x1, x2 = theta_deg[i], theta_deg[i+1]
            g = Iavg ** 0.5
            ax_bar.fill_between([x1, x2], [0]*2, [1]*2,
                                color=(g, g*0.97, g*0.25), linewidth=0)
        ax_bar.set_xlim(-82, 82)
        ax_bar.set_ylim(0, 1)
        ax_bar.axis('off')
        ax_bar.text(0.005, 0.5, 'Screen pattern →', color='white', fontsize=8.5,
                    ha='left', va='center', transform=ax_bar.transAxes, fontweight='600')

        # ── bottom: sinc² curve ───────────────────────────────────────────────
        ax_int.set_facecolor(CBG)
        ax_int.plot(theta_deg, I, color=CB, lw=2.3, zorder=5)
        ax_int.fill_between(theta_deg, I, 0, alpha=0.10, color=CB, zorder=4)
        ax_int.set_xlim(-82, 82)
        ax_int.set_ylim(-0.12, 1.22)

        for spine in ['top', 'right']:
            ax_int.spines[spine].set_visible(False)
        for spine in ['left', 'bottom']:
            ax_int.spines[spine].set_color('#cbd5e1')
        ax_int.tick_params(colors=CGR, labelsize=9)
        ax_int.set_xlabel('Angle  θ  (degrees)', fontsize=10, color=CGR, labelpad=4)
        ax_int.set_ylabel('Relative Intensity', fontsize=10, color=CGR)

        # dark fringes
        for n in range(1, nmax + 1):
            sin_n = n / a_lam
            if sin_n >= 1.0:
                break
            th_deg_n = np.degrees(np.arcsin(sin_n))
            for sgn in [1, -1]:
                xn = sgn * th_deg_n
                ax_int.axvline(xn, color=CR, lw=1.1, ls='--', alpha=0.55, zorder=3)
                ax_int.plot(xn, 0, 'v', color=CR, ms=9, zorder=8,
                            markeredgecolor='white', markeredgewidth=1.3)
                if sgn > 0:
                    ax_int.text(xn, -0.095, f'N{n}\n{th_deg_n:.1f}°',
                                color=CR, fontsize=7.5, ha='center', fontweight='700')

        # central max
        ax_int.plot(0, 1.0, 'o', color=CG, ms=12, zorder=9,
                    markeredgecolor='white', markeredgewidth=2)
        ax_int.text(0, 1.10, 'A₀  (Central maximum — brightest & widest)',
                    ha='center', fontsize=9, color=CG, fontweight='800')

        # side maxima
        for n in range(1, nmax + 1):
            sin_am = (n + 0.5) / a_lam
            if sin_am >= 1.0:
                break
            th_am = np.degrees(np.arcsin(sin_am))
            for sgn in [1, -1]:
                region = (theta_deg > sgn*th_am - 6) & (theta_deg < sgn*th_am + 6)
                if not region.any():
                    continue
                pk = np.argmax(I[region])
                pk_x = theta_deg[region][pk]
                pk_I = I[region][pk]
                ax_int.plot(pk_x, pk_I, 'o', color=CG, ms=8, zorder=8,
                            markeredgecolor='white', markeredgewidth=1.5)
                if sgn > 0:
                    ax_int.text(pk_x + 0.5, pk_I + 0.04,
                                f'A{n}\n({pk_I*100:.0f}%)',
                                ha='left', fontsize=7.5, color=CG, fontweight='700')

        # formula
        ax_int.text(0.99, 0.97,
                    'I(θ) = I₀ · [ sin(πa sinθ/λ) / (πa sinθ/λ) ]²',
                    transform=ax_int.transAxes, ha='right', va='top',
                    fontsize=8.5, color=CDK, style='italic',
                    bbox=dict(boxstyle='round,pad=0.4', fc='white',
                              ec='#e2e8f0', lw=1.2))

        fig.suptitle(
            f'Intensity Pattern — a = {a_lam:.4g}λ   →   n_max = {nmax}   →'
            f'   {2*nmax} dark fringes  |  {2*nmax+1} bright fringes',
            fontsize=10.5, color=CDK, fontweight='800', y=0.945)

        return _png(fig)


# ═══════════════════════════════════════════════════════════════════════════════
#  MAIN RENDER
# ═══════════════════════════════════════════════════════════════════════════════
def render_diffraction():
    st.markdown(_CSS, unsafe_allow_html=True)
    st.markdown('<div class="dif-wrap">', unsafe_allow_html=True)

    # ── Hero ─────────────────────────────────────────────────────────────────
    st.markdown("""
    <div class="hero-dif">
      <h1>🌊 Diffraction — Single-Slit &amp; Double-Slit</h1>
      <p>
        When a wave squeezes through a narrow slit it <b>bends and spreads</b>,
        creating a pattern of bright and dark bands on a screen. This happens because
        every point inside the slit acts as a new wave source (Huygens' principle)
        and those secondary waves <b>interfere</b> with each other.
      </p>
    </div>
    """, unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════════════
    # 01 — Key condition
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown('<div class="dif-h2">01 — When Does Diffraction Matter?</div>',
                unsafe_allow_html=True)
    st.markdown("""
    <div class="dif-card">
      <div class="dif-grid">
        <div class="dif-info">
          <b>Condition for strong diffraction</b><br><br>
          <span class="dif-tag tag-blue">slit width a ≈ λ</span><br><br>
          • a ≫ λ → nearly no bending (ray-like, geometric shadow)<br>
          • a ≈ λ → strong bending, wide central maximum<br>
          • a ≪ λ → almost circular spreading (point-source like)
        </div>
        <div class="dif-info">
          <b>Huygens' Principle (the why)</b><br><br>
          Every point on a wavefront is a new point source of spherical waves.
          The slit lets through a strip → each sub-source radiates outward →
          secondary waves <b>add constructively in some directions</b>
          and <b>cancel in others</b>, producing the pattern.<br><br>
          <span class="dif-tag tag-purp">Diffraction</span>
          <span class="dif-tag tag-blue">Interference</span> — two sides of the same phenomenon.
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════════════
    # 02 — Setup & Formula
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown('<div class="dif-h2">02 — Setup, Geometry &amp; the Dark-Fringe Formula</div>',
                unsafe_allow_html=True)

    st.markdown("""
    <div class="dif-card">
      <div class="dif-card-title">Key formula — dark fringe (node) condition</div>
      <div class="dif-formula">a · sinθ = n · λ &emsp;&emsp; n = ±1, ±2, ±3, …</div>
      <div class="dif-grid" style="margin-top:12px">
        <div class="dif-hl">
          <b>Variables</b><br>
          <b>a</b> = slit width<br>
          <b>θ</b> = angle from central axis to the dark fringe<br>
          <b>λ</b> = wavelength<br>
          <b>n</b> = order number (1 = 1st dark fringe, 2 = 2nd, …)
        </div>
        <div class="dif-hl dif-hl-r">
          ⚠️ <b>Common trap — n = 0 is NOT dark</b><br><br>
          The centre (θ = 0) is always the <b>bright</b> central maximum A₀.<br>
          Dark fringes only exist for <b>n = ±1, ±2, ±3, …</b><br><br>
          Reason: when θ = 0, all path differences = 0 → perfect constructive.
        </div>
      </div>
      <div class="dif-hl dif-hl-y" style="margin-top:10px">
        <b>Why does a·sinθ = nλ give darkness?</b> &ensp;
        Split the slit into 2 halves. Every point in the top half pairs with a
        point in the bottom half, separated by a/2. When the path difference
        between each pair = λ/2 (i.e. a/2·sinθ = λ/2 → a·sinθ = λ),
        every pair cancels → total darkness. Same logic repeated gives n = 2, 3, …
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.image(_io.BytesIO(_fig_setup()), use_container_width=True)

    # ══════════════════════════════════════════════════════════════════════════
    # 03 — Intensity pattern
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown('<div class="dif-h2">03 — Intensity Pattern (sinc² shape)</div>',
                unsafe_allow_html=True)
    st.markdown("""
    <div class="dif-card">
      <div class="dif-grid">
        <div class="dif-info">
          <b>Central maximum A₀</b><br>
          • Always at θ = 0<br>
          • Widest and <b>brightest</b> (I = I₀)<br>
          • Width between N₁ each side = 2·arcsin(λ/a)
        </div>
        <div class="dif-info">
          <b>Side maxima A₁, A₂, …</b><br>
          • Lie <em>between</em> consecutive dark fringes<br>
          • Get progressively <b>dimmer</b> (≈ 4.5%, 1.6%, … of I₀)<br>
          • Approximate: sinθ ≈ (n+½)·λ/a
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # slider for interactive intensity plot
    a_lam_slider = st.slider(
        'Ratio  a / λ  (slit width ÷ wavelength)',
        min_value=1.0, max_value=8.0, value=3.0, step=0.5,
        help='Drag to see how changing a/λ shifts and multiplies the dark fringes'
    )
    nmax_slider = int(a_lam_slider)
    col_info, col_nums = st.columns([2, 1])
    with col_info:
        st.info(f'**a/λ = {a_lam_slider:.4g}** → n_max = **{nmax_slider}** → '
                f'**{2*nmax_slider} dark fringes** | **{2*nmax_slider+1} bright fringes**')
    with col_nums:
        if nmax_slider > 0:
            angles = [np.degrees(np.arcsin(n / a_lam_slider))
                      for n in range(1, nmax_slider+1)
                      if n / a_lam_slider < 1.0]
            angle_str = ',  '.join(f'N{i+1} = {a:.1f}°' for i, a in enumerate(angles))
            st.caption(f'Dark fringe angles: {angle_str}')

    st.image(_io.BytesIO(_fig_intensity(a_lam_slider)), use_container_width=True)

    # ══════════════════════════════════════════════════════════════════════════
    # 04 — Counting n_max and total lines
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown('<div class="dif-h2">04 — Counting Dark &amp; Bright Fringes</div>',
                unsafe_allow_html=True)
    st.markdown("""
    <div class="dif-card">
      <div class="dif-grid3">
        <div class="dif-info" style="border-left:4px solid #dc2626">
          <b style="color:#dc2626">Maximum order</b><br><br>
          <code style="font-size:.98rem">n_max = ⌊ a / λ ⌋</code><br><br>
          Integer part of a/λ.<br>
          (sinθ ≤ 1, so nλ/a ≤ 1 → n ≤ a/λ)
        </div>
        <div class="dif-info" style="border-left:4px solid #dc2626">
          <b style="color:#dc2626">Total dark fringes</b><br><br>
          <code style="font-size:.98rem">= 2 × n_max</code><br><br>
          N1, N2, … N_max on <em>each side</em>.<br>
          e.g. n_max = 3 → <b>6 dark fringes</b>
        </div>
        <div class="dif-info" style="border-left:4px solid #16a34a">
          <b style="color:#16a34a">Total bright fringes</b><br><br>
          <code style="font-size:.98rem">= 2 × n_max + 1</code><br><br>
          Central A₀ + A₁…A_{n_max−1} each side.<br>
          e.g. n_max = 3 → <b>7 bright fringes</b>
        </div>
      </div>

      <div style="margin-top:14px">
        <div class="dif-hl dif-hl-g" style="margin-bottom:8px">
          <b>Example 1:</b>&ensp; a = 6 cm, λ = 2 cm<br>
          n_max = ⌊ 6/2 ⌋ = ⌊ 3 ⌋ = <b>3</b> &emsp;→&emsp;
          Dark fringes = 2×3 = <b>6</b> &emsp; Bright fringes = 2×3+1 = <b>7</b>
        </div>
        <div class="dif-hl dif-hl-g">
          <b>Example 2:</b>&ensp; a = 8 cm, λ = 2.5 cm<br>
          n_max = ⌊ 8/2.5 ⌋ = ⌊ 3.2 ⌋ = <b>3</b> &emsp;→&emsp;
          Dark fringes = <b>6</b> &nbsp;
          <span style="color:#dc2626">(NOT 6.4 — always floor, never round)</span>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════════════
    # 05 — Finding angles
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown('<div class="dif-h2">05 — Finding the Angle of a Dark Fringe</div>',
                unsafe_allow_html=True)
    st.markdown("""
    <div class="dif-card">
      <div class="dif-formula">sinθ_n = n · λ / a &emsp;→&emsp; θ_n = arcsin( n·λ / a )</div>

      <div class="dif-step"><div class="dif-step-num">1</div>
        <div>Write the formula: &nbsp; sinθ = nλ/a</div></div>
      <div class="dif-step"><div class="dif-step-num">2</div>
        <div>Substitute n, λ, a and compute sinθ</div></div>
      <div class="dif-step"><div class="dif-step-num">3</div>
        <div>Take arcsin to get θ &nbsp;(or leave as sinθ if asked)</div></div>

      <div class="dif-grid" style="margin-top:14px">
        <div class="dif-hl">
          <b>Worked example — find θ₂:</b><br>
          a = 8 cm, λ = 2.5 cm<br><br>
          sinθ₂ = 2 × 2.5 / 8 = 5/8 = 0.625<br>
          θ₂ = arcsin(0.625) ≈ <b>38.7°</b>
        </div>
        <div class="dif-hl dif-hl-p">
          <b>Approximate bright-fringe angle:</b><br>
          A<sub>n</sub> lies roughly midway between N<sub>n</sub> and N<sub>n+1</sub><br><br>
          sinθ_A ≈ (n + ½)·λ / a<br><br>
          e.g. A₁ (between N₁ and N₂, a=8, λ=2.5):<br>
          sinθ ≈ 1.5 × 2.5/8 = 0.469 → θ ≈ 27.9°<br>
          <em style="font-size:.76rem">(approximation only — exact requires calculus)</em>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════════════
    # 06 — Effect of changing a or λ
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown('<div class="dif-h2">06 — Effect of Changing a or λ</div>',
                unsafe_allow_html=True)
    st.markdown("""
    <div class="dif-card">
      <div class="dif-formula">n_max = ⌊ a / λ ⌋</div>
      <table class="ref-table" style="margin-top:12px">
        <tr>
          <th>Change</th>
          <th>Effect on a/λ</th>
          <th>n_max &amp; fringes</th>
          <th>Pattern shape</th>
        </tr>
        <tr>
          <td>Wider slit &nbsp;(a ↑)</td>
          <td>a/λ ↑</td>
          <td>n_max ↑, more dark fringes</td>
          <td>Narrower central max, fringes closer together</td>
        </tr>
        <tr>
          <td>Narrower slit &nbsp;(a ↓)</td>
          <td>a/λ ↓</td>
          <td>n_max ↓, fewer fringes</td>
          <td>Wider central max, more spreading</td>
        </tr>
        <tr>
          <td>Longer wavelength &nbsp;(λ ↑)</td>
          <td>a/λ ↓</td>
          <td>n_max ↓, fewer fringes</td>
          <td>Larger angles, more diffraction</td>
        </tr>
        <tr>
          <td>Shorter wavelength &nbsp;(λ ↓)</td>
          <td>a/λ ↑</td>
          <td>n_max ↑, more fringes</td>
          <td>Smaller angles, sharper pattern</td>
        </tr>
        <tr>
          <td>Freq. becomes f/3 &nbsp;(λ → 3λ)</td>
          <td>a/λ → a/3λ</td>
          <td>n_new = ⌊original n_max/3⌋</td>
          <td>Much fewer fringes, much wider central max</td>
        </tr>
      </table>

      <div class="dif-hl dif-hl-y" style="margin-top:12px">
        <b>Exam-style worked example (Q65-type):</b><br>
        Original: 6 dark fringes → n_max = 3 → a/λ = 3<br>
        New: a → 2a, frequency → f/3 (so λ → 3λ)<br>
        n_new = ⌊ 2a / 3λ ⌋ = ⌊ (2/3) × 3 ⌋ = ⌊ 2 ⌋ = <b>2</b><br>
        New dark fringes = 2 × 2 = <b>4 fringes</b>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════════════
    # 07 — Double-Slit
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown('<div class="dif-h2">07 — Double-Slit Interference (review)</div>',
                unsafe_allow_html=True)
    st.markdown("""
    <div class="dif-card">
      <div class="dif-card-title">Two coherent point sources separated by d</div>
      <div class="dif-grid">
        <div>
          <div class="dif-formula2">Δr = nλ → bright (antinodal)</div>
          n_max = ⌊ d/λ ⌋<br>
          Total bright (antinodal) lines = <b>2·n_max + 1</b><br>
          <span style="font-size:.8rem;color:#64748b">(includes central line n=0)</span>
        </div>
        <div>
          <div class="dif-formula" style="border-color:#dc2626">Δr = (n−½)λ → dark (nodal)</div>
          Total dark (nodal) lines = <b>2·n_max</b><br>
          <span style="font-size:.8rem;color:#64748b">(n = 1, 2, … n_max each side)</span>
        </div>
      </div>
      <div class="dif-hl dif-hl-g" style="margin-top:12px">
        <b>Example (Q68-type):</b>&ensp; d = 8 cm, measured Δr = 4 cm → λ = 2 cm<br>
        n_max = ⌊ 8/2 ⌋ = 4<br>
        Bright (antinodal) lines = 2×4+1 = <b>9 lines</b> &emsp;
        Dark (nodal) lines = 2×4 = <b>8 lines</b>
      </div>
      <div class="dif-hl dif-hl-r" style="margin-top:8px">
        ⚠️ <b>Single-slit vs Double-slit:</b><br>
        Single slit: formula gives <b>dark</b> fringes (a·sinθ = nλ → destructive)<br>
        Double slit: formula gives <b>bright</b> fringes (d·sinθ = nλ → constructive)<br>
        The n=0 case: single-slit centre is <b>bright</b>, double-slit centre is also <b>bright</b>.
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════════════
    # REF — Quick reference table
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown('<div class="dif-h2">📋 Quick-Reference Cheat Sheet</div>',
                unsafe_allow_html=True)
    st.markdown("""
    <div class="dif-card">
      <table class="ref-table">
        <tr>
          <th>Quantity</th><th>Formula</th><th>Notes</th>
        </tr>
        <tr>
          <td><b>Dark fringe condition</b></td>
          <td><code>a · sinθ = nλ</code></td>
          <td>n = 1, 2, 3, … &nbsp;(NOT n=0)</td>
        </tr>
        <tr>
          <td><b>Maximum order</b></td>
          <td><code>n_max = ⌊ a/λ ⌋</code></td>
          <td>Floor (integer part) of a/λ — never round up</td>
        </tr>
        <tr>
          <td><b>Total dark fringes</b></td>
          <td><code>2 × n_max</code></td>
          <td>Symmetric about centre (±N1, ±N2, …)</td>
        </tr>
        <tr>
          <td><b>Total bright fringes</b></td>
          <td><code>2 × n_max + 1</code></td>
          <td>Includes central A₀; side maxima dimmer</td>
        </tr>
        <tr>
          <td><b>nth dark-fringe angle</b></td>
          <td><code>sinθ_n = nλ/a</code></td>
          <td>Use arcsin to get degrees</td>
        </tr>
        <tr>
          <td><b>Approx bright angle</b></td>
          <td><code>sinθ ≈ (n+½)λ/a</code></td>
          <td>Approximate; between Nₙ and Nₙ₊₁</td>
        </tr>
        <tr>
          <td><b>Double-slit bright</b></td>
          <td><code>d · sinθ = nλ</code></td>
          <td>n = 0, ±1, ±2, … → antinodal: 2n_max+1</td>
        </tr>
        <tr>
          <td><b>Double-slit dark</b></td>
          <td><code>d · sinθ = (n−½)λ</code></td>
          <td>n = 1, 2, … → nodal: 2n_max</td>
        </tr>
      </table>

      <div class="dif-grid3" style="margin-top:16px">
        <div class="dif-info">
          <b>3-step method</b><br>
          ① n_max = ⌊ a/λ ⌋<br>
          ② dark = 2×n_max<br>
          ③ sinθ = nλ/a for angles
        </div>
        <div class="dif-info">
          <b>Trap: never round up</b><br>
          a/λ = 3.9 → n_max = <b>3</b><br>
          a/λ = 4.0 → n_max = <b>4</b><br>
          a/λ = 4.0 means sinθ₄=1, exactly 90°
        </div>
        <div class="dif-info">
          <b>Single vs Double</b><br>
          Single: nλ = a·sinθ → <b>dark</b><br>
          Double: nλ = d·sinθ → <b>bright</b><br>
          Opposite meanings for n!
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
