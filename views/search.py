"""
Global Search View.
Enables cross-entity search across players, teams, matches, and venues with direct navigation.
"""
import streamlit as st

from components.navbar import navigate_to
from components.ui_cards import get_role_badge
import queries


def render_search_view():
    """Renders the Global Search interface."""
    st.markdown("### 🔍 Global Cricket Search")
    st.caption("Search across players, franchises, match fixtures, and stadium venues.")

    # Process pending target search term BEFORE the text_input widget is created
    if "target_search_term" in st.session_state:
        val = st.session_state.pop("target_search_term")
        st.session_state.global_search_input = val
        st.session_state.search_term = val

    if "global_search_input" not in st.session_state:
        st.session_state.global_search_input = ""

    c_search, c_clear = st.columns([5, 1])
    with c_search:
        search_query = st.text_input(
            label="Search Database",
            placeholder="Type player name (e.g., Virat, Bumrah), team (e.g., CSK, Mumbai), venue, or city...",
            key="global_search_input",
        )
    with c_clear:
        st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
        if st.button("❌ Clear", key="btn_clear_search", use_container_width=True):
            st.session_state.target_search_term = ""
            st.rerun()

    # Preset quick-search chips
    st.markdown("**Quick Searches:**")
    quick_cols = st.columns(6)
    presets = ["Virat Kohli", "Jasprit Bumrah", "Chennai Super Kings", "Mumbai Indians", "Wankhede Stadium", "Chepauk"]
    for i, preset in enumerate(presets):
        with quick_cols[i]:
            if st.button(preset, key=f"chip_{i}", use_container_width=True):
                st.session_state.target_search_term = preset
                st.rerun()

    st.markdown("<hr style='margin: 1rem 0;'>", unsafe_allow_html=True)

    term = st.session_state.get("global_search_input", "").strip()
    if not term:
        st.info("💡 Enter a keyword above or click any preset chip to search registered players, teams, venues, and matches.")
        return

    # Execute searches across all entities
    players_df = queries.search_players(term)
    teams_df = queries.search_teams(term)
    matches_df = queries.search_matches(term)
    venues_df = queries.search_venues(term)

    total_results = len(players_df) + len(teams_df) + len(matches_df) + len(venues_df)

    if total_results == 0:
        st.warning(f"No results found matching '{term}'. Try searching with a different name, role, or team.")
        return

    st.success(f"Found **{total_results}** matching results for '**{term}**'")

    # Results Tabs
    tab_players, tab_teams, tab_matches, tab_venues = st.tabs([
        f"👤 Players ({len(players_df)})",
        f"🛡️ Teams ({len(teams_df)})",
        f"🏏 Matches ({len(matches_df)})",
        f"🏟️ Venues ({len(venues_df)})",
    ])

    # 1. Players Tab
    with tab_players:
        if players_df.empty:
            st.info("No players matched your search.")
        else:
            for _, p in players_df.iterrows():
                with st.container():
                    c1, c2, c3, c4 = st.columns([2.5, 1.8, 2.0, 1.2])
                    with c1:
                        st.markdown(f"**{p['full_name']}**")
                        st.markdown(get_role_badge(p["role"]), unsafe_allow_html=True)
                    with c2:
                        st.markdown(f"**Team:** {p['team_name']}")
                    with c3:
                        st.caption(f"Bat: {p['batting_style']}")
                        if p["bowling_style"]:
                            st.caption(f"Bowl: {p['bowling_style']}")
                    with c4:
                        if st.button("View Profile", key=f"btn_search_p_{p['player_id']}", use_container_width=True):
                            navigate_to("👤 Player Profiles", player_id=int(p["player_id"]))
                    st.markdown("<hr style='margin: 0.3rem 0; border: none; border-top: 1px solid #f1f5f9;'>", unsafe_allow_html=True)

    # 2. Teams Tab
    with tab_teams:
        if teams_df.empty:
            st.info("No teams matched your search.")
        else:
            for _, t in teams_df.iterrows():
                with st.container():
                    c1, c2, c3 = st.columns([3, 3, 1.5])
                    with c1:
                        st.markdown(f"### 🛡️ {t['team_name']}")
                        st.caption(f"Country: {t['country']}")
                    with c2:
                        st.markdown(f"**Head Coach:** {t['coach'] or 'N/A'}")
                    with c3:
                        if st.button("View Team", key=f"btn_search_t_{t['team_id']}", use_container_width=True):
                            navigate_to("🛡️ Teams", team_id=int(t["team_id"]))
                    st.markdown("<hr style='margin: 0.3rem 0; border: none; border-top: 1px solid #f1f5f9;'>", unsafe_allow_html=True)

    # 3. Matches Tab
    with tab_matches:
        if matches_df.empty:
            st.info("No matches matched your search.")
        else:
            for _, m in matches_df.iterrows():
                with st.container():
                    c1, c2, c3, c4 = st.columns([1.5, 2.5, 2.5, 1.2])
                    with c1:
                        st.caption(f"🗓️ {m['match_date']}")
                        st.markdown(f"**{m['city']}**")
                    with c2:
                        st.markdown(f"**{m['home_team']}** vs **{m['away_team']}**")
                        st.caption(m["venue_name"])
                    with c3:
                        st.markdown(f"<span style='color: #059669; font-weight: 600;'>{m['result_summary']}</span>", unsafe_allow_html=True)
                    with c4:
                        if st.button("View Scorecard", key=f"btn_search_m_{m['match_id']}", use_container_width=True):
                            navigate_to("🏏 Match Centre", match_id=int(m["match_id"]))
                    st.markdown("<hr style='margin: 0.3rem 0; border: none; border-top: 1px solid #f1f5f9;'>", unsafe_allow_html=True)

    # 4. Venues Tab
    with tab_venues:
        if venues_df.empty:
            st.info("No venues matched your search.")
        else:
            for _, v in venues_df.iterrows():
                with st.container():
                    c1, c2 = st.columns([4, 2])
                    with c1:
                        st.markdown(f"**{v['venue_name']}**")
                        st.caption(f"📍 {v['city']}, {v['country']}")
                    with c2:
                        st.markdown(f"**Capacity:** {v['capacity']:,} spectators" if v['capacity'] else "Capacity: N/A")
                    st.markdown("<hr style='margin: 0.3rem 0; border: none; border-top: 1px solid #f1f5f9;'>", unsafe_allow_html=True)
