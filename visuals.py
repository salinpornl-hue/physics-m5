import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# Thai-compatible font fallback chain
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = [
    'TH Sarabun New', 'Tahoma', 'Arial Unicode MS', 'DejaVu Sans', 'sans-serif'
]


def _fig(w=7, h=3):
    fig, ax = plt.subplots(figsize=(w, h))
    return fig, ax


# ── Q1 : two graphs λ=0.8m, T=4s ─────────────────────────────────────────────
def _q1():
    fig, axes = plt.subplots(1, 2, figsize=(9, 3))
    x = np.linspace(0, 1.6, 500)
    axes[0].plot(x, np.sin(2*np.pi*x/0.8), 'b')
    axes[0].set_xlabel('ตำแหน่ง x (ม.)')
    axes[0].set_ylabel('การกระจัด')
    axes[0].set_title('รูป (1): การกระจัดกับตำแหน่ง')
    axes[0].axhline(0, color='k', lw=0.8)
    for v in [0.4, 0.8, 1.2, 1.6]:
        axes[0].axvline(v, color='gray', lw=0.5, ls='--')
    axes[0].set_xticks([0, 0.4, 0.8, 1.2, 1.6])

    t = np.linspace(0, 8, 500)
    axes[1].plot(t, np.sin(2*np.pi*t/4), 'r')
    axes[1].set_xlabel('เวลา t (วินาที)')
    axes[1].set_ylabel('การกระจัด')
    axes[1].set_title('รูป (2): การกระจัดกับเวลา')
    axes[1].axhline(0, color='k', lw=0.8)
    for v in [1, 2, 3, 4, 5, 6, 7]:
        axes[1].axvline(v, color='gray', lw=0.5, ls='--')
    axes[1].set_xticks([0, 1, 2, 3, 4, 5, 6, 7])
    fig.tight_layout()
    return fig


# ── Q2 : wave after 0.5 s, λ=4m ─────────────────────────────────────────────
def _q2():
    fig, ax = _fig(7, 3)
    x = np.linspace(0, 8, 500)
    ax.plot(x, np.sin(2*np.pi*x/4), 'b', lw=2)
    ax.axhline(0, color='k', lw=0.8)
    ax.set_xlabel('ตำแหน่ง (ม.)')
    ax.set_ylabel('การกระจัด')
    ax.set_title('ข้อ 2: รูปร่างคลื่นหลังสั่น 0.5 วินาที')
    ax.set_xticks([0, 2, 4, 6, 8])
    for v in [0, 2, 4, 6, 8]:
        ax.axvline(v, color='gray', lw=0.5, ls='--')
    fig.tight_layout()
    return fig


# ── Q3 : position wave λ=8cm ─────────────────────────────────────────────────
def _q3():
    fig, ax = _fig(8, 3)
    x = np.linspace(0, 24, 500)
    ax.plot(x, np.sin(2*np.pi*x/8), 'b', lw=2)
    ax.axhline(0, color='k', lw=0.8)
    ax.set_xlabel('ตำแหน่ง (ซม.)')
    ax.set_ylabel('การกระจัด')
    ax.set_title('ข้อ 3: รูปร่างคลื่น (λ = 8 ซม.)')
    ax.set_xticks(range(0, 25, 2))
    fig.tight_layout()
    return fig


# ── Q4 : displacement-time graph T=0.2s ──────────────────────────────────────
def _q4():
    fig, ax = _fig(7, 3)
    t = np.linspace(0, 0.6, 500)
    ax.plot(t, np.sin(2*np.pi*t/0.2), 'r', lw=2)
    ax.axhline(0, color='k', lw=0.8)
    ax.set_xlabel('เวลา t (วินาที)')
    ax.set_ylabel('การกระจัด')
    ax.set_title('ข้อ 4: กราฟการกระจัดกับเวลา (T = 0.2 วินาที)')
    ax.set_xticks([0, 0.1, 0.2, 0.3, 0.4, 0.5])
    for v in [0.1, 0.2, 0.3, 0.4, 0.5]:
        ax.axvline(v, color='gray', lw=0.5, ls='--')
    fig.tight_layout()
    return fig


# ── Q5 : rope 3m, two snapshots ──────────────────────────────────────────────
def _q5():
    fig, axes = plt.subplots(1, 2, figsize=(10, 3.5))
    x = np.linspace(0, 3, 300)

    axes[0].plot(x, np.sin(2*np.pi*x/2), 'b', lw=2)
    axes[0].axhline(0, color='k', lw=0.8)
    axes[0].set_xlabel('ตำแหน่ง (ม.)')
    axes[0].set_ylabel('การกระจัด')
    axes[0].set_title('รูป (ก): t = 0')
    axes[0].set_xticks([0, 1, 2, 3])

    axes[1].plot(x, np.sin(2*np.pi*x/2 + np.pi), 'r', lw=2, ls='--')
    axes[1].axhline(0, color='k', lw=0.8)
    axes[1].set_xlabel('ตำแหน่ง (ม.)')
    axes[1].set_title('รูป (ข): t = 2 วินาที (เลื่อน λ/2)')
    axes[1].set_xticks([0, 1, 2, 3])

    fig.suptitle('ข้อ 5: คลื่นในเส้นเชือก 3 เมตร', y=1.02)
    fig.tight_layout()
    return fig


# ── Q13 : triangular pulse on grid, moving right ─────────────────────────────
def _q13():
    fig, axes = plt.subplots(1, 3, figsize=(12, 3))
    times = [0, 0.1, 0.2]
    speed = 20

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
        axes[idx].set_title(f't = {t} วินาที')
        axes[idx].set_xlabel('ตำแหน่ง (ช่อง)')

    fig.suptitle('ข้อ 13: คลื่นดลเคลื่อนที่ไปขวา (20 ช่อง/วินาที)', y=1.02)
    fig.tight_layout()
    return fig


# ── Q17 : sine wave with labeled points ──────────────────────────────────────
def _q17():
    fig, ax = _fig(10, 4)
    x = np.linspace(0, 4*np.pi, 500)
    y = np.sin(x)
    ax.plot(x, y, 'b', lw=2)
    ax.axhline(0, color='k', lw=0.8)
    ax.set_xlabel('ตำแหน่ง')
    ax.set_ylabel('การกระจัด')
    ax.set_title('ข้อ 17: จุด a–q บนคลื่น')

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


# ── Q20 : displacement-time graph, T=0.2s ────────────────────────────────────
def _q20():
    fig, ax = _fig(7, 3)
    t = np.linspace(0, 0.5, 500)
    ax.plot(t, 0.1*np.sin(2*np.pi*t/0.2), 'b', lw=2)
    ax.axhline(0, color='k', lw=0.8)
    ax.set_xlabel('เวลา t (วินาที)')
    ax.set_ylabel('การกระจัด (ม.)')
    ax.set_title('ข้อ 20: v = 2 ม./วินาที, T = 0.2 วินาที')
    ax.set_xticks([0, 0.1, 0.2, 0.3, 0.4, 0.5])
    ax.set_yticks([-0.1, 0, 0.1])
    for v in [0.1, 0.2, 0.3, 0.4, 0.5]:
        ax.axvline(v, color='gray', lw=0.5, ls='--')
    fig.tight_layout()
    return fig


# ── Q32 : refraction deep→shallow, θ1=60°, v1=2v2 ────────────────────────────
def _q32():
    fig, ax = _fig(6, 5)
    ax.axhline(0, color='k', lw=1.5, ls='--', label='รอยต่อ')
    ax.text(-2.8, 0.2, 'น้ำลึก (v₁)', fontsize=10)
    ax.text(-2.8, -0.5, 'น้ำตื้น (v₂)', fontsize=10)

    ax.annotate('', xy=(0, 0), xytext=(-2, 2*np.tan(np.radians(30))),
                arrowprops=dict(arrowstyle='->', color='blue', lw=2))
    ax.annotate('', xy=(1.5, -1.5*np.tan(np.radians(25.7))), xytext=(0, 0),
                arrowprops=dict(arrowstyle='->', color='red', lw=2))
    ax.axvline(0, color='gray', lw=1, ls=':')
    ax.annotate('θ₁=60°', xy=(-0.6, 0.5), fontsize=10, color='blue')
    ax.annotate('θ₂≈26°', xy=(0.3, -0.4), fontsize=10, color='red')
    ax.set_xlim(-3, 3); ax.set_ylim(-2, 3)
    ax.set_title('ข้อ 32: การหักเหของคลื่น (v₁=2v₂, θ₁=60°)')
    ax.axis('off')
    fig.tight_layout()
    return fig


# ── Q35 : refraction shallow→deep, θ1=30° ────────────────────────────────────
def _q35():
    fig, ax = _fig(6, 5)
    ax.axhline(0, color='k', lw=1.5, ls='--')
    ax.text(-2.8, 0.2, 'น้ำตื้น (v₁)', fontsize=10)
    ax.text(-2.8, -0.6, 'น้ำลึก (v₂=√3·v₁)', fontsize=10)
    ax.annotate('', xy=(0, 0), xytext=(-1.5, 1.5*np.tan(np.radians(60))),
                arrowprops=dict(arrowstyle='->', color='blue', lw=2))
    ax.annotate('', xy=(1.5, -1.5*np.tan(np.radians(60))), xytext=(0, 0),
                arrowprops=dict(arrowstyle='->', color='red', lw=2))
    ax.axvline(0, color='gray', lw=1, ls=':')
    ax.annotate('θ₁=30°', xy=(-0.8, 0.6), fontsize=10, color='blue')
    ax.annotate('θ₂=60°', xy=(0.2, -0.7), fontsize=10, color='red')
    ax.set_xlim(-3, 3); ax.set_ylim(-3, 3)
    ax.set_title('ข้อ 35: น้ำตื้น→ลึก (λ₂=√3·λ₁, θ₁=30°→θ₂=60°)')
    ax.axis('off')
    fig.tight_layout()
    return fig


# ── Q43 : two coherent sources d=10cm, λ=2.5cm ───────────────────────────────
def _q43():
    # Compute exact positions from given distances
    # S1=(0,5), S2=(0,-5); d=10cm
    # A: r1=12, r2=17  →  y=7.25, x≈11.79
    # B: r1=14.5, r2=15.75  →  y≈1.89, x≈14.16
    # C: r1=16, r2=24  →  y=16, x≈11.62
    s1 = np.array([0.0,  5.0])
    s2 = np.array([0.0, -5.0])

    def find_point(r1, r2):
        y = (r2**2 - r1**2) / 20.0
        x2 = r1**2 - (y - 5)**2
        x = np.sqrt(max(x2, 0))
        return np.array([x, y])

    A = find_point(12, 17)    # ≈ (11.79, 7.25)  → ปฏิบัพที่ 2
    B = find_point(14.5, 15.75)  # ≈ (14.16, 1.89) → บัพที่ 1
    C = find_point(16, 24)    # ≈ (11.62, 16)    → ระหว่างแนว

    fig, ax = plt.subplots(figsize=(7, 8))
    ax.plot(*s1, 'ro', ms=10)
    ax.plot(*s2, 'bs', ms=10)
    ax.annotate('S₁', s1, textcoords='offset points', xytext=(-22, 0),
                fontsize=11, color='red')
    ax.annotate('S₂', s2, textcoords='offset points', xytext=(-22, 0),
                fontsize=11, color='blue')

    # Draw labeled points
    pts = {'A': (A, 'green', 'ปฏิบัพที่ 2'),
           'B': (B, 'purple', 'บัพที่ 1'),
           'C': (C, 'orange', 'ระหว่างแนว')}
    for name, (pt, color, desc) in pts.items():
        ax.plot(*pt, 'o', color=color, ms=9)
        ax.annotate(f'{name} ({desc})', pt,
                    textcoords='offset points', xytext=(6, 4),
                    fontsize=9, color=color)

    ax.set_xlim(-2, 20)
    ax.set_ylim(-8, 20)
    ax.axhline(0, color='gray', lw=0.5, ls='--')
    ax.set_xlabel('x (ซม.)')
    ax.set_ylabel('y (ซม.)')
    ax.set_title('ข้อ 43: S₁S₂ = 10 ซม., λ = 2.5 ซม.')
    fig.tight_layout()
    return fig


# ── Q44 : two sources d=12cm, λ=4cm ──────────────────────────────────────────
def _q44():
    fig, ax = _fig(7, 6)
    d = 12; lam = 4
    s1y, s2y = d/2, -d/2
    ax.plot(0, s1y, 'ro', ms=8)
    ax.plot(0, s2y, 'bs', ms=8)
    ax.annotate('S₁', (0, s1y), textcoords='offset points', xytext=(-20, 0),
                fontsize=11, color='red')
    ax.annotate('S₂', (0, s2y), textcoords='offset points', xytext=(-20, 0),
                fontsize=11, color='blue')

    thetas_anti = [np.arcsin(n*lam/d) for n in range(int(d/lam)+1)
                   if abs(n*lam/d) <= 1]
    thetas_node = [np.arcsin((n-0.5)*lam/d) for n in range(1, int(d/lam)+2)
                   if abs((n-0.5)*lam/d) <= 1]
    r = 20
    for th in thetas_anti:
        for sign in [1, -1]:
            ax.plot([0, r*np.cos(sign*th)], [0, r*np.sin(sign*th)],
                    'g-', lw=1, alpha=0.6)
    for th in thetas_node:
        for sign in [1, -1]:
            ax.plot([0, r*np.cos(sign*th)], [0, r*np.sin(sign*th)],
                    'r--', lw=1, alpha=0.5)

    ax.plot(0, 19, 'k^', ms=8)
    ax.annotate('X', (0, 19), textcoords='offset points', xytext=(5, 0), fontsize=11)
    ax.set_xlim(-5, 25); ax.set_ylim(-15, 15)
    ax.set_xlabel('x (ซม.)'); ax.set_ylabel('y (ซม.)')
    ax.set_title('ข้อ 44: S₁S₂=12 ซม., λ=4 ซม.\n'
                 '(เส้นสีเขียว=แนวปฏิบัพ, เส้นประแดง=แนวบัพ)')
    fig.tight_layout()
    return fig


# ── Q49 : double slit d=6cm, first antinode at 30° ───────────────────────────
def _q49():
    fig, ax = _fig(6, 5)
    ax.plot(0, 3, 'ro', ms=8); ax.plot(0, -3, 'bs', ms=8)
    ax.annotate('S₁', (0, 3), textcoords='offset points', xytext=(-22, 0),
                fontsize=11, color='red')
    ax.annotate('S₂', (0, -3), textcoords='offset points', xytext=(-22, 0),
                fontsize=11, color='blue')
    r = 12; th = np.radians(30)
    ax.annotate('', xy=(r*np.cos(th), r*np.sin(th)), xytext=(0, 0),
                arrowprops=dict(arrowstyle='->', color='green', lw=2))
    ax.annotate('', xy=(r*np.cos(-th), r*np.sin(-th)), xytext=(0, 0),
                arrowprops=dict(arrowstyle='->', color='green', lw=2))
    ax.annotate('30°', (4, 2.5), fontsize=11, color='green')
    ax.annotate('30°', (4, -3), fontsize=11, color='green')
    ax.axhline(0, color='gray', lw=0.8, ls='--')
    ax.set_xlim(-2, 14); ax.set_ylim(-8, 8)
    ax.set_title('ข้อ 49: ปฏิบัพแรกเบน 30°, d=6 ซม.\n→ λ = d·sin30° = 3 ซม.')
    ax.axis('off')
    fig.tight_layout()
    return fig


# ── Q50 : double slit geometry for x calculation ─────────────────────────────
def _q50():
    fig, ax = _fig(7, 5)
    ax.plot(0, 0.5, 'ro', ms=8); ax.plot(0, -0.5, 'bs', ms=8)
    ax.annotate('S₁', (0, 0.5), textcoords='offset points',
                xytext=(-22, 5), fontsize=11, color='red')
    ax.annotate('S₂', (0, -0.5), textcoords='offset points',
                xytext=(-22, -12), fontsize=11, color='blue')
    ax.annotate('', xy=(6, 0.6), xytext=(0, 0),
                arrowprops=dict(arrowstyle='->', color='green', lw=2))
    ax.plot([6, 6], [-1.5, 1.5], 'k-', lw=2)
    ax.annotate('O (แนวกลาง)', (6, 0),
                textcoords='offset points', xytext=(5, -15), fontsize=9)
    ax.annotate('P (ปฏิบัพที่ 1)', (6, 0.6),
                textcoords='offset points', xytext=(5, 0), fontsize=9)
    ax.annotate('x', (6.4, 0.3), fontsize=11, color='purple')
    ax.annotate('L = 60 ซม.', (3, -1.2), fontsize=10)
    ax.set_xlim(-1, 8); ax.set_ylim(-2, 2)
    ax.set_title('ข้อ 50: d=10 ซม., λ=1 ซม., L=60 ซม. → x=6 ซม.')
    ax.axis('off')
    fig.tight_layout()
    return fig


# ── Q53 : wire 40cm, fundamental mode ────────────────────────────────────────
def _q53():
    fig, ax = _fig(7, 3)
    x = np.linspace(0, 0.4, 300)
    ax.plot(x, np.sin(np.pi*x/0.4)*0.5, 'b', lw=2.5)
    ax.plot(x, -np.sin(np.pi*x/0.4)*0.5, 'b--', lw=1.5, alpha=0.5)
    ax.axhline(0, color='k', lw=1)
    ax.plot(0, 0, 'ko', ms=8); ax.plot(0.4, 0, 'ko', ms=8)
    ax.annotate('ปลายตรึง', (0, 0),
                textcoords='offset points', xytext=(-5, -18), fontsize=9)
    ax.annotate('ปลายตรึง', (0.4, 0),
                textcoords='offset points', xytext=(-30, -18), fontsize=9)
    ax.annotate('ปฏิบัพ', (0.2, 0.5),
                textcoords='offset points', xytext=(0, 5), fontsize=9, ha='center')
    ax.set_xlabel('ตำแหน่ง (ม.)')
    ax.set_title('ข้อ 53: คลื่นนิ่ง L=0.4 ม. (1 ห่วง)')
    ax.set_xticks([0, 0.1, 0.2, 0.3, 0.4])
    ax.set_ylim(-0.8, 0.8)
    fig.tight_layout()
    return fig


# ── Q57 : standing wave, node spacing = 10cm ─────────────────────────────────
def _q57():
    fig, ax = _fig(8, 3)
    L = 0.5
    x = np.linspace(0, 5*L, 500)
    ax.plot(x, np.sin(2*np.pi*x/L)*0.5, 'b', lw=2)
    ax.plot(x, -np.sin(2*np.pi*x/L)*0.5, 'b--', lw=1, alpha=0.5)
    ax.axhline(0, color='k', lw=1)
    nodes = np.arange(0, 5*L+0.01, L/2)
    ax.plot(nodes, np.zeros_like(nodes), 'ro', ms=6,
            label='บัพ (ห่างกัน 10 ซม.)')
    ax.set_xlabel('ตำแหน่ง (ม.)')
    ax.set_title('ข้อ 57: คลื่นนิ่ง — ระยะห่างบัพ = 10 ซม.')
    ax.legend(fontsize=9)
    fig.tight_layout()
    return fig


# ── Q59 : resonance on 1.25m string ──────────────────────────────────────────
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
        axes[i].set_xlabel('ตำแหน่ง (ม.)')
        axes[i].set_ylim(-0.7, 0.7)
    fig.suptitle('ข้อ 59: การสั่นพ้อง L=1.25 ม., v=160 ม./วินาที', y=1.02)
    fig.tight_layout()
    return fig


# ── Q60 : 2nd overtone (3rd harmonic) on 1.20m wire ──────────────────────────
def _q60():
    fig, ax = _fig(7, 3)
    L = 1.2
    x = np.linspace(0, L, 300)
    ax.plot(x, np.sin(3*np.pi*x/L)*0.5, 'b', lw=2.5)
    ax.plot(x, -np.sin(3*np.pi*x/L)*0.5, 'b--', lw=1.5, alpha=0.5)
    ax.axhline(0, color='k', lw=1)
    ax.plot(0, 0, 'ko', ms=8); ax.plot(L, 0, 'ko', ms=8)
    ax.set_title('ข้อ 60: โอเวอร์โทนที่ 2 (ฮาร์โมนิกที่ 3), L=1.2 ม.')
    ax.set_xlabel('ตำแหน่ง (ม.)')
    ax.set_ylim(-0.8, 0.8)
    fig.tight_layout()
    return fig


# ── Q63 : single slit diffraction, a=6cm, λ=2cm ─────────────────────────────
def _q63():
    fig, ax = _fig(8, 4)
    theta = np.linspace(-np.pi/2, np.pi/2, 1000)
    a, lam = 6, 2
    beta = np.pi * a * np.sin(theta) / lam
    with np.errstate(divide='ignore', invalid='ignore'):
        I = np.where(beta == 0, 1.0, (np.sin(beta)/beta)**2)
    ax.plot(np.degrees(theta), I, 'b', lw=2)
    ax.axhline(0, color='k', lw=0.8)
    for n in [-3, -2, -1, 1, 2, 3]:
        th_null = np.degrees(np.arcsin(n*lam/a))
        ax.axvline(th_null, color='red', lw=1, ls='--', alpha=0.7)
        ax.text(th_null, 0.05, f'n={n}', fontsize=7, ha='center', color='red')
    ax.set_xlabel('มุม θ (องศา)')
    ax.set_ylabel('ความเข้ม (I/I₀)')
    ax.set_title('ข้อ 63: การเลี้ยวเบนช่องเดี่ยว (a=6 ซม., λ=2 ซม.)\n'
                 'แนวบัพ 6 แนว (n=±1,±2,±3)')
    fig.tight_layout()
    return fig


# ── Q64 : single slit a=8cm, λ=2.5cm ────────────────────────────────────────
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
    ax.set_xlabel('มุม θ (องศา)')
    ax.set_ylabel('ความเข้ม (I/I₀)')
    ax.set_title('ข้อ 64: ช่องเดี่ยว (a=8 ซม., λ=2.5 ซม.)\n'
                 'n=±1,±2,±3 → บัพ 6 แนว')
    fig.tight_layout()
    return fig


# ── Q68 : double slit d=8cm, λ=2cm ──────────────────────────────────────────
def _q68():
    fig, ax = _fig(7, 5)
    d, lam = 8, 2
    ax.plot(0, d/2, 'ro', ms=10); ax.plot(0, -d/2, 'bs', ms=10)
    ax.annotate('ช่อง 1', (0, d/2), textcoords='offset points',
                xytext=(-48, 0), fontsize=10, color='red')
    ax.annotate('ช่อง 2', (0, -d/2), textcoords='offset points',
                xytext=(-48, 0), fontsize=10, color='blue')

    n_max = int(d/lam)
    for n in range(-n_max, n_max+1):
        val = n*lam/d
        if abs(val) <= 1:
            th = np.arcsin(val)
            r = 15
            color = 'green' if n == 0 else 'limegreen'
            ax.plot([0, r*np.cos(th)], [0, r*np.sin(th)],
                    '-', color=color, lw=1.5, alpha=0.7)
            ax.text(r*np.cos(th)*1.05, r*np.sin(th)*1.05,
                    f'A{abs(n)}', fontsize=8, color=color)

    ax.set_xlim(-3, 18); ax.set_ylim(-12, 12)
    ax.set_xlabel('x (ซม.)')
    ax.set_title('ข้อ 68: ช่องคู่ d=8 ซม., λ=2 ซม.\n'
                 '(สีเขียว=แนวปฏิบัพ)')
    fig.tight_layout()
    return fig


# ── Public API ────────────────────────────────────────────────────────────────

_PLOT_MAP = {
    1: _q1, 2: _q2, 3: _q3, 4: _q4, 5: _q5,
    13: _q13, 17: _q17, 20: _q20,
    32: _q32, 35: _q35,
    43: _q43, 44: _q44,
    49: _q49, 50: _q50,
    53: _q53, 57: _q57, 59: _q59, 60: _q60,
    63: _q63, 64: _q64, 68: _q68,
}


def get_plot_for_question(q_num: int):
    """Return a matplotlib Figure for question q_num, or None."""
    fn = _PLOT_MAP.get(q_num)
    if fn is None:
        return None
    try:
        return fn()
    except Exception as e:
        print(f"[visuals] ข้อ {q_num} ผิดพลาด: {e}")
        return None
