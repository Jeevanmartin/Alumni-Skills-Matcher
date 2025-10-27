# File: app.py
from flask import Flask, render_template, request
import sqlite3
import os

app = Flask(__name__)
DB_NAME = 'alumni_matcher.db'

# --- Utility Function to Fetch All Skills ---
def get_all_skills():
    """Fetches all unique skill names from the Skills table for the dropdown."""
    conn = None
    skills = []
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT SkillName FROM Skills ORDER BY SkillName")
        skills = [row[0] for row in cursor.fetchall()]
    except sqlite3.Error as e:
        print(f"Database error fetching skills: {e}")
    finally:
        if conn:
            conn.close()
    return skills


# --- Utility Function to Query Database (Case-Insensitive) ---
def get_alumni_data(skill_name=""):
    """
    Connects to the database and runs the query to find alumni with the specified skill.
    Uses COLLATE NOCASE for case-insensitive matching.
    """
    conn = None
    results = []
    
    if not skill_name:
        return []

    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        query = """
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
            S.SkillName LIKE ? COLLATE NOCASE
        ORDER BY
            CASE ASk.ProficiencyLevel
                WHEN 'Expert' THEN 1
                WHEN 'Intermediate' THEN 2
                ELSE 3
            END, A.LastName;
        """
        
        # NOTE: We search for the exact skill name entered by the user
        cursor.execute(query, (skill_name,))
        
        columns = [col[0] for col in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            conn.close()
    
    return results


# --- Flask Routes ---
@app.route('/', methods=['GET', 'POST'])
def index():
    # Fetch all skills for the HTML datalist
    all_skills = get_all_skills()
    
    search_skill = "" 
    alumni_list = []
    
    if request.method == 'POST':
        # Get the skill from the search form
        search_skill = request.form.get('skill', '').strip()
        alumni_list = get_alumni_data(search_skill)
    
    # Render the HTML template, passing all required data
    return render_template('index.html', 
                           alumni=alumni_list, 
                           current_skill=search_skill,
                           all_skills=all_skills)

if __name__ == '__main__':
    if not os.path.exists(DB_NAME):
        print(f"🚨 Error: Database '{DB_NAME}' not found. Please run create_db.py first.")
    else:
        app.run(debug=True)