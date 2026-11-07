-- ============================================================================
-- CRICKET ANALYSIS APPLICATION: DATABASE VIEWS
-- File: 04_create_views.sql
-- Description: 10 simple and practical SQL views for tournament statistics.
--              Written using standard JOINs, GROUP BY, and aggregates so they
--              are easy to understand and explain in project presentations.
-- ============================================================================

-- ----------------------------------------------------------------------------
-- 1. VIEW: TOP_RUN_SCORERS
-- Shows leading run scorers with batting average and strike rate
-- ----------------------------------------------------------------------------
CREATE OR REPLACE VIEW TOP_RUN_SCORERS AS
SELECT 
    p.player_id,
    p.full_name AS player_name,
    t.team_name,
    COUNT(bp.batting_id) AS innings_played,
    SUM(bp.runs_scored) AS total_runs,
    SUM(bp.balls_faced) AS total_balls_faced,
    SUM(bp.fours) AS fours,
    SUM(bp.sixes) AS sixes,
    MAX(bp.runs_scored) AS highest_score,
    -- Batting average = Total runs / Total times dismissed (innings - not_outs)
    ROUND(
        SUM(bp.runs_scored)::NUMERIC / 
        NULLIF(COUNT(bp.batting_id) - SUM(CASE WHEN bp.not_out THEN 1 ELSE 0 END), 0), 
        2
    ) AS batting_average,
    -- Strike rate = (Total runs / Total balls faced) * 100
    ROUND(
        (SUM(bp.runs_scored)::NUMERIC * 100.0) / 
        NULLIF(SUM(bp.balls_faced), 0), 
        2
    ) AS strike_rate
FROM PLAYERS p
JOIN TEAMS t ON p.team_id = t.team_id
JOIN BATTING_PERFORMANCE bp ON p.player_id = bp.player_id
GROUP BY p.player_id, p.full_name, t.team_name
ORDER BY total_runs DESC;

-- ----------------------------------------------------------------------------
-- 2. VIEW: TOP_WICKET_TAKERS
-- Shows leading wicket takers with bowling economy and average
-- ----------------------------------------------------------------------------
CREATE OR REPLACE VIEW TOP_WICKET_TAKERS AS
SELECT 
    p.player_id,
    p.full_name AS player_name,
    t.team_name,
    COUNT(bwp.bowling_id) AS innings_bowled,
    SUM(bwp.balls_bowled) AS total_balls_bowled,
    SUM(bwp.wickets_taken) AS total_wickets,
    SUM(bwp.runs_conceded) AS runs_conceded,
    -- Economy rate = Runs conceded / (Balls bowled / 6.0)
    ROUND(
        SUM(bwp.runs_conceded)::NUMERIC / 
        NULLIF(SUM(bwp.balls_bowled)::NUMERIC / 6.0, 0), 
        2
    ) AS economy_rate,
    -- Bowling average = Runs conceded / Wickets taken
    ROUND(
        SUM(bwp.runs_conceded)::NUMERIC / 
        NULLIF(SUM(bwp.wickets_taken), 0), 
        2
    ) AS bowling_average
FROM PLAYERS p
JOIN TEAMS t ON p.team_id = t.team_id
JOIN BOWLING_PERFORMANCE bwp ON p.player_id = bwp.player_id
GROUP BY p.player_id, p.full_name, t.team_name
ORDER BY total_wickets DESC, economy_rate ASC;

-- ----------------------------------------------------------------------------
-- 3. VIEW: TEAM_PERFORMANCE
-- Calculates matches played, wins, losses, and win percentage for each team
-- ----------------------------------------------------------------------------
CREATE OR REPLACE VIEW TEAM_PERFORMANCE AS
SELECT 
    t.team_id,
    t.team_name,
    COUNT(m.match_id) AS matches_played,
    COUNT(CASE WHEN m.result_summary LIKE '%' || t.team_name || ' won%' THEN 1 END) AS wins,
    COUNT(CASE WHEN m.result_summary NOT LIKE '%' || t.team_name || ' won%' AND m.result_summary IS NOT NULL THEN 1 END) AS losses,
    ROUND(
        (COUNT(CASE WHEN m.result_summary LIKE '%' || t.team_name || ' won%' THEN 1 END)::NUMERIC * 100.0) / 
        NULLIF(COUNT(m.match_id), 0), 
        2
    ) AS win_percentage
FROM TEAMS t
LEFT JOIN MATCHES m ON t.team_id = m.home_team_id OR t.team_id = m.away_team_id
GROUP BY t.team_id, t.team_name
ORDER BY wins DESC, win_percentage DESC;

-- ----------------------------------------------------------------------------
-- 4. VIEW: MATCH_SCORECARD
-- Clean fixture scorecard showing match date, venue, scores, and result
-- ----------------------------------------------------------------------------
CREATE OR REPLACE VIEW MATCH_SCORECARD AS
SELECT 
    m.match_id,
    m.match_date,
    v.venue_name,
    v.city,
    ht.team_name AS home_team,
    at.team_name AS away_team,
    -- Innings 1 score
    t1.team_name AS first_batting_team,
    CONCAT(i1.total_runs, '/', i1.wickets_lost, ' (', i1.overs_played, ' ov)') AS first_innings_score,
    -- Innings 2 score
    t2.team_name AS second_batting_team,
    CONCAT(i2.total_runs, '/', i2.wickets_lost, ' (', i2.overs_played, ' ov)') AS second_innings_score,
    m.result_summary
FROM MATCHES m
JOIN VENUES v ON m.venue_id = v.venue_id
JOIN TEAMS ht ON m.home_team_id = ht.team_id
JOIN TEAMS at ON m.away_team_id = at.team_id
LEFT JOIN INNINGS i1 ON m.match_id = i1.match_id AND i1.innings_number = 1
LEFT JOIN TEAMS t1 ON i1.batting_team_id = t1.team_id
LEFT JOIN INNINGS i2 ON m.match_id = i2.match_id AND i2.innings_number = 2
LEFT JOIN TEAMS t2 ON i2.batting_team_id = t2.team_id
ORDER BY m.match_date DESC;

-- ----------------------------------------------------------------------------
-- 5. VIEW: VENUE_STATISTICS
-- Stadium analytics: matches hosted and average 1st and 2nd innings totals
-- ----------------------------------------------------------------------------
CREATE OR REPLACE VIEW VENUE_STATISTICS AS
SELECT 
    v.venue_id,
    v.venue_name,
    v.city,
    v.capacity,
    COUNT(DISTINCT m.match_id) AS matches_played,
    ROUND(AVG(CASE WHEN i.innings_number = 1 THEN i.total_runs END), 1) AS avg_1st_innings_score,
    ROUND(AVG(CASE WHEN i.innings_number = 2 THEN i.total_runs END), 1) AS avg_2nd_innings_score,
    MAX(i.total_runs) AS highest_innings_score
FROM VENUES v
LEFT JOIN MATCHES m ON v.venue_id = m.venue_id
LEFT JOIN INNINGS i ON m.match_id = i.match_id
GROUP BY v.venue_id, v.venue_name, v.city, v.capacity
ORDER BY matches_played DESC;

-- ----------------------------------------------------------------------------
-- 6. VIEW: PLAYER_BATTING_SUMMARY
-- Career batting summary for all players
-- ----------------------------------------------------------------------------
CREATE OR REPLACE VIEW PLAYER_BATTING_SUMMARY AS
SELECT 
    p.player_id,
    p.full_name AS player_name,
    t.team_name,
    p.role,
    COUNT(bp.batting_id) AS innings_count,
    COALESCE(SUM(bp.runs_scored), 0) AS total_runs,
    COALESCE(SUM(bp.balls_faced), 0) AS total_balls,
    COALESCE(SUM(bp.fours), 0) AS total_fours,
    COALESCE(SUM(bp.sixes), 0) AS total_sixes,
    COALESCE(MAX(bp.runs_scored), 0) AS highest_score,
    ROUND(
        COALESCE(SUM(bp.runs_scored), 0)::NUMERIC / 
        NULLIF(COUNT(bp.batting_id) - COALESCE(SUM(CASE WHEN bp.not_out THEN 1 ELSE 0 END), 0), 0), 
        2
    ) AS batting_average,
    ROUND(
        (COALESCE(SUM(bp.runs_scored), 0)::NUMERIC * 100.0) / 
        NULLIF(COALESCE(SUM(bp.balls_faced), 0), 0), 
        2
    ) AS strike_rate
FROM PLAYERS p
JOIN TEAMS t ON p.team_id = t.team_id
LEFT JOIN BATTING_PERFORMANCE bp ON p.player_id = bp.player_id
GROUP BY p.player_id, p.full_name, t.team_name, p.role
ORDER BY total_runs DESC;

-- ----------------------------------------------------------------------------
-- 7. VIEW: PLAYER_BOWLING_SUMMARY
-- Career bowling summary for all bowlers
-- ----------------------------------------------------------------------------
CREATE OR REPLACE VIEW PLAYER_BOWLING_SUMMARY AS
SELECT 
    p.player_id,
    p.full_name AS player_name,
    t.team_name,
    p.bowling_style,
    COUNT(bwp.bowling_id) AS innings_bowled,
    COALESCE(SUM(bwp.balls_bowled), 0) AS balls_bowled,
    COALESCE(SUM(bwp.maidens), 0) AS maidens,
    COALESCE(SUM(bwp.runs_conceded), 0) AS runs_conceded,
    COALESCE(SUM(bwp.wickets_taken), 0) AS wickets_taken,
    ROUND(
        COALESCE(SUM(bwp.runs_conceded), 0)::NUMERIC / 
        NULLIF(COALESCE(SUM(bwp.balls_bowled), 0)::NUMERIC / 6.0, 0), 
        2
    ) AS economy_rate,
    ROUND(
        COALESCE(SUM(bwp.runs_conceded), 0)::NUMERIC / 
        NULLIF(COALESCE(SUM(bwp.wickets_taken), 0), 0), 
        2
    ) AS bowling_average
FROM PLAYERS p
JOIN TEAMS t ON p.team_id = t.team_id
LEFT JOIN BOWLING_PERFORMANCE bwp ON p.player_id = bwp.player_id
GROUP BY p.player_id, p.full_name, t.team_name, p.bowling_style
ORDER BY wickets_taken DESC;

-- ----------------------------------------------------------------------------
-- 8. VIEW: PLAYER_FIELDING_SUMMARY
-- Fielding summary showing catches, stumpings, and run-outs
-- ----------------------------------------------------------------------------
CREATE OR REPLACE VIEW PLAYER_FIELDING_SUMMARY AS
SELECT 
    p.player_id,
    p.full_name AS player_name,
    t.team_name,
    p.role,
    COALESCE(SUM(fp.catches), 0) AS catches,
    COALESCE(SUM(fp.stumpings), 0) AS stumpings,
    COALESCE(SUM(fp.run_outs), 0) AS run_outs,
    COALESCE(SUM(fp.catches + fp.stumpings + fp.run_outs), 0) AS total_dismissals
FROM PLAYERS p
JOIN TEAMS t ON p.team_id = t.team_id
LEFT JOIN FIELDING_PERFORMANCE fp ON p.player_id = fp.player_id
GROUP BY p.player_id, p.full_name, t.team_name, p.role
HAVING COALESCE(SUM(fp.catches + fp.stumpings + fp.run_outs), 0) > 0
ORDER BY total_dismissals DESC;

-- ----------------------------------------------------------------------------
-- 9. VIEW: TEAM_HEAD_TO_HEAD
-- Simple head-to-head match count and results between team pairs
-- ----------------------------------------------------------------------------
CREATE OR REPLACE VIEW TEAM_HEAD_TO_HEAD AS
SELECT 
    t1.team_name AS team_1,
    t2.team_name AS team_2,
    COUNT(m.match_id) AS total_matches,
    COUNT(CASE WHEN m.result_summary LIKE '%' || t1.team_name || ' won%' THEN 1 END) AS team_1_wins,
    COUNT(CASE WHEN m.result_summary LIKE '%' || t2.team_name || ' won%' THEN 1 END) AS team_2_wins
FROM MATCHES m
JOIN TEAMS t1 ON m.home_team_id = t1.team_id
JOIN TEAMS t2 ON m.away_team_id = t2.team_id
GROUP BY t1.team_name, t2.team_name;

-- ----------------------------------------------------------------------------
-- 10. VIEW: INNINGS_SUMMARY
-- Innings level breakdown showing total score, wickets, and run rate
-- ----------------------------------------------------------------------------
CREATE OR REPLACE VIEW INNINGS_SUMMARY AS
SELECT 
    i.innings_id,
    m.match_id,
    m.match_date,
    i.innings_number,
    t.team_name AS batting_team,
    i.total_runs,
    i.wickets_lost,
    i.overs_played,
    ROUND(
        i.total_runs::NUMERIC / 
        NULLIF(i.balls_bowled::NUMERIC / 6.0, 0), 
        2
    ) AS run_rate,
    m.result_summary
FROM INNINGS i
JOIN MATCHES m ON i.match_id = m.match_id
JOIN TEAMS t ON i.batting_team_id = t.team_id
ORDER BY m.match_date DESC, i.innings_number ASC;
