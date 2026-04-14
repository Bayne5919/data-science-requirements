"""Phase 4: Sample Data Analysis."""

import streamlit as st
from utils.state import advance_phase


def render():
    """Render the sample data analysis phase."""
    st.markdown(
        '<div class="gov-card">'
        "<h3>Phase 4 — Sample Data Analysis</h3>"
        "<p>If you have sample data available, upload it here for an initial "
        "feasibility assessment. We'll examine structure, quality, and volume to "
        "inform project scoping. This step is optional — you can skip ahead if "
        "data isn't available yet.</p>"
        "</div>",
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="gov-alert-warning">'
        "<strong>Classification reminder:</strong> Only upload data at or below "
        f"your authorized level (<strong>{st.session_state.clearance_level or 'Not set'}</strong>). "
        "Do not upload classified data to this system unless the hosting environment "
        "has been approved for that classification level."
        "</div>",
        unsafe_allow_html=True,
    )

    # --- File Upload ---
    st.subheader("Upload Sample Data")
    uploaded_file = st.file_uploader(
        "Select a data file to analyze",
        type=["csv", "xlsx", "xls", "json", "parquet", "tsv"],
        help="Supported formats: CSV, Excel, JSON, Parquet, TSV",
    )

    if uploaded_file is not None:
        st.session_state.uploaded_data = uploaded_file

        st.markdown(
            '<div class="gov-alert-success">'
            f"<strong>File received:</strong> {uploaded_file.name} "
            f"({uploaded_file.size / 1024:.1f} KB)"
            "</div>",
            unsafe_allow_html=True,
        )

        # --- Placeholder Analysis Results ---
        # TODO: Implement actual data profiling (pandas profiling, shape, dtypes, nulls, etc.)
        st.subheader("Preliminary Analysis")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("File Size", f"{uploaded_file.size / 1024:.1f} KB")
        with col2:
            st.metric("Format", uploaded_file.name.split(".")[-1].upper())
        with col3:
            st.metric("Status", "Pending Analysis")

        st.info(
            "**Data profiling not yet implemented.** When connected, this section will show:\n"
            "- Row and column counts\n"
            "- Data types per column\n"
            "- Missing value percentages\n"
            "- Class distribution (for classification projects)\n"
            "- Time range (for time series projects)\n"
            "- Basic statistical summaries\n"
            "- Data quality flags and recommendations"
        )

    else:
        st.markdown(
            '<div class="gov-alert-info">'
            "No data uploaded yet. You can upload a sample file above, or skip "
            "this step and proceed to Jira project matching."
            "</div>",
            unsafe_allow_html=True,
        )

    st.divider()

    # --- Navigation ---
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Skip — Continue without data", use_container_width=True):
            advance_phase()
            st.rerun()
    with col2:
        if uploaded_file and st.button(
            "Continue with analysis", use_container_width=True
        ):
            advance_phase()
            st.rerun()
