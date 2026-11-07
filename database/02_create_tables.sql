-- ============================================================================
-- CRICKET ANALYSIS APPLICATION: TABLE DEFINITIONS (DDL)
-- File: 02_create_tables.sql
-- Description: Creates the 9 core tables with Primary Keys, Foreign Keys,
--              NOT NULL constraints, and basic CHECK constraints.
-- ============================================================================

-- Drop tables in reverse order of dependencies so we can rerun safely
DROP TABLE IF EXISTS DELIVERIES CASCADE;
DROP TABLE IF EXISTS FIELDING_PERFORMANCE CASCADE;
DROP TABLE IF EXISTS BOWLING_PERFORMANCE CASCADE;
DROP TABLE IF EXISTS BATTING_PERFORMANCE CASCADE;
DROP TABLE IF EXISTS INNINGS CASCADE;
DROP TABLE IF EXISTS MATCHES CASCADE;
DROP TABLE IF EXISTS VENUES CASCADE;
DROP TABLE IF EXISTS PLAYERS CASCADE;
DROP TABLE IF EXISTS TEAMS CASCADE;

-- ----------------------------------------------------------------------------
-- 1. TEAMS Table
-- Stores team information
-- ----------------------------------------------------------------------------
CREATE TABLE TEAMS (
    team_id     SERIAL PRIMARY KEY,
    team_name   VARCHAR(100) NOT NULL UNIQUE,
    country     VARCHAR(50) NOT NULL,
    coach       VARCHAR(100)
);

-- ----------------------------------------------------------------------------
-- 2. PLAYERS Table
-- Stores player details and links each player to their current team
-- ----------------------------------------------------------------------------
CREATE TABLE PLAYERS (
    player_id       SERIAL PRIMARY KEY,
    full_name       VARCHAR(100) NOT NULL,
    date_of_birth   DATE NOT NULL,
    role            VARCHAR(30) NOT NULL CHECK (role IN ('batter', 'bowler', 'all-rounder', 'wicketkeeper')),
    batting_style   VARCHAR(30) NOT NULL,
    bowling_style   VARCHAR(50),
    team_id         INT NOT NULL REFERENCES TEAMS(team_id) ON UPDATE CASCADE ON DELETE RESTRICT
);

-- ----------------------------------------------------------------------------
-- 3. VENUES Table
-- Stores cricket stadiums and cities
-- ----------------------------------------------------------------------------
CREATE TABLE VENUES (
    venue_id    SERIAL PRIMARY KEY,
    venue_name  VARCHAR(150) NOT NULL,
    city        VARCHAR(100) NOT NULL,
    country     VARCHAR(50) NOT NULL DEFAULT 'India',
    capacity    INT CHECK (capacity > 0)
);

-- ----------------------------------------------------------------------------
-- 4. MATCHES Table
-- Stores fixtures between two teams at a specific venue
-- ----------------------------------------------------------------------------
CREATE TABLE MATCHES (
    match_id        SERIAL PRIMARY KEY,
    match_date      DATE NOT NULL,
    match_format    VARCHAR(20) NOT NULL DEFAULT 'T20',
    home_team_id    INT NOT NULL REFERENCES TEAMS(team_id),
    away_team_id    INT NOT NULL REFERENCES TEAMS(team_id),
    venue_id        INT NOT NULL REFERENCES VENUES(venue_id),
    result_summary  VARCHAR(255),
    CHECK (home_team_id <> away_team_id)
);

-- ----------------------------------------------------------------------------
-- 5. INNINGS Table
-- Stores team totals for each innings of a match
-- Note: balls_bowled is stored as integer for accurate cricket rate calculations
-- ----------------------------------------------------------------------------
CREATE TABLE INNINGS (
    innings_id      SERIAL PRIMARY KEY,
    match_id        INT NOT NULL REFERENCES MATCHES(match_id) ON DELETE CASCADE,
    batting_team_id INT NOT NULL REFERENCES TEAMS(team_id),
    innings_number  INT NOT NULL CHECK (innings_number IN (1, 2)),
    total_runs      INT NOT NULL DEFAULT 0 CHECK (total_runs >= 0),
    wickets_lost    INT NOT NULL DEFAULT 0 CHECK (wickets_lost BETWEEN 0 AND 10),
    overs_played    NUMERIC(4,1) NOT NULL DEFAULT 0.0,
    balls_bowled    INT NOT NULL DEFAULT 0 CHECK (balls_bowled >= 0),
    UNIQUE (match_id, innings_number)
);

-- ----------------------------------------------------------------------------
-- 6. BATTING_PERFORMANCE Table
-- Stores individual batsman scorecards for an innings
-- ----------------------------------------------------------------------------
CREATE TABLE BATTING_PERFORMANCE (
    batting_id          SERIAL PRIMARY KEY,
    innings_id          INT NOT NULL REFERENCES INNINGS(innings_id) ON DELETE CASCADE,
    player_id           INT NOT NULL REFERENCES PLAYERS(player_id),
    runs_scored         INT NOT NULL DEFAULT 0 CHECK (runs_scored >= 0),
    balls_faced         INT NOT NULL DEFAULT 0 CHECK (balls_faced >= 0),
    fours               INT NOT NULL DEFAULT 0 CHECK (fours >= 0),
    sixes               INT NOT NULL DEFAULT 0 CHECK (sixes >= 0),
    dismissal           VARCHAR(60) DEFAULT 'not out',
    not_out             BOOLEAN NOT NULL DEFAULT FALSE,
    batting_position    INT CHECK (batting_position BETWEEN 1 AND 11),
    UNIQUE (innings_id, player_id)
);

-- ----------------------------------------------------------------------------
-- 7. BOWLING_PERFORMANCE Table
-- Stores individual bowler figures for an innings
-- overs_bowled is for display (e.g. 4.0, 3.2), balls_bowled is for math
-- ----------------------------------------------------------------------------
CREATE TABLE BOWLING_PERFORMANCE (
    bowling_id      SERIAL PRIMARY KEY,
    innings_id      INT NOT NULL REFERENCES INNINGS(innings_id) ON DELETE CASCADE,
    player_id       INT NOT NULL REFERENCES PLAYERS(player_id),
    overs_bowled    NUMERIC(3,1) NOT NULL DEFAULT 0.0,
    balls_bowled    INT NOT NULL DEFAULT 0 CHECK (balls_bowled >= 0),
    maidens         INT NOT NULL DEFAULT 0 CHECK (maidens >= 0),
    runs_conceded   INT NOT NULL DEFAULT 0 CHECK (runs_conceded >= 0),
    wickets_taken   INT NOT NULL DEFAULT 0 CHECK (wickets_taken BETWEEN 0 AND 10),
    UNIQUE (innings_id, player_id)
);

-- ----------------------------------------------------------------------------
-- 8. FIELDING_PERFORMANCE Table
-- Stores catches, stumpings, and run-outs by fielders
-- ----------------------------------------------------------------------------
CREATE TABLE FIELDING_PERFORMANCE (
    fielding_id     SERIAL PRIMARY KEY,
    innings_id      INT NOT NULL REFERENCES INNINGS(innings_id) ON DELETE CASCADE,
    player_id       INT NOT NULL REFERENCES PLAYERS(player_id),
    catches         INT NOT NULL DEFAULT 0 CHECK (catches >= 0),
    stumpings       INT NOT NULL DEFAULT 0 CHECK (stumpings >= 0),
    run_outs        INT NOT NULL DEFAULT 0 CHECK (run_outs >= 0),
    UNIQUE (innings_id, player_id)
);

-- ----------------------------------------------------------------------------
-- 9. DELIVERIES Table
-- Stores ball-by-ball events for in-depth analysis
-- ----------------------------------------------------------------------------
CREATE TABLE DELIVERIES (
    delivery_id     SERIAL PRIMARY KEY,
    innings_id      INT NOT NULL REFERENCES INNINGS(innings_id) ON DELETE CASCADE,
    over_number     INT NOT NULL CHECK (over_number >= 1),
    ball_number     INT NOT NULL CHECK (ball_number >= 1),
    striker_id      INT NOT NULL REFERENCES PLAYERS(player_id),
    bowler_id       INT NOT NULL REFERENCES PLAYERS(player_id),
    runs_batter     INT NOT NULL DEFAULT 0 CHECK (runs_batter BETWEEN 0 AND 6),
    extras          INT NOT NULL DEFAULT 0 CHECK (extras >= 0),
    total_runs      INT NOT NULL DEFAULT 0,
    wicket_type     VARCHAR(30),
    CHECK (striker_id <> bowler_id),
    UNIQUE (innings_id, over_number, ball_number)
);
