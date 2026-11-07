-- ============================================================================
-- CRICKET ANALYSIS APPLICATION: DATABASE INITIALIZATION
-- File: 01_create_database.sql
-- Description: Simple and clean database creation script for PostgreSQL.
-- ============================================================================

-- Drop the database if it already exists (useful when restarting from scratch)
DROP DATABASE IF EXISTS cricket_analytics;

-- Create the database
CREATE DATABASE cricket_analytics;

-- Connect to the newly created database (in psql)
\connect cricket_analytics;
