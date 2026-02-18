import streamlit as st
import google.generativeai as genai
from datetime import datetime

# --- 1. CONFIG & CUSTOM UI (ทำให้เหมือนแอป) ---
st.set_page_config(page_title="PEA MAERIM Fleet Flow", layout="wide")

# CSS ขั้นสูงเพื่อแต่งหน้าตาให้เหมือนต้นฉบับ
st.markdown("""
    <style>
    /* ปรับแต่งพื้นหลังและ Font */
    @import url('https://fonts.googleapis.com/css2?family=Sarabun:wght@300;400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Sarabun', sans-serif; }
    
    .stApp { background-color: #F0F2F6; }
    
    /* แต่งแถบเมนูข้างบน (Mobile-friendly Header) */
    .main-header {
        background: linear-gradient(90deg, #542173 0%, #7B3EAD 100%);
        padding: 20px;
        border-radius: 0px 0px 30px 30px;
        color: white;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 4px 15px rgba(84, 33, 115, 0.3);
    }
    
    /* แต่งการ์ดสถานะ */
    .card {
        background: white;
        padding: 25px;
        border-radius: 20px;
        border-top: 6px solid #FFB800;
        box-shadow: 0 10px 20px rgba(0,0,0,0.05);
        text-align: center;
        transition: transform 0.3s;
    }
    .card:hover { transform: translateY(-5px); }
    
    /* ปุ่มกดสไตล์ PEA */
    .stButton>button {
        width: 100%;
        background: #542173;
        color: white;
        border-radius: 15px;
        padding: 10px;
        border: none;
        font-weight: bold;
    }
    .stButton>button:hover {
        background: #FFB800;
        color: #542173;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. HEADER ---
st.markdown("""
    <div class="main-header">
        <h1 style="color: white; margin:0;">PEA MAERIM Fleet Flow</h1>
        <p style="color: #FFB800; margin:0;">ระบบบริหารจัดการยานพาหนะ กฟภ.แม่ริม</p>
    </div>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR NAVIGATION ---
with st.sidebar:
    st.image("https://www.pea.co.th/Portals/0/logo.png", width=150)
    st.markdown("---")
    menu = st.selectbox("เลือกเมนูการใช้งาน", 
        ["หน้าหลัก", "จองรถยนต์", "ตรวจเช็ครถก่อนใช้", "คืนรถยนต์", "ประวัติการซ่อม & AI"])

# --- 4. APP LOGIC ---

if menu == "หน้าหลัก":
    # ส่วนสรุปจำนวนรถ (Stat Cards)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="card"><p>รถทั้งหมด</p><h2 style="color:#542173">8</h2></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="card"><p>พร้อมใช้</p><h2 style="color:green">5</h2></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="card"><p>แจ้งเตือนภาษี</p><h2 style="color:red">2</h2></div>', unsafe_allow_html=True)
    
    st.markdown("### 📍 สถานะรถยนต์ปัจจุบัน")
    # แสดงการ์ดรถแบบที่ออกแบบไว้
    st.markdown("""
        <div style="background: white; padding: 15px; border-radius: 15px; margin-bottom: 10px; border-left: 10px solid green; display: flex; justify-content: space-between; align-items: center;">
            <div>
                <b>ทะเบียน กข-1234 (รถตู้)</b><br>
                <small>อายุใช้งาน: 3 ปี 2 เดือน | เลขไมล์: 45,200 กม.</small>
            </div>
            <div style="color: green; font-weight: bold;">ว่าง</div>
        </div>
        """, unsafe_allow_html=True)

elif menu == "จองรถยนต์":
    st.subheader("📝 แบบฟอร์มขอใช้รถยนต์")
    with st.expander("คลิกเพื่อกรอกข้อมูลการจอง", expanded=True):
        name = st.text_input("ชื่อ-นามสกุล ผู้ขอใช้รถ")
        emp_id = st.text_input("รหัสพนักงาน")
        car = st.selectbox("เลือกยานพาหนะ", ["กข-1234 (รถตู้)", "มค-5566 (รถกระบะ)", "ทส-9988 (รถเครน)"])
        t1, t2 = st.columns(2)
        start = t1.date_input("วันที่เริ่ม")
        end = t2.date_input("วันที่คืน")
        
        if st.button("ยืนยันคำขอจองรถ"):
            if name and emp_id:
                st.balloons()
                st.success("ส่งข้อมูลขอจองไปยังผู้อนุมัติเรียบร้อยแล้ว!")
            else:
                st.error("กรุณากรอกข้อมูลพนักงานให้ครบถ้วน")

# ส่วนที่เหลือ (AI, ตรวจสภาพ) คุณสามารถใช้โครงสร้างเดิมได้เลยครับ
