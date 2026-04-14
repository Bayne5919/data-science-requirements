"""Phase 5: Jira Project Matching."""

import streamlit as st
from utils.state import advance_phase

# Placeholder historical projects for demonstration
SAMPLE_MATCHES = [
    {
        "key": "DS-1042",
        "title": "Document Classification Pipeline — Agency X",
        "status": "Completed",
        "similarity": 87,
        "summary": "Built a multi-label classification model to categorize incoming "
        "correspondence by topic and urgency for a federal agency's intake office.",
        "tech_stack": "Python, scikit-learn, FastAPI, PostgreSQL",
        "duration": "14 weeks",
    },
    {
        "key": "DS-0987",
        "title": "NLP-Powered Policy Search — Agency Y",
        "status": "Completed",
        "similarity": 72,
        "summary": "Developed a retrieval-augmented generation (RAG) system for searching "
        "and summarizing internal policy documents using an LLM.",
        "tech_stack": "Python, LangChain, OpenAI API, Elasticsearch",
        "duration": "18 weeks",
    },
    {
        "key": "DS-1103",
        "title": "Attrition Forecasting Model — Agency Z",
        "status": "In Progress",
        "similarity": 54,
        "summary": "Time series forecasting model to predict personnel attrition rates "
        "by directorate, enabling proactive recruitment planning.",
        "tech_stack": "Python, Prophet, Streamlit, Snowflake",
        "duration": "10 weeks (estimated)",
    },
]


def render():
    """Render the Jira project matching phase."""
    st.markdown(
        '<div class="gov-card">'
        "<h3>Phase 5 — Historical Project Matching</h3>"
        "<p>Based on your requirements, we search for similar past and active "
        "projects on our Jira board. Reviewing comparable work helps refine your "
        "scope and gives realistic timeline benchmarks.</p>"
        "</div>",
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="gov-alert-info">'
        "<strong>Note:</strong> Only projects within your authorized access level "
        f"(<strong>{st.session_state.clearance_level or 'Not set'}</strong>) are displayed."
        "</div>",
        unsafe_allow_html=True,
    )

    # --- Search / Match Button ---
    st.subheader("Search for Similar Projects")

    if st.button("Search Jira Board", use_container_width=True):
        # TODO: Replace with actual Jira API integration
        with st.spinner("Searching historical projects..."):
            import time
            time.sleep(1)  # Simulate search delay
            st.session_state.jira_matches = SAMPLE_MATCHES

    # --- Display Matches ---
    if st.session_state.jira_matches:
        st.subheader(f"Found {len(st.session_state.jira_matches)} Similar Projects")

        for i, match in enumerate(st.session_state.jira_matches):
            with st.container():
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.markdown(f"**{match['key']}** — {match['title']}")
                with col2:
                    st.metric("Similarity", f"{match['similarity']}%")

                st.caption(f"Status: {match['status']}  |  Duration: {match['duration']}  |  Stack: {match['tech_stack']}")
                st.markdown(match["summary"])

                if st.button(f"Select this as reference", key=f"select_match_{i}"):
                    st.session_state.selected_match = match

                st.divider()

        # --- Feedback on Selected Match ---
        if st.session_state.selected_match:
            st.markdown(
                '<div class="gov-alert-success">'
                f"<strong>Selected reference project:</strong> "
                f"{st.session_state.selected_match['key']} — "
                f"{st.session_state.selected_match['title']}"
                "</div>",
                unsafe_allow_html=True,
            )

            st.session_state.match_feedback = st.text_area(
                "What would need to change from this reference project to fit your needs?",
                value=st.session_state.match_feedback,
                height=100,
                placeholder="e.g., We need it to handle classified data, the volume is "
                "much larger, we need a dashboard instead of an API...",
            )

    else:
        st.markdown(
            '<div class="gov-alert-info">'
            "Click <strong>Search Jira Board</strong> above to find similar historical "
            "projects. Results shown here are currently placeholder data for demonstration."
            "</div>",
            unsafe_allow_html=True,
        )

    st.divider()

    if st.button("Continue to Scope Document", use_container_width=True):
        advance_phase()
        st.rerun()
