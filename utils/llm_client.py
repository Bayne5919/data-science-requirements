"""Local LLM client for AI-assisted requirements gathering via Ollama."""

import json
import requests
import streamlit as st


DEFAULT_OLLAMA_URL = "http://localhost:11434"

REQUIREMENTS_SYSTEM_PROMPT = """\
You are a senior data science requirements analyst working with U.S. government agencies. \
You are having a conversation with a project requestor to understand their data science needs.

Here is what you already know about this project:

{context}

Your approach:
- Start by asking about their core problem — what decision or outcome are they trying to support?
- Ask ONE focused follow-up question at a time based on their last response. Do not ask multiple questions in a single message.
- Listen carefully to what they say and drill deeper before moving on to new topics.
- Naturally work through these areas over the course of the conversation:
  * The business problem and who it affects
  * Who the end users are
  * How they'd measure success
  * What data they have (or don't)
  * Data sensitivity / classification level
  * Timeline constraints and compliance requirements
  * How they want the solution delivered (dashboard, API, report, etc.)
  * Key stakeholders and who maintains it long-term
  * Priority level (mission-critical vs exploratory)
- When the user gives vague answers, ask for specifics. Suggest concrete examples.
- Keep your responses concise — 2-4 sentences plus your follow-up question.
- Be professional but conversational. This should feel like talking to a helpful colleague, not filling out a form.\
"""

EXTRACTION_SYSTEM_PROMPT = """\
You are a data extraction assistant. Given a conversation between a requirements analyst and \
a project requestor, extract all project requirements mentioned into a structured JSON object.

Return ONLY a JSON object with these fields (use empty string "" if not discussed):
{
  "business_problem": "the core problem or decision this project supports",
  "end_users": "who will use the solution",
  "success_criteria": "how success will be measured, metrics, thresholds",
  "data_availability": "one of: Yes — ready to share, Yes — but needs preparation, No — need to identify sources, Unsure, or empty",
  "data_classification": "one of: Unclassified, CUI, Secret, Top Secret, or empty",
  "data_volume": "approximate size or record count",
  "constraints_deadline": "any timeline or deadline mentioned",
  "constraints_compliance": ["list", "of", "compliance", "frameworks"],
  "hosting_environment": "one of: Cloud (FedRAMP authorized), On-premises, Air-gapped, Hybrid, Unsure, or empty",
  "integration_needs": "systems this must connect to",
  "delivery_format": "one of: Interactive dashboard, REST API, Periodic report, Embedded model, Standalone application, Multiple / Other, or empty",
  "stakeholders_approver": "approving authority name or title",
  "stakeholders_users": "primary user team or role",
  "stakeholders_maintainer": "long-term maintainer team or role",
  "priority_level": "one of: Mission-critical, Operational improvement, Exploratory / R&D, or empty"
}

Return ONLY valid JSON. No markdown fences, no explanation, no extra text.\
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


def _get_ollama_url() -> str:
    """Get the configured Ollama URL."""
    return st.session_state.get("ollama_url", DEFAULT_OLLAMA_URL).rstrip("/")


def _get_model() -> str:
    """Get the selected Ollama model."""
    return st.session_state.get("ollama_model", "")


def is_configured() -> bool:
    """Check if Ollama is reachable and a model is selected."""
    url = _get_ollama_url()
    model = _get_model()
    if not model:
        return False
    try:
        resp = requests.get(f"{url}/api/tags", timeout=3)
        return resp.status_code == 200
    except requests.ConnectionError:
        return False


def get_available_models() -> list[str]:
    """Query Ollama for available models. Returns a list of model names."""
    url = _get_ollama_url()
    try:
        resp = requests.get(f"{url}/api/tags", timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            return [m["name"] for m in data.get("models", [])]
    except (requests.ConnectionError, requests.Timeout, ValueError):
        pass
    return []


def _chat_completion(messages: list[dict], system: str = "") -> str:
    """Send a chat completion request to Ollama's native /api/chat endpoint.

    Uses the native endpoint with stream=false for better timeout handling
    with large models. Ollama keeps the connection alive with heartbeat
    while the model loads / generates.
    """
    url = _get_ollama_url()
    model = _get_model()
    if not model:
        raise ValueError("No Ollama model selected.")

    full_messages = []
    if system:
        full_messages.append({"role": "system", "content": system})
    full_messages.extend(messages)

    try:
        resp = requests.post(
            f"{url}/api/chat",
            json={
                "model": model,
                "messages": full_messages,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "num_predict": 1024,
                },
            },
            timeout=600,  # 10 min — large models need time to load on first call
        )
    except requests.Timeout:
        raise RuntimeError(
            f"Request timed out after 10 minutes. "
            f"Model '{model}' may be too large for your hardware. "
            f"Try a smaller model (e.g. qwen2.5:7b)."
        )

    if resp.status_code != 200:
        # Try to extract a useful error message from Ollama
        try:
            err_data = resp.json()
            msg = err_data.get("error", resp.text)
        except (ValueError, AttributeError):
            msg = resp.text
        if "memory" in str(msg).lower():
            raise RuntimeError(
                f"Model '{model}' requires more memory than is available. "
                f"Try a smaller model (e.g. qwen2.5:7b)."
            )
        raise RuntimeError(f"Ollama error ({resp.status_code}): {msg}")

    data = resp.json()
    return data["message"]["content"]


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
    """Send a chat to the LLM for requirements assistance. Returns assistant text."""
    context = build_project_context()
    system = REQUIREMENTS_SYSTEM_PROMPT.format(context=context)
    return _chat_completion(messages, system=system)


def extract_requirements_from_chat(chat_history: list[dict]) -> dict:
    """Extract structured requirements from the conversation history.

    Returns a dict matching the requirements schema, or empty dict on failure.
    """
    if not chat_history:
        return {}

    # Build a summary of the conversation for extraction
    conversation_text = "\n".join(
        f"{'Analyst' if m['role'] == 'assistant' else 'Requestor'}: {m['content']}"
        for m in chat_history
    )

    try:
        result = _chat_completion(
            messages=[{"role": "user", "content": conversation_text}],
            system=EXTRACTION_SYSTEM_PROMPT,
        )
        # Try to parse JSON from the response
        # Strip markdown fences if the model wraps them anyway
        cleaned = result.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.split("\n", 1)[1] if "\n" in cleaned else cleaned[3:]
        if cleaned.endswith("```"):
            cleaned = cleaned.rsplit("```", 1)[0]
        cleaned = cleaned.strip()

        extracted = json.loads(cleaned)
        # Ensure compliance is a list
        if isinstance(extracted.get("constraints_compliance"), str):
            val = extracted["constraints_compliance"]
            extracted["constraints_compliance"] = [v.strip() for v in val.split(",") if v.strip()] if val else []
        return extracted
    except (json.JSONDecodeError, requests.RequestException, ValueError, KeyError):
        return {}


def generate_scope_section(section: str) -> str:
    """Generate a specific scope document section using the LLM.

    section: one of "title_summary", "methodology", "timeline"
    """
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

    return _chat_completion(
        messages=[{"role": "user", "content": prompts[section]}],
        system=system,
    )
