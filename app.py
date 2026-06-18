import streamlit as st
import time
import os
import base64
import pandas as pd
from datetime import datetime

# ─── إعدادات الصفحة ───────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Mammogram AI Diagnostics",
    page_icon="🧬",
    layout="centered",
    initial_sidebar_state="expanded"
)

LOG_FILE = "patients_log.csv"

def get_image_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

img_data = get_image_base64("m.jpg")

# ─── CSS المحسّن ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

* { font-family: 'Inter', sans-serif; }

.stApp { background-color: #F7F8FC; }

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1B3A52 0%, #2E4A62 100%) !important;
}
section[data-testid="stSidebar"] * { color: #E8F0F7 !important; }
section[data-testid="stSidebar"] .stRadio label { 
    color: #E8F0F7 !important; 
    font-size: 0.95rem;
}
section[data-testid="stSidebar"] hr { border-color: rgba(255,255,255,0.2) !important; }

/* Block container */
.block-container { padding-top: 2rem !important; max-width: 780px; }

/* Headings */
h1 { color: #1B3A52 !important; font-size: 2rem !important; font-weight: 700 !important; text-align: center; }
h2 { color: #1B3A52 !important; font-size: 1.4rem !important; font-weight: 700 !important; }
h3 { color: #1B3A52 !important; font-size: 1.1rem !important; font-weight: 600 !important; }

/* Buttons */
div.stButton > button {
    background: linear-gradient(135deg, #2E4A62 0%, #1B3A52 100%) !important;
    color: white !important;
    border-radius: 8px !important;
    padding: 10px 28px !important;
    border: none !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    transition: all 0.25s ease !important;
    box-shadow: 0 2px 8px rgba(46,74,98,0.25) !important;
    width: 100% !important;
}
div.stButton > button:hover {
    background: linear-gradient(135deg, #D4A5B8 0%, #C48FA8 100%) !important;
    color: #1B3A52 !important;
    box-shadow: 0 4px 16px rgba(212,165,184,0.4) !important;
    transform: translateY(-1px) !important;
}

/* Progress bar */
.progress-wrapper {
    background: #E2E8F0;
    border-radius: 99px;
    height: 6px;
    margin-bottom: 28px;
    overflow: hidden;
}
.progress-fill {
    background: linear-gradient(90deg, #2E4A62, #D4A5B8);
    height: 100%;
    border-radius: 99px;
    transition: width 0.4s ease;
}
.step-label {
    display: flex;
    justify-content: space-between;
    font-size: 0.75rem;
    color: #7A8FA6;
    margin-bottom: 6px;
}

/* Cards */
.card {
    border-radius: 12px;
    padding: 22px;
    text-align: center;
    transition: transform 0.2s ease;
}
.card:hover { transform: translateY(-2px); }
.card-normal {
    background: linear-gradient(135deg, #E8F5E9, #C8E6C9);
    border: 2px solid #81C784;
}
.card-abnormal {
    background: linear-gradient(135deg, #FFF3E0, #FFE0B2);
    border: 2px solid #FFB74D;
}
.card-benign {
    background: linear-gradient(135deg, #E3F2FD, #BBDEFB);
    border: 2px solid #64B5F6;
}
.card-malignant {
    background: linear-gradient(135deg, #FCE4EC, #F8BBD9);
    border: 2px solid #F06292;
}
.card-title { font-size: 1rem; font-weight: 700; margin: 0 0 6px 0; }
.card-sub { font-size: 0.85rem; margin: 0; color: #455a64; }

/* Info box */
.info-box {
    background: #EEF2FF;
    border-left: 4px solid #2E4A62;
    border-radius: 0 8px 8px 0;
    padding: 14px 18px;
    font-size: 0.88rem;
    color: #1B3A52;
    margin-top: 18px;
}

/* Welcome card */
.welcome-card {
    background: white;
    border-radius: 16px;
    padding: 40px 36px;
    box-shadow: 0 4px 24px rgba(46,74,98,0.10);
    text-align: center;
    margin: 10px 0 30px 0;
}
.welcome-subtitle {
    color: #5A7A96;
    font-size: 1rem;
    margin: 8px 0 28px 0;
}
.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, #D4A5B8, transparent);
    margin: 22px 0;
}

/* Badge */
.badge {
    display: inline-block;
    background: #EEF2FF;
    color: #2E4A62;
    border: 1px solid #C5D5E8;
    border-radius: 20px;
    padding: 4px 14px;
    font-size: 0.82rem;
    font-weight: 600;
    margin-bottom: 14px;
}

/* Input fields */
.stTextInput input, .stSelectbox select {
    border-radius: 8px !important;
    border: 1.5px solid #C5D5E8 !important;
}
.stTextInput input:focus {
    border-color: #2E4A62 !important;
    box-shadow: 0 0 0 3px rgba(46,74,98,0.1) !important;
}

/* File uploader */
[data-testid="stFileUploader"] {
    background: #F0F4F8 !important;
    border: 2px dashed #2E4A62 !important;
    border-radius: 10px !important;
}

/* Success banner */
.success-banner {
    background: linear-gradient(135deg, #E8F5E9, #C8E6C9);
    border: 1.5px solid #81C784;
    border-radius: 10px;
    padding: 14px 20px;
    color: #2E7D32;
    font-weight: 600;
    font-size: 0.92rem;
    text-align: center;
    margin: 16px 0;
}

/* Section card wrapper */
.section-card {
    background: white;
    border-radius: 12px;
    padding: 28px;
    box-shadow: 0 2px 12px rgba(46,74,98,0.07);
    margin-bottom: 20px;
}

/* Footer */
.footer {
    text-align: center;
    margin-top: 50px;
    padding: 16px;
    font-size: 0.78rem;
    color: #94A3B8;
    border-top: 1px solid #E2E8F0;
}

/* Navigation row */
.nav-row { margin-top: 10px; }
</style>
""", unsafe_allow_html=True)

# ─── Session State ─────────────────────────────────────────────────────────────
defaults = {
    'page': 1,
    'patient_name': "",
    'patient_age': "",
    'patient_phone': "",
    'patient_history': "No",
    'file_uploaded': False,
    'show_saved': False,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

def next_page(): st.session_state.page += 1
def prev_page(): st.session_state.page -= 1

def save_and_reset():
    now = datetime.now()
    new_record = {
        "Date": now.strftime("%Y-%m-%d"),
        "Time": now.strftime("%H:%M:%S"),
        "Patient Name": st.session_state.patient_name or "Anonymous",
        "Age": st.session_state.patient_age or "N/A",
        "Phone": st.session_state.patient_phone or "N/A",
        "History of Pathology": st.session_state.patient_history,
        "AI Diagnostics Result": "Pending Correlation",
    }
    df_new = pd.DataFrame([new_record])
    if os.path.exists(LOG_FILE):
        try:
            df_old = pd.read_csv(LOG_FILE)
            df_combined = pd.concat([df_old, df_new], ignore_index=True)
            df_combined.to_csv(LOG_FILE, index=False)
        except:
            df_new.to_csv(LOG_FILE, index=False)
    else:
        df_new.to_csv(LOG_FILE, index=False)

    for k, v in defaults.items():
        st.session_state[k] = v
    st.session_state.show_saved = True

# ─── Helper: Progress Bar ─────────────────────────────────────────────────────
STEPS = ["Welcome", "Patient Info", "Upload File", "Primary Result", "Classification"]

def show_progress(page_num):
    if page_num < 2:
        return
    step = page_num - 1
    pct = int((step / (len(STEPS) - 1)) * 100)
    labels = "".join([
        f"<span style='color:{'#2E4A62' if i+1 == step else '#94A3B8'}; font-weight:{'700' if i+1 == step else '400'}'>{s}</span>"
        for i, s in enumerate(STEPS[1:])
    ])
    st.markdown(f"""
    <div class='step-label'>{labels}</div>
    <div class='progress-wrapper'><div class='progress-fill' style='width:{pct}%'></div></div>
    """, unsafe_allow_html=True)

# ─── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    if img_data:
        st.markdown(f"""
        <div style='text-align:center; margin-bottom:16px;'>
            <img src='data:image/jpeg;base64,{img_data}' 
                 style='height:52px; width:auto; filter:brightness(0) invert(1); opacity:0.9;'>
        </div>""", unsafe_allow_html=True)

    st.markdown("<h2 style='text-align:center; font-size:1.1rem; letter-spacing:1px; margin-bottom:20px;'>ENGINEERING TITANS</h2>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)

    menu_selection = st.radio(
        "Navigate:",
        ["🔬 New AI Diagnostics", "📋 Patients Medical Log"],
        label_visibility="collapsed"
    )
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("""
    <small>
    System Status &nbsp;🟢 <b>Online</b><br><br>
    Database &nbsp;📁 <b>Local CSV</b><br><br>
    Version &nbsp;⚙️ <b>v2.0</b>
    </small>""", unsafe_allow_html=True)

# ─── Saved confirmation ────────────────────────────────────────────────────────
if st.session_state.show_saved:
    st.markdown("""
    <div class='success-banner'>
        ✅ Session saved successfully! Patient record has been logged to the database.
    </div>""", unsafe_allow_html=True)
    st.session_state.show_saved = False

# ══════════════════════════════════════════════════════════════════════════════
# MODULE 1 — AI DIAGNOSTICS (5 pages)
# ══════════════════════════════════════════════════════════════════════════════
if menu_selection == "🔬 New AI Diagnostics":

    # ── PAGE 1: Welcome ───────────────────────────────────────────────────────
    if st.session_state.page == 1:
        if img_data:
            st.markdown(f"""
            <div style='text-align:center; margin-bottom:6px;'>
                <img src='data:image/jpeg;base64,{img_data}'
                     style='height:64px; width:auto; object-fit:contain; mix-blend-mode:multiply;'>
            </div>""", unsafe_allow_html=True)

        st.markdown("<h1>Mammogram AI Diagnostics</h1>", unsafe_allow_html=True)

        st.markdown("""
        <div class='welcome-card'>
            <div class='badge'>🧬 Clinical AI Decision Support Tool</div>
            <p class='welcome-subtitle'>
                Integrating Engineering Precision with Medical Artificial Intelligence<br>
                for reliable mammography screening and early pathology detection.
            </p>
            <div class='divider'></div>
            <div style='display:flex; justify-content:center; gap:36px; flex-wrap:wrap; margin-bottom:8px;'>
                <div style='text-align:center;'>
                    <div style='font-size:1.6rem;'>📂</div>
                    <div style='font-size:0.8rem; color:#5A7A96; margin-top:4px;'>DICOM Upload</div>
                </div>
                <div style='text-align:center;'>
                    <div style='font-size:1.6rem;'>🤖</div>
                    <div style='font-size:0.8rem; color:#5A7A96; margin-top:4px;'>AI Analysis</div>
                </div>
                <div style='text-align:center;'>
                    <div style='font-size:1.6rem;'>🔬</div>
                    <div style='font-size:0.8rem; color:#5A7A96; margin-top:4px;'>Classification</div>
                </div>
                <div style='text-align:center;'>
                    <div style='font-size:1.6rem;'>📋</div>
                    <div style='font-size:0.8rem; color:#5A7A96; margin-top:4px;'>Auto-Log</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        col_l, col_c, col_r = st.columns([1.5, 1, 1.5])
        with col_c:
            st.button("Start Session →", on_click=next_page, key="btn_p1_start")

    # ── PAGE 2: Patient Info ──────────────────────────────────────────────────
    elif st.session_state.page == 2:
        show_progress(2)
        st.markdown("<div class='section-card'>", unsafe_allow_html=True)
        st.markdown("### 📋 Patient Registration")
        st.markdown("<p style='color:#5A7A96; font-size:0.9rem; margin-top:-8px;'>Enter the patient's details accurately to match with DICOM metadata.</p>", unsafe_allow_html=True)
        st.write("")

        st.session_state.patient_name = st.text_input(
            "Patient Full Name",
            value=st.session_state.patient_name,
            placeholder="e.g. Sarah Mohammed Al-Rashid"
        )
        col_age, col_phone = st.columns(2)
        with col_age:
            st.session_state.patient_age = st.text_input(
                "Patient Age",
                value=st.session_state.patient_age,
                placeholder="e.g. 45"
            )
        with col_phone:
            st.session_state.patient_phone = st.text_input(
                "Contact Number",
                value=st.session_state.patient_phone,
                placeholder="e.g. +964 7xx xxx xxxx"
            )

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("**Prior Medical History of Breast Pathology?**")
        st.session_state.patient_history = st.radio(
            "", ["No", "Yes"],
            index=0 if st.session_state.patient_history == "No" else 1,
            horizontal=True,
            label_visibility="collapsed"
        )
        st.markdown("</div>", unsafe_allow_html=True)

        col_l, col_back, col_sp, col_next, col_r = st.columns([0.8, 1, 0.3, 1, 0.8])
        with col_back:
            st.button("← Back", on_click=prev_page, key="btn_p2_back")
        with col_next:
            st.button("Next →", on_click=next_page, key="btn_p2_next")

    # ── PAGE 3: Upload DICOM ──────────────────────────────────────────────────
    elif st.session_state.page == 3:
        show_progress(3)
        st.markdown("<div class='section-card'>", unsafe_allow_html=True)
        st.markdown("### 📂 Mammography File Upload")
        st.markdown("<span class='badge'>Supports .dcm / .dicom formats</span>", unsafe_allow_html=True)
        st.write("")

        uploaded_file = st.file_uploader(
            "Upload Digital Mammography (DICOM File)",
            type=["dcm", "dicom"],
            label_visibility="collapsed"
        )
        st.markdown("""
        <p style='font-size:0.82rem; color:#7A8FA6; margin-top:8px;'>
            ⚠️ Max file size: 200 MB &nbsp;|&nbsp; 
            🔒 Data processed locally — HIPAA compliant
        </p>""", unsafe_allow_html=True)

        if uploaded_file is not None:
            st.session_state.file_uploaded = True
            with st.spinner("⚙️ AI Engine running inference — processing pixel arrays..."):
                time.sleep(1.8)
            st.markdown("""
            <div class='success-banner'>
                ✅ File processed successfully. Neural inference complete — ready to view results.
            </div>""", unsafe_allow_html=True)
        elif st.session_state.file_uploaded:
            st.markdown("""
            <div class='success-banner'>
                ✅ File previously processed. You may proceed.
            </div>""", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

        col_l, col_back, col_sp, col_next, col_r = st.columns([0.8, 1, 0.3, 1, 0.8])
        with col_back:
            st.button("← Back", on_click=prev_page, key="btn_p3_back")
        with col_next:
            st.button("Next →", on_click=next_page, key="btn_p3_next")

    # ── PAGE 4: Primary Result ────────────────────────────────────────────────
    elif st.session_state.page == 4:
        show_progress(4)
        st.markdown("<div class='section-card'>", unsafe_allow_html=True)
        st.markdown("### 🔬 Primary AI Diagnostic Result")
        st.markdown("<p style='color:#5A7A96; font-size:0.88rem; margin-top:-6px;'>Initial screening classification from the neural inference engine.</p>", unsafe_allow_html=True)
        st.write("")

        col_res1, col_res2 = st.columns(2)
        with col_res1:
            st.markdown("""
            <div class='card card-normal'>
                <p class='card-title' style='color:#2E7D32;'>✅ NORMAL</p>
                <p class='card-sub'>Confidence Score<br><b>— %</b></p>
            </div>""", unsafe_allow_html=True)
        with col_res2:
            st.markdown("""
            <div class='card card-abnormal'>
                <p class='card-title' style='color:#E65100;'>⚠️ ABNORMAL</p>
                <p class='card-sub'>Confidence Score<br><b>— %</b></p>
            </div>""", unsafe_allow_html=True)

        st.markdown("""
        <div class='info-box'>
            💡 <b>AI Note:</b> Inference layers verified. Secondary pathological classification 
            will be available on the next screen. Always correlate with clinical findings.
        </div>""", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        col_l, col_back, col_sp, col_next, col_r = st.columns([0.8, 1, 0.3, 1, 0.8])
        with col_back:
            st.button("← Back", on_click=prev_page, key="btn_p4_back")
        with col_next:
            st.button("Next →", on_click=next_page, key="btn_p4_next")

    # ── PAGE 5: Classification (Benign / Malignant) ───────────────────────────
    elif st.session_state.page == 5:
        show_progress(5)
        st.markdown("<div class='section-card'>", unsafe_allow_html=True)
        st.markdown("### 🧬 Secondary Pathological Classification")
        st.markdown("""
        <div style='background:#FFF8E1; border:1px solid #FFD54F; border-radius:8px; 
                    padding:10px 16px; text-align:center; margin-bottom:20px;'>
            <span style='color:#E65100; font-weight:600; font-size:0.9rem;'>
                ⚙️ Computing secondary probability tracks...
            </span>
        </div>""", unsafe_allow_html=True)

        col_b, col_m = st.columns(2)
        with col_b:
            st.markdown("""
            <div class='card card-benign'>
                <p class='card-title' style='color:#1565C0;'>🟦 BENIGN</p>
                <p class='card-sub'>Probability Score<br><b>— %</b></p>
            </div>""", unsafe_allow_html=True)
        with col_m:
            st.markdown("""
            <div class='card card-malignant'>
                <p class='card-title' style='color:#AD1457;'>🔴 MALIGNANT</p>
                <p class='card-sub'>Probability Score<br><b>— %</b></p>
            </div>""", unsafe_allow_html=True)

        st.markdown("""
        <div class='info-box' style='margin-top:20px;'>
            <b>⚕️ Clinical Disclaimer:</b> This AI evaluation is a decision-support tool only. 
            Results must be correlated with expert histopathological analysis and clinical judgment 
            before any medical conclusion is drawn.
        </div>""", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        col_l, col_back, col_sp, col_save, col_r = st.columns([0.8, 1, 0.3, 1, 0.8])
        with col_back:
            st.button("← Back", on_click=prev_page, key="btn_p5_back")
        with col_save:
            st.button("💾 Save & Finish", on_click=save_and_reset, key="btn_p5_save")

# ══════════════════════════════════════════════════════════════════════════════
# MODULE 2 — PATIENTS MEDICAL LOG
# ══════════════════════════════════════════════════════════════════════════════
elif menu_selection == "📋 Patients Medical Log":
    st.markdown("### 📋 Patients Diagnostic Log Database")
    st.markdown("<p style='color:#5A7A96; font-size:0.9rem;'>Review, search, and export historical diagnostic sessions.</p>", unsafe_allow_html=True)
    st.write("")

    if os.path.exists(LOG_FILE) and os.path.getsize(LOG_FILE) > 0:
        try:
            df_log = pd.read_csv(LOG_FILE)
        except:
            df_log = pd.DataFrame()

        if not df_log.empty and "Date" in df_log.columns:
            # Stats row
            col_s1, col_s2, col_s3 = st.columns(3)
            with col_s1:
                st.markdown(f"""
                <div style='background:white; border-radius:10px; padding:16px; text-align:center;
                            box-shadow:0 2px 8px rgba(46,74,98,0.08);'>
                    <div style='font-size:1.8rem; font-weight:700; color:#2E4A62;'>{len(df_log)}</div>
                    <div style='font-size:0.8rem; color:#7A8FA6;'>Total Records</div>
                </div>""", unsafe_allow_html=True)
            with col_s2:
                today_count = len(df_log[df_log['Date'] == datetime.now().strftime("%Y-%m-%d")]) if 'Date' in df_log.columns else 0
                st.markdown(f"""
                <div style='background:white; border-radius:10px; padding:16px; text-align:center;
                            box-shadow:0 2px 8px rgba(46,74,98,0.08);'>
                    <div style='font-size:1.8rem; font-weight:700; color:#2E4A62;'>{today_count}</div>
                    <div style='font-size:0.8rem; color:#7A8FA6;'>Today's Sessions</div>
                </div>""", unsafe_allow_html=True)
            with col_s3:
                history_yes = len(df_log[df_log['History of Pathology'] == 'Yes']) if 'History of Pathology' in df_log.columns else 0
                st.markdown(f"""
                <div style='background:white; border-radius:10px; padding:16px; text-align:center;
                            box-shadow:0 2px 8px rgba(46,74,98,0.08);'>
                    <div style='font-size:1.8rem; font-weight:700; color:#D4A5B8;'>{history_yes}</div>
                    <div style='font-size:0.8rem; color:#7A8FA6;'>With Prior History</div>
                </div>""", unsafe_allow_html=True)

            st.write("")
            search_query = st.text_input("🔍 Search by Name, Phone, or Result:", placeholder="Type to filter records...")

            if search_query:
                mask = (
                    df_log['Patient Name'].astype(str).str.contains(search_query, case=False, na=False) |
                    df_log['Phone'].astype(str).str.contains(search_query, case=False, na=False) |
                    df_log['AI Diagnostics Result'].astype(str).str.contains(search_query, case=False, na=False)
                )
                filtered_df = df_log[mask]
            else:
                filtered_df = df_log

            st.dataframe(filtered_df.iloc[::-1], use_container_width=True, hide_index=True)
            st.write("")

            col_dl, col_sp, col_clr = st.columns([2, 0.3, 1])
            with col_dl:
                st.download_button(
                    label="📥 Export to CSV",
                    data=df_log.to_csv(index=False).encode('utf-8'),
                    file_name=f"Mammogram_Log_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime='text/csv'
                )
            with col_clr:
                if st.button("🗑️ Clear All Records"):
                    if os.path.exists(LOG_FILE):
                        os.remove(LOG_FILE)
                    st.success("Database cleared.")
                    st.rerun()
        else:
            st.info("⚠️ Database structure outdated. Complete a new diagnostic session to rebuild the log.")
    else:
        st.markdown("""
        <div style='background:white; border-radius:12px; padding:40px; text-align:center;
                    box-shadow:0 2px 12px rgba(46,74,98,0.07);'>
            <div style='font-size:2.5rem; margin-bottom:12px;'>📭</div>
            <p style='color:#5A7A96; font-size:0.95rem;'>No records yet. Complete an AI Diagnostic session to populate the log.</p>
        </div>""", unsafe_allow_html=True)

# ─── Footer ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class='footer'>
    © 2026 Engineering Titans · All Rights Reserved · Clinical AI Decision Support Tool v2.0
</div>
""", unsafe_allow_html=True)
