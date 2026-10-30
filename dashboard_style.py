
import streamlit as st


def apply_dashboard_style():
    st.markdown("""
    <style>
    /* Main dashboard background */
    .stApp {
        background: #f5f7fc;
        color: #172033;
    }

    /* Main content */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1400px;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(
            180deg, #111b35 0%, #1d315c 100%
        );
    }

    section[data-testid="stSidebar"] * {
        color: #f1f5f9;
    }

    /* Headings */
    h1, h2, h3 {
        font-family: 'Segoe UI', sans-serif;
        letter-spacing: -0.5px;
    }

    h1 {
        color: #192b50;
        font-weight: 800;
    }

    /* Buttons */
    div.stButton > button[kind="primary"],
    div.stFormSubmitButton > button[kind="primary"] {
        background: linear-gradient(
            90deg, #4f46e5, #7c3aed
        );
        color: white;
        border: none;
        border-radius: 10px;
        font-weight: 600;
    }

    /* Metrics */
    [data-testid="stMetric"] {
        background: white;
        padding: 18px;
        border: 1px solid #e2e8f0;
        border-radius: 14px;
        box-shadow: 0 4px 12px rgba(15, 23, 42, 0.04);
    }

    /* Tabs */
    button[data-baseweb="tab"] {
        font-weight: 600;
        padding: 12px 18px;
    }

    /* Upload widgets */
    [data-testid="stFileUploader"] {
        border-radius: 12px;
    }

    /* Alerts */
    [data-testid="stAlert"] {
        border-radius: 12px;
    }

    /* Horizontal divider */
    hr {
        border-color: #e2e8f0;
    }
    /* Sidebar buttons */
section[data-testid="stSidebar"] .stButton button {
    background-color: #4f46e5;
    color: #ffffff !important;
    border: none;
    border-radius: 10px;
    font-weight: 600;
}

section[data-testid="stSidebar"] .stButton button:hover {
    background-color: #6366f1;
    color: #ffffff !important;
}
    </style>
    """, unsafe_allow_html=True)


def show_dashboard_header():
    st.markdown("""
    <div style="
        padding: 26px 30px;
        background: linear-gradient(
            110deg, #1e3a8a, #4f46e5, #7c3aed
        );
        border-radius: 18px;
        color: white;
        margin-bottom: 24px;
    ">
        <div style="font-size: 13px; opacity: .85;">
            INTELLIGENT RECRUITMENT PLATFORM
        </div>
        <div style="
            font-size: 32px;
            font-weight: 800;
            margin-top: 8px;
        ">
            AI Resume Screening Dashboard
        </div>
        <div style="
            font-size: 15px;
            margin-top: 8px;
            opacity: .9;
        ">
            Analyze resumes, compare candidates,
            and discover relevant skills using AI.
        </div>
    </div>
    """, unsafe_allow_html=True)


def show_dashboard_metrics():
    a, b, c, d = st.columns(4)

    with a:
        st.metric("AI Models", "2", "TF-IDF + BERT")
    with b:
        st.metric("Resume Formats", "2", "PDF / DOCX")
    with c:
        st.metric("Analysis", "NLP", "Skill matching")
    with d:
        st.metric("Backend", "FastAPI", "API integration")

def show_welcome_section():
    st.markdown("### 🚀 Recruitment Intelligence")
    st.info(
        "Upload resumes, compare candidates with job descriptions, "
        "identify matching skills, and review AI-generated rankings."
    )
def show_welcome_section():
    st.markdown("### 🚀 Recruitment Intelligence")
    st.info(
        "Upload resumes, compare candidates with job descriptions, "
        "identify matching skills, and review AI-generated rankings."
    )