"""Session state management for the Requirements Gathering Tool."""

import streamlit as st

# Phase definitions
PHASES = {
    1: {"name": "Authentication", "icon": "🔐", "description": "PKI Certificate Verification"},
    2: {"name": "Project Type", "icon": "📋", "description": "Orientation & Category Selection"},
    3: {"name": "Requirements", "icon": "📝", "description": "Detailed Requirements Elicitation"},
    4: {"name": "Data Analysis", "icon": "📊", "description": "Sample Data Review & Feasibility"},
    5: {"name": "Jira Matching", "icon": "🔍", "description": "Historical Project Matching"},
    6: {"name": "Scope & Timeline", "icon": "📄", "description": "Final Scope Document Generation"},
}


def init_session_state():
    """Initialize all session state variables with defaults."""
    defaults = {
        # Navigation
        "current_phase": 1,
        "max_unlocked_phase": 1,
        # Phase 1: Auth
        "authenticated": False,
        "user_name": "",
        "clearance_level": "",
        "cert_uploaded": False,
        # Phase 2: Project Type
        "selected_categories": [],
        "problem_description": "",
        # Phase 3: Requirements
        "requirements": {
            "business_problem": "",
            "success_criteria": "",
            "end_users": "",
            "data_availability": "",
            "data_classification": "",
            "data_volume": "",
            "constraints_deadline": "",
            "constraints_compliance": [],
            "hosting_environment": "",
            "integration_needs": "",
            "delivery_format": "",
            "stakeholders_approver": "",
            "stakeholders_users": "",
            "stakeholders_maintainer": "",
            "priority_level": "",
        },
        # Phase 4: Data Analysis
        "uploaded_data": None,
        "data_analysis_results": None,
        # Phase 5: Jira
        "jira_matches": [],
        "selected_match": None,
        "match_feedback": "",
        # Phase 6: Scope
        "scope_document": None,
        # AI / Ollama Configuration
        "ollama_url": "http://localhost:11434",
        "ollama_model": "",
        "ai_chat_history": [],
        # AI-generated scope fields
        "ai_project_title": "",
        "ai_project_summary": "",
        "ai_methodology": "",
        "ai_timeline": "",
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def advance_phase():
    """Move to the next phase if not already at the last."""
    if st.session_state.current_phase < 6:
        st.session_state.current_phase += 1
        st.session_state.max_unlocked_phase = max(
            st.session_state.max_unlocked_phase, st.session_state.current_phase
        )


def go_to_phase(phase: int):
    """Navigate to a specific phase if it's unlocked."""
    if 1 <= phase <= st.session_state.max_unlocked_phase:
        st.session_state.current_phase = phase
