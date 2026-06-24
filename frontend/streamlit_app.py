# frontend/streamlit_app.py
import streamlit as st
import requests
from PIL import Image

API_URL = "https://your-api.onrender.com/predict/"

st.set_page_config(
    page_title="GlowAI | Skin Analyzer",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─────────────────────────────────────────────────────────────
#  PREMIUM SOFT-LIGHT DESIGN SYSTEM
# ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:wght@400;600&display=swap');

    /* ── Global Reset ── */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* ── Soft warm background ── */
    .stApp {
        background: linear-gradient(135deg, #fdf6f0 0%, #fef0f5 40%, #f0f4ff 100%);
        min-height: 100vh;
    }

    /* ── Hide Streamlit chrome ── */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    header { visibility: hidden; }
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
        max-width: 1200px !important;
    }

    /* ── Hero header ── */
    .hero-header {
        text-align: center;
        padding: 2.5rem 2rem 1.5rem;
        margin-bottom: 0.5rem;
    }
    .hero-logo {
        font-family: 'Playfair Display', serif;
        font-size: 3.2rem;
        font-weight: 600;
        background: linear-gradient(135deg, #c9748f 0%, #a855b5 50%, #6366f1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        line-height: 1.1;
        letter-spacing: -0.5px;
    }
    .hero-tagline {
        font-size: 1rem;
        color: #9c8fa0;
        margin-top: 0.4rem;
        font-weight: 400;
        letter-spacing: 0.5px;
    }
    .hero-divider {
        width: 60px;
        height: 3px;
        background: linear-gradient(90deg, #f0abbc, #c084fc, #818cf8);
        border-radius: 2px;
        margin: 1rem auto 0;
    }

    /* ── Glass panel cards ── */
    .glass-panel {
        background: rgba(255, 255, 255, 0.72);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.9);
        border-radius: 20px;
        padding: 2rem;
        box-shadow:
            0 4px 24px rgba(200, 150, 180, 0.10),
            0 1px 4px rgba(180, 130, 200, 0.06),
            inset 0 1px 0 rgba(255,255,255,0.8);
        margin-bottom: 1.2rem;
    }

    /* ── Section headings ── */
    .section-heading {
        font-family: 'Playfair Display', serif;
        font-size: 1.25rem;
        font-weight: 600;
        color: #4a3f5c;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    /* ── Upload zone styling ── */
    [data-testid="stFileUploader"] {
        border: 2px dashed rgba(196, 116, 160, 0.35) !important;
        border-radius: 16px !important;
        background: rgba(255, 245, 250, 0.6) !important;
        padding: 1.2rem !important;
        transition: all 0.3s ease !important;
    }
    [data-testid="stFileUploader"]:hover {
        border-color: rgba(196, 116, 160, 0.65) !important;
        background: rgba(255, 240, 248, 0.8) !important;
    }

    /* ── Preview image ── */
    [data-testid="stImage"] img {
        border-radius: 14px !important;
        box-shadow: 0 8px 32px rgba(180, 120, 160, 0.20) !important;
    }

    /* ── Analyse button ── */
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #d97ca8 0%, #a855b5 50%, #818cf8 100%);
        color: white !important;
        border: none !important;
        padding: 0.85rem 1.5rem !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        border-radius: 14px !important;
        letter-spacing: 0.3px;
        transition: all 0.35s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
        box-shadow: 0 4px 18px rgba(168, 85, 181, 0.30) !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) scale(1.01) !important;
        box-shadow: 0 8px 28px rgba(168, 85, 181, 0.42) !important;
        opacity: 0.96 !important;
    }
    .stButton > button:active {
        transform: translateY(0px) scale(0.99) !important;
    }

    /* ── Result metric cards ── */
    .metric-card {
        border-radius: 16px;
        padding: 1.2rem 1.4rem;
        margin-bottom: 0.8rem;
        position: relative;
        overflow: hidden;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .metric-card:hover {
        transform: translateY(-2px);
    }
    .metric-card-skin {
        background: linear-gradient(135deg, rgba(219, 182, 255, 0.22) 0%, rgba(196, 181, 253, 0.18) 100%);
        border: 1px solid rgba(196, 181, 253, 0.45);
        box-shadow: 0 4px 20px rgba(167, 139, 250, 0.12);
    }
    .metric-card-concern {
        background: linear-gradient(135deg, rgba(253, 186, 211, 0.22) 0%, rgba(249, 168, 212, 0.18) 100%);
        border: 1px solid rgba(249, 168, 212, 0.45);
        box-shadow: 0 4px 20px rgba(236, 72, 153, 0.10);
    }
    .metric-label {
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 1px;
        text-transform: uppercase;
        color: #9580a8;
        margin-bottom: 0.35rem;
    }
    .metric-value {
        font-family: 'Playfair Display', serif;
        font-size: 1.6rem;
        font-weight: 600;
        color: #3d2f52;
        line-height: 1.1;
    }
    .metric-value-skin  { color: #6d28d9; }
    .metric-value-concern { color: #be185d; }
    .metric-confidence {
        font-size: 0.78rem;
        color: #7a6890;
        margin-top: 0.3rem;
        display: flex;
        align-items: center;
        gap: 0.3rem;
    }
    .conf-dot {
        width: 7px; height: 7px; border-radius: 50%;
        display: inline-block;
        background: #a3e635;
        box-shadow: 0 0 6px rgba(163, 230, 53, 0.6);
    }

    /* ── Routine step cards ── */
    .routine-step {
        display: flex;
        align-items: flex-start;
        gap: 1rem;
        padding: 1rem 1.2rem;
        border-radius: 14px;
        margin-bottom: 0.7rem;
        background: rgba(255,255,255,0.60);
        border: 1px solid rgba(220, 200, 240, 0.45);
        box-shadow: 0 2px 12px rgba(180, 140, 200, 0.08);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .routine-step:hover {
        transform: translateX(4px);
        box-shadow: 0 4px 18px rgba(180, 140, 200, 0.16);
        background: rgba(255,255,255,0.80);
    }
    .step-number {
        width: 32px; height: 32px;
        border-radius: 10px;
        display: flex; align-items: center; justify-content: center;
        font-size: 0.8rem; font-weight: 700;
        flex-shrink: 0;
        color: white;
    }
    .step-number-am { background: linear-gradient(135deg, #fb923c, #f59e0b); }
    .step-number-pm { background: linear-gradient(135deg, #818cf8, #a855f7); }
    .step-content { flex: 1; }
    .step-name {
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.8px;
        text-transform: uppercase;
        color: #7a6890;
        margin-bottom: 0.2rem;
    }
    .step-products {
        font-size: 0.95rem;
        font-weight: 500;
        color: #3d2f52;
        line-height: 1.4;
    }

    /* ── Tab styling ── */
    [data-testid="stTabs"] [data-baseweb="tab-list"] {
        background: rgba(245, 240, 255, 0.6) !important;
        border-radius: 14px !important;
        padding: 5px !important;
        gap: 4px !important;
        border: 1px solid rgba(220, 200, 250, 0.4) !important;
    }
    [data-testid="stTabs"] [data-baseweb="tab"] {
        border-radius: 10px !important;
        font-weight: 600 !important;
        font-size: 0.88rem !important;
        color: #9580a8 !important;
        transition: all 0.25s ease !important;
        padding: 0.5rem 1.2rem !important;
    }
    [data-testid="stTabs"] [aria-selected="true"] {
        background: white !important;
        color: #6d28d9 !important;
        box-shadow: 0 2px 10px rgba(109, 40, 217, 0.15) !important;
    }

    /* ── Expander ── */
    [data-testid="stExpander"] {
        border: 1px solid rgba(220, 200, 240, 0.45) !important;
        border-radius: 14px !important;
        background: rgba(255,255,255,0.50) !important;
        box-shadow: 0 2px 12px rgba(180,140,200,0.06) !important;
    }

    /* ── Info / empty state ── */
    .empty-state {
        text-align: center;
        padding: 3.5rem 1.5rem;
        color: #b8a8c8;
    }
    .empty-state-icon {
        font-size: 3rem;
        margin-bottom: 0.8rem;
        opacity: 0.6;
        display: block;
    }
    .empty-state-text {
        font-size: 0.95rem;
        line-height: 1.6;
        color: #7a6a8a;
    }

    /* ── Spinner ── */
    .stSpinner > div {
        border-color: #d97ca8 transparent transparent transparent !important;
    }

    /* ── Metrics inside expander ── */
    .tech-metric {
        background: rgba(245, 240, 255, 0.55);
        border: 1px solid rgba(216, 180, 254, 0.40);
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
    }
    .tech-metric-title {
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.8px;
        text-transform: uppercase;
        color: #9580a8;
        margin-bottom: 0.5rem;
    }
    .tech-metric-val {
        font-family: 'Playfair Display', serif;
        font-size: 1.8rem;
        font-weight: 600;
        color: #6d28d9;
    }
    .tech-metric-sub {
        font-size: 0.75rem;
        color: #7a6890;
        margin-top: 0.25rem;
    }

    /* ── Toast override ── */
    [data-testid="stToast"] {
        background: rgba(255,255,255,0.92) !important;
        border: 1px solid rgba(200,180,230,0.5) !important;
        border-radius: 14px !important;
        box-shadow: 0 8px 24px rgba(160,120,200,0.18) !important;
        color: #4a3f5c !important;
    }

    /* ── Scrollbar ── */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: rgba(200,160,220,0.4); border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
#  HERO HEADER
# ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-header">
    <div class="hero-logo">🌸 GlowAI</div>
    <div class="hero-tagline">AI-Powered Personalised Skin Analysis & Routine Builder</div>
    <div class="hero-divider"></div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
#  MAIN LAYOUT
# ─────────────────────────────────────────────────────────────
left_panel, right_panel = st.columns([1, 1.4], gap="large")

# ── LEFT PANEL ──────────────────────────────────────────────
# ── LEFT PANEL ──────────────────────────────────────────────
with left_panel:
    st.markdown('<div class="section-heading glass-panel">🌸Upload Photo</div>', unsafe_allow_html=True)
    

    uploaded_file = st.file_uploader(
        "Upload a well-lit selfie here — our CNN does the rest",
        type=["jpg", "jpeg", "png"],
        label_visibility="visible"
    )

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="", use_container_width=True)
        st.write("")
        analyze_btn = st.button("✨  Analyse My Skin", use_container_width=True)
    else:
        st.markdown("""
        <div style="text-align:center; padding: 2.5rem 1rem; color: #c0aad0;">
            <span style="font-size:2.5rem; display:block; margin-bottom:0.6rem; opacity:0.55">🌿</span>
            <span style="font-size:0.9rem; line-height:1.6;">Upload a clear, front-facing photo<br>for the best analysis results.</span>
        </div>
        """, unsafe_allow_html=True)

    # Tips card
    st.markdown("""
    <div class="glass-panel" style="padding: 1.3rem 1.6rem;">
        <div class="section-heading" style="font-size:1rem; margin-bottom:0.6rem;">💡 Photo Tips</div>
        <ul style="color:#9580a8; font-size:0.85rem; line-height:1.9; padding-left:1.1rem; margin:0;">
            <li>Use natural daylight — avoid harsh flash</li>
            <li>Face the camera directly, no tilt</li>
            <li>Remove glasses for best accuracy</li>
            <li>Clean, bare skin gives cleaner results</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# ── RIGHT PANEL ─────────────────────────────────────────────
with right_panel:
    st.markdown('<div class="section-heading glass-panel">📊 Your Skin Report</div>', unsafe_allow_html=True)
  
    if uploaded_file is not None and 'analyze_btn' in locals() and analyze_btn:
        with st.spinner("Running deep learning analysis…"):
            try:
                uploaded_file.seek(0)
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                response = requests.post(API_URL, files=files, timeout=30)

                if response.status_code == 200:
                    data = response.json()
                    st.toast("Analysis complete!", icon="🌸")

                    # ── METRIC CARDS ──────────────────────────────────
                    col1, col2 = st.columns(2, gap="medium")
                    with col1:
                        st.markdown(f"""
                        <div class="metric-card metric-card-skin">
                            <div class="metric-label">Skin Type</div>
                            <div class="metric-value metric-value-skin">{data['skin_type']}</div>
                        </div>
                        """, unsafe_allow_html=True)
                    with col2:
                        st.markdown(f"""
                        <div class="metric-card metric-card-concern">
                            <div class="metric-label">Primary Concern</div>
                            <div class="metric-value metric-value-concern" style="font-size:1.3rem;">{data['concern']}</div>
                        </div>
                        """, unsafe_allow_html=True)

                    st.write("")
                    st.markdown('<div class="section-heading" style="font-size:1rem;">🌿 Your Personalised Routine</div>', unsafe_allow_html=True)

                    # ── ROUTINE TABS ──────────────────────────────────
                    tab_am, tab_pm = st.tabs(["☀️  Morning Routine", "🌙  Night Routine"])

                    with tab_am:
                        st.write("")
                        for idx, step in enumerate(data["routine"]["morning"], 1):
                            products_str = ", ".join(step["products"])
                            st.markdown(f"""
                            <div class="routine-step">
                                <div class="step-number step-number-am">{idx:02d}</div>
                                <div class="step-content">
                                    <div class="step-name">{step['step']}</div>
                                    <div class="step-products">{products_str}</div>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)

                    with tab_pm:
                        st.write("")
                        for idx, step in enumerate(data["routine"]["night"], 1):
                            products_str = ", ".join(step["products"])
                            st.markdown(f"""
                            <div class="routine-step">
                                <div class="step-number step-number-pm">{idx:02d}</div>
                                <div class="step-content">
                                    <div class="step-name">{step['step']}</div>
                                    <div class="step-products">{products_str}</div>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)

                else:
                    st.error(f"⚠️ Backend error (HTTP {response.status_code}). Make sure the FastAPI server is running.")

            except Exception as e:
                st.error(f"🔌 Could not reach the backend: {e}")

    else:
        st.markdown("""
        <div class="empty-state">
            <span class="empty-state-icon">✨</span>
            <div class="empty-state-text">
                Upload a photo and tap <strong style="color:#c47ab0;">Analyse My Skin</strong><br>
                to receive your AI-curated skincare routine.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)