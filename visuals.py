import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np


def _fig(w=7, h=3):
    fig, ax = plt.subplots(figsize=(w, h))
    return fig, ax


# ── Q1 : two graphs λ=0.8m, T=4s ──────────────────────────────────────────
def _q1():
    fig, axes = plt.subplots(1, 2, figsize=(9, 3))
    x = np.linspace(0, 1.6, 500)
    axes[0].plot(x, np.sin(2*np.pi*x/0.8), 'b')
    axes[0].set_xlabel('x (m)'); axes[0].set_ylabel('Displacement')
    axes[0].set_title('รูป (1): displacement vs position')
    axes[0].axhline(0, color='k', lw=0.8)
    for v in [0.4, 0.8, 1.2, 1.6]:
        axes[0].axvline(v, color='gray', lw=0.5, ls='--')
    axes[0].set_xticks([0, 0.4, 0.8, 1.2, 1.6])

    t = np.linspace(0, 8, 500)
    axes[1].plot(t, np.sin(2*np.pi*t/4), 'r')
    axes[1].set_xlabel('t (s)'); axes[1].set_ylabel('Displacement')
    axes[1].set_title('รูป (2): displacement vs time')
    axes[1].axhline(0, color='k', lw=0.8)
    for v in [1, 2, 3, 4, 5, 6, 7]:
        axes[1].axvline(v, color='gray', lw=0.5, ls='--')
    axes[1].set_xticks([0, 1, 2, 3, 4, 5, 6, 7])
    fig.tight_layout()
    return fig


# ── Q2 : wave after 0.5 s, λ=4m ──────────────────────────────────────────
def _q2():
    fig, ax = _fig(7, 3)
    x = np.linspace(0, 8, 500)
    ax.plot(x, np.sin(2*np.pi*x/4), 'b', lw=2)
    ax.axhline(0, color='k', lw=0.8)
    ax.set_xlabel('Position (m)'); ax.set_ylabel('Displacement')
    ax.set_title('ข้อ 2: รูปร่างคลื่นหลังสั่น 0.5 วินาที')
    ax.set_xticks([0, 2, 4, 6, 8])
    for v in [0, 2, 4, 6, 8]:
        ax.axvline(v, color='gray', lw=0.5, ls='--')
    fig.tight_layout()
    return fig


# ── Q3 : position wave λ=8cm, with cm axis ────────────────────────────────
def _q3():
    fig, ax = _fig(8, 3)
    x = np.linspace(0, 24, 500)
    ax.plot(x, np.sin(2*np.pi*x/8), 'b', lw=2)
    ax.axhline(0, color='k', lw=0.8)
    ax.set_xlabel('Position (cm)'); ax.set_ylabel('Displacement')
    ax.set_title('ข้อ 3: รูปร่างคลื่น (λ = 8 cm)')
    ax.set_xticks(range(0, 25, 2))
    fig.tight_layout()
    return fig


# ── Q4 : displacement-time graph T=0.2s ───────────────────────────────────
def _q4():
    fig, ax = _fig(7, 3)
    t = np.linspace(0, 0.6, 500)
    ax.plot(t, np.sin(2*np.pi*t/0.2), 'r', lw=2)
    ax.axhline(0, color='k', lw=0.8)
    ax.set_xlabel('Time t (s)'); ax.set_ylabel('Displacement')
    ax.set_title('ข้อ 4: กราฟDisplacement-Time (T = 0.2 s)')
    ax.set_xticks([0, 0.1, 0.2, 0.3, 0.4, 0.5])
    for v in [0.1, 0.2, 0.3, 0.4, 0.5]:
        ax.axvline(v, color='gray', lw=0.5, ls='--')
    fig.tight_layout()
    return fig


# ── Q5 : rope 3m, two snapshots ───────────────────────────────────────────
def _q5():
    fig, axes = plt.subplots(1, 2, figsize=(10, 3.5))
    x = np.linspace(0, 3, 300)

    # รูป (ก): t=0, λ=2m
    axes[0].plot(x, np.sin(2*np.pi*x/2), 'b', lw=2, label='t = 0')
    axes[0].axhline(0, color='k', lw=0.8)
    axes[0].set_xlabel('Position (m)'); axes[0].set_ylabel('Displacement')
    axes[0].set_title('รูป (ก): t = 0')
    axes[0].set_xticks([0, 1, 2, 3])

    # รูป (ข): เลื่อนไป λ/2 = 1 m
    axes[1].plot(x, np.sin(2*np.pi*x/2 + np.pi), 'r', lw=2, label='t = 2 s', ls='--')
    axes[1].axhline(0, color='k', lw=0.8)
    axes[1].set_xlabel('Position (m)')
    axes[1].set_title('รูป (ข): t = 2 s (เลื่อน λ/2)')
    axes[1].set_xticks([0, 1, 2, 3])

    fig.suptitle('ข้อ 5: คลื่นในเส้นเชือก 3 เมตร', y=1.02)
    fig.tight_layout()
    return fig


# ── Q13 : triangular pulse on grid, moving right ──────────────────────────
def _q13():
    fig, axes = plt.subplots(1, 3, figsize=(12, 3))
    times = [0, 0.1, 0.2]
    speed = 20  # channels/s

    def pulse(x, offset):
        y = np.zeros_like(x)
        for i, xi in enumerate(x):
            rel = xi - offset
            if -2 <= rel <= 0:
                y[i] = rel + 2
            elif 0 < rel <= 2:
                y[i] = -rel + 2
        return y

    for idx, t in enumerate(times):
        x = np.linspace(-5, 25, 600)
        offset = speed * t
        y = pulse(x, offset)
        axes[idx].plot(x, y, 'b', lw=2)
        axes[idx].axhline(0, color='k', lw=0.8)
        axes[idx].set_xlim(-3, 22)
        axes[idx].set_ylim(-0.5, 3)
        axes[idx].grid(True, lw=0.3)
        axes[idx].set_title(f't = {t} s')
        axes[idx].set_xlabel('Position (ช่อง)')

    fig.suptitle('ข้อ 13: คลื่นดลเคลื่อนที่ไปขวา (20 ช่อง/s)', y=1.02)
    fig.tight_layout()
    return fig


# ── Q17 : sine wave with labeled points ───────────────────────────────────
def _q17():
    fig, ax = _fig(10, 4)
    x = np.linspace(0, 4*np.pi, 500)
    y = np.sin(x)
    ax.plot(x, y, 'b', lw=2)
    ax.axhline(0, color='k', lw=0.8)
    ax.set_xlabel('Position'); ax.set_ylabel('Displacement')
    ax.set_title('ข้อ 17: จุด a–q บนคลื่น')

    # label key points: a=0, b=π/4, c=π/2, d=3π/4, e=π, f=5π/4, g=3π/2,
    # h=7π/4, i=2π, j=9π/4, k=5π/2, l=11π/4, m=3π, n=13π/4, o=7π/2,
    # p=15π/4, q=4π
    labels = list('abcdefghijklmnopq')
    positions = [i * np.pi/4 for i in range(17)]
    for lbl, pos in zip(labels, positions):
        if pos <= 4*np.pi:
            yv = np.sin(pos)
            ax.annotate(lbl, (pos, yv), textcoords='offset points',
                        xytext=(0, 8 if yv >= 0 else -14),
                        fontsize=9, color='red', ha='center')
            ax.plot(pos, yv, 'ro', ms=4)
    fig.tight_layout()
    return fig


# ── Q20 : displacement-time graph, T=0.4s, A=0.1 ─────────────────────────
def _q20():
    fig, ax = _fig(7, 3)
    t = np.linspace(0, 0.5, 500)
    ax.plot(t, 0.1*np.sin(2*np.pi*t/0.2), 'b', lw=2)
    ax.axhline(0, color='k', lw=0.8)
    ax.set_xlabel('Time t (s)'); ax.set_ylabel('Displacement (m)')
    ax.set_title('ข้อ 20: v = 2 m/s, T = 0.2 s')
    ax.set_xticks([0, 0.1, 0.2, 0.3, 0.4, 0.5])
    ax.set_yticks([-0.1, 0, 0.1])
    for v in [0.1, 0.2, 0.3, 0.4, 0.5]:
        ax.axvline(v, color='gray', lw=0.5, ls='--')
    fig.tight_layout()
    return fig


# ── Q32 : refraction deep→shallow, θ1=60°, v1=2v2 ────────────────────────
def _q32():
    fig, ax = _fig(6, 5)
    ax.axhline(0, color='k', lw=1.5, ls='--', label='Boundary')
    ax.text(-2.8, 0.2, 'Deep water (v₁)', fontsize=10)
    ax.text(-2.8, -0.5, 'Shallow water (v₂)', fontsize=10)

    # incident ray
    ax.annotate('', xy=(0, 0), xytext=(-2, 2*np.tan(np.radians(30))),
                arrowprops=dict(arrowstyle='->', color='blue', lw=2))
    # refracted ray
    ax.annotate('', xy=(1.5, -1.5*np.tan(np.radians(25.7))), xytext=(0, 0),
                arrowprops=dict(arrowstyle='->', color='red', lw=2))
    # normal
    ax.axvline(0, color='gray', lw=1, ls=':')
    ax.annotate('θ₁=60°', xy=(-0.6, 0.5), fontsize=10, color='blue')
    ax.annotate('θ₂≈26°', xy=(0.3, -0.4), fontsize=10, color='red')
    ax.set_xlim(-3, 3); ax.set_ylim(-2, 3)
    ax.set_title('ข้อ 32: การหักเหของคลื่น (v₁=2v₂, θ₁=60°)')
    ax.axis('off')
    fig.tight_layout()
    return fig


# ── Q35 : refraction shallow→deep, θ1=30° ────────────────────────────────
def _q35():
    fig, ax = _fig(6, 5)
    ax.axhline(0, color='k', lw=1.5, ls='--')
    ax.text(-2.8, 0.2, 'Shallow water (v₁)', fontsize=10)
    ax.text(-2.8, -0.5, 'Deep water (v₂=√3·v₁)', fontsize=10)
    ax.annotate('', xy=(0, 0), xytext=(-1.5, 1.5*np.tan(np.radians(60))),
                arrowprops=dict(arrowstyle='->', color='blue', lw=2))
    ax.annotate('', xy=(1.5, -1.5*np.tan(np.radians(60))), xytext=(0, 0),
                arrowprops=dict(arrowstyle='->', color='red', lw=2))
    ax.axvline(0, color='gray', lw=1, ls=':')
    ax.annotate('θ₁=30°', xy=(-0.8, 0.6), fontsize=10, color='blue')
    ax.annotate('θ₂=60°', xy=(0.2, -0.7), fontsize=10, color='red')
    ax.set_xlim(-3, 3); ax.set_ylim(-3, 3)
    ax.set_title('ข้อ 35: ตื้น→ลึก (λ₂=√3·λ₁, θ₁=30°→θ₂=60°)')
    ax.axis('off')
    fig.tight_layout()
    return fig


# ── Q43 : two coherent sources d=10cm, λ=2.5cm ────────────────────────────
def _q43():
    fig, ax = _fig(7, 6)
    s1 = np.array([0, 5]); s2 = np.array([0, -5])
    ax.plot(*s1, 'ro', ms=8, label='S₁'); ax.plot(*s2, 'bs', ms=8, label='S₂')
    ax.annotate('S₁', s1, textcoords='offset points', xytext=(-18, 0), fontsize=11, color='red')
    ax.annotate('S₂', s2, textcoords='offset points', xytext=(-18, 0), fontsize=11, color='blue')

    # draw labeled points A, B, C
    points = {'A': (12*np.cos(np.arccos((12**2+17**2-10**2)/(2*12*17))/2),
                    12*np.sin(np.arccos((12**2+17**2-10**2)/(2*12*17))/2)),
              'B': (14, 1), 'C': (20, 0)}
    colors = {'A': 'green', 'B': 'purple', 'C': 'orange'}
    for name, (px, py) in points.items():
        ax.plot(px, py, 'o', color=colors[name], ms=7)
        ax.annotate(name, (px, py), textcoords='offset points',
                    xytext=(5, 5), fontsize=11, color=colors[name])

    ax.set_xlim(-2, 25); ax.set_ylim(-8, 8)
    ax.axhline(0, color='gray', lw=0.5, ls='--')
    ax.set_xlabel('x (cm)'); ax.set_ylabel('y (cm)')
    ax.set_title('ข้อ 43: S₁S₂ = 10 cm, λ = 2.5 cm')
    ax.legend()
    fig.tight_layout()
    return fig


# ── Q44 : two sources d=12cm, λ=4cm ──────────────────────────────────────
def _q44():
    fig, ax = _fig(7, 6)
    d = 12
    lam = 4
    s1y, s2y = d/2, -d/2
    ax.plot(0, s1y, 'ro', ms=8); ax.plot(0, s2y, 'bs', ms=8)
    ax.annotate('S₁', (0, s1y), textcoords='offset points', xytext=(-18, 0), fontsize=11, color='red')
    ax.annotate('S₂', (0, s2y), textcoords='offset points', xytext=(-18, 0), fontsize=11, color='blue')

    # draw antinodal/nodal lines
    thetas_anti = [np.arcsin(n*lam/d) for n in range(int(d/lam)+1) if abs(n*lam/d) <= 1]
    thetas_node = [np.arcsin((n-0.5)*lam/d) for n in range(1, int(d/lam)+2) if abs((n-0.5)*lam/d) <= 1]
    r = 20
    for th in thetas_anti:
        for sign in [1, -1]:
            ax.plot([0, r*np.cos(sign*th)], [0, r*np.sin(sign*th)], 'g-', lw=1, alpha=0.6)
    for th in thetas_node:
        for sign in [1, -1]:
            ax.plot([0, r*np.cos(sign*th)], [0, r*np.sin(sign*th)], 'r--', lw=1, alpha=0.5)

    ax.plot(0, 19, 'k^', ms=8); ax.annotate('X', (0, 19), textcoords='offset points',
                                              xytext=(5, 0), fontsize=11)
    ax.set_xlim(-5, 25); ax.set_ylim(-15, 15)
    ax.set_xlabel('x (cm)'); ax.set_ylabel('y (cm)')
    ax.set_title('ข้อ 44: S₁S₂=12 cm, λ=4 cm\n(เส้นสีเขียว=Antinode, เส้นประแดง=บัพ)')
    fig.tight_layout()
    return fig


# ── Q49 : double slit d=6cm, first antinode at 30° ───────────────────────
def _q49():
    fig, ax = _fig(6, 5)
    ax.plot(0, 3, 'ro', ms=8); ax.plot(0, -3, 'bs', ms=8)
    ax.annotate('S₁', (0, 3), textcoords='offset points', xytext=(-20, 0), fontsize=11, color='red')
    ax.annotate('S₂', (0, -3), textcoords='offset points', xytext=(-20, 0), fontsize=11, color='blue')
    r = 12
    th = np.radians(30)
    ax.annotate('', xy=(r*np.cos(th), r*np.sin(th)), xytext=(0, 0),
                arrowprops=dict(arrowstyle='->', color='green', lw=2))
    ax.annotate('', xy=(r*np.cos(-th), r*np.sin(-th)), xytext=(0, 0),
                arrowprops=dict(arrowstyle='->', color='green', lw=2))
    ax.annotate('30°', (4, 2.5), fontsize=11, color='green')
    ax.annotate('30°', (4, -3), fontsize=11, color='green')
    ax.axhline(0, color='gray', lw=0.8, ls='--')
    ax.set_xlim(-2, 14); ax.set_ylim(-8, 8)
    ax.set_title('ข้อ 49: Antinodeแรกเบน 30°, d=6 cm\n→ λ = d·sin30° = 3 cm')
    ax.axis('off')
    fig.tight_layout()
    return fig


# ── Q50 : double slit geometry for x calculation ─────────────────────────
def _q50():
    fig, ax = _fig(7, 5)
    ax.plot(0, 0.5, 'ro', ms=8); ax.plot(0, -0.5, 'bs', ms=8)
    ax.annotate('S₁', (0, 0.5), textcoords='offset points', xytext=(-20, 5), fontsize=11, color='red')
    ax.annotate('S₂', (0, -0.5), textcoords='offset points', xytext=(-20, -10), fontsize=11, color='blue')
    ax.annotate('', xy=(6, 0.6), xytext=(0, 0),
                arrowprops=dict(arrowstyle='->', color='green', lw=2))
    ax.plot([6, 6], [-1.5, 1.5], 'k-', lw=2)
    ax.annotate('O (Center line)', (6, 0), textcoords='offset points', xytext=(5, -15), fontsize=9)
    ax.annotate('P (Antinodeที่ 1)', (6, 0.6), textcoords='offset points', xytext=(5, 0), fontsize=9)
    ax.annotate('x', (6.4, 0.3), fontsize=11, color='purple')
    ax.annotate('L = 60 cm', (3, -1.2), fontsize=10)
    ax.set_xlim(-1, 8); ax.set_ylim(-2, 2)
    ax.set_title('ข้อ 50: d=10 cm, λ=1 cm, L=60 cm → x=6 cm')
    ax.axis('off')
    fig.tight_layout()
    return fig


# ── Q53 : wire 40cm, fundamental mode ─────────────────────────────────────
def _q53():
    fig, ax = _fig(7, 3)
    x = np.linspace(0, 0.4, 300)
    ax.plot(x, np.sin(np.pi*x/0.4)*0.5, 'b', lw=2.5)
    ax.plot(x, -np.sin(np.pi*x/0.4)*0.5, 'b--', lw=1.5, alpha=0.5)
    ax.axhline(0, color='k', lw=1)
    ax.plot(0, 0, 'ko', ms=8); ax.plot(0.4, 0, 'ko', ms=8)
    ax.annotate('Fixed end', (0, 0), textcoords='offset points', xytext=(-5, -18), fontsize=9)
    ax.annotate('Fixed end', (0.4, 0), textcoords='offset points', xytext=(-30, -18), fontsize=9)
    ax.annotate('Antinode', (0.2, 0.5), textcoords='offset points', xytext=(0, 5), fontsize=9, ha='center')
    ax.set_xlabel('Position (m)'); ax.set_title('ข้อ 53: คลื่นนิ่ง L=0.4 m (1 loop)')
    ax.set_xticks([0, 0.1, 0.2, 0.3, 0.4])
    ax.set_ylim(-0.8, 0.8)
    fig.tight_layout()
    return fig


# ── Q57 : standing wave, node spacing = 10cm ──────────────────────────────
def _q57():
    fig, ax = _fig(8, 3)
    L = 0.5  # λ = 0.2m, 5 loops shown
    x = np.linspace(0, 5*L, 500)
    ax.plot(x, np.sin(2*np.pi*x/L)*0.5, 'b', lw=2)
    ax.plot(x, -np.sin(2*np.pi*x/L)*0.5, 'b--', lw=1, alpha=0.5)
    ax.axhline(0, color='k', lw=1)
    # mark nodes every λ/2 = 10cm
    nodes = np.arange(0, 5*L+0.01, L/2)
    ax.plot(nodes, np.zeros_like(nodes), 'ro', ms=6, label='บัพ (ห่างกัน 10 cm)')
    ax.set_xlabel('Position (m)'); ax.set_title('ข้อ 57: คลื่นนิ่ง ระยะห่างบัพ = 10 cm')
    ax.legend(fontsize=9)
    fig.tight_layout()
    return fig


# ── Q59 : resonance on 1.25m string ──────────────────────────────────────
def _q59():
    fig, axes = plt.subplots(1, 3, figsize=(12, 3.5))
    L = 1.25
    modes = [1, 2, 3]
    freqs = [64, 128, 192]
    for i, (n, f) in enumerate(zip(modes, freqs)):
        x = np.linspace(0, L, 300)
        axes[i].plot(x, np.sin(n*np.pi*x/L)*0.5, 'b', lw=2)
        axes[i].plot(x, -np.sin(n*np.pi*x/L)*0.5, 'b--', lw=1, alpha=0.5)
        axes[i].axhline(0, color='k', lw=1)
        axes[i].plot(0, 0, 'ko', ms=6); axes[i].plot(L, 0, 'ko', ms=6)
        axes[i].set_title(f'n={n}, f={f} Hz')
        axes[i].set_xlabel('Position (m)')
        axes[i].set_ylim(-0.7, 0.7)
    fig.suptitle('ข้อ 59: การสั่นพ้อง L=1.25 m, v=160 m/s', y=1.02)
    fig.tight_layout()
    return fig


# ── Q60 : 2nd overtone (3rd harmonic) on 1.20m wire ──────────────────────
def _q60():
    fig, ax = _fig(7, 3)
    L = 1.2
    x = np.linspace(0, L, 300)
    ax.plot(x, np.sin(3*np.pi*x/L)*0.5, 'b', lw=2.5)
    ax.plot(x, -np.sin(3*np.pi*x/L)*0.5, 'b--', lw=1.5, alpha=0.5)
    ax.axhline(0, color='k', lw=1)
    ax.plot(0, 0, 'ko', ms=8); ax.plot(L, 0, 'ko', ms=8)
    ax.set_title('ข้อ 60: โอเวอร์โทนที่ 2 (ฮาร์โมนิกที่ 3), L=1.2 m')
    ax.set_xlabel('Position (m)')
    ax.set_ylim(-0.8, 0.8)
    fig.tight_layout()
    return fig


# ── Q63 : single slit diffraction, a=6cm, λ=2cm ──────────────────────────
def _q63():
    fig, ax = _fig(8, 4)
    theta = np.linspace(-np.pi/2, np.pi/2, 1000)
    a, lam = 6, 2
    beta = np.pi * a * np.sin(theta) / lam
    with np.errstate(divide='ignore', invalid='ignore'):
        I = np.where(beta == 0, 1.0, (np.sin(beta)/beta)**2)
    ax.plot(np.degrees(theta), I, 'b', lw=2)
    ax.axhline(0, color='k', lw=0.8)
    # mark nulls
    for n in [-3, -2, -1, 1, 2, 3]:
        th_null = np.degrees(np.arcsin(n*lam/a))
        ax.axvline(th_null, color='red', lw=1, ls='--', alpha=0.7)
        ax.text(th_null, 0.05, f'n={n}', fontsize=7, ha='center', color='red')
    ax.set_xlabel('มุม θ (องศา)'); ax.set_ylabel('ความเข้ม (I/I₀)')
    ax.set_title('ข้อ 63: การเลี้ยวเบนช่องเดี่ยว (a=6 cm, λ=2 cm)\nแนวบัพ 6 แนว (n=±1,±2,±3)')
    fig.tight_layout()
    return fig


# ── Q64 : single slit a=8cm, λ=2.5cm ─────────────────────────────────────
def _q64():
    fig, ax = _fig(8, 4)
    theta = np.linspace(-np.pi/2, np.pi/2, 1000)
    a, lam = 8, 2.5
    beta = np.pi * a * np.sin(theta) / lam
    with np.errstate(divide='ignore', invalid='ignore'):
        I = np.where(beta == 0, 1.0, (np.sin(beta)/beta)**2)
    ax.plot(np.degrees(theta), I, 'b', lw=2)
    ax.axhline(0, color='k', lw=0.8)
    for n in [-3, -2, -1, 1, 2, 3]:
        th_null = np.degrees(np.arcsin(n*lam/a))
        ax.axvline(th_null, color='red', lw=1, ls='--', alpha=0.7)
        ax.text(th_null, 0.05, f'n={n}', fontsize=7, ha='center', color='red')
    ax.set_xlabel('มุม θ (องศา)'); ax.set_ylabel('ความเข้ม (I/I₀)')
    ax.set_title('ข้อ 64: ช่องเดี่ยว (a=8 cm, λ=2.5 cm)\nน=±1,±2,±3 → บัพ 6 แนว')
    fig.tight_layout()
    return fig


# ── Q68 : double slit d=8cm, λ=2cm ───────────────────────────────────────
def _q68():
    fig, ax = _fig(7, 5)
    d, lam = 8, 2
    ax.plot(0, d/2, 'ro', ms=10); ax.plot(0, -d/2, 'bs', ms=10)
    ax.annotate('ช่อง 1', (0, d/2), textcoords='offset points', xytext=(-45, 0), fontsize=10, color='red')
    ax.annotate('ช่อง 2', (0, -d/2), textcoords='offset points', xytext=(-45, 0), fontsize=10, color='blue')

    # antinodal lines
    n_max = int(d/lam)
    for n in range(-n_max, n_max+1):
        val = n*lam/d
        if abs(val) <= 1:
            th = np.arcsin(val)
            r = 15
            color = 'green' if n == 0 else 'limegreen'
            ax.plot([0, r*np.cos(th)], [0, r*np.sin(th)], '-', color=color, lw=1.5, alpha=0.7)
            ax.text(r*np.cos(th)*1.05, r*np.sin(th)*1.05, f'A{abs(n)}', fontsize=8, color=color)

    # mark point A
    ax.plot(10, 10*np.tan(np.radians(np.degrees(np.arcsin(2*lam/d)))), 'k^', ms=8)
    ax.annotate('A (Antinodeที่ 2)', xy=(10, 4.2), fontsize=9)

    ax.set_xlim(-3, 18); ax.set_ylim(-12, 12)
    ax.set_xlabel('x (cm)'); ax.set_title('ข้อ 68: ช่องคู่ d=8 cm, λ=2 cm\n(สีเขียว=แนวAntinode)')
    fig.tight_layout()
    return fig


# ─────────────────────────────────────────────────────────────────────────────
# PUBLIC API
# ─────────────────────────────────────────────────────────────────────────────

_PLOT_MAP = {
    1: _q1,
    2: _q2,
    3: _q3,
    4: _q4,
    5: _q5,
    13: _q13,
    17: _q17,
    20: _q20,
    32: _q32,
    35: _q35,
    43: _q43,
    44: _q44,
    49: _q49,
    50: _q50,
    53: _q53,
    57: _q57,
    59: _q59,
    60: _q60,
    63: _q63,
    64: _q64,
    68: _q68,
}


def get_plot_for_question(q_num: int):
    """Return a matplotlib Figure for question q_num, or None."""
    fn = _PLOT_MAP.get(q_num)
    if fn is None:
        return None
    try:
        return fn()
    except Exception as e:
        print(f"[visuals] Q{q_num} error: {e}")
        return None
