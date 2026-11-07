"""
SQL Queries module for Cricket Analytics Web Application.
All queries are parameterized to prevent SQL injection and use the actual database schema and views.
"""
from typing import Any, Dict, List, Optional
import pandas as pd
from database import execute_query, execute_one


# =============================================================================
# 1. HOME & OVERVIEW
# =============================================================================

def get_kpis() -> Dict[str, Any]:
    """Fetch high-level KPI counts for the dashboard overview."""
    query = """
    SELECT 
        (SELECT COUNT(*) FROM MATCHES) AS total_matches,
        (SELECT COUNT(*) FROM TEAMS) AS total_teams,
        (SELECT COUNT(*) FROM PLAYERS) AS total_players,
        (SELECT COUNT(*) FROM VENUES) AS total_venues,
        (SELECT COALESCE(SUM(total_runs), 0) FROM INNINGS) AS total_runs,
        (SELECT COALESCE(SUM(wickets_lost), 0) FROM INNINGS) AS total_wickets;
    """
    row = execute_one(query)
    return row or {
        "total_matches": 0,
        "total_teams": 0,
        "total_players": 0,
        "total_venues": 0,
        "total_runs": 0,
        "total_wickets": 0,
    }


def get_standings() -> pd.DataFrame:
    """Fetch team standings from TEAM_PERFORMANCE view."""
    query = """
    SELECT 
        team_id,
        team_name,
        matches_played,
        wins,
        losses,
        win_percentage
    FROM TEAM_PERFORMANCE
    ORDER BY wins DESC, win_percentage DESC;
    """
    return execute_query(query)


def get_top_run_scorers(limit: int = 5) -> pd.DataFrame:
    """Fetch top run scorers from TOP_RUN_SCORERS view."""
    query = """
    SELECT 
        player_id,
        player_name,
        team_name,
        innings_played,
        total_runs,
        highest_score,
        batting_average,
        strike_rate,
        fours,
        sixes
    FROM TOP_RUN_SCORERS
    ORDER BY total_runs DESC
    LIMIT %s;
    """
    return execute_query(query, (limit,))


def get_top_wicket_takers(limit: int = 5) -> pd.DataFrame:
    """Fetch top wicket takers from TOP_WICKET_TAKERS view."""
    query = """
    SELECT 
        player_id,
        player_name,
        team_name,
        innings_bowled,
        total_wickets,
        runs_conceded,
        economy_rate,
        bowling_average
    FROM TOP_WICKET_TAKERS
    ORDER BY total_wickets DESC, economy_rate ASC
    LIMIT %s;
    """
    return execute_query(query, (limit,))


def get_recent_matches(limit: int = 10) -> pd.DataFrame:
    """Fetch recent matches from MATCH_SCORECARD view."""
    query = """
    SELECT 
        match_id,
        match_date,
        venue_name,
        city,
        home_team,
        away_team,
        first_batting_team,
        first_innings_score,
        second_batting_team,
        second_innings_score,
        result_summary
    FROM MATCH_SCORECARD
    ORDER BY match_date DESC
    LIMIT %s;
    """
    return execute_query(query, (limit,))


def get_venue_statistics() -> pd.DataFrame:
    """Fetch venue stats from VENUE_STATISTICS view."""
    query = """
    SELECT 
        venue_id,
        venue_name,
        city,
        capacity,
        matches_played,
        avg_1st_innings_score,
        avg_2nd_innings_score,
        highest_innings_score
    FROM VENUE_STATISTICS
    ORDER BY matches_played DESC, avg_1st_innings_score DESC;
    """
    return execute_query(query)


# =============================================================================
# 2. GLOBAL SEARCH
# =============================================================================

def search_players(term: str) -> pd.DataFrame:
    """Search players by name, role, batting style, or team name."""
    query = """
    SELECT 
        p.player_id,
        p.full_name,
        p.role,
        p.batting_style,
        p.bowling_style,
        t.team_name,
        t.team_id
    FROM PLAYERS p
    JOIN TEAMS t ON p.team_id = t.team_id
    WHERE p.full_name ILIKE %s 
       OR p.role ILIKE %s 
       OR t.team_name ILIKE %s
    ORDER BY p.full_name ASC;
    """
    pattern = f"%{term}%"
    return execute_query(query, (pattern, pattern, pattern))


def search_teams(term: str) -> pd.DataFrame:
    """Search teams by name or coach."""
    query = """
    SELECT 
        team_id,
        team_name,
        country,
        coach
    FROM TEAMS
    WHERE team_name ILIKE %s OR coach ILIKE %s
    ORDER BY team_name ASC;
    """
    pattern = f"%{term}%"
    return execute_query(query, (pattern, pattern))


def search_venues(term: str) -> pd.DataFrame:
    """Search venues by stadium name or city."""
    query = """
    SELECT 
        venue_id,
        venue_name,
        city,
        country,
        capacity
    FROM VENUES
    WHERE venue_name ILIKE %s OR city ILIKE %s
    ORDER BY venue_name ASC;
    """
    pattern = f"%{term}%"
    return execute_query(query, (pattern, pattern))


def search_matches(term: str) -> pd.DataFrame:
    """Search matches by participating teams, venue, or result."""
    query = """
    SELECT 
        m.match_id,
        m.match_date,
        v.venue_name,
        v.city,
        ht.team_name AS home_team,
        at.team_name AS away_team,
        m.result_summary
    FROM MATCHES m
    JOIN VENUES v ON m.venue_id = v.venue_id
    JOIN TEAMS ht ON m.home_team_id = ht.team_id
    JOIN TEAMS at ON m.away_team_id = at.team_id
    WHERE ht.team_name ILIKE %s 
       OR at.team_name ILIKE %s 
       OR v.venue_name ILIKE %s 
       OR v.city ILIKE %s
       OR m.result_summary ILIKE %s
    ORDER BY m.match_date DESC;
    """
    pattern = f"%{term}%"
    return execute_query(query, (pattern, pattern, pattern, pattern, pattern))


# =============================================================================
# 3. PLAYER PROFILES
# =============================================================================

def get_all_players() -> pd.DataFrame:
    """Get list of all players for dropdown selectors."""
    query = """
    SELECT 
        p.player_id,
        p.full_name,
        p.role,
        t.team_name,
        t.team_id
    FROM PLAYERS p
    JOIN TEAMS t ON p.team_id = t.team_id
    ORDER BY p.full_name ASC;
    """
    return execute_query(query)


def get_player_bio(player_id: int) -> Optional[Dict[str, Any]]:
    """Get core biographical data for a player."""
    query = """
    SELECT 
        p.player_id,
        p.full_name,
        p.date_of_birth,
        EXTRACT(YEAR FROM AGE(CURRENT_DATE, p.date_of_birth))::INT AS age,
        p.role,
        p.batting_style,
        p.bowling_style,
        t.team_id,
        t.team_name,
        t.coach
    FROM PLAYERS p
    JOIN TEAMS t ON p.team_id = t.team_id
    WHERE p.player_id = %s;
    """
    return execute_one(query, (player_id,))


def get_player_batting_summary(player_id: int) -> Optional[Dict[str, Any]]:
    """Career batting summary for a player."""
    query = """
    SELECT * 
    FROM PLAYER_BATTING_SUMMARY
    WHERE player_id = %s;
    """
    return execute_one(query, (player_id,))


def get_player_bowling_summary(player_id: int) -> Optional[Dict[str, Any]]:
    """Career bowling summary for a player."""
    query = """
    SELECT * 
    FROM PLAYER_BOWLING_SUMMARY
    WHERE player_id = %s;
    """
    return execute_one(query, (player_id,))


def get_player_fielding_summary(player_id: int) -> Optional[Dict[str, Any]]:
    """Career fielding summary for a player."""
    query = """
    SELECT * 
    FROM PLAYER_FIELDING_SUMMARY
    WHERE player_id = %s;
    """
    return execute_one(query, (player_id,))


def get_player_batting_match_log(player_id: int) -> pd.DataFrame:
    """Individual match-by-match batting performance."""
    query = """
    SELECT 
        m.match_id,
        m.match_date,
        v.venue_name,
        opp.team_name AS opposition,
        bp.batting_position,
        bp.runs_scored,
        bp.balls_faced,
        bp.fours,
        bp.sixes,
        bp.dismissal,
        bp.not_out,
        ROUND((bp.runs_scored::NUMERIC * 100.0) / NULLIF(bp.balls_faced, 0), 2) AS strike_rate
    FROM BATTING_PERFORMANCE bp
    JOIN INNINGS i ON bp.innings_id = i.innings_id
    JOIN MATCHES m ON i.match_id = m.match_id
    JOIN VENUES v ON m.venue_id = v.venue_id
    JOIN TEAMS opp ON (opp.team_id = CASE 
        WHEN m.home_team_id = i.batting_team_id THEN m.away_team_id 
        ELSE m.home_team_id END)
    WHERE bp.player_id = %s
    ORDER BY m.match_date ASC;
    """
    return execute_query(query, (player_id,))


def get_player_bowling_match_log(player_id: int) -> pd.DataFrame:
    """Individual match-by-match bowling performance."""
    query = """
    SELECT 
        m.match_id,
        m.match_date,
        v.venue_name,
        opp.team_name AS opposition,
        bwp.overs_bowled,
        bwp.balls_bowled,
        bwp.maidens,
        bwp.runs_conceded,
        bwp.wickets_taken,
        ROUND(bwp.runs_conceded::NUMERIC / NULLIF(bwp.balls_bowled::NUMERIC / 6.0, 0), 2) AS economy_rate
    FROM BOWLING_PERFORMANCE bwp
    JOIN INNINGS i ON bwp.innings_id = i.innings_id
    JOIN MATCHES m ON i.match_id = m.match_id
    JOIN VENUES v ON m.venue_id = v.venue_id
    JOIN TEAMS opp ON opp.team_id = i.batting_team_id
    WHERE bwp.player_id = %s
    ORDER BY m.match_date ASC;
    """
    return execute_query(query, (player_id,))


# =============================================================================
# 4. MATCH CENTRE & SCORECARDS
# =============================================================================

def get_matches_list() -> pd.DataFrame:
    """Get list of all matches for match centre selector."""
    query = """
    SELECT 
        m.match_id,
        m.match_date,
        m.match_format,
        v.venue_name,
        v.city,
        ht.team_name AS home_team,
        at.team_name AS away_team,
        m.result_summary
    FROM MATCHES m
    JOIN VENUES v ON m.venue_id = v.venue_id
    JOIN TEAMS ht ON m.home_team_id = ht.team_id
    JOIN TEAMS at ON m.away_team_id = at.team_id
    ORDER BY m.match_date DESC;
    """
    return execute_query(query)


def get_match_details(match_id: int) -> Optional[Dict[str, Any]]:
    """Get comprehensive match details."""
    query = """
    SELECT 
        m.match_id,
        m.match_date,
        m.match_format,
        v.venue_name,
        v.city,
        v.capacity,
        ht.team_name AS home_team,
        ht.team_id AS home_team_id,
        at.team_name AS away_team,
        at.team_id AS away_team_id,
        m.result_summary
    FROM MATCHES m
    JOIN VENUES v ON m.venue_id = v.venue_id
    JOIN TEAMS ht ON m.home_team_id = ht.team_id
    JOIN TEAMS at ON m.away_team_id = at.team_id
    WHERE m.match_id = %s;
    """
    return execute_one(query, (match_id,))


def get_match_innings_data(match_id: int) -> pd.DataFrame:
    """Get innings records for a match."""
    query = """
    SELECT 
        i.innings_id,
        i.match_id,
        i.innings_number,
        i.batting_team_id,
        t.team_name AS batting_team,
        i.total_runs,
        i.wickets_lost,
        i.overs_played,
        i.balls_bowled,
        ROUND(i.total_runs::NUMERIC / NULLIF(i.balls_bowled::NUMERIC / 6.0, 0), 2) AS run_rate
    FROM INNINGS i
    JOIN TEAMS t ON i.batting_team_id = t.team_id
    WHERE i.match_id = %s
    ORDER BY i.innings_number ASC;
    """
    return execute_query(query, (match_id,))


def get_innings_batting_scorecard(innings_id: int) -> pd.DataFrame:
    """Get full batting card for an innings."""
    query = """
    SELECT 
        bp.batting_id,
        bp.batting_position,
        p.player_id,
        p.full_name AS batter_name,
        bp.dismissal,
        bp.runs_scored,
        bp.balls_faced,
        bp.fours,
        bp.sixes,
        bp.not_out,
        ROUND((bp.runs_scored::NUMERIC * 100.0) / NULLIF(bp.balls_faced, 0), 2) AS strike_rate
    FROM BATTING_PERFORMANCE bp
    JOIN PLAYERS p ON bp.player_id = p.player_id
    WHERE bp.innings_id = %s
    ORDER BY bp.batting_position ASC NULLS LAST, bp.batting_id ASC;
    """
    return execute_query(query, (innings_id,))


def get_innings_bowling_scorecard(innings_id: int) -> pd.DataFrame:
    """Get full bowling card for an innings."""
    query = """
    SELECT 
        bwp.bowling_id,
        p.player_id,
        p.full_name AS bowler_name,
        bwp.overs_bowled,
        bwp.balls_bowled,
        bwp.maidens,
        bwp.runs_conceded,
        bwp.wickets_taken,
        ROUND(bwp.runs_conceded::NUMERIC / NULLIF(bwp.balls_bowled::NUMERIC / 6.0, 0), 2) AS economy_rate
    FROM BOWLING_PERFORMANCE bwp
    JOIN PLAYERS p ON bwp.player_id = p.player_id
    WHERE bwp.innings_id = %s
    ORDER BY bwp.wickets_taken DESC, economy_rate ASC;
    """
    return execute_query(query, (innings_id,))


def get_match_deliveries(match_id: int) -> pd.DataFrame:
    """Get ball-by-ball deliveries recorded for a match."""
    query = """
    SELECT 
        d.delivery_id,
        d.innings_id,
        i.innings_number,
        bt.team_name AS batting_team,
        d.over_number,
        d.ball_number,
        sp.full_name AS striker,
        bp.full_name AS bowler,
        d.runs_batter,
        d.extras,
        d.total_runs,
        d.wicket_type
    FROM DELIVERIES d
    JOIN INNINGS i ON d.innings_id = i.innings_id
    JOIN TEAMS bt ON i.batting_team_id = bt.team_id
    JOIN PLAYERS sp ON d.striker_id = sp.player_id
    JOIN PLAYERS bp ON d.bowler_id = bp.player_id
    WHERE i.match_id = %s
    ORDER BY i.innings_number ASC, d.over_number ASC, d.ball_number ASC;
    """
    return execute_query(query, (match_id,))


# =============================================================================
# 5. TEAM PAGES
# =============================================================================

def get_all_teams() -> pd.DataFrame:
    """Get all teams with their performance summary."""
    query = """
    SELECT 
        t.team_id,
        t.team_name,
        t.country,
        t.coach,
        tp.matches_played,
        tp.wins,
        tp.losses,
        tp.win_percentage
    FROM TEAMS t
    LEFT JOIN TEAM_PERFORMANCE tp ON t.team_id = tp.team_id
    ORDER BY t.team_name ASC;
    """
    return execute_query(query)


def get_team_squad(team_id: int) -> pd.DataFrame:
    """Get all players registered in a team with their aggregated stats."""
    query = """
    SELECT 
        p.player_id,
        p.full_name,
        p.role,
        p.batting_style,
        p.bowling_style,
        COALESCE(bs.total_runs, 0) AS runs,
        COALESCE(bs.strike_rate, 0) AS batting_sr,
        COALESCE(bws.wickets_taken, 0) AS wickets,
        COALESCE(bws.economy_rate, 0) AS economy
    FROM PLAYERS p
    LEFT JOIN PLAYER_BATTING_SUMMARY bs ON p.player_id = bs.player_id
    LEFT JOIN PLAYER_BOWLING_SUMMARY bws ON p.player_id = bws.player_id
    WHERE p.team_id = %s
    ORDER BY 
        CASE p.role 
            WHEN 'batter' THEN 1 
            WHEN 'wicketkeeper' THEN 2 
            WHEN 'all-rounder' THEN 3 
            ELSE 4 
        END, 
        p.full_name ASC;
    """
    return execute_query(query, (team_id,))


def get_team_match_history(team_id: int) -> pd.DataFrame:
    """Get match history for a specific team."""
    query = """
    SELECT 
        m.match_id,
        m.match_date,
        v.venue_name,
        v.city,
        CASE WHEN m.home_team_id = %s THEN at.team_name ELSE ht.team_name END AS opponent,
        CASE WHEN m.home_team_id = %s THEN 'Home' ELSE 'Away' END AS venue_type,
        m.result_summary,
        CASE 
            WHEN m.result_summary LIKE '%%' || t.team_name || ' won%%' THEN 'Won'
            WHEN m.result_summary IS NOT NULL THEN 'Lost'
            ELSE 'No Result'
        END AS outcome
    FROM MATCHES m
    JOIN VENUES v ON m.venue_id = v.venue_id
    JOIN TEAMS ht ON m.home_team_id = ht.team_id
    JOIN TEAMS at ON m.away_team_id = at.team_id
    JOIN TEAMS t ON t.team_id = %s
    WHERE m.home_team_id = %s OR m.away_team_id = %s
    ORDER BY m.match_date DESC;
    """
    return execute_query(query, (team_id, team_id, team_id, team_id, team_id))


def get_team_innings_totals(team_id: int) -> pd.DataFrame:
    """Get innings scores for a team across matches."""
    query = """
    SELECT 
        m.match_id,
        m.match_date,
        i.innings_number,
        i.total_runs,
        i.wickets_lost,
        i.overs_played,
        ROUND(i.total_runs::NUMERIC / NULLIF(i.balls_bowled::NUMERIC / 6.0, 0), 2) AS run_rate,
        opp.team_name AS opposition
    FROM INNINGS i
    JOIN MATCHES m ON i.match_id = m.match_id
    JOIN TEAMS opp ON (opp.team_id = CASE 
        WHEN m.home_team_id = i.batting_team_id THEN m.away_team_id 
        ELSE m.home_team_id END)
    WHERE i.batting_team_id = %s
    ORDER BY m.match_date ASC;
    """
    return execute_query(query, (team_id,))


# =============================================================================
# 6. ANALYTICS & COMPARISONS
# =============================================================================

def get_head_to_head_all() -> pd.DataFrame:
    """Fetch complete head-to-head records from TEAM_HEAD_TO_HEAD."""
    query = """
    SELECT 
        team_1,
        team_2,
        total_matches,
        team_1_wins,
        team_2_wins
    FROM TEAM_HEAD_TO_HEAD
    ORDER BY total_matches DESC, team_1 ASC;
    """
    return execute_query(query)


def get_all_batting_leaderboard() -> pd.DataFrame:
    """Full tournament batting leaderboard."""
    query = """
    SELECT 
        player_id,
        player_name,
        team_name,
        role,
        innings_count,
        total_runs,
        total_balls,
        total_fours,
        total_sixes,
        highest_score,
        batting_average,
        strike_rate
    FROM PLAYER_BATTING_SUMMARY
    WHERE innings_count > 0
    ORDER BY total_runs DESC;
    """
    return execute_query(query)


def get_all_bowling_leaderboard() -> pd.DataFrame:
    """Full tournament bowling leaderboard."""
    query = """
    SELECT 
        player_id,
        player_name,
        team_name,
        bowling_style,
        innings_bowled,
        balls_bowled,
        maidens,
        runs_conceded,
        wickets_taken,
        economy_rate,
        bowling_average
    FROM PLAYER_BOWLING_SUMMARY
    WHERE innings_bowled > 0
    ORDER BY wickets_taken DESC, economy_rate ASC;
    """
    return execute_query(query)


def get_all_fielding_leaderboard() -> pd.DataFrame:
    """Full tournament fielding leaderboard."""
    query = """
    SELECT 
        player_id,
        player_name,
        team_name,
        role,
        catches,
        stumpings,
        run_outs,
        total_dismissals
    FROM PLAYER_FIELDING_SUMMARY
    ORDER BY total_dismissals DESC;
    """
    return execute_query(query)
