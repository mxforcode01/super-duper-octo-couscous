import streamlit as st
from datetime import datetime, timedelta

# Page configuration
st.set_page_config(page_title="RFP Responses", layout="wide", page_icon="📄")

# Custom CSS for clean, modern styling matching qa_container.py
st.markdown("""
<style>
    /* Main background - light grey */
    .main {
        background-color: #f5f5f7;
    }
    
    .block-container {
        padding-top: 3rem;
        padding-bottom: 3rem;
    }
    
    /* Header section */
    .title-section {
        display: flex;
        align-items: center;
        gap: 15px;
        margin-bottom: 2rem;
    }
    
    .icon-box {
        width: 60px;
        height: 60px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 28px;
    }
    
    .page-title {
        font-size: 32px;
        font-weight: 700;
        color: #1a1a1a;
        margin: 0;
    }
    
    /* Gradient button */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.6rem 1.5rem !important;
        font-weight: 600 !important;
        font-size: 15px !important;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4) !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button[kind="primary"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 16px rgba(102, 126, 234, 0.5) !important;
    }
    
    .count-text {
        color: #888;
        font-size: 14px;
        margin-bottom: 1.5rem;
    }
    
    /* RFP Card Title */
    .rfp-title {
        font-size: 20px;
        font-weight: 600;
        color: #1a1a1a;
        line-height: 1.4;
        margin: 0;
    }
    
    /* Status badge */
    .status-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        margin-bottom: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .status-submitted {
        background-color: #d4f4dd;
        color: #00a758;
    }
    
    .status-draft {
        background-color: #fff4e6;
        color: #f39c12;
    }
    
    .status-review {
        background-color: #e8eaf6;
        color: #5c6bc0;
    }
    
    /* Info items */
    .info-row {
        display: flex;
        gap: 2rem;
        margin-top: 1rem;
        margin-bottom: 0.5rem;
    }
    
    .info-item {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 14px;
        color: #666;
    }
    
    .info-icon {
        font-size: 16px;
    }
    
    /* Uniform button styling - matching qa_container.py */
    .stButton > button {
        border-radius: 8px !important;
        font-weight: 500 !important;
        font-size: 14px !important;
        padding: 0.5rem 1rem !important;
        transition: all 0.2s ease !important;
        background-color: #667eea !important;
        color: white !important;
        border: none !important;
    }
    
    .stButton > button:hover {
        background-color: #5568d3 !important;
        transform: translateY(-1px) !important;
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: white;
    }
    
    /* Container styling */
    [data-testid="stVerticalBlock"] > [style*="flex-direction: column;"] > [data-testid="stVerticalBlock"] {
        background-color: white;
    }
    
    /* Hide streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Sample data
rfp_data = [
    {
        "id": 1,
        "status": "SUBMITTED",
        "title": "Banking Solutions for SME Sector",
        "created": "Oct 10, 2025",
        "due": "Oct 25, 2025",
        "client": "TechCorp Industries",
        "assignee": "John Davis",
        "progress": 100
    },
    {
        "id": 2,
        "status": "DRAFT",
        "title": "Digital Transformation Project Q4",
        "created": "Oct 12, 2025",
        "due": "Oct 30, 2025",
        "client": "Global Finance Ltd",
        "assignee": "Sarah Chen",
        "progress": 45
    },
    {
        "id": 3,
        "status": "IN REVIEW",
        "title": "Treasury Management Services",
        "created": "Oct 8, 2025",
        "due": "Oct 25, 2025",
        "client": "Manufacturing Corp",
        "assignee": "John Davis",
        "progress": 75
    },
    {
        "id": 4,
        "status": "SUBMITTED",
        "title": "Trade Finance Solutions APAC",
        "created": "Oct 5, 2025",
        "due": "Oct 20, 2025",
        "client": "Asia Trading Co",
        "assignee": "Mike Wilson",
        "progress": 100
    },
    {
        "id": 5,
        "status": "DRAFT",
        "title": "Sustainability Investment Framework",
        "created": "Oct 15, 2025",
        "due": "Nov 5, 2025",
        "client": "Green Energy Partners",
        "assignee": "Sarah Chen",
        "progress": 30
    }
]

# Initialize session state
if 'rfp_list' not in st.session_state:
    st.session_state.rfp_list = rfp_data

# Helper functions
def get_status_badge(status):
    icons = {
        "SUBMITTED": "✓",
        "DRAFT": "📝",
        "IN REVIEW": "⏳"
    }
    classes = {
        "SUBMITTED": "status-submitted",
        "DRAFT": "status-draft",
        "IN REVIEW": "status-review"
    }
    icon = icons.get(status, "")
    badge_class = classes.get(status, "")
    return f'<div class="status-badge {badge_class}">{icon} {status}</div>'

# HEADER
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("""
    <div class="title-section">
        <div class="icon-box">📄</div>
        <h1 class="page-title">RFP Responses</h1>
    </div>
    """, unsafe_allow_html=True)

with col2:
    if st.button("➕ Create New RFP", type="primary", use_container_width=True):
        st.session_state.page = "new_rfp"
        st.success("✨ Opening new RFP form...")

st.write("")

# Filter RFPs (no filters for now, but structure is ready)
filtered_rfps = st.session_state.rfp_list

# Count
st.markdown(f'<p class="count-text">Showing {len(filtered_rfps)} of {len(st.session_state.rfp_list)} responses</p>', unsafe_allow_html=True)

# Display RFP Cards in containers (matching qa_container.py style)
for rfp in filtered_rfps:
    with st.container(border=True):
        # Status badge
        st.markdown(get_status_badge(rfp['status']), unsafe_allow_html=True)
        
        # Title and Buttons in same row
        title_col, btn_col1, btn_col2 = st.columns([6, 1, 1])
        
        with title_col:
            st.markdown(f'<div class="rfp-title">{rfp["title"]}</div>', unsafe_allow_html=True)
        
        with btn_col1:
            if st.button("✏️ Modify", key=f"mod_{rfp['id']}", use_container_width=True):
                st.session_state.selected_rfp = rfp['id']
                st.info(f"✏️ Editing: {rfp['title']}")
        
        with btn_col2:
            if st.button("🗑️ Delete", key=f"del_{rfp['id']}", use_container_width=True):
                st.session_state.rfp_list = [r for r in st.session_state.rfp_list if r['id'] != rfp['id']]
                st.rerun()
        
        # Info row - Client, Created, Due Date
        st.markdown(f"""
        <div class="info-row">
            <div class="info-item">
                <span class="info-icon">🏢</span>
                <span>Client: <strong>{rfp["client"]}</strong></span>
            </div>
            <div class="info-item">
                <span class="info-icon">📅</span>
                <span>Created: <strong>{rfp["created"]}</strong></span>
            </div>
            <div class="info-item">
                <span class="info-icon">⏰</span>
                <span>Due: <strong>{rfp["due"]}</strong></span>
            </div>
        </div>
        """, unsafe_allow_html=True)

# Empty state
if len(filtered_rfps) == 0:
    st.markdown("""
    <div style="text-align: center; padding: 3rem; color: #888;">
        <h3>No RFP responses found</h3>
        <p>Try adjusting your filters or create a new RFP response.</p>
    </div>
    """, unsafe_allow_html=True)