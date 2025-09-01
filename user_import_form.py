import streamlit as st
from datetime import date, datetime
import pandas as pd
from css_rfp import FORM_STYLES
# Page configuration
# st.set_page_config(
#     page_title="Project Details Form",
#     page_icon="📋",
#     layout="wide",
#     initial_sidebar_state="collapsed"
# )

# Custom CSS to match the HTML design
st.markdown(FORM_STYLES, unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">', unsafe_allow_html=True)
st.markdown('<h1 class="main-title">RFP Details</h1>', unsafe_allow_html=True)
st.markdown('<p class="main-subtitle">Let\'s get your RFP started with some basic information</p>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Form
with st.form("project_form"):
    # Essential Information Section
    st.markdown('<div class="section-title">Essential Information</div>', unsafe_allow_html=True)
    
    # st.markdown('<div class="fields-container">', unsafe_allow_html=True)
    
    # Row 1: Client Name and Project Title (2 columns)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="required">Client Name</div>', unsafe_allow_html=True)
        client_name = st.text_input("Client Name", label_visibility="collapsed", key="client_name")
    
    with col2:
        st.markdown('<div class="required">Project Title</div>', unsafe_allow_html=True)
        project_title = st.text_input("Project Title", label_visibility="collapsed", key="project_title")
    
    # Row 2: Submission Deadline (full width)
    st.markdown('<div class="required">Submission Deadline</div>', unsafe_allow_html=True)
    deadline = st.date_input("Submission Deadline", 
                           min_value=date.today(), 
                           label_visibility="collapsed",
                           key="deadline")
    
    # Optional Fields in Expander
    with st.expander("**Additional Details**"):
        st.markdown('<div style="margin-top: 10px;"></div>', unsafe_allow_html=True)
        
        # Optional fields in 2 columns
        opt_col1, opt_col2 = st.columns(2)
        
        with opt_col1:
            st.markdown('<div class="optional">Region</div>', unsafe_allow_html=True)
            region = st.text_input("Region", 
                                 placeholder="e.g., North America, EMEA",
                                 label_visibility="collapsed",
                                 key="region")
            
            st.markdown('<div class="optional">Client Type</div>', unsafe_allow_html=True)
            client_type = st.text_input("Client Type", 
                                      placeholder="e.g., Enterprise, SMB, Startup",
                                      label_visibility="collapsed",
                                      key="client_type")
        
        with opt_col2:
            st.markdown('<div class="optional">Country</div>', unsafe_allow_html=True)
            country = st.text_input("Country", 
                                   placeholder="e.g., United States, Germany",
                                   label_visibility="collapsed",
                                   key="country")
            
            st.markdown('<div class="optional">Deal ID</div>', unsafe_allow_html=True)
            deal_id = st.text_input("Deal ID", 
                                  placeholder="e.g., DEAL-2024-001",
                                  label_visibility="collapsed",
                                  key="deal_id")
    
    st.markdown('</div>', unsafe_allow_html=True)  # Close fields-container
    
    # Project Objectives Section
    st.markdown('<div class="section-title">Project Objectives</div>', unsafe_allow_html=True)
    st.markdown('<div class="required">Client Objectives</div>', unsafe_allow_html=True)
    objectives = st.text_area("Client Objectives", 
                            placeholder="Describe the main goals and objectives for this project...",
                            height=120,
                            label_visibility="collapsed",
                            key="objectives")
    
    # Supporting Documents Section  
    st.markdown('<div class="section-title">Upload RFP Questionnaire</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Excel File",
                                   type=['xlsx', 'xls'],
                                   help="Click to browse or drag and drop your .xlsx or .xls file here")
    
    # Submit Button
    st.markdown('<div style="margin-top: 30px;"></div>', unsafe_allow_html=True)
    submitted = st.form_submit_button("Generate with AI")
    
    # Form validation and processing
    if submitted:
        # Check required fields
        required_fields = {
            'Client Name': client_name,
            'Project Title': project_title,
            'Submission Deadline': deadline,
            'Client Objectives': objectives
        }
        
        missing_fields = [field for field, value in required_fields.items() if not value]
        
        if missing_fields:
            st.error(f"Please fill in the following required fields: {', '.join(missing_fields)}")
        else:
            # Success message
            st.success("🎉 Project created successfully!")
            
            # Display collected data
            st.markdown("### Collected Information:")
            
            # Essential info
            st.markdown("**Essential Information:**")
            st.write(f"• Client Name: {client_name}")
            st.write(f"• Project Title: {project_title}")
            st.write(f"• Submission Deadline: {deadline.strftime('%B %d, %Y')}")
            
            # Optional info (only show if provided)
            optional_info = []
            if region: optional_info.append(f"• Region: {region}")
            if country: optional_info.append(f"• Country: {country}")
            if client_type: optional_info.append(f"• Client Type: {client_type}")
            if deal_id: optional_info.append(f"• Deal ID: {deal_id}")
            
            if optional_info:
                st.markdown("**Additional Details:**")
                for info in optional_info:
                    st.write(info)
            
            # Objectives
            st.markdown("**Project Objectives:**")
            st.write(objectives)
            
            # File info
            if uploaded_file is not None:
                st.markdown("**Uploaded File:**")
                st.write(f"• File: {uploaded_file.name}")
                st.write(f"• Size: {uploaded_file.size} bytes")
                
                # You could process the Excel file here
                # df = pd.read_excel(uploaded_file)
                # st.dataframe(df.head())