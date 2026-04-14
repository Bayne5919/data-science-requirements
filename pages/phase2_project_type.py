"""Phase 2: Project Type Orientation."""

import streamlit as st
from utils.state import advance_phase

# Data science project categories with government-relevant examples
PROJECT_CATEGORIES = {
    "Classification": {
        "icon": "🏷️",
        "description": "Automatically assign items to predefined categories.",
        "examples": [
            "Categorizing incoming documents by sensitivity level",
            "Flagging anomalous network traffic",
            "Triaging support tickets by urgency",
        ],
    },
    "Numeric Prediction (Regression)": {
        "icon": "📈",
        "description": "Predict a continuous numeric value based on input data.",
        "examples": [
            "Forecasting equipment maintenance costs",
            "Estimating processing times for applications",
            "Predicting staffing needs by office",
        ],
    },
    "Time Series Forecasting": {
        "icon": "📅",
        "description": "Predict future values based on historical time-ordered data.",
        "examples": [
            "Predicting resource demand over the next quarter",
            "Budget trend analysis and projection",
            "Personnel attrition forecasting",
        ],
    },
    "LLM Integrations": {
        "icon": "🤖",
        "description": "Leverage large language models for text understanding and generation.",
        "examples": [
            "Document summarization for leadership briefs",
            "Policy Q&A assistants",
            "Automated report generation from structured data",
        ],
    },
    "Clustering / Segmentation": {
        "icon": "🔗",
        "description": "Discover natural groupings in data without predefined labels.",
        "examples": [
            "Grouping similar cases for workload balancing",
            "Identifying patterns in operational data",
            "Segmenting user behavior for service improvement",
        ],
    },
    "Computer Vision": {
        "icon": "👁️",
        "description": "Extract information from images, video, or scanned documents.",
        "examples": [
            "Satellite imagery analysis",
            "Document OCR and field extraction",
            "Facility inspection image review",
        ],
    },
    "Recommendation Systems": {
        "icon": "🎯",
        "description": "Suggest the most relevant items based on patterns and preferences.",
        "examples": [
            "Matching personnel to training opportunities",
            "Suggesting relevant policies or precedents",
            "Recommending subject matter experts for a given topic",
        ],
    },
}


def render():
    """Render the project type orientation phase."""
    st.markdown(
        '<div class="gov-card">'
        "<h3>Phase 2 — Project Type Orientation</h3>"
        "<p>Data science projects generally fall into a set of well-understood "
        "categories. Selecting the right category helps us scope your initiative "
        "accurately. Review the options below and select all that apply.</p>"
        "</div>",
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="gov-alert-info">'
        "<strong>Not sure which to pick?</strong> Describe the problem you're trying "
        "to solve in the text box at the bottom, and we can recommend categories."
        "</div>",
        unsafe_allow_html=True,
    )

    # --- Category Selection ---
    st.subheader("Select Project Categories")

    selected = list(st.session_state.selected_categories)

    for cat_name, cat_info in PROJECT_CATEGORIES.items():
        checked = st.checkbox(
            f"{cat_info['icon']}  **{cat_name}**",
            value=cat_name in selected,
            key=f"cat_{cat_name}",
        )
        st.caption(cat_info["description"])
        with st.expander("See government-relevant examples"):
            for ex in cat_info["examples"]:
                st.markdown(f"- {ex}")

        if checked and cat_name not in selected:
            selected.append(cat_name)
        elif not checked and cat_name in selected:
            selected.remove(cat_name)

    st.session_state.selected_categories = selected

    st.divider()

    # --- Free-text Problem Description ---
    st.subheader("Describe Your Problem (Optional)")
    problem_desc = st.text_area(
        "If you're unsure which categories apply, describe the problem you're "
        "trying to solve and we'll help match it.",
        value=st.session_state.problem_description,
        height=120,
        placeholder="e.g., We need to reduce the time analysts spend reading through "
        "hundreds of policy documents each week...",
    )
    st.session_state.problem_description = problem_desc

    st.divider()

    # --- Summary & Continue ---
    if selected:
        st.markdown(
            '<div class="gov-alert-success">'
            f"<strong>Selected categories ({len(selected)}):</strong> "
            f"{', '.join(selected)}"
            "</div>",
            unsafe_allow_html=True,
        )

    can_proceed = len(selected) > 0 or len(problem_desc.strip()) > 0
    if st.button("Continue to Requirements", disabled=not can_proceed, use_container_width=True):
        advance_phase()
        st.rerun()

    if not can_proceed:
        st.caption("Select at least one category or describe your problem to proceed.")
