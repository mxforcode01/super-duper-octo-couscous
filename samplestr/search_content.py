import streamlit as st
# from main import *
# from css_rfp import SEARCH_STYLES
import time
import pandas as pd

# ==================== HELPER FUNCTIONS ====================

def human_like_response(response, processing_time_str):
    """Stream response word by word for natural effect"""
    for word in response.split(" "):
        yield word + " "
        time.sleep(0.03)
    yield processing_time_str


def generate_ai_response(session_state, user_qn):
    """
    Generate AI response with processing time
    Returns: (response_text, processing_time_str, references, suggested_questions)
    """
    start_time = time.time()
    # Get context and references from backend
    # context_strings, references = send_to_backend(session_state, user_qn)
    
    # Get AI answer
    # response = get_answer(user_qn, context_strings)
    response = "This is a mock response to your query about '{}'.".format(user_qn)
    references = [
        {"filename": "Document1.pdf", "url": "http://example.com/doc1", "Updated Date": "2024-01-15"},
        {"filename": "Document2.pdf", "url": "http://example.com/doc2", "Updated Date": "2024-02-20"}
    ]

    # Calculate processing time
    end_time = time.time()
    elapsed_time = f'{end_time - start_time:.1f}'
    processing_time_str = f"  \n:blue[Processing Time: {elapsed_time}s]"
    
    # Generate suggested questions based on the query
    suggested_questions = generate_suggested_questions(user_qn, response)
    
    return response, processing_time_str, references, suggested_questions


def generate_suggested_questions(user_question, ai_response):
    """
    Generate 3 suggested follow-up questions based on the user's query and AI response
    TODO: Replace with actual logic based on your AI model
    """
    # Mock suggestions - replace with your actual logic
    suggestions_map = {
        "loan": [
            "What are the interest rates for business loans?",
            "What documents are required for loan application?",
            "How long does the loan approval process take?"
        ],
        "sustainability": [
            "What is our renewable energy investment strategy?",
            "How do we measure our carbon footprint?",
            "What are our diversity and inclusion targets?"
        ],
        "digital banking": [
            "How do I set up mobile banking?",
            "What security features does digital banking have?",
            "Can I open an account online?"
        ],
        "default": [
            "Can you provide more details on this topic?",
            "What are the related policies?",
            "Where can I find additional documentation?"
        ]
    }
    
    # Simple keyword matching - replace with your actual logic
    user_question_lower = user_question.lower()
    for keyword, suggestions in suggestions_map.items():
        if keyword in user_question_lower:
            return suggestions
    
    return suggestions_map["default"]


def render_references(refs):
    """Display references as a formatted table"""
    if not refs:
        st.caption("No references available.")
        return
    
    # Convert to DataFrame and format links
    reference_df = pd.DataFrame(refs)
    reference_df['Filename'] = reference_df.apply(
        lambda x: f'<a href="{x["url"]}" target="_blank">{x["filename"]}</a>', 
        axis=1
    )
    
    # Custom table styling
    st.markdown(
        """
        <style>
        table td { text-align: left !important; }
        table th { text-align: left !important; }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown(
        reference_df[['Filename', 'Updated Date']].to_html(escape=False, index=False), 
        unsafe_allow_html=True
    )


def render_suggested_questions(suggestions, message_idx):
    """Display suggested questions as clickable buttons"""
    if not suggestions:
        return
    
    st.markdown("**Continue exploring:**")
    
    for i, suggestion in enumerate(suggestions):
        # Use unique key for each button
        if st.button(
            suggestion, 
            key=f"suggestion_{message_idx}_{i}",
            use_container_width=True
        ):
            # Add suggestion as new user message
            st.session_state.qamessages.append({
                "role": "user", 
                "content": suggestion
            })
            
            # Generate AI response for this suggestion
            with st.spinner('Processing...'):
                response, time_str, refs, new_suggestions = generate_ai_response(
                    st.session_state, 
                    suggestion
                )
                
                # Add AI response to chat history with streaming flag
                st.session_state.qamessages.append({
                    "role": "assistant",
                    "content": "",  # Empty initially
                    "response": response,
                    "time_str": time_str,
                    "references": refs,
                    "suggestions": new_suggestions,
                    "needs_streaming": True
                })
            
            st.rerun()


def initialize_session_state():
    """Initialize all session state variables"""
    if "qamessages" not in st.session_state:
        st.session_state.qamessages = []
    
    if "qasources" not in st.session_state:
        st.session_state.qasources = ["All"]
    
    if "qaprompt" not in st.session_state:
        st.session_state.qaprompt = ""
    
    if "user_input" not in st.session_state:
        st.session_state.user_input = {
            'region': "ALL",
            'country': "ALL"
        }


def render_header():
    """Render the custom header with navigation"""
    st.markdown(
        """
        <div class="top-bar">
            <div class="top-bar-left">TB Sales</div>
            <div class="top-bar-right">
                <a href="#">Content Library</a>
                <a href="#">FAQ</a>
                <a href="#" class="custom-button">Home</a>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_welcome_state():
    """Display welcome message with starter questions when chat is empty"""
    st.markdown(
        """
        <div style="text-align: center; padding: 60px 24px;">
            <div style="font-size: 64px; margin-bottom: 24px;">💬</div>
            <h2 style="color: #1A202C; margin-bottom: 12px;">How can I help you today?</h2>
            <p style="color: #718096; font-size: 16px; margin-bottom: 32px;">
                Search through our knowledge base using natural language. Ask me anything!
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Starter questions
    col1, col2 = st.columns(2)
    
    starter_questions = [
        "What are the latest sustainability initiatives?",
        "How do I apply for a business loan?",
        "What are our digital banking features?",
        "Where can I find compliance policies?"
    ]
    
    with col1:
        if st.button(starter_questions[0], key="starter1", use_container_width=True):
            process_user_input(starter_questions[0])
        
        if st.button(starter_questions[2], key="starter3", use_container_width=True):
            process_user_input(starter_questions[2])
    
    with col2:
        if st.button(starter_questions[1], key="starter2", use_container_width=True):
            process_user_input(starter_questions[1])
        
        if st.button(starter_questions[3], key="starter4", use_container_width=True):
            process_user_input(starter_questions[3])


def process_user_input(prompt):
    """Process user input and generate AI response"""
    # Add user message to chat history
    st.session_state.qamessages.append({
        "role": "user",
        "content": prompt
    })
    
    # Generate AI response
    sources = st.session_state.qasources
    if len(sources) == 0:
        sources = ['All']
    
    st.session_state.qasources = sources
    st.session_state.qaprompt = prompt
    
    with st.spinner('Processing...'):
        response, time_str, refs, suggestions = generate_ai_response(
            st.session_state, 
            prompt
        )
        
        # Add AI response to chat history with streaming flag
        st.session_state.qamessages.append({
            "role": "assistant",
            "content": "",  # Empty initially, will be filled during streaming
            "response": response,  # Store the actual response
            "time_str": time_str,  # Store the time string
            "references": refs,
            "suggestions": suggestions,
            "needs_streaming": True  # Flag to indicate this message needs streaming
        })
    
    st.rerun()


# ==================== MAIN APP ====================

def show():
    """Main function to render the search content page"""
    
    # Apply custom CSS
    st.markdown("""
        <style>
        /* Suggested question buttons styling */
        div[data-testid="stButton"] > button {
            border: 2px solid #2563EB;
            background-color: #FFFFFF;
            color: #2563EB;
            font-weight: 500;
            transition: all 0.3s ease;
        }
        
        div[data-testid="stButton"] > button:hover {
            background-color: #2563EB;
            color: #FFFFFF;
        }
        
        /* Back button specific styling */
        div[data-testid="column"]:last-child div[data-testid="stButton"] > button {
            border: 2px solid #DC2626;
            background-color: #DC2626;
            color: #FFFFFF;
            font-weight: 600;
        }
        
        div[data-testid="column"]:last-child div[data-testid="stButton"] > button:hover {
            background-color: #B91C1C;
            border-color: #B91C1C;
        }
        
        /* Alternative approach for more specific targeting if needed */
        button[kind="secondary"] {
            border: 2px solid #2563EB;
            background-color: #FFFFFF;
            color: #2563EB;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # st.markdown(SEARCH_STYLES, unsafe_allow_html=True)
    
    # Render header
    
    
    # Page title and description
    col2, col3 = st.columns([9,1])
    # with col1:
    #     st.title("Search Content 🔍")
    #     st.write("Ask questions related to products and services")
    with col3:
        back_button = st.button("Back")
        if back_button:
            st.info("Clicked Back button - implement navigation logic here.")
        
    # Initialize session state
    initialize_session_state()
    
    # Show welcome state if no messages
    if len(st.session_state.qamessages) == 0:
        render_welcome_state()
    
    # Display chat history
    for idx, message in enumerate(st.session_state.qamessages):
        with st.chat_message(message["role"]):
            if message["role"] == "assistant" and message.get("needs_streaming", False):
                # This is a new message that needs streaming
                message_placeholder = st.empty()
                
                # Stream the response
                full_response = ""
                for chunk in human_like_response(message["response"], message["time_str"]):
                    full_response += chunk
                    message_placeholder.markdown(full_response)
                
                # Update the message content and remove the streaming flag
                st.session_state.qamessages[idx]["content"] = full_response
                st.session_state.qamessages[idx]["needs_streaming"] = False
                
                # Show references
                if "references" in message:
                    with st.expander("📚 See sources", expanded=False):
                        render_references(message["references"])
                
                # Show suggested questions
                if "suggestions" in message:
                    render_suggested_questions(message["suggestions"], idx)
            else:
                # Display already streamed messages normally
                st.markdown(message["content"])
                
                # Show references for assistant messages
                if message["role"] == "assistant" and "references" in message:
                    with st.expander("📚 See sources", expanded=False):
                        render_references(message["references"])
                
                # Show suggested questions for assistant messages
                if message["role"] == "assistant" and "suggestions" in message:
                    render_suggested_questions(message["suggestions"], idx)
    
    # Chat input
    if prompt := st.chat_input("Ask me"):
        # Display user message immediately
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Add to history and process
        process_user_input(prompt)


# Run the app
if __name__ == "__main__":
    show()
