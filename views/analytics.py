"""
Tournament Analytics View.
Provides head-to-head comparisons (Player vs Player, Team vs Team),
deep tournament leaderboards with dynamic filters, and stadium venue analytics.
"""
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from components.navbar import navigate_to
from components.ui_cards import render_metric_card
import queries


def render_analytics_view():
    """Renders the Analytics and Comparisons interface."""
    st.markdown("### 📊 In-Depth Tournament Analytics & Comparisons")

    tab_h2h_player, tab_h2h_team, tab_leaderboards, tab_venues = st.tabs([
        "⚔️ Player Comparison",
        "🛡️ Team Head-to-Head",
        "🏆 Tournament Leaderboards",
        "🏟️ Stadium Deep-Dive",
    ])

    # =========================================================================
    # 1. Player Comparison Tab
    # =========================================================================
    with tab_h2h_player:
        st.markdown("#### Head-to-Head Player Comparison")
        comp_type = st.radio("Comparison Category:", ["🏏 Batters", "🎯 Bowlers"], horizontal=True, key="comp_cat_radio")

        all_players = queries.get_all_players()
        if all_players.empty:
            st.warning("No players available for comparison.")
        else:
            player_list = all_players["player_id"].tolist()
            player_names = {row["player_id"]: f"{row['full_name']} ({row['team_name']})" for _, row in all_players.iterrows()}

            col_p1, col_p2 = st.columns(2)
            with col_p1:
                p1_id = st.selectbox(
                    "Select Player 1:",
                    options=player_list,
                    format_func=lambda pid: player_names.get(pid, f"Player {pid}"),
                    index=0,
                    key="comp_p1",
                )
                if st.button("View Player 1 Profile 👤", key="btn_view_p1", use_container_width=True):
                    navigate_to("👤 Player Profiles", player_id=int(p1_id))

            with col_p2:
                default_p2_idx = 1 if len(player_list) > 1 else 0
                p2_id = st.selectbox(
                    "Select Player 2:",
                    options=player_list,
                    format_func=lambda pid: player_names.get(pid, f"Player {pid}"),
                    index=default_p2_idx,
                    key="comp_p2",
                )
                if st.button("View Player 2 Profile 👤", key="btn_view_p2", use_container_width=True):
                    navigate_to("👤 Player Profiles", player_id=int(p2_id))

            p1_bio = queries.get_player_bio(p1_id)
            p2_bio = queries.get_player_bio(p2_id)

            if comp_type == "🏏 Batters":
                p1_bat = queries.get_player_batting_summary(p1_id) or {}
                p2_bat = queries.get_player_batting_summary(p2_id) or {}

                # Side-by-side metric display
                c1, c2, c3, c4 = st.columns(4)
                with c1:
                    st.metric(
                        f"Runs: {p1_bio['full_name']}",
                        p1_bat.get("total_runs", 0),
                        delta=f"{p1_bat.get('total_runs', 0) - p2_bat.get('total_runs', 0)} vs {p2_bio['full_name']}",
                    )
                with c2:
                    st.metric(f"Runs: {p2_bio['full_name']}", p2_bat.get("total_runs", 0))
                with c3:
                    st.metric(f"Strike Rate: {p1_bio['full_name']}", f"{p1_bat.get('strike_rate', 0.0) or 0.0}")
                with c4:
                    st.metric(f"Strike Rate: {p2_bio['full_name']}", f"{p2_bat.get('strike_rate', 0.0) or 0.0}")

                # Comparison Bar Chart
                metrics = ["Total Runs", "Highest Score", "Fours", "Sixes"]
                p1_vals = [
                    p1_bat.get("total_runs", 0),
                    p1_bat.get("highest_score", 0),
                    p1_bat.get("total_fours", 0),
                    p1_bat.get("total_sixes", 0),
                ]
                p2_vals = [
                    p2_bat.get("total_runs", 0),
                    p2_bat.get("highest_score", 0),
                    p2_bat.get("total_fours", 0),
                    p2_bat.get("total_sixes", 0),
                ]

                fig_comp = go.Figure(
                    data=[
                        go.Bar(name=p1_bio["full_name"], x=metrics, y=p1_vals, marker_color="#0284c7"),
                        go.Bar(name=p2_bio["full_name"], x=metrics, y=p2_vals, marker_color="#f97316"),
                    ]
                )
                fig_comp.update_layout(
                    barmode="group",
                    title="Batting Metrics Comparison",
                    height=320,
                    margin=dict(l=20, r=20, t=40, b=20),
                )
                st.plotly_chart(fig_comp, use_container_width=True)

            else:  # Bowlers
                p1_bowl = queries.get_player_bowling_summary(p1_id) or {}
                p2_bowl = queries.get_player_bowling_summary(p2_id) or {}

                c1, c2, c3, c4 = st.columns(4)
                with c1:
                    st.metric(
                        f"Wickets: {p1_bio['full_name']}",
                        p1_bowl.get("wickets_taken", 0),
                        delta=f"{p1_bowl.get('wickets_taken', 0) - p2_bowl.get('wickets_taken', 0)} vs {p2_bio['full_name']}",
                    )
                with c2:
                    st.metric(f"Wickets: {p2_bio['full_name']}", p2_bowl.get("wickets_taken", 0))
                with c3:
                    st.metric(f"Economy: {p1_bio['full_name']}", f"{p1_bowl.get('economy_rate', 0.0) or 0.0}")
                with c4:
                    st.metric(f"Economy: {p2_bio['full_name']}", f"{p2_bowl.get('economy_rate', 0.0) or 0.0}")

                b_metrics = ["Wickets", "Maidens", "Runs Conceded"]
                p1_b_vals = [
                    p1_bowl.get("wickets_taken", 0),
                    p1_bowl.get("maidens", 0),
                    p1_bowl.get("runs_conceded", 0),
                ]
                p2_b_vals = [
                    p2_bowl.get("wickets_taken", 0),
                    p2_bowl.get("maidens", 0),
                    p2_bowl.get("runs_conceded", 0),
                ]

                fig_b_comp = go.Figure(
                    data=[
                        go.Bar(name=p1_bio["full_name"], x=b_metrics, y=p1_b_vals, marker_color="#7e22ce"),
                        go.Bar(name=p2_bio["full_name"], x=b_metrics, y=p2_b_vals, marker_color="#059669"),
                    ]
                )
                fig_b_comp.update_layout(
                    barmode="group",
                    title="Bowling Figures Comparison",
                    height=320,
                    margin=dict(l=20, r=20, t=40, b=20),
                )
                st.plotly_chart(fig_b_comp, use_container_width=True)

    # =========================================================================
    # 2. Team Head-to-Head Tab
    # =========================================================================
    with tab_h2h_team:
        st.markdown("#### Franchise Head-to-Head Analysis")
        h2h_df = queries.get_head_to_head_all()

        if h2h_df.empty:
            st.info("No head-to-head records found.")
        else:
            all_teams = queries.get_all_teams()
            team_ids_map = {row["team_name"]: row["team_id"] for _, row in all_teams.iterrows()}
            team_names = all_teams["team_name"].tolist()

            col_t1, col_t2 = st.columns(2)
            with col_t1:
                t1_select = st.selectbox("Select Team 1:", options=team_names, index=0, key="h2h_t1")
                if st.button(f"View {t1_select} Page 🛡️", key="btn_view_h2h_t1", use_container_width=True):
                    navigate_to("🛡️ Teams", team_id=int(team_ids_map[t1_select]))

            with col_t2:
                default_t2_idx = 1 if len(team_names) > 1 else 0
                t2_select = st.selectbox("Select Team 2:", options=team_names, index=default_t2_idx, key="h2h_t2")
                if st.button(f"View {t2_select} Page 🛡️", key="btn_view_h2h_t2", use_container_width=True):
                    navigate_to("🛡️ Teams", team_id=int(team_ids_map[t2_select]))

            # Look for match pair in both orders
            match_row = h2h_df[
                ((h2h_df["team_1"] == t1_select) & (h2h_df["team_2"] == t2_select))
                | ((h2h_df["team_1"] == t2_select) & (h2h_df["team_2"] == t1_select))
            ]

            if match_row.empty:
                st.info(f"No direct matches have been played between **{t1_select}** and **{t2_select}** in the dataset.")
            else:
                row = match_row.iloc[0]
                t1_wins = row["team_1_wins"] if row["team_1"] == t1_select else row["team_2_wins"]
                t2_wins = row["team_2_wins"] if row["team_1"] == t1_select else row["team_1_wins"]
                total_played = row["total_matches"]

                c1, c2, c3 = st.columns(3)
                with c1:
                    render_metric_card(f"{t1_select} Wins", t1_wins, f"Out of {total_played} fixtures", "🛡️")
                with c2:
                    render_metric_card(f"{t2_select} Wins", t2_wins, f"Out of {total_played} fixtures", "🛡️")
                with c3:
                    render_metric_card("Total Matches", total_played, "Direct Clashes", "⚔️")

                fig_h2h = go.Figure(
                    data=[
                        go.Bar(
                            x=[t1_select, t2_select],
                            y=[t1_wins, t2_wins],
                            marker_color=["#0284c7", "#10b981"],
                            text=[t1_wins, t2_wins],
                            textposition="auto",
                        )
                    ]
                )
                fig_h2h.update_layout(title="Direct Head-to-Head Victories", height=280, yaxis_title="Matches Won")
                st.plotly_chart(fig_h2h, use_container_width=True)

            st.markdown("##### All Head-to-Head Records in Tournament")
            st.dataframe(
                h2h_df.rename(columns={
                    "team_1": "Home Team",
                    "team_2": "Away Team",
                    "total_matches": "Played",
                    "team_1_wins": "Home Wins",
                    "team_2_wins": "Away Wins",
                }),
                hide_index=True,
                use_container_width=True,
            )

    # =========================================================================
    # 3. Leaderboards & Filters Tab
    # =========================================================================
    with tab_leaderboards:
        st.markdown("#### Tournament Leaderboards & Custom Filters")
        board_type = st.radio("Leaderboard:", ["🏏 Batting Leaderboard", "🎯 Bowling Leaderboard", "🧤 Fielding Leaderboard"], horizontal=True, key="board_type_radio")

        if board_type == "🏏 Batting Leaderboard":
            bat_board = queries.get_all_batting_leaderboard()

            # Dynamic Filters
            f1, f2, f3 = st.columns(3)
            with f1:
                teams_filter = ["All Teams"] + sorted(bat_board["team_name"].unique().tolist())
                selected_team_filter = st.selectbox("Filter by Team:", teams_filter, key="bat_filt_team")
            with f2:
                roles_filter = ["All Roles"] + sorted(bat_board["role"].unique().tolist())
                selected_role_filter = st.selectbox("Filter by Role:", roles_filter, key="bat_filt_role")
            with f3:
                min_runs = st.slider("Minimum Runs:", 0, int(bat_board["total_runs"].max() if not bat_board.empty else 100), 0, key="bat_filt_runs")

            filtered_bat = bat_board.copy()
            if selected_team_filter != "All Teams":
                filtered_bat = filtered_bat[filtered_bat["team_name"] == selected_team_filter]
            if selected_role_filter != "All Roles":
                filtered_bat = filtered_bat[filtered_bat["role"] == selected_role_filter]
            filtered_bat = filtered_bat[filtered_bat["total_runs"] >= min_runs]

            st.markdown(f"**Showing {len(filtered_bat)} Players**")
            st.dataframe(
                filtered_bat[[
                    "player_name", "team_name", "role", "innings_count", "total_runs", 
                    "highest_score", "batting_average", "strike_rate", "total_fours", "total_sixes"
                ]].rename(columns={
                    "player_name": "Player",
                    "team_name": "Team",
                    "role": "Role",
                    "innings_count": "Inn",
                    "total_runs": "Runs",
                    "highest_score": "HS",
                    "batting_average": "Avg",
                    "strike_rate": "SR",
                    "total_fours": "4s",
                    "total_sixes": "6s",
                }),
                hide_index=True,
                use_container_width=True,
                column_config={
                    "Avg": st.column_config.NumberColumn("Avg", format="%.2f"),
                    "SR": st.column_config.NumberColumn("SR", format="%.2f"),
                },
            )

            if not filtered_bat.empty:
                c_sel_lb, c_btn_lb = st.columns([3, 1.5])
                with c_sel_lb:
                    lead_batter_id = st.selectbox(
                        "Inspect Batter Career Profile:",
                        options=filtered_bat["player_id"].tolist(),
                        format_func=lambda pid: filtered_bat[filtered_bat["player_id"] == pid]["player_name"].values[0],
                        key="sel_lead_bat",
                    )
                with c_btn_lb:
                    st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
                    if st.button("Open Player Profile 👤", key="btn_lead_bat", use_container_width=True):
                        navigate_to("👤 Player Profiles", player_id=int(lead_batter_id))

        elif board_type == "🎯 Bowling Leaderboard":
            bowl_board = queries.get_all_bowling_leaderboard()

            f1, f2 = st.columns(2)
            with f1:
                teams_b_filter = ["All Teams"] + sorted(bowl_board["team_name"].unique().tolist())
                selected_team_b_filter = st.selectbox("Filter by Team:", teams_b_filter, key="bowl_filt_team")
            with f2:
                min_wkts = st.slider("Minimum Wickets:", 0, int(bowl_board["wickets_taken"].max() if not bowl_board.empty else 10), 0, key="bowl_filt_wkts")

            filtered_bowl = bowl_board.copy()
            if selected_team_b_filter != "All Teams":
                filtered_bowl = filtered_bowl[filtered_bowl["team_name"] == selected_team_b_filter]
            filtered_bowl = filtered_bowl[filtered_bowl["wickets_taken"] >= min_wkts]

            st.markdown(f"**Showing {len(filtered_bowl)} Bowlers**")
            st.dataframe(
                filtered_bowl[[
                    "player_name", "team_name", "bowling_style", "innings_bowled",
                    "balls_bowled", "maidens", "runs_conceded", "wickets_taken", "economy_rate", "bowling_average"
                ]].rename(columns={
                    "player_name": "Player",
                    "team_name": "Team",
                    "bowling_style": "Style",
                    "innings_bowled": "Inn",
                    "balls_bowled": "Balls",
                    "maidens": "Mdns",
                    "runs_conceded": "Runs",
                    "wickets_taken": "Wkts",
                    "economy_rate": "Econ",
                    "bowling_average": "Avg",
                }),
                hide_index=True,
                use_container_width=True,
                column_config={
                    "Econ": st.column_config.NumberColumn("Econ", format="%.2f"),
                    "Avg": st.column_config.NumberColumn("Avg", format="%.2f"),
                },
            )

            if not filtered_bowl.empty:
                c_sel_lbb, c_btn_lbb = st.columns([3, 1.5])
                with c_sel_lbb:
                    lead_bowler_id = st.selectbox(
                        "Inspect Bowler Career Profile:",
                        options=filtered_bowl["player_id"].tolist(),
                        format_func=lambda pid: filtered_bowl[filtered_bowl["player_id"] == pid]["player_name"].values[0],
                        key="sel_lead_bowl",
                    )
                with c_btn_lbb:
                    st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
                    if st.button("Open Bowler Profile 🎯", key="btn_lead_bowl", use_container_width=True):
                        navigate_to("👤 Player Profiles", player_id=int(lead_bowler_id))

        else:
            field_board = queries.get_all_fielding_leaderboard()
            st.dataframe(
                field_board[[
                    "player_name", "team_name", "role", "catches", "stumpings", "run_outs", "total_dismissals"
                ]].rename(columns={
                    "player_name": "Player",
                    "team_name": "Team",
                    "role": "Role",
                    "catches": "Catches",
                    "stumpings": "Stumpings",
                    "run_outs": "Run Outs",
                    "total_dismissals": "Total Dismissals",
                }),
                hide_index=True,
                use_container_width=True,
            )

            if not field_board.empty:
                c_sel_lbf, c_btn_lbf = st.columns([3, 1.5])
                with c_sel_lbf:
                    lead_fielder_id = st.selectbox(
                        "Inspect Fielder Career Profile:",
                        options=field_board["player_id"].tolist(),
                        format_func=lambda pid: field_board[field_board["player_id"] == pid]["player_name"].values[0],
                        key="sel_lead_field",
                    )
                with c_btn_lbf:
                    st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
                    if st.button("Open Fielder Profile 🧤", key="btn_lead_field", use_container_width=True):
                        navigate_to("👤 Player Profiles", player_id=int(lead_fielder_id))

    # =========================================================================
    # 4. Stadium Deep-Dive Tab
    # =========================================================================
    with tab_venues:
        st.markdown("#### Stadium & Venue Intelligence")
        venues_df = queries.get_venue_statistics()

        if venues_df.empty:
            st.info("No venue records available.")
        else:
            col_v1, col_v2 = st.columns([1.2, 0.8])
            with col_v1:
                fig_v_cap = px.bar(
                    venues_df,
                    x="venue_name",
                    y="capacity",
                    text="capacity",
                    color="matches_played",
                    title="Stadium Capacity & Matches Hosted",
                    labels={"venue_name": "Stadium", "capacity": "Capacity", "matches_played": "Matches"},
                )
                fig_v_cap.update_layout(xaxis_tickangle=-25, height=340, margin=dict(l=20, r=20, t=40, b=80))
                st.plotly_chart(fig_v_cap, use_container_width=True)

            with col_v2:
                fig_v_scores = px.scatter(
                    venues_df,
                    x="avg_1st_innings_score",
                    y="avg_2nd_innings_score",
                    size="capacity",
                    color="venue_name",
                    hover_name="city",
                    title="1st vs 2nd Innings Scoring Pattern",
                    labels={
                        "avg_1st_innings_score": "Avg 1st Innings Runs",
                        "avg_2nd_innings_score": "Avg 2nd Innings Runs",
                    },
                )
                fig_v_scores.update_layout(height=340, showlegend=False, margin=dict(l=20, r=20, t=40, b=20))
                st.plotly_chart(fig_v_scores, use_container_width=True)

            st.dataframe(
                venues_df.rename(columns={
                    "venue_name": "Venue",
                    "city": "City",
                    "capacity": "Capacity",
                    "matches_played": "Matches",
                    "avg_1st_innings_score": "Avg 1st Inn",
                    "avg_2nd_innings_score": "Avg 2nd Inn",
                    "highest_innings_score": "Highest Score",
                }),
                hide_index=True,
                use_container_width=True,
            )
