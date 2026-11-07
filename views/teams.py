"""
Team Pages View.
Displays franchise profiles, squad roster, win-loss analytics, scoring charts, and match history.
"""
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from components.navbar import navigate_to
from components.ui_cards import get_role_badge, render_metric_card
import queries


def render_teams_view():
    """Renders the Team Pages interface."""
    st.markdown("### 🛡️ IPL Franchise Profiles & Squads")

    # Fetch all teams
    teams_df = queries.get_all_teams()
    if teams_df.empty:
        st.warning("No teams found in the database.")
        return

    team_ids = teams_df["team_id"].tolist()

    # Fallback initialization
    if "selected_team_id" not in st.session_state or st.session_state.selected_team_id not in team_ids:
        st.session_state.selected_team_id = team_ids[0]

    # Team options dictionary
    team_options = {row["team_id"]: row["team_name"] for _, row in teams_df.iterrows()}
    
    c_prev, c_sel, c_next = st.columns([1, 4, 1])
    current_idx = team_ids.index(st.session_state.selected_team_id)

    with c_prev:
        st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
        prev_disabled = current_idx == 0
        if st.button("⬅️ Prev Team", key=f"btn_prev_t_{st.session_state.selected_team_id}", disabled=prev_disabled, use_container_width=True):
            st.session_state.selected_team_id = team_ids[current_idx - 1]
            st.rerun()

    with c_sel:
        selected_team_id = st.selectbox(
            label="Select Franchise",
            options=team_ids,
            index=current_idx,
            format_func=lambda tid: team_options.get(tid, f"Team {tid}"),
            key=f"team_sel_box_{st.session_state.selected_team_id}",
        )
        if selected_team_id != st.session_state.selected_team_id:
            st.session_state.selected_team_id = selected_team_id
            st.rerun()

    with c_next:
        st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
        next_disabled = current_idx == len(team_ids) - 1
        if st.button("Next Team ➡️", key=f"btn_next_t_{st.session_state.selected_team_id}", disabled=next_disabled, use_container_width=True):
            st.session_state.selected_team_id = team_ids[current_idx + 1]
            st.rerun()

    # Current team row
    team_row = teams_df[teams_df["team_id"] == st.session_state.selected_team_id].iloc[0]

    # 1. Team Header Banner
    st.markdown(
        f"""
        <div style="background: #ffffff; border: 1px solid #cbd5e1; border-radius: 12px; padding: 1.2rem; margin: 1rem 0; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h2 style="margin: 0; font-size: 1.6rem; color: #0f172a;">🛡️ {team_row['team_name']}</h2>
                    <p style="margin: 0.2rem 0 0 0; color: #64748b; font-size: 0.9rem;">Country: <strong>{team_row['country']}</strong> | Head Coach: <strong>{team_row['coach'] or 'N/A'}</strong></p>
                </div>
                <div style="text-align: right;">
                    <span style="font-size: 1.2rem; font-weight: 700; color: #059669;">Win Rate: {team_row['win_percentage'] or 0.0}%</span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # 2. Performance Metric Cards
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        render_metric_card("Matches Played", int(team_row["matches_played"] or 0), "Tournament Fixtures", "🏏")
    with m2:
        render_metric_card("Matches Won", int(team_row["wins"] or 0), "Victories", "🏆")
    with m3:
        render_metric_card("Matches Lost", int(team_row["losses"] or 0), "Defeats", "❌")
    with m4:
        render_metric_card("Win Percentage", f"{team_row['win_percentage'] or 0.0}%", "Success Rate", "📈")

    st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)

    # Tabs: Squad Roster, Performance Charts, Match History
    tab_squad, tab_charts, tab_history = st.tabs(["👥 Squad Roster", "📊 Team Analytics", "📅 Match History"])

    # Squad Tab
    with tab_squad:
        squad_df = queries.get_team_squad(st.session_state.selected_team_id)
        if squad_df.empty:
            st.info("No squad players registered for this team.")
        else:
            st.markdown(f"#### Active Squad ({len(squad_df)} Players)")

            for _, p in squad_df.iterrows():
                with st.container():
                    c1, c2, c3, c4, c5 = st.columns([2.5, 1.8, 1.8, 1.8, 1.2])
                    with c1:
                        st.markdown(f"**{p['full_name']}**")
                        st.markdown(get_role_badge(p["role"]), unsafe_allow_html=True)
                    with c2:
                        st.caption(f"Bat: {p['batting_style']}")
                        if p["bowling_style"]:
                            st.caption(f"Bowl: {p['bowling_style']}")
                    with c3:
                        st.markdown(f"**{p['runs']}** Runs")
                        st.caption(f"SR: {p['batting_sr']:.1f}")
                    with c4:
                        st.markdown(f"**{p['wickets']}** Wickets")
                        st.caption(f"Econ: {p['economy']:.1f}")
                    with c5:
                        if st.button("Profile 👤", key=f"btn_squad_p_{p['player_id']}", use_container_width=True):
                            navigate_to("👤 Player Profiles", player_id=int(p["player_id"]))
                    st.markdown("<hr style='margin: 0.3rem 0; border: none; border-top: 1px solid #f1f5f9;'>", unsafe_allow_html=True)

    # Charts Tab
    with tab_charts:
        col_c1, col_c2 = st.columns(2)

        with col_c1:
            # Win/Loss Donut
            wins = int(team_row["wins"] or 0)
            losses = int(team_row["losses"] or 0)
            if wins + losses > 0:
                fig_donut = go.Figure(
                    data=[
                        go.Pie(
                            labels=["Wins", "Losses"],
                            values=[wins, losses],
                            hole=0.5,
                            marker_colors=["#10b981", "#ef4444"],
                        )
                    ]
                )
                fig_donut.update_layout(
                    title="Win vs Loss Ratio",
                    height=280,
                    margin=dict(l=20, r=20, t=40, b=20),
                )
                st.plotly_chart(fig_donut, use_container_width=True)
            else:
                st.info("No match results recorded yet.")

        with col_c2:
            # Top Run Scorers in team
            if not squad_df.empty:
                top_batters = squad_df.sort_values("runs", ascending=False).head(5)
                fig_squad_bat = px.bar(
                    top_batters.sort_values("runs", ascending=True),
                    x="runs",
                    y="full_name",
                    orientation="h",
                    text="runs",
                    title="Top Team Run Scorers",
                    color="runs",
                    color_continuous_scale="Teal",
                    labels={"runs": "Total Runs", "full_name": "Player"},
                )
                fig_squad_bat.update_layout(height=280, margin=dict(l=20, r=20, t=40, b=20), coloraxis_showscale=False)
                fig_squad_bat.update_traces(textposition="outside")
                st.plotly_chart(fig_squad_bat, use_container_width=True)

        # Innings Totals Chart
        innings_totals = queries.get_team_innings_totals(st.session_state.selected_team_id)
        if not innings_totals.empty:
            st.markdown("##### Innings Scores Progression")
            fig_totals = px.bar(
                innings_totals,
                x="opposition",
                y="total_runs",
                text="total_runs",
                title="Scores by Match Opposition",
                color="run_rate",
                color_continuous_scale="Blues",
                labels={"opposition": "Opponent", "total_runs": "Runs", "run_rate": "Run Rate"},
            )
            fig_totals.update_layout(height=280, margin=dict(l=20, r=20, t=40, b=20))
            fig_totals.update_traces(textposition="outside")
            st.plotly_chart(fig_totals, use_container_width=True)

    # Match History Tab
    with tab_history:
        history_df = queries.get_team_match_history(st.session_state.selected_team_id)
        if history_df.empty:
            st.info("No match fixtures recorded for this team.")
        else:
            st.markdown(f"#### Match Fixtures & Results ({len(history_df)} Matches)")

            for _, m in history_df.iterrows():
                with st.container():
                    c1, c2, c3, c4 = st.columns([1.5, 2.5, 3.0, 1.2])
                    with c1:
                        st.caption(f"🗓️ {m['match_date']}")
                        st.markdown(f"**{m['venue_type']} Match**")
                    with c2:
                        st.markdown(f"vs **{m['opponent']}**")
                        st.caption(f"{m['venue_name']}, {m['city']}")
                    with c3:
                        is_win = m["outcome"] == "Won"
                        badge_color = "#15803d" if is_win else "#b91c1c"
                        st.markdown(
                            f"<span style='color: {badge_color}; font-weight: 600;'>{m['outcome'].upper()}</span> - {m['result_summary']}",
                            unsafe_allow_html=True,
                        )
                    with c4:
                        if st.button("Scorecard 🏏", key=f"btn_team_m_{m['match_id']}", use_container_width=True):
                            navigate_to("🏏 Match Centre", match_id=int(m["match_id"]))
                    st.markdown("<hr style='margin: 0.3rem 0; border: none; border-top: 1px solid #f1f5f9;'>", unsafe_allow_html=True)
