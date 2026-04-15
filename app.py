"""
Data Science Requirements Gathering Tool
=========================================
A structured intake application for government data science projects.
Guides customers through authentication, project scoping, data analysis,
historical project matching, and scope document generation.
"""

import streamlit as st

# Must be the first Streamlit command
st.set_page_config(
    page_title="DS Requirements Tool",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded",
)

from utils.state import PHASES, init_session_state, go_to_phase
from utils.styles import get_custom_css
from pages import phase1_auth, phase2_project_type, phase3_requirements
from pages import phase4_data_analysis, phase5_jira_matching, phase6_scope

# --- Initialize State & Styles ---
init_session_state()
st.markdown(get_custom_css(), unsafe_allow_html=True)

# --- Header Banner ---
st.markdown(
    '<div class="gov-banner">'
    "<h1>🏛️ Data Science Requirements Gathering Tool</h1>"
    "<p>Structured intake for government data science initiatives</p>"
    "</div>",
    unsafe_allow_html=True,
)

# --- Phase Progress Tracker ---
phase_html = '<div class="phase-tracker">'
for phase_num, phase_info in PHASES.items():
    if phase_num == st.session_state.current_phase:
        css_class = "active"
    elif phase_num < st.session_state.current_phase:
        css_class = "completed"
    elif phase_num <= st.session_state.max_unlocked_phase:
        css_class = ""
    else:
        css_class = "locked"
    phase_html += (
        f'<div class="phase-step {css_class}">'
        f"{phase_info['icon']} {phase_info['name']}"
        f"</div>"
    )
phase_html += "</div>"
st.markdown(phase_html, unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.markdown("## Navigation")
    for phase_num, phase_info in PHASES.items():
        is_unlocked = phase_num <= st.session_state.max_unlocked_phase
        is_current = phase_num == st.session_state.current_phase

        label = f"{phase_info['icon']}  Phase {phase_num}: {phase_info['name']}"
        if is_current:
            label = f"▸ {label}"

        if is_unlocked:
            if st.button(
                label,
                key=f"nav_{phase_num}",
                use_container_width=True,
                disabled=is_current,
            ):
                go_to_phase(phase_num)
                st.rerun()
        else:
            st.button(
                f"🔒  Phase {phase_num}: {phase_info['name']}",
                key=f"nav_{phase_num}",
                use_container_width=True,
                disabled=True,
            )

    st.divider()

    # Session info
    st.markdown("## Session Info")
    if st.session_state.authenticated:
        st.markdown(f"**User:** {st.session_state.user_name}")
        st.markdown(f"**Clearance:** {st.session_state.clearance_level}")
    else:
        st.caption("Not yet authenticated.")

    st.divider()

    # AI / Ollama Configuration
    st.markdown("## AI Assistant")
    from utils.llm_client import get_available_models, is_configured

    ollama_url = st.text_input(
        "Ollama URL",
        value=st.session_state.ollama_url,
        placeholder="http://localhost:11434",
        help="Address of your local Ollama instance.",
    )
    if ollama_url != st.session_state.ollama_url:
        st.session_state.ollama_url = ollama_url

    models = get_available_models()
    if models:
        current_model = st.session_state.ollama_model
        idx = models.index(current_model) if current_model in models else 0
        selected_model = st.selectbox("Model", options=models, index=idx)
        if selected_model != st.session_state.ollama_model:
            st.session_state.ollama_model = selected_model
    else:
        st.session_state.ollama_model = ""
        st.caption("No models found. Is Ollama running?")

    if is_configured():
        st.markdown(
            '<span style="color:#2e8540;">● Connected</span>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<span style="color:#e5a000;">● Not connected</span>',
            unsafe_allow_html=True,
        )

    st.divider()
    st.caption(
        "Data Science Requirements Gathering Tool v0.1.0\n\n"
        "For official use only."
    )

# --- Render Current Phase ---
PHASE_RENDERERS = {
    1: phase1_auth.render,
    2: phase2_project_type.render,
    3: phase3_requirements.render,
    4: phase4_data_analysis.render,
    5: phase5_jira_matching.render,
    6: phase6_scope.render,
}

current = st.session_state.current_phase
st.markdown(f"**Phase {current} of 6** — {PHASES[current]['description']}")
st.divider()
PHASE_RENDERERS[current]()
