"""Phase 3: Requirements Elicitation."""

import streamlit as st
from utils.state import advance_phase


def render():
    """Render the requirements elicitation phase."""
    st.markdown(
        '<div class="gov-card">'
        "<h3>Phase 3 — Requirements Elicitation</h3>"
        "<p>Help us understand your project needs in detail. Complete as many fields "
        "as you can — you can always come back and update them later. Fields marked "
        "with <strong>*</strong> are required to generate a scope document.</p>"
        "</div>",
        unsafe_allow_html=True,
    )

    reqs = st.session_state.requirements

    # ── Section 1: Business Problem ──
    st.subheader("Business Problem & Objectives")
    reqs["business_problem"] = st.text_area(
        "What decision or outcome is this project supporting? *",
        value=reqs["business_problem"],
        height=100,
        placeholder="e.g., Leadership needs a faster way to identify high-risk applications "
        "before they reach the review board...",
    )
    reqs["end_users"] = st.text_input(
        "Who are the primary end users? *",
        value=reqs["end_users"],
        placeholder="e.g., Program analysts in the Office of Risk Management",
    )

    st.divider()

    # ── Section 2: Success Criteria ──
    st.subheader("Success Criteria")
    reqs["success_criteria"] = st.text_area(
        "How will you know this project succeeded? What metrics matter? *",
        value=reqs["success_criteria"],
        height=100,
        placeholder="e.g., Reduce average document triage time from 4 hours to under 30 minutes; "
        "achieve at least 90% accuracy on classification...",
    )

    st.divider()

    # ── Section 3: Data Availability ──
    st.subheader("Data Availability")
    col1, col2 = st.columns(2)
    with col1:
        reqs["data_availability"] = st.selectbox(
            "Do you currently have data available?",
            options=["", "Yes — ready to share", "Yes — but needs preparation", "No — need to identify sources", "Unsure"],
            index=["", "Yes — ready to share", "Yes — but needs preparation", "No — need to identify sources", "Unsure"].index(reqs["data_availability"]) if reqs["data_availability"] else 0,
        )
        reqs["data_classification"] = st.selectbox(
            "Data classification level",
            options=["", "Unclassified", "CUI", "Secret", "Top Secret"],
            index=["", "Unclassified", "CUI", "Secret", "Top Secret"].index(reqs["data_classification"]) if reqs["data_classification"] else 0,
        )
    with col2:
        reqs["data_volume"] = st.text_input(
            "Approximate data volume",
            value=reqs["data_volume"],
            placeholder="e.g., ~50,000 records, 2 GB of PDFs",
        )

    st.divider()

    # ── Section 4: Constraints ──
    st.subheader("Constraints & Compliance")
    col1, col2 = st.columns(2)
    with col1:
        reqs["constraints_deadline"] = st.text_input(
            "Target deadline or milestone",
            value=reqs["constraints_deadline"],
            placeholder="e.g., Need initial results by Q3 FY2026",
        )
        reqs["hosting_environment"] = st.selectbox(
            "Hosting environment",
            options=["", "Cloud (FedRAMP authorized)", "On-premises", "Air-gapped", "Hybrid", "Unsure"],
            index=["", "Cloud (FedRAMP authorized)", "On-premises", "Air-gapped", "Hybrid", "Unsure"].index(reqs["hosting_environment"]) if reqs["hosting_environment"] else 0,
        )
    with col2:
        compliance_options = ["FedRAMP", "FISMA", "ATO Required", "HIPAA", "ITAR", "Section 508"]
        reqs["constraints_compliance"] = st.multiselect(
            "Applicable compliance frameworks",
            options=compliance_options,
            default=reqs["constraints_compliance"],
        )

    st.divider()

    # ── Section 5: Integration & Delivery ──
    st.subheader("Integration & Delivery")
    col1, col2 = st.columns(2)
    with col1:
        reqs["integration_needs"] = st.text_input(
            "Systems this must connect to",
            value=reqs["integration_needs"],
            placeholder="e.g., ServiceNow, agency data warehouse, Tableau",
        )
    with col2:
        reqs["delivery_format"] = st.selectbox(
            "Preferred delivery format",
            options=["", "Interactive dashboard", "REST API", "Periodic report", "Embedded model", "Standalone application", "Multiple / Other"],
            index=["", "Interactive dashboard", "REST API", "Periodic report", "Embedded model", "Standalone application", "Multiple / Other"].index(reqs["delivery_format"]) if reqs["delivery_format"] else 0,
        )

    st.divider()

    # ── Section 6: Stakeholders ──
    st.subheader("Stakeholders")
    col1, col2, col3 = st.columns(3)
    with col1:
        reqs["stakeholders_approver"] = st.text_input(
            "Approving authority",
            value=reqs["stakeholders_approver"],
            placeholder="Name / title",
        )
    with col2:
        reqs["stakeholders_users"] = st.text_input(
            "Primary users",
            value=reqs["stakeholders_users"],
            placeholder="Team / role",
        )
    with col3:
        reqs["stakeholders_maintainer"] = st.text_input(
            "Long-term maintainer",
            value=reqs["stakeholders_maintainer"],
            placeholder="Team / role",
        )

    st.divider()

    # ── Section 7: Priority ──
    st.subheader("Priority Level")
    reqs["priority_level"] = st.radio(
        "How would you characterize this initiative?",
        options=["Mission-critical", "Operational improvement", "Exploratory / R&D"],
        index=["Mission-critical", "Operational improvement", "Exploratory / R&D"].index(reqs["priority_level"]) if reqs["priority_level"] else 1,
        horizontal=True,
    )

    st.session_state.requirements = reqs

    st.divider()

    # ── Completeness Check ──
    required_fields = ["business_problem", "end_users", "success_criteria"]
    filled = sum(1 for f in required_fields if reqs[f].strip())
    total = len(required_fields)

    if filled < total:
        st.markdown(
            f'<div class="gov-alert-warning">'
            f"<strong>{filled}/{total} required fields completed.</strong> "
            f"Please fill in the remaining required fields (marked with *) to continue."
            f"</div>",
            unsafe_allow_html=True,
        )

    can_proceed = filled == total
    if st.button("Continue to Data Analysis", disabled=not can_proceed, use_container_width=True):
        advance_phase()
        st.rerun()
