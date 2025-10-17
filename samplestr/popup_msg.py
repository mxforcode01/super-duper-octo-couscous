import streamlit as st
from datetime import datetime

# --- Dialog ---
@st.dialog("Export RFP — Review & Attestation")
def confirm_export_dialog():
    st.markdown("""
**Please confirm that you have:**

- Reviewed all AI-assisted responses for **factual accuracy, completeness, and client suitability**.  
- Acknowledge that **Generative AI may produce errors or omissions**, and that **you are responsible** for the final content sent to clients.

""")

    agree = st.checkbox("I have reviewed the items above and accept responsibility for the exported content.")


    col1, col2 = st.columns(2)
    with col1:
        if st.button("Cancel", use_container_width=True):
            st.session_state["rfp_attested"] = False
            st.session_state["rfp_attest_meta"] = None
            st.rerun()

    with col2:
        disabled = not agree  # require the checkbox; keep initials optional or set `and initials` to require
        if st.button("I Attest & Export", type="primary", disabled=disabled, use_container_width=True):
            st.session_state["rfp_attested"] = True

            # Trigger your export flow here (function call, state flag, etc.)
            st.rerun()

# --- Trigger button somewhere in your page ---
st.button("Export RFP", on_click=confirm_export_dialog)

# --- Example: act on attestation (elsewhere on the page) ---
if st.session_state.get("rfp_attested"):
    # call your actual export function here
    st.success("RFP export started. (You can show progress or a download link here.)")
    # reset flag if you want single-use behavior
    st.session_state["rfp_attested"] = False
