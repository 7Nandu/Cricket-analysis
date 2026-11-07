"""
Match Centre View.
Displays fixture listings, interactive scorecard selector, batting/bowling innings details,
and ball-by-ball analysis.
"""
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from components.navbar import navigate_to
from components.ui_cards import render_metric_card
import queries


def render_match_centre_view():
    """Renders the Match Centre interface."""
    st.markdown("### 🏏 Match Centre & Official Scorecards")

    # Fetch all matches for the dropdown/selector
    matches_df = queries.get_matches_list()
    if matches_df.empty:
        st.warning("No matches found in the database.")
        return

    match_ids = matches_df["match_id"].tolist()

    # Fallback initialization
    if "selected_match_id" not in st.session_state or st.session_state.selected_match_id not in match_ids:
        st.session_state.selected_match_id = match_ids[0]

    # Format selector labels
    match_options = {}
    for _, row in matches_df.iterrows():
        label = f"Match {row['match_id']} | {row['match_date']} | {row['home_team']} vs {row['away_team']} ({row['city']})"
        match_options[row["match_id"]] = label

    # Top fixture selection row with Prev / Next buttons
    c_prev, c_sel, c_next = st.columns([1, 4, 1])
    current_idx = match_ids.index(st.session_state.selected_match_id)

    with c_prev:
        st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
        prev_disabled = current_idx == 0
        if st.button("⬅️ Prev Match", key=f"btn_prev_m_{st.session_state.selected_match_id}", disabled=prev_disabled, use_container_width=True):
            st.session_state.selected_match_id = match_ids[current_idx - 1]
            st.rerun()

    with c_sel:
        selected_match_id = st.selectbox(
            label="Select Match Fixture",
            options=match_ids,
            index=current_idx,
            format_func=lambda mid: match_options.get(mid, f"Match {mid}"),
            key=f"match_sel_box_{st.session_state.selected_match_id}",
        )
        if selected_match_id != st.session_state.selected_match_id:
            st.session_state.selected_match_id = selected_match_id
            st.rerun()

    with c_next:
        st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
        next_disabled = current_idx == len(match_ids) - 1
        if st.button("Next Match ➡️", key=f"btn_next_m_{st.session_state.selected_match_id}", disabled=next_disabled, use_container_width=True):
            st.session_state.selected_match_id = match_ids[current_idx + 1]
            st.rerun()

    # Fetch match details and innings
    match_details = queries.get_match_details(st.session_state.selected_match_id)
    if not match_details:
        st.error("Match record could not be loaded.")
        return

    # 1. Match Header Card
    st.markdown(
        f"""
        <div style="background: #ffffff; border: 1px solid #cbd5e1; border-radius: 12px; padding: 1.2rem; margin: 1rem 0; box-shadow: 0 2px 4px rgba(0,0,0,0.04);">
            <div style="display: flex; justify-content: space-between; color: #64748b; font-size: 0.85rem; margin-bottom: 0.5rem;">
                <span>🗓️ <strong>{match_details['match_date']}</strong> | Format: <strong>{match_details['match_format']}</strong></span>
                <span>🏟️ <strong>{match_details['venue_name']}</strong>, {match_details['city']} (Cap: {match_details['capacity']:,})</span>
            </div>
            <div style="display: flex; align-items: center; justify-content: space-between; margin: 0.5rem 0;">
                <div style="font-size: 1.4rem; font-weight: 700; color: #0f172a;">
                    {match_details['home_team']} <span style="color: #94a3b8; font-weight: 400; font-size: 1.1rem;">vs</span> {match_details['away_team']}
                </div>
            </div>
            <div style="margin-top: 0.5rem; font-size: 1rem; color: #059669; font-weight: 600;">
                🏆 {match_details['result_summary']}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # 2. Innings Breakdown
    innings_df = queries.get_match_innings_data(st.session_state.selected_match_id)
    if innings_df.empty:
        st.info("No innings data recorded for this match.")
        return

    # Tabs for each innings + Ball-by-Ball
    tabs_list = [f"Innings {row['innings_number']}: {row['batting_team']}" for _, row in innings_df.iterrows()]
    tabs_list.append("📊 Deliveries & Ball-by-Ball")
    tabs = st.tabs(tabs_list)

    # Render each innings tab
    for i, (_, inn_row) in enumerate(innings_df.iterrows()):
        with tabs[i]:
            inn_id = int(inn_row["innings_id"])
            batting_team = inn_row["batting_team"]
            
            # Innings summary metrics
            m1, m2, m3, m4 = st.columns(4)
            with m1:
                render_metric_card("Total Runs", inn_row["total_runs"], f"{batting_team} Innings", "🏏")
            with m2:
                render_metric_card("Wickets Lost", f"{inn_row['wickets_lost']} / 10", "Fall of Wickets", "🎯")
            with m3:
                render_metric_card("Overs Bowled", f"{inn_row['overs_played']} ov", f"{inn_row['balls_bowled']} balls", "⏱️")
            with m4:
                render_metric_card("Run Rate", f"{inn_row['run_rate']}", "Runs Per Over", "⚡")

            st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)

            # Batting Scorecard
            st.markdown("#### 🏏 Batting Scorecard")
            batting_card = queries.get_innings_batting_scorecard(inn_id)
            if batting_card.empty:
                st.info("No individual batting entries recorded.")
            else:
                display_bat = batting_card.copy()
                display_bat["Player"] = display_bat["batter_name"]
                display_bat["Pos"] = display_bat["batting_position"].fillna("-")
                display_bat["Dismissal"] = display_bat["dismissal"]
                display_bat["R"] = display_bat["runs_scored"]
                display_bat["B"] = display_bat["balls_faced"]
                display_bat["4s"] = display_bat["fours"]
                display_bat["6s"] = display_bat["sixes"]
                display_bat["SR"] = display_bat["strike_rate"].fillna(0.0)

                st.dataframe(
                    display_bat[["Pos", "Player", "Dismissal", "R", "B", "4s", "6s", "SR"]],
                    hide_index=True,
                    use_container_width=True,
                    column_config={
                        "SR": st.column_config.NumberColumn("SR", format="%.2f"),
                    },
                )

                # Quick player jump selector
                col_sel, col_btn = st.columns([3, 1.5])
                with col_sel:
                    selected_batter = st.selectbox(
                        "Inspect Batter Career Profile:",
                        options=batting_card["player_id"].tolist(),
                        format_func=lambda pid: batting_card[batting_card["player_id"] == pid]["batter_name"].values[0],
                        key=f"sel_bat_{inn_id}",
                    )
                with col_btn:
                    st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
                    if st.button("Open Batter Profile 👤", key=f"btn_p_bat_{inn_id}", use_container_width=True):
                        navigate_to("👤 Player Profiles", player_id=int(selected_batter))

            st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)

            # Bowling Scorecard
            st.markdown("#### 🎯 Bowling Figures")
            bowling_card = queries.get_innings_bowling_scorecard(inn_id)
            if bowling_card.empty:
                st.info("No bowling entries recorded.")
            else:
                display_bowl = bowling_card.copy()
                display_bowl["Bowler"] = display_bowl["bowler_name"]
                display_bowl["O"] = display_bowl["overs_bowled"]
                display_bowl["M"] = display_bowl["maidens"]
                display_bowl["R"] = display_bowl["runs_conceded"]
                display_bowl["W"] = display_bowl["wickets_taken"]
                display_bowl["Econ"] = display_bowl["economy_rate"].fillna(0.0)

                st.dataframe(
                    display_bowl[["Bowler", "O", "M", "R", "W", "Econ"]],
                    hide_index=True,
                    use_container_width=True,
                    column_config={
                        "Econ": st.column_config.NumberColumn("Econ", format="%.2f"),
                    },
                )

                # Quick bowler jump selector
                col_b_sel, col_b_btn = st.columns([3, 1.5])
                with col_b_sel:
                    selected_bowler = st.selectbox(
                        "Inspect Bowler Career Profile:",
                        options=bowling_card["player_id"].tolist(),
                        format_func=lambda pid: bowling_card[bowling_card["player_id"] == pid]["bowler_name"].values[0],
                        key=f"sel_bowl_{inn_id}",
                    )
                with col_b_btn:
                    st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
                    if st.button("Open Bowler Profile 🎯", key=f"btn_p_bowl_{inn_id}", use_container_width=True):
                        navigate_to("👤 Player Profiles", player_id=int(selected_bowler))

    # Deliveries Tab
    with tabs[-1]:
        st.markdown("#### 🔍 Ball-by-Ball Analysis (Database Records)")
        deliveries_df = queries.get_match_deliveries(st.session_state.selected_match_id)

        if deliveries_df.empty:
            st.info(
                f"Detailed ball-by-ball delivery events have not been logged for Match {st.session_state.selected_match_id}. "
                "The database contains high-level innings, batting, and bowling scorecards."
            )
        else:
            st.success(f"Loaded **{len(deliveries_df)}** delivery records for Match {st.session_state.selected_match_id}")

            # Over-by-over summary chart
            over_summary = (
                deliveries_df.groupby(["innings_number", "over_number"])["total_runs"]
                .sum()
                .reset_index()
            )
            fig_overs = px.bar(
                over_summary,
                x="over_number",
                y="total_runs",
                color="innings_number",
                barmode="group",
                title="Runs Scored Per Over",
                labels={"over_number": "Over Number", "total_runs": "Runs", "innings_number": "Innings"},
            )
            fig_overs.update_layout(height=280, margin=dict(l=20, r=20, t=40, b=20))
            st.plotly_chart(fig_overs, use_container_width=True)

            # Deliveries raw log table
            st.markdown("##### Delivery Log")
            disp_del = deliveries_df[[
                "innings_number", "over_number", "ball_number", "striker", "bowler", 
                "runs_batter", "extras", "total_runs", "wicket_type"
            ]].rename(columns={
                "innings_number": "Inn",
                "over_number": "Over",
                "ball_number": "Ball",
                "striker": "Striker",
                "bowler": "Bowler",
                "runs_batter": "Bat Runs",
                "extras": "Extras",
                "total_runs": "Total",
                "wicket_type": "Wicket",
            })
            st.dataframe(disp_del, hide_index=True, use_container_width=True)
