import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

def get_plot_for_question(q_index):
    """ฟังก์ชันนี้จะเลือกวาดรูปตามเลขข้อที่รับเข้ามา"""
    
    # ตัวอย่างข้อที่ 1: วาดกราฟคลื่น
    if q_index == 1:
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(5, 5))
        x = np.linspace(0, 4*np.pi, 100)
        ax1.plot(x, np.sin(x), color='blue')
        ax1.set_title("รูปที่ (1) กราฟ y-x")
        
        t = np.linspace(0, 2, 100)
        ax2.plot(t, np.sin(2 * np.pi * t), color='red')
        ax2.set_title("รูปที่ (2) กราฟ y-t")
        plt.tight_layout()
        return fig
    
    # เพิ่มข้ออื่นๆ ที่นี่...
    # elif q_index == 13: ...
    
    return None
