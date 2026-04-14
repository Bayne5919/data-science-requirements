"""Government-formal CSS styling inspired by USWDS (U.S. Web Design System)."""


def get_custom_css() -> str:
    """Return custom CSS for a government-formal look and feel."""
    return """
    <style>
        /* ── Typography & Base ── */
        @import url('https://fonts.googleapis.com/css2?family=Source+Sans+Pro:wght@300;400;600;700&display=swap');

        html, body, [class*="css"] {
            font-family: 'Source Sans Pro', 'Helvetica Neue', Helvetica, Arial, sans-serif;
        }

        /* ── Header Banner ── */
        .gov-banner {
            background-color: #1a2e44;
            color: #ffffff;
            padding: 1rem 1.5rem;
            border-radius: 4px;
            margin-bottom: 1.5rem;
        }
        .gov-banner h1 {
            color: #ffffff;
            font-size: 1.6rem;
            font-weight: 700;
            margin: 0 0 0.25rem 0;
            letter-spacing: 0.02em;
        }
        .gov-banner p {
            color: #a9c4e0;
            font-size: 0.95rem;
            margin: 0;
        }

        /* ── Phase Progress Bar ── */
        .phase-tracker {
            display: flex;
            justify-content: space-between;
            margin: 0.5rem 0 1.5rem 0;
            padding: 0;
        }
        .phase-step {
            flex: 1;
            text-align: center;
            padding: 0.6rem 0.25rem;
            font-size: 0.78rem;
            font-weight: 600;
            color: #71767a;
            border-bottom: 3px solid #dfe1e2;
            transition: all 0.2s ease;
        }
        .phase-step.active {
            color: #005ea2;
            border-bottom-color: #005ea2;
            background-color: #eff6fb;
        }
        .phase-step.completed {
            color: #2e8540;
            border-bottom-color: #2e8540;
        }
        .phase-step.locked {
            color: #c9c9c9;
            border-bottom-color: #f0f0f0;
        }

        /* ── Cards / Sections ── */
        .gov-card {
            background: #ffffff;
            border: 1px solid #dfe1e2;
            border-left: 4px solid #005ea2;
            border-radius: 4px;
            padding: 1.25rem 1.5rem;
            margin-bottom: 1rem;
        }
        .gov-card h3 {
            color: #1b1b1b;
            font-size: 1.15rem;
            font-weight: 700;
            margin-top: 0;
        }
        .gov-card p {
            color: #3d4551;
            line-height: 1.6;
        }

        /* ── Alert / Info Boxes ── */
        .gov-alert-info {
            background-color: #e7f2f8;
            border-left: 4px solid #005ea2;
            padding: 1rem 1.25rem;
            border-radius: 2px;
            margin-bottom: 1rem;
            color: #1b1b1b;
        }
        .gov-alert-warning {
            background-color: #faf3d1;
            border-left: 4px solid #e5a000;
            padding: 1rem 1.25rem;
            border-radius: 2px;
            margin-bottom: 1rem;
            color: #1b1b1b;
        }
        .gov-alert-success {
            background-color: #ecf3ec;
            border-left: 4px solid #2e8540;
            padding: 1rem 1.25rem;
            border-radius: 2px;
            margin-bottom: 1rem;
            color: #1b1b1b;
        }

        /* ── Buttons ── */
        .stButton > button {
            background-color: #005ea2;
            color: #ffffff;
            border: none;
            border-radius: 4px;
            padding: 0.6rem 1.5rem;
            font-weight: 600;
            font-size: 0.95rem;
            letter-spacing: 0.02em;
        }
        .stButton > button:hover {
            background-color: #1a4480;
        }

        /* ── Sidebar ── */
        section[data-testid="stSidebar"] {
            background-color: #f0f0f0;
            border-right: 1px solid #dfe1e2;
        }
        section[data-testid="stSidebar"] .stMarkdown h2 {
            color: #1b1b1b;
            font-size: 1.1rem;
            font-weight: 700;
            border-bottom: 2px solid #005ea2;
            padding-bottom: 0.5rem;
        }

        /* ── Category Selection Cards ── */
        .category-card {
            background: #ffffff;
            border: 1px solid #dfe1e2;
            border-radius: 4px;
            padding: 1rem;
            margin-bottom: 0.75rem;
            cursor: pointer;
            transition: border-color 0.2s;
        }
        .category-card:hover {
            border-color: #005ea2;
        }
        .category-card.selected {
            border-color: #005ea2;
            border-left: 4px solid #005ea2;
            background-color: #eff6fb;
        }

        /* ── Footer ── */
        .gov-footer {
            border-top: 2px solid #dfe1e2;
            padding-top: 0.75rem;
            margin-top: 2rem;
            font-size: 0.8rem;
            color: #71767a;
            text-align: center;
        }
    </style>
    """
