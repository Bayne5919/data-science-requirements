"""Phase 1: Authentication & Access Control."""

import streamlit as st
from utils.state import advance_phase


def render():
    """Render the authentication and access control phase."""
    st.markdown(
        '<div class="gov-card">'
        "<h3>Phase 1 — Authentication & Access Control</h3>"
        "<p>Before discussing any project specifics, we need to verify your identity "
        "and access level. Please provide your PKI certificate for authentication.</p>"
        "</div>",
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="gov-alert-info">'
        "<strong>Why is this required?</strong> Projects may contain classified or "
        "sensitive information. Authentication ensures you only see projects and "
        "examples within your authorized access level."
        "</div>",
        unsafe_allow_html=True,
    )

    # --- Certificate Upload ---
    st.subheader("Certificate Upload")
    cert_file = st.file_uploader(
        "Upload your PKI certificate (.p12 file)",
        type=["p12", "pfx"],
        help="Your organization-issued PKI certificate for identity verification.",
    )

    if cert_file is not None:
        st.session_state.cert_uploaded = True

    cert_password = st.text_input(
        "Certificate password",
        type="password",
        help="The passphrase associated with your PKI certificate.",
    )

    st.divider()

    # --- User Information ---
    st.subheader("User Information")
    col1, col2 = st.columns(2)
    with col1:
        user_name = st.text_input(
            "Full name",
            value=st.session_state.user_name,
            placeholder="e.g., Jane Doe",
        )
    with col2:
        clearance_level = st.selectbox(
            "Access / clearance level",
            options=["", "Unclassified", "CUI", "Secret", "Top Secret", "TS/SCI"],
            index=0,
            help="Select the highest classification level you are authorized to access.",
        )

    st.divider()

    # --- Authenticate Button ---
    can_submit = cert_file is not None and cert_password and user_name and clearance_level
    if st.button("Verify & Continue", disabled=not can_submit, use_container_width=True):
        # TODO: Implement actual PKI verification logic
        st.session_state.authenticated = True
        st.session_state.user_name = user_name
        st.session_state.clearance_level = clearance_level
        advance_phase()
        st.rerun()

    if not can_submit:
        st.caption("Please complete all fields above to proceed.")

    # --- Already Authenticated Notice ---
    if st.session_state.authenticated:
        st.markdown(
            '<div class="gov-alert-success">'
            f"<strong>Authenticated.</strong> Welcome, {st.session_state.user_name}. "
            f"Clearance level: <strong>{st.session_state.clearance_level}</strong>."
            "</div>",
            unsafe_allow_html=True,
        )
