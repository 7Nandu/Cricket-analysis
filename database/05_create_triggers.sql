-- ============================================================================
-- CRICKET ANALYSIS APPLICATION: DATABASE TRIGGERS
-- File: 05_create_triggers.sql
-- Description: 4 clean, practical, and genuinely useful database triggers.
--              Each trigger enforces a specific cricket scoring rule or data
--              consistency check without unnecessary complexity.
-- ============================================================================

-- ----------------------------------------------------------------------------
-- TRIGGER 1: trg_set_delivery_total (Table: DELIVERIES)
-- Purpose: Automatically calculates total_runs = runs_batter + extras.
-- Why it's useful: The scorer only enters runs from the bat and extras;
--                  the database guarantees total_runs is always accurate.
-- ----------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION fn_set_delivery_total()
RETURNS TRIGGER AS $$
BEGIN
    NEW.total_runs := COALESCE(NEW.runs_batter, 0) + COALESCE(NEW.extras, 0);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_set_delivery_total ON DELIVERIES;

CREATE TRIGGER trg_set_delivery_total
    BEFORE INSERT OR UPDATE ON DELIVERIES
    FOR EACH ROW
    EXECUTE FUNCTION fn_set_delivery_total();


-- ----------------------------------------------------------------------------
-- TRIGGER 2: trg_validate_overs_format (Table: BOWLING_PERFORMANCE)
-- Purpose: Enforces cricket overs rules. In cricket, 4.3 means 4 overs and 3 balls.
--          An over only has 6 balls, so decimals like 3.6, 4.8, or 2.9 are invalid.
-- Why it's useful: Prevents users from accidentally inserting impossible overs.
-- ----------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION fn_validate_overs_format()
RETURNS TRIGGER AS $$
DECLARE
    v_balls INT;
BEGIN
    -- Extract the ball part after decimal (e.g. 4.3 -> 3, 4.0 -> 0)
    v_balls := ROUND((NEW.overs_bowled * 10)::NUMERIC % 10);

    IF v_balls > 5 THEN
        RAISE EXCEPTION 'Invalid cricket overs: %. Balls bowled cannot exceed 5 after decimal point.', NEW.overs_bowled;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_validate_overs_format ON BOWLING_PERFORMANCE;

CREATE TRIGGER trg_validate_overs_format
    BEFORE INSERT OR UPDATE ON BOWLING_PERFORMANCE
    FOR EACH ROW
    EXECUTE FUNCTION fn_validate_overs_format();


-- ----------------------------------------------------------------------------
-- TRIGGER 3: trg_sync_batting_not_out (Table: BATTING_PERFORMANCE)
-- Purpose: Keeps the boolean not_out flag in sync with the dismissal description.
-- Why it's useful: Prevents inconsistent records where a player has a dismissal
--                  like 'caught b Bumrah' but not_out is accidentally left TRUE.
-- ----------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION fn_sync_batting_not_out()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.dismissal IS NULL OR LOWER(TRIM(NEW.dismissal)) = 'not out' THEN
        NEW.not_out := TRUE;
        NEW.dismissal := 'not out';
    ELSE
        NEW.not_out := FALSE;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_sync_batting_not_out ON BATTING_PERFORMANCE;

CREATE TRIGGER trg_sync_batting_not_out
    BEFORE INSERT OR UPDATE ON BATTING_PERFORMANCE
    FOR EACH ROW
    EXECUTE FUNCTION fn_sync_batting_not_out();


-- ----------------------------------------------------------------------------
-- TRIGGER 4: trg_validate_player_age (Table: PLAYERS)
-- Purpose: Ensures a player's date of birth is valid (must be at least 15 years
--          old and not a future date).
-- Why it's useful: Validates basic player registration data at the database level.
-- ----------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION fn_validate_player_age()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.date_of_birth > (CURRENT_DATE - INTERVAL '15 years') THEN
        RAISE EXCEPTION 'Invalid date of birth: %. Player must be at least 15 years old.', NEW.date_of_birth;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_validate_player_age ON PLAYERS;

CREATE TRIGGER trg_validate_player_age
    BEFORE INSERT OR UPDATE ON PLAYERS
    FOR EACH ROW
    EXECUTE FUNCTION fn_validate_player_age();
