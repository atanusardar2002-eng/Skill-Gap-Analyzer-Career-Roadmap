"""
Custom CSS & Styling for GDG AI Skill Gap Analyzer
Modern, high-contrast, polished interface with Google Developer Groups colors.
"""

def get_custom_css() -> str:
    return """
    <style>
    /* Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    /* GDG Header Container */
    .gdg-header {
        background: linear-gradient(135deg, rgba(66, 133, 244, 0.12) 0%, rgba(52, 168, 83, 0.08) 50%, rgba(234, 67, 53, 0.08) 100%);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 2rem 2.5rem;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.25);
        backdrop-filter: blur(12px);
    }

    .gdg-badge-group {
        display: flex;
        gap: 8px;
        margin-bottom: 12px;
        align-items: center;
    }

    .gdg-dot {
        width: 10px;
        height: 10px;
        border-radius: 50%;
        display: inline-block;
    }
    .gdg-blue { background-color: #4285F4; box-shadow: 0 0 10px #4285F4; }
    .gdg-red { background-color: #EA4335; box-shadow: 0 0 10px #EA4335; }
    .gdg-yellow { background-color: #FBBC05; box-shadow: 0 0 10px #FBBC05; }
    .gdg-green { background-color: #34A853; box-shadow: 0 0 10px #34A853; }

    .gdg-title {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(90deg, #4285F4, #a855f7, #34A853);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        letter-spacing: -0.5px;
    }

    .gdg-subtitle {
        color: #94a3b8;
        font-size: 1.05rem;
        margin-top: 8px;
        margin-bottom: 0;
    }

    /* Score Card */
    .score-card {
        background: rgba(26, 32, 48, 0.7);
        border: 1px solid rgba(66, 133, 244, 0.3);
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        margin-bottom: 1.5rem;
        box-shadow: 0 8px 24px rgba(0,0,0,0.3);
    }

    .score-number {
        font-size: 3.5rem;
        font-weight: 800;
        letter-spacing: -1px;
    }

    .score-high {
        color: #34A853;
        text-shadow: 0 0 20px rgba(52, 168, 83, 0.4);
    }
    .score-medium {
        color: #FBBC05;
        text-shadow: 0 0 20px rgba(251, 188, 5, 0.4);
    }
    .score-low {
        color: #EA4335;
        text-shadow: 0 0 20px rgba(234, 67, 53, 0.4);
    }

    /* Metric Cards */
    .metric-box {
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 14px;
        padding: 1rem 1.25rem;
        text-align: left;
    }

    .metric-box h4 {
        margin: 0;
        font-size: 0.85rem;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .metric-box p {
        margin: 6px 0 0 0;
        font-size: 1.4rem;
        font-weight: 700;
        color: #f1f5f9;
    }

    /* Skill Tags */
    .skill-tag {
        display: inline-block;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        margin: 4px 6px 6px 0;
        box-shadow: 0 2px 6px rgba(0,0,0,0.2);
    }

    .skill-matched {
        background: rgba(52, 168, 83, 0.15);
        color: #4ade80;
        border: 1px solid rgba(52, 168, 83, 0.4);
    }

    .skill-missing {
        background: rgba(234, 67, 53, 0.15);
        color: #f87171;
        border: 1px solid rgba(234, 67, 53, 0.4);
    }

    .skill-improving {
        background: rgba(251, 188, 5, 0.15);
        color: #facc15;
        border: 1px solid rgba(251, 188, 5, 0.4);
    }

    /* Roadmap Phase Cards */
    .roadmap-phase-card {
        background: linear-gradient(180deg, rgba(30, 41, 59, 0.85) 0%, rgba(15, 23, 42, 0.85) 100%);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-left: 5px solid #4285F4;
        border-radius: 14px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }

    .roadmap-phase-card:hover {
        transform: translateY(-2px);
        border-left-color: #34A853;
    }

    .phase-badge {
        background: #4285F4;
        color: white;
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        display: inline-block;
        margin-bottom: 8px;
    }

    .phase-title {
        font-size: 1.25rem;
        font-weight: 700;
        color: #f8fafc;
        margin: 0 0 10px 0;
    }

    .phase-duration {
        color: #94a3b8;
        font-size: 0.9rem;
        margin-bottom: 12px;
    }

    .resource-chip {
        background: rgba(66, 133, 244, 0.15);
        border: 1px solid rgba(66, 133, 244, 0.3);
        border-radius: 8px;
        padding: 6px 12px;
        display: inline-block;
        margin: 4px;
        font-size: 0.82rem;
        color: #93c5fd;
        text-decoration: none;
    }
    
    /* Career Coach Chat Styling */
    .stChatMessage {
        border-radius: 12px !important;
        margin-bottom: 8px !important;
    }

    /* Streamlit Custom adjustments */
    div[data-testid="stSidebar"] {
        border-right: 1px solid rgba(255, 255, 255, 0.08);
    }
    </style>
    """
