"""
Database connectivity module for Cricket Analytics.
Provides safe parameterized query execution and error handling.
"""
from contextlib import contextmanager
from typing import Any, Dict, List, Optional, Tuple
import pandas as pd
import psycopg
from psycopg.rows import dict_row
import streamlit as st

from config import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER


def get_db_params() -> dict:
    return {
        "host": DB_HOST,
        "port": DB_PORT,
        "dbname": DB_NAME,
        "user": DB_USER,
        "password": DB_PASSWORD,
        "connect_timeout": 5,
    }


@contextmanager
def get_connection():
    """Context manager for database connections."""
    conn = None
    try:
        conn = psycopg.connect(**get_db_params())
        yield conn
    except Exception as e:
        raise ConnectionError(f"Database connection error: {e}")
    finally:
        if conn and not conn.closed:
            conn.close()


def test_connection() -> Tuple[bool, Optional[str]]:
    """Test if database is reachable."""
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1;")
                cur.fetchone()
        return True, None
    except Exception as e:
        return False, str(e)


@st.cache_data(ttl=60, show_spinner=False)
def execute_query(sql: str, params: Optional[Tuple[Any, ...]] = None) -> pd.DataFrame:
    """
    Executes a read query with optional parameters and returns a Pandas DataFrame.
    Parameterized to prevent SQL injection.
    Cached for 60 seconds for snappy UI navigation.
    """
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, params or ())
                if cur.description:
                    columns = [desc[0] for desc in cur.description]
                    data = cur.fetchall()
                    return pd.DataFrame(data, columns=columns)
                return pd.DataFrame()
    except Exception as e:
        st.error(f"Database Query Error: {e}")
        return pd.DataFrame()


def execute_one(sql: str, params: Optional[Tuple[Any, ...]] = None) -> Optional[Dict[str, Any]]:
    """
    Executes a query and returns a single row as a dictionary.
    """
    try:
        with get_connection() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute(sql, params or ())
                row = cur.fetchone()
                return dict(row) if row else None
    except Exception as e:
        st.error(f"Database Query Error: {e}")
        return None

