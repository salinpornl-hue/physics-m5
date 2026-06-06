import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Arc, FancyArrowPatch
import numpy as np

# ════════════════════════════════════════════════════════════════════════════
# Q1  — Fig(1): x=0→1.6m, λ=0.8m  |  Fig(2): t=0→7s, starts NEGATIVE (trough first)
# From PDF: Fig(2) begins going DOWN from zero (cosine-like, phase=π)
# ════════════════════════════════════════════════════════════════════════════
def _q1():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 3.2))

    # Fig(1): displacement vs position, λ=0.8 m, starts at 0 going up
    x = np.linspace(0, 1.6, 500)
    ax1.plot(x, np.sin(2*np.pi*x/0.8), 'b-', lw=2)
    ax1.axhline(0, color='k', lw=1)
    ax1.axvline(0, color='k', lw=1)
    ax1.set_xlim(-0.05, 1.75)
    ax1.set_xticks([0, 0.4, 0.8, 1.2, 1.6])
    ax1.set_xlabel('x (m)'); ax1.set_ylabel('y')
    ax1.set_title('Fig (1): Displacement vs Position')
    for v in [0.4, 0.8, 1.2, 1.6]:
        ax1.axvline(v, color='lightgray', lw=0.6, ls='--')

    # Fig(2): displacement vs TIME — from PDF the wave starts at 0 then goes
    # NEGATIVE first (trough near t=1), so phase = π  → sin(2πt/4 + π) = -sin(2πt/4)
    t = np.linspace(0, 7, 500)
    ax2.plot(t, -np.sin(2*np.pi*t/4), 'b-', lw=2)
    ax2.axhline(0, color='k', lw=1)
    ax2.axvline(0, color='k', lw=1)
    ax2.set_xlim(-0.2, 7.5)
    ax2.set_xticks([0, 1, 2, 3, 4, 5, 6, 7])
    ax2.set_xlabel('t (s)'); ax2.set_ylabel('y')
    ax2.set_title('Fig (2): Displacement vs Time')
    for v in [1, 3, 5, 7]:
        ax2.axvline(v, color='lightgray', lw=0.6, ls='--')

    fig.tight_layout()
    return fig

# ════════════════════════════════════════════════════════════════════════════
# Q2 — 1.5 cycles, x: 0→6 m, starts at 0 going positive
# ════════════════════════════════════════════════════════════════════════════
def _q2():
    fig, ax = plt.subplots(figsize=(7, 3))
    x = np.linspace(0, 6, 500)
    ax.plot(x, np.sin(2*np.pi*x/4), 'b-', lw=2)
    ax.axhline(0, color='k', lw=1); ax.axvline(0, color='k', lw=1)
    ax.set_xlim(-0.2, 6.5); ax.set_xticks([0, 2, 4, 6])
    ax.set_xlabel('x (m)'); ax.set_ylabel('y')
    ax.set_title('Q2: Wave shape after 0.5 s  (λ = 4 m)')
    fig.tight_layout()
    return fig

# ════════════════════════════════════════════════════════════════════════════
# Q3 — From PDF: starts going DOWN from zero (negative first peak near x=4),
#      x-axis labels: 2,4,6,8,10,12,16,18,20,22  (λ=8 cm)
# ════════════════════════════════════════════════════════════════════════════
def _q3():
    fig, ax = plt.subplots(figsize=(9, 3))
    x = np.linspace(0, 22, 500)
    # PDF shows wave starting at 0 going DOWN → phase = π
    ax.plot(x, -np.sin(2*np.pi*x/8), 'b-', lw=2)
    ax.axhline(0, color='k', lw=1); ax.axvline(0, color='k', lw=1)
    ax.set_xlim(-0.5, 23)
    ax.set_xticks([0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22])
    ax.set_xlabel('Position (cm)'); ax.set_ylabel('Displacement')
    ax.set_title('Q3: Wave shape  (λ = 8 cm, starts negative)')
    fig.tight_layout()
    return fig

# ════════════════════════════════════════════════════════════════════════════
# Q4 — t: 0→0.5 s, T=0.2 s, starts at 0 going positive
# ════════════════════════════════════════════════════════════════════════════
def _q4():
    fig, ax = plt.subplots(figsize=(7, 3))
    t = np.linspace(0, 0.5, 500)
    ax.plot(t, 0.1*np.sin(2*np.pi*t/0.2), 'b-', lw=2)
    ax.axhline(0, color='k', lw=1); ax.axvline(0, color='k', lw=1)
    ax.set_xlim(-0.01, 0.55); ax.set_ylim(-0.13, 0.13)
    ax.set_xticks([0, 0.1, 0.2, 0.3, 0.4, 0.5])
    ax.set_xlabel('t (s)'); ax.set_ylabel('Displacement')
    ax.set_title('Q4: Displacement-Time  (T = 0.2 s)')
    for v in [0.1, 0.2, 0.3, 0.4, 0.5]:
        ax.axvline(v, color='lightgray', lw=0.5, ls='--')
    fig.tight_layout()
    return fig

# ════════════════════════════════════════════════════════════════════════════
# Q5 — Fig(ก)/(ข) both x: 0→3 m
# ════════════════════════════════════════════════════════════════════════════
def _q5():
    fig, axes = plt.subplots(1, 2, figsize=(9, 3.5))
    x = np.linspace(0, 3, 300)
    axes[0].plot(x, np.sin(2*np.pi*x/2), 'b-', lw=2)
    axes[0].axhline(0, color='k', lw=1)
    axes[0].set_xlim(-0.1, 3.3); axes[0].set_xticks([0,1,2,3])
    axes[0].set_xlabel('x (m)'); axes[0].set_ylabel('y')
    axes[0].set_title('Fig (ก): t = 0')

    axes[1].plot(x, np.sin(2*np.pi*x/2 + np.pi), 'b-', lw=2)
    axes[1].axhline(0, color='k', lw=1)
    axes[1].set_xlim(-0.1, 3.3); axes[1].set_xticks([0,1,2,3])
    axes[1].set_xlabel('x (m)'); axes[1].set_ylabel('y')
    axes[1].set_title('Fig (ข): t = 2 s  (shifted λ/2)')

    fig.suptitle('Q5: Rope 3 m, λ = 2 m', y=1.01)
    fig.tight_layout()
    return fig

# ════════════════════════════════════════════════════════════════════════════
# Q13 — Exact shape from PDF: flat level 0 on LEFT, peak /\ in MIDDLE,
#        flat level 0 going down to lower flat on RIGHT, arrow pointing right
# ════════════════════════════════════════════════════════════════════════════
def _q13():
    fig, ax = plt.subplots(figsize=(12, 4))
    ax.set_xlim(0, 30); ax.set_ylim(-1.5, 3.5)
    # draw grid
    for gx in range(0, 31):
        ax.axvline(gx, color='lightgray', lw=0.35)
    for gy in np.arange(-1, 3.5, 0.5):
        ax.axhline(gy, color='lightgray', lw=0.35)
    ax.axhline(0, color='k', lw=1.2)

    # Pulse from PDF: reading the image carefully:
    # flat at y=0 from x=0 to x=4
    # rises to peak at x=7 height=2
    # drops back to 0 at x=10
    # flat at y=0 from x=10 to x=14
    # drops to y=-0.5 at x=14
    # flat at y=-0.5 from x=14 to x=30
    px = [0,  4,  7, 10, 10, 14, 14, 30]
    py = [0,  0,  2,  0,  0,  0,-0.5,-0.5]
    ax.plot(px, py, 'k-', lw=3)

    # Arrow showing direction (right)
    ax.annotate('', xy=(22, 2.8), xytext=(20, 2.8),
                arrowprops=dict(arrowstyle='->', color='k', lw=2.5))

    ax.set_xticks(range(0, 31, 2))
    ax.set_xlabel('Position (cells)')
    ax.set_title('Q13: Pulse, v = 20 cells/s, t = 0  →')
    fig.tight_layout()
    return fig

# ════════════════════════════════════════════════════════════════════════════
# Q17 — sine 2 cycles, points a–i labelled (from PDF only a–i shown, not a–q)
# ════════════════════════════════════════════════════════════════════════════
def _q17():
    fig, ax = plt.subplots(figsize=(10, 4))
    lam = 4
    x = np.linspace(0, 2*lam, 600)
    y = np.sin(2*np.pi*x/lam)
    ax.plot(x, y, 'b-', lw=2)
    ax.axhline(0, color='k', lw=1); ax.axvline(0, color='k', lw=1)
    ax.set_xlim(-0.3, 8.5); ax.set_ylim(-1.5, 1.7)

    labels = list('abcdefghijklmnopq')
    positions = [i*lam/4 for i in range(17)]
    for lbl, xp in zip(labels, positions):
        if xp > 2*lam: break
        yp = np.sin(2*np.pi*xp/lam)
        ax.plot(xp, yp, 'ro', ms=5, zorder=5)
        offset = (0, 14) if yp >= 0 else (0, -16)
        ax.annotate(lbl, (xp, yp), textcoords='offset points',
                    xytext=offset, ha='center', fontsize=10,
                    color='black', fontweight='bold')

    ax.set_xlabel('Position'); ax.set_ylabel('Displacement')
    ax.set_title('Q17: Points a–q on the wave (every λ/4)')
    ax.annotate('', xy=(8.4, 0), xytext=(7.8, 0),
                arrowprops=dict(arrowstyle='->', color='k', lw=1.5))
    ax.text(8.45, 0, 'x', va='center', fontsize=10)
    fig.tight_layout()
    return fig

# ════════════════════════════════════════════════════════════════════════════
# Q20 — t: 0→0.5 s, A=0.1, T=0.2 s
# ════════════════════════════════════════════════════════════════════════════
def _q20():
    fig, ax = plt.subplots(figsize=(7, 3.5))
    t = np.linspace(0, 0.5, 500)
    ax.plot(t, 0.1*np.sin(2*np.pi*t/0.2), 'b-', lw=2)
    ax.axhline(0, color='k', lw=1); ax.axvline(0, color='k', lw=1)
    ax.set_xlim(-0.02, 0.55); ax.set_ylim(-0.13, 0.13)
    ax.set_xticks([0, 0.1, 0.2, 0.3, 0.4, 0.5])
    ax.set_yticks([-0.1, 0, 0.1])
    ax.set_xlabel('t (s)'); ax.set_ylabel('Displacement')
    ax.set_title('Q20: v = 2 m/s, T = 0.2 s  → λ = 0.4 m')
    for v in [0.1, 0.2, 0.3, 0.4, 0.5]:
        ax.axvline(v, color='lightgray', lw=0.6, ls='--')
    fig.tight_layout()
    return fig

# ════════════════════════════════════════════════════════════════════════════
# Q24 — S1 top-left, S2 bottom-left, O at right with distances 20cm and 30cm
# ════════════════════════════════════════════════════════════════════════════
def _q24():
    fig, ax = plt.subplots(figsize=(6, 5))
    ax.set_xlim(-0.5, 5); ax.set_ylim(-0.5, 4.5)
    ax.set_aspect('equal')

    # S1 at (0, 3.5), S2 at (0, 0), O at (4, 1.5) roughly matching PDF
    s1 = np.array([0.0, 3.5])
    s2 = np.array([0.0, 0.0])
    O  = np.array([4.0, 1.5])

    ax.plot(*s1, 'ko', ms=7, zorder=5)
    ax.plot(*s2, 'ko', ms=7, zorder=5)
    ax.plot(*O,  'ko', ms=7, zorder=5)

    ax.text(s1[0]-0.25, s1[1]+0.1, r'$S_1$', fontsize=12, ha='right')
    ax.text(s2[0]-0.25, s2[1]-0.2, r'$S_2$', fontsize=12, ha='right')
    ax.text(O[0]+0.1,  O[1]+0.1,  'O',      fontsize=12)

    # lines S1→O and S2→O
    ax.plot([s1[0], O[0]], [s1[1], O[1]], 'b-', lw=1.5)
    ax.plot([s2[0], O[0]], [s2[1], O[1]], 'r-', lw=1.5)

    # midpoint labels
    mid1 = (s1 + O) / 2
    mid2 = (s2 + O) / 2
    ax.text(mid1[0]-0.3, mid1[1]+0.15, '20 cm', fontsize=10, color='blue',
            rotation=np.degrees(np.arctan2(O[1]-s1[1], O[0]-s1[0])))
    ax.text(mid2[0]+0.05, mid2[1]-0.3, '30 cm', fontsize=10, color='red',
            rotation=np.degrees(np.arctan2(O[1]-s2[1], O[0]-s2[0])))

    # λ labels
    ax.text(-0.45, s1[1]-0.4, r'$\lambda_1=8$ cm', fontsize=9, color='blue')
    ax.text(-0.45, s2[1]+0.1, r'$\lambda_2=10$ cm', fontsize=9, color='red')

    ax.set_title('Q24: S₁S₂ coherent sources, find Δφ at O')
    ax.axis('off')
    fig.tight_layout()
    return fig

# ════════════════════════════════════════════════════════════════════════════
# Q26 — phasor / circle diagram from PDF: circle with A(1) at 60°, B(2) at 30°
# ════════════════════════════════════════════════════════════════════════════
def _q26():
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.set_xlim(-1.7, 1.7); ax.set_ylim(-1.7, 1.7)
    ax.set_aspect('equal')

    # Draw circle
    theta_circ = np.linspace(0, 2*np.pi, 300)
    ax.plot(np.cos(theta_circ), np.sin(theta_circ), 'k-', lw=1.2)

    # Cross hairs
    ax.axhline(0, color='k', lw=0.8, ls='--', alpha=0.5)
    ax.axvline(0, color='k', lw=0.8, ls='--', alpha=0.5)

    # Wave A: initial phase 60° (from positive x-axis)
    phi_A = np.radians(60)
    ax.annotate('', xy=(np.cos(phi_A), np.sin(phi_A)), xytext=(0, 0),
                arrowprops=dict(arrowstyle='->', color='blue', lw=2.5))
    ax.text(np.cos(phi_A)*1.15, np.sin(phi_A)*1.15,
            'A\n(f=200Hz\nφ₀=60°)', fontsize=9, color='blue', ha='center')

    # Wave B: initial phase 30°
    phi_B = np.radians(30)
    ax.annotate('', xy=(np.cos(phi_B), np.sin(phi_B)), xytext=(0, 0),
                arrowprops=dict(arrowstyle='->', color='red', lw=2.5))
    ax.text(np.cos(phi_B)*1.15, np.sin(phi_B)*1.15,
            'B\n(f=180Hz\nφ₀=30°)', fontsize=9, color='red', ha='center')

    # Angle labels on circle edge
    for deg, label, col in [(150,'150°','gray'),(90,'90°','gray'),
                              (30,'30°','gray'),(0,'0°','gray')]:
        r = 1.45
        ax.text(r*np.cos(np.radians(deg)), r*np.sin(np.radians(deg)),
                label, ha='center', va='center', fontsize=8, color=col)

    ax.set_title('Q26: Phasor diagram\nA(200Hz,60°) sent 1.2s before B(180Hz,30°)')
    ax.axis('off')
    fig.tight_layout()
    return fig

# ════════════════════════════════════════════════════════════════════════════
# Q27 — phasor circle from PDF: A at 50°, B at 20° (after 0.6 s)
# ════════════════════════════════════════════════════════════════════════════
def _q27():
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.set_xlim(-1.7, 1.7); ax.set_ylim(-1.7, 1.7)
    ax.set_aspect('equal')

    theta_circ = np.linspace(0, 2*np.pi, 300)
    ax.plot(np.cos(theta_circ), np.sin(theta_circ), 'k-', lw=1.2)
    ax.axhline(0, color='k', lw=0.8, ls='--', alpha=0.5)
    ax.axvline(0, color='k', lw=0.8, ls='--', alpha=0.5)

    phi_A = np.radians(50)
    ax.annotate('', xy=(np.cos(phi_A), np.sin(phi_A)), xytext=(0, 0),
                arrowprops=dict(arrowstyle='->', color='blue', lw=2.5))
    ax.text(np.cos(phi_A)*1.2, np.sin(phi_A)*1.2,
            'A (240Hz\nφ₀=50°)', fontsize=9, color='blue', ha='center')

    phi_B = np.radians(20)
    ax.annotate('', xy=(np.cos(phi_B), np.sin(phi_B)), xytext=(0, 0),
                arrowprops=dict(arrowstyle='->', color='red', lw=2.5))
    ax.text(np.cos(phi_B)*1.2, np.sin(phi_B)*1.2,
            'B (280Hz\nφ₀=20°)', fontsize=9, color='red', ha='center')

    # angle arc between A and B
    arc_th = np.linspace(np.radians(20), np.radians(50), 50)
    ax.plot(0.5*np.cos(arc_th), 0.5*np.sin(arc_th), 'purple', lw=2)
    ax.text(0.6*np.cos(np.radians(35)), 0.6*np.sin(np.radians(35)),
            'Δφ=30°', fontsize=9, color='purple', ha='center')

    ax.set_title('Q27: Phasor diagram\nA(240Hz,50°) sent 0.6s before B(280Hz,20°)')
    ax.axis('off')
    fig.tight_layout()
    return fig

# ════════════════════════════════════════════════════════════════════════════
# Q28 / Q29 — superposition on grid
# ════════════════════════════════════════════════════════════════════════════
def _q28():
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.set_xlim(0, 24); ax.set_ylim(-2, 4)
    for gx in range(0, 25): ax.axvline(gx, color='lightgray', lw=0.35)
    for gy in range(-2, 5):  ax.axhline(gy, color='lightgray', lw=0.35)
    ax.axhline(0, color='k', lw=1.2)

    px_r = [0, 2, 4, 6, 8, 24]
    py_r = [0, 0, 2, 0, 0,  0]
    ax.plot(px_r, py_r, 'b-', lw=2.5, label='Right-moving (blue)')
    ax.annotate('', xy=(9.5, 2.2), xytext=(8, 2.2),
                arrowprops=dict(arrowstyle='->', color='b', lw=2))

    px_l = [0, 14, 16, 18, 20, 22, 24]
    py_l = [0,  0,  0,  2,  0,  0,  0]
    ax.plot(px_l, py_l, 'r-', lw=2.5, label='Left-moving (red)')
    ax.annotate('', xy=(14.5, 2.2), xytext=(16, 2.2),
                arrowprops=dict(arrowstyle='->', color='r', lw=2))

    ax.set_xticks(range(0, 25, 2))
    ax.set_xlabel('Position (cells)')
    ax.set_title('Q28: Two pulses, v = 2 cells/s, t = 0')
    ax.legend(loc='upper right', fontsize=9)
    fig.tight_layout()
    return fig

def _q29():
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.set_xlim(0, 24); ax.set_ylim(-3, 4)
    for gx in range(0, 25): ax.axvline(gx, color='lightgray', lw=0.35)
    for gy in range(-2, 4):  ax.axhline(gy, color='lightgray', lw=0.35)
    ax.axhline(0, color='k', lw=1.2)

    px_r = [0, 1, 4, 7, 24]
    py_r = [0, 0, 3, 0,  0]
    ax.plot(px_r, py_r, 'b-', lw=2.5, label='Right-moving (blue)')
    ax.annotate('', xy=(8.5, 2.8), xytext=(7, 2.8),
                arrowprops=dict(arrowstyle='->', color='b', lw=2))

    px_l = [0, 15, 17, 19, 24]
    py_l = [0,  0,  2,  0,  0]
    ax.plot(px_l, py_l, 'r-', lw=2.5, label='Left-moving (red)')
    ax.annotate('', xy=(14, 2.3), xytext=(15.5, 2.3),
                arrowprops=dict(arrowstyle='->', color='r', lw=2))

    ax.set_xticks(range(0, 25, 2))
    ax.set_xlabel('Position (cells)')
    ax.set_title('Q29: Two pulses, v = 2 cells/s, t = 0')
    ax.legend(loc='upper right', fontsize=9)
    fig.tight_layout()
    return fig

# ════════════════════════════════════════════════════════════════════════════
# Q30, Q31
# ════════════════════════════════════════════════════════════════════════════
def _q30():
    fig, ax = plt.subplots(figsize=(10, 3.5))
    ax.set_xlim(0, 20); ax.set_ylim(-1, 3)
    for gx in range(0, 21): ax.axvline(gx, color='lightgray', lw=0.35)
    for gy in range(-1, 4):  ax.axhline(gy, color='lightgray', lw=0.35)
    ax.axhline(0, color='k', lw=1.2)
    ax.plot([0,2,4,6,8,20], [0,0,2,0,0,0], 'k-', lw=2.5)
    ax.annotate('', xy=(9.5,2.2), xytext=(8,2.2),
                arrowprops=dict(arrowstyle='->', color='k', lw=2))
    ax.set_xticks(range(0,21,2)); ax.set_xlabel('Position (cells)')
    ax.set_title('Q30: Pulse, v = 4 cells/s, t = 0  →')
    fig.tight_layout()
    return fig

def _q31():
    fig, ax = plt.subplots(figsize=(10, 3.5))
    ax.set_xlim(0, 20); ax.set_ylim(-1, 3)
    for gx in range(0, 21): ax.axvline(gx, color='lightgray', lw=0.35)
    for gy in range(-1, 4):  ax.axhline(gy, color='lightgray', lw=0.35)
    ax.axhline(0, color='k', lw=1.2)
    ax.plot([0,12,14,16,18,20],[0,0,2,0,0,0], 'k-', lw=2.5)
    ax.annotate('', xy=(17,2.2), xytext=(15.5,2.2),
                arrowprops=dict(arrowstyle='->', color='k', lw=2))
    ax.plot(20, 0, 'wo', ms=11, mec='k', mew=2.5, zorder=5)
    ax.text(20.2, 0.15, 'Free\nend', fontsize=8)
    ax.set_xticks(range(0,21,2)); ax.set_xlabel('Position (cells)')
    ax.set_title('Q31: Pulse → free end, v = 4 cells/s, t = 0')
    fig.tight_layout()
    return fig

# ════════════════════════════════════════════════════════════════════════════
# Q32 — refraction diagram with proper angle arcs
# ════════════════════════════════════════════════════════════════════════════
def _refrac(th1_deg, th2_deg, med1='Deep', med2='Shallow', title='',
            critical=False, v_ratio=''):
    """Draw refraction/reflection diagram matching textbook style."""
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_xlim(-4, 4); ax.set_ylim(-3.5, 4)
    ax.set_aspect('equal')

    # boundary (horizontal dashed line at y=0)
    ax.axhline(0, color='k', lw=2, ls='--')
    # normal (vertical dashed line)
    ax.axvline(0, color='gray', lw=1, ls=':', alpha=0.7)

    th1 = np.radians(th1_deg)
    th2 = np.radians(th2_deg)
    L   = 3.0

    # Incident ray: comes from upper-left toward origin
    ix, iy = -L*np.sin(th1), L*np.cos(th1)
    ax.annotate('', xy=(0, 0), xytext=(ix, iy),
                arrowprops=dict(arrowstyle='->', color='blue', lw=2.5,
                                mutation_scale=15))

    if critical:
        # Refracted ray goes along boundary (90°)
        ax.annotate('', xy=(L, 0), xytext=(0, 0),
                    arrowprops=dict(arrowstyle='->', color='red', lw=2.5,
                                    mutation_scale=15, ls='dashed'))
        # Reflected ray
        ax.annotate('', xy=(L*np.sin(th1), L*np.cos(th1)), xytext=(0, 0),
                    arrowprops=dict(arrowstyle='->', color='orange', lw=2,
                                    mutation_scale=12))
    else:
        rx, ry = L*np.sin(th2), -L*np.cos(th2)
        ax.annotate('', xy=(rx, ry), xytext=(0, 0),
                    arrowprops=dict(arrowstyle='->', color='red', lw=2.5,
                                    mutation_scale=15))

    # Angle arc for θ1 (between normal and incident)
    arc1_th = np.linspace(np.pi/2, np.pi/2 + th1, 40)
    ax.plot(0.8*np.cos(arc1_th), 0.8*np.sin(arc1_th), 'blue', lw=1.5)
    ax.text(-0.55, 0.9, f'θ₁={th1_deg}°', color='blue', fontsize=11,
            ha='right')

    if not critical:
        arc2_th = np.linspace(-np.pi/2, -np.pi/2 + th2, 40)
        ax.plot(0.8*np.cos(arc2_th), 0.8*np.sin(arc2_th), 'red', lw=1.5)
        ax.text(0.55, -0.9, f'θ₂={th2_deg}°', color='red', fontsize=11,
                ha='left')
    else:
        ax.text(1.0, 0.2, 'θ₂=90°', color='red', fontsize=11)

    # Medium labels
    ax.text(-3.8, 2.5, med1, fontsize=11, style='italic',
            bbox=dict(boxstyle='round,pad=0.2', fc='lightblue', alpha=0.5))
    ax.text(-3.8,-2.5, med2, fontsize=11, style='italic',
            bbox=dict(boxstyle='round,pad=0.2', fc='lightyellow', alpha=0.5))

    if v_ratio:
        ax.text(1.5, 3.2, v_ratio, fontsize=10, color='green')

    ax.set_title(title, fontsize=10, pad=8)
    ax.axis('off')
    fig.tight_layout()
    return fig

def _q32():
    return _refrac(60, 26, 'Deep (v₁)', 'Shallow (v₂=v₁/2)',
                   'Q32: Deep→Shallow\nθ₁=60°, v₁=2v₂ → θ₂≈26°',
                   v_ratio='v₁ = 2v₂')

def _q33():
    """Q33: deep→shallow, wavefront at 30° to boundary → θ₁≈41.8°"""
    fig, ax = plt.subplots(figsize=(7, 6))
    ax.set_xlim(-4, 4); ax.set_ylim(-3.5, 4)
    ax.set_aspect('equal')

    ax.axhline(0, color='k', lw=2, ls='--')
    ax.axvline(0, color='gray', lw=1, ls=':', alpha=0.7)

    th1 = np.radians(41.8)   # incident angle from normal (in deep water)
    th2 = np.radians(30)     # refracted angle from normal (in shallow water)
    L = 3.0

    # Incident ray
    ix, iy = -L*np.sin(th1), L*np.cos(th1)
    ax.annotate('', xy=(0, 0), xytext=(ix, iy),
                arrowprops=dict(arrowstyle='->', color='blue', lw=2.5, mutation_scale=15))

    # Refracted ray
    rx, ry = L*np.sin(th2), -L*np.cos(th2)
    ax.annotate('', xy=(rx, ry), xytext=(0, 0),
                arrowprops=dict(arrowstyle='->', color='red', lw=2.5, mutation_scale=15))

    # Angle arcs
    arc1 = np.linspace(np.pi/2, np.pi/2 + th1, 40)
    ax.plot(0.8*np.cos(arc1), 0.8*np.sin(arc1), 'blue', lw=1.5)
    ax.text(-0.65, 0.9, f'θ₁≈41.8°', color='blue', fontsize=10, ha='right')

    arc2 = np.linspace(-np.pi/2, -np.pi/2 + th2, 40)
    ax.plot(0.8*np.cos(arc2), 0.8*np.sin(arc2), 'red', lw=1.5)
    ax.text(0.5, -0.85, 'θ₂=30°', color='red', fontsize=10)

    # Wavefront lines (perpendicular to ray)
    for k in range(4):
        d = (k+1)*0.6
        # incident wavefronts in deep region
        cx, cy = -d*np.sin(th1), d*np.cos(th1)
        perp_x = np.cos(th1+np.pi/2)
        perp_y = np.sin(th1+np.pi/2)
        ax.plot([cx-perp_x, cx+perp_x], [cy-perp_y, cy+perp_y], 'b-', lw=1, alpha=0.5)

    for k in range(4):
        d = (k+0.5)*0.55
        cx, cy = d*np.sin(th2), -d*np.cos(th2)
        perp_x = np.cos(th2+np.pi/2)
        perp_y = np.sin(th2+np.pi/2)
        ax.plot([cx-perp_x, cx+perp_x], [cy-perp_y, cy+perp_y], 'r-', lw=1, alpha=0.5)

    # λ labels
    ax.text(-3.5, 2.2, 'น้ำลึก\nλ₁=2 cm', fontsize=10, color='blue',
            bbox=dict(boxstyle='round,pad=0.2', fc='lightblue', alpha=0.5))
    ax.text(-3.5, -2.5, 'น้ำตื้น\nλ₂=1.5 cm', fontsize=10, color='red',
            bbox=dict(boxstyle='round,pad=0.2', fc='lightyellow', alpha=0.5))

    # Wavefront angle label on boundary
    ax.text(1.4, 0.2, '30° จากรอยต่อ', fontsize=9, color='darkred')

    ax.set_title('Q33: น้ำลึก→น้ำตื้น\nλ₁=2cm, λ₂=1.5cm, θ₂จาก normal=30° → θ₁≈41.8°', fontsize=10)
    ax.axis('off')
    fig.tight_layout()
    return fig


def _q34():
    """Q34 wavefront diagram from PDF: parallel wavefronts in A and B with boundary"""
    fig, ax = plt.subplots(figsize=(7, 6))
    ax.set_xlim(0, 14); ax.set_ylim(0, 10)
    ax.set_aspect('equal')

    # Boundary (vertical line at x=7)
    ax.plot([7, 7], [0, 10], 'k-', lw=2.5)
    ax.text(1, 9.3, 'Zone A', fontsize=12, fontweight='bold', color='navy')
    ax.text(8, 9.3, 'Zone B', fontsize=12, fontweight='bold', color='darkred')

    # Wavefronts in A: lines at angle (θ_A=45° from normal → lines slope)
    # normal is horizontal; angle from normal = 45°
    # wavefront lines are perpendicular to the ray direction
    # Ray angle in A: 45° from horizontal → wavefronts at 45° to vertical
    for xi in [1.5, 3.0, 4.5, 6.0]:
        ax.plot([xi-2, xi+2], [1, 9], 'b-', lw=1.8, alpha=0.9)
    ax.text(1.8, 5.5, '45°', color='blue', fontsize=12, fontweight='bold')

    # Wavefronts in B: θ_B=30° from normal → steeper lines
    for xi in [8.0, 9.5, 11.0, 12.5]:
        ax.plot([xi-0.9, xi+0.9], [1, 9], 'r-', lw=1.8, alpha=0.9)
    ax.text(11, 5.5, '30°', color='red', fontsize=12, fontweight='bold')

    # Normal line at boundary (horizontal dashed)
    ax.plot([4, 10], [5, 5], 'gray', lw=1, ls='--', alpha=0.6)
    ax.text(10.2, 5, 'normal', fontsize=8, color='gray')

    ax.set_title('Q34: Wavefront refraction A→B\n(θ_A=45°, θ_B=30°, f=40 Hz)', fontsize=10)
    ax.axis('off')
    fig.tight_layout()
    return fig

def _q35():
    return _refrac(30, 60, 'Shallow (v₁)', 'Deep (v₂=√3·v₁)',
                   'Q35: Shallow→Deep\nθ₁=30°, λ₂=√3λ₁ → θ₂=60°',
                   v_ratio='v₂ = √3·v₁')

def _q36():
    return _refrac(45, 30, 'Deep (v₁)', 'Shallow (v₂)',
                   'Q36: Deep→Shallow\nθ₁=45°, θ₂=30°, λ₂=2√2 cm, f=20Hz → v₁=80 cm/s',
                   v_ratio='v₁=80 cm/s')

def _q37():
    return _refrac(37, 90, 'Deep (v₁=5v₂/3)', 'Shallow (v₂)',
                   'Q37: Critical angle (Deep→Shallow)\nsin θ_c = 3/5 → θ_c = 37°',
                   critical=True, v_ratio='sinθ_c = v₂/v₁ = 3/5')

def _q38():
    return _refrac(30, 90, 'Deep (v₁=2v₂)', 'Shallow (v₂)',
                   'Q38: Total internal reflection\nθ_c = 30°  (sinθ_c = 1/2)',
                   critical=True, v_ratio='v₁ = 2v₂')

def _q39():
    return _refrac(45, 90, 'Shallow (v₁)', 'Deep (v₂)',
                   'Q39: θ₁=30°→θ₂=45°, changed to θ₁=45°\nθ₂=90° (critical/total reflection)',
                   critical=True)

# ════════════════════════════════════════════════════════════════════════════
# Q41 — wavefront refraction from PDF: slanted parallel lines zone(ก)→(ข)
# ════════════════════════════════════════════════════════════════════════════
def _q41():
    fig, ax = plt.subplots(figsize=(7, 6))
    ax.set_xlim(0, 12); ax.set_ylim(0, 10)

    # Boundary at x=6
    ax.plot([6, 6], [0, 10], 'k-', lw=2.5)
    ax.text(0.5, 9.2, '(ก)', fontsize=13, fontweight='bold')
    ax.text(7.0, 9.2, '(ข)', fontsize=13, fontweight='bold')

    # Zone (ก): wavefronts at 60° angle from boundary (from PDF shows ~60°)
    # spacing=12cm
    for x0 in [1, 2.5, 4, 5.5]:
        ax.plot([x0-2.5, x0+0.5], [0.5, 9.5], 'b-', lw=1.8)

    # Zone (ข): wavefronts at 45° from boundary
    for x0 in [7, 8.5, 10, 11.5]:
        ax.plot([x0-1.5, x0+1.5], [0.5, 9.5], 'r-', lw=1.8)

    # Angle labels
    ax.text(3.5, 2.5, '60°', color='blue', fontsize=13, fontweight='bold')
    ax.text(9.0, 2.5, '45°', color='red',  fontsize=13, fontweight='bold')

    ax.set_title('Q41: Wavefront refraction (ก)→(ข)\n'
                 'λ(ก)=12 cm, v(ข)=6√2 cm/s → f≈0.87 Hz', fontsize=10)
    ax.axis('off')
    fig.tight_layout()
    return fig

# ════════════════════════════════════════════════════════════════════════════
# Q42 — three cases: deep/shallow boundary shapes from PDF
# ════════════════════════════════════════════════════════════════════════════
def _q42():
    fig, axes = plt.subplots(1, 3, figsize=(12, 5))

    configs = [
        # (title, deep_label_pos, shallow_label_pos, boundary_type)
        ('Fig(1)\nDeep△ on top,\nShallow bottom', 'top', 'bottom', 'V'),
        ('Fig(2)\nShallow△ on top,\nDeep sides',   'bottom','top',  'V2'),
        ('Fig(3)\nDeep left,\nShallow right',       'left', 'right', 'diag'),
    ]

    for ax, (title, d_side, s_side, btype) in zip(axes, configs):
        ax.set_xlim(0, 8); ax.set_ylim(0, 8)

        if btype == 'V':
            # V-shape boundary: deep triangle on top, shallow on bottom
            ax.fill_between([0,8], [8,8], [4,4], alpha=0.15, color='blue')
            ax.fill_between([0,8], [4,4], [0,0], alpha=0.15, color='yellow')
            # Boundary V shape
            bx = [0, 4, 8]; by = [4, 2, 4]
            ax.plot(bx, by, 'k-', lw=2)
            ax.text(1, 6.5, 'Deep (ลึก)',   fontsize=9, color='blue')
            ax.text(1, 1.0, 'Shallow (ตื้น)', fontsize=9, color='saddlebrown')
            # source below
            ax.plot(4, 0.5, 'k^', ms=10, zorder=5)
            ax.text(4, 0.0, 'Source', ha='center', fontsize=8)
            # wavefronts (concentric partial circles)
            for r in [1.5, 3.0, 4.5]:
                th = np.linspace(0, np.pi, 100)
                ax.plot(4+r*np.cos(th), 0.5+r*np.sin(th), 'b-', lw=1, alpha=0.6)

        elif btype == 'V2':
            # Inverted V: shallow on top
            ax.fill_between([0,8],[8,8],[4,4], alpha=0.15, color='yellow')
            ax.fill_between([0,8],[4,4],[0,0], alpha=0.15, color='blue')
            bx = [0, 4, 8]; by = [4, 6, 4]
            ax.plot(bx, by, 'k-', lw=2)
            ax.text(1, 7,   'Shallow', fontsize=9, color='saddlebrown')
            ax.text(1, 1.5, 'Deep',    fontsize=9, color='blue')
            ax.plot(4, 0.5, 'k^', ms=10, zorder=5)
            for r in [1.5, 3.0, 4.5]:
                th = np.linspace(0, np.pi, 100)
                ax.plot(4+r*np.cos(th), 0.5+r*np.sin(th), 'b-', lw=1, alpha=0.6)

        else:
            # diagonal boundary
            ax.fill_between([0,8],[8,8],[8,0], alpha=0.15, color='blue')
            ax.fill_between([0,8],[8,0],[0,0], alpha=0.15, color='yellow')
            ax.plot([0,8],[8,0],'k-',lw=2)
            ax.text(0.5,7,'Deep',fontsize=9,color='blue')
            ax.text(5,1,'Shallow',fontsize=9,color='saddlebrown')
            ax.plot(0.5, 0.5, 'k^', ms=10, zorder=5)
            for r in [1.5, 3.0, 4.5]:
                th = np.linspace(-np.pi/4, 3*np.pi/4, 100)
                ax.plot(0.5+r*np.cos(th), 0.5+r*np.sin(th), 'b-', lw=1, alpha=0.6)

        ax.set_title(title, fontsize=9)
        ax.axis('off')

    fig.suptitle('Q42: Wave refraction at deep/shallow boundary (3 cases)', y=1.01)
    fig.tight_layout()
    return fig

# ════════════════════════════════════════════════════════════════════════════
# Q43 — Two coherent sources d=10cm, λ=2.5cm
# ════════════════════════════════════════════════════════════════════════════
def _q43():
    fig, ax = plt.subplots(figsize=(8, 6))
    d, lam = 10, 2.5
    n_max = int(d/lam)
    ax.plot(0, d/2, 'ro', ms=9, zorder=5)
    ax.plot(0,-d/2, 'bs', ms=9, zorder=5)
    ax.annotate(r'$S_1$', (0, d/2),  xytext=(-16, 0), textcoords='offset points',
                fontsize=12, color='red', fontweight='bold')
    ax.annotate(r'$S_2$', (0,-d/2), xytext=(-16,-12), textcoords='offset points',
                fontsize=12, color='blue', fontweight='bold')

    r_max = 28
    for n in range(-n_max, n_max+1):
        val = n*lam/d
        if abs(val) <= 1:
            th = np.arcsin(val)
            ax.plot([0, r_max*np.cos(th)], [0, r_max*np.sin(th)],
                    'g-', lw=1, alpha=0.5)
    for n in range(1, n_max+1):
        for sign in [1,-1]:
            val = (n-0.5)*lam/d
            if abs(val) <= 1:
                th = np.arcsin(sign*val)
                ax.plot([0, r_max*np.cos(th)], [0, r_max*np.sin(th)],
                        'r--', lw=0.8, alpha=0.4)

    pts = {'A': (17, 8), 'B': (14.5, 0.6), 'C': (24, 0)}
    colors = {'A':'purple','B':'darkorange','C':'teal'}
    for name, (px, py) in pts.items():
        ax.plot(px, py, 'D', color=colors[name], ms=8, zorder=5)
        ax.annotate(name, (px,py), xytext=(4,4), textcoords='offset points',
                    fontsize=12, color=colors[name], fontweight='bold')

    ax.axhline(0, color='gray', lw=0.5, ls='--')
    ax.set_xlim(-3, 30); ax.set_ylim(-10, 10)
    ax.set_xlabel('x (cm)'); ax.set_ylabel('y (cm)')
    ax.set_title('Q43: d=10 cm, λ=2.5 cm  (green=antinode, red-dash=node)')
    fig.tight_layout()
    return fig

# ════════════════════════════════════════════════════════════════════════════
# Q44 — d=12cm, λ=4cm
# ════════════════════════════════════════════════════════════════════════════
def _q44():
    fig, ax = plt.subplots(figsize=(8, 6))
    d, lam = 12, 4
    n_max = int(d/lam)
    ax.plot(0, d/2, 'ro', ms=9); ax.plot(0,-d/2, 'bs', ms=9)
    ax.annotate(r'$S_1$',(0,d/2), xytext=(-16,0), textcoords='offset points',
                fontsize=11, color='red')
    ax.annotate(r'$S_2$',(0,-d/2), xytext=(-16,-12), textcoords='offset points',
                fontsize=11, color='blue')

    r_max = 30
    for n in range(-n_max, n_max+1):
        val = n*lam/d
        if abs(val)<=1:
            th = np.arcsin(val)
            ax.plot([0,r_max*np.cos(th)],[0,r_max*np.sin(th)],'g-',lw=1.2,alpha=0.6)
            ax.text(r_max*np.cos(th)*1.04, r_max*np.sin(th)*1.04,
                    f'A{abs(n)}', fontsize=8, color='green')
    for n in range(1, n_max+1):
        for sign in [1,-1]:
            val = (n-0.5)*lam/d
            if abs(val)<=1:
                th = np.arcsin(sign*val)
                ax.plot([0,r_max*np.cos(th)],[0,r_max*np.sin(th)],'r--',lw=0.8,alpha=0.5)

    ax.plot(0, 19, 'k^', ms=9, zorder=5)
    ax.annotate('X (r₁=19,r₂=25)', (0,19), xytext=(2,0),
                textcoords='offset points', fontsize=9)
    ax.plot([0,0],[d/2,25],'k:',lw=1)
    ax.set_xlim(-5,32); ax.set_ylim(-16,26)
    ax.set_xlabel('x (cm)'); ax.set_ylabel('y (cm)')
    ax.set_title('Q44: d=12 cm, λ=4 cm  →  X on N₂ (path diff=6=1.5λ)')
    fig.tight_layout()
    return fig

# ════════════════════════════════════════════════════════════════════════════
# Q47 — interference pattern showing S1 S2 with solid (antinode) and
#        dashed (node) lines — from PDF figure
# ════════════════════════════════════════════════════════════════════════════
def _q47():
    fig, ax = plt.subplots(figsize=(8, 6))
    # Two sources on left side
    ax.plot(-3, 1, 'ko', ms=8, zorder=5)
    ax.plot(-3,-1, 'ko', ms=8, zorder=5)
    ax.annotate(r'$S_1$', (-3,1),  xytext=(-8, 2), textcoords='offset points',
                fontsize=11)
    ax.annotate(r'$S_2$', (-3,-1), xytext=(-8,-10), textcoords='offset points',
                fontsize=11)

    # Draw wavefronts from each source (circular arcs)
    for src_y, color in [(1,'blue'),(-1,'red')]:
        for r in [1.5, 3, 4.5, 6, 7.5]:
            th = np.linspace(-np.pi*0.6, np.pi*0.6, 120)
            ax.plot(-3+r*np.cos(th), src_y+r*np.sin(th), '-',
                    color=color, lw=0.8, alpha=0.4)

    # Antinodal lines (solid green) — d=2λ case from PDF
    d, lam = 2, 1  # normalized
    n_max = 2
    r_max = 10
    for n in range(-n_max, n_max+1):
        val = n*lam/d
        if abs(val)<=1:
            th = np.arcsin(val)
            x_end = r_max*np.cos(th) - 3
            y_end = r_max*np.sin(th)
            ax.plot([-3, x_end], [0, y_end], 'g-', lw=2, alpha=0.8)
    # Nodal lines (dashed red)
    for n in range(1, n_max+1):
        for sign in [1,-1]:
            val = (n-0.5)*lam/d
            if abs(val)<=1:
                th = np.arcsin(sign*val)
                x_end = r_max*np.cos(th) - 3
                y_end = r_max*np.sin(th)
                ax.plot([-3, x_end], [0, y_end], 'r--', lw=1.5, alpha=0.7)

    ax.set_xlim(-4, 8); ax.set_ylim(-6, 6)
    ax.set_xlabel('x'); ax.set_ylabel('y')
    ax.set_title('Q47: Interference pattern, d=2λ\n(solid green=antinode, red-dash=node)')
    fig.tight_layout()
    return fig

# ════════════════════════════════════════════════════════════════════════════
# Q48 — from PDF: S1---x---S2 horizontal, P below at angle θ from S1S2 line
# ════════════════════════════════════════════════════════════════════════════
def _q48():
    fig, ax = plt.subplots(figsize=(7, 6))
    ax.set_xlim(-1, 8); ax.set_ylim(-5, 2)
    ax.set_aspect('equal')

    # S1 at (0,0), S2 at (6,0) — x=S1S2 distance
    s1 = np.array([0.0, 0.0])
    s2 = np.array([6.0, 0.0])
    ax.plot(*s1, 'ro', ms=9, zorder=5)
    ax.plot(*s2, 'bs', ms=9, zorder=5)
    ax.text(s1[0]-0.1, s1[1]+0.2, r'$S_1$', fontsize=12, color='red', ha='right')
    ax.text(s2[0]+0.1, s2[1]+0.2, r'$S_2$', fontsize=12, color='blue')

    # x-distance arrow above
    ax.annotate('', xy=(6, 1.5), xytext=(0, 1.5),
                arrowprops=dict(arrowstyle='<->', color='k', lw=1.5))
    ax.text(3, 1.7, 'x', ha='center', fontsize=14)

    # O directly below S1, P to the right of O
    O = np.array([0.0, -4.0])
    P = np.array([4.0, -4.0])
    ax.plot(*O, 'k.', ms=5)
    ax.plot(*P, 'k^', ms=8, zorder=5)
    ax.text(O[0]-0.1, O[1]-0.2, 'O', ha='right', fontsize=12)
    ax.text(P[0]+0.1, P[1]-0.2, 'P', ha='left',  fontsize=12)

    # Lines from sources to P
    ax.plot([s1[0], P[0]], [s1[1], P[1]], 'b-', lw=1.5, alpha=0.6)
    ax.plot([s2[0], P[0]], [s2[1], P[1]], 'r-', lw=1.5, alpha=0.6)

    # Vertical line S1→O
    ax.plot([s1[0], O[0]], [s1[1], O[1]], 'k-', lw=1)

    # θ angle at S1
    th_val = np.arctan2(P[1]-s1[1], P[0]-s1[0])
    th_deg = abs(np.degrees(th_val))
    arc_th = np.linspace(np.radians(-90), th_val, 40)
    ax.plot(0.8*np.cos(arc_th), 0.8*np.sin(arc_th), 'purple', lw=1.5)
    ax.text(0.5, -1.0, f'θ', color='purple', fontsize=13)

    ax.set_title('Q48: S₁S₂=x, P on 2nd antinode\n'
                 r'$\sin\theta = 2\lambda/x$', fontsize=10)
    ax.axis('off')
    fig.tight_layout()
    return fig

# ════════════════════════════════════════════════════════════════════════════
# Q49 — d=6cm, 1st antinode at 30°
# ════════════════════════════════════════════════════════════════════════════
def _q49():
    fig, ax = plt.subplots(figsize=(6, 5))
    ax.set_aspect('equal')
    d = 6
    ax.plot(0, d/2, 'ro', ms=9); ax.plot(0,-d/2, 'bs', ms=9)
    ax.annotate(r'$S_1$',(0,d/2),  xytext=(-16,0),  textcoords='offset points',
                fontsize=11, color='red')
    ax.annotate(r'$S_2$',(0,-d/2), xytext=(-16,-12), textcoords='offset points',
                fontsize=11, color='blue')
    r = 10
    for sign in [1,-1]:
        th = sign*np.radians(30)
        ax.annotate('', xy=(r*np.cos(th), r*np.sin(th)), xytext=(0,0),
                    arrowprops=dict(arrowstyle='->', color='green', lw=2.5))
    ax.axhline(0, color='gray', lw=0.8, ls='--')
    ax.text(5, 3.2, '30°', fontsize=12, color='green')
    ax.text(5,-3.8, '30°', fontsize=12, color='green')
    ax.set_xlim(-3, 12); ax.set_ylim(-8, 8)
    ax.set_title('Q49: d=6 cm, 1st antinode at ±30°\n→ λ = d·sin30° = 3 cm')
    ax.axis('off')
    fig.tight_layout()
    return fig

# ════════════════════════════════════════════════════════════════════════════
# Q50 — from PDF: S1(top), S2(bottom), both on LEFT, vertical screen at right,
#        θ angle at sources, O on screen (center), P above O, x = distance O→P
# ════════════════════════════════════════════════════════════════════════════
def _q50():
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.set_xlim(-1, 9); ax.set_ylim(-4, 4)

    # Sources S1 top, S2 bottom, centered at x=0
    s1 = np.array([0.0,  0.5])
    s2 = np.array([0.0, -0.5])
    ax.plot(*s1, 'ro', ms=9, zorder=5)
    ax.plot(*s2, 'bs', ms=9, zorder=5)
    ax.text(s1[0]-0.15, s1[1]+0.15, r'$S_1$', fontsize=12, color='red', ha='right')
    ax.text(s2[0]-0.15, s2[1]-0.25, r'$S_2$', fontsize=12, color='blue', ha='right')

    # Screen (vertical line at x=7.5, representing L=60cm)
    ax.plot([7.5, 7.5], [-3.5, 3.5], 'k-', lw=3)

    # O = center on screen, P = 1st antinode above
    O = np.array([7.5, 0.0])
    P = np.array([7.5, 0.6])  # x = 6cm scaled
    ax.plot(*O, 'ko', ms=6, zorder=5)
    ax.plot(*P, 'g^', ms=10, zorder=5)
    ax.text(O[0]+0.15, O[1]-0.1, r'$A_0$', fontsize=11, color='k')
    ax.text(P[0]+0.15, P[1],     'P', fontsize=11, color='green')

    # Ray from S1 to P
    ax.plot([s1[0], P[0]], [s1[1], P[1]], 'g--', lw=1.5, alpha=0.7)
    ax.plot([s2[0], P[0]], [s2[1], P[1]], 'g--', lw=1.5, alpha=0.7)

    # Horizontal center line
    ax.plot([0, 7.5], [0, 0], 'k:', lw=1)

    # θ angle arc at source midpoint
    mid = (s1+s2)/2
    th_val = np.arctan2(P[1]-mid[1], P[0]-mid[0])
    arc_t = np.linspace(0, th_val, 40)
    ax.plot(mid[0]+1.5*np.cos(arc_t), mid[1]+1.5*np.sin(arc_t), 'purple', lw=2)
    ax.text(mid[0]+1.7, mid[1]+0.15, 'θ', fontsize=13, color='purple')

    # x distance arrow on screen
    ax.annotate('', xy=(7.8, P[1]), xytext=(7.8, 0),
                arrowprops=dict(arrowstyle='<->', color='k', lw=1.5))
    ax.text(8.1, P[1]/2, 'x=6 cm', fontsize=10, color='k', va='center')

    # L label below
    ax.annotate('', xy=(7.5,-3.0), xytext=(0,-3.0),
                arrowprops=dict(arrowstyle='<->', color='k', lw=1.5))
    ax.text(3.75, -3.3, 'L = 60 cm', ha='center', fontsize=10)

    ax.set_title('Q50: d=10 cm, λ=1 cm, L=60 cm\n→ x = Lλ/d = 6 cm', fontsize=10)
    ax.axis('off')
    fig.tight_layout()
    return fig

# ════════════════════════════════════════════════════════════════════════════
# Q51 — from PDF: reflector at top, S below it 8cm, P to the side 12cm from S
# ════════════════════════════════════════════════════════════════════════════
def _q51():
    fig, ax = plt.subplots(figsize=(7, 6))
    ax.set_xlim(-2, 14); ax.set_ylim(-2, 12)
    ax.set_aspect('equal')

    # Reflector at top (hatched wall)
    ax.fill_between([0, 12], [10, 10], [10.6, 10.6], color='gray', alpha=0.8)
    for xi in np.arange(0.5, 12, 0.8):
        ax.plot([xi, xi-0.4], [10, 10.5], 'k-', lw=0.8)
    ax.text(6, 11, 'Reflector', ha='center', fontsize=10)

    # Source S at (6, 2) — 8cm below reflector
    S = np.array([6.0, 2.0])
    ax.plot(*S, 'ko', ms=10, zorder=5)
    ax.text(S[0]-0.4, S[1]-0.5, 'S', fontsize=13, fontweight='bold')

    # Dimension: S to reflector = 8 cm
    ax.annotate('', xy=(6,10), xytext=(6, 2),
                arrowprops=dict(arrowstyle='<->', color='k', lw=1.5))
    ax.text(6.2, 6, '8 cm', fontsize=10, va='center')

    # Image source S' (mirror of S) at (6, 18) — above reflector
    Sp = np.array([6.0, 18.0])  # Not drawn, used conceptually

    # Point P: 12cm from S — place to the right
    P = np.array([6+12*np.cos(np.radians(30)), 2+12*np.sin(np.radians(30))])
    ax.plot(*P, 'r^', ms=10, zorder=5)
    ax.text(P[0]+0.2, P[1]+0.2, 'P', fontsize=13, color='red', fontweight='bold')

    # Line S to P
    ax.plot([S[0], P[0]], [S[1], P[1]], 'b-', lw=1.5)
    ax.text((S[0]+P[0])/2+0.3, (S[1]+P[1])/2, '12 cm', fontsize=10, color='blue')

    # Circular wavefronts from S
    for r in [3, 6, 9]:
        th = np.linspace(-np.pi/2, np.pi/2, 120)
        ax.plot(S[0]+r*np.cos(th), S[1]+r*np.sin(th), 'b-', lw=0.8, alpha=0.4)

    ax.set_title('Q51: S 8 cm from reflector, P 12 cm from S\n'
                 'λ=4 cm → find interference type at P', fontsize=10)
    ax.axis('off')
    fig.tight_layout()
    return fig

# ════════════════════════════════════════════════════════════════════════════
# Q52 — from PDF: S1 left, S2 right (horizontal), P axis vertical from S1
# ════════════════════════════════════════════════════════════════════════════
def _q52():
    fig, ax = plt.subplots(figsize=(7, 7))
    ax.set_xlim(-1, 5); ax.set_ylim(-1, 6)

    # S1 at (0,0), S2 at (2,0)  (d=2m)
    s1 = np.array([0.0, 0.0])
    s2 = np.array([2.0, 0.0])
    ax.plot(*s1, 'ro', ms=10, zorder=5)
    ax.plot(*s2, 'bs', ms=10, zorder=5)
    ax.text(s1[0]-0.15, s1[1]-0.25, r'$S_1$', fontsize=13, color='red',   ha='right')
    ax.text(s2[0]+0.1,  s2[1]-0.25, r'$S_2$', fontsize=13, color='blue')

    # Horizontal line S1→S2
    ax.annotate('', xy=(2,0), xytext=(0,0),
                arrowprops=dict(arrowstyle='->', color='k', lw=1.5))

    # P-axis: vertical from S1 upward (S1P perpendicular to S1S2)
    ax.annotate('', xy=(0, 5.5), xytext=(0, 0),
                arrowprops=dict(arrowstyle='->', color='k', lw=1.5))
    ax.text(-0.1, 5.7, 'P', fontsize=13, ha='right')

    # Antinodal intersection points on S1P axis
    # From solution: y = 3.75, 1.5, 0.58, 0
    ys = [3.75, 1.5, 0.58, 0.0]
    ns = ['n=1','n=2','n=3','n=4']
    for y, label in zip(ys, ns):
        ax.plot(0, y, 'g^', ms=9, zorder=5)
        ax.text(0.12, y, label, fontsize=9, color='green', va='center')
        # Dashed line to S2
        ax.plot([0, 2], [y, 0], 'gray', lw=0.8, ls='--', alpha=0.6)

    ax.set_title('Q52: S₁S₂=2m, λ=0.5m, f=20Hz\nAntinodal lines cut S₁P axis',
                 fontsize=10)
    ax.axis('off')
    fig.tight_layout()
    return fig

# ════════════════════════════════════════════════════════════════════════════
# Q53 — wire 40 cm, 1 loop
# ════════════════════════════════════════════════════════════════════════════
def _q53():
    fig, ax = plt.subplots(figsize=(7, 3))
    L = 40
    x = np.linspace(0, L, 300)
    ax.fill_between(x, np.sin(np.pi*x/L)*1.5, -np.sin(np.pi*x/L)*1.5,
                    alpha=0.15, color='blue')
    ax.plot(x,  np.sin(np.pi*x/L)*1.5, 'b-', lw=2.5)
    ax.plot(x, -np.sin(np.pi*x/L)*1.5, 'b--', lw=1.5, alpha=0.5)
    ax.axhline(0, color='k', lw=1)
    for xend in [0, L]:
        ax.plot(xend, 0, 'ks', ms=10, zorder=5)
    ax.annotate('', xy=(L,-2), xytext=(0,-2),
                arrowprops=dict(arrowstyle='<->', color='k', lw=1.5))
    ax.text(L/2, -2.6, '40 cm', ha='center', fontsize=10)
    ax.set_xlim(-3, L+3); ax.set_ylim(-3.5, 3)
    ax.set_title('Q53: Wire L=40 cm, 1 loop, f=20 Hz → v=16 m/s')
    ax.axis('off')
    fig.tight_layout()
    return fig

# ════════════════════════════════════════════════════════════════════════════
# Q54 — rope 3m, λ=0.5m, 12 loops
# ════════════════════════════════════════════════════════════════════════════
def _q54():
    fig, ax = plt.subplots(figsize=(10, 3))
    L, n = 3.0, 12
    x = np.linspace(0, L, 600)
    ax.fill_between(x, np.sin(n*np.pi*x/L)*0.8, -np.sin(n*np.pi*x/L)*0.8,
                    alpha=0.12, color='blue')
    ax.plot(x,  np.sin(n*np.pi*x/L)*0.8, 'b-', lw=2)
    ax.plot(x, -np.sin(n*np.pi*x/L)*0.8, 'b--', lw=1, alpha=0.5)
    ax.axhline(0, color='k', lw=1)
    ax.plot(0, 0, 'ks', ms=10, zorder=5)
    ax.plot(L, 0, 'ws', ms=10, mec='k', mew=2, zorder=5)
    ax.text(-0.1, 0, 'A', ha='right', fontsize=11, fontweight='bold')
    ax.text(L+0.1, 0, 'B', ha='left',  fontsize=11, fontweight='bold')
    ax.annotate('', xy=(L,-1.2), xytext=(0,-1.2),
                arrowprops=dict(arrowstyle='<->', color='k', lw=1.5))
    ax.text(L/2, -1.5, '3 m, λ=0.5 m → 12 loops, 13 nodes, 12 antinodes',
            ha='center', fontsize=9)
    ax.set_xlim(-0.3, L+0.3); ax.set_ylim(-2, 1.5)
    ax.set_title('Q54: Rope L=3 m, λ=0.5 m')
    ax.axis('off')
    fig.tight_layout()
    return fig

# ════════════════════════════════════════════════════════════════════════════
# Q55 — source 20cm from reflector, λ=4cm
# ════════════════════════════════════════════════════════════════════════════
def _q55():
    fig, ax = plt.subplots(figsize=(9, 3.5))
    L, lam = 20, 4
    x = np.linspace(0, L, 500)
    ax.fill_between(x, np.sin(2*np.pi*x/lam)*0.8, -np.sin(2*np.pi*x/lam)*0.8,
                    alpha=0.12, color='blue')
    ax.plot(x,  np.sin(2*np.pi*x/lam)*0.8, 'b-', lw=2)
    ax.plot(x, -np.sin(2*np.pi*x/lam)*0.8, 'b--', lw=1, alpha=0.4)
    ax.axhline(0, color='k', lw=1)

    nodes = np.arange(0, L+0.1, lam/2)
    anti  = np.arange(lam/4, L, lam/2)
    ax.plot(nodes, np.zeros_like(nodes), 'rv', ms=7, zorder=5, label=f'N ({len(nodes)}=11)')
    ax.plot(anti,  np.zeros_like(anti),  'g^', ms=7, zorder=5, label=f'A ({len(anti)}=10)')

    ax.plot(0, 0, 'ko', ms=10, zorder=6)
    ax.text(-0.5, 0.3, 'S', fontsize=11, fontweight='bold')
    ax.axvline(L, color='k', lw=3)
    ax.text(L+0.3, 0.3, 'Reflector', fontsize=9)
    ax.annotate('', xy=(L,-1.2), xytext=(0,-1.2),
                arrowprops=dict(arrowstyle='<->', color='k', lw=1.5))
    ax.text(L/2, -1.5, '20 cm = 5λ', ha='center', fontsize=9)
    ax.set_xlim(-1.5, L+2.5); ax.set_ylim(-2, 1.5)
    ax.set_title('Q55: S 20cm from reflector, λ=4cm → 11 nodes, 10 antinodes')
    ax.legend(loc='upper right', fontsize=9)
    ax.axis('off')
    fig.tight_layout()
    return fig

# ════════════════════════════════════════════════════════════════════════════
# Q56 — spring 20cm, λ=8cm
# ════════════════════════════════════════════════════════════════════════════
def _q56():
    fig, ax = plt.subplots(figsize=(9, 3))
    L, lam = 20, 8
    n = int(2*L/lam)
    x = np.linspace(0, L, 400)
    ax.fill_between(x, np.sin(n*np.pi*x/L)*0.9, -np.sin(n*np.pi*x/L)*0.9,
                    alpha=0.12, color='blue')
    ax.plot(x,  np.sin(n*np.pi*x/L)*0.9, 'b-', lw=2)
    ax.plot(x, -np.sin(n*np.pi*x/L)*0.9, 'b--', lw=1, alpha=0.4)
    ax.axhline(0, color='k', lw=1)
    nodes = np.arange(0, L+0.1, lam/2)
    anti  = np.arange(lam/4, L, lam/2)
    ax.plot(nodes, np.zeros_like(nodes), 'rv', ms=7, zorder=5, label=f'N=6')
    ax.plot(anti,  np.zeros_like(anti),  'g^', ms=7, zorder=5, label=f'A=5')
    ax.plot(0, 0, 'ks', ms=10, zorder=6); ax.plot(L, 0, 'ks', ms=10, zorder=6)
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
# Q57 — node spacing=10cm, v=160cm/s
# ════════════════════════════════════════════════════════════════════════════
def _q57():
    fig, ax = plt.subplots(figsize=(9, 3))
    lam, L = 20, 60
    x = np.linspace(0, L, 500)
    ax.fill_between(x, np.sin(2*np.pi*x/lam)*0.9, -np.sin(2*np.pi*x/lam)*0.9,
                    alpha=0.12, color='blue')
    ax.plot(x,  np.sin(2*np.pi*x/lam)*0.9, 'b-', lw=2)
    ax.plot(x, -np.sin(2*np.pi*x/lam)*0.9, 'b--', lw=1, alpha=0.4)
    ax.axhline(0, color='k', lw=1)
    nodes = np.arange(0, L+0.1, 10)
    ax.plot(nodes, np.zeros_like(nodes), 'rv', ms=8, zorder=5, label='Node')
    ax.annotate('', xy=(10,-1.3), xytext=(0,-1.3),
                arrowprops=dict(arrowstyle='<->', color='k', lw=1.5))
    ax.text(5, -1.6, '10 cm', ha='center', fontsize=9)
    ax.set_xlim(-2, L+2); ax.set_ylim(-2, 1.5)
    ax.set_title('Q57: Node spacing=10cm, v=160cm/s → f=8Hz')
    ax.legend(loc='upper right', fontsize=9)
    ax.axis('off')
    fig.tight_layout()
    return fig

# ════════════════════════════════════════════════════════════════════════════
# Q59 — L=1.25m, resonance modes
# ════════════════════════════════════════════════════════════════════════════
def _q59():
    fig, axes = plt.subplots(1, 3, figsize=(12, 3.5))
    L = 1.25
    for idx, (n, f, lbl) in enumerate([(1,64,'n=1\nf=64 Hz'),
                                        (2,128,'n=2\nf=128 Hz'),
                                        (3,192,'n=3\nf=192 Hz')]):
        ax = axes[idx]
        x = np.linspace(0, L, 300)
        ax.fill_between(x, np.sin(n*np.pi*x/L)*0.8, -np.sin(n*np.pi*x/L)*0.8,
                        alpha=0.12, color='blue')
        ax.plot(x,  np.sin(n*np.pi*x/L)*0.8, 'b-', lw=2)
        ax.plot(x, -np.sin(n*np.pi*x/L)*0.8, 'b--', lw=1, alpha=0.5)
        ax.axhline(0, color='k', lw=1)
        ax.plot(0, 0, 'ks', ms=8); ax.plot(L, 0, 'ks', ms=8)
        ax.annotate('', xy=(L,-1.2), xytext=(0,-1.2),
                    arrowprops=dict(arrowstyle='<->', color='k', lw=1.2))
        ax.text(L/2, -1.5, '1.25 m', ha='center', fontsize=8)
        ax.set_title(lbl, fontsize=9); ax.set_ylim(-2, 1.2); ax.axis('off')
    fig.suptitle('Q59: Resonance L=1.25m, v=160m/s', y=1.02)
    fig.tight_layout()
    return fig

# ════════════════════════════════════════════════════════════════════════════
# Q60 — L=1.20m, 2nd overtone (n=3)
# ════════════════════════════════════════════════════════════════════════════
def _q60():
    fig, ax = plt.subplots(figsize=(8, 3))
    L, n = 1.20, 3
    x = np.linspace(0, L, 300)
    ax.fill_between(x, np.sin(n*np.pi*x/L)*0.8, -np.sin(n*np.pi*x/L)*0.8,
                    alpha=0.12, color='blue')
    ax.plot(x,  np.sin(n*np.pi*x/L)*0.8, 'b-', lw=2.5)
    ax.plot(x, -np.sin(n*np.pi*x/L)*0.8, 'b--', lw=1.5, alpha=0.5)
    ax.axhline(0, color='k', lw=1)
    ax.plot(0, 0, 'ks', ms=10); ax.plot(L, 0, 'ks', ms=10)
    ax.annotate('', xy=(L,-1.1), xytext=(0,-1.1),
                arrowprops=dict(arrowstyle='<->', color='k', lw=1.5))
    ax.text(L/2, -1.4, '1.20 m', ha='center', fontsize=10)
    ax.set_xlim(-0.05, L+0.05); ax.set_ylim(-2, 1.2)
    ax.set_title('Q60: 2nd overtone (n=3), f=320Hz → v=256 m/s')
    ax.axis('off')
    fig.tight_layout()
    return fig

# ════════════════════════════════════════════════════════════════════════════
# Q61 — rope 0.9m, harmonic 4 (4 loops)
# ════════════════════════════════════════════════════════════════════════════
def _q61():
    fig, ax = plt.subplots(figsize=(8, 3))
    L, n = 0.9, 4
    x = np.linspace(0, L, 300)
    ax.fill_between(x, np.sin(n*np.pi*x/L)*0.8, -np.sin(n*np.pi*x/L)*0.8,
                    alpha=0.12, color='blue')
    ax.plot(x,  np.sin(n*np.pi*x/L)*0.8, 'b-', lw=2.5)
    ax.plot(x, -np.sin(n*np.pi*x/L)*0.8, 'b--', lw=1.5, alpha=0.5)
    ax.axhline(0, color='k', lw=1)
    # Hatched fixed ends
    ax.plot(0, 0, 'ks', ms=12, zorder=5); ax.plot(L, 0, 'ks', ms=12, zorder=5)
    # λ/2 label
    ax.annotate('', xy=(L/n, -1.2), xytext=(0, -1.2),
                arrowprops=dict(arrowstyle='<->', color='purple', lw=1.5))
    ax.text(L/(2*n), -1.5, r'$\lambda/2$', ha='center', fontsize=10, color='purple')
    ax.annotate('', xy=(L,-1.8), xytext=(0,-1.8),
                arrowprops=dict(arrowstyle='<->', color='k', lw=1.5))
    ax.text(L/2, -2.1, 'L = 0.9 m', ha='center', fontsize=10)
    ax.set_xlim(-0.05, L+0.05); ax.set_ylim(-2.5, 1.2)
    ax.set_title('Q61: 4th harmonic (4 loops), L=0.9m, T=100N → f≈88.9Hz')
    ax.axis('off')
    fig.tight_layout()
    return fig

# ════════════════════════════════════════════════════════════════════════════
# Q62 — guitar string: 2 loops (T=40N) vs 3 loops (T=90N)
# ════════════════════════════════════════════════════════════════════════════
def _q62():
    fig, axes = plt.subplots(1, 2, figsize=(11, 3.5))
    L = 0.75   # 75 cm vibrating length
    mu = 0.01296  # kg/m (12.96 g / 1 m)

    configs = [
        (40, 2, 'T = 40 N → n = 2 loops'),
        (90, 3, 'T = 90 N → n = 3 loops'),
    ]
    for ax, (T, n, title) in zip(axes, configs):
        v = np.sqrt(T / mu)
        f = n * v / (2 * L)
        x = np.linspace(0, L, 400)
        ax.fill_between(x, np.sin(n*np.pi*x/L)*0.8, -np.sin(n*np.pi*x/L)*0.8,
                        alpha=0.15, color='blue')
        ax.plot(x,  np.sin(n*np.pi*x/L)*0.8, 'b-', lw=2.5)
        ax.plot(x, -np.sin(n*np.pi*x/L)*0.8, 'b--', lw=1.5, alpha=0.5)
        ax.axhline(0, color='k', lw=1)
        ax.plot(0, 0, 'ks', ms=10, zorder=5)
        ax.plot(L, 0, 'ks', ms=10, zorder=5)
        # Node markers
        nodes = np.linspace(0, L, n+1)
        ax.plot(nodes, np.zeros_like(nodes), 'rv', ms=7, zorder=5)
        ax.annotate('', xy=(L, -1.2), xytext=(0, -1.2),
                    arrowprops=dict(arrowstyle='<->', color='k', lw=1.5))
        ax.text(L/2, -1.5, f'L = 75 cm', ha='center', fontsize=9)
        ax.set_xlim(-0.03, L+0.03); ax.set_ylim(-2, 1.4)
        ax.set_title(f'{title}\nv={v:.1f} cm/s, f={f:.1f} Hz', fontsize=9)
        ax.axis('off')

    fig.suptitle('Q62: สายกีตาร์ L=75cm, μ=0.01296 kg/m — เปรียบเทียบ 2 กรณี', y=1.02)
    fig.tight_layout()
    return fig


# ════════════════════════════════════════════════════════════════════════════
# Q63 — single slit a=6cm, λ=2cm
# ════════════════════════════════════════════════════════════════════════════
def _q63():
    fig, ax = plt.subplots(figsize=(8, 4))
    a, lam = 6, 2
    theta = np.linspace(-np.pi/2, np.pi/2, 2000)
    beta  = np.pi*a*np.sin(theta)/lam
    with np.errstate(divide='ignore', invalid='ignore'):
        I = np.where(np.abs(beta)<1e-9, 1.0, (np.sin(beta)/beta)**2)
    ax.plot(np.degrees(theta), I, 'b-', lw=2)
    ax.axhline(0, color='k', lw=0.8)
    ax.fill_between(np.degrees(theta), I, alpha=0.15, color='blue')
    for n in range(-3, 4):
        if n==0: continue
        th_n = np.degrees(np.arcsin(n*lam/a))
        ax.axvline(th_n, color='red', lw=1.2, ls='--', alpha=0.8)
        ax.text(th_n, -0.07, f'n={n}', ha='center', fontsize=8, color='red')
    ax.set_xlabel('θ (degrees)'); ax.set_ylabel('I/I₀')
    ax.set_title('Q63: Single slit a=6cm, λ=2cm → 6 dark fringes (n=±1,±2,±3)')
    ax.set_xlim(-50, 50)
    fig.tight_layout()
    return fig

# ════════════════════════════════════════════════════════════════════════════
# Q64 — single slit a=8cm, λ=2.5cm
# ════════════════════════════════════════════════════════════════════════════
def _q64():
    fig, ax = plt.subplots(figsize=(8, 4))
    a, lam = 8, 2.5
    theta = np.linspace(-np.pi/2, np.pi/2, 2000)
    beta  = np.pi*a*np.sin(theta)/lam
    with np.errstate(divide='ignore', invalid='ignore'):
        I = np.where(np.abs(beta)<1e-9, 1.0, (np.sin(beta)/beta)**2)
    ax.plot(np.degrees(theta), I, 'b-', lw=2)
    ax.axhline(0, color='k', lw=0.8)
    ax.fill_between(np.degrees(theta), I, alpha=0.15, color='blue')
    for n in range(-3, 4):
        if n==0: continue
        th_n = np.degrees(np.arcsin(n*lam/a))
        ax.axvline(th_n, color='red', lw=1.2, ls='--', alpha=0.8)
        ax.text(th_n, -0.07, f'n={n}', ha='center', fontsize=8, color='red')
    th2 = np.degrees(np.arcsin(2*lam/a))
    ax.text(th2+1, 0.12, f'θ₂={th2:.1f}°', fontsize=9, color='darkred')
    ax.set_xlabel('θ (degrees)'); ax.set_ylabel('I/I₀')
    ax.set_title(f'Q64: Single slit a=8cm, λ=2.5cm → θ₂={th2:.1f}°')
    ax.set_xlim(-60, 60)
    fig.tight_layout()
    return fig

# ════════════════════════════════════════════════════════════════════════════
# Q68 — double slit d=8cm, λ=2cm
# ════════════════════════════════════════════════════════════════════════════
def _q68():
    fig, ax = plt.subplots(figsize=(8, 6))
    d, lam = 8, 2
    n_max = int(d/lam)
    ax.plot(0, d/2, 'ro', ms=10, zorder=5)
    ax.plot(0,-d/2, 'bs', ms=10, zorder=5)
    ax.annotate('Slit 1', (0,d/2),  xytext=(-50,2),  textcoords='offset points',
                fontsize=10, color='red')
    ax.annotate('Slit 2', (0,-d/2), xytext=(-50,-10), textcoords='offset points',
                fontsize=10, color='blue')
    r_max = 18
    for n in range(-n_max, n_max+1):
        val = n*lam/d
        if abs(val)<=1:
            th = np.arcsin(val)
            ax.plot([0,r_max*np.cos(th)],[0,r_max*np.sin(th)],'g-',lw=1.5,alpha=0.7)
            ax.text(r_max*np.cos(th)*1.06, r_max*np.sin(th)*1.06,
                    f'A{abs(n)}', fontsize=9, color='green')
    for n in range(1, n_max+1):
        for sign in [1,-1]:
            val = (n-0.5)*lam/d
            if abs(val)<=1:
                th = np.arcsin(sign*val)
                ax.plot([0,r_max*np.cos(th)],[0,r_max*np.sin(th)],
                        'r--',lw=1,alpha=0.5)
    th_A2 = np.arcsin(2*lam/d)
    r_A = 12
    ax.plot(r_A*np.cos(th_A2), r_A*np.sin(th_A2), 'k^', ms=10, zorder=5)
    ax.annotate('A (n=2)\nr₁=10, r₂=14 cm',
                (r_A*np.cos(th_A2), r_A*np.sin(th_A2)),
                xytext=(5,5), textcoords='offset points', fontsize=9)
    ax.set_xlim(-3,20); ax.set_ylim(-12,12)
    ax.set_xlabel('x (cm)'); ax.set_ylabel('y (cm)')
    ax.set_title('Q68: Double slit d=8cm, λ=2cm\nGreen=antinode(9), Red-dash=node(8)')
    fig.tight_layout()
    return fig

# ════════════════════════════════════════════════════════════════════════════
# PUBLIC API
# ════════════════════════════════════════════════════════════════════════════
_PLOT_MAP = {
    1:_q1, 2:_q2, 3:_q3, 4:_q4, 5:_q5,
    13:_q13, 17:_q17, 20:_q20,
    24:_q24, 26:_q26, 27:_q27,
    28:_q28, 29:_q29, 30:_q30, 31:_q31,
    32:_q32, 33:_q33, 34:_q34, 35:_q35, 36:_q36, 37:_q37, 38:_q38, 39:_q39,
    41:_q41, 42:_q42,
    43:_q43, 44:_q44,
    47:_q47, 48:_q48, 49:_q49,
    50:_q50, 51:_q51, 52:_q52,
    53:_q53, 54:_q54, 55:_q55, 56:_q56, 57:_q57,
    59:_q59, 60:_q60, 61:_q61, 62:_q62,
    63:_q63, 64:_q64, 68:_q68,
}

def get_plot_for_question(q_num: int):
    fn = _PLOT_MAP.get(q_num)
    if fn is None:
        return None
    try:
        return fn()
    except Exception as e:
        print(f'[visuals] Q{q_num} error: {e}')
        return None
