"""
Player Profile View.
Displays biographical details, career batting/bowling/fielding statistics,
interactive performance charts, and match-by-match logs.
"""
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from components.navbar import navigate_to
from components.ui_cards import get_role_badge, render_metric_card
import queries


def render_player_profile_view():
    """Renders the comprehensive Player Profile interface."""
    st.markdown("### 👤 Player Career & Performance Profile")

    # Fetch all players for dropdown
    all_players = queries.get_all_players()
    if all_players.empty:
        st.warning("No players found in the database.")
        return

    player_ids = all_players["player_id"].tolist()

    # Fallback initialization
    if "selected_player_id" not in st.session_state or st.session_state.selected_player_id not in player_ids:
        st.session_state.selected_player_id = player_ids[0]

    # Dropdown selector options
    player_options = {}
    for _, row in all_players.iterrows():
        label = f"{row['full_name']} ({row['role'].title()} | {row['team_name']})"
        player_options[row["player_id"]] = label

    c_prev, c_sel, c_next = st.columns([1, 4, 1])
    current_idx = player_ids.index(st.session_state.selected_player_id)

    with c_prev:
        st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
        prev_disabled = current_idx == 0
        if st.button("⬅️ Prev Player", key=f"btn_prev_p_{st.session_state.selected_player_id}", disabled=prev_disabled, use_container_width=True):
            st.session_state.selected_player_id = player_ids[current_idx - 1]
            st.rerun()

    with c_sel:
        selected_player_id = st.selectbox(
            label="Select Player",
            options=player_ids,
            index=current_idx,
            format_func=lambda pid: player_options.get(pid, f"Player {pid}"),
            key=f"player_sel_box_{st.session_state.selected_player_id}",
        )
        if selected_player_id != st.session_state.selected_player_id:
            st.session_state.selected_player_id = selected_player_id
            st.rerun()

    with c_next:
        st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
        next_disabled = current_idx == len(player_ids) - 1
        if st.button("Next Player ➡️", key=f"btn_next_p_{st.session_state.selected_player_id}", disabled=next_disabled, use_container_width=True):
            st.session_state.selected_player_id = player_ids[current_idx + 1]
            st.rerun()

    # Fetch player details
    bio = queries.get_player_bio(st.session_state.selected_player_id)
    if not bio:
        st.error("Player record could not be loaded.")
        return

    bat_summary = queries.get_player_batting_summary(st.session_state.selected_player_id)
    bowl_summary = queries.get_player_bowling_summary(st.session_state.selected_player_id)
    field_summary = queries.get_player_fielding_summary(st.session_state.selected_player_id)

    # 1. Player Bio Banner
    col_bio1, col_bio2 = st.columns([2.5, 1.5])
    with col_bio1:
        st.markdown(
            f"""
            <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; padding: 1.2rem; box-shadow: 0 1px 3px rgba(0,0,0,0.05); margin-bottom: 1rem;">
                <div style="display: flex; align-items: center; gap: 0.8rem; margin-bottom: 0.5rem;">
                    <h2 style="margin: 0; font-size: 1.6rem; color: #0f172a;">{bio['full_name']}</h2>
                    {get_role_badge(bio['role'])}
                </div>
                <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 0.6rem; font-size: 0.9rem; color: #334155; margin-top: 0.8rem;">
                    <div>🛡️ <strong>Franchise:</strong> {bio['team_name']}</div>
                    <div>🎂 <strong>Date of Birth:</strong> {bio['date_of_birth']} ({bio['age']} yrs)</div>
                    <div>🏏 <strong>Batting Style:</strong> {bio['batting_style']}</div>
                    <div>🎯 <strong>Bowling Style:</strong> {bio['bowling_style'] or 'N/A'}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col_bio2:
        st.markdown(
            f"""
            <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 12px; padding: 1.2rem; box-shadow: 0 1px 3px rgba(0,0,0,0.05); margin-bottom: 1rem;">
                <div style="font-size: 0.85rem; font-weight: 600; color: #64748b; text-transform: uppercase;">Team Management</div>
                <div style="font-size: 1.1rem; font-weight: 700; color: #0f172a; margin-top: 0.4rem;">{bio['team_name']}</div>
                <div style="font-size: 0.85rem; color: #475569; margin-top: 0.3rem;">Head Coach: <strong>{bio['coach']}</strong></div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("View Franchise Page 🛡️", key=f"btn_view_franchise_{bio['team_id']}", use_container_width=True):
            navigate_to("🛡️ Teams", team_id=int(bio["team_id"]))

    # 2. Career Summary Metrics
    st.markdown("#### 📊 Career Aggregate Statistics")
    m1, m2, m3, m4, m5, m6 = st.columns(6)

    total_runs = bat_summary.get("total_runs", 0) if bat_summary else 0
    bat_avg = bat_summary.get("batting_average", "-") if bat_summary else "-"
    bat_sr = bat_summary.get("strike_rate", "-") if bat_summary else "-"
    highest = bat_summary.get("highest_score", 0) if bat_summary else 0

    wickets = bowl_summary.get("wickets_taken", 0) if bowl_summary else 0
    economy = bowl_summary.get("economy_rate", "-") if bowl_summary else "-"
    catches = field_summary.get("catches", 0) if field_summary else 0

    with m1:
        render_metric_card("Runs Scored", total_runs, f"HS: {highest}", "🏏")
    with m2:
        render_metric_card("Batting Avg", bat_avg if bat_avg is not None else "-", "Runs/Dismissal", "📈")
    with m3:
        render_metric_card("Strike Rate", bat_sr if bat_sr is not None else "-", "Per 100 Balls", "⚡")
    with m4:
        render_metric_card("Wickets", wickets, "Dismissals Taken", "🎯")
    with m5:
        render_metric_card("Economy", economy if economy is not None else "-", "Runs/Over", "📉")
    with m6:
        render_metric_card("Catches", catches, "Fielding Dismissals", "🧤")

    st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)

    # 3. Match Logs and Visualizations
    tab_bat, tab_bowl, tab_field = st.tabs(["🏏 Batting Breakdown", "🎯 Bowling Breakdown", "🧤 Fielding Summary"])

    # Batting Tab
    with tab_bat:
        bat_log = queries.get_player_batting_match_log(st.session_state.selected_player_id)
        if bat_log.empty:
            st.info("No batting innings recorded for this player in the database.")
        else:
            col_chart1, col_chart2 = st.columns(2)

            with col_chart1:
                fig_runs = px.bar(
                    bat_log,
                    x="opposition",
                    y="runs_scored",
                    text="runs_scored",
                    title="Runs Scored by Opponent",
                    color="runs_scored",
                    color_continuous_scale="Blues",
                    labels={"opposition": "Opponent", "runs_scored": "Runs"},
                )
                fig_runs.update_layout(height=280, margin=dict(l=20, r=20, t=40, b=20), coloraxis_showscale=False)
                fig_runs.update_traces(textposition="outside")
                st.plotly_chart(fig_runs, use_container_width=True)

            with col_chart2:
                # Boundary breakdown
                fours_runs = int(bat_log["fours"].sum()) * 4
                sixes_runs = int(bat_log["sixes"].sum()) * 6
                other_runs = max(0, total_runs - (fours_runs + sixes_runs))

                labels = ["Runs in Fours (4s)", "Runs in Sixes (6s)", "Singles/Doubles"]
                values = [fours_runs, sixes_runs, other_runs]

                fig_pie = go.Figure(
                    data=[
                        go.Pie(
                            labels=labels,
                            values=values,
                            hole=0.45,
                            marker_colors=["#0284c7", "#f97316", "#10b981"],
                        )
                    ]
                )
                fig_pie.update_layout(
                    title="Run Distribution (Boundary vs Running)",
                    height=280,
                    margin=dict(l=20, r=20, t=40, b=20),
                )
                st.plotly_chart(fig_pie, use_container_width=True)

            st.markdown("##### Match-by-Match Batting Log")
            disp_bat = bat_log[[
                "match_id", "match_date", "opposition", "venue_name", "batting_position",
                "runs_scored", "balls_faced", "fours", "sixes", "strike_rate", "dismissal"
            ]].rename(columns={
                "match_date": "Date",
                "opposition": "Opposition",
                "venue_name": "Venue",
                "batting_position": "Pos",
                "runs_scored": "Runs",
                "balls_faced": "Balls",
                "fours": "4s",
                "sixes": "6s",
                "strike_rate": "SR",
                "dismissal": "Dismissal",
            })
            st.dataframe(disp_bat.drop(columns=["match_id"]), hide_index=True, use_container_width=True)

            # Jump to match scorecard button
            c_sel_m, c_btn_m = st.columns([3, 1.5])
            with c_sel_m:
                selected_match_to_view = st.selectbox(
                    "Inspect Match Scorecard:",
                    options=bat_log["match_id"].tolist(),
                    format_func=lambda mid: f"Match {mid} vs {bat_log[bat_log['match_id'] == mid]['opposition'].values[0]} ({bat_log[bat_log['match_id'] == mid]['match_date'].values[0]})",
                    key=f"p_view_match_bat_{st.session_state.selected_player_id}",
                )
            with c_btn_m:
                st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
                if st.button("Open Match Scorecard 🏏", key=f"btn_open_m_bat_{st.session_state.selected_player_id}", use_container_width=True):
                    navigate_to("🏏 Match Centre", match_id=int(selected_match_to_view))

    # Bowling Tab
    with tab_bowl:
        bowl_log = queries.get_player_bowling_match_log(st.session_state.selected_player_id)
        if bowl_log.empty:
            st.info("No bowling spells recorded for this player in the database.")
        else:
            col_b1, col_b2 = st.columns(2)
            with col_b1:
                fig_wkts = px.bar(
                    bowl_log,
                    x="opposition",
                    y="wickets_taken",
                    text="wickets_taken",
                    title="Wickets Taken by Opponent",
                    color="wickets_taken",
                    color_continuous_scale="Purples",
                    labels={"opposition": "Opponent", "wickets_taken": "Wickets"},
                )
                fig_wkts.update_layout(height=280, margin=dict(l=20, r=20, t=40, b=20), coloraxis_showscale=False)
                fig_wkts.update_traces(textposition="outside")
                st.plotly_chart(fig_wkts, use_container_width=True)

            with col_b2:
                fig_econ = px.line(
                    bowl_log,
                    x="opposition",
                    y="economy_rate",
                    markers=True,
                    title="Economy Rate Progression",
                    labels={"opposition": "Opponent", "economy_rate": "Economy (RPO)"},
                )
                fig_econ.update_traces(line_color="#7e22ce")
                fig_econ.update_layout(height=280, margin=dict(l=20, r=20, t=40, b=20))
                st.plotly_chart(fig_econ, use_container_width=True)

            st.markdown("##### Match-by-Match Bowling Log")
            disp_bowl = bowl_log[[
                "match_id", "match_date", "opposition", "venue_name", "overs_bowled",
                "maidens", "runs_conceded", "wickets_taken", "economy_rate"
            ]].rename(columns={
                "match_date": "Date",
                "opposition": "Opposition",
                "venue_name": "Venue",
                "overs_bowled": "Overs",
                "maidens": "Maidens",
                "runs_conceded": "Runs",
                "wickets_taken": "Wickets",
                "economy_rate": "Economy",
            })
            st.dataframe(disp_bowl.drop(columns=["match_id"]), hide_index=True, use_container_width=True)

            c_sel_mb, c_btn_mb = st.columns([3, 1.5])
            with c_sel_mb:
                selected_match_bowl_view = st.selectbox(
                    "Inspect Match Scorecard:",
                    options=bowl_log["match_id"].tolist(),
                    format_func=lambda mid: f"Match {mid} vs {bowl_log[bowl_log['match_id'] == mid]['opposition'].values[0]} ({bowl_log[bowl_log['match_id'] == mid]['match_date'].values[0]})",
                    key=f"p_view_match_bowl_{st.session_state.selected_player_id}",
                )
            with c_btn_mb:
                st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
                if st.button("Open Match Scorecard 🎯", key=f"btn_open_m_bowl_{st.session_state.selected_player_id}", use_container_width=True):
                    navigate_to("🏏 Match Centre", match_id=int(selected_match_bowl_view))

    # Fielding Tab
    with tab_field:
        if not field_summary:
            st.info("No fielding dismissals recorded for this player in the database.")
        else:
            f1, f2, f3, f4 = st.columns(4)
            with f1:
                render_metric_card("Catches", field_summary.get("catches", 0), "Fielding Catches", "🧤")
            with f2:
                render_metric_card("Stumpings", field_summary.get("stumpings", 0), "Wicketkeeper Stumpings", "⚡")
            with f3:
                render_metric_card("Run Outs", field_summary.get("run_outs", 0), "Direct / Assisted Hits", "🎯")
            with f4:
                render_metric_card("Total Dismissals", field_summary.get("total_dismissals", 0), "Total Field Impact", "⭐")
