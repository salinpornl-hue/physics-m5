import matplotlib.pyplot as plt
import numpy as np

def get_plot_for_question(q_index):
    """Function to generate plots based on the question index."""
    
    # Question 1: Wave graphs (y-x and y-t)
    if q_index == 1:
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6, 7))
        
        # รูปที่ 1: กราฟ y-x (ความยาวคลื่น lambda = 0.2 m)
        x = np.linspace(0, 0.2, 100)
        y1 = 0.1 * np.sin(2 * np.pi * x / 0.2)
        ax1.plot(x, y1, color='blue', linewidth=2)
        ax1.set_title("Figure (1): Displacement vs Position (y-x)")
        ax1.set_xlabel("Position (m)")
        ax1.set_ylabel("Displacement (cm)")
        ax1.set_xticks([0, 0.1, 0.2])
        ax1.grid(True)
        
        # รูปที่ 2: กราฟ y-t (คาบ T = 0.1 s)
        t = np.linspace(0, 0.1, 100)
        y2 = 0.1 * np.sin(2 * np.pi * t / 0.1)
        ax2.plot(t, y2, color='red', linewidth=2)
        ax2.set_title("Figure (2): Displacement vs Time (y-t)")
        ax2.set_xlabel("Time (s)")
        ax2.set_ylabel("Displacement (cm)")
        ax2.set_xticks([0, 0.05, 0.1])
        ax2.grid(True)
        
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
