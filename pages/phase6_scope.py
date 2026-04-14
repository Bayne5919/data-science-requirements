"""Phase 6: Scope & Timeline Output."""

import streamlit as st
from datetime import date
from utils.claude_client import is_configured, generate_scope_section


def render():
    """Render the scope and timeline output phase."""
    st.markdown(
        '<div class="gov-card">'
        "<h3>Phase 6 — Project Scope & Timeline</h3>"
        "<p>Review the compiled scope document below. This synthesizes your "
        "requirements, data analysis, and historical project matches into a "
        "formal project definition. You can edit sections before exporting.</p>"
        "</div>",
        unsafe_allow_html=True,
    )

    reqs = st.session_state.requirements
    categories = st.session_state.selected_categories
    match = st.session_state.selected_match

    # ── 1. Project Title & Summary ──
    st.subheader("1. Project Title & Summary")
    if is_configured():
        if st.button("Generate Title & Summary with AI", key="ai_title"):
            with st.spinner("Generating..."):
                try:
                    result = generate_scope_section("title_summary")
                    for line in result.split("\n"):
                        line = line.strip()
                        if line.lower().startswith("title:"):
                            st.session_state.ai_project_title = line.split(":", 1)[1].strip()
                        elif line.lower().startswith("summary:"):
                            st.session_state.ai_project_summary = line.split(":", 1)[1].strip()
                    if not st.session_state.ai_project_title:
                        st.session_state.ai_project_title = result.split("\n")[0]
                    if not st.session_state.ai_project_summary:
                        st.session_state.ai_project_summary = result
                    st.rerun()
                except Exception as e:
                    st.error(f"AI error: {e}")

    project_title = st.text_input(
        "Project title",
        value=st.session_state.ai_project_title,
        placeholder="e.g., Automated Document Triage System",
    )
    project_summary = st.text_area(
        "Executive summary",
        value=st.session_state.ai_project_summary,
        height=80,
        placeholder="A brief 2-3 sentence summary of the project...",
    )

    st.divider()

    # ── 2. Problem Statement & Objectives ──
    st.subheader("2. Problem Statement & Objectives")
    st.markdown(f"**Business Problem:** {reqs['business_problem'] or '*Not provided*'}")
    st.markdown(f"**End Users:** {reqs['end_users'] or '*Not provided*'}")
    st.markdown(f"**Success Criteria:** {reqs['success_criteria'] or '*Not provided*'}")

    st.divider()

    # ── 3. Proposed Approach ──
    st.subheader("3. Proposed Approach")
    if categories:
        st.markdown(f"**Project Type(s):** {', '.join(categories)}")
    else:
        st.markdown("**Project Type(s):** *Not selected*")

    if is_configured():
        if st.button("Generate Methodology with AI", key="ai_method"):
            with st.spinner("Generating..."):
                try:
                    st.session_state.ai_methodology = generate_scope_section("methodology")
                    st.rerun()
                except Exception as e:
                    st.error(f"AI error: {e}")

    methodology = st.text_area(
        "Methodology notes (optional)",
        value=st.session_state.ai_methodology,
        height=80,
        placeholder="e.g., Iterative development with bi-weekly stakeholder reviews; "
        "start with baseline model, then refine...",
    )

    st.divider()

    # ── 4. Data Overview ──
    st.subheader("4. Data Overview")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**Availability:** {reqs['data_availability'] or '*Not specified*'}")
        st.markdown(f"**Classification:** {reqs['data_classification'] or '*Not specified*'}")
    with col2:
        st.markdown(f"**Volume:** {reqs['data_volume'] or '*Not specified*'}")
        if st.session_state.uploaded_data:
            st.markdown(f"**Sample uploaded:** {st.session_state.uploaded_data.name}")
        else:
            st.markdown("**Sample uploaded:** None")

    st.divider()

    # ── 5. Deliverables ──
    st.subheader("5. Deliverables")
    st.markdown(f"**Delivery Format:** {reqs['delivery_format'] or '*Not specified*'}")
    st.markdown(f"**Integration Points:** {reqs['integration_needs'] or '*Not specified*'}")
    deliverables_notes = st.text_area(
        "Additional deliverables or documentation requirements",
        height=60,
        placeholder="e.g., Model documentation, user guide, training session for analysts...",
    )

    st.divider()

    # ── 6. Success Metrics ──
    st.subheader("6. Success Metrics")
    st.markdown(reqs["success_criteria"] or "*Defined in Section 2 above.*")

    st.divider()

    # ── 7. Constraints & Assumptions ──
    st.subheader("7. Constraints & Assumptions")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**Deadline:** {reqs['constraints_deadline'] or '*No deadline specified*'}")
        st.markdown(f"**Hosting:** {reqs['hosting_environment'] or '*Not specified*'}")
    with col2:
        compliance = ", ".join(reqs["constraints_compliance"]) if reqs["constraints_compliance"] else "*None selected*"
        st.markdown(f"**Compliance:** {compliance}")
        st.markdown(f"**Priority:** {reqs['priority_level'] or '*Not specified*'}")

    st.divider()

    # ── 8. Similar Prior Work ──
    st.subheader("8. Similar Prior Work")
    if match:
        st.markdown(
            f"**Reference Project:** {match['key']} — {match['title']}\n\n"
            f"{match['summary']}\n\n"
            f"*Duration: {match['duration']} | Stack: {match['tech_stack']}*"
        )
    else:
        st.markdown("*No reference project selected.*")

    st.divider()

    # ── 9. Required Adjustments ──
    st.subheader("9. Required Adjustments from Reference")
    st.markdown(st.session_state.match_feedback or "*No adjustments noted.*")

    st.divider()

    # ── 10. Timeline Estimate ──
    st.subheader("10. Rough Timeline Estimate")
    st.markdown(
        '<div class="gov-alert-warning">'
        "<strong>Timeline Disclaimer:</strong> This estimate reflects elapsed time "
        "<em>after</em> the project is formally started and resourced. Actual duration "
        "may vary based on priority level, team availability, data access approvals, "
        "security reviews, and ATO requirements. Higher priority projects may receive "
        "dedicated resources; lower priority projects may experience delays due to "
        "competing demands."
        "</div>",
        unsafe_allow_html=True,
    )

    if is_configured():
        if st.button("Generate Timeline with AI", key="ai_timeline"):
            with st.spinner("Generating..."):
                try:
                    st.session_state.ai_timeline = generate_scope_section("timeline")
                    st.rerun()
                except Exception as e:
                    st.error(f"AI error: {e}")

    if st.session_state.ai_timeline:
        st.markdown(st.session_state.ai_timeline)
    else:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Discovery & Planning", "2–3 weeks")
        with col2:
            st.metric("Development & Testing", "8–12 weeks")
        with col3:
            st.metric("Deployment & Handoff", "2–4 weeks")

        st.caption("Total estimated range: **12–19 weeks** (placeholder — click Generate above for AI estimate)")

    st.divider()

    # ── 11. Open Questions / Next Steps ──
    st.subheader("11. Open Questions & Next Steps")
    open_questions = st.text_area(
        "Capture any open questions or immediate next steps",
        height=100,
        placeholder="e.g., Need to confirm data access with IT security; schedule demo "
        "of reference project with stakeholders...",
    )

    st.divider()

    # ── Export Actions ──
    st.subheader("Export Scope Document")
    st.markdown(
        '<div class="gov-alert-info">'
        "Export functionality will generate a formatted document containing all "
        "sections above. Choose your preferred format below."
        "</div>",
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        st.button("Export as Word (.docx)", use_container_width=True, disabled=True)
    with col2:
        st.button("Export as PDF", use_container_width=True, disabled=True)
    with col3:
        st.button("Export as Markdown", use_container_width=True, disabled=True)

    st.caption("Export functionality is not yet implemented.")

    # --- Footer ---
    st.markdown(
        '<div class="gov-footer">'
        f"Scope document generated on {date.today().strftime('%B %d, %Y')}. "
        "This document is a draft and does not constitute a binding commitment."
        "</div>",
        unsafe_allow_html=True,
    )
