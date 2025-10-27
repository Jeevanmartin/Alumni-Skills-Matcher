# File: create_db.py
import sqlite3
import os
import csv 

# --- Configuration ---
DB_NAME = 'alumni_matcher.db'
SQL_FILE_PATH = os.path.join('sql', 'schema.sql')
CSV_FILE_PATH = 'alumni_data.csv' 
# ---------------------

def create_database():
    """
    Connects to the database, executes the base schema, loads data from CSV,
    and runs a demo query to verify data integrity.
    """
    conn = None 
    try:
        # 1. Connect and Execute Base Schema (Drops existing tables and creates new ones)
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        if not os.path.exists(SQL_FILE_PATH):
            print(f"🚨 Error: SQL file not found at {SQL_FILE_PATH}")
            print("Ensure 'schema.sql' is in the 'sql/' directory.")
            return

        with open(SQL_FILE_PATH, 'r') as f:
            sql_script = f.read()
        
        cursor.executescript(sql_script)
        conn.commit()

        # 2. Load Data from CSV
        if os.path.exists(CSV_FILE_PATH):
            print(f"🔄 Loading data from {CSV_FILE_PATH}...")
            
            with open(CSV_FILE_PATH, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                
                alumni_map = {} 
                skill_map = {}  
                
                # Helper function to generate the next unique ID
                def get_next_id(table, id_col):
                    cursor.execute(f"SELECT MAX({id_col}) FROM {table}")
                    max_id = cursor.fetchone()[0]
                    return (max_id or 0) + 1

                for row in reader:
                    # A. Insert/Get Alumni
                    alumni_key = (row['FirstName'], row['LastName'])
                    if alumni_key not in alumni_map:
                        alumni_id = get_next_id('Alumni', 'AlumniID')
                        # Note: We are ignoring GradYear and Email for now since CSV doesn't have it
                        cursor.execute("INSERT INTO Alumni (AlumniID, FirstName, LastName) VALUES (?, ?, ?)", 
                                        (alumni_id, row['FirstName'], row['LastName']))
                        alumni_map[alumni_key] = alumni_id
                    else:
                        alumni_id = alumni_map[alumni_key]

                    # B. Insert/Get Skill
                    skill_name = row['SkillName']
                    if skill_name not in skill_map:
                        skill_id = get_next_id('Skills', 'SkillID')
                        cursor.execute("INSERT INTO Skills (SkillID, SkillName) VALUES (?, ?)", 
                                        (skill_id, skill_name))
                        skill_map[skill_name] = skill_id
                    else:
                        skill_id = skill_map[skill_name]
                    
                    # C. Insert Alumni_Skills Relationship
                    cursor.execute("INSERT INTO Alumni_Skills (AlumniID, SkillID, ProficiencyLevel) VALUES (?, ?, ?)", 
                                    (alumni_id, skill_id, row['ProficiencyLevel']))

            conn.commit()
            print(f"✅ Database '{DB_NAME}' created and populated successfully.")
        else:
             print(f"🚨 Warning: CSV data file not found at {CSV_FILE_PATH}. Only schema executed.")


        # --- 3. Run Demo Query (Verification) ---
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
            S.SkillName = 'Python'
        ORDER BY ASk.ProficiencyLevel DESC;
        """
        print("\n--- DEMO QUERY RESULTS: Alumni with 'Python' ---")
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
        if conn:
            conn.close()

if __name__ == "__main__":
    create_database()