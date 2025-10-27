# University Alumni Skills Matcher (DBMS Project MVP)

This is a minimal viable database project demonstrating a conceptual **Alumni Skills Matcher** system. It uses **SQLite** for simplicity and portability, and Python to manage the database creation.

## 🚀 Project Goal

To efficiently match current students or faculty seeking specific expertise with alumni who possess those skills using a relational database model.

## 📚 Database Schema Overview

| Table | Purpose | Key Columns |
|---|---|---|
| `Alumni` | Stores core alumni information. | `AlumniID`, `FirstName`, `LastName`, `Email` |
| `Skills` | A master list of all available skills. | `SkillID`, `SkillName` |
| `Alumni_Skills` | A many-to-many junction table to link alumni to their skills and proficiency levels. | `AlumniID`, `SkillID`, `ProficiencyLevel` |

## ⚙️ Setup and Run (Requires Python 3)

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Jeevanmartin/Alumni-Skills-Matcher
    cd University-Alumni-Skills-Matcher
    ```

2.  **Run the setup script:**
    ```bash
    python create_db.py
    ```
    This command executes the `sql/schema.sql` file, creates the `alumni_matcher.db` database, and runs a sample "skills match" query.
