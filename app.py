import streamlit as st
from visuals import get_plot_for_question
from answers import ANSWERS
from answer_keys import ANSWER_KEYS, check_answer
from summary import render_summary

st.set_page_config(
    page_title="ฟิสิกส์ ม.5 — คลื่นกล",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ═══════════════════════════════════════════════════════════════════════════════
# GLOBAL CSS
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sarabun:wght@300;400;600;700&display=swap');

/* ── Reset & base ─────────────────────────────────────────── */
html, body, [class*="css"] {
    font-family: 'Sarabun', 'Helvetica Neue', Arial, sans-serif;
}
.block-container {
    padding: 1.2rem 1.8rem 2rem !important;
    max-width: 1400px;
}

/* ── Hide Streamlit chrome ───────────────────────────────── */
#MainMenu, footer, header { visibility: hidden; }

/* ── Sidebar ─────────────────────────────────────────────── */
section[data-testid="stSidebar"] {
    background: #0f172a;
    border-right: none;
}
section[data-testid="stSidebar"] * {
    color: #e2e8f0 !important;
}
section[data-testid="stSidebar"] .stButton > button {
    background: #1e293b !important;
    border: 1px solid #334155 !important;
    color: #94a3b8 !important;
    border-radius: 6px !important;
    padding: 0 !important;
    font-size: 0.70rem !important;
    min-height: 24px !important;
    height: 24px !important;
    line-height: 1 !important;
    transition: all 0.15s ease !important;
}
section[data-testid="stSidebar"] .stButton > button:hover {
    background: #2563eb !important;
    border-color: #2563eb !important;
    color: #fff !important;
}
section[data-testid="stSidebar"] .stButton > button[kind="primary"] {
    background: #2563eb !important;
    border-color: #1d4ed8 !important;
    color: #fff !important;
    font-weight: 700 !important;
}
section[data-testid="stSidebar"] [data-testid="stDownloadButton"] button {
    background: #065f46 !important;
    border-color: #047857 !important;
    color: #fff !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    height: auto !important;
    min-height: 36px !important;
    padding: 6px 12px !important;
    font-size: 0.78rem !important;
}

/* ── Sidebar labels ──────────────────────────────────────── */
.topic-label {
    font-size: 0.68rem;
    font-weight: 700;
    color: #64748b !important;
    margin: 10px 0 3px 0;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}
.sidebar-title {
    font-size: 1.1rem;
    font-weight: 700;
    color: #f1f5f9 !important;
    letter-spacing: 0.02em;
}
.sidebar-sub {
    font-size: 0.72rem;
    color: #64748b !important;
    margin-top: 2px;
}
.progress-text {
    font-size: 0.72rem;
    color: #94a3b8 !important;
    text-align: right;
}

/* ── Tabs ─────────────────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
    gap: 0;
    background: #f8fafc;
    border-radius: 10px 10px 0 0;
    border-bottom: 2px solid #e2e8f0;
    padding: 0 4px;
}
.stTabs [data-baseweb="tab"] {
    height: 44px;
    padding: 0 24px;
    font-size: 0.88rem;
    font-weight: 600;
    color: #64748b;
    border-radius: 8px 8px 0 0;
    border: none;
    background: transparent;
}
.stTabs [aria-selected="true"] {
    color: #2563eb !important;
    background: #fff !important;
    border-bottom: 2px solid #2563eb !important;
}

/* ── Question header ─────────────────────────────────────── */
.q-header-bar {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 4px;
}
.q-num-badge {
    background: #2563eb;
    color: white;
    font-size: 0.78rem;
    font-weight: 700;
    padding: 3px 10px;
    border-radius: 20px;
    white-space: nowrap;
}
.topic-chip {
    background: #eff6ff;
    color: #2563eb;
    font-size: 0.72rem;
    font-weight: 600;
    padding: 3px 10px;
    border-radius: 20px;
    border: 1px solid #bfdbfe;
}
.q-title {
    font-size: 1.45rem;
    font-weight: 700;
    color: #0f172a;
    line-height: 1.3;
    margin: 6px 0 14px 0;
}

/* ── Cards ────────────────────────────────────────────────── */
.card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 20px 24px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
}
.answer-card-header {
    background: linear-gradient(135deg, #1e40af 0%, #2563eb 100%);
    color: white;
    border-radius: 10px 10px 0 0;
    padding: 10px 18px;
    font-size: 0.85rem;
    font-weight: 700;
    letter-spacing: 0.03em;
    display: flex;
    align-items: center;
    gap: 8px;
}
.answer-card-body {
    background: #f8faff;
    border: 1px solid #c7d9f8;
    border-top: none;
    border-radius: 0 0 10px 10px;
    padding: 18px 20px;
    min-height: 180px;
}
.answer-placeholder {
    text-align: center;
    padding: 48px 20px;
    color: #94a3b8;
    font-size: 0.9rem;
}
.answer-placeholder .icon { font-size: 2rem; margin-bottom: 8px; }

/* ── Input section ───────────────────────────────────────── */
.input-section-label {
    font-size: 0.8rem;
    font-weight: 700;
    color: #475569;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-bottom: 8px;
    padding-top: 4px;
}

/* ── Divider ─────────────────────────────────────────────── */
hr { border-color: #e2e8f0 !important; margin: 12px 0 !important; }

/* ── Streamlit button overrides (main area) ─────────────── */
.stButton > button {
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    transition: all 0.15s ease !important;
}
.stButton > button[kind="primary"] {
    background: #2563eb !important;
    border: none !important;
}
.stButton > button[kind="primary"]:hover {
    background: #1d4ed8 !important;
    box-shadow: 0 4px 12px rgba(37,99,235,0.35) !important;
}

/* ── Text input ──────────────────────────────────────────── */
.stTextInput > div > div > input {
    border-radius: 8px !important;
    border: 1.5px solid #e2e8f0 !important;
    font-size: 0.92rem !important;
}
.stTextInput > div > div > input:focus {
    border-color: #2563eb !important;
    box-shadow: 0 0 0 3px rgba(37,99,235,0.15) !important;
}

/* ── Success/Error ───────────────────────────────────────── */
.stSuccess, .stError {
    border-radius: 8px !important;
    font-size: 0.88rem !important;
}

/* ── Caption / footer ───────────────────────────────────── */
.app-footer {
    text-align: center;
    color: #94a3b8;
    font-size: 0.72rem;
    padding: 16px 0 4px;
    border-top: 1px solid #f1f5f9;
    margin-top: 24px;
}
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# QUESTION BANK
# ═══════════════════════════════════════════════════════════════════════════════
raw_questions = r"""เชือกเส้นหนึ่งสั่นด้วยความถี่ค่าหนึ่ง ทำให้เกิดคลื่นต่อเนื่องเคลื่อนที่ไปทางขวาดังรูปที่ (1) เป็นภาพถ่ายการสั่นของเส้นเชือกในช่วงหนึ่งและในขณะที่คลื่นเคลื่อนที่ไป อนุภาคของเส้นเชือก การเคลื่อนที่ ขึ้น - ลง ซึ่งเมื่อเขียนกราฟแสดงความสัมพันธ์ระหว่างการกระจัดกับเวลาจะได้ดัง รูปที่ (2) จงหาอัตราเร็วของคลื่นบนเส้นเชือก
ในการสั่นเชือกที่มีความยาวมากเส้นหนึ่ง ปรากฏว่าหลังจากการสั่น 0.5 วินาที ได้คลื่นดังรูป จงหาอัตราเร็วของคลื่นบนเชือกเส้นนี้
เชือกที่ยาวมาก และสม่ำเสมอเส้นหนึ่งถูกขึงตึง ถ้าเราสะบัดปลายเชือกอีกข้างหนึ่ง ขึ้นลงอย่างสม่ำเสมอ เป็นเวลา 0.5 วินาที รูปร่างของเส้นเชือกจะเปลี่ยนแปลงดังรูป จงหา (ก) ความยาวคลื่น (ข) อัตราเร็วของคลื่น (ค) ความถี่ของคลื่น (ง) ความถี่ที่สะบัดปลายเชือก
จากรูปแสดงถึงการกระจัดของอนุภาคหนึ่งในตัวกลางเมื่อมีคลื่นผ่านโดยคลื่นที่ผ่านมีความเร็ว 20 เมตร/วินาที จงหาความยาวคลื่นของคลื่นที่กำลังเคลื่อนที่
เชือกยาวมากเส้นหนึ่งกำลังสั่น เมื่อมองเพียงส่วนหนึ่งซึ่งยาว 3.0 เมตร เห็นคลื่นในเส้นเชือกดังรูป (ก) แต่พอ 2 วินาที ต่อมาเปลี่ยนเป็นรูป (ข) จงหาอัตราเร็วของคลื่นที่มีค่าน้อยที่สุดเท่าไร
แหล่งกำเนิดคลื่นผิวน้ำสั่นด้วยความถี่ 20 รอบ/วินาที และพบว่าสันคลื่นน้ำ 5 สันติดต่อกันห่างกัน 20 เซนติเมตร จงหาอัตราเร็วของคลื่นผิวน้ำ
น้องดายืนอยู่ที่ท่าน้ำ สังเกตเห็นคลื่นผิวน้ำที่เกิดจากเรือวิ่งกระทบฝั่ง 20 ลูกคลื่นในเวลา 10 วินาที และทราบว่าอัตราเร็วของคลื่นผิวน้ำ 10 เมตร/วินาที อยากทราบว่าสันคลื่นที่อยู่ติดกันห่างกันเท่าไร
ชรินทร์โยนก้อนหินลงน้ำ ทำให้เกิดคลื่นผิวน้ำ 3 ลูกคลื่นวิ่งตามกันมา ถ้าตำแหน่งก้อนหินกระทบผิวน้ำห่างออกไป 10 เมตร พบว่าคลื่นลูกแรกวิ่งมาถึงฝั่งใช้เวลา 5 วินาที คลื่นลูกถัดไปมาถึงเมื่อเวลา 5.5 และ 6.0 วินาทีตามลำดับ จงหาความยาวคลื่นผิวน้ำที่เกิด
บัวตองยืนอยู่ริมฝั่งโขงสังเกตเห็นคลื่นผิวน้ำเคลื่อนกระทบฝั่ง มีระยะห่างระหว่างสันคลื่นที่อยู่ติดกัน 10 เมตร และคลื่นมีอัตราเร็ว 5 เมตร/วินาที อยากทราบว่าคลื่นขบวนนี้จะเคลื่อนกระทบฝั่งนาทีละกี่ลูก
แหล่งกำเนิดคลื่นน้ำจะต้องสั่นด้วยความถี่เท่าไร จึงทำให้เกิดคลื่นน้ำเคลื่อนที่ได้ทาง 40 เมตร ในเวลา 5 วินาที และมีระยะห่างของสันคลื่นจากสันที่ 1 ถึงสันที่ 5 เท่ากับ 2 เมตร
เชือกเส้นหนึ่งยาว 4 เมตร มีมวล 40 กรัม ปลายข้างหนึ่งติดกับเครื่องเคาะ ซึ่งสั่นอย่างสม่ำเสมอปลายอีกข้างหนึ่งมีแรงดึง 25 นิวตัน จงหาอัตราเร็วของคลื่นบนเส้นเชือก
เชือกเส้นหนึ่งเมื่อมีความตึง 45 นิวตัน พบว่าคลื่นบนเส้นเชือกมีอัตราเร็ว 30 เมตร/วินาที ถ้าลดความตึงเหลือ 20 นิวตัน อัตราเร็วของคลื่นบนเส้นเชือกมีค่าเท่าใด
คลื่นดลกำลังเคลื่อนที่จากซ้ายไปขวาด้วยอัตราเร็วคงที่ 20 ช่อง/วินาที ณ เวลาเริ่มต้น $t = 0$ เห็นคลื่นดังรูป เขียนรูปร่างคลื่น เมื่อเวลา 0.1, 0.2, 0.3, 0.4 และ 0.5 วินาที
เชือกเบาเส้นหนึ่งขึงตรึงในแนวระดับ แล้วสั่นที่ปลายข้างหนึ่งให้มีการกระจัดเป็นฟังก์ชันรูปไซน์ด้วยความถี่ 50 เฮิรตซ์ พบว่าคลื่นที่เกิดเคลื่อนที่ไปทางแกน +x ด้วยอัตราเร็ว 20 เมตร/วินาที จงหา ก. ความยาวคลื่นในเส้นเชือก ข. รูปร่างคลื่นจะเป็นอย่างไรเมื่อเวลาผ่านไป 0.1 วินาที
ลูกตุ้มอย่างง่ายผูกติดกับสายแขวนยาว 80 เซนติเมตร จงหาความถี่ธรรมชาติของการแกว่งของลูกตุ้มอย่างง่ายนี้
วัตถุมวล 0.4 กิโลกรัมติดกับปลายข้างหนึ่งของสปริงเส้นหนึ่งที่มีค่าคงตัวของสปริง 160 นิวตัน/เมตร ส่วนปลายของสปริงอีกข้างหนึ่งยึดติดกับเพดาน เมื่อออกแรงดึงวัตถุให้เคลื่อนที่ลงในแนวดิ่งเล็กน้อย แล้วปล่อยวัตถุจะสั่นขึ้นลงด้วยความถี่เท่าใด
ก. จงบอกตำแหน่งที่มีเฟสตรงกันกับจุด a, b, c, d, e, f, g, h, i ข. จงบอกตำแหน่งที่มีเฟสตรงข้ามกับจุด a, b, c, d, e, f, g, h, i วิเคราะห์โจทย์
คลื่นต่อเนื่องขบวนหนึ่งมีอัตราเร็ว 20 เมตร/วินาที เกิดจากแหล่งกำเนิดซึ่งสั่นด้วยความถี่ 40 เฮิรตซ์ ก. จุด 2 จุดบนคลื่นห่างกัน 10 เซนติเมตร จะมีเฟสต่างกันเท่าไร ข. จุด 2 จุดบนคลื่นมีเฟสต่างกัน $90^{\circ}$ จะห่างกันเท่าไร
คลื่นขบวนหนึ่งมีความถี่ 20 เฮิรตซ์ ระยะห่างระหว่างจุด 2 จุด ที่มีเฟสต่างกัน $\frac{\pi}{6}$ เรเดียน เป็น 0.5 เมตร จงหาอัตราเร็วของคลื่นนี้
จากรูปคลื่นมีอัตราเร็ว 2 เมตร/วินาที จุด 2 จุด บนคลื่นที่มีเฟสต่างกัน $\frac{3\pi}{2}$ เรเดียน จะอยู่ห่างกันเท่าไร
คลื่นต่อเนื่องขบวนหนึ่งเกิดจากแหล่งกำเนิดที่สั่น 40 รอบ/วินาที วัดอัตราเร็วคลื่นได้ 10 เมตร/วินาที จุด 2 จุดบนคลื่นซึ่งห่างกัน 1.5 เมตร จะมีเฟสต่างกันเท่าไร
คลื่นต่อเนื่องสองขบวน มีความถี่ 120 Hz และ 122 Hz เริ่มเคลื่อนที่ออกจากจุดเดียวกันด้วยเฟสตรงกัน เมื่อเวลา 1.2 วินาที คลื่นทั้งสองจะมีเฟสต่างกันเท่าไร
คลื่นผิวน้ำต่อเนื่องกระจายออกจากแหล่งกำเนิดคลื่น ซึ่งมีความถี่ 20 เฮิรตซ์ มีอัตราเร็ว 40 เซนติเมตร/วินาที ณ ตำแหน่งที่อยู่ห่างจากแหล่งกำเนิดเป็นระยะ 20 และ 21 เซนติเมตร จะมีเฟสต่างกันกี่องศา
แหล่งกำเนิด $S_1, S_2$ ให้คลื่นเฟสตรงกัน มีความยาวคลื่น 8 และ 10 เซนติเมตร ตามลำดับ จงหา ณ จุด P ที่อยู่ห่างจากแหล่งกำเนิด $S_1$ และ $S_2$ เป็นระยะ 20 และ 30 เซนติเมตร ดังรูป จะมีเฟสต่างกันเท่าใด
คลื่นต่อเนื่องขบวนหนึ่งเกิดจากแหล่งกำเนิด ซึ่งมีความถี่ 50 เฮิรตซ์ มีอัตราเร็ว 40 เมตร/วินาที จงหา ก. ณ จุดใดจุดหนึ่ง เมื่อเวลาผ่านไป 0.03 วินาที จะมีเฟสเปลี่ยนไปเท่าใด ข. ณ เวลาใดเวลาหนึ่ง จุด 2 จุด ห่างกัน 1 เมตร จะมีเฟสต่างกันเท่าใด
ส่งคลื่นที่มีความถี่ 200 เฮิรตซ์ออกไปโดยมีเฟสเริ่มต้น $60^{\circ}$ ต่อมาอีก 1.2 วินาทีก็ส่งคลื่นที่มีความถี่ 180 เฮิรตซ์ ออกไปโดยมีเฟสเริ่มต้น $30^{\circ}$ หลังจากนั้นนานเท่าใด จึงจะมีเฟสต่างกัน $90^{\circ}$ เป็นครั้งแรกและครั้งที่สอง
ส่งคลื่นความถี่ 240 เฮิรตซ์ออกไปโดยมีเฟสเริ่มต้น $50^{\circ}$ ต่อมาอีก 0.6 วินาที ก็ส่งคลื่นความถี่ 280 เฮิรตซ์ ออกไปโดยมีเฟสเริ่มต้น $20^{\circ}$ หลังจากนั้นนานเท่าใดจึงจะมีเฟสตรงกันเป็นครั้งแรก
จงเขียนรูปร่างของคลื่นซึ่งเกิดการซ้อนทับของคลื่นที่เคลื่อนที่เข้าหากันดังต่อไปนี้ทุกๆ วินาทีเป็นเวลา 5 วินาที กำหนดให้คลื่นมีอัตราเร็ว 2 ช่องต่อวินาที
จงเขียนรูปร่างของคลื่นซึ่งเกิดการซ้อนทับของคลื่นที่เคลื่อนที่เข้าหากันดังต่อไปนี้ทุกๆ วินาทีเป็นเวลา 5 วินาที กำหนดให้คลื่นมีอัตราเร็ว 2 ช่องต่อวินาที
คลื่นดลในเส้นเชือกมีอัตราเร็ว 4 ช่องต่อวินาที เมื่อเวลา $t = 0$ ดังรูป จงหาลักษณะของคลื่นเมื่อเวลาผ่านไป 2, 3, 4 วินาที ตามลำดับ
คลื่นดลในเส้นเชือกมีอัตราเร็ว 4 ช่องต่อวินาที เคลื่อนที่ตกกระทบจุดสะท้อนอิสระ เมื่อเวลา $t = 0$ เป็นดังรูป จงหาลักษณะของคลื่นเมื่อเวลาผ่านไป 2, 3 และ 4 วินาที ตามลำดับ
คลื่นน้ำในถาดคลื่นมีอัตราเร็วในน้ำลึกเป็น 2 เท่าของอัตราเร็วคลื่นในน้ำตื้น ถ้าคลื่นเคลื่อนที่จากน้ำลึกไปสู่น้ำตื้น โดยทำมุมตกกระทบ $60^{\circ}$ จงหามุมหักเหของคลื่นน้ำในน้ำตื้น
คลื่นน้ำในถาดคลื่นพบว่าบริเวณน้ำลึกระยะห่างระหว่างหน้าคลื่นที่ติดกันเท่ากับ 2 เซนติเมตร และบริเวณน้ำตื้นระยะห่างระหว่างหน้าคลื่นที่ติดกันเท่ากับ 1.5 เซนติเมตร ถ้ามุมระหว่างหน้าคลื่นในน้ำตื้นทำมุม $30^{\circ}$ กับรอยต่อของน้ำลึกและน้ำตื้น อยากทราบว่ามุมระหว่างหน้าคลื่นในน้ำลึกกับรอยต่อของน้ำลึกและน้ำตื้นเป็นเท่าใด
เมื่อคลื่นหน้าตรงเคลื่อนที่จากบริเวณ A ไปสู่บริเวณ B ในถาดคลื่น ทำให้เกิดการหักเหของคลื่น ปรากฏดังภาพ ถ้าแหล่งกำเนิดคลื่นมีความถี่ 40 Hz อัตราเร็วของคลื่นในบริเวณ B จะมีค่าเท่าไร
คลื่นน้ำขบวนหนึ่งเคลื่อนที่จากบริเวณน้ำตื้นไปสู่บริเวณน้ำลึก โดยแนวทางเดินของคลื่นตกกระทบทำมุมตกกระทบ $30^{\circ}$ ถ้าความยาวคลื่นในบริเวณน้ำลึกเป็น $\sqrt{3}$ เท่าของความยาวคลื่นในน้ำตื้น จงหามุมหักเห
คลื่นน้ำในถาดคลื่น เคลื่อนที่จากบริเวณน้ำลึกไปสู่บริเวณน้ำตื้น โดยมีมุมตกกระทบ $45^{\circ}$ และมุมหักเห $30^{\circ}$ ถ้าระยะห่างของหน้าคลื่นหักเหที่ติดกันวัดได้ $2\sqrt{2}$ เซนติเมตร และแหล่งกำเนิดคลื่นมีความถี่ 20 Hz จงหาอัตราเร็วคลื่นตกกระทบ
คลื่นน้ำมีอัตราเร็วในน้ำลึกเป็น 5/3 เท่าของอัตราเร็วในน้ำตื้น คลื่นจะต้องตั้งต้นเคลื่อนที่จากบริเวณใด จึงจะเกิดมุมวิกฤตได้ และมุมวิกฤตมีค่าเท่าใด
ถ้าอัตราเร็วของคลื่นในบริเวณน้ำลึก เป็น 2 เท่าของอัตราเร็วของคลื่นในบริเวณน้ำตื้น จงหามุมตกกระทบที่ทำให้เกิดการสะท้อนกลับหมด
คลื่นน้ำในถาดคลื่น เคลื่อนที่จากน้ำตื้นไปสู่น้ำลึก โดยมีมุมตกกระทบ $30^{\circ}$ และมุมหักเห $45^{\circ}$ ถ้าเปลี่ยนมุมตกกระทบเป็น $45^{\circ}$ มุมหักเหจะมีขนาดเท่าใด
แหล่งกำเนิดคลื่นน้ำสั่นด้วยความถี่ 8 เฮิรตซ์ วัดอัตราเร็วของคลื่นน้ำได้ 4 เมตร/วินาที เมื่อคลื่นน้ำเคลื่อนที่เข้าไปในบริเวณที่ตื้นกว่าเดิม โดยหน้าคลื่นตกกระทบทำมุม $\theta_1$ กับรอยต่อระหว่างตัวกลางพบว่าหน้าคลื่นหักเหทำมุม $\theta_2$ กับรอยต่อระหว่างตัวกลาง และระยะห่างของหน้าคลื่นหักเหที่ถัดกัน 5 แนวห่างกัน 1.8 เมตร จงหาอัตราส่วน $\sin\theta_1$ ต่อ $\sin\theta_2$
คลื่นน้ำเคลื่อนที่ผ่านบริเวณที่มีความลึกต่างกัน เกิดปรากฏการณ์ดังรูป ในบริเวณ (ก) หน้าคลื่นอยู่ห่างกัน 12 เซนติเมตร ในบริเวณ (ข) คลื่นมีความเร็ว $6\sqrt{2}$ เซนติเมตร/วินาที ถ้าต้นกำเนิดมาจากบริเวณ (ก) ความถี่ของต้นกำเนิดคลื่นมีค่าเท่าใด
กำหนดให้คลื่นน้ำหน้าตรงตกกระทบรอยต่อของบริเวณน้ำลึกและน้ำตื้นดังรูป จงเขียนภาพคลื่นหักเห
แหล่งกำเนิดอาพันธ์ 2 แหล่งห่างกัน 10 เซนติเมตร ให้คลื่นมีความยาวคลื่นเท่ากัน 2.5 เซนติเมตร เฟสตรงกัน จงหาว่าตำแหน่งต่อไปนี้อยู่บนแนวบัพหรือปฏิบัพที่เท่าใด ก. จุด A อยู่ห่างจากแหล่งกำเนิดทั้งสองเป็นระยะ 12 เซนติเมตร และ 17 เซนติเมตร ข. จุด B อยู่ห่างจากแหล่งกำเนิดทั้งสองเป็นระยะ 14.5 เซนติเมตร และ 15.75 เซนติเมตร ค. จุด C อยู่ห่างจากแหล่งกำเนิดทั้งสองเป็นระยะ 16 เซนติเมตร และ 24 เซนติเมตร
แหล่งกำเนิดอาพันธ์ 2 แหล่งเฟสตรงกัน ห่างกัน 12 เซนติเมตร มีความถี่เท่ากัน 10 เฮิรตซ์ และคลื่นเคลื่อนที่ด้วยอัตราเร็ว 40 เซนติเมตร/วินาที เท่ากัน จงหา ก. จุด X อยู่ห่างจากแหล่งกำเนิดทั้งสองเป็นระยะ 19 และ 25 เซนติเมตร ตามลำดับ จุด X จะอยู่บนแนวเสริมหรือหักล้างกันที่เท่าใด ข. จำนวนบัพและปฏิบัพที่เกิดขึ้นทั้งหมด
$S_1$ และ $S_2$ เป็นแหล่งกำเนิดอาพันธ์ห่างกัน 10 เซนติเมตร ให้คลื่นเฟสตรงกันและมีระยะห่างระหว่างหน้าคลื่น 2 เซนติเมตร ก. บนแนวเส้นตรง $S_1, S_2$ มีแนวปฏิบัพและบัพกี่แนว ข. ระหว่าง $S_1, S_2$ มีแนวปฏิบัพและบัพกี่แนว
$S_1$ และ $S_2$ เป็นแหล่งกำเนิดอาพันธ์ให้เฟสตรงข้ามกันห่างกัน 10 เซนติเมตร ให้คลื่นมีความยาวคลื่น 4 เซนติเมตร จงหาแนวปฏิบัพและบัพที่เกิดขึ้นระหว่าง $S_1$ และ $S_2$
จากการทดลองการแทรกสอดของคลื่นจากแหล่งกำเนิด $S_1$ และ $S_2$ ซึ่งมีเฟสตรงกัน ความถี่เท่ากัน วางห่างกัน $d$ ทำให้เกิดภาพการแทรกสอดในถาดคลื่นดังรูป โดยที่เส้นทึบแสดงแนวปฏิบัพ และเส้นประแสดงแนวบัพ ดังนั้นระยะห่างระหว่างแหล่งกำเนิดทั้งสองควรเป็นเท่าไรในเทอมของความยาวคลื่น
$S_1$ และ $S_2$ เป็นแหล่งกำเนิดอาพันธ์ มีเฟสตรงกัน ห่างกัน $a$ ให้คลื่นมีความยาวคลื่นเท่ากันคือ $\lambda$, P เป็นจุดที่เกิดการแทรกสอดแบบเสริมกันจุดที่ 2 จากแนวกลาง อยากทราบว่า $\theta$ จะมีค่าเท่าใด
แหล่งกำเนิดอาพันธ์ 2 แหล่งให้เฟสตรงกัน ห่างกัน 6 เซนติเมตรปรากฏว่าแนวเสริมกันครั้งแรกเบนออกจากแนวกลาง $30^{\circ}$ จงหาความยาวคลื่นจากแหล่งกำเนิดทั้งสอง
$S_1$ และ $S_2$ เป็นแหล่งกำเนิดอาพันธ์สองแหล่ง ห่างกัน 10 เซนติเมตร มีเฟสตรงกัน ความยาวคลื่น 1 เซนติเมตร จงหาระยะ x ซึ่งเป็นระยะจากแนวกลางไปยังตำแหน่งเสริมกันครั้งแรกจากแนวกลาง ดังรูป โดยระยะ $OA_0 = 60$ เซนติเมตร
จากรูป จุดกำเนิดคลื่นน้ำ S อยู่ห่างจากผิวสะท้อน 8 เซนติเมตร กระจายคลื่นที่มีความยาวคลื่น 4 เซนติเมตร ออกโดยรอบ ถ้าจุด P เป็นจุดใดๆ ซึ่งอยู่ห่างจาก S เป็นระยะ 12 เซนติเมตร จงหาว่าจุด P จะอยู่บนแนวอะไรของการแทรกสอด
จากรูป $S_1$ และ $S_2$ เป็นแหล่งกำเนิดอาพันธ์มีเฟสตรงกัน ให้คลื่นมีความถี่ 20 เฮิรตซ์ อยู่ห่างกัน 2 เมตร วัดอัตราเร็วของคลื่นได้ 10 เมตร/วินาที จงหาตำแหน่งของจุดที่แนวปฏิบัพตัดแนว $S_1P$ ซึ่งตั้งฉากกับเส้น $S_1$ และ $S_2$
ลวดเส้นหนึ่งยาว 40 เซนติเมตร ปลายทั้งสองถูกขึงตึง เมื่อดีดลวดตรงกลางทำให้เส้นลวดสั่นขึ้นลงด้วยความถี่ 20 เฮิรตซ์ จงหาอัตราเร็วของคลื่นในลวดเส้นนี้
เชือกเส้นหนึ่งยาว 3 เมตร ปลายข้างหนึ่งยึดติดกับกำแพง จับปลายอีกข้างหนึ่งสะบัดขึ้นลงอย่างสม่ำเสมอทำให้เกิดคลื่นมีความยาวคลื่น 0.5 เมตร จงหาว่าระหว่างปลายเส้นเชือกทั้งสองมีตำแหน่งบัพและปฏิบัพกี่ตำแหน่ง
แหล่งกำเนิดคลื่นน้ำในถาดคลื่นอยู่ห่างจากผิวสะท้อนระนาบตรง 20 เซนติเมตร ให้คลื่นมีความยาวคลื่น 4 เซนติเมตร ตกกระทบผิวสะท้อนในแนวตั้งฉาก จงหาว่าระหว่างแหล่งกำเนิดและผิวสะท้อนจะมีตำแหน่งบัพและปฏิบัพกี่ตำแหน่ง
คลื่นต่อเนื่องในขดสปริง มีความยาวคลื่น 8 เซนติเมตร เคลื่อนที่ไปยังปลายข้างหนึ่งซึ่งยึดแน่นไว้ ถ้าลวดสปริงยาว 20 เซนติเมตร จะเกิดคลื่นนิ่งมีบัพกี่บัพ และมีปฏิบัพกี่ปฏิบัพ
คลื่นนิ่งมีระยะห่างของบัพที่ติดกัน 10 เซนติเมตร ถ้าอัตราเร็วของคลื่น 160 เซนติเมตร/วินาที จงหาความถี่ของแหล่งกำเนิด
ในการทดลองคลื่นนิ่งบนเส้นเชือก ถ้าความถี่ของคลื่นนิ่งเป็น 500 เฮิรตซ์ และอัตราเร็วของคลื่นในเส้นเชือกเท่ากับ 400 เมตรต่อวินาที ตำแหน่งบัพสองตำแหน่งที่อยู่ถัดกันจะห่างกันเท่าไร
เชือกเบาเส้นหนึ่งยาว 1.25 เมตร ถูกขึงตึงที่ปลายทั้งสองข้าง เมื่อทำให้เชือกสั่นวัดอัตราเร็วได้ 160 เมตรต่อวินาที ถ้าคลื่นในเส้นเชือกเกิดการสั่นพ้องได้ต้องให้ความถี่เข้าไปเท่าไร
เส้นลวดยาว 1.20 เมตร ปลายทั้งสองถูกขึงตึง เมื่อลวดสั่นด้วยความถี่ 320 เฮิรตซ์ จะเกิดการสั่นพ้องในขั้นโอเวอร์โทนที่ 2 จงหาอัตราเร็วของคลื่นในลวดเส้นนี้
เชือกเส้นหนึ่งยาว 90 เซนติเมตรหนัก 56.25 กรัม ถูกทำให้สั่นด้วยความถี่เท่าไร จึงจะเกิดการสั่นพ้องในขั้นฮาร์โมนิกที่ 4 ขณะนั้นเชือกมีความตึง 100 นิวตัน
สายกีตาร์ยาว 1 เมตร มีมวล 12.96 กรัม ถูกขึงตึงที่จุดสองจุดห่างกัน 75 เซนติเมตร เมื่อทำให้สายกีตาร์สั่นวัดความตึงในสายกีตาร์ได้ 40 นิวตัน พบว่าเกิดการสั่นพ้องขึ้นในสายกีตาร์ แต่เมื่อเพิ่มความตึงขึ้นเป็น 90 นิวตัน ปรากฏว่าเกิดการสั่นพ้องขึ้นในสายกีตาร์ในขั้นถัดไป จงหาจำนวน loop ของคลื่นนิ่งที่เกิดทั้งสองครั้ง
ช่องเปิดเดี่ยวกว้าง 6 เซนติเมตร ให้คลื่นหน้าตรงมีความยาวคลื่น 2 เซนติเมตร เคลื่อนที่ผ่าน จงหาแนวบัพที่เกิดขึ้นทั้งหมด
คลื่นน้ำหน้าตรงมีความยาวคลื่น 2.5 เซนติเมตร ผ่านอย่างตั้งฉากกับช่องเปิดเดี่ยวซึ่งกว้าง 8 เซนติเมตร จงหา ก. แนวบัพที่เกิดขึ้นทั้งหมด ข. แนวบัพที่ 2 เบนจากแนวกลางเท่าไร ค. แนวปฏิบัพแรกเบนจากแนวกลางเท่าไร
คลื่นหน้าตรงต่อเนื่องเคลื่อนที่ผ่านช่องเปิดเดี่ยวโดยหน้าคลื่นขนานกับช่องเปิดนี้ปรากฏว่าเกิดบัพ 6 แนวพอดี ถ้าความกว้างของช่องเปิดเพิ่มขึ้นเป็นสองเท่าของเดิมและความถี่ของคลื่นลดลงเป็น 1/3 เท่าของเดิม จะเกิดแนวบัพผ่านช่องเปิดกี่แนว
ช่องแคบเดี่ยวจะต้องกว้างเท่าไรจึงจะทำให้คลื่นที่มีความยาวคลื่น 3 เซนติเมตร ผ่านแล้วเกิดแนวบัพทั้งหมด 6 แนว
ช่องเดี่ยวกว้าง 4 เซนติเมตร จะต้องให้คลื่นมีความยาวคลื่นเท่าไร ผ่านในแนวตั้งฉากกับช่องเดี่ยวนี้ จึงจะทำให้เกิดแนวบัพรอบช่องเดี่ยว 4 แนว
ช่องแคบคู่อยู่ห่างกัน 8 เซนติเมตร ในถาดคลื่น ถ้าทำให้เกิดคลื่นหน้าตรงผ่านช่องแคบคู่นั้นในแนวตั้งฉาก ทำให้เกิดการแทรกสอดขึ้น ถ้าจุด A อยู่บนแนวปฏิบัพที่ 2 ซึ่งอยู่ห่างจากช่องแคบทั้งสองเป็นระยะ 10 เซนติเมตร และ 14 เซนติเมตร ตามลำดับ จงหา ก. ความยาวคลื่นน้ำ ข. แนวบัพและปฏิบัพที่เกิดขึ้นทั้งหมด
"""
questions = [q.strip() for q in raw_questions.strip().split("\n") if q.strip()]

# ── Topic groups ──────────────────────────────────────────────────────────────
TOPICS = [
    ("🌊 สมบัติพื้นฐาน",     list(range(1,  13))),
    ("📦 คลื่นดล",            list(range(13, 15))),
    ("🔁 SHM",                list(range(15, 17))),
    ("📐 เฟส",                list(range(17, 28))),
    ("➕ การซ้อนทับ",         list(range(28, 32))),
    ("↗️ การหักเห",           list(range(32, 43))),
    ("🌀 การแทรกสอด",         list(range(43, 53))),
    ("🎵 คลื่นนิ่ง/สั่นพ้อง", list(range(53, 63))),
    ("🔬 การเลี้ยวเบน",       list(range(63, 69))),
]

# ── Session state ─────────────────────────────────────────────────────────────
if "results"    not in st.session_state: st.session_state.results    = {}
if "selected_q" not in st.session_state: st.session_state.selected_q = 1
if "show_ans"   not in st.session_state: st.session_state.show_ans   = False


def _select(q: int):
    st.session_state.selected_q = q
    st.session_state.show_ans   = False


def _badge(q: int) -> str:
    if q not in st.session_state.results: return ""
    res = st.session_state.results[q]
    return " ✅" if all(res) else (" ⚠️" if any(res) else " ✗")


def _fmt(expected: float, tol: float, unit: str) -> str:
    u = f" {unit}" if unit else ""
    return f"{int(round(expected))}{u}" if tol == 0 else f"{expected:.4g}{u}"


def _progress() -> tuple[int, int]:
    done = sum(1 for q, r in st.session_state.results.items() if r and all(r))
    return done, len(questions)


# ═══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    # ── App title ──────────────────────────────────────────────────────────
    st.markdown("""
    <div style="padding: 16px 4px 8px;">
        <div class="sidebar-title">🌊 คลื่นกล — ม.5</div>
        <div class="sidebar-sub">Physics Exercise Platform</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Progress bar ───────────────────────────────────────────────────────
    done, total = _progress()
    pct = done / total
    st.markdown(f"""
    <div style="margin: 0 0 4px 0;">
        <div style="display:flex;justify-content:space-between;margin-bottom:4px;">
            <span style="font-size:0.68rem;color:#64748b;font-weight:600;text-transform:uppercase;letter-spacing:0.06em;">ความก้าวหน้า</span>
            <span style="font-size:0.68rem;color:#94a3b8;">{done}/{total} ข้อ</span>
        </div>
        <div style="background:#1e293b;border-radius:4px;height:5px;overflow:hidden;">
            <div style="background:linear-gradient(90deg,#2563eb,#38bdf8);width:{pct*100:.0f}%;height:100%;border-radius:4px;transition:width 0.3s;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    # ── Export button ──────────────────────────────────────────────────────
    if st.button("📄 สร้างไฟล์โจทย์ทั้งหมด",
                 use_container_width=True, key="gen_pdf_btn"):
        with st.spinner("กำลังสร้างไฟล์..."):
            from pdf_export import generate_problems_pdf
            st.session_state["_pdf_bytes"] = generate_problems_pdf(
                questions, get_plot_for_question
            )

    if "_pdf_bytes" in st.session_state:
        st.download_button(
            "⬇ ดาวน์โหลด HTML → เปิด → Ctrl+P",
            data=st.session_state["_pdf_bytes"],
            file_name="physics_problems.html",
            mime="text/html",
            use_container_width=True,
            key="dl_pdf_btn",
            type="primary",
        )

    st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
    st.markdown("<hr style='border-color:#1e293b;margin:8px 0;'>", unsafe_allow_html=True)

    # ── Question navigation ────────────────────────────────────────────────
    for topic_name, q_nums in TOPICS:
        st.markdown(
            f'<p class="topic-label">{topic_name}</p>',
            unsafe_allow_html=True,
        )
        for row_start in range(0, len(q_nums), 6):
            row  = q_nums[row_start: row_start + 6]
            cols = st.columns(len(row))
            for col, qn in zip(cols, row):
                is_active = st.session_state.selected_q == qn
                label     = f"{qn}{_badge(qn)}"
                if col.button(label, key=f"nav_{qn}",
                              type="primary" if is_active else "secondary",
                              use_container_width=True):
                    _select(qn)
                    st.rerun()

    st.markdown("""
    <div style="padding:16px 0 4px;text-align:center;font-size:0.65rem;color:#334155;">
        ฟิสิกส์ ม.5 · Streamlit
    </div>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN TABS
# ═══════════════════════════════════════════════════════════════════════════════
tab_exercise, tab_summary = st.tabs(["📚  แบบฝึกหัด", "📖  สรุปทฤษฎีการแทรกสอด"])

with tab_summary:
    render_summary()

with tab_exercise:
    i        = st.session_state.selected_q
    q_text   = questions[i - 1]
    key_data = ANSWER_KEYS.get(i)
    answer   = ANSWERS.get(i)
    topic_of_q = next((t for t, qs in TOPICS if i in qs), "")
    badge_str  = _badge(i)

    # ── Question header ───────────────────────────────────────────────────
    col_title, col_nav = st.columns([8, 1], gap="small")

    with col_title:
        st.markdown(f"""
        <div class="q-header-bar">
            <span class="q-num-badge">ข้อที่ {i}</span>
            <span class="topic-chip">{topic_of_q}</span>
            {'<span style="font-size:1.1rem;">'+badge_str.strip()+'</span>' if badge_str.strip() else ''}
        </div>
        """, unsafe_allow_html=True)

    with col_nav:
        st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
        n1, n2 = st.columns(2)
        if n1.button("◀", disabled=(i <= 1), use_container_width=True, key="prev"):
            _select(i - 1); st.rerun()
        if n2.button("▶", disabled=(i >= len(questions)), use_container_width=True, key="next"):
            _select(i + 1); st.rerun()

    st.markdown("<hr style='margin:10px 0 18px'>", unsafe_allow_html=True)

    # ── Two-column layout ─────────────────────────────────────────────────
    left, right = st.columns([11, 9], gap="large")

    # ── LEFT: Question + input ────────────────────────────────────────────
    with left:
        # Question text in a card
        st.markdown(f"""
        <div class="card" style="margin-bottom:16px;line-height:1.9;font-size:1.0rem;">
            {q_text}
        </div>
        """, unsafe_allow_html=True)

        fig = get_plot_for_question(i)
        if fig:
            st.pyplot(fig, use_container_width=True)

        # Answer input section
        st.markdown("<div class='input-section-label'>✏️ กรอกคำตอบ</div>",
                    unsafe_allow_html=True)

        if key_data is None:
            st.info("📝 ข้อนี้ตรวจโดยดูจากเฉลยละเอียด")
            st.text_area("บันทึกคำตอบ / แนวคิด", key=f"note_{i}", height=80,
                         label_visibility="collapsed",
                         placeholder="จดแนวคิดหรือคำตอบของคุณที่นี่...")
        else:
            n = len(key_data)
            cols = st.columns(min(n, 2))
            for j, (label, exp, unit, tol) in enumerate(key_data):
                unit_lbl = f" ({unit})" if unit else ""
                with cols[j % min(n, 2)]:
                    st.text_input(
                        f"{label}{unit_lbl}",
                        key=f"ans_{i}_{j}",
                        placeholder=f"เช่น {_fmt(exp, tol, '')}",
                    )

            if st.button("✅ ตรวจคำตอบ", key=f"btn_{i}",
                         type="primary", use_container_width=True):
                res = [
                    check_answer(st.session_state.get(f"ans_{i}_{j}", ""), exp, tol)
                    for j, (_, exp, _, tol) in enumerate(key_data)
                ]
                st.session_state.results[i] = res

            if i in st.session_state.results:
                st.markdown("<div style='margin-top:10px'></div>", unsafe_allow_html=True)
                for is_ok, (label, exp, unit, tol) in zip(
                        st.session_state.results[i], key_data):
                    ans_str = _fmt(exp, tol, unit)
                    if is_ok:
                        st.success(f"✓  {label} — ถูกต้อง!")
                    else:
                        st.error(f"✗  {label} — ยังไม่ถูก  |  เฉลย: **{ans_str}**")

    # ── RIGHT: Answer panel ───────────────────────────────────────────────
    with right:
        st.markdown("""
        <div class="answer-card-header">
            📖 &nbsp;เฉลยละเอียด
        </div>
        <div class="answer-card-body">
        """, unsafe_allow_html=True)

        if not st.session_state.show_ans:
            st.markdown("""
            <div class="answer-placeholder">
                <div class="icon">🔒</div>
                กดปุ่มด้านล่างเพื่อเปิดเฉลย
            </div>
            """, unsafe_allow_html=True)
        else:
            if answer:
                st.markdown(answer)
            else:
                st.info("ยังไม่มีเฉลยสำหรับข้อนี้")

        st.markdown("</div>", unsafe_allow_html=True)

        btn_label = "🙈  ซ่อนเฉลย" if st.session_state.show_ans else "👁  แสดงเฉลย"
        st.markdown("<div style='margin-top:8px'></div>", unsafe_allow_html=True)
        if st.button(btn_label, key="toggle_ans", use_container_width=True):
            st.session_state.show_ans = not st.session_state.show_ans
            st.rerun()
