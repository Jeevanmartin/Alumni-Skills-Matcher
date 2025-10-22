# File: create_db.py
import sqlite3
import os

# --- Configuration ---
# The name of the SQLite database file to be created
DB_NAME = 'alumni_matcher.db'

# Define the path to the SQL schema file using os.path.join 
# for cross-platform compatibility. It looks for 'schema.sql' inside the 'sql' folder.
SQL_FILE_PATH = os.path.join('sql', 'schema.sql')

# ---------------------

def create_database():
    """
    Connects to the database, reads the SQL script, executes it, and runs a demo query.
    """
    conn = None # Initialize connection
    try:
        # Connects to the database file (creates it if it doesn't exist)
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        # Check if the SQL file exists before trying to read it
        if not os.path.exists(SQL_FILE_PATH):
            print(f"🚨 Error: SQL file not found at {SQL_FILE_PATH}")
            print("Ensure 'schema.sql' is in the 'sql/' directory.")
            return

        # Read the entire SQL script
        with open(SQL_FILE_PATH, 'r') as f:
            sql_script = f.read()

        # Execute all DDL and DML commands from the script
        cursor.executescript(sql_script)
        conn.commit()
        print(f"✅ Database '{DB_NAME}' created and populated successfully.")

        # --- Run Demo Query ---
        demo_query = """
        SELECT
            A.FirstName,
            A.LastName,
            ASk.ProficiencyLevel,
            S.SkillName
        FROM
            Alumni A
        JOIN
            Alumni_Skills ASk ON A.AlumniID = ASk.AlumniID
        JOIN
            Skills S ON ASk.SkillID = S.SkillID
        WHERE
            S.SkillName = 'Data Analysis';
        """
        print("\n--- DEMO QUERY RESULTS: Alumni with 'Data Analysis' ---")
        cursor.execute(demo_query)
        results = cursor.fetchall()
        for row in results:
            print(row)
        # ----------------------

    except sqlite3.Error as e:
        print(f"🚨 A database error occurred: {e}")
    except Exception as e:
        print(f"🚨 An unexpected error occurred: {e}")
    finally:
        # Ensure the connection is closed
        if conn:
            conn.close()

if __name__ == "__main__":
    create_database()