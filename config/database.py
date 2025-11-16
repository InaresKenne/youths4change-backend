import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_db_connection():
    """
    Create and return a database connection
    Uses connection pooling for better performance
    """
    try:
        # Get connection string from environment variable
        database_url = os.getenv('DATABASE_URL')
        
        if not database_url:
            raise ValueError("DATABASE_URL not found in environment variables")
        
        # Create connection
        conn = psycopg2.connect(
            database_url,
            cursor_factory=RealDictCursor  # Returns results as dictionaries
        )
        
        return conn
    
    except Exception as e:
        print(f"Error connecting to database: {e}")
        raise

def execute_query(query, params=None, fetch=True):
    """
    Execute a database query and return results
    
    Args:
        query: SQL query string
        params: Tuple of parameters for the query
        fetch: Boolean - whether to fetch results (SELECT) or not (INSERT/UPDATE/DELETE)
    
    Returns:
        List of dictionaries for SELECT queries
        Number of affected rows for INSERT/UPDATE/DELETE
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute(query, params or ())
        
        if fetch:
            # SELECT query - return results
            result = cursor.fetchall()
            conn.close()
            return result
        else:
            # INSERT/UPDATE/DELETE - commit and return affected rows
            conn.commit()
            affected_rows = cursor.rowcount
            
            # For INSERT with RETURNING, fetch the returned data
            if query.strip().upper().startswith('INSERT') and 'RETURNING' in query.upper():
                result = cursor.fetchone()
                conn.close()
                return result
            
            conn.close()
            return affected_rows
    
    except Exception as e:
        conn.rollback()
        conn.close()
        raise e