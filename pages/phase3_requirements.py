"""Phase 3: Requirements Elicitation — Conversational AI Interface."""

import streamlit as st
from utils.state import advance_phase
from utils.llm_client import is_configured, chat_requirements, extract_requirements_from_chat


OPENING_MESSAGE = (
    "Hi! I'm here to help define your data science project requirements. "
    "Let's start with the big picture — **what problem are you trying to solve, "
    "and what decision or outcome will this project support?**"
)

# All trackable requirement fields with display labels
FIELD_LABELS = {
    "business_problem": "Business Problem",
    "end_users": "End Users",
    "success_criteria": "Success Criteria",
    "data_availability": "Data Availability",
    "data_classification": "Data Classification",
    "data_volume": "Data Volume",
    "constraints_deadline": "Deadline",
    "constraints_compliance": "Compliance",
    "hosting_environment": "Hosting",
    "integration_needs": "Integration",
    "delivery_format": "Delivery Format",
    "stakeholders_approver": "Approver",
    "stakeholders_users": "Users",
    "stakeholders_maintainer": "Maintainer",
    "priority_level": "Priority",
}


def _field_has_value(val) -> bool:
    """Check if a requirements field has a meaningful value."""
    if isinstance(val, list):
        return len(val) > 0
    if isinstance(val, str):
        return bool(val.strip())
    return bool(val)


def _count_filled(reqs: dict) -> tuple[int, int]:
    """Count how many total trackable fields are filled."""
    filled = sum(1 for key in FIELD_LABELS if _field_has_value(reqs.get(key, "")))
    return filled, len(FIELD_LABELS)


def _merge_extracted(reqs: dict, extracted: dict) -> dict:
    """Merge extracted values into requirements, only overwriting empty fields
    or updating with non-empty values."""
    for key, val in extracted.items():
        if key in reqs and val:
            # For list fields, don't overwrite with empty
            if isinstance(val, list) and not val:
                continue
            if isinstance(val, str) and not val.strip():
                continue
            reqs[key] = val
    return reqs


def render():
    """Render the conversational requirements elicitation phase."""
    reqs = st.session_state.requirements
    filled, total = _count_filled(reqs)

    st.markdown(
        '<div class="gov-card">'
        "<h3>Phase 3 — Requirements Elicitation</h3>"
        "<p>Have a conversation with the AI assistant about your project. "
        "Requirements are automatically extracted after each response.</p>"
        "</div>",
        unsafe_allow_html=True,
    )

    if not is_configured():
        st.warning(
            "Connect to Ollama in the sidebar to use the AI requirements assistant. "
            "Select a model and ensure Ollama is running."
        )
        _render_manual_fallback()
        return

    # --- Layout: chat on left, requirements tracker on right ---
    chat_col, tracker_col = st.columns([3, 1])

    with tracker_col:
        st.markdown("#### 📋 Requirements")
        st.caption(f"**{filled} / {total}** captured")

        # Progress bar
        st.progress(filled / total if total > 0 else 0)

        # Field status list
        for key, label in FIELD_LABELS.items():
            val = reqs.get(key, "")
            has_val = _field_has_value(val)
            icon = "✅" if has_val else "⬜"
            if has_val:
                display_val = ", ".join(val) if isinstance(val, list) else val
                # Truncate long values for the sidebar
                if len(display_val) > 60:
                    display_val = display_val[:57] + "..."
                st.markdown(f"{icon} **{label}**")
                st.caption(display_val)
            else:
                st.markdown(f"{icon} {label}")

    with chat_col:
        # --- Seed the conversation with an opening message ---
        if not st.session_state.ai_chat_history:
            st.session_state.ai_chat_history.append(
                {"role": "assistant", "content": OPENING_MESSAGE}
            )

        # --- Chat display ---
        for msg in st.session_state.ai_chat_history:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        # --- Chat input ---
        if user_input := st.chat_input("Tell me about your project..."):
            # Add user message
            st.session_state.ai_chat_history.append(
                {"role": "user", "content": user_input}
            )
            with st.chat_message("user"):
                st.markdown(user_input)

            # Get AI response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    try:
                        response = chat_requirements(
                            st.session_state.ai_chat_history
                        )
                        st.markdown(response)
                        st.session_state.ai_chat_history.append(
                            {"role": "assistant", "content": response}
                        )
                    except Exception as e:
                        st.error(f"Error communicating with Ollama: {e}")

            # --- Auto-extract after every user message ---
            with st.spinner("Extracting requirements..."):
                try:
                    extracted = extract_requirements_from_chat(
                        st.session_state.ai_chat_history
                    )
                    if extracted:
                        st.session_state.requirements = _merge_extracted(reqs, extracted)
                except Exception:
                    pass  # Extraction failed silently — user can keep chatting

            st.rerun()  # Refresh to update the tracker panel

    st.divider()

    # --- Completeness status and navigation ---
    # Re-count after potential extraction
    filled, total = _count_filled(st.session_state.requirements)

    if filled < total:
        missing = [
            label for key, label in FIELD_LABELS.items()
            if not _field_has_value(st.session_state.requirements.get(key, ""))
        ]
        st.markdown(
            f'<div class="gov-alert-warning">'
            f"<strong>{filled}/{total} requirements captured.</strong> "
            f"Still needed: {', '.join(missing[:5])}"
            f"{'...' if len(missing) > 5 else ''}"
            f"</div>",
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<div class="gov-alert-success">'
            "<strong>All requirements captured!</strong> "
            "Review the extracted fields in the panel on the right, then proceed."
            "</div>",
            unsafe_allow_html=True,
        )

    # Show proceed button — always visible but styled differently based on completeness
    if filled == total:
        if st.button(
            "✅ All Requirements Captured — Proceed to Data Analysis",
            use_container_width=True,
            type="primary",
        ):
            advance_phase()
            st.rerun()
    else:
        if st.button(
            f"Proceed to Data Analysis ({filled}/{total} captured)",
            use_container_width=True,
            help="You can proceed at any time, but some fields are still missing.",
        ):
            advance_phase()
            st.rerun()


def _render_manual_fallback():
    """Render a minimal manual form when Ollama is not available."""
    st.divider()
    st.markdown(
        '<div class="gov-alert-info">'
        "Ollama is not connected. You can fill in the core requirements manually below."
        "</div>",
        unsafe_allow_html=True,
    )

    reqs = st.session_state.requirements

    reqs["business_problem"] = st.text_area(
        "What decision or outcome is this project supporting? *",
        value=reqs["business_problem"],
        height=100,
    )
    reqs["end_users"] = st.text_input(
        "Who are the primary end users? *",
        value=reqs["end_users"],
    )
    reqs["success_criteria"] = st.text_area(
        "How will you know this project succeeded? *",
        value=reqs["success_criteria"],
        height=100,
    )

    st.session_state.requirements = reqs

    st.divider()

    required = ["business_problem", "end_users", "success_criteria"]
    filled = sum(1 for f in required if reqs.get(f, "").strip())
    can_proceed = filled == len(required)
    if st.button("Continue to Data Analysis", disabled=not can_proceed, use_container_width=True):
        advance_phase()
        st.rerun()
