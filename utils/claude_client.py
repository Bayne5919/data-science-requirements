"""Claude API client for AI-assisted requirements gathering."""

import os
import anthropic
import streamlit as st

MODEL = "claude-sonnet-4-20250514"

REQUIREMENTS_SYSTEM_PROMPT = """\
You are a senior data science requirements analyst working with U.S. government agencies. \
Your role is to help project requestors clearly articulate their data science project needs.

You have access to the following context about the current project intake:

{context}

Your job:
- Ask targeted follow-up questions to help the user clarify vague or incomplete requirements.
- Suggest concrete success criteria, metrics, and acceptance thresholds when the user struggles.
- Point out potential gaps (data access, compliance, stakeholder buy-in) they may not have considered.
- Keep responses concise and actionable — this is a government intake process, not a brainstorm.
- Reference the specific form fields (business problem, end users, success criteria, etc.) \
so the user knows exactly what to update.

Do NOT generate entire scope documents here — that happens in a later phase. \
Focus on helping the user fill out the requirements form completely and precisely.\
"""

SCOPE_SYSTEM_PROMPT = """\
You are a senior data science project scoping analyst for U.S. government agencies. \
Generate professional, concise content for project scope documents.

Project context:
{context}

Write in a formal but readable government style. Be specific and actionable. \
Do not use marketing language or filler. Ground recommendations in the actual \
project details provided.\
"""


def get_api_key() -> str | None:
    """Get the API key from environment or session state."""
    return os.environ.get("ANTHROPIC_API_KEY") or st.session_state.get("api_key") or None


def is_configured() -> bool:
    """Check if a Claude API key is available."""
    key = get_api_key()
    return bool(key and key.strip())


def get_client() -> anthropic.Anthropic:
    """Return an Anthropic client using the available API key."""
    key = get_api_key()
    if not key:
        raise ValueError("No API key configured.")
    return anthropic.Anthropic(api_key=key.strip())


def build_project_context() -> str:
    """Build a text summary of all collected project info for use in prompts."""
    parts = []

    # Phase 1: User info
    if st.session_state.get("user_name"):
        parts.append(f"Requestor: {st.session_state.user_name}")
    if st.session_state.get("clearance_level"):
        parts.append(f"Clearance level: {st.session_state.clearance_level}")

    # Phase 2: Project categories
    cats = st.session_state.get("selected_categories", [])
    if cats:
        parts.append(f"Project type(s): {', '.join(cats)}")
    desc = st.session_state.get("problem_description", "")
    if desc:
        parts.append(f"Initial problem description: {desc}")

    # Phase 3: Requirements
    reqs = st.session_state.get("requirements", {})
    field_labels = {
        "business_problem": "Business problem",
        "end_users": "End users",
        "success_criteria": "Success criteria",
        "data_availability": "Data availability",
        "data_classification": "Data classification",
        "data_volume": "Data volume",
        "constraints_deadline": "Deadline",
        "constraints_compliance": "Compliance frameworks",
        "hosting_environment": "Hosting environment",
        "integration_needs": "Integration needs",
        "delivery_format": "Delivery format",
        "stakeholders_approver": "Approving authority",
        "stakeholders_users": "Primary users",
        "stakeholders_maintainer": "Long-term maintainer",
        "priority_level": "Priority level",
    }
    for key, label in field_labels.items():
        val = reqs.get(key, "")
        if isinstance(val, list):
            val = ", ".join(val) if val else ""
        if val:
            parts.append(f"{label}: {val}")

    # Phase 4: Data upload info
    uploaded = st.session_state.get("uploaded_data")
    if uploaded:
        parts.append(f"Sample data uploaded: {uploaded.name} ({uploaded.size / 1024:.1f} KB)")

    # Phase 5: Reference project
    match = st.session_state.get("selected_match")
    if match:
        parts.append(
            f"Reference project: {match['key']} — {match['title']} "
            f"(similarity: {match['similarity']}%, duration: {match['duration']}, "
            f"stack: {match['tech_stack']})"
        )
    feedback = st.session_state.get("match_feedback", "")
    if feedback:
        parts.append(f"Adjustments from reference: {feedback}")

    return "\n".join(parts) if parts else "No project information collected yet."


def chat_requirements(messages: list[dict]) -> str:
    """Send a chat to Claude for requirements assistance. Returns assistant text."""
    client = get_client()
    context = build_project_context()
    system = REQUIREMENTS_SYSTEM_PROMPT.format(context=context)

    response = client.messages.create(
        model=MODEL,
        max_tokens=1024,
        system=system,
        messages=messages,
    )
    return response.content[0].text


def generate_scope_section(section: str) -> str:
    """Generate a specific scope document section using Claude.

    section: one of "title_summary", "methodology", "timeline"
    """
    client = get_client()
    context = build_project_context()
    system = SCOPE_SYSTEM_PROMPT.format(context=context)

    prompts = {
        "title_summary": (
            "Generate a concise project title and a 2-3 sentence executive summary "
            "for this data science project. Format as:\n\n"
            "Title: <title>\n\nSummary: <summary>"
        ),
        "methodology": (
            "Recommend a methodology and technical approach for this project. "
            "Include: recommended algorithms/techniques, development methodology "
            "(agile, iterative, etc.), key milestones, and any technical risks. "
            "Keep it to one concise paragraph."
        ),
        "timeline": (
            "Estimate a realistic timeline for this project broken into phases: "
            "Discovery & Planning, Development & Testing, Deployment & Handoff. "
            "For each phase give a week range and key activities. "
            "Consider the project type, complexity, data readiness, and hosting environment. "
            "End with a total estimated range."
        ),
    }

    if section not in prompts:
        raise ValueError(f"Unknown section: {section}")

    response = client.messages.create(
        model=MODEL,
        max_tokens=1024,
        system=system,
        messages=[{"role": "user", "content": prompts[section]}],
    )
    return response.content[0].text
