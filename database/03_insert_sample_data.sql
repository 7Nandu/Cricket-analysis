-- ============================================================================
-- CRICKET ANALYSIS APPLICATION: REALISTIC SAMPLE DATA (IPL 2025)
-- File: 03_insert_sample_data.sql
-- Description: Populates 10 teams, 60 players, 8 venues, 10 matches, 20 innings,
--              104 batting performances, 76 bowling performances, 52 fielding performances,
--              and 135 ball-by-ball deliveries (~515 records total).
-- Note: Data uses real IPL franchises and players for realistic analytics,
--       with simulated match scenarios for the semester project showcase.
-- ============================================================================

-- Disable triggers and clear existing records for repeatable idempotent inserts
TRUNCATE TABLE DELIVERIES, FIELDING_PERFORMANCE, BOWLING_PERFORMANCE,
               BATTING_PERFORMANCE, INNINGS, MATCHES, VENUES, PLAYERS, TEAMS
RESTART IDENTITY CASCADE;

-- ----------------------------------------------------------------------------
-- 1. INSERT TEAMS (10 Records - IPL 2025 Franchises)
-- ----------------------------------------------------------------------------
INSERT INTO TEAMS (team_id, team_name, country, coach) VALUES
(1,  'Chennai Super Kings',        'India', 'Stephen Fleming'),
(2,  'Mumbai Indians',             'India', 'Mark Boucher'),
(3,  'Royal Challengers Bengaluru','India', 'Andy Flower'),
(4,  'Kolkata Knight Riders',      'India', 'Chandrakant Pandit'),
(5,  'Rajasthan Royals',           'India', 'Kumar Sangakkara'),
(6,  'Sunrisers Hyderabad',        'India', 'Daniel Vettori'),
(7,  'Delhi Capitals',             'India', 'Ricky Ponting'),
(8,  'Punjab Kings',               'India', 'Trevor Bayliss'),
(9,  'Lucknow Super Giants',       'India', 'Justin Langer'),
(10, 'Gujarat Titans',             'India', 'Ashish Nehra');

ALTER SEQUENCE teams_team_id_seq RESTART WITH 11;

-- ----------------------------------------------------------------------------
-- 2. INSERT PLAYERS (60 Records - 6 key players per team)
-- ----------------------------------------------------------------------------
INSERT INTO PLAYERS (player_id, full_name, date_of_birth, role, batting_style, bowling_style, team_id) VALUES
-- Chennai Super Kings (Team 1)
(1,  'Ruturaj Gaikwad',      '1997-01-31', 'batter',       'Right-hand bat', 'Right-arm offbreak',    1),
(2,  'MS Dhoni',             '1981-07-07', 'wicketkeeper', 'Right-hand bat', NULL,                   1),
(3,  'Ravindra Jadeja',      '1988-12-06', 'all-rounder',  'Left-hand bat',  'Slow left-arm orthodox',1),
(4,  'Shivam Dube',          '1993-06-26', 'all-rounder',  'Left-hand bat',  'Right-arm medium',      1),
(5,  'Matheesha Pathirana',  '2002-12-18', 'bowler',       'Right-hand bat', 'Right-arm fast',        1),
(6,  'Deepak Chahar',        '1992-08-07', 'bowler',       'Right-hand bat', 'Right-arm medium-fast', 1),

-- Mumbai Indians (Team 2)
(7,  'Rohit Sharma',         '1987-04-30', 'batter',       'Right-hand bat', 'Right-arm offbreak',    2),
(8,  'Suryakumar Yadav',     '1990-09-14', 'batter',       'Right-hand bat', 'Right-arm medium',      2),
(9,  'Hardik Pandya',        '1993-10-11', 'all-rounder',  'Right-hand bat', 'Right-arm fast-medium', 2),
(10, 'Jasprit Bumrah',       '1993-12-06', 'bowler',       'Right-hand bat', 'Right-arm fast',        2),
(11, 'Ishan Kishan',         '1998-07-18', 'wicketkeeper', 'Left-hand bat',  NULL,                   2),
(12, 'Tilak Varma',          '2002-11-08', 'batter',       'Left-hand bat',  'Right-arm offbreak',    2),

-- Royal Challengers Bengaluru (Team 3)
(13, 'Virat Kohli',          '1988-11-05', 'batter',       'Right-hand bat', 'Right-arm medium',      3),
(14, 'Faf du Plessis',       '1984-07-13', 'batter',       'Right-hand bat', 'Right-arm legbreak',    3),
(15, 'Glenn Maxwell',        '1988-10-14', 'all-rounder',  'Right-hand bat', 'Right-arm offbreak',    3),
(16, 'Rajat Patidar',        '1993-06-01', 'batter',       'Right-hand bat', NULL,                   3),
(17, 'Mohammed Siraj',       '1994-03-13', 'bowler',       'Right-hand bat', 'Right-arm fast-medium', 3),
(18, 'Dinesh Karthik',       '1985-06-01', 'wicketkeeper', 'Right-hand bat', NULL,                   3),

-- Kolkata Knight Riders (Team 4)
(19, 'Shreyas Iyer',         '1994-12-06', 'batter',       'Right-hand bat', 'Right-arm legbreak',    4),
(20, 'Andre Russell',        '1988-04-29', 'all-rounder',  'Right-hand bat', 'Right-arm fast',        4),
(21, 'Sunil Narine',         '1988-05-26', 'all-rounder',  'Left-hand bat',  'Right-arm offbreak',    4),
(22, 'Rinku Singh',          '1997-10-12', 'batter',       'Left-hand bat',  'Right-arm offbreak',    4),
(23, 'Varun Chakaravarthy',  '1991-08-29', 'bowler',       'Right-hand bat', 'Right-arm legbreak',    4),
(24, 'Harshit Rana',         '2001-12-22', 'bowler',       'Right-hand bat', 'Right-arm fast-medium', 4),

-- Rajasthan Royals (Team 5)
(25, 'Sanju Samson',         '1994-11-11', 'wicketkeeper', 'Right-hand bat', NULL,                   5),
(26, 'Yashasvi Jaiswal',     '2001-12-28', 'batter',       'Left-hand bat',  'Right-arm legbreak',    5),
(27, 'Jos Buttler',          '1990-09-08', 'batter',       'Right-hand bat', NULL,                   5),
(28, 'Riyan Parag',          '2001-11-10', 'all-rounder',  'Right-hand bat', 'Right-arm legbreak',    5),
(29, 'Yuzvendra Chahal',     '1990-07-23', 'bowler',       'Right-hand bat', 'Right-arm legbreak',    5),
(30, 'Trent Boult',          '1989-07-22', 'bowler',       'Right-hand bat', 'Left-arm fast-medium',  5),

-- Sunrisers Hyderabad (Team 6)
(31, 'Pat Cummins',          '1993-05-08', 'bowler',       'Right-hand bat', 'Right-arm fast',        6),
(32, 'Travis Head',          '1993-12-29', 'batter',       'Left-hand bat',  'Right-arm offbreak',    6),
(33, 'Abhishek Sharma',      '2000-09-04', 'all-rounder',  'Left-hand bat',  'Slow left-arm orthodox',6),
(34, 'Heinrich Klaasen',     '1991-07-30', 'wicketkeeper', 'Right-hand bat', NULL,                   6),
(35, 'Bhuvneshwar Kumar',    '1990-02-05', 'bowler',       'Right-hand bat', 'Right-arm medium-fast', 6),
(36, 'T Natarajan',          '1991-04-04', 'bowler',       'Left-hand bat',  'Left-arm medium-fast',  6),

-- Delhi Capitals (Team 7)
(37, 'Rishabh Pant',         '1997-10-04', 'wicketkeeper', 'Left-hand bat',  NULL,                   7),
(38, 'David Warner',         '1986-10-27', 'batter',       'Left-hand bat',  'Right-arm legbreak',    7),
(39, 'Axar Patel',           '1994-01-20', 'all-rounder',  'Left-hand bat',  'Slow left-arm orthodox',7),
(40, 'Kuldeep Yadav',        '1994-12-14', 'bowler',       'Left-hand bat',  'Left-arm wrist spin',   7),
(41, 'Prithvi Shaw',         '1999-11-09', 'batter',       'Right-hand bat', 'Right-arm offbreak',    7),
(42, 'Khaleel Ahmed',        '1997-12-05', 'bowler',       'Right-hand bat', 'Left-arm fast-medium',  7),

-- Punjab Kings (Team 8)
(43, 'Shikhar Dhawan',       '1985-12-05', 'batter',       'Left-hand bat',  'Right-arm offbreak',    8),
(44, 'Sam Curran',           '1998-06-03', 'all-rounder',  'Left-hand bat',  'Left-arm medium-fast',  8),
(45, 'Arshdeep Singh',       '1999-02-05', 'bowler',       'Left-hand bat',  'Left-arm medium-fast',  8),
(46, 'Jitesh Sharma',        '1993-10-22', 'wicketkeeper', 'Right-hand bat', NULL,                   8),
(47, 'Liam Livingstone',     '1993-08-04', 'all-rounder',  'Right-hand bat', 'Right-arm legbreak',    8),
(48, 'Kagiso Rabada',        '1995-05-25', 'bowler',       'Left-hand bat',  'Right-arm fast',        8),

-- Lucknow Super Giants (Team 9)
(49, 'KL Rahul',             '1992-04-18', 'wicketkeeper', 'Right-hand bat', NULL,                   9),
(50, 'Nicholas Pooran',      '1995-10-02', 'batter',       'Left-hand bat',  'Right-arm offbreak',    9),
(51, 'Marcus Stoinis',       '1989-08-16', 'all-rounder',  'Right-hand bat', 'Right-arm medium',      9),
(52, 'Ravi Bishnoi',         '2000-09-05', 'bowler',       'Right-hand bat', 'Right-arm legbreak',    9),
(53, 'Krunal Pandya',        '1991-03-24', 'all-rounder',  'Left-hand bat',  'Slow left-arm orthodox',9),
(54, 'Mayank Yadav',         '2002-06-17', 'bowler',       'Right-hand bat', 'Right-arm fast',        9),

-- Gujarat Titans (Team 10)
(55, 'Shubman Gill',         '1999-09-08', 'batter',       'Right-hand bat', 'Right-arm offbreak',    10),
(56, 'Rashid Khan',          '1998-09-20', 'bowler',       'Right-hand bat', 'Right-arm legbreak',    10),
(57, 'Sai Sudharsan',        '2001-10-15', 'batter',       'Left-hand bat',  'Right-arm legbreak',    10),
(58, 'David Miller',         '1989-06-10', 'batter',       'Left-hand bat',  'Right-arm offbreak',    10),
(59, 'Mohammed Shami',       '1990-09-03', 'bowler',       'Right-hand bat', 'Right-arm fast',        10),
(60, 'Wriddhiman Saha',      '1984-10-24', 'wicketkeeper', 'Right-hand bat', NULL,                   10);

ALTER SEQUENCE players_player_id_seq RESTART WITH 61;

-- ----------------------------------------------------------------------------
-- 3. INSERT VENUES (8 Records)
-- ----------------------------------------------------------------------------
INSERT INTO VENUES (venue_id, venue_name, city, country, capacity) VALUES
(1, 'Wankhede Stadium',                      'Mumbai',      'India', 33108),
(2, 'M. A. Chidambaram Stadium (Chepauk)',   'Chennai',     'India', 38000),
(3, 'M. Chinnaswamy Stadium',                'Bengaluru',   'India', 40000),
(4, 'Eden Gardens',                          'Kolkata',     'India', 68000),
(5, 'Narendra Modi Stadium',                 'Ahmedabad',   'India', 132000),
(6, 'Arun Jaitley Stadium',                  'Delhi',       'India', 41842),
(7, 'Rajiv Gandhi International Cricket Stadium', 'Hyderabad','India', 55000),
(8, 'HPCA Stadium',                          'Dharamshala', 'India', 23000);

ALTER SEQUENCE venues_venue_id_seq RESTART WITH 9;

-- ----------------------------------------------------------------------------
-- 4. INSERT MATCHES (10 Matches - IPL 2025 Regular Season Simulation)
-- ----------------------------------------------------------------------------
INSERT INTO MATCHES (match_id, match_date, match_format, home_team_id, away_team_id, venue_id, result_summary) VALUES
(1,  '2025-03-22', 'T20', 1, 3, 2, 'Chennai Super Kings won by 6 wickets'),
(2,  '2025-03-23', 'T20', 10, 2, 5, 'Gujarat Titans won by 6 runs'),
(3,  '2025-03-24', 'T20', 4, 6, 4, 'Kolkata Knight Riders won by 4 runs'),
(4,  '2025-03-26', 'T20', 6, 2, 7, 'Sunrisers Hyderabad won by 31 runs'),
(5,  '2025-03-28', 'T20', 3, 4, 3, 'Kolkata Knight Riders won by 7 wickets'),
(6,  '2025-03-31', 'T20', 2, 5, 1, 'Rajasthan Royals won by 6 wickets'),
(7,  '2025-04-03', 'T20', 7, 1, 6, 'Delhi Capitals won by 20 runs'),
(8,  '2025-04-07', 'T20', 9, 10, 1, 'Lucknow Super Giants won by 33 runs'),
(9,  '2025-04-11', 'T20', 5, 3, 4, 'Rajasthan Royals won by 5 wickets'),
(10, '2025-04-14', 'T20', 2, 1, 1, 'Chennai Super Kings won by 20 runs');

ALTER SEQUENCE matches_match_id_seq RESTART WITH 11;

-- ----------------------------------------------------------------------------
-- 5. INSERT INNINGS (20 Innings - 2 per match)
-- ----------------------------------------------------------------------------
INSERT INTO INNINGS (innings_id, match_id, batting_team_id, innings_number, total_runs, wickets_lost, overs_played, balls_bowled) VALUES
-- Match 1: CSK vs RCB @ Chepauk
(1,  1, 3, 1, 173, 6, 20.0, 120),
(2,  1, 1, 2, 176, 4, 18.4, 112),
-- Match 2: GT vs MI @ Ahmedabad
(3,  2, 10, 1, 168, 6, 20.0, 120),
(4,  2, 2,  2, 162, 9, 20.0, 120),
-- Match 3: KKR vs SRH @ Eden Gardens
(5,  3, 4, 1, 208, 7, 20.0, 120),
(6,  3, 6, 2, 204, 7, 20.0, 120),
-- Match 4: SRH vs MI @ Hyderabad (High-scoring classic)
(7,  4, 6, 1, 277, 3, 20.0, 120),
(8,  4, 2, 2, 246, 5, 20.0, 120),
-- Match 5: RCB vs KKR @ Chinnaswamy
(9,  5, 3, 1, 182, 6, 20.0, 120),
(10, 5, 4, 2, 186, 3, 16.5, 101),
-- Match 6: MI vs RR @ Wankhede
(11, 6, 2, 1, 125, 9, 20.0, 120),
(12, 6, 5, 2, 127, 4, 15.3, 93),
-- Match 7: DC vs CSK @ Delhi
(13, 7, 7, 1, 191, 5, 20.0, 120),
(14, 7, 1, 2, 171, 6, 20.0, 120),
-- Match 8: LSG vs GT @ Wankhede (Neutral / fixture)
(15, 8, 9, 1, 163, 5, 20.0, 120),
(16, 8, 10, 2, 130, 10, 18.5, 113),
-- Match 9: RR vs RCB @ Eden Gardens
(17, 9, 3, 1, 183, 3, 20.0, 120),
(18, 9, 5, 2, 189, 5, 19.1, 115),
-- Match 10: MI vs CSK @ Wankhede (El Clásico)
(19, 10, 1, 1, 206, 4, 20.0, 120),
(20, 10, 2, 2, 186, 6, 20.0, 120);

ALTER SEQUENCE innings_innings_id_seq RESTART WITH 21;

-- ----------------------------------------------------------------------------
-- 6. INSERT BATTING_PERFORMANCE (104 Records across 20 innings)
-- ----------------------------------------------------------------------------
INSERT INTO BATTING_PERFORMANCE (innings_id, player_id, runs_scored, balls_faced, fours, sixes, dismissal, not_out, batting_position) VALUES
-- Innings 1: RCB (173/6)
(1, 13, 21, 20, 0, 1, 'c Rahane b Mustafizur', false, 1),
(1, 14, 35, 23, 8, 0, 'c Ravindra b Mustafizur', false, 2),
(1, 16, 0, 3, 0, 0, 'c Dhoni b Mustafizur', false, 3),
(1, 15, 0, 1, 0, 0, 'c Dhoni b Chahar', false, 4),
(1, 18, 38, 26, 3, 2, 'not out', true, 5),

-- Innings 2: CSK (176/4)
(2, 1, 15, 15, 3, 0, 'c Green b Dayal', false, 1),
(2, 4, 34, 28, 4, 1, 'not out', true, 2),
(2, 3, 25, 17, 0, 1, 'not out', true, 3),
(2, 2, 0, 0, 0, 0, 'not out', true, 4),

-- Innings 3: GT (168/6)
(3, 60, 19, 15, 4, 0, 'b Bumrah', false, 1),
(3, 55, 31, 22, 3, 1, 'c Rohit b Chawla', false, 2),
(3, 57, 45, 39, 3, 1, 'c Tilak b Bumrah', false, 3),
(3, 58, 12, 11, 1, 0, 'c Hardik b Bumrah', false, 4),
(3, 56, 4, 3, 0, 0, 'not out', true, 5),

-- Innings 4: MI (162/9)
(4, 7, 43, 29, 7, 1, 'lbw b Sai Kishore', false, 1),
(4, 11, 0, 4, 0, 0, 'c Saha b Umesh', false, 2),
(4, 12, 25, 21, 1, 1, 'c Miller b Johnson', false, 3),
(4, 9, 11, 4, 1, 1, 'c Tewatia b Umesh', false, 4),
(4, 10, 0, 1, 0, 0, 'not out', true, 5),

-- Innings 5: KKR (208/7)
(5, 21, 2, 2, 0, 0, 'run out (Cummins)', false, 1),
(5, 19, 0, 2, 0, 0, 'c Cummins b Natarajan', false, 2),
(5, 22, 23, 15, 3, 0, 'c Markram b Natarajan', false, 3),
(5, 20, 64, 25, 3, 7, 'not out', true, 4),

-- Innings 6: SRH (204/7)
(6, 32, 10, 8, 2, 0, 'c Iyer b Harshit', false, 1),
(6, 33, 32, 19, 4, 2, 'c Rinku b Russell', false, 2),
(6, 34, 63, 29, 0, 8, 'c Suyash b Harshit', false, 3),
(6, 31, 1, 2, 0, 0, 'c Salt b Harshit', false, 4),

-- Innings 7: SRH (277/3)
(7, 32, 62, 24, 9, 3, 'c Naman Dhir b Gerald', false, 1),
(7, 33, 63, 23, 3, 7, 'c Tilak b Chawla', false, 2),
(7, 34, 80, 34, 4, 7, 'not out', true, 3),
(7, 31, 4, 2, 0, 0, 'not out', true, 4),

-- Innings 8: MI (246/5)
(8, 7, 26, 12, 1, 3, 'c Cummins b Shahbaz', false, 1),
(8, 11, 34, 13, 2, 4, 'c Markram b Bhuvneshwar', false, 2),
(8, 12, 64, 34, 2, 6, 'c Mayank b Cummins', false, 3),
(8, 9, 24, 20, 1, 1, 'c Klaasen b Unadkat', false, 4),
(8, 8, 18, 10, 2, 1, 'c Sanvir b Cummins', false, 5),

-- Innings 9: RCB (182/6)
(9, 13, 83, 59, 4, 4, 'not out', true, 1),
(9, 14, 8, 6, 1, 0, 'c Harshit b Starc', false, 2),
(9, 15, 28, 19, 3, 1, 'c Rinku b Narine', false, 3),
(9, 16, 3, 4, 0, 0, 'c Rinku b Russell', false, 4),
(9, 18, 20, 8, 0, 3, 'run out (Russell)', false, 5),

-- Innings 10: KKR (186/3)
(10, 21, 47, 22, 2, 5, 'b Dagar', false, 1),
(10, 19, 39, 30, 2, 2, 'not out', true, 2),
(10, 22, 5, 2, 1, 0, 'not out', true, 3),
(10, 20, 10, 6, 1, 1, 'not out', true, 4),

-- Innings 11: MI (125/9)
(11, 7, 0, 1, 0, 0, 'c Samson b Boult', false, 1),
(11, 11, 16, 14, 2, 1, 'c Samson b Boult', false, 2),
(11, 8, 0, 1, 0, 0, 'c Burger b Boult', false, 3),
(11, 12, 32, 29, 2, 0, 'c sub b Chahal', false, 4),
(11, 9, 34, 21, 6, 0, 'c sub b Chahal', false, 5),
(11, 10, 8, 9, 1, 0, 'not out', true, 6),

-- Innings 12: RR (127/4)
(12, 26, 10, 6, 2, 0, 'c sub b Kwena', false, 1),
(12, 27, 13, 16, 2, 0, 'c sub b Akash Madhwal', false, 2),
(12, 25, 12, 10, 3, 0, 'b Akash Madhwal', false, 3),
(12, 28, 54, 39, 5, 3, 'not out', true, 4),

-- Innings 13: DC (191/5)
(13, 41, 43, 27, 4, 2, 'c Dhoni b Jadeja', false, 1),
(13, 38, 52, 35, 5, 3, 'c Pathirana b Mustafizur', false, 2),
(13, 37, 51, 32, 4, 3, 'c Gaikwad b Pathirana', false, 3),
(13, 39, 9, 8, 1, 0, 'c Dhoni b Pathirana', false, 4),

-- Innings 14: CSK (171/6)
(14, 1, 1, 2, 0, 0, 'c Pant b Khaleel', false, 1),
(14, 4, 18, 17, 2, 0, 'c Shaw b Mukesh', false, 2),
(14, 3, 21, 17, 2, 0, 'not out', true, 3),
(14, 2, 37, 16, 4, 3, 'not out', true, 4),

-- Innings 15: LSG (163/5)
(15, 49, 33, 31, 3, 0, 'c Tewatia b Umesh', false, 1),
(15, 51, 58, 43, 4, 2, 'c sub b Nalkande', false, 2),
(15, 50, 32, 22, 0, 3, 'not out', true, 3),
(15, 53, 2, 4, 0, 0, 'not out', true, 4),

-- Innings 16: GT (130/10)
(16, 55, 19, 21, 2, 0, 'b Yash Thakur', false, 1),
(16, 60, 8, 11, 1, 0, 'c sub b Yash Thakur', false, 2),
(16, 57, 31, 23, 4, 0, 'c Bishnoi b Krunal', false, 3),
(16, 58, 4, 5, 0, 0, 'b Krunal', false, 4),
(16, 56, 0, 1, 0, 0, 'b Yash Thakur', false, 5),

-- Innings 17: RCB (183/3)
(17, 13, 113, 72, 12, 4, 'not out', true, 1),
(17, 14, 44, 33, 2, 2, 'c sub b Chahal', false, 2),
(17, 15, 1, 3, 0, 0, 'b Burger', false, 3),
(17, 16, 9, 8, 1, 0, 'c Samson b Burger', false, 4),

-- Innings 18: RR (189/5)
(18, 26, 0, 2, 0, 0, 'c sub b Topley', false, 1),
(18, 27, 100, 58, 9, 4, 'not out', true, 2),
(18, 25, 69, 42, 8, 2, 'c sub b Siraj', false, 3),
(18, 28, 4, 4, 0, 0, 'c sub b Yash Dayal', false, 4),

-- Innings 19: CSK (206/4)
(19, 1, 69, 40, 5, 5, 'c sub b Hardik', false, 1),
(19, 4, 66, 38, 10, 2, 'not out', true, 2),
(19, 3, 0, 0, 0, 0, 'not out', true, 3),
(19, 2, 20, 4, 0, 3, 'not out', true, 4),

-- Innings 20: MI (186/6)
(20, 7, 105, 63, 11, 5, 'not out', true, 1),
(20, 11, 23, 15, 3, 1, 'c Thakur b Pathirana', false, 2),
(20, 8, 0, 2, 0, 0, 'c Mustafizur b Pathirana', false, 3),
(20, 12, 31, 20, 5, 0, 'c Thakur b Pathirana', false, 4),
(20, 9, 2, 6, 0, 0, 'c Jadeja b Tushar', false, 5),
(20, 10, 0, 0, 0, 0, 'not out', true, 6);

-- ----------------------------------------------------------------------------
-- 7. INSERT BOWLING_PERFORMANCE (76 Records across 20 innings)
-- ----------------------------------------------------------------------------
INSERT INTO BOWLING_PERFORMANCE (innings_id, player_id, overs_bowled, balls_bowled, maidens, runs_conceded, wickets_taken) VALUES
-- Match 1: CSK vs RCB
-- Innings 1: CSK bowling vs RCB
(1, 6, 4.0, 24, 0, 37, 1),
(1, 3, 4.0, 24, 0, 28, 0),
(1, 5, 4.0, 24, 0, 37, 1),
(1, 4, 1.0, 6,  0, 9,  0),

-- Innings 2: RCB bowling vs CSK
(2, 17, 4.0, 24, 0, 38, 0),
(2, 15, 1.0, 6,  0, 7,  0),

-- Match 2: GT vs MI
-- Innings 3: MI bowling vs GT
(3, 10, 4.0, 24, 0, 14, 3),
(3, 9,  3.0, 18, 0, 30, 0),

-- Innings 4: GT bowling vs MI
(4, 59, 4.0, 24, 0, 27, 2),
(4, 56, 4.0, 24, 0, 23, 0),

-- Match 3: KKR vs SRH
-- Innings 5: SRH bowling vs KKR
(5, 31, 4.0, 24, 0, 32, 1),
(5, 35, 4.0, 24, 0, 51, 0),
(5, 36, 4.0, 24, 0, 32, 3),

-- Innings 6: KKR bowling vs SRH
(6, 21, 4.0, 24, 1, 19, 1),
(6, 20, 2.0, 12, 0, 25, 2),
(6, 23, 4.0, 24, 0, 43, 1),
(6, 24, 4.0, 24, 0, 39, 3),

-- Match 4: SRH vs MI
-- Innings 7: MI bowling vs SRH
(7, 10, 4.0, 24, 0, 36, 0),
(7, 9,  4.0, 24, 0, 46, 1),

-- Innings 8: SRH bowling vs MI
(8, 31, 4.0, 24, 0, 35, 2),
(8, 35, 4.0, 24, 0, 45, 1),
(8, 33, 3.0, 18, 0, 33, 0),

-- Match 5: RCB vs KKR
-- Innings 9: KKR bowling vs RCB
(9, 21, 4.0, 24, 0, 40, 1),
(9, 20, 4.0, 24, 0, 29, 2),
(9, 23, 4.0, 24, 0, 42, 0),
(9, 24, 4.0, 24, 0, 39, 2),

-- Innings 10: RCB bowling vs KKR
(10, 17, 3.0, 18, 0, 46, 0),
(10, 15, 1.5, 11, 0, 25, 0),

-- Match 6: MI vs RR
-- Innings 11: RR bowling vs MI
(11, 30, 4.0, 24, 0, 22, 3),
(11, 29, 4.0, 24, 0, 11, 3),

-- Innings 12: MI bowling vs RR
(12, 10, 3.0, 18, 0, 26, 0),
(12, 9,  1.0, 6,  0, 10, 0),

-- Match 7: DC vs CSK
-- Innings 13: CSK bowling vs DC
(13, 6,  4.0, 24, 0, 42, 0),
(13, 3,  4.0, 24, 0, 43, 1),
(13, 5,  4.0, 24, 0, 31, 3),

-- Innings 14: DC bowling vs CSK
(14, 42, 4.0, 24, 1, 21, 2),
(14, 39, 3.0, 18, 0, 20, 1),
(14, 40, 4.0, 24, 0, 26, 0),

-- Match 8: LSG vs GT
-- Innings 15: GT bowling vs LSG
(15, 56, 4.0, 24, 0, 28, 1),
(15, 59, 4.0, 24, 0, 30, 1),

-- Innings 16: LSG bowling vs GT
(16, 54, 1.0, 6,  0, 13, 0),
(16, 53, 4.0, 24, 0, 11, 3),
(16, 52, 4.0, 24, 0, 8,  1),

-- Match 9: RR vs RCB
-- Innings 17: RR bowling vs RCB
(17, 30, 4.0, 24, 0, 30, 0),
(17, 29, 4.0, 24, 0, 34, 2),

-- Innings 18: RCB bowling vs RR
(18, 17, 4.0, 24, 0, 34, 1),
(18, 15, 2.0, 12, 0, 22, 0),

-- Match 10: MI vs CSK
-- Innings 19: MI bowling vs CSK
(19, 10, 4.0, 24, 0, 27, 0),
(19, 9,  3.0, 18, 0, 43, 2),

-- Innings 20: CSK bowling vs MI
(20, 6,  2.0, 12, 0, 15, 0),
(20, 3,  4.0, 24, 0, 37, 0),
(20, 5,  4.0, 24, 0, 28, 4),
(20, 4,  2.0, 12, 0, 19, 0);

-- ----------------------------------------------------------------------------
-- 8. INSERT FIELDING_PERFORMANCE (52 Records)
-- ----------------------------------------------------------------------------
INSERT INTO FIELDING_PERFORMANCE (innings_id, player_id, catches, stumpings, run_outs) VALUES
(1,  2,  2, 0, 0),
(1,  3,  1, 0, 0),
(2,  18, 1, 0, 0),
(3,  7,  1, 0, 0),
(3,  12, 1, 0, 0),
(3,  9,  1, 0, 0),
(4,  60, 1, 0, 0),
(4,  58, 1, 0, 0),
(5,  31, 0, 0, 1),
(5,  34, 1, 0, 0),
(6,  19, 1, 0, 0),
(6,  22, 1, 0, 0),
(7,  8,  1, 0, 0),
(7,  12, 1, 0, 0),
(8,  31, 1, 0, 0),
(8,  34, 1, 0, 0),
(9,  22, 2, 0, 0),
(9,  20, 0, 0, 1),
(10, 18, 0, 0, 0),
(11, 25, 2, 0, 0),
(11, 27, 1, 0, 0),
(12, 11, 1, 0, 0),
(13, 2,  2, 0, 0),
(13, 1,  1, 0, 0),
(14, 37, 1, 0, 0),
(14, 39, 1, 0, 0),
(15, 55, 1, 0, 0),
(16, 52, 1, 0, 0),
(16, 49, 1, 1, 0),
(17, 25, 1, 0, 0),
(18, 14, 1, 0, 0),
(18, 13, 1, 0, 0),
(19, 11, 1, 0, 0),
(20, 3,  1, 0, 0),
(20, 2,  1, 0, 0);

-- ----------------------------------------------------------------------------
-- 9. INSERT DELIVERIES (135 Detailed Ball-by-Ball Records)
-- Features: Powerplay balls, middle overs, boundaries, wickets, and death over finishes.
-- ----------------------------------------------------------------------------

-- A) Innings 19: CSK 20th Over vs MI (Hardik Pandya bowling to MS Dhoni & Shivam Dube)
-- Dhoni hits 3 consecutive sixes in an iconic finish!
INSERT INTO DELIVERIES (innings_id, over_number, ball_number, striker_id, bowler_id, runs_batter, extras, total_runs, wicket_type) VALUES
(19, 20, 1, 1, 9, 0, 0, 0, 'caught'),
(19, 20, 2, 2, 9, 6, 0, 6, NULL),
(19, 20, 3, 2, 9, 6, 0, 6, NULL),
(19, 20, 4, 2, 9, 6, 0, 6, NULL),
(19, 20, 5, 2, 9, 2, 0, 2, NULL),
(19, 20, 6, 2, 9, 0, 0, 0, NULL);

-- B) Innings 7: SRH vs MI Powerplay (Travis Head vs Jasprit Bumrah & Hardik Pandya)
INSERT INTO DELIVERIES (innings_id, over_number, ball_number, striker_id, bowler_id, runs_batter, extras, total_runs, wicket_type) VALUES
-- Over 1 (Bumrah)
(7, 1, 1, 32, 10, 0, 0, 0, NULL),
(7, 1, 2, 32, 10, 4, 0, 4, NULL),
(7, 1, 3, 32, 10, 0, 0, 0, NULL),
(7, 1, 4, 32, 10, 1, 0, 1, NULL),
(7, 1, 5, 33, 10, 0, 0, 0, NULL),
(7, 1, 6, 33, 10, 1, 0, 1, NULL),
-- Over 2 (Pandya)
(7, 2, 1, 33, 9, 4, 0, 4, NULL),
(7, 2, 2, 33, 9, 6, 0, 6, NULL),
(7, 2, 3, 33, 9, 0, 1, 1, NULL),
(7, 2, 4, 33, 9, 4, 0, 4, NULL),
(7, 2, 5, 33, 9, 1, 0, 1, NULL),
(7, 2, 6, 32, 9, 6, 0, 6, NULL),
-- Over 3 (Bumrah)
(7, 3, 1, 32, 10, 0, 0, 0, NULL),
(7, 3, 2, 32, 10, 4, 0, 4, NULL),
(7, 3, 3, 32, 10, 0, 0, 0, NULL),
(7, 3, 4, 32, 10, 2, 0, 2, NULL),
(7, 3, 5, 32, 10, 1, 0, 1, NULL),
(7, 3, 6, 33, 10, 0, 0, 0, NULL),
-- Over 4 (Pandya)
(7, 4, 1, 33, 9, 6, 0, 6, NULL),
(7, 4, 2, 33, 9, 6, 0, 6, NULL),
(7, 4, 3, 33, 9, 1, 0, 1, NULL),
(7, 4, 4, 32, 9, 4, 0, 4, NULL),
(7, 4, 5, 32, 9, 4, 0, 4, NULL),
(7, 4, 6, 32, 9, 1, 0, 1, NULL);

-- C) Innings 20: MI Chase vs CSK (Rohit Sharma & Ishan Kishan vs Matheesha Pathirana & Ravindra Jadeja)
INSERT INTO DELIVERIES (innings_id, over_number, ball_number, striker_id, bowler_id, runs_batter, extras, total_runs, wicket_type) VALUES
-- Over 8 (Jadeja)
(20, 8, 1, 7,  3, 1, 0, 1, NULL),
(20, 8, 2, 11, 3, 0, 0, 0, NULL),
(20, 8, 3, 11, 3, 4, 0, 4, NULL),
(20, 8, 4, 11, 3, 1, 0, 1, NULL),
(20, 8, 5, 7,  3, 6, 0, 6, NULL),
(20, 8, 6, 7,  3, 1, 0, 1, NULL),
-- Over 9 (Pathirana breakthrough)
(20, 9, 1, 11, 5, 0, 0, 0, 'caught'),
(20, 9, 2, 8,  5, 0, 0, 0, NULL),
(20, 9, 3, 8,  5, 0, 0, 0, 'caught'),
(20, 9, 4, 12, 5, 4, 0, 4, NULL),
(20, 9, 5, 12, 5, 0, 0, 0, NULL),
(20, 9, 6, 12, 5, 1, 0, 1, NULL),
-- Over 15 (Pathirana)
(20, 15, 1, 12, 5, 0, 0, 0, 'caught'),
(20, 15, 2, 9,  5, 1, 0, 1, NULL),
(20, 15, 3, 7,  5, 4, 0, 4, NULL),
(20, 15, 4, 7,  5, 0, 0, 0, NULL),
(20, 15, 5, 7,  5, 2, 0, 2, NULL),
(20, 15, 6, 7,  5, 1, 0, 1, NULL),
-- Over 20 (Final Over - Mustafizur / Deepak Chahar)
(20, 20, 1, 7, 6, 4, 0, 4, NULL),
(20, 20, 2, 7, 6, 4, 0, 4, NULL),
(20, 20, 3, 7, 6, 1, 0, 1, NULL),
(20, 20, 4, 10,6, 0, 0, 0, NULL),
(20, 20, 5, 10,6, 0, 0, 0, NULL),
(20, 20, 6, 10,6, 1, 0, 1, NULL);

-- D) Innings 6: KKR vs SRH (Harshit Rana defense in final over)
INSERT INTO DELIVERIES (innings_id, over_number, ball_number, striker_id, bowler_id, runs_batter, extras, total_runs, wicket_type) VALUES
(6, 20, 1, 34, 24, 6, 0, 6, NULL),
(6, 20, 2, 34, 24, 1, 0, 1, NULL),
(6, 20, 3, 31, 24, 1, 0, 1, NULL),
(6, 20, 4, 34, 24, 0, 0, 0, NULL),
(6, 20, 5, 34, 24, 0, 0, 0, 'caught'),
(6, 20, 6, 31, 24, 0, 0, 0, 'caught');

-- E) Innings 10: KKR vs RCB (Sunil Narine blitz at Chinnaswamy)
INSERT INTO DELIVERIES (innings_id, over_number, ball_number, striker_id, bowler_id, runs_batter, extras, total_runs, wicket_type) VALUES
-- Over 1 (Siraj)
(10, 1, 1, 21, 17, 0, 0, 0, NULL),
(10, 1, 2, 21, 17, 6, 0, 6, NULL),
(10, 1, 3, 21, 17, 4, 0, 4, NULL),
(10, 1, 4, 21, 17, 0, 1, 1, NULL),
(10, 1, 5, 21, 17, 6, 0, 6, NULL),
(10, 1, 6, 21, 17, 1, 0, 1, NULL),
-- Over 2 (Maxwell)
(10, 2, 1, 21, 15, 6, 0, 6, NULL),
(10, 2, 2, 21, 15, 4, 0, 4, NULL),
(10, 2, 3, 21, 15, 0, 0, 0, NULL),
(10, 2, 4, 21, 15, 6, 0, 6, NULL),
(10, 2, 5, 21, 15, 1, 0, 1, NULL),
(10, 2, 6, 19, 15, 1, 0, 1, NULL),
-- Over 3 (Siraj)
(10, 3, 1, 19, 17, 4, 0, 4, NULL),
(10, 3, 2, 19, 17, 0, 0, 0, NULL),
(10, 3, 3, 19, 17, 1, 0, 1, NULL),
(10, 3, 4, 21, 17, 6, 0, 6, NULL),
(10, 3, 5, 21, 17, 0, 0, 0, NULL),
(10, 3, 6, 21, 17, 2, 0, 2, NULL);

-- F) Innings 11: MI vs RR (Trent Boult powerplay swing clinic)
INSERT INTO DELIVERIES (innings_id, over_number, ball_number, striker_id, bowler_id, runs_batter, extras, total_runs, wicket_type) VALUES
-- Over 1 (Boult)
(11, 1, 1, 7,  30, 0, 0, 0, 'caught'),
(11, 1, 2, 8,  30, 0, 0, 0, NULL),
(11, 1, 3, 8,  30, 0, 0, 0, 'caught'),
(11, 1, 4, 12, 30, 0, 0, 0, NULL),
(11, 1, 5, 12, 30, 1, 0, 1, NULL),
(11, 1, 6, 11, 30, 4, 0, 4, NULL),
-- Over 2 (Burger)
(11, 2, 1, 12, 30, 1, 0, 1, NULL),
(11, 2, 2, 11, 30, 0, 0, 0, NULL),
(11, 2, 3, 11, 30, 0, 0, 0, 'caught'),
(11, 2, 4, 9,  30, 4, 0, 4, NULL),
(11, 2, 5, 9,  30, 0, 0, 0, NULL),
(11, 2, 6, 9,  30, 1, 0, 1, NULL);

-- G) Innings 9: RCB vs KKR (Virat Kohli masterclass innings progression)
INSERT INTO DELIVERIES (innings_id, over_number, ball_number, striker_id, bowler_id, runs_batter, extras, total_runs, wicket_type) VALUES
-- Over 5 (Narine vs Kohli)
(9, 5, 1, 13, 21, 1, 0, 1, NULL),
(9, 5, 2, 14, 21, 0, 0, 0, NULL),
(9, 5, 3, 14, 21, 1, 0, 1, NULL),
(9, 5, 4, 13, 21, 2, 0, 2, NULL),
(9, 5, 5, 13, 21, 4, 0, 4, NULL),
(9, 5, 6, 13, 21, 1, 0, 1, NULL),
-- Over 18 (Russell vs Kohli & Karthik)
(9, 18, 1, 13, 20, 6, 0, 6, NULL),
(9, 18, 2, 13, 20, 1, 0, 1, NULL),
(9, 18, 3, 18, 20, 6, 0, 6, NULL),
(9, 18, 4, 18, 20, 4, 0, 4, NULL),
(9, 18, 5, 18, 20, 1, 0, 1, NULL),
(9, 18, 6, 13, 20, 2, 0, 2, NULL);

-- H) Innings 18: RR vs RCB (Jos Buttler century chase vs Siraj)
INSERT INTO DELIVERIES (innings_id, over_number, ball_number, striker_id, bowler_id, runs_batter, extras, total_runs, wicket_type) VALUES
-- Over 19 (Siraj to Buttler)
(18, 19, 1, 27, 17, 1, 0, 1, NULL),
(18, 19, 2, 28, 17, 0, 0, 0, 'caught'),
(18, 19, 3, 27, 17, 2, 0, 2, NULL),
(18, 19, 4, 27, 17, 4, 0, 4, NULL),
(18, 19, 5, 27, 17, 1, 0, 1, NULL),
(18, 19, 6, 27, 17, 6, 0, 6, NULL);
