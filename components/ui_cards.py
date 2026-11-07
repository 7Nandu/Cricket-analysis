"""
UI Components and Styling for Cricket Analytics Web Application.
Provides custom CSS, metric cards, badges, and layout helpers.
"""
import streamlit as st


def inject_custom_css():
    """Injects modern, clean, sports-analytics CSS stylesheet."""
    css = """
    <style>
    /* Hide Streamlit default sidebar & header decoration */
    [data-testid="stSidebar"] {
        display: none !important;
    }
    [data-testid="collapsedControl"] {
        display: none !important;
    }
    header[data-testid="stHeader"] {
        background-color: transparent !important;
    }
    
    /* Global App Container */
    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 3rem !important;
        max-width: 1280px !important;
    }

    /* Top Brand Bar */
    .brand-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0.8rem 1.4rem;
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        border-radius: 12px;
        color: #f8fafc;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.08);
    }
    .brand-title {
        font-size: 1.5rem;
        font-weight: 700;
        letter-spacing: -0.025em;
        margin: 0;
        display: flex;
        align-items: center;
        gap: 0.6rem;
    }
    .brand-subtitle {
        font-size: 0.85rem;
        color: #94a3b8;
        margin: 0;
        font-weight: 400;
    }
    .db-badge {
        background-color: rgba(16, 185, 129, 0.15);
        color: #10b981;
        border: 1px solid rgba(16, 185, 129, 0.3);
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 0.4rem;
    }

    /* Top Horizontal Navigation Container */
    .nav-container {
        margin-bottom: 1.5rem;
        padding: 0.4rem;
        background-color: #f1f5f9;
        border-radius: 10px;
        border: 1px solid #e2e8f0;
    }

    /* Metric Cards */
    .metric-card {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 1rem 1.2rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.08);
        border-color: #cbd5e1;
    }
    .metric-label {
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #64748b;
        margin-bottom: 0.25rem;
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #0f172a;
        line-height: 1.2;
    }
    .metric-subtext {
        font-size: 0.75rem;
        color: #94a3b8;
        margin-top: 0.3rem;
    }

    /* Section Headings */
    .section-title {
        font-size: 1.2rem;
        font-weight: 700;
        color: #0f172a;
        margin-top: 1.2rem;
        margin-bottom: 0.8rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        border-bottom: 2px solid #f1f5f9;
        padding-bottom: 0.4rem;
    }

    /* Match Result Card */
    .match-card {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 0.8rem;
        box-shadow: 0 1px 2px rgba(0,0,0,0.04);
        transition: border-color 0.15s ease;
    }
    .match-card:hover {
        border-color: #0284c7;
    }
    .match-header {
        font-size: 0.8rem;
        color: #64748b;
        display: flex;
        justify-content: space-between;
        margin-bottom: 0.5rem;
    }
    .match-teams {
        font-size: 1.05rem;
        font-weight: 600;
        color: #0f172a;
        margin-bottom: 0.4rem;
    }
    .match-scores {
        font-size: 0.9rem;
        color: #334155;
        margin-bottom: 0.4rem;
    }
    .match-result {
        font-size: 0.85rem;
        font-weight: 600;
        color: #059669;
    }

    /* Badges */
    .badge {
        display: inline-block;
        padding: 0.2rem 0.5rem;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    .badge-batter { background-color: #e0f2fe; color: #0369a1; }
    .badge-bowler { background-color: #fef3c7; color: #b45309; }
    .badge-allrounder { background-color: #dcfce7; color: #15803d; }
    .badge-wk { background-color: #f3e8ff; color: #7e22ce; }
    .badge-win { background-color: #dcfce7; color: #15803d; }
    .badge-loss { background-color: #fee2e2; color: #b91c1c; }

    /* Tables */
    .dataframe {
        font-size: 0.88rem !important;
        border-radius: 8px !important;
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


def render_metric_card(label: str, value: str | int | float, subtext: str = "", icon: str = ""):
    """Renders a styled metric card."""
    icon_html = f"<span style='font-size: 1.1rem; margin-right: 0.3rem;'>{icon}</span>" if icon else ""
    html = f"""
    <div class="metric-card">
        <div class="metric-label">{icon_html}{label}</div>
        <div class="metric-value">{value}</div>
        {"<div class='metric-subtext'>" + subtext + "</div>" if subtext else ""}
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def render_header(title: str = "CRICKET ANALYTICS HUB", subtitle: str = "IPL 2025 Performance & Statistics"):
    """Renders top brand header."""
    html = f"""
    <div class="brand-header">
        <div>
            <h1 class="brand-title">🏏 {title}</h1>
            <p class="brand-subtitle">{subtitle}</p>
        </div>
        <div class="db-badge">
            <span style="font-size: 0.9rem;">●</span> PostgreSQL Live (cricket_analytics)
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def get_role_badge(role: str) -> str:
    """Returns HTML for a styled role badge."""
    role_lower = str(role).lower()
    if "batter" in role_lower:
        return f'<span class="badge badge-batter">🏏 Batter</span>'
    elif "bowler" in role_lower:
        return f'<span class="badge badge-bowler">🎯 Bowler</span>'
    elif "all-rounder" in role_lower:
        return f'<span class="badge badge-allrounder">⚡ All-Rounder</span>'
    elif "keeper" in role_lower or "wicket" in role_lower:
        return f'<span class="badge badge-wk">🧤 Wicketkeeper</span>'
    return f'<span class="badge badge-batter">{role}</span>'

