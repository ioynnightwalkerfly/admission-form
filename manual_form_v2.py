import streamlit as st
import requests
from datetime import datetime

# ==========================================
# ⚙️ ตั้งค่า LINE
# ==========================================
LINE_TOKEN = "s1Q5YP0fuYSn8TZldaO5pvI3uVEYjSMMC2XQ9DfAZA0ioyZp3uxPFWlqHUzqxmsSImenfaWuiNnse1Q3QaGl7Pj9c8u79m6PXZkRZuwr4J535obAkdt4not7fcah0m4zW7XE+qOGBim0Cpmwc+ANTgdB04t89/1O/w1cDnyilFU="
GROUP_ID = "C7b1de1ece104d6805c5dad65f334c1d6"
# ==========================================

def send_line_message(message):
    url = 'https://api.line.me/v2/bot/message/push'
    headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {LINE_TOKEN}'}
    data = {"to": GROUP_ID, "messages": [{"type": "text", "text": message}]}
    return requests.post(url, headers=headers, json=data)

# --- ตั้งค่าหน้าเว็บ ---
st.set_page_config(page_title="ระบบบันทึกรับสมัคร (Admin)", page_icon="🎓", layout="centered")

# --- CSS ตกแต่ง ---
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        border-radius: 20px;
        height: 50px;
        font-weight: bold;
    }
    .report-section {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🎓 ระบบแจ้งเตือนผู้สมัคร (Admin)")

# --- จัดการ Session State เพื่อล้างค่า ---
if 'reset_trigger' not in st.session_state:
    st.session_state.reset_trigger = False

if 'default_time' not in st.session_state:
    st.session_state.default_time = datetime.now().strftime("%d/%m/%Y %H:%M")

def clear_form():
    st.session_state.reset_trigger = True
    st.session_state.default_time = datetime.now().strftime("%d/%m/%Y %H:%M")
    st.rerun()

# Logic การคืนค่าฟอร์ม
if st.session_state.reset_trigger:
    st.session_state.reset_trigger = False
    name_val, school_val, gpax_val, phone_val, link_val = "", "", "", "", ""
    time_val = st.session_state.default_time
else:
    name_val = st.session_state.get("k_name", "")
    school_val = st.session_state.get("k_school", "")
    gpax_val = st.session_state.get("k_gpax", "")
    phone_val = st.session_state.get("k_phone", "")
    time_val = st.session_state.get("k_time", st.session_state.default_time)
    link_val = st.session_state.get("k_link", "")

# ==========================================
# 📝 ส่วนที่ 1: ฟอร์มกรอกข้อมูลผู้สมัคร
# ==========================================
with st.form("admission_form"):
    st.subheader("1. ข้อมูลนักศึกษา")
    col1, col2 = st.columns(2)
    with col1:
        student_name = st.text_input("👤 ชื่อ-นามสกุล", value=name_val, key="k_name")
        school_name = st.text_input("🏫 โรงเรียนเดิม", value=school_val, key="k_school")
    with col2:
        gpax = st.text_input("📊 เกรดเฉลี่ย (GPAX)", value=gpax_val, key="k_gpax")
        phone = st.text_input("📞 เบอร์โทรศัพท์", value=phone_val, key="k_phone")
    
    apply_time = st.text_input("🕒 เวลาที่สมัคร", value=time_val, key="k_time")

    st.subheader("2. หลักฐานการสมัคร")
    drive_link = st.text_input("🔗 ลิงก์ Google Drive", value=link_val, key="k_link")
    
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
    
    # ปุ่มส่งข้อมูล
    submitted = st.form_submit_button("🚀 ยืนยันและส่งแจ้งเตือน")

    if submitted:
        if not student_name:
            st.error("⚠️ กรุณากรอกชื่อนักศึกษา!")
        else:
            # สร้างข้อความ
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
            try:
                res = send_line_message(final_msg)
                if res.status_code == 200:
                    st.success(f"✅ ส่งข้อมูลของ '{student_name}' เรียบร้อยแล้ว!")
                    st.balloons()
                    st.info("💡 ข้อมูลยังค้างอยู่หน้าจอ | กดปุ่ม 'ล้างหน้าจอ' ด้านล่างเพื่อเริ่มคนใหม่")
                else:
                    st.error(f"❌ ส่งไม่ผ่าน: {res.text}")
            except Exception as e:
                st.error(f"❌ Error: {e}")

# ปุ่ม Reset
st.markdown("<br>", unsafe_allow_html=True)
if st.button("🔄 ล้างหน้าจอ (กรอกคนต่อไป)"):
    clear_form()

# ==========================================
# 📢 ส่วนที่ 2: รายงานกรณีไม่มีผู้สมัคร (New Feature)
# ==========================================
st.markdown("---")
with st.expander("📢 รายงานสถานะประจำวัน (คลิกเพื่อเปิด)"):
    st.write("ใช้สำหรับกดรายงานผู้บริหาร ในวันที่ **ไม่มีผู้สมัคร**")
    
    col_a, col_b = st.columns([3, 1])
    with col_a:
        report_date = st.text_input("วันที่รายงาน", value=datetime.now().strftime("%d/%m/%Y"), key="report_date")
    
    if st.button("✅ แจ้งว่า 'วันนี้ไม่มีผู้สมัคร'", type="primary"):
        no_app_msg = f"""🔔 รายงานสถานะ 
📅 ประจำวันที่: {report_date}

✅ ตรวจสอบแล้ว ยังไม่พบผู้สมัครรายใหม่ในรอบนี้ครับ"""
        
        try:
            res = send_line_message(no_app_msg)
            if res.status_code == 200:
                st.success("ส่งรายงานสถานะเรียบร้อย!")
            else:
                st.error("เกิดข้อผิดพลาดในการส่ง")
        except Exception as e:
            st.error(f"Error: {e}")
