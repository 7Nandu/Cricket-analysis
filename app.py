"""
Cricket Analytics Web Application.
Main entry point using Streamlit, Python, PostgreSQL, Pandas, and Plotly.
"""
import streamlit as st

# 1. Page Configuration (Wide layout, collapsed sidebar for top horizontal navigation)
st.set_page_config(
    page_title="Cricket Analytics Hub | IPL 2025",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="collapsed",
)

from components.navbar import render_navbar
from components.ui_cards import inject_custom_css, render_header
from database import test_connection
from views.analytics import render_analytics_view
from views.home import render_home_view
from views.match_centre import render_match_centre_view
from views.player_profile import render_player_profile_view
from views.search import render_search_view
from views.teams import render_teams_view


def main():
    # Inject styling
    inject_custom_css()

    # Verify Database Connection
    db_ok, db_err = test_connection()
    if not db_ok:
        render_header()
        st.error(
            f"⚠️ **Database Connection Error:** Unable to reach PostgreSQL database `cricket_analytics`.\n\n"
            f"Details: `{db_err}`\n\n"
            f"Please ensure PostgreSQL is running and credentials in `.env` are configured correctly."
        )
        st.info("Ensure `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, and `DB_PASSWORD` are set in `.env`.")
        return

    # Top Brand Header
    render_header(
        title="CRICKET ANALYTICS HUB",
        subtitle="IPL 2025 Comprehensive Performance, Match Center & Visual Intelligence",
    )

    # Horizontal Top Navigation Bar
    render_navbar()

    # Route according to active page in Session State
    active_page = st.session_state.get("current_page", "🏠 Home")

    if active_page == "🏠 Home":
        render_home_view()
    elif active_page == "🔍 Global Search":
        render_search_view()
    elif active_page == "🏏 Match Centre":
        render_match_centre_view()
    elif active_page == "👤 Player Profiles":
        render_player_profile_view()
    elif active_page == "🛡️ Teams":
        render_teams_view()
    elif active_page == "📊 Analytics":
        render_analytics_view()
    else:
        render_home_view()

    # Footer
    st.markdown("<div style='margin-top: 3rem;'></div>", unsafe_allow_html=True)
    st.markdown(
        """
        <div style="text-align: center; color: #94a3b8; font-size: 0.8rem; border-top: 1px solid #e2e8f0; padding-top: 1.2rem; margin-top: 2rem;">
            🏏 <strong>Cricket Analytics Hub</strong> • Built with Streamlit, PostgreSQL, Pandas & Plotly • IPL 2025 Data Engine
        </div>
        """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()

