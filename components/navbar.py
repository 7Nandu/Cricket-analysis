"""
Horizontal Top Navigation Bar component.
Provides responsive tab selection, session state synchronization, and page routing.
"""
import streamlit as st

NAV_OPTIONS = [
    "🏠 Home",
    "🔍 Global Search",
    "🏏 Match Centre",
    "👤 Player Profiles",
    "🛡️ Teams",
    "📊 Analytics",
]


def render_navbar():
    """Renders the top horizontal navigation bar using st.pills."""
    # Process target page if set by programmatic navigation BEFORE creating the widget
    if "target_page" in st.session_state:
        target = st.session_state.pop("target_page")
        if target in NAV_OPTIONS:
            st.session_state.current_page = target
            st.session_state.top_nav_selection = target

    if "current_page" not in st.session_state or st.session_state.current_page not in NAV_OPTIONS:
        st.session_state.current_page = "🏠 Home"

    if "top_nav_selection" not in st.session_state or st.session_state.top_nav_selection not in NAV_OPTIONS:
        st.session_state.top_nav_selection = st.session_state.current_page

    def on_pills_change():
        if "top_nav_selection" in st.session_state and st.session_state.top_nav_selection:
            st.session_state.current_page = st.session_state.top_nav_selection

    selected = st.pills(
        label="Navigation Menu",
        options=NAV_OPTIONS,
        label_visibility="collapsed",
        key="top_nav_selection",
        on_change=on_pills_change,
    )

    if selected and selected != st.session_state.current_page:
        st.session_state.current_page = selected

    st.markdown("<div style='margin-bottom: 1rem;'></div>", unsafe_allow_html=True)


def navigate_to(
    page: str,
    player_id: int = None,
    match_id: int = None,
    team_id: int = None,
    search_term: str = None,
):
    """Programmatic navigation helper for buttons and links."""
    st.session_state.target_page = page
    if player_id is not None:
        st.session_state.selected_player_id = int(player_id)
    if match_id is not None:
        st.session_state.selected_match_id = int(match_id)
    if team_id is not None:
        st.session_state.selected_team_id = int(team_id)
    if search_term is not None:
        st.session_state.target_search_term = str(search_term)
    st.rerun()
