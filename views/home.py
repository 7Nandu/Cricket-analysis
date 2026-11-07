"""
Home Dashboard View.
Provides high-level tournament KPIs, standings, top performers, recent fixtures, and venue statistics.
"""
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from components.navbar import navigate_to
from components.ui_cards import render_metric_card
import queries


def render_home_view():
    """Renders the Home Dashboard page."""
    # 1. KPI Metric Row
    kpis = queries.get_kpis()
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    with col1:
        render_metric_card("Matches", kpis["total_matches"], "IPL 2025 Fixtures", "🏏")
    with col2:
        render_metric_card("Teams", kpis["total_teams"], "Franchises", "🛡️")
    with col3:
        render_metric_card("Players", kpis["total_players"], "Active Squads", "👤")
    with col4:
        render_metric_card("Venues", kpis["total_venues"], "Stadiums", "🏟️")
    with col5:
        render_metric_card("Runs Scored", f"{kpis['total_runs']:,}", "Tournament Total", "⚡")
    with col6:
        render_metric_card("Wickets", kpis["total_wickets"], "Total Dismissals", "🎯")

    st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)

    # 2. Standings & Win Distribution
    st.markdown("### 🏆 Tournament Standings & Team Performance")
    standings_df = queries.get_standings()

    if not standings_df.empty:
        col_table, col_chart = st.columns([1.1, 0.9])
        with col_table:
            # Format standings table for display
            display_df = standings_df.copy()
            display_df["Rank"] = range(1, len(display_df) + 1)
            display_df = display_df.rename(
                columns={
                    "team_name": "Team",
                    "matches_played": "Mat",
                    "wins": "Won",
                    "losses": "Lost",
                    "win_percentage": "Win %",
                }
            )
            st.dataframe(
                display_df[["Rank", "Team", "Mat", "Won", "Lost", "Win %"]],
                hide_index=True,
                use_container_width=True,
                column_config={
                    "Win %": st.column_config.ProgressColumn(
                        "Win %",
                        format="%.1f%%",
                        min_value=0,
                        max_value=100,
                    ),
                },
            )

            # Quick franchise jump button
            c_sel_t, c_btn_t = st.columns([3, 1.5])
            with c_sel_t:
                sel_team_home = st.selectbox(
                    "Inspect Team Page:",
                    options=standings_df["team_id"].tolist(),
                    format_func=lambda tid: standings_df[standings_df["team_id"] == tid]["team_name"].values[0],
                    key="home_team_sel",
                )
            with c_btn_t:
                st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
                if st.button("View Team Page 🛡️", key="btn_home_view_team", use_container_width=True):
                    navigate_to("🛡️ Teams", team_id=int(sel_team_home))

        with col_chart:
            fig = px.bar(
                standings_df.sort_values("wins", ascending=True),
                x="wins",
                y="team_name",
                orientation="h",
                title="Team Wins Comparison",
                labels={"wins": "Wins", "team_name": "Team"},
                color="win_percentage",
                color_continuous_scale="Teal",
                text="wins",
            )
            fig.update_layout(
                margin=dict(l=0, r=20, t=40, b=10),
                height=350,
                xaxis_title="Matches Won",
                yaxis_title="",
                coloraxis_colorbar=dict(title="Win %"),
            )
            fig.update_traces(textposition="outside")
            st.plotly_chart(fig, use_container_width=True)

    st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)

    # 3. Top Performers (Orange & Purple Cap Previews)
    col_bat, col_bowl = st.columns(2)

    with col_bat:
        st.markdown("### 🟠 Leading Run Scorers")
        top_bat = queries.get_top_run_scorers(5)
        if not top_bat.empty:
            fig_bat = px.bar(
                top_bat.sort_values("total_runs", ascending=True),
                x="total_runs",
                y="player_name",
                orientation="h",
                text="total_runs",
                color="total_runs",
                color_continuous_scale="Oranges",
                labels={"total_runs": "Runs", "player_name": "Player"},
            )
            fig_bat.update_layout(
                margin=dict(l=0, r=20, t=20, b=10),
                height=260,
                showlegend=False,
                coloraxis_showscale=False,
                xaxis_title="Runs Scored",
                yaxis_title="",
            )
            fig_bat.update_traces(textposition="outside")
            st.plotly_chart(fig_bat, use_container_width=True)

            bat_preview = top_bat[["player_name", "team_name", "total_runs", "batting_average", "strike_rate"]].rename(
                columns={
                    "player_name": "Player",
                    "team_name": "Team",
                    "total_runs": "Runs",
                    "batting_average": "Avg",
                    "strike_rate": "SR",
                }
            )
            st.dataframe(bat_preview, hide_index=True, use_container_width=True)

            c_sel_bp, c_btn_bp = st.columns([3, 1.5])
            with c_sel_bp:
                top_bat_p_id = st.selectbox(
                    "Inspect Batter Profile:",
                    options=top_bat["player_id"].tolist(),
                    format_func=lambda pid: top_bat[top_bat["player_id"] == pid]["player_name"].values[0],
                    key="home_top_bat_sel",
                )
            with c_btn_bp:
                st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
                if st.button("View Profile 👤", key="btn_home_view_bat", use_container_width=True):
                    navigate_to("👤 Player Profiles", player_id=int(top_bat_p_id))

    with col_bowl:
        st.markdown("### 🟣 Leading Wicket Takers")
        top_bowl = queries.get_top_wicket_takers(5)
        if not top_bowl.empty:
            fig_bowl = px.bar(
                top_bowl.sort_values("total_wickets", ascending=True),
                x="total_wickets",
                y="player_name",
                orientation="h",
                text="total_wickets",
                color="total_wickets",
                color_continuous_scale="Purples",
                labels={"total_wickets": "Wickets", "player_name": "Player"},
            )
            fig_bowl.update_layout(
                margin=dict(l=0, r=20, t=20, b=10),
                height=260,
                showlegend=False,
                coloraxis_showscale=False,
                xaxis_title="Wickets Taken",
                yaxis_title="",
            )
            fig_bowl.update_traces(textposition="outside")
            st.plotly_chart(fig_bowl, use_container_width=True)

            bowl_preview = top_bowl[["player_name", "team_name", "total_wickets", "economy_rate", "bowling_average"]].rename(
                columns={
                    "player_name": "Player",
                    "team_name": "Team",
                    "total_wickets": "Wkts",
                    "economy_rate": "Econ",
                    "bowling_average": "Avg",
                }
            )
            st.dataframe(bowl_preview, hide_index=True, use_container_width=True)

            c_sel_bwp, c_btn_bwp = st.columns([3, 1.5])
            with c_sel_bwp:
                top_bowl_p_id = st.selectbox(
                    "Inspect Bowler Profile:",
                    options=top_bowl["player_id"].tolist(),
                    format_func=lambda pid: top_bowl[top_bowl["player_id"] == pid]["player_name"].values[0],
                    key="home_top_bowl_sel",
                )
            with c_btn_bwp:
                st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
                if st.button("View Profile 🎯", key="btn_home_view_bowl", use_container_width=True):
                    navigate_to("👤 Player Profiles", player_id=int(top_bowl_p_id))

    st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)

    # 4. Recent Fixtures & Results
    st.markdown("### 📅 Recent Match Fixtures & Results")
    recent_matches = queries.get_recent_matches(6)

    if not recent_matches.empty:
        for idx, row in recent_matches.iterrows():
            with st.container():
                c1, c2, c3, c4 = st.columns([1.2, 2.4, 2.4, 1.0])
                with c1:
                    st.caption(f"🗓️ {row['match_date']}")
                    st.markdown(f"**{row['city']}**")
                    st.caption(f"{row['venue_name']}")
                with c2:
                    st.markdown(f"**{row['home_team']}** vs **{row['away_team']}**")
                    st.caption(f"1st: {row['first_batting_team']} ({row['first_innings_score']})")
                with c3:
                    st.markdown(f"<span style='color: #059669; font-weight: 600;'>{row['result_summary']}</span>", unsafe_allow_html=True)
                    st.caption(f"2nd: {row['second_batting_team']} ({row['second_innings_score']})")
                with c4:
                    if st.button("View Scorecard", key=f"btn_match_{row['match_id']}", use_container_width=True):
                        navigate_to("🏏 Match Centre", match_id=int(row["match_id"]))
                st.markdown("<hr style='margin: 0.4rem 0 0.8rem 0; border: none; border-top: 1px solid #f1f5f9;'>", unsafe_allow_html=True)

    # 5. Venue Scoring Breakdown
    st.markdown("### 🏟️ Venue Scoring Trends")
    venue_df = queries.get_venue_statistics()
    if not venue_df.empty:
        fig_venue = go.Figure()
        fig_venue.add_trace(
            go.Bar(
                name="Avg 1st Innings",
                x=venue_df["venue_name"],
                y=venue_df["avg_1st_innings_score"],
                marker_color="#0284c7",
            )
        )
        fig_venue.add_trace(
            go.Bar(
                name="Avg 2nd Innings",
                x=venue_df["venue_name"],
                y=venue_df["avg_2nd_innings_score"],
                marker_color="#10b981",
            )
        )
        fig_venue.update_layout(
            barmode="group",
            xaxis_tickangle=-25,
            height=340,
            margin=dict(l=20, r=20, t=30, b=80),
            yaxis_title="Average Runs",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        )
        st.plotly_chart(fig_venue, use_container_width=True)
