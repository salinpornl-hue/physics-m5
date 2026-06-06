import matplotlib.pyplot as plt
import numpy as np

def get_plot_for_question(q_index):
    """Function to generate plots based on the question index."""
    
    # Question 1: Wave graphs (y-x and y-t)
    if q_index == 1:
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6))
        
        # กราฟ (1) y-x: ความยาวคลื่น (lambda) = 0.8 m
        x = np.linspace(0, 1.6, 500)
        y1 = np.sin(2 * np.pi * x / 0.8)
        
        ax1.plot(x, y1, color='black', linewidth=2)
        ax1.set_title('รูป (1)', loc='left', fontsize=12, fontweight='bold')
        ax1.set_xlabel('x(m)', loc='right')
        ax1.set_xticks([0, 0.4, 0.8, 1.2, 1.6])
        ax1.set_yticks([])
        ax1.axhline(0, color='black', linewidth=1)
        ax1.spines['left'].set_visible(False)
        ax1.spines['right'].set_visible(False)
        ax1.spines['top'].set_visible(False)
        
        # กราฟ (2) y-t: คาบ (period) T = 4 s
        # ปรับให้เริ่มที่จุดยอด (cos) เพื่อให้เหมือนรูป
        t = np.linspace(0, 8, 500)
        y2 = np.cos(2 * np.pi * t / 4)
        
        ax2.plot(t, y2, color='black', linewidth=2)
        ax2.set_title('รูป (2)', loc='left', fontsize=12, fontweight='bold')
        ax2.set_xlabel('t(s)', loc='right')
        ax2.set_xticks([0, 1, 3, 5, 7])
        ax2.set_yticks([])
        ax2.axhline(0, color='black', linewidth=1)
        ax2.spines['left'].set_visible(False)
        ax2.spines['right'].set_visible(False)
        ax2.spines['top'].set_visible(False)
        
        plt.tight_layout()
        return fig
        
    elif q_index == 2:
        fig, ax = plt.subplots(figsize=(6, 3))
        # สร้างกราฟคลื่น sine จำลองตามรูปโจทย์
        x = np.linspace(0, 10, 200)
        y = np.sin(np.pi * x / 2) # จำลองรูปคลื่น
        
        ax.plot(x, y, color='purple', linewidth=2)
        ax.set_title("Figure for Question 2: Wave at t = 0.5s")
        ax.set_xlabel("Position (m)")
        ax.set_ylabel("Displacement (cm)")
        ax.grid(True, linestyle='--', alpha=0.6)
        
        # เพิ่มเส้นขีดบอกตำแหน่งสำคัญตามโจทย์ (ตัวอย่าง)
        ax.axhline(0, color='black', linewidth=0.5)
        
        plt.tight_layout()
        return fig
    
    # Add other questions here as we go...
    return None
