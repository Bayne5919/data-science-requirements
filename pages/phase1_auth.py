"""Phase 1: Authentication & Access Control."""

import streamlit as st
from utils.state import advance_phase


def render():
    """Render the authentication and access control phase."""
    st.markdown(
        '<div class="gov-card">'
        "<h3>Phase 1 — Authentication & Access Control</h3>"
        "<p>Before discussing any project specifics, we need to verify your identity "
        "and access level. Select your clearance level below to get started.</p>"
        "</div>",
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="gov-alert-info">'
        "<strong>Why is this required?</strong> Projects may contain classified or "
        "sensitive information. Authentication ensures you only see projects and "
        "examples within your authorized access level. Unclassified users may "
        "proceed without a PKI certificate."
        "</div>",
        unsafe_allow_html=True,
    )

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
        clearance_options = ["", "Unclassified", "CUI", "Secret", "Top Secret", "TS/SCI"]
        current_idx = (
            clearance_options.index(st.session_state.clearance_level)
            if st.session_state.clearance_level in clearance_options
            else 0
        )
        clearance_level = st.selectbox(
            "Access / clearance level",
            options=clearance_options,
            index=current_idx,
            help="Select the highest classification level you are authorized to access.",
        )

    is_unclassified = clearance_level == "Unclassified"

    st.divider()

    # --- PKI Certificate (required for CUI and above) ---
    if is_unclassified:
        st.markdown(
            '<div class="gov-alert-info">'
            "<strong>Unclassified access selected.</strong> PKI certificate is not "
            "required. You will only be able to view projects and data at the "
            "Unclassified level."
            "</div>",
            unsafe_allow_html=True,
        )
    else:
        st.subheader("Certificate Upload")
        st.markdown(
            "A PKI certificate is required for **CUI** and above."
        )
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

    # --- Authenticate Button ---
    if is_unclassified:
        can_submit = bool(user_name and clearance_level)
    else:
        can_submit = (
            st.session_state.cert_uploaded
            and cert_password  # noqa: F821 — only evaluated when not unclassified
            and user_name
            and clearance_level
        )

    if st.button("Verify & Continue", disabled=not can_submit, use_container_width=True):
        # TODO: Implement actual PKI verification logic for classified levels
        st.session_state.authenticated = True
        st.session_state.user_name = user_name
        st.session_state.clearance_level = clearance_level
        advance_phase()
        st.rerun()

    if not can_submit:
        if not user_name or not clearance_level:
            st.caption("Please enter your name and select a clearance level to proceed.")
        elif not is_unclassified:
            st.caption("Please upload your PKI certificate and enter the password to proceed.")

    # --- Already Authenticated Notice ---
    if st.session_state.authenticated:
        st.markdown(
            '<div class="gov-alert-success">'
            f"<strong>Authenticated.</strong> Welcome, {st.session_state.user_name}. "
            f"Clearance level: <strong>{st.session_state.clearance_level}</strong>."
            "</div>",
            unsafe_allow_html=True,
        )
