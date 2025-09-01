import streamlit as st
from datetime import datetime
import time
import json
from css_rfp import QA_STYLES
# -----------------------------
# Page / global styles
# -----------------------------
st.set_page_config(page_title="Digital Transformation Initiative", layout="wide")

# Tailwind-like utility CSS for quick styling (scoped)
st.markdown(QA_STYLES,unsafe_allow_html=True)

# -----------------------------
# Demo data
# -----------------------------
QUESTIONS = [
    {
        "id": 1,
        "title": "Please describe your company's experience with similar digital transformation projects in the last 5 years.",
        "body": "Our company has successfully delivered over 50 digital transformation projects in the past 5 years...",
    },
    {
        "id": 2,
        "title": "How will you ensure data security and compliance with industry regulations?",
        "body": "Our comprehensive security framework ensures complete compliance with GDPR, HIPAA, SOC 2, and ISO 27001 standards...",
    },
]

# Initial executive summary
INITIAL_SUMMARY = """## Executive Summary

TechCorp Solutions proposes a comprehensive digital transformation initiative designed to modernize your organization's technology infrastructure and business processes. 

### Key Highlights

**Experience & Expertise**: With over 50 successful digital transformation projects delivered in the past 5 years, our team brings proven expertise across multiple industries including healthcare, finance, and retail. Our certified professionals have deep knowledge in cloud migration, data analytics, and process automation.

**Security & Compliance**: We maintain the highest standards of data security with comprehensive compliance frameworks covering GDPR, HIPAA, SOC 2, and ISO 27001. Our zero-trust security architecture ensures your data remains protected throughout the transformation journey.

**Implementation Approach**: Our phased implementation methodology minimizes disruption while maximizing value delivery. We begin with a thorough assessment phase, followed by strategic planning, pilot implementation, and full-scale rollout with continuous optimization.

**Expected Outcomes**: 
- 40% reduction in operational costs within 18 months
- 60% improvement in process efficiency
- Enhanced customer experience with 24/7 digital services
- Real-time data insights for better decision-making

**Investment & Timeline**: Total investment of $2.5M over 12 months, with ROI expected within 24 months. Our milestone-based approach ensures transparency and accountability at every stage.

This proposal represents not just a technology upgrade, but a strategic partnership to drive your organization's digital future."""

# -----------------------------
# Questions Session state
# -----------------------------
if "open_panel" not in st.session_state: 
    st.session_state.open_panel = False
if "active_qid" not in st.session_state: 
    st.session_state.active_qid = None
if "threads" not in st.session_state: 
    st.session_state.threads = {}  # {qid: [{role, content, ts}]}
if "answers" not in st.session_state: 
    st.session_state.answers = {}  # {qid: text}
if "chat_input" not in st.session_state:
    st.session_state.chat_input = ""
if "processing" not in st.session_state:
    st.session_state.processing = False
if "references" not in st.session_state:
    # Example structure: {qa_id: [{"title": "...","url":"...","source":"..."}]}
    st.session_state.references = {}

# Executive Summary specific states
if "executive_summary" not in st.session_state:
    st.session_state.executive_summary = INITIAL_SUMMARY
if "summary_history" not in st.session_state:
    st.session_state.summary_history = [INITIAL_SUMMARY]
if "summary_history_index" not in st.session_state:
    st.session_state.summary_history_index = 0
if "summary_chat_open" not in st.session_state:
    st.session_state.summary_chat_open = False
if "summary_threads" not in st.session_state:
    st.session_state.summary_threads = []
if "summary_processing" not in st.session_state:
    st.session_state.summary_processing = False
# Track active tab
if "active_tab" not in st.session_state:
    st.session_state.active_tab = 0

# Helpers
def human_like_response(message):
    for word in message.split(" "):
        yield word + " "
        time.sleep(0.02)

def push_message(qid: int, role: str, content: str, **extra):
    if qid not in st.session_state.threads:
        st.session_state.threads[qid] = []
    msg = {
        "role": role,
        "content": content,
        "ts": datetime.utcnow().isoformat()
    }
    msg.update(extra)
    st.session_state.threads[qid].append(msg)

def push_summary_message(role: str, content: str, **extra):
    msg = {
        "role": role,
        "content": content,
        "ts": datetime.utcnow().isoformat()
    }
    msg.update(extra)
    st.session_state.summary_threads.append(msg)

def open_chat(qid: int):
    st.session_state.active_qid = qid
    st.session_state.open_panel = True
    st.session_state.summary_chat_open = False

def _render_refs(qid, references_dict):
    df_dict = {"Filename": [], "Paragraph": []}
    refs = references_dict.get(qid, [])
    # can put this into table
    if not refs:
        st.caption("No references yet.")
        return
    # Accept dicts like {"filename":..., "url":..., "paragraph":...}
    for individual_ref in refs:
        filename = individual_ref['filename']
        url = individual_ref['url']
        paragraph = individual_ref['paragraph']
        df_dict['Filename'].append(f"[{filename}]({url})")
        df_dict['Paragraph'].append(paragraph)
    st.table(df_dict)

def open_summary_chat():
    st.session_state.summary_chat_open = True
    st.session_state.open_panel = True
    st.session_state.active_qid = None

def send_message():
    """Callback function for sending messages"""
    if st.session_state.chat_input and st.session_state.active_qid:
        qid = st.session_state.active_qid
        text = st.session_state.chat_input.strip()
        if text:
            push_message(qid, "user", text)
            qa = next((q for q in QUESTIONS if q["id"] == qid), None)
            if qa:
                reply = f'I understand you\'re asking about "{qa["title"][:30]}...". Here\'s my response to: {text}'
                push_message(qid, "assistant", reply)
            st.session_state.chat_input = ""

def undo_summary():
    if st.session_state.summary_history_index > 0:
        st.session_state.summary_history_index -= 1
        st.session_state.executive_summary = st.session_state.summary_history[st.session_state.summary_history_index]

def redo_summary():
    if st.session_state.summary_history_index < len(st.session_state.summary_history) - 1:
        st.session_state.summary_history_index += 1
        st.session_state.executive_summary = st.session_state.summary_history[st.session_state.summary_history_index]

def add_to_summary_history(new_summary):
    # Remove any history after current index (for when we're in the middle of history)
    st.session_state.summary_history = st.session_state.summary_history[:st.session_state.summary_history_index + 1]
    # Add new summary
    st.session_state.summary_history.append(new_summary)
    st.session_state.summary_history_index = len(st.session_state.summary_history) - 1
    st.session_state.executive_summary = new_summary

def generate_enhanced_summary(prompt):
    """Simulate AI generating an enhanced summary based on user prompt"""
    # This is a simulated enhancement - in production, this would call your AI service
    enhanced = st.session_state.executive_summary
    
    # Simulate different enhancements based on keywords in prompt
    if "shorter" in prompt.lower() or "concise" in prompt.lower():
        enhanced = """## Executive Summary

TechCorp Solutions offers a proven digital transformation solution with 50+ successful implementations. 

**Core Strengths**: Industry expertise, comprehensive security (GDPR, HIPAA, SOC 2, ISO 27001 compliant), and phased implementation approach.

**Key Benefits**: 40% cost reduction, 60% efficiency improvement, enhanced customer experience, real-time insights.

**Investment**: $2.5M over 12 months with 24-month ROI."""
        
    elif "technical" in prompt.lower() or "detail" in prompt.lower():
        enhanced = st.session_state.executive_summary + """

### Technical Architecture

**Cloud Infrastructure**: Multi-cloud strategy leveraging AWS, Azure, and GCP for optimal workload distribution. Kubernetes orchestration for containerized applications with auto-scaling capabilities.

**Data Platform**: Real-time data pipeline using Apache Kafka, Spark for processing, and Snowflake for analytics. Machine learning models deployed via MLOps framework.

**Security Stack**: Zero-trust architecture with microsegmentation, SIEM integration, automated threat detection, and 24/7 SOC monitoring."""
        
    elif "benefit" in prompt.lower() or "value" in prompt.lower():
        enhanced = st.session_state.executive_summary + """

### Additional Value Propositions

**Innovation Acceleration**: Access to our innovation lab and emerging technology pilots including AI/ML, IoT, and blockchain solutions.

**Change Management**: Comprehensive training programs and change management support to ensure smooth adoption across all organizational levels.

**Continuous Improvement**: Post-implementation optimization services with quarterly business reviews and performance benchmarking."""
    
    else:
        # Default enhancement
        enhanced = st.session_state.executive_summary.replace(
            "TechCorp Solutions proposes",
            "TechCorp Solutions is excited to propose"
        ).replace(
            "comprehensive digital transformation",
            "innovative and comprehensive digital transformation"
        )
    
    return enhanced

def get_change_summary(old_summary, new_summary):
    """Generate a summary of changes between old and new summaries"""
    # This is a simplified change detection - in production, you'd use more sophisticated diff algorithms
    changes = []
    
    if len(new_summary) < len(old_summary) * 0.7:
        changes.append("✂️ Condensed the summary to be more concise while maintaining key points")
    elif len(new_summary) > len(old_summary) * 1.3:
        changes.append("➕ Expanded the summary with additional details and sections")
    
    if "Technical Architecture" in new_summary and "Technical Architecture" not in old_summary:
        changes.append("🔧 Added technical architecture details")
    
    if "Value Propositions" in new_summary and "Value Propositions" not in old_summary:
        changes.append("💡 Included additional value propositions")
    
    if not changes:
        changes.append("✨ Enhanced language and improved clarity throughout the summary")
    
    return "\n".join(changes)

# -----------------------------
# Main content
# -----------------------------

# Header with Export button
header_col1, header_col2 = st.columns([5, 1])

with header_col1:
    st.markdown(
        """
        <div style="padding: 0;">
            <div class="header-title">Digital Transformation Initiative</div>
            <div class="header-subtitle">Client: TechCorp Solutions | Deadline: 2025-09-15</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with header_col2:
    # Prepare export data
    export_data = {
        "title": "Digital Transformation Initiative",
        "client": "TechCorp Solutions",
        "deadline": "2025-09-15",
        "executive_summary": st.session_state.executive_summary,
        "questions": []
    }
    
    for qa in QUESTIONS:
        answer = st.session_state.answers.get(qa["id"], "")
        export_data["questions"].append({
            "id": qa["id"],
            "question": qa["title"],
            "answer": answer if answer else "No answer provided yet"
        })
    
    # Convert to JSON
    export_json = json.dumps(export_data, indent=2)
    
    # Direct download button
    st.download_button(
        label="📥 Export RFP",
        data=export_json,
        file_name=f"RFP_Export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
        mime="application/json",
        key="export_rfp",
        use_container_width=True
    )

# Add some spacing after header
st.markdown("<div style='margin-bottom: 1rem;'></div>", unsafe_allow_html=True)

# Custom tab implementation with improved design
tab_col1, tab_col2, tab_spacer = st.columns([1.2, 1.2, 6])

with tab_col1:
    # Add invisible marker for CSS targeting
    if st.session_state.active_tab == 0:
        st.markdown('<div class="tab-button-active" style="display:none;"></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="tab-button-inactive" style="display:none;"></div>', unsafe_allow_html=True)
    
    if st.button(
        f"Questions ({len(QUESTIONS)})",
        key="tab_btn_questions",    
        use_container_width=True
    ):
        st.session_state.active_tab = 0
        st.rerun()

with tab_col2:
    # Add invisible marker for CSS targeting
    if st.session_state.active_tab == 1:
        st.markdown('<div class="tab-button-active" style="display:none;"></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="tab-button-inactive" style="display:none;"></div>', unsafe_allow_html=True)
    
    if st.button(
        "Executive Summary",
        key="tab_btn_summary", 
        use_container_width=True
    ):
        st.session_state.active_tab = 1
        st.rerun()

# Visual separator with cleaner styling
st.markdown(
    """
    <div style='
        border-bottom: 2px solid #E5E7EB; 
        margin-top: -1.0rem; 
        margin-bottom: 1.5rem;
        margin-left: -1rem;
        margin-right: -1rem;
    '></div>
    """,
    unsafe_allow_html=True
)

# Display content based on active tab
if st.session_state.active_tab == 0:
    # Questions Tab Content
    for qa in QUESTIONS:
        with st.container(border=True):
            st.markdown('<div class="qa-card-sentinel"></div>', unsafe_allow_html=True)
            st.markdown(
                f'<div class="card-header"><span class="qdot">{qa["id"]}</span> '
                f'<span class="question-title">{qa["title"]}</span></div>',
                unsafe_allow_html=True,
            )
            
            # Add marker for button styling
            st.markdown('<div class="qa-buttons-container" style="display:none;"></div>', unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns([6, 1, 1])
                
            with col2:
                if st.button("💬 Ask AI", key=f"chat_{qa['id']}", use_container_width=True):
                    open_chat(qa["id"])
            with col3:
                if st.button("✨ Rewrite", key=f"rephrase_{qa['id']}", use_container_width=True):
                    open_chat(qa["id"])
            
            key = f"ans_{qa['id']}"
            current = st.session_state.answers.get(qa["id"], "")
            new_val = st.text_area(" ", value=current, key=key, label_visibility="collapsed", height=200)
            st.session_state.answers[qa["id"]] = new_val

            # --- References UI (popover if available; otherwise expander) ---
            # refs = st.session_state.references.get(qa["id"], [])
            label = f"📚 References"

            # st.session_state.references[qa_id] = [
            #     {"title": "MAS Technology Risk Management Guidelines", "url": "https://www.mas.gov.sg/...", "source": "MAS"},
            #     {"title": "Internal Data Dictionary v3", "url": "https://sharepoint/...", "source": "SharePoint"},
            #     "Email from Ops (2025-08-12)"
            # ]

            with st.expander(label, expanded=False):
                _render_refs(qa['id'], st.session_state.references)

elif st.session_state.active_tab == 1:
    # Executive Summary Tab Content
    st.markdown('<div class="exec-summary-sentinel"></div>', unsafe_allow_html=True)
    
    # Executive Summary text area
    summary_key = f"exec_summary_{st.session_state.summary_history_index}"
    new_summary = st.text_area(
        "Executive Summary",
        value=st.session_state.executive_summary,
        key=summary_key,
        height=500,
        label_visibility="collapsed"
    )
    
    # Update summary if manually edited
    if new_summary != st.session_state.executive_summary:
        add_to_summary_history(new_summary)

    # Executive Summary buttons
    sum_col1, sum_col2, sum_col3, sum_col4 = st.columns([2, 4, 1, 1])
    
    with sum_col1:
        if st.button("🚀 Enhance with AI", key="enhance_summary", use_container_width=True):
            open_summary_chat()
    
    with sum_col3:
        undo_disabled = st.session_state.summary_history_index == 0
        if st.button("↩️ Undo", key="undo_summary", use_container_width=True, disabled=undo_disabled):
            undo_summary()
            st.rerun()
    
    with sum_col4:
        redo_disabled = st.session_state.summary_history_index >= len(st.session_state.summary_history) - 1
        if st.button("↪️ Redo", key="redo_summary", use_container_width=True, disabled=redo_disabled):
            redo_summary()
            st.rerun()
# -----------------------------
# Right-hand chat panel (Streamlit sidebar)
# -----------------------------
if st.session_state.open_panel:
    with st.sidebar:
        if st.session_state.summary_chat_open:
            # Executive Summary Enhancement Chat
            hleft, hright = st.columns([12,1])
            with hleft:
                st.markdown('<div class="chat-title">AI Summary Enhancement</div>', unsafe_allow_html=True)
                st.markdown(
                    '<div class="muted" style="font-size:12px">Enhance your executive summary with AI assistance</div>',
                    unsafe_allow_html=True,
                )
            with hright:
                if st.button('✕', key='close_summary_panel'):
                    st.session_state.summary_chat_open = False
                    st.session_state.open_panel = False
                    st.rerun()

            st.divider()

            # Chat container for summary
            chat_container = st.container(height=400)
            with chat_container:
                thread = st.session_state.summary_threads
                if not thread:
                    with st.chat_message("assistant"):
                        st.write("👋 Hi! I can help you enhance your executive summary. You can ask me to:\n\n• Make it more concise\n• Add technical details\n• Emphasize benefits and value\n• Adjust the tone or style\n• Focus on specific aspects\n\nWhat would you like to improve?")
                else:
                    for i, msg in enumerate(thread):
                        with st.chat_message(msg["role"]):
                            if (i == len(thread) - 1
                                and msg["role"] == "assistant"
                                and msg.get("stream", False)):
                                st.write_stream(human_like_response(msg["content"]))
                                st.session_state.summary_threads[i]["stream"] = False
                            else:
                                st.write(msg["content"])
            
            # Input for summary enhancement
            prompt = st.chat_input("How would you like to enhance the summary?", key="summary_chat_prompt")
            if prompt:
                # Add user message
                push_summary_message("user", prompt)
                st.rerun()

            # Handle AI response for summary
            if (st.session_state.summary_threads 
                and st.session_state.summary_threads[-1]["role"] == "user" 
                and not st.session_state.summary_processing):
                
                st.session_state.summary_processing = True
                
                with st.spinner("🤔 Enhancing your summary..."):
                    time.sleep(2)
                    
                    # Get the old summary before enhancement
                    old_summary = st.session_state.executive_summary
                    
                    # Generate enhanced summary
                    user_prompt = st.session_state.summary_threads[-1]["content"]
                    new_summary = generate_enhanced_summary(user_prompt)
                    
                    # Add to history
                    add_to_summary_history(new_summary)
                    
                    # Generate change summary
                    changes = get_change_summary(old_summary, new_summary)
                    
                    # Create response
                    response = f"""I've enhanced your executive summary based on your request: "{user_prompt}"

**Changes made:**
{changes}

The updated summary has been applied to the text area. You can:
- Continue refining with more instructions
- Use Undo/Redo buttons to navigate through versions
- Manually edit the text directly

Would you like any other adjustments?"""
                    
                    push_summary_message("assistant", response, stream=True)
                
                st.session_state.summary_processing = False
                st.rerun()
                
        else:
            # Original Questions Chat Panel
            qid = st.session_state.active_qid
            qa = next((q for q in QUESTIONS if q["id"] == qid), None)

            # Header
            hleft, hright = st.columns([12,1])
            with hleft:
                st.markdown('<div class="chat-title">AI Assistant</div>', unsafe_allow_html=True)
                if qa:
                    st.markdown(
                        f'<div class="muted" style="font-size:12px">Q{qa["id"]} — {qa["title"]}</div>',
                        unsafe_allow_html=True,
                    )
            with hright:
                if st.button('✕', key='close_panel'):
                    st.session_state.open_panel = False
                    st.session_state.active_qid = None
                    st.rerun()

            st.divider()

            # Chat container
            chat_container = st.container(height=400)
            with chat_container:
                thread = st.session_state.threads.get(qid, [])
                if not thread:
                    with st.chat_message("assistant"):
                        st.write("👋 Hi! How can I help you with this question?")
                else:
                    for i, msg in enumerate(thread):
                        with st.chat_message(msg["role"]):
                            if (i == len(thread) - 1
                                and msg["role"] == "assistant"
                                and msg.get("stream", False)):
                                st.write_stream(human_like_response(msg["content"]))
                                st.session_state.threads[qid][i]["stream"] = False
                            else:
                                st.write(msg["content"])
            
            # Input
            prompt = st.chat_input("Type your message here...", key="chat_prompt")
            if prompt:
                # Add user message and immediately rerun to show it
                push_message(qid, "user", prompt)
                st.rerun()

            # Handle AI response separately - check if last message needs AI response
            thread = st.session_state.threads.get(qid, [])
            if thread and thread[-1]["role"] == "user" and not st.session_state.get("processing", False):
                # Set processing flag to prevent multiple responses
                st.session_state.processing = True
                
                with st.spinner("🤔 AI is thinking..."):
                    time.sleep(2)
                    qa = next((q for q in QUESTIONS if q["id"] == qid), None)
                    if qa:
                        reply = f'I understand you\'re asking about "{qa["title"][:30]}...". Here\'s my response to: {thread[-1]["content"]}'
                        push_message(qid, "assistant", reply, stream=True)
                
                # Reset processing flag
                st.session_state.processing = False
                st.rerun()