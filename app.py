import streamlit as st
import google.generativeai as genai
from PIL import Image
import io, os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="AI MedLens — Upload",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ══════════════════════════════════════════════════════════════════
#  HEALTHCARE COLOR PALETTE
#  • Deep Teal   #0B6E7C  → Trust, expertise, calm (primary)
#  • Sky Blue    #4FC3F7  → Clarity, technology (accent)
#  • Soft White  #F4F9FB  → Cleanliness, safety (bg)
#  • Warm Slate  #1C3A45  → Professionalism, text
#  • Heal Green  #2E9E6B  → Health, positive outcomes
#  • Alert Red   #D63F3F  → Warnings, urgent
# ══════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400&family=Playfair+Display:wght@600;700&display=swap');

:root {
    --primary:      #0B6E7C;
    --primary-d:    #084F59;
    --primary-l:    #1A8A9A;
    --accent:       #4FC3F7;
    --accent-d:     #29AAE1;
    --bg:           #F4F9FB;
    --bg-card:      #FFFFFF;
    --text:         #1C3A45;
    --muted:        #5A7D8A;
    --border:       rgba(11,110,124,0.18);
    --border-l:     rgba(11,110,124,0.09);
    --green:        #2E9E6B;
    --green-bg:     rgba(46,158,107,0.08);
    --red:          #D63F3F;
    --red-bg:       rgba(214,63,63,0.07);
    --teal-pale:    #E8F5F7;
    --teal-pale2:   #D0EDF1;
}

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, .stApp {
    background: var(--bg) !important;
    font-family: 'DM Sans', sans-serif !important;
    color: var(--text) !important;
}

/* Subtle background pattern */
.stApp::before {
    content: '';
    position: fixed; inset: 0;
    background:
        radial-gradient(ellipse at 10% 5%,  rgba(79,195,247,0.08) 0%, transparent 45%),
        radial-gradient(ellipse at 90% 95%, rgba(11,110,124,0.06) 0%, transparent 45%);
    pointer-events: none; z-index: 0;
}

#MainMenu, footer, .stDeployButton,
header[data-testid="stHeader"],
[data-testid="stSidebar"],
[data-testid="collapsedControl"] { display: none !important; }

.block-container {
    padding: 0 !important;
    max-width: 100% !important;
    position: relative; z-index: 1;
}

/* ── NAV ─────────────────────────────────────────────────── */
.ml-nav {
    background: linear-gradient(135deg, var(--primary-d) 0%, var(--primary) 60%, var(--primary-l) 100%);
    padding: 1rem 2.5rem;
    display: flex; align-items: center; justify-content: space-between;
    box-shadow: 0 4px 20px rgba(11,110,124,0.28);
    position: sticky; top: 0; z-index: 200;
}
.ml-logo {
    font-family: 'Playfair Display', serif;
    font-size: 1.35rem; font-weight: 700; color: white;
    display: flex; align-items: center; gap: 0.55rem;
}
.ml-logo .icon {
    width: 34px; height: 34px;
    background: rgba(255,255,255,0.18); border-radius: 10px;
    display: flex; align-items: center; justify-content: center; font-size: 1.1rem;
}
.ml-nav-pills { display: flex; gap: 0.35rem; }
.ml-pill {
    font-size: 0.72rem; font-weight: 600;
    padding: 0.35rem 1rem; border-radius: 999px;
    color: rgba(255,255,255,0.6);
    border: 1px solid rgba(255,255,255,0.22); background: transparent;
    font-family: 'DM Sans', sans-serif;
}
.ml-pill.active {
    background: white; color: var(--primary); border-color: white;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

/* ── PAGE CONTAINER ──────────────────────────────────────── */
.ml-page {
    max-width: 600px;
    margin: 0 auto;
    padding: 2.5rem 1.5rem 3rem;
}

/* ── HERO ────────────────────────────────────────────────── */
.ml-hero {
    background: linear-gradient(135deg, var(--primary-d) 0%, var(--primary) 55%, var(--primary-l) 100%);
    border-radius: 22px; padding: 2.25rem 2rem;
    margin-bottom: 2rem; text-align: center;
    position: relative; overflow: hidden;
    box-shadow: 0 16px 40px rgba(11,110,124,0.28);
}
.ml-hero::before {
    content: '💊';
    position: absolute; right: 1.5rem; top: 1.2rem;
    font-size: 4rem; opacity: 0.08;
}
.ml-hero::after {
    content: '';
    position: absolute; left: -40px; bottom: -40px;
    width: 160px; height: 160px; border-radius: 50%;
    background: rgba(79,195,247,0.12);
}
.ml-hero-tag {
    display: inline-block;
    background: rgba(255,255,255,0.16);
    border: 1px solid rgba(255,255,255,0.28);
    border-radius: 999px; padding: 0.22rem 0.9rem;
    font-size: 0.65rem; font-weight: 700;
    letter-spacing: 0.12em; text-transform: uppercase;
    color: rgba(255,255,255,0.92); margin-bottom: 0.7rem;
}
.ml-hero-title {
    font-family: 'Playfair Display', serif;
    font-size: 2rem; font-weight: 700;
    color: white; line-height: 1.15; margin-bottom: 0.5rem;
}
.ml-hero-sub {
    font-size: 0.88rem; color: rgba(255,255,255,0.78); line-height: 1.65;
}

/* ── STEPS ───────────────────────────────────────────────── */
.ml-steps {
    display: flex; align-items: center; justify-content: center;
    margin: 0 0 2rem;
}
.ml-step { display: flex; flex-direction: column; align-items: center; }
.ml-step-circle {
    width: 40px; height: 40px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-weight: 700; font-size: 0.88rem;
    border: 2px solid var(--border); background: white; color: var(--muted);
    font-family: 'DM Sans', sans-serif;
}
.ml-step-circle.active {
    background: linear-gradient(135deg, var(--primary-d), var(--primary-l));
    color: white; border-color: transparent;
    box-shadow: 0 4px 14px rgba(11,110,124,0.38);
}
.ml-step-circle.done { background: var(--green); color: white; border-color: transparent; }
.ml-step-label {
    font-size: 0.65rem; font-weight: 600; color: var(--muted);
    margin-top: 0.4rem; text-transform: uppercase; letter-spacing: 0.06em;
}
.ml-step-label.active { color: var(--primary); }
.ml-step-line { height: 2px; width: 60px; background: var(--border-l); margin-bottom: 1.6rem; }
.ml-step-line.done { background: var(--green); }

/* ── UPLOAD BOX ──────────────────────────────────────────── */
.ml-upload-box {
    background: white;
    border-radius: 22px;
    padding: 0.75rem;
    box-shadow: 0 6px 28px rgba(11,110,124,0.1);
    border: 1px solid var(--border);
    margin-bottom: 1.5rem;
}

[data-testid="stFileUploader"] {
    border: 2px dashed rgba(11,110,124,0.28) !important;
    border-radius: 16px !important;
    background: var(--teal-pale) !important;
    transition: all 0.2s !important;
    min-height: 180px !important;
}
[data-testid="stFileUploader"]:hover {
    border-color: var(--primary) !important;
    background: var(--teal-pale2) !important;
}
[data-testid="stFileUploader"] section {
    padding: 2rem 1rem !important;
    display: flex !important; flex-direction: column !important;
    align-items: center !important; justify-content: center !important;
    text-align: center !important; min-height: 160px !important;
}
[data-testid="stFileUploader"] * {
    font-family: 'DM Sans', sans-serif !important;
    color: var(--muted) !important;
    font-size: 0.85rem !important; text-align: center !important;
}
[data-testid="stFileUploaderDropzoneInstructions"] {
    display: flex !important; flex-direction: column !important;
    align-items: center !important; gap: 0.3rem !important;
}
[data-testid="stFileUploaderDropzoneInstructions"]::before {
    content: '📁';
    font-size: 2.8rem !important; display: block !important;
    margin-bottom: 0.4rem !important;
}
[data-testid="stFileUploader"] button {
    background: linear-gradient(135deg, var(--primary-d), var(--primary-l)) !important;
    color: white !important; border: none !important;
    border-radius: 12px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important; font-size: 0.88rem !important;
    padding: 0.6rem 1.75rem !important; margin-top: 0.75rem !important;
    box-shadow: 0 5px 16px rgba(11,110,124,0.3) !important;
    transition: all 0.2s !important; cursor: pointer !important;
}
[data-testid="stFileUploader"] button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 22px rgba(11,110,124,0.42) !important;
}

/* ── IMAGE PREVIEW ───────────────────────────────────────── */
[data-testid="stImage"] {
    display: flex !important; justify-content: center !important;
    margin: 0.75rem 0 !important;
}
[data-testid="stImage"] img {
    max-width: 240px !important; max-height: 240px !important;
    width: auto !important; height: auto !important;
    object-fit: contain !important;
    border-radius: 14px !important;
    box-shadow: 0 6px 24px rgba(11,110,124,0.15) !important;
    border: 1px solid var(--border) !important;
    display: block !important;
}

/* ── CHIPS ───────────────────────────────────────────────── */
.ml-chip-row {
    display: flex; gap: 0.5rem; flex-wrap: wrap;
    justify-content: center; margin: 0.75rem 0 0.5rem;
}
.ml-chip {
    display: inline-flex; align-items: center; gap: 0.3rem;
    font-size: 0.72rem; font-weight: 500;
    padding: 0.25rem 0.75rem; border-radius: 999px;
}
.ml-chip .dot { width: 5px; height: 5px; border-radius: 50%; background: currentColor; }
.ml-chip.ok   { background: var(--green-bg); color: var(--green); border: 1px solid rgba(46,158,107,0.25); }
.ml-chip.info { background: var(--teal-pale); color: var(--primary); border: 1px solid var(--border); }

/* ── SCAN BUTTON ─────────────────────────────────────────── */
.ml-scan-btn { width: 100%; margin-top: 0.75rem; }
.stButton > button {
    background: linear-gradient(135deg, var(--primary-d), var(--primary-l)) !important;
    color: white !important; border: none !important;
    border-radius: 16px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 700 !important; font-size: 1rem !important;
    padding: 0.85rem 1.5rem !important; width: 100% !important;
    box-shadow: 0 8px 22px rgba(11,110,124,0.3) !important;
    transition: all 0.22s !important; letter-spacing: 0.02em !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 12px 30px rgba(11,110,124,0.44) !important;
}

/* ── ALERTS ──────────────────────────────────────────────── */
.ml-err {
    background: var(--red-bg); border-left: 3px solid var(--red);
    border-radius: 0 12px 12px 0; padding: 0.8rem 1rem;
    font-size: 0.85rem; color: var(--red); margin-top: 0.75rem; line-height: 1.6;
}
.ml-ok {
    background: var(--green-bg); border-left: 3px solid var(--green);
    border-radius: 0 12px 12px 0; padding: 0.8rem 1rem;
    font-size: 0.85rem; color: var(--green); margin-top: 0.75rem; line-height: 1.6;
}

/* ── TIPS SECTION ────────────────────────────────────────── */
.ml-tips {
    background: white; border-radius: 20px;
    border: 1px solid var(--border);
    box-shadow: 0 4px 18px rgba(11,110,124,0.07);
    padding: 1.5rem 1.75rem; margin-top: 1.5rem;
}
.ml-tips-header {
    display: flex; align-items: center; gap: 0.6rem;
    margin-bottom: 1.1rem; padding-bottom: 0.85rem;
    border-bottom: 1px solid var(--border-l);
}
.ml-tips-icon {
    width: 34px; height: 34px; border-radius: 10px;
    background: linear-gradient(135deg, var(--primary-d), var(--primary-l));
    display: flex; align-items: center; justify-content: center;
    font-size: 1rem; flex-shrink: 0;
    box-shadow: 0 3px 10px rgba(11,110,124,0.25);
}
.ml-tips-title {
    font-family: 'Playfair Display', serif;
    font-size: 1rem; font-weight: 600; color: var(--text);
}
.ml-tip-item {
    display: flex; align-items: flex-start; gap: 0.75rem;
    padding: 0.6rem 0; border-bottom: 1px solid var(--border-l);
}
.ml-tip-item:last-child { border-bottom: none; padding-bottom: 0; }
.ml-tip-num {
    width: 24px; height: 24px; border-radius: 50%; flex-shrink: 0;
    background: linear-gradient(135deg, var(--primary-d), var(--primary-l));
    color: white; font-size: 0.72rem; font-weight: 700;
    display: flex; align-items: center; justify-content: center;
    margin-top: 0.1rem;
}
.ml-tip-text { font-size: 0.92rem; color: var(--text); line-height: 1.55; }
.ml-tip-text strong { font-weight: 600; color: var(--primary); }

/* ── EMPTY STATE ─────────────────────────────────────────── */
.ml-empty {
    text-align: center; padding: 2rem 1.5rem;
    border: 2px dashed rgba(11,110,124,0.18);
    border-radius: 20px; background: white;
    box-shadow: 0 4px 16px rgba(11,110,124,0.06);
    margin-bottom: 1.5rem;
}
.ml-empty-icon { font-size: 2.8rem; margin-bottom: 0.6rem; }
.ml-empty-title {
    font-family: 'Playfair Display', serif;
    font-size: 1rem; font-weight: 600; color: var(--text); margin-bottom: 0.3rem;
}
.ml-empty-sub { font-size: 0.82rem; color: var(--muted); line-height: 1.6; }
.ml-fpills { display: flex; gap: 0.4rem; flex-wrap: wrap; justify-content: center; margin-top: 1rem; }
.ml-fpill {
    font-size: 0.72rem; font-weight: 500; color: var(--primary);
    padding: 0.28rem 0.75rem; border-radius: 999px;
    border: 1px solid var(--border); background: var(--teal-pale);
}

/* ── DISCLAIMER ──────────────────────────────────────────── */
.ml-disclaimer {
    background: rgba(11,110,124,0.05); border: 1px solid var(--border);
    border-radius: 14px; padding: 0.9rem 1.1rem;
    font-size: 0.8rem; color: var(--muted); line-height: 1.6;
    margin-top: 1.5rem;
}
.ml-disclaimer strong { color: var(--primary); }

.stSpinner > div { border-top-color: var(--primary) !important; }
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-thumb { background: rgba(11,110,124,0.22); border-radius: 3px; }
</style>
""", unsafe_allow_html=True)

# ── Session init ───────────────────────────────────────────────────────────────
for k, v in [("image_bytes", None), ("analysis_result", None),
             ("chat_history", []), ("analyzed", False), ("api_key", "")]:
    if k not in st.session_state:
        st.session_state[k] = v

# ── Gemini ─────────────────────────────────────────────────────────────────────
ANALYSIS_PROMPT = """
You are an expert medical document analyst specializing in handwritten prescription reading.
Carefully analyze this prescription image and extract ALL visible information.

Respond in this EXACT structured format:

=== PATIENT INFORMATION ===
Patient Name: [name or "Not visible"]
Age/Gender: [info or "Not visible"]
Date: [date or "Not visible"]

=== DOCTOR & CLINIC INFORMATION ===
Doctor Name: [name or "Not visible"]
Qualification: [e.g., MBBS, MD or "Not visible"]
Hospital/Clinic: [name or "Not visible"]
Address: [address or "Not visible"]
Contact: [phone/email or "Not visible"]
Registration No: [reg no or "Not visible"]

=== DIAGNOSIS / COMPLAINTS ===
[List diagnosis, chief complaints, or reason for visit. Write "Not mentioned" if absent.]

=== PRESCRIBED MEDICINES ===
Medicine 1:
  - Name: [full brand/generic name]
  - Dosage: [e.g., 500mg, 10ml, 1 tablet]
  - Frequency: [e.g., Once daily, Twice daily, TID, SOS]
  - Duration: [e.g., 5 days, 2 weeks, Until finished]
  - Instructions: [e.g., After meals, With plenty of water]

[Continue for all medicines]

=== SPECIAL INSTRUCTIONS ===
[Diet, lifestyle, follow-up, lab tests. Write "None" if absent.]

=== ILLEGIBLE / UNCLEAR SECTIONS ===
[Describe unclear parts. Write "None" if all clear.]

=== CONFIDENCE ASSESSMENT ===
Overall Readability: [Excellent / Good / Fair / Poor]
Confidence Level: [High / Medium / Low]
Notes: [Caveats about accuracy]

Be thorough. Mark unclear names as [Unclear - possible: X]. Never guess dosages.
"""

def get_model():
    key = os.getenv("GOOGLE_API_KEY", "").strip()
    if not key or key == "your_gemini_api_key_here":
        key = st.session_state.get("api_key", "").strip()
    if not key or key == "your_gemini_api_key_here":
        return None
    genai.configure(api_key=key)
    return genai.GenerativeModel("gemini-2.5-flash")

def analyze_prescription(image, model):
    return model.generate_content([ANALYSIS_PROMPT, image]).text

# ── NAV ────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="ml-nav">
    <div class="ml-logo"><div class="icon">💊</div> AI MedLens</div>
    <div class="ml-nav-pills">
        <span class="ml-pill active">Upload</span>
        <span class="ml-pill">Results</span>
        <span class="ml-pill">Query AI</span>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="ml-page">', unsafe_allow_html=True)

# Hero
st.markdown("""
<div class="ml-hero">
    <div class="ml-hero-tag">⚕ AI-Powered Medical Analysis</div>
    <div class="ml-hero-title">Prescription Reader</div>
    <div class="ml-hero-sub">Upload your handwritten or printed prescription<br>and let AI extract all details instantly.</div>
</div>
""", unsafe_allow_html=True)

# Steps
done = st.session_state.get("analyzed", False)
st.markdown(f"""
<div class="ml-steps">
    <div class="ml-step">
        <div class="ml-step-circle {'done' if done else 'active'}">{'✓' if done else '1'}</div>
        <div class="ml-step-label {'active' if not done else ''}">Upload</div>
    </div>
    <div class="ml-step-line {'done' if done else ''}"></div>
    <div class="ml-step">
        <div class="ml-step-circle {'active' if done else ''}">2</div>
        <div class="ml-step-label {'active' if done else ''}">Results</div>
    </div>
    <div class="ml-step-line"></div>
    <div class="ml-step">
        <div class="ml-step-circle">3</div>
        <div class="ml-step-label">Query AI</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Upload box
st.markdown('<div class="ml-upload-box">', unsafe_allow_html=True)
uploaded = st.file_uploader(
    "Upload prescription",
    type=["jpg", "jpeg", "png"],
    label_visibility="collapsed"
)
st.markdown('</div>', unsafe_allow_html=True)

# After upload
if uploaded:
    raw = uploaded.read()
    st.session_state["image_bytes"] = raw
    img = Image.open(io.BytesIO(raw))
    st.image(img, width=240)

    kb = len(raw) / 1024
    st.markdown(f"""
    <div class="ml-chip-row">
        <span class="ml-chip ok"><span class="dot"></span> Ready</span>
        <span class="ml-chip info">{img.width}×{img.height}px</span>
        <span class="ml-chip info">{kb:.1f} KB</span>
        <span class="ml-chip info">{uploaded.name.split('.')[-1].upper()}</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="ml-scan-btn">', unsafe_allow_html=True)
    if st.button("🔬  Scan Prescription"):
        model = get_model()
        if not model:
            st.markdown('<div class="ml-err">⚠️ API key not found. Please add GOOGLE_API_KEY to your .env file.</div>', unsafe_allow_html=True)
        else:
            with st.spinner("Scanning your prescription with AI..."):
                try:
                    result = analyze_prescription(img, model)
                    st.session_state["analysis_result"] = result
                    st.session_state["chat_history"] = []
                    st.session_state["analyzed"] = True
                    st.switch_page("pages/2_Results.py")
                except Exception as e:
                    err = str(e)
                    if "429" in err or "quota" in err.lower():
                        st.markdown('<div class="ml-err">⚠️ Quota exceeded. Wait until tomorrow or create a new API key at aistudio.google.com/apikey</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="ml-err">❌ {err[:200]}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

else:
    st.markdown("""
    <div class="ml-empty">
        <div class="ml-empty-icon">🏥</div>
        <div class="ml-empty-title">No Prescription Yet</div>
        <div class="ml-empty-sub">Click the box above to upload a JPG, JPEG, or PNG.<br>Handwritten or printed — both supported.</div>
        <div class="ml-fpills">
            <span class="ml-fpill">💊 Medicines</span>
            <span class="ml-fpill">👤 Patient</span>
            <span class="ml-fpill">👨‍⚕️ Doctor</span>
            <span class="ml-fpill">📋 Instructions</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Tips
st.markdown("""
<div class="ml-tips">
    <div class="ml-tips-header">
        <div class="ml-tips-icon">📸</div>
        <div class="ml-tips-title">Tips for Best Results</div>
    </div>
    <div class="ml-tip-item">
        <div class="ml-tip-num">1</div>
        <div class="ml-tip-text"><strong>Even lighting</strong> — avoid shadows falling on the text</div>
    </div>
    <div class="ml-tip-item">
        <div class="ml-tip-num">2</div>
        <div class="ml-tip-text"><strong>Flat angle</strong> — hold camera parallel to the paper</div>
    </div>
    <div class="ml-tip-item">
        <div class="ml-tip-num">3</div>
        <div class="ml-tip-text"><strong>Full frame</strong> — entire prescription must be in the image</div>
    </div>
    <div class="ml-tip-item">
        <div class="ml-tip-num">4</div>
        <div class="ml-tip-text"><strong>Good resolution</strong> — minimum 400×400px for best accuracy</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="ml-disclaimer">
    ⚕ <strong>Disclaimer:</strong> For informational purposes only.
    Always consult a licensed healthcare professional before taking any medication.
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
