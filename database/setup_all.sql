-- ============================================================================
-- CRICKET ANALYSIS APPLICATION: MASTER SETUP SCRIPT
-- File: setup_all.sql
-- Description: Executes all simplified scripts sequentially in psql.
-- ============================================================================

\echo '--- 1/4: Creating Tables (02_create_tables.sql) ---'
\i 02_create_tables.sql

\echo '--- 2/4: Inserting Sample Data (03_insert_sample_data.sql) ---'
\i 03_insert_sample_data.sql

\echo '--- 3/4: Creating Views (04_create_views.sql) ---'
\i 04_create_views.sql

\echo '--- 4/4: Creating Triggers (05_create_triggers.sql) ---'
\i 05_create_triggers.sql

\echo '========================================================'
\echo ' Cricket Analytics Database setup completed successfully! '
\echo '========================================================'
