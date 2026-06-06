import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from matplotlib.patches import FancyArrowPatch

# ── helpers ──────────────────────────────────────────────────────────────────
def _close_figs():
    plt.close('all')

# ════════════════════════════════════════════════════════════════════════════
# Q1  :  x-axis 0→1.6 m (λ=0.8m)  |  t-axis 0→7 s (T=4s)
# ════════════════════════════════════════════════════════════════════════════
def _q1():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 3.2))

    # --- รูป (1): position vs displacement, λ=0.8 m ---
    x = np.linspace(0, 1.6, 500)
    ax1.plot(x, np.sin(2*np.pi*x/0.8), 'b-', lw=2)
    ax1.axhline(0, color='k', lw=1)
    ax1.axvline(0, color='k', lw=1)
    ax1.set_xlim(-0.05, 1.7)
    ax1.set_xticks([0, 0.4, 0.8, 1.2, 1.6])
    ax1.set_xticklabels(['0', '0.4', '0.8', '1.2', '1.6'])
    ax1.set_xlabel('x (m)')
    ax1.set_ylabel('y')
    ax1.set_title('Fig (1): Displacement vs Position')
    for v in [0.4, 0.8, 1.2, 1.6]:
        ax1.axvline(v, color='gray', lw=0.5, ls='--')

    # --- รูป (2): time vs displacement, T=4 s ---
    t = np.linspace(0, 7, 500)
    ax2.plot(t, np.sin(2*np.pi*t/4), 'b-', lw=2)
    ax2.axhline(0, color='k', lw=1)
    ax2.axvline(0, color='k', lw=1)
    ax2.set_xlim(-0.2, 7.5)
    ax2.set_xticks([0, 1, 2, 3, 4, 5, 6, 7])
    ax2.set_xlabel('t (s)')
    ax2.set_ylabel('y')
    ax2.set_title('Fig (2): Displacement vs Time')
    for v in [1, 3, 5, 7]:
        ax2.axvline(v, color='gray', lw=0.5, ls='--')

    fig.tight_layout()
    return fig

# ════════════════════════════════════════════════════════════════════════════
# Q2  :  x-axis 0→6 m, 1.5 wave cycles visible (λ=4 m)
# ════════════════════════════════════════════════════════════════════════════
def _q2():
    fig, ax = plt.subplots(figsize=(7, 3))
    x = np.linspace(0, 6, 500)
    ax.plot(x, np.sin(2*np.pi*x/4), 'b-', lw=2)
    ax.axhline(0, color='k', lw=1)
    ax.axvline(0, color='k', lw=1)
    ax.set_xlim(-0.2, 6.5)
    ax.set_xticks([0, 2, 4, 6])
    ax.set_xlabel('x (m)')
    ax.set_ylabel('y')
    ax.set_title('Q2: Wave after 0.5 s  (λ = 4 m)')
    fig.tight_layout()
    return fig

# ════════════════════════════════════════════════════════════════════════════
# Q3  :  x-axis 0→22 cm  (5 ½ cycles, λ=8 cm)  ตามรูปในโจทย์
# ════════════════════════════════════════════════════════════════════════════
def _q3():
    fig, ax = plt.subplots(figsize=(9, 3))
    x = np.linspace(0, 22, 500)
    ax.plot(x, np.sin(2*np.pi*x/8), 'b-', lw=2)
    ax.axhline(0, color='k', lw=1)
    ax.axvline(0, color='k', lw=1)
    ax.set_xlim(-0.5, 23)
    # ตามรูป: มีตัวเลข 4, 8, 10(≈12), 18, 20, 22 บน x
    ax.set_xticks([0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22])
    ax.set_xlabel('Position (cm)')
    ax.set_ylabel('Displacement')
    ax.set_title('Q3: Wave shape  (λ = 8 cm)')
    fig.tight_layout()
    return fig

# ════════════════════════════════════════════════════════════════════════════
# Q4  :  t-axis 0→0.5 s (T=0.2 s, 2.5 cycles)  ตามรูปในโจทย์
# ════════════════════════════════════════════════════════════════════════════
def _q4():
    fig, ax = plt.subplots(figsize=(7, 3))
    t = np.linspace(0, 0.5, 500)
    ax.plot(t, 0.1*np.sin(2*np.pi*t/0.2), 'b-', lw=2)
    ax.axhline(0, color='k', lw=1)
    ax.axvline(0, color='k', lw=1)
    ax.set_xlim(-0.01, 0.55)
    ax.set_ylim(-0.13, 0.13)
    ax.set_xticks([0, 0.1, 0.2, 0.3, 0.4, 0.5])
    ax.set_xlabel('t (s)')
    ax.set_ylabel('Displacement')
    ax.set_title('Q4: Displacement-Time graph  (T = 0.2 s)')
    for v in [0.1, 0.2, 0.3, 0.4, 0.5]:
        ax.axvline(v, color='gray', lw=0.5, ls='--')
    fig.tight_layout()
    return fig

# ════════════════════════════════════════════════════════════════════════════
# Q5  :  รูป (ก) และ (ข) บน x-axis 0→3 m, λ=2 m
# ════════════════════════════════════════════════════════════════════════════
def _q5():
    fig, axes = plt.subplots(1, 2, figsize=(9, 3.5))
    x = np.linspace(0, 3, 300)

    # รูป (ก): t=0 — 1.5 cycles
    axes[0].plot(x, np.sin(2*np.pi*x/2), 'b-', lw=2)
    axes[0].axhline(0, color='k', lw=1)
    axes[0].set_xlim(-0.1, 3.2)
    axes[0].set_xticks([0, 1, 2, 3])
    axes[0].set_xlabel('x (m)')
    axes[0].set_ylabel('y')
    axes[0].set_title('Fig (ก): t = 0')
    axes[0].text(3.1, 0.02, '3 (m)', va='bottom', fontsize=9)

    # รูป (ข): t=2 s — เลื่อนขวา 1 m = λ/2 → กลับเฟส
    axes[1].plot(x, np.sin(2*np.pi*x/2 + np.pi), 'b-', lw=2)
    axes[1].axhline(0, color='k', lw=1)
    axes[1].set_xlim(-0.1, 3.2)
    axes[1].set_xticks([0, 1, 2, 3])
    axes[1].set_xlabel('x (m)')
    axes[1].set_ylabel('y')
    axes[1].set_title('Fig (ข): t = 2 s')
    axes[1].text(3.1, 0.02, '3 (m)', va='bottom', fontsize=9)

    fig.suptitle('Q5: Rope 3 m, λ = 2 m', y=1.01)
    fig.tight_layout()
    return fig

# ════════════════════════════════════════════════════════════════════════════
# Q13 :  triangular pulse on grid (ตามรูปในโจทย์ — pulse เหมือน /\ \_)
# ════════════════════════════════════════════════════════════════════════════
def _q13():
    """แสดง initial state ของ Q13 เหมือนโจทย์ (triangular pulse + flat region)"""
    fig, ax = plt.subplots(figsize=(10, 3.5))

    # grid
    ax.set_xlim(0, 30)
    ax.set_ylim(-1.5, 3)
    for gx in range(0, 31):
        ax.axvline(gx, color='lightgray', lw=0.4)
    for gy in np.arange(-1, 3.5, 0.5):
        ax.axhline(gy, color='lightgray', lw=0.4)

    # pulse shape ตามโจทย์: flat at y=0 (x=0..5), rise (x=5..8), peak (x=8),
    #   down (x=8..10), flat y=-0.5 (x=10..16), back to 0 (x=16..30)
    # ปรับตามรูป: /\ แล้ว flat ต่ำ
    px = [0, 5, 5, 8, 10, 16, 16, 30]
    py = [0, 0, 0, 2,  0,  0, -0.5, -0.5]
    # รูปที่ถูกต้องตามโจทย์ (triangle peak ขวา + flat ซ้าย ระดับต่ำ)
    px2 = [0,  6,  9, 12, 16, 16, 30]
    py2 = [0,  0,  2,  0,  0, -0.5, -0.5]
    ax.plot(px2, py2, 'k-', lw=2.5)
    ax.axhline(0, color='k', lw=1)

    # arrow (direction)
    ax.annotate('', xy=(20, 2.5), xytext=(18, 2.5),
                arrowprops=dict(arrowstyle='->', color='k', lw=2))
    ax.set_xticks(range(0, 31, 2))
    ax.set_xlabel('Position (cells)')
    ax.set_title('Q13: Pulse wave, v = 20 cells/s  (t = 0)')
    fig.tight_layout()
    return fig

# ════════════════════════════════════════════════════════════════════════════
# Q17 :  sine wave 2 full cycles, points a–q labelled ตามโจทย์
# ════════════════════════════════════════════════════════════════════════════
def _q17():
    fig, ax = plt.subplots(figsize=(11, 4))

    lam = 4  # arbitrary units; 2 cycles shown
    x = np.linspace(0, 2*lam, 600)
    y = np.sin(2*np.pi*x/lam)
    ax.plot(x, y, 'b-', lw=2)
    ax.axhline(0, color='k', lw=1)
    ax.axvline(0, color='k', lw=1)
    ax.set_xlim(-0.3, 8.5)
    ax.set_ylim(-1.5, 1.7)

    # points every λ/4
    labels = list('abcdefghijklmnopq')
    positions = [i*lam/4 for i in range(17)]
    for lbl, xp in zip(labels, positions):
        if xp > 2*lam:
            break
        yp = np.sin(2*np.pi*xp/lam)
        ax.plot(xp, yp, 'ro', ms=5, zorder=5)
        offset = (0, 14) if yp >= 0 else (0, -16)
        ax.annotate(lbl, (xp, yp), textcoords='offset points',
                    xytext=offset, ha='center', fontsize=10, color='black',
                    fontweight='bold')

    ax.set_xlabel('Position')
    ax.set_ylabel('Displacement')
    ax.set_title('Q17: Points a–q on the wave (every λ/4)')
    # arrow at end
    ax.annotate('', xy=(8.4, 0), xytext=(7.8, 0),
                arrowprops=dict(arrowstyle='->', color='k', lw=1.5))
    ax.text(8.45, 0, 'x', va='center', fontsize=10)
    fig.tight_layout()
    return fig

# ════════════════════════════════════════════════════════════════════════════
# Q20 :  t-axis 0→0.5 s, A=0.1, T=0.2 s (ตามรูปในโจทย์)
# ════════════════════════════════════════════════════════════════════════════
def _q20():
    fig, ax = plt.subplots(figsize=(7, 3.5))
    t = np.linspace(0, 0.5, 500)
    ax.plot(t, 0.1*np.sin(2*np.pi*t/0.2), 'b-', lw=2)
    ax.axhline(0, color='k', lw=1)
    ax.axvline(0, color='k', lw=1)
    ax.set_xlim(-0.02, 0.55)
    ax.set_ylim(-0.13, 0.13)
    ax.set_xticks([0, 0.1, 0.2, 0.3, 0.4, 0.5])
    ax.set_yticks([-0.1, 0, 0.1])
    ax.set_yticklabels(['-0.1', '0', '0.1'])
    ax.set_xlabel('t (s)')
    ax.set_ylabel('Displacement')
    ax.set_title('Q20: v = 2 m/s, T = 0.2 s  → λ = 0.4 m')
    for v in [0.1, 0.2, 0.3, 0.4, 0.5]:
        ax.axvline(v, color='lightgray', lw=0.6, ls='--')
    fig.tight_layout()
    return fig

# ════════════════════════════════════════════════════════════════════════════
# Q28/Q29 :  superposition on grid (triangular pulses moving toward each other)
#  — แสดง t=0 เท่านั้น พร้อม label
# ════════════════════════════════════════════════════════════════════════════
def _q28():
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.set_xlim(0, 24)
    ax.set_ylim(-2, 4)

    for gx in range(0, 25):
        ax.axvline(gx, color='lightgray', lw=0.4)
    for gy in range(-2, 5):
        ax.axhline(gy, color='lightgray', lw=0.4)
    ax.axhline(0, color='k', lw=1.2)

    # Right-moving pulse (ซ้าย): peak at x=4, height=2
    px_r = [0, 2, 4, 6, 8, 24]
    py_r = [0, 0, 2, 0, 0,  0]
    ax.plot(px_r, py_r, 'b-', lw=2.5, label='Right-moving')
    ax.annotate('', xy=(9, 2.2), xytext=(7.5, 2.2),
                arrowprops=dict(arrowstyle='->', color='b', lw=1.5))

    # Left-moving pulse (ขวา): peak at x=18, height=2
    px_l = [0, 14, 16, 18, 20, 22, 24]
    py_l = [0,  0,  0,  2,  0,  0,  0]
    ax.plot(px_l, py_l, 'r-', lw=2.5, label='Left-moving')
    ax.annotate('', xy=(15, 2.2), xytext=(16.5, 2.2),
                arrowprops=dict(arrowstyle='->', color='r', lw=1.5))

    ax.set_xticks(range(0, 25, 2))
    ax.set_xlabel('Position (cells)')
    ax.set_title('Q28: Superposition of two pulses (v = 2 cells/s), t = 0')
    ax.legend(loc='upper right', fontsize=9)
    fig.tight_layout()
    return fig

def _q29():
    """Q29: คล้าย Q28 แต่ pulse มีรูปร่างต่างกัน (ตามรูปในโจทย์)"""
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.set_xlim(0, 24)
    ax.set_ylim(-3, 4)

    for gx in range(0, 25):
        ax.axvline(gx, color='lightgray', lw=0.4)
    for gy in range(-2, 4):
        ax.axhline(gy, color='lightgray', lw=0.4)
    ax.axhline(0, color='k', lw=1.2)

    # Right-moving: wider triangle, height 3
    px_r = [0, 1, 4, 7, 24]
    py_r = [0, 0, 3, 0,  0]
    ax.plot(px_r, py_r, 'b-', lw=2.5, label='Right-moving')
    ax.annotate('', xy=(8, 2.8), xytext=(6.5, 2.8),
                arrowprops=dict(arrowstyle='->', color='b', lw=1.5))

    # Left-moving: narrower, height 2
    px_l = [0, 15, 17, 19, 24]
    py_l = [0,  0,  2,  0,  0]
    ax.plot(px_l, py_l, 'r-', lw=2.5, label='Left-moving')
    ax.annotate('', xy=(14, 2.3), xytext=(15.5, 2.3),
                arrowprops=dict(arrowstyle='->', color='r', lw=1.5))

    ax.set_xticks(range(0, 25, 2))
    ax.set_xlabel('Position (cells)')
    ax.set_title('Q29: Superposition of two pulses (v = 2 cells/s), t = 0')
    ax.legend(loc='upper right', fontsize=9)
    fig.tight_layout()
    return fig

# ════════════════════════════════════════════════════════════════════════════
# Q30 :  pulse v=4 cells/s, t=0 เหมือนโจทย์
# ════════════════════════════════════════════════════════════════════════════
def _q30():
    fig, ax = plt.subplots(figsize=(10, 3.5))
    ax.set_xlim(0, 20)
    ax.set_ylim(-1, 3)

    for gx in range(0, 21):
        ax.axvline(gx, color='lightgray', lw=0.4)
    for gy in range(-1, 4):
        ax.axhline(gy, color='lightgray', lw=0.4)
    ax.axhline(0, color='k', lw=1.2)

    # triangular pulse at left, moving right
    px = [0, 2, 4, 6, 8, 20]
    py = [0, 0, 2, 0, 0,  0]
    ax.plot(px, py, 'k-', lw=2.5)
    ax.annotate('', xy=(9.5, 2.2), xytext=(8, 2.2),
                arrowprops=dict(arrowstyle='->', color='k', lw=1.5))

    ax.set_xticks(range(0, 21, 2))
    ax.set_xlabel('Position (cells)')
    ax.set_title('Q30: Pulse wave, v = 4 cells/s  (t = 0)')
    fig.tight_layout()
    return fig

# ════════════════════════════════════════════════════════════════════════════
# Q31 :  pulse สะท้อน free end (เหมือนโจทย์)
# ════════════════════════════════════════════════════════════════════════════
def _q31():
    fig, ax = plt.subplots(figsize=(10, 3.5))
    ax.set_xlim(0, 20)
    ax.set_ylim(-1, 3)

    for gx in range(0, 21):
        ax.axvline(gx, color='lightgray', lw=0.4)
    for gy in range(-1, 4):
        ax.axhline(gy, color='lightgray', lw=0.4)
    ax.axhline(0, color='k', lw=1.2)

    # pulse near right end (free end at x=20)
    px = [0, 12, 14, 16, 18, 20]
    py = [0,  0,  2,  0,  0,  0]
    ax.plot(px, py, 'k-', lw=2.5)
    ax.annotate('', xy=(17, 2.2), xytext=(15.5, 2.2),
                arrowprops=dict(arrowstyle='->', color='k', lw=1.5))
    # free-end marker
    ax.plot(20, 0, 'wo', ms=10, mec='k', mew=2, zorder=5)
    ax.text(20.2, 0.1, 'Free\nend', fontsize=8)

    ax.set_xticks(range(0, 21, 2))
    ax.set_xlabel('Position (cells)')
    ax.set_title('Q31: Pulse approaching free end, v = 4 cells/s  (t = 0)')
    fig.tight_layout()
    return fig

# ════════════════════════════════════════════════════════════════════════════
# Q32–Q42 : refraction diagrams ที่มีรูปในโจทย์
# ════════════════════════════════════════════════════════════════════════════
def _refraction_diagram(th1_deg, th2_deg, label1='Medium 1', label2='Medium 2', title=''):
    """Generic refraction diagram."""
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.axhline(0, color='k', lw=1.5, ls='--')
    ax.axvline(0, color='gray', lw=1, ls=':')

    th1 = np.radians(th1_deg)
    th2 = np.radians(th2_deg)
    L = 2.5

    # incident ray (from upper-left toward origin)
    ax.annotate('', xy=(0, 0),
                xytext=(-L*np.sin(th1), L*np.cos(th1)),
                arrowprops=dict(arrowstyle='->', color='blue', lw=2))
    # refracted ray (from origin downward)
    ax.annotate('', xy=(L*np.sin(th2), -L*np.cos(th2)),
                xytext=(0, 0),
                arrowprops=dict(arrowstyle='->', color='red', lw=2))
    # angle labels
    ax.text(-0.6, 0.5, f'θ₁={th1_deg}°', color='blue', fontsize=11)
    ax.text(0.2, -0.5, f'θ₂={th2_deg}°', color='red', fontsize=11)

    ax.text(-2.8,  0.15, label1, fontsize=10)
    ax.text(-2.8, -0.3,  label2, fontsize=10)
    ax.set_xlim(-3, 3); ax.set_ylim(-3, 3)
    ax.set_title(title)
    ax.axis('off')
    fig.tight_layout()
    return fig

def _q32():
    return _refraction_diagram(60, 26, 'Deep (v₁=2v₂)', 'Shallow (v₂)',
                                title='Q32: Deep→Shallow, θ₁=60°, θ₂≈26°')

def _q34():
    """Q34: zone A→B from diagram (θ_A=45°, θ_B=30°)"""
    fig, ax = plt.subplots(figsize=(6, 5))
    ax.set_xlim(0, 22)
    ax.set_ylim(0, 10)

    # vertical boundary at x=11
    ax.axvline(11, color='k', lw=2)
    ax.text(0.5, 9.2, 'Zone A', fontsize=12, fontweight='bold')
    ax.text(12, 9.2, 'Zone B', fontsize=12, fontweight='bold')

    # wavefronts in A (parallel lines, slight angle)
    for xi in [2, 4, 6, 8, 10]:
        ax.plot([xi-0.5, xi+0.5], [1, 9], 'b-', lw=1.2, alpha=0.8)

    # wavefronts in B (steeper angle)
    for xi in [12, 14, 16, 18, 20]:
        ax.plot([xi-0.3, xi+0.3], [1, 9], 'r-', lw=1.2, alpha=0.8)

    # angles
    ax.text(8.5, 4.5, '45°', fontsize=11, color='blue')
    ax.text(11.5, 4.5, '30°', fontsize=11, color='red')
    ax.set_axis_off()
    ax.set_title('Q34: Refraction A→B  (θ_A=45°, θ_B=30°, f=40 Hz)')
    fig.tight_layout()
    return fig

def _q35():
    return _refraction_diagram(30, 60, 'Shallow (v₁)', 'Deep (v₂=√3·v₁)',
                                title='Q35: Shallow→Deep, θ₁=30°, θ₂=60°')

def _q36():
    return _refraction_diagram(45, 30, 'Deep (v₁)', 'Shallow (v₂)',
                                title='Q36: Deep→Shallow, θ₁=45°, θ₂=30°')

def _q37():
    """Q37: มุมวิกฤต — คลื่นจากลึก→ตื้น"""
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.axhline(0, color='k', lw=1.5, ls='--')
    ax.axvline(0, color='gray', lw=1, ls=':')
    ax.text(-2.8, 0.15, 'Deep (v₁=5v₂/3)', fontsize=9)
    ax.text(-2.8, -0.3, 'Shallow (v₂)', fontsize=10)
    th = np.radians(37)
    ax.annotate('', xy=(0, 0), xytext=(-2.5*np.sin(th), 2.5*np.cos(th)),
                arrowprops=dict(arrowstyle='->', color='blue', lw=2))
    # refracted along surface
    ax.annotate('', xy=(2.5, 0), xytext=(0, 0),
                arrowprops=dict(arrowstyle='->', color='red', lw=2, ls='dashed'))
    ax.text(-0.8, 0.6, 'θ_c=37°', color='blue', fontsize=11)
    ax.text(0.5, 0.15, 'θ₂=90°', color='red', fontsize=11)
    ax.set_xlim(-3, 3); ax.set_ylim(-2, 3)
    ax.set_title('Q37: Critical angle (Deep→Shallow)\nsin θ_c = 3/5, θ_c = 37°')
    ax.axis('off')
    fig.tight_layout()
    return fig

def _q38():
    return _refraction_diagram(30, 90, 'Deep (v₁=2v₂)', 'Shallow',
                                title='Q38: Total reflection, θ_c = 30°\n(sin θ_c = 1/2)')

def _q39():
    return _refraction_diagram(45, 90, 'Shallow (v₁)', 'Deep (v₂)',
                                title='Q39: θ₁=45°, θ₂=90° (critical angle)')

# ════════════════════════════════════════════════════════════════════════════
# Q43  : two coherent sources, d=10 cm, λ=2.5 cm — show source+points
# ════════════════════════════════════════════════════════════════════════════
def _q43():
    fig, ax = plt.subplots(figsize=(8, 6))
    d = 10   # cm between S1 S2
    lam = 2.5

    # sources at (0, ±5)
    ax.plot(0, d/2,  'ro', ms=9, zorder=5, label='S₁')
    ax.plot(0, -d/2, 'bs', ms=9, zorder=5, label='S₂')
    ax.annotate('S₁', (0, d/2),  xytext=(-2, 0), textcoords='offset points',
                fontsize=11, color='red', fontweight='bold')
    ax.annotate('S₂', (0, -d/2), xytext=(-2,-12), textcoords='offset points',
                fontsize=11, color='blue', fontweight='bold')

    # antinodal lines (in-phase, far field)
    n_max = int(d/lam)
    theta_range = np.linspace(-np.pi/2.2, np.pi/2.2, 200)
    r_max = 28
    for n in range(-n_max, n_max+1):
        val = n*lam/d
        if abs(val) <= 1:
            th = np.arcsin(val)
            ax.plot([0, r_max*np.cos(th)], [0, r_max*np.sin(th)],
                    'g-', lw=1, alpha=0.5)
    for n in range(1, n_max+1):
        for sign in [1, -1]:
            val = (n-0.5)*lam/d
            if abs(val) <= 1:
                th = np.arcsin(sign*val)
                ax.plot([0, r_max*np.cos(th)], [0, r_max*np.sin(th)],
                        'r--', lw=0.8, alpha=0.4)

    # points A, B, C
    pts = {
        'A': (17*np.cos(np.arccos((17**2+12**2-d**2)/(2*17*12))), 8),
        'B': (14.5, 0.6),
        'C': (24, 0),
    }
    colors = {'A': 'purple', 'B': 'darkorange', 'C': 'teal'}
    for name, (px, py) in pts.items():
        ax.plot(px, py, 'D', color=colors[name], ms=8, zorder=5)
        ax.annotate(name, (px, py), xytext=(4, 4), textcoords='offset points',
                    fontsize=12, color=colors[name], fontweight='bold')

    ax.axhline(0, color='gray', lw=0.5, ls='--')
    ax.set_xlim(-3, 30); ax.set_ylim(-10, 10)
    ax.set_xlabel('x (cm)'); ax.set_ylabel('y (cm)')
    ax.set_title('Q43: S₁S₂ = 10 cm, λ = 2.5 cm\n(green=antinodal, red-dash=nodal)')
    ax.legend(loc='upper left', fontsize=9)
    fig.tight_layout()
    return fig

# ════════════════════════════════════════════════════════════════════════════
# Q44  : d=12 cm, λ=4 cm, show point X
# ════════════════════════════════════════════════════════════════════════════
def _q44():
    fig, ax = plt.subplots(figsize=(8, 6))
    d, lam = 12, 4
    n_max = int(d/lam)  # =3

    ax.plot(0,  d/2, 'ro', ms=9); ax.plot(0, -d/2, 'bs', ms=9)
    ax.annotate('S₁', (0, d/2),  xytext=(-14,0),  textcoords='offset points',
                fontsize=11, color='red')
    ax.annotate('S₂', (0, -d/2), xytext=(-14,-12), textcoords='offset points',
                fontsize=11, color='blue')

    r_max = 30
    for n in range(-n_max, n_max+1):
        val = n*lam/d
        if abs(val) <= 1:
            th = np.arcsin(val)
            ax.plot([0, r_max*np.cos(th)], [0, r_max*np.sin(th)],
                    'g-', lw=1.2, alpha=0.6)
            ax.text(r_max*np.cos(th)*1.03, r_max*np.sin(th)*1.03,
                    f'A{abs(n)}', fontsize=8, color='green')
    for n in range(1, n_max+1):
        for sign in [1, -1]:
            val = (n-0.5)*lam/d
            if abs(val) <= 1:
                th = np.arcsin(sign*val)
                ax.plot([0, r_max*np.cos(th)], [0, r_max*np.sin(th)],
                        'r--', lw=0.8, alpha=0.5)

    # Point X: r1=19, r2=25 → on S1P axis
    # Using geometry: S1 at (0,6), S2 at (0,-6), X perpendicular from S1
    # |r2-r1|=6=1.5λ → node 2
    ax.plot(0, 19, 'k^', ms=9, zorder=5)
    ax.annotate('X (r₁=19, r₂=25 cm)', (0, 19), xytext=(2, 0),
                textcoords='offset points', fontsize=9)
    ax.plot([0, 0], [d/2, 25], 'k:', lw=1)

    ax.set_xlim(-5, 32); ax.set_ylim(-16, 26)
    ax.set_xlabel('x (cm)'); ax.set_ylabel('y (cm)')
    ax.set_title('Q44: d=12 cm, λ=4 cm\nX at N₂ (path diff=6=1.5λ)')
    fig.tight_layout()
    return fig

# ════════════════════════════════════════════════════════════════════════════
# Q49  : d=6 cm, n=1 at 30°
# ════════════════════════════════════════════════════════════════════════════
def _q49():
    fig, ax = plt.subplots(figsize=(6, 5))
    d = 6
    ax.plot(0, d/2, 'ro', ms=9); ax.plot(0, -d/2, 'bs', ms=9)
    ax.annotate('S₁', (0, d/2),  xytext=(-16, 0),  textcoords='offset points',
                fontsize=11, color='red')
    ax.annotate('S₂', (0, -d/2), xytext=(-16,-12), textcoords='offset points',
                fontsize=11, color='blue')

    r = 10
    for sign in [1, -1]:
        th = sign * np.radians(30)
        ax.annotate('', xy=(r*np.cos(th), r*np.sin(th)), xytext=(0, 0),
                    arrowprops=dict(arrowstyle='->', color='green', lw=2.5))
    ax.axhline(0, color='gray', lw=0.8, ls='--')
    ax.text(5, 3.2, '30°', fontsize=12, color='green')
    ax.text(5, -3.8, '30°', fontsize=12, color='green')
    ax.set_xlim(-3, 12); ax.set_ylim(-8, 8)
    ax.set_title('Q49: d=6 cm, 1st antinode at ±30°\n→ λ = d·sin30° = 3 cm')
    ax.axis('off')
    fig.tight_layout()
    return fig

# ════════════════════════════════════════════════════════════════════════════
# Q50  : d=10 cm, λ=1 cm, L=60 cm, find x
# ════════════════════════════════════════════════════════════════════════════
def _q50():
    fig, ax = plt.subplots(figsize=(7, 5))
    # Sources at left
    ax.plot(0, 0.5, 'ro', ms=8); ax.plot(0, -0.5, 'bs', ms=8)
    ax.annotate('S₁\n(d=10cm)', (0, 0.5),  xytext=(-55, 0),  textcoords='offset points',
                fontsize=9, color='red')
    ax.annotate('S₂', (0, -0.5), xytext=(-20, -15), textcoords='offset points',
                fontsize=9, color='blue')

    # Screen at x=6 (representing L=60 cm)
    ax.plot([6, 6], [-2, 2], 'k-', lw=3)
    ax.text(6.1, 0, 'O\n(center)', fontsize=8, va='center')
    ax.text(6.1, 0.6, 'P\n(1st max)', fontsize=8, va='center', color='green')
    ax.plot(6, 0.6, 'g*', ms=12, zorder=5)

    # Ray to P
    ax.plot([0, 6], [0, 0.6], 'g--', lw=1.5, alpha=0.6)
    ax.annotate('', xy=(6, 0), xytext=(6, 0.6),
                arrowprops=dict(arrowstyle='<->', color='purple', lw=1.5))
    ax.text(6.3, 0.3, 'x = 6 cm', color='purple', fontsize=10)
    ax.annotate('', xy=(6, -0.1), xytext=(0, -0.1),
                arrowprops=dict(arrowstyle='<->', color='k', lw=1.2))
    ax.text(3, -0.3, 'L = 60 cm', ha='center', fontsize=10)

    ax.set_xlim(-1.5, 7.5); ax.set_ylim(-2, 2)
    ax.set_title('Q50: d=10 cm, λ=1 cm, L=60 cm\n→ x = Lλ/d = 6 cm')
    ax.axis('off')
    fig.tight_layout()
    return fig

# ════════════════════════════════════════════════════════════════════════════
# Q52 : S1S2=2m, λ=0.5m, find antinodal positions on S1P axis
# ════════════════════════════════════════════════════════════════════════════
def _q52():
    fig, ax = plt.subplots(figsize=(7, 6))
    d = 2   # m
    lam = 0.5

    # Sources
    ax.plot(0, d/2, 'ro', ms=9, zorder=5)
    ax.plot(0,-d/2, 'bs', ms=9, zorder=5)
    ax.annotate('S₁', (0, d/2),  xytext=(-20, 2),  textcoords='offset points',
                fontsize=11, color='red')
    ax.annotate('S₂', (0,-d/2), xytext=(-20,-12), textcoords='offset points',
                fontsize=11, color='blue')

    # S1P axis (vertical from S1 upward)
    ax.axvline(0, color='gray', lw=0.8, ls='--')
    ax.annotate('', xy=(0, 5), xytext=(0, d/2),
                arrowprops=dict(arrowstyle='->', color='k', lw=1.5))
    ax.text(0.1, 5.1, 'P axis', fontsize=9)

    # Mark antinode positions on S1P axis
    antinode_y = [3.75, 1.5, 0.58, 1.0+d/2]  # from solution
    labels = ['n=1: y=3.75m', 'n=2: y=1.5m', 'n=3: y≈0.58m', 'n=4: y=0']
    colors2 = ['green','limegreen','yellowgreen','olive']
    for yp, lbl, col in zip([3.75,1.5,0.58,0], labels, colors2):
        ax.plot(0, yp, 'o', color=col, ms=8, zorder=5)
        ax.text(0.15, yp, lbl, fontsize=8, color=col, va='center')

    ax.set_xlim(-1, 3); ax.set_ylim(-2, 6)
    ax.set_xlabel('x (m)'); ax.set_ylabel('y (m)')
    ax.set_title('Q52: Antinodal positions on S₁P axis\n(S₁S₂=2m, λ=0.5m)')
    fig.tight_layout()
    return fig

# ════════════════════════════════════════════════════════════════════════════
# Q53 : wire 40 cm, 1 loop (fundamental)
# ════════════════════════════════════════════════════════════════════════════
def _q53():
    fig, ax = plt.subplots(figsize=(7, 3))
    L = 40  # cm
    x = np.linspace(0, L, 300)
    ax.fill_between(x, np.sin(np.pi*x/L)*1.5,
                    -np.sin(np.pi*x/L)*1.5, alpha=0.15, color='blue')
    ax.plot(x,  np.sin(np.pi*x/L)*1.5, 'b-', lw=2.5)
    ax.plot(x, -np.sin(np.pi*x/L)*1.5, 'b--', lw=1.5, alpha=0.5)
    ax.axhline(0, color='k', lw=1)
    # fixed ends
    for xend in [0, L]:
        ax.plot(xend, 0, 'ks', ms=10, zorder=5)
    # dimension arrow
    ax.annotate('', xy=(L, -2), xytext=(0, -2),
                arrowprops=dict(arrowstyle='<->', color='k', lw=1.5))
    ax.text(L/2, -2.5, '40 cm', ha='center', fontsize=10)
    ax.set_xlim(-3, L+3); ax.set_ylim(-3.5, 3)
    ax.set_title('Q53: Standing wave on wire L=40 cm (1 loop, f=20 Hz)')
    ax.set_xlabel('Position (cm)')
    ax.axis('off')
    ax.axhline(0, color='k', lw=1)
    fig.tight_layout()
    return fig

# ════════════════════════════════════════════════════════════════════════════
# Q54 : rope 3 m, λ=0.5 m, 12 loops
# ════════════════════════════════════════════════════════════════════════════
def _q54():
    fig, ax = plt.subplots(figsize=(10, 3))
    L = 3.0
    n = 12
    x = np.linspace(0, L, 600)
    ax.fill_between(x, np.sin(n*np.pi*x/L)*0.8,
                    -np.sin(n*np.pi*x/L)*0.8, alpha=0.12, color='blue')
    ax.plot(x,  np.sin(n*np.pi*x/L)*0.8, 'b-', lw=2)
    ax.plot(x, -np.sin(n*np.pi*x/L)*0.8, 'b--', lw=1, alpha=0.5)
    ax.axhline(0, color='k', lw=1)
    ax.plot(0, 0, 'ks', ms=10, zorder=5)  # fixed end A
    ax.plot(L, 0, 'ws', ms=10, mec='k', mew=2, zorder=5)  # free end B
    ax.text(-0.1, 0, 'A', ha='right', fontsize=11, fontweight='bold')
    ax.text(L+0.1, 0, 'B', ha='left',  fontsize=11, fontweight='bold')
    ax.annotate('', xy=(L, -1.2), xytext=(0, -1.2),
                arrowprops=dict(arrowstyle='<->', color='k', lw=1.5))
    ax.text(L/2, -1.5, '3 m, λ=0.5 m → 12 loops', ha='center', fontsize=9)
    ax.set_xlim(-0.3, L+0.3); ax.set_ylim(-2, 1.5)
    ax.set_title('Q54: Rope L=3m, λ=0.5m → 13 nodes, 12 antinodes')
    ax.axis('off')
    fig.tight_layout()
    return fig

# ════════════════════════════════════════════════════════════════════════════
# Q55 : source 20 cm from reflector, λ=4 cm → standing wave
# ════════════════════════════════════════════════════════════════════════════
def _q55():
    fig, ax = plt.subplots(figsize=(9, 3.5))
    L = 20  # cm
    lam = 4
    x = np.linspace(0, L, 500)
    ax.fill_between(x, np.sin(2*np.pi*x/lam)*0.8,
                    -np.sin(2*np.pi*x/lam)*0.8, alpha=0.12, color='blue')
    ax.plot(x,  np.sin(2*np.pi*x/lam)*0.8, 'b-', lw=2)
    ax.plot(x, -np.sin(2*np.pi*x/lam)*0.8, 'b--', lw=1, alpha=0.4)
    ax.axhline(0, color='k', lw=1)

    # Nodes (at x=0,2,4,...,20) — every λ/2=2 cm
    nodes = np.arange(0, L+0.1, lam/2)
    ax.plot(nodes, np.zeros_like(nodes), 'rv', ms=7, zorder=5, label='Node (N)')
    antinodes = np.arange(lam/4, L, lam/2)
    ax.plot(antinodes, np.zeros_like(antinodes), 'g^', ms=7, zorder=5, label='Antinode (A)')

    # Source and reflector
    ax.plot(0, 0, 'ko', ms=10, zorder=6)
    ax.text(-0.5, 0.3, 'S', fontsize=11, fontweight='bold')
    ax.axvline(L, color='k', lw=3)
    ax.text(L+0.3, 0.3, 'Reflector', fontsize=9)

    ax.annotate('', xy=(L, -1.2), xytext=(0, -1.2),
                arrowprops=dict(arrowstyle='<->', color='k', lw=1.5))
    ax.text(L/2, -1.5, '20 cm = 5λ', ha='center', fontsize=9)
    ax.set_xlim(-1.5, L+2); ax.set_ylim(-2, 1.5)
    ax.set_title('Q55: S 20 cm from reflector, λ=4 cm → 11 nodes, 10 antinodes')
    ax.legend(loc='upper right', fontsize=9)
    ax.axis('off')
    fig.tight_layout()
    return fig

# ════════════════════════════════════════════════════════════════════════════
# Q56 : spring 20 cm, λ=8 cm → 5 loops
# ════════════════════════════════════════════════════════════════════════════
def _q56():
    fig, ax = plt.subplots(figsize=(9, 3))
    L, lam = 20, 8
    n = int(2*L/lam)  # =5 half-wavelengths
    x = np.linspace(0, L, 400)
    ax.fill_between(x, np.sin(n*np.pi*x/L)*0.9,
                    -np.sin(n*np.pi*x/L)*0.9, alpha=0.12, color='blue')
    ax.plot(x,  np.sin(n*np.pi*x/L)*0.9, 'b-', lw=2)
    ax.plot(x, -np.sin(n*np.pi*x/L)*0.9, 'b--', lw=1, alpha=0.4)
    ax.axhline(0, color='k', lw=1)

    nodes = np.arange(0, L+0.1, lam/2)
    anti  = np.arange(lam/4, L, lam/2)
    ax.plot(nodes, np.zeros_like(nodes), 'rv', ms=7, zorder=5, label=f'Nodes (N={len(nodes)}=6)')
    ax.plot(anti,  np.zeros_like(anti),  'g^', ms=7, zorder=5, label=f'Antinodes (A={len(anti)}=5)')
    ax.plot(0, 0, 'ks', ms=10, zorder=6)
    ax.plot(L, 0, 'ks', ms=10, zorder=6)

    ax.annotate('', xy=(L,-1.3), xytext=(0,-1.3),
                arrowprops=dict(arrowstyle='<->', color='k', lw=1.5))
    ax.text(L/2, -1.6, '20 cm', ha='center', fontsize=9)
    ax.set_xlim(-1, L+1.5); ax.set_ylim(-2, 1.5)
    ax.set_title('Q56: Spring L=20 cm, λ=8 cm → 6 nodes, 5 antinodes')
    ax.legend(loc='upper right', fontsize=9)
    ax.axis('off')
    fig.tight_layout()
    return fig

# ════════════════════════════════════════════════════════════════════════════
# Q57 : standing wave, node spacing=10 cm, v=160 cm/s
# ════════════════════════════════════════════════════════════════════════════
def _q57():
    fig, ax = plt.subplots(figsize=(9, 3))
    lam = 20   # cm  (node spacing = λ/2 = 10 cm)
    L   = 60   # show 3 full wavelengths
    x = np.linspace(0, L, 500)
    ax.fill_between(x, np.sin(2*np.pi*x/lam)*0.9,
                    -np.sin(2*np.pi*x/lam)*0.9, alpha=0.12, color='blue')
    ax.plot(x,  np.sin(2*np.pi*x/lam)*0.9, 'b-', lw=2)
    ax.plot(x, -np.sin(2*np.pi*x/lam)*0.9, 'b--', lw=1, alpha=0.4)
    ax.axhline(0, color='k', lw=1)

    nodes = np.arange(0, L+0.1, 10)
    ax.plot(nodes, np.zeros_like(nodes), 'rv', ms=8, zorder=5, label='Node')

    # ← → dimension of node spacing
    ax.annotate('', xy=(10, -1.3), xytext=(0, -1.3),
                arrowprops=dict(arrowstyle='<->', color='k', lw=1.5))
    ax.text(5, -1.6, '10 cm', ha='center', fontsize=9)

    ax.set_xlim(-2, L+2); ax.set_ylim(-2, 1.5)
    ax.set_title('Q57: Node spacing = 10 cm, v=160 cm/s → f=8 Hz')
    ax.legend(loc='upper right', fontsize=9)
    ax.axis('off')
    fig.tight_layout()
    return fig

# ════════════════════════════════════════════════════════════════════════════
# Q59 : L=1.25 m, resonance — show first 3 harmonics
# ════════════════════════════════════════════════════════════════════════════
def _q59():
    fig, axes = plt.subplots(1, 3, figsize=(12, 3.5))
    L = 1.25
    for idx, (n, f, label) in enumerate([(1,64,'n=1 (fundamental)\nf=64 Hz'),
                                          (2,128,'n=2 (1st overtone)\nf=128 Hz'),
                                          (3,192,'n=3 (2nd overtone)\nf=192 Hz')]):
        ax = axes[idx]
        x = np.linspace(0, L, 300)
        ax.fill_between(x, np.sin(n*np.pi*x/L)*0.8,
                        -np.sin(n*np.pi*x/L)*0.8, alpha=0.12, color='blue')
        ax.plot(x,  np.sin(n*np.pi*x/L)*0.8, 'b-', lw=2)
        ax.plot(x, -np.sin(n*np.pi*x/L)*0.8, 'b--', lw=1, alpha=0.5)
        ax.axhline(0, color='k', lw=1)
        ax.plot(0, 0, 'ks', ms=8); ax.plot(L, 0, 'ks', ms=8)
        ax.annotate('', xy=(L,-1.2), xytext=(0,-1.2),
                    arrowprops=dict(arrowstyle='<->', color='k', lw=1.2))
        ax.text(L/2, -1.5, '1.25 m', ha='center', fontsize=8)
        ax.set_title(label, fontsize=9)
        ax.set_ylim(-2, 1.2); ax.axis('off')
    fig.suptitle('Q59: Resonance on L=1.25 m, v=160 m/s', y=1.02)
    fig.tight_layout()
    return fig

# ════════════════════════════════════════════════════════════════════════════
# Q60 : L=1.20 m, 2nd overtone (n=3)
# ════════════════════════════════════════════════════════════════════════════
def _q60():
    fig, ax = plt.subplots(figsize=(8, 3))
    L = 1.20
    n = 3
    x = np.linspace(0, L, 300)
    ax.fill_between(x, np.sin(n*np.pi*x/L)*0.8,
                    -np.sin(n*np.pi*x/L)*0.8, alpha=0.12, color='blue')
    ax.plot(x,  np.sin(n*np.pi*x/L)*0.8, 'b-', lw=2.5)
    ax.plot(x, -np.sin(n*np.pi*x/L)*0.8, 'b--', lw=1.5, alpha=0.5)
    ax.axhline(0, color='k', lw=1)
    ax.plot(0, 0, 'ks', ms=10); ax.plot(L, 0, 'ks', ms=10)
    ax.annotate('', xy=(L,-1.1), xytext=(0,-1.1),
                arrowprops=dict(arrowstyle='<->', color='k', lw=1.5))
    ax.text(L/2, -1.4, '1.20 m', ha='center', fontsize=10)
    ax.set_xlim(-0.05, L+0.05); ax.set_ylim(-2, 1.2)
    ax.set_title('Q60: 2nd overtone (n=3) on L=1.20 m, f=320 Hz → v=256 m/s')
    ax.axis('off')
    fig.tight_layout()
    return fig

# ════════════════════════════════════════════════════════════════════════════
# Q63 : single slit a=6cm, λ=2cm — diffraction pattern
# ════════════════════════════════════════════════════════════════════════════
def _q63():
    fig, ax = plt.subplots(figsize=(8, 4))
    a, lam = 6, 2
    theta = np.linspace(-np.pi/2, np.pi/2, 2000)
    beta  = np.pi*a*np.sin(theta)/lam
    with np.errstate(divide='ignore', invalid='ignore'):
        I = np.where(np.abs(beta) < 1e-9, 1.0, (np.sin(beta)/beta)**2)

    ax.plot(np.degrees(theta), I, 'b-', lw=2)
    ax.axhline(0, color='k', lw=0.8)
    ax.fill_between(np.degrees(theta), I, alpha=0.15, color='blue')

    # mark nulls
    for n in range(-3, 4):
        if n == 0: continue
        th_n = np.degrees(np.arcsin(n*lam/a))
        ax.axvline(th_n, color='red', lw=1.2, ls='--', alpha=0.8)
        ax.text(th_n, -0.07, f'n={n}', ha='center', fontsize=8, color='red')

    ax.set_xlabel('θ (degrees)'); ax.set_ylabel('Intensity I/I₀')
    ax.set_title('Q63: Single slit, a=6 cm, λ=2 cm → 6 dark fringes (n=±1,±2,±3)')
    ax.set_xticks(range(-90, 91, 10))
    ax.set_xlim(-50, 50)
    fig.tight_layout()
    return fig

# ════════════════════════════════════════════════════════════════════════════
# Q64 : single slit a=8cm, λ=2.5cm
# ════════════════════════════════════════════════════════════════════════════
def _q64():
    fig, ax = plt.subplots(figsize=(8, 4))
    a, lam = 8, 2.5
    theta = np.linspace(-np.pi/2, np.pi/2, 2000)
    beta  = np.pi*a*np.sin(theta)/lam
    with np.errstate(divide='ignore', invalid='ignore'):
        I = np.where(np.abs(beta) < 1e-9, 1.0, (np.sin(beta)/beta)**2)

    ax.plot(np.degrees(theta), I, 'b-', lw=2)
    ax.axhline(0, color='k', lw=0.8)
    ax.fill_between(np.degrees(theta), I, alpha=0.15, color='blue')

    for n in range(-3, 4):
        if n == 0: continue
        th_n = np.degrees(np.arcsin(n*lam/a))
        ax.axvline(th_n, color='red', lw=1.2, ls='--', alpha=0.8)
        ax.text(th_n, -0.07, f'n={n}', ha='center', fontsize=8, color='red')
    # n=2 angle label
    th2 = np.degrees(np.arcsin(2*lam/a))
    ax.text(th2+1, 0.15, f'θ₂={th2:.1f}°', fontsize=9, color='darkred')

    ax.set_xlabel('θ (degrees)'); ax.set_ylabel('Intensity I/I₀')
    ax.set_title(f'Q64: Single slit, a=8 cm, λ=2.5 cm\nn=±1,±2,±3 → 6 dark fringes, θ₂≈{th2:.1f}°')
    ax.set_xlim(-60, 60)
    fig.tight_layout()
    return fig

# ════════════════════════════════════════════════════════════════════════════
# Q68 : double slit d=8cm, λ=2cm
# ════════════════════════════════════════════════════════════════════════════
def _q68():
    fig, ax = plt.subplots(figsize=(8, 6))
    d, lam = 8, 2
    n_max = int(d/lam)  # =4

    ax.plot(0,  d/2, 'ro', ms=10, zorder=5)
    ax.plot(0, -d/2, 'bs', ms=10, zorder=5)
    ax.annotate('Slit 1', (0, d/2),  xytext=(-50, 2), textcoords='offset points',
                fontsize=10, color='red')
    ax.annotate('Slit 2', (0,-d/2), xytext=(-50,-10), textcoords='offset points',
                fontsize=10, color='blue')

    r_max = 18
    for n in range(-n_max, n_max+1):
        val = n*lam/d
        if abs(val) <= 1:
            th = np.arcsin(val)
            style = 'g-'
            ax.plot([0, r_max*np.cos(th)], [0, r_max*np.sin(th)],
                    style, lw=1.5, alpha=0.7)
            ax.text(r_max*np.cos(th)*1.06, r_max*np.sin(th)*1.06,
                    f'A{abs(n)}', fontsize=9, color='green')

    for n in range(1, n_max+1):
        for sign in [1, -1]:
            val = (n-0.5)*lam/d
            if abs(val) <= 1:
                th = np.arcsin(sign*val)
                ax.plot([0, r_max*np.cos(th)], [0, r_max*np.sin(th)],
                        'r--', lw=1, alpha=0.5)
                ax.text(r_max*np.cos(th)*1.06, r_max*np.sin(th)*1.06,
                        f'N{n}', fontsize=8, color='red', alpha=0.8)

    # Point A on 2nd antinode
    th_A2 = np.arcsin(2*lam/d)
    r_A = 12
    ax.plot(r_A*np.cos(th_A2), r_A*np.sin(th_A2), 'k^', ms=10, zorder=5)
    ax.annotate('A (n=2)\nr₁=10, r₂=14 cm',
                (r_A*np.cos(th_A2), r_A*np.sin(th_A2)),
                xytext=(5, 5), textcoords='offset points', fontsize=9)

    ax.set_xlim(-3, 20); ax.set_ylim(-12, 12)
    ax.set_xlabel('x (cm)'); ax.set_ylabel('y (cm)')
    ax.set_title('Q68: Double slit d=8 cm, λ=2 cm\nGreen=antinodal (9), Red-dash=nodal (8)')
    fig.tight_layout()
    return fig

# ════════════════════════════════════════════════════════════════════════════
# PUBLIC API
# ════════════════════════════════════════════════════════════════════════════
_PLOT_MAP = {
    1:  _q1,
    2:  _q2,
    3:  _q3,
    4:  _q4,
    5:  _q5,
    13: _q13,
    17: _q17,
    20: _q20,
    28: _q28,
    29: _q29,
    30: _q30,
    31: _q31,
    32: _q32,
    34: _q34,
    35: _q35,
    36: _q36,
    37: _q37,
    38: _q38,
    39: _q39,
    43: _q43,
    44: _q44,
    49: _q49,
    50: _q50,
    52: _q52,
    53: _q53,
    54: _q54,
    55: _q55,
    56: _q56,
    57: _q57,
    59: _q59,
    60: _q60,
    63: _q63,
    64: _q64,
    68: _q68,
}

def get_plot_for_question(q_num: int):
    """Return matplotlib Figure for question q_num, or None."""
    fn = _PLOT_MAP.get(q_num)
    if fn is None:
        return None
    try:
        fig = fn()
        return fig
    except Exception as e:
        print(f'[visuals] Q{q_num} error: {e}')
        return None
