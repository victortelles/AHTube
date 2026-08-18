import os

# Project Information
APP_NAME = "AHTube"
APP_SUBTITLE = "Extractor profesional de Audio (MP3) y Video (MP4) desde YouTube"
OUTPUT_DIR = "downloads"

# Asset Paths
LOGO_ALPHA_PATH = os.path.join("src", "assets", "AHTyler_Logo_der_Alpha.png")
STEP1_IMG_PATH = os.path.join("src", "assets", "step_paste_link.jpg")
STEP2_IMG_PATH = os.path.join("src", "assets", "step_select_format.jpg")
STEP3_IMG_PATH = os.path.join("src", "assets", "step_download.jpg")

# Custom CSS for Premium Blue Theme
CUSTOM_CSS = """
    <style>
    /* Global Background & Typography */
    .stApp {
        background-color: #0F172A;
        color: #F8FAFC;
        font-family: 'Inter', system-ui, -apple-system, sans-serif;
    }
    
    /* Header Card */
    .main-title {
        color: #60A5FA;
        font-size: 2.2rem;
        font-weight: 800;
        letter-spacing: -0.5px;
        margin-bottom: 4px;
    }
    .sub-title {
        color: #94A3B8;
        font-size: 0.95rem;
        font-weight: 400;
    }

    /* Inputs */
    .stTextInput > div > div > input {
        background-color: #1E293B !important;
        color: #F8FAFC !important;
        border: 1px solid #334155 !important;
        border-radius: 10px !important;
        padding: 12px 16px !important;
        font-size: 1rem !important;
        transition: border-color 0.2s ease !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: #3B82F6 !important;
        box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2) !important;
    }

    /* Primary Action Buttons */
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%) !important;
        color: #FFFFFF !important;
        font-weight: 600 !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 10px 20px !important;
        font-size: 1rem !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.25) !important;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #3B82F6 0%, #2563EB 100%) !important;
        transform: translateY(-1px);
        box-shadow: 0 6px 16px rgba(37, 99, 235, 0.35) !important;
    }

    /* Cards & Container Styles */
    .preview-card {
        background: #1E293B;
        border: 1px solid #334155;
        border-radius: 14px;
        padding: 20px;
        margin-top: 15px;
        margin-bottom: 20px;
    }

    .badge-audio {
        background-color: rgba(37, 99, 235, 0.15);
        color: #60A5FA;
        border: 1px solid rgba(59, 130, 246, 0.3);
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        display: inline-block;
        margin-bottom: 6px;
    }

    .badge-video {
        background-color: rgba(168, 85, 247, 0.15);
        color: #C084FC;
        border: 1px solid rgba(168, 85, 247, 0.3);
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        display: inline-block;
        margin-bottom: 6px;
    }

    .file-title {
        color: #F8FAFC;
        font-size: 0.95rem;
        font-weight: 600;
        margin: 0;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }

    .file-meta {
        color: #64748B;
        font-size: 0.8rem;
        margin-top: 2px;
    }

    .file-counter {
        color: #94A3B8;
        font-size: 0.85rem;
        margin-top: -8px;
        margin-bottom: 8px;
    }
    </style>
"""
