import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Project Request Form",
    page_icon="📋",
    layout="centered"
)

# Custom CSS for styling
st.markdown("""
    <style>
    /* Main container styling */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Form container */
    .stApp {
        max-width: 800px;
        margin: 0 auto;
    }
    
    /* Section headers */
    .section-header {
        font-size: 1.3rem;
        font-weight: 600;
        color: #2d3748;
        margin-top: 2rem;
        margin-bottom: 0.5rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #e2e8f0;
    }
    
    /* Section description */
    .section-description {
        color: #718096;
        font-size: 0.9rem;
        font-style: italic;
        margin-bottom: 1rem;
    }
    
    /* Badge styling */
    .badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 12px;
        font-size: 0.7rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-left: 0.5rem;
    }
    
    .badge-required {
        background: #fed7d7;
        color: #c53030;
    }
    
    .badge-optional {
        background: #fef5e7;
        color: #d69e2e;
    }
    
    /* Filter group styling */
    .filter-group {
        background: #f0f4f8;
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    /* Style the container holding filter fields */
    div[data-testid="stVerticalBlock"]:has(.filter-label) {
        background: #f0f4f8;
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .filter-label {
        font-size: 0.75rem;
        font-weight: 600;
        color: #4a5568;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 1rem;
    }
    
    /* Radio button container */
    div[data-testid="stRadio"] > div {
        background: #f7fafc;
        border: 2px solid #e2e8f0;
        border-radius: 12px;
        padding: 1.5rem;
    }
    
    /* Submit button */
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: 600;
        padding: 0.75rem 1.5rem;
        border-radius: 8px;
        border: none;
        transition: transform 0.2s;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 20px rgba(102, 126, 234, 0.4);
    }
    </style>
""", unsafe_allow_html=True)

# Helper function to render section headers
def render_section_header(icon, title, badge_text, badge_type):
    badge_class = "badge-required" if badge_type == "required" else "badge-optional"
    st.markdown(f"""
        <div class="section-header">
            {icon} {title} 
            <span class="badge {badge_class}">{badge_text}</span>
        </div>
    """, unsafe_allow_html=True)

# Helper function to render section description
def render_section_description(text):
    st.markdown(f'<div class="section-description">{text}</div>', unsafe_allow_html=True)

# Main title
st.title("📋 Project Request Form")
st.caption("Fill out the details below to generate your documents")

# Output selection
st.markdown("### What would you like to generate? *")
output_choice = st.radio(
    "output_selection",
    options=[
        "Executive Summary only",
        "RFP Questionnaires only",
        "Both Executive Summary and RFP Questionnaires"
    ],
    index=2,  # Default to "Both"
    label_visibility="collapsed"
)

# Determine what sections to show based on selection
show_exec = output_choice in ["Executive Summary only", "Both Executive Summary and RFP Questionnaires"]
show_rfp = output_choice in ["RFP Questionnaires only", "Both Executive Summary and RFP Questionnaires"]

# Determine badge types
exec_badge = "REQUIRED" if show_exec and output_choice != "RFP Questionnaires only" else "OPTIONAL"
rfp_badge = "REQUIRED" if show_rfp and output_choice != "Executive Summary only" else "OPTIONAL"

exec_badge_type = "required" if exec_badge == "REQUIRED" else "optional"
rfp_badge_type = "required" if rfp_badge == "REQUIRED" else "optional"

# Create the form
with st.form("project_form"):
    
    # Section 1: Project Information
    render_section_header("📋", "Project Information", "REQUIRED", "required")
    render_section_description("Basic details needed for all outputs")
    
    # Client Name and Project Title
    col1, col2 = st.columns(2)
    with col1:
        client_name = st.text_input("Client Name *", placeholder="Enter client name")
    with col2:
        project_title = st.text_input("Project Title *", placeholder="Enter project title")
    
    # Filter Group
    # st.markdown('<div class="filter-group">', unsafe_allow_html=True)
    st.markdown("**FILTERS & CATEGORIES**")
    
    col3, col4 = st.columns(2)
    with col3:
        region = st.selectbox(
            "Region *",
            options=["", "North America", "Europe", "Asia Pacific", "Latin America", "Middle East & Africa"],
            index=0
        )
    with col4:
        country = st.selectbox(
            "Country *",
            options=["", "United States", "United Kingdom", "Singapore", "Australia", "Canada", "Germany", "Japan"],
            index=0
        )
    
    col5, col6 = st.columns(2)
    with col5:
        client_type = st.selectbox(
            "Client Type *",
            options=["", "Enterprise", "SMB", "Startup", "Government", "Non-Profit"],
            index=0
        )
    with col6:
        product_type = st.selectbox(
            "Product Type *",
            options=["", "SaaS", "Consulting", "Implementation", "Support", "Training"],
            index=0
        )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Section 2: Executive Summary (conditionally rendered)
    if show_exec:
        render_section_header("📄", "Executive Summary Details", exec_badge, exec_badge_type)
        render_section_description("These details help us create a compelling executive summary")
        
        client_objectives = st.text_area(
            "Client Objectives *" if exec_badge == "REQUIRED" else "Client Objectives",
            placeholder="Describe the client's key objectives and goals for this project...",
            height=120
        )
        
        solution_overview = st.text_area(
            "Solution Overview *" if exec_badge == "REQUIRED" else "Solution Overview",
            placeholder="Provide a high-level overview of your proposed solution...",
            height=120
        )
    else:
        client_objectives = None
        solution_overview = None
    
    # Section 3: RFP Questionnaires (conditionally rendered)
    if show_rfp:
        render_section_header("❓", "RFP Questionnaires", rfp_badge, rfp_badge_type)
        render_section_description("Upload or paste your RFP questions here")
        
        rfp_questions = st.text_area(
            "RFP Questions *" if rfp_badge == "REQUIRED" else "RFP Questions",
            placeholder="Paste your RFP questionnaire here, or describe the questions you need answered...",
            height=120
        )
    else:
        rfp_questions = None
    
    # Dynamic submit button text
    if output_choice == "Executive Summary only":
        button_text = "Generate Executive Summary"
    elif output_choice == "RFP Questionnaires only":
        button_text = "Generate RFP Responses"
    else:
        button_text = "Generate Documents"
    
    # Submit button
    submitted = st.form_submit_button(button_text, use_container_width=True)
    
    # Form validation and submission logic
    if submitted:
        errors = []
        
        # Validate required fields
        if not client_name:
            errors.append("Client Name is required")
        if not project_title:
            errors.append("Project Title is required")
        if not region:
            errors.append("Region is required")
        if not country:
            errors.append("Country is required")
        if not client_type:
            errors.append("Client Type is required")
        if not product_type:
            errors.append("Product Type is required")
        
        # Validate conditional fields
        if show_exec and exec_badge == "REQUIRED":
            if not client_objectives:
                errors.append("Client Objectives is required for Executive Summary")
            if not solution_overview:
                errors.append("Solution Overview is required for Executive Summary")
        
        if show_rfp and rfp_badge == "REQUIRED":
            if not rfp_questions:
                errors.append("RFP Questions is required for RFP Questionnaires")
        
        # Display results
        if errors:
            st.error("Please fix the following errors:")
            for error in errors:
                st.error(f"• {error}")
        else:
            st.success("✅ Form submitted successfully!")
            st.balloons()
            
            # Display summary
            with st.expander("📊 View Submission Summary", expanded=True):
                st.subheader("Project Information")
                st.write(f"**Client Name:** {client_name}")
                st.write(f"**Project Title:** {project_title}")
                st.write(f"**Region:** {region}")
                st.write(f"**Country:** {country}")
                st.write(f"**Client Type:** {client_type}")
                st.write(f"**Product Type:** {product_type}")
                
                if show_exec and client_objectives:
                    st.subheader("Executive Summary")
                    st.write(f"**Client Objectives:** {client_objectives}")
                    st.write(f"**Solution Overview:** {solution_overview}")
                
                if show_rfp and rfp_questions:
                    st.subheader("RFP Questionnaires")
                    st.write(f"**RFP Questions:** {rfp_questions}")
                
                st.info(f"📄 Output Type: {output_choice}")

# Footer
st.markdown("---")
st.caption("💡 Tip: Select your desired output at the top to see relevant fields")