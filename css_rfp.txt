QA_STYLES = """
<style>
/* ====== THEME: Professional Blue + Accent Green ======
    Blues:   #1E3A8A (deep), #0473EA (brand), #2563EB (accent)
    Greens:  #047857 (emerald), #065F46 (hover)
    Grays:   #F9FAFB (bg), #F3F4F6, #E5E7EB, #1F2937, #111827
======================================================= */

.stApp {
    /* Deeper blue gradient for main background */
    background: white;
    padding: 20px;
    min-height: 100vh;
}

/* Hide Streamlit elements */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Header styling for columns layout */
.header-title {
    font-size: 2rem;
    font-weight: 700;
    color: #111827;
    margin-bottom: 0.5rem;
    margin-top: -0.5rem;
}
.header-subtitle {
    color: #6B7280;
    font-size: 1.1rem;
    margin-bottom: 0.5rem;
}



/* Download button that appears after export */
.stDownloadButton > button {
    background: #0473EA !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.5rem 1rem !important;
    font-weight: 500 !important;
}

.stDownloadButton > button:hover {
    background: #1E3A8A !important;
}


/* Main content container - white background */
.main > div.block-container {
    background: #FAFBFF; /* soft light gray */
    border-radius: 12px;
    padding: 2rem !important;
    max-width: 100%;
    box-shadow: 0 1px 3px rgba(0,0,0,0.08);
}

/* Progress Bar (kept green to match accent) */
.stProgress > div > div > div > div {
    background: linear-gradient(90deg, #10B981, #34D399);
    height: 10px !important;
    border-radius: 10px;
}
.stProgress > div > div > div {
    background-color: rgba(255, 255, 255, 0.3);
    height: 10px !important;
    border-radius: 10px;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    margin-left: 0 !important;
    margin-right: 0 !important;
    background: transparent !important;
    border-radius: 0 !important;
}

.stTabs [data-baseweb="tab"] {
    height: 50px;
    padding: 0 1rem;
    background: transparent !important;
    border: none;
    color: #6B7280;
    font-weight: 500;
    font-size: 1rem;
    
}
.stTabs [data-baseweb="tab"]:hover { color: #111827; }
.stTabs [data-baseweb="tab-highlight"]{
    background: transparent !important; /* or set to #2563EB if you prefer recolor */
    height: 0 !important;
}
.stTabs [aria-selected="true"]{
    background: transparent !important;
    color: #2563EB;
    border-bottom: 3px solid #2563EB;
    font-weight: 600;
}

/* Cards */
.card { border: 1px solid rgba(0,0,0,0.08); border-radius: 14px; padding: 16px; }
.card + .card { margin-top: 18px; }
.card-header { margin-bottom: 8px; }
.muted { color: rgba(0,0,0,0.6); }
.chip { font-size:12px; background:#F3F4F6; border:1px solid #E5E7EB; border-radius:9999px; padding:2px 8px; }

/* Q&A card: container */
.qa-card-sentinel { display: none; }

div[data-testid="stVerticalBlock"]:has(.qa-card-sentinel) {
    background: #FFFFFF; /* #FAFBFF */
    border: none;
    border-radius: 14px;
    padding: 16px;
    box-shadow: 0 1px 2px rgba(0,0,0,0.04);
    margin-bottom: 18px;
    overflow: hidden;
    position: relative;
}

/* Executive Summary container */
.exec-summary-sentinel { display: none; }

div[data-testid="stVerticalBlock"]:has(.exec-summary-sentinel) {
    background: #FFFFFF; /* #FAFBFF */
    border: none;
    border-radius: 14px;
    padding: 16px;
    box-shadow: 0 1px 2px rgba(0,0,0,0.04);
    margin-bottom: 18px;
    overflow: hidden;
    position: relative;
}


/* Question index dot now uses the new blue gradient */
.qdot{
    display:inline-flex;
    height:32px;
    width:32px;
    align-items:center;
    justify-content:center;
    border-radius:50%;
    background:#FFFFFF !important;      /* white background */
    color:#111827 !important;            /* near-black text */
    border:2px solid #2563EB;            /* blue border */
    font-size:14px;
    font-weight:700;
    box-shadow:0 1px 2px rgba(0,0,0,0.06);
}
.question-title {
    font-weight: 600;
    margin-left: 12px;
    color: #1F2937;
    font-size: 1.1rem;
}
.answer-label.in-row{ 
    margin-top: 16px; 
    font-weight: 600;
}
/* === Buttons Questions=== */
/* Chat with AI (Primary) -> Blue - Target buttons in Q&A context */
div[data-testid="stVerticalBlock"]:has(.qa-card-sentinel) div[data-testid="stHorizontalBlock"] > div:nth-child(2) .stButton > button {
    background: #0473EA !important;           /* blue */
    color: #FFFFFF !important;
    border: 0 !important;
    box-shadow: 0 6px 16px rgba(4, 120, 87, 0.30) !important;
    transition: transform .15s ease, box-shadow .15s ease;
}

div[data-testid="stVerticalBlock"]:has(.qa-card-sentinel) div[data-testid="stHorizontalBlock"] > div:nth-child(2) .stButton > button:hover {
    background: #1E3A8A !important;           /* darker blue on hover */
    transform: translateY(-2px);
    box-shadow: 0 10px 24px rgba(4, 120, 87, 0.35) !important;
}

/* Rephrase (Secondary) -> Blue outline - Target buttons in Q&A context */
div[data-testid="stVerticalBlock"]:has(.qa-card-sentinel) div[data-testid="stHorizontalBlock"] > div:last-child .stButton > button {
    background: white !important;
    color: #2563EB !important;
    border: 2px solid #2563EB !important;
    transition: transform .12s ease, background .12s ease, color .12s ease;
}

div[data-testid="stVerticalBlock"]:has(.qa-card-sentinel) div[data-testid="stHorizontalBlock"] > div:last-child .stButton > button:hover {
    background: #2563EB !important;
    color: white !important;
    transform: translateY(-1px);
}

/* === Buttons Executive Summmary=== */
/* Enhance with AI (Primary) -> Blue */
div[data-testid="stVerticalBlock"]:has(.exec-summary-sentinel) div[data-testid="stHorizontalBlock"] > div:nth-child(1) .stButton > button {
    background: #0473EA !important;           /* blue */
    color: #FFFFFF !important;
    border: 0 !important;
    box-shadow: 0 6px 16px rgba(4, 120, 87, 0.30) !important;
    transition: transform .15s ease, box-shadow .15s ease;
}

div[data-testid="stVerticalBlock"]:has(.exec-summary-sentinel) div[data-testid="stHorizontalBlock"] > div:nth-child(1) .stButton > button:hover {
    background: #1E3A8A !important;           /* darker blue on hover */
    transform: translateY(-2px);
    box-shadow: 0 10px 24px rgba(4, 120, 87, 0.35) !important;
}

/* Text Area */
div[data-testid="stTextArea"] textarea,.stTextArea textarea{
    background: #FAFBFF !important;
    color: #111827 !important;                 /* text */
    border: 1px solid #E5E7EB !important;      /* subtle border */
    border-radius: 12px !important;
}


/* === Sidebar (right chat panel) === */
section[data-testid="stSidebar"] { 
    width: 520px !important; 
    background: #FAFBFF !important;         /* soft light gray to complement deep blue bg F9FAFB */
    border-left: 1px solid #E5E7EB !important;
    box-shadow: none !important;
}
section[data-testid="stSidebar"] * { color: #111827; }

/* Full-height layout inside sidebar */
section[data-testid="stSidebar"] > div:first-child {
    height: 100vh !important;
    max-height: 100vh !important;
    display: flex;
    flex-direction: column;
    padding-top: 1rem;
    padding-bottom: 0;
}
section[data-testid="stSidebar"] .block-container {
    flex: 1;
    display: flex;
    flex-direction: column;
    max-height: 100%;
    padding-top: 0;
    padding-bottom: 0;
    overflow: hidden;
}
.chat-header { 
    padding: 12px 14px; 
    border-bottom: 1px solid #E5E7EB; 
    flex-shrink: 0;
}
.chat-title { font-weight:600; color:#1F2937; } /**/
.chat-body { 
    flex: 1; 
    overflow-y: auto; 
    padding: 12px 14px; 
    background: #FFFFFF ; 
    border-radius: 12px;
}
.chat-footer { 
    border-top: 1px solid #E5E7EB; 
    padding: 10px 12px; 
    flex-shrink: 0;
    background:#F9FAFB;
}

/* Keep chat input pinned */
[data-testid="stChatInput"] {
    position: sticky;
    bottom: 0;
    background: white;
    z-index: 1;
}

/* Bubbles */
.bubble { max-width:80%; border-radius: 16px; padding: 8px 10px; font-size: 14px; box-shadow: 0 1px 1px rgba(0,0,0,0.04); margin-bottom: 8px; }
.bubble-user  { margin-left:auto; background:#2563EB; color: white; border-bottom-right-radius:6px; } /* blue accent */
.bubble-ai    { margin-right:auto; background:#F3F4F6; color: #111827; border-bottom-left-radius:6px; }

/* Custom Tab Buttons */
.custom-tab-container {
    display: flex;
    gap: 4px;
    border-bottom: 2px solid #E5E7EB;
    padding-bottom: 0;
    margin-bottom: 1.5rem;
}

/* Style for tab buttons to look like actual tabs */
div[data-testid="column"]:has(.tab-button-active) .stButton > button,
div[data-testid="column"]:has(.tab-button-inactive) .stButton > button {
    border-radius: 8px 8px 0 0 !important;
    border: none !important;
    padding: 0.75rem 1.5rem !important;
    font-weight: 500 !important;
    transition: all 0.2s ease !important;
    margin-bottom: -2px !important;
    position: relative !important;
    z-index: 1 !important;
}

/* Active tab styling */
div[data-testid="column"]:has(.tab-button-active) .stButton > button {
    background: #FFFFFF !important;
    color: #2563EB !important;
    border-bottom: 3px solid #2563EB !important;
    box-shadow: 0 -2px 8px rgba(37, 99, 235, 0.1) !important;
}

/* Inactive tab styling */
div[data-testid="column"]:has(.tab-button-inactive) .stButton > button {
    background: #F3F4F6 !important;
    color: #6B7280 !important;
    border-bottom: 2px solid #E5E7EB !important;
}

div[data-testid="column"]:has(.tab-button-inactive) .stButton > button:hover {
    background: #E5E7EB !important;
    color: #374151 !important;
}

/* Executive Summary specific styles */
.summary-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;
}
</style>
"""

FORM_STYLES = """
<style>
    /* Background gradient */
    .main > div, .stApp {
        background: #FAFBFF; /* soft light gray FAFBFF*/
        padding: 20px;
        min-height: 200vh;
        background-attachment: fixed;
        background-size: cover;
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main container styling - WHITE BACKGROUND ON TOP */
    .block-container {
        background: rgba(255, 255, 255, 0.95) !important;
        backdrop-filter: blur(10px);
        border-radius: 20px;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
        padding: 40px !important;

        /* center and space */
        margin: 20px auto;

        box-sizing: border-box;
        min-height: calc(200dvh - 40px);
        
        max-width: 800px;
        position: relative;
        z-index: 10;
    }
    
    /* Header styling */
    .main-header {
        text-align: center;
        margin-bottom: 0.5px;
    }
    
    .main-title {
        color: #333;
        font-size: 2.5rem;
        font-weight: 300;
        margin-bottom: 10px;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    .main-subtitle {
        color: #666;
        font-size: 1.1rem;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Section styling */
    .form-section {
        margin-bottom: 35px;
    }
    
    .section-title {
        color: #4a5568;
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        gap: 10px;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    .section-title::before {
        content: '';
        width: 4px;
        height: 24px;
        background: linear-gradient(135deg, #0473EA, #2C3A87);
        border-radius: 2px;
    }
    
    /* Fields container */
    .fields-container {
        background: #f8fafc;
        border-radius: 16px;
        padding: 30px;
        border: 1px solid #e2e8f0;
        margin-bottom: 20px;
    }
    
    /* Optional fields styling */
    .optional-fields {
        background: #f1f5f9;
        border-radius: 12px;
        padding: 25px;
        border: 1px dashed #cbd5e1;
        margin-top: 20px;
    }
    
    .optional-header {
        color: #64748b;
        font-size: 1rem;
        font-weight: 500;
        margin-bottom: 15px;
        padding: 12px 16px;
        border-radius: 8px;
        background: rgba(102, 126, 234, 0.05);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Input styling */
    .stTextInput > div > div > input,
    .stDateInput > div > div > input,
    .stTextArea > div > div > textarea {
        border-radius: 12px !important;
        border: 2px solid #e5e7eb !important;
        padding: 14px 16px !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
    }
    
    
    /* Label styling */
    .stTextInput > label,
    .stDateInput > label,
    .stTextArea > label,
    .stFileUploader > label {
        color: #374151 !important;
        font-weight: 500 !important;
        font-size: 0.95rem !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
    }
    
    /* File uploader styling */
    .stFileUploader > div {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%) !important;
        border-radius: 16px !important;
        border: 2px dashed #cbd5e1 !important;
        padding: 30px !important;
        text-align: center !important;
    }
    
    .stFileUploader > div:hover {
        border-color: #667eea !important;
        background: linear-gradient(135deg, #f0f4ff 0%, #e0e7ff 100%) !important;
    }
    
    /* Submit button styling */
    .stButton > button {
        background: linear-gradient(135deg, #0473EA 0%, #2C3A87 100%) !important;
        color: white !important;
        border: none !important;
        padding: 16px 40px !important;
        border-radius: 12px !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        width: 100% !important;
        transition: all 0.3s ease !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 10px 25px rgba(102, 126, 234, 0.3) !important;
    }
    
    /* Required field indicator */
    .required::after {
        content: " *";
        color: #ef4444;
    }
    
    /* Optional field indicator */
    .optional::after {
        content: " (optional)";
        color: #9ca3af;
        font-weight: 400;
        font-size: 0.85rem;
    }
    
    /* Expander styling */
    .streamlit-expander {
        background: #f1f5f9 !important;
        border-radius: 12px !important;
        border: 1px dashed #cbd5e1 !important;
    }
    
    .streamlit-expander > div:first-child {
        background: rgba(102, 126, 234, 0.05) !important;
        border-radius: 8px !important;
        color: #64748b !important;
        font-weight: 500 !important;
    }
    
    /* Hide expander arrow and add custom */
    .streamlit-expander svg {
        display: none;
    }
    
    .streamlit-expander > div:first-child::after {
        content: ' ▼';
        float: right;
        color: #9ca3af;
        font-size: 0.8rem;
    }

    
</style>
"""