import streamlit as st
import requests
from datetime import datetime

# ==========================================
# ⚙️ ตั้งค่า LINE
# ==========================================
LINE_TOKEN = "Gaow3ZPWwaqdrBsLWEF54B6xlMmrls4NV1exzMjShgmWQS6bsCWyxlPm6tli+MY4ImenfaWuiNnse1Q3QaGl7Pj9c8u79m6PXZkRZuwr4J5/DKd6yw0zLz1yQL62EmXMnC94YGgBi/1CX4ZTxbeSXwdB04t89/1O/w1cDnyilFU="
GROUP_ID = "Ca5467fb421c7c3878130f77530617627"
# ==========================================

def send_line_message(message):
    url = 'https://api.line.me/v2/bot/message/push'
    headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {LINE_TOKEN}'}
    data = {"to": GROUP_ID, "messages": [{"type": "text", "text": message}]}
    return requests.post(url, headers=headers, json=data)

# --- ตั้งค่าหน้าเว็บ ---
st.set_page_config(page_title="ระบบบันทึกรับสมัคร (Admin)", page_icon="🎓", layout="centered")

# --- CSS ตกแต่งปุ่ม ---
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        border-radius: 20px;
        height: 50px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🎓 ระบบแจ้งเตือนผู้สมัคร (Admin)")
st.caption("สำหรับเจ้าหน้าที่กรอกข้อมูลเพื่อแจ้งเตือนผู้บริหาร")

# --- ใช้ Session State จัดการสถานะ ---
if 'form_submitted' not in st.session_state:
    st.session_state.form_submitted = False

# --- ฟอร์มกรอกข้อมูล ---
with st.form("admission_form", clear_on_submit=True):
    st.subheader("1. ข้อมูลนักศึกษา")
    
    col1, col2 = st.columns(2)
    with col1:
        student_name = st.text_input("👤 ชื่อ-นามสกุล", placeholder="ระบุชื่อภาษาไทย...")
        # [NEW] เพิ่มช่องโรงเรียนตรงนี้
        school_name = st.text_input("🏫 โรงเรียนเดิม", placeholder="เช่น รร.ราชสีมาวิทยาลัย")
        
    with col2:
        gpax = st.text_input("📊 เกรดเฉลี่ย (GPAX)", placeholder="เช่น 3.50")
        phone = st.text_input("📞 เบอร์โทรศัพท์", placeholder="08x-xxx-xxxx")
    
    # เวลาที่สมัคร (เอาไว้แถวล่างสุดของส่วนตัว)
    apply_time = st.text_input("🕒 เวลาที่สมัคร", value=datetime.now().strftime("%d/%m/%Y %H:%M"))

    st.subheader("2. หลักฐานการสมัคร")
    drive_link = st.text_input("🔗 ลิงก์ Google Drive (รวมเอกสาร)", placeholder="https://drive.google.com/...")
    
    st.markdown("**รายการเอกสารที่แนบมา:**")
    c1, c2 = st.columns(2)
    with c1:
        doc_photo = st.checkbox("รูปถ่าย 1 นิ้ว")
        doc_idcard = st.checkbox("สำเนาบัตรประชาชน")
        doc_house = st.checkbox("สำเนาทะเบียนบ้าน")
        doc_parents = st.checkbox("ทะเบียนบ้าน บิดา/มารดา")
    with c2:
        doc_transcript = st.checkbox("ใบ ปพ.1 (Transcript)")
        doc_portfolio = st.checkbox("แฟ้มสะสมผลงาน (Portfolio)")
        doc_scores = st.checkbox("คะแนนสอบ (IELTS/9 วิชา)")
        doc_slip = st.checkbox("หลักฐานการโอนเงิน")

    st.markdown("---")
    
    # --- จัดเตรียมข้อความส่งไลน์ ---
    docs_list = []
    if doc_photo: docs_list.append("- รูปถ่าย")
    if doc_idcard: docs_list.append("- บัตรประชาชน")
    if doc_house: docs_list.append("- ทะเบียนบ้าน")
    if doc_parents: docs_list.append("- ทะเบียนบ้าน พ่อแม่")
    if doc_transcript: docs_list.append("- Transcript")
    if doc_portfolio: docs_list.append("- Portfolio")
    if doc_scores: docs_list.append("- คะแนนสอบ")
    if doc_slip: docs_list.append("- สลิปโอนเงิน")
    
    docs_text = "\n".join(docs_list) if docs_list else "- (ไม่มีเอกสารแนบ)"
    
    # [UPDATE] เพิ่มชื่อโรงเรียนลงในข้อความ
    final_msg = f"""🔔 ผู้สมัครใหม่ (รับเรื่องโดยเจ้าหน้าที่)
----------------------------
👤 ชื่อ: {student_name}
🏫 รร.: {school_name if school_name else "-"}
📊 เกรด: {gpax}
📞 โทร: {phone}
🕒 เวลา: {apply_time}
----------------------------
📂 เอกสารที่ได้รับ:
{docs_text}

🔗 ลิงก์เอกสาร:
{drive_link if drive_link else "(ไม่มีลิงก์)"}
"""

    # ปุ่มส่ง
    submitted = st.form_submit_button("🚀 ยืนยันและส่งแจ้งเตือน")

    if submitted:
        if not student_name:
            st.error("⚠️ กรุณากรอกชื่อนักศึกษา!")
        else:
            try:
                res = send_line_message(final_msg)
                if res.status_code == 200:
                    st.success(f"✅ ส่งข้อมูลของ '{student_name}' เรียบร้อยแล้ว!")
                    st.balloons()
                else:
                    st.error(f"❌ เกิดข้อผิดพลาด: {res.text}")
            except Exception as e:
                st.error(f"❌ Error: {e}")