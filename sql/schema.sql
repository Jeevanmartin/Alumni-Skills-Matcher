-- University Alumni Skills Matcher - Base Schema
-- File: sql/schema.sql

-- Standard practice: Drop tables before creating them to ensure a clean start
-- This is essential for the create_db.py script to run successfully multiple times.
DROP TABLE IF EXISTS Alumni_Skills;
DROP TABLE IF EXISTS Alumni;
DROP TABLE IF EXISTS Skills;

-- 1. ALUMNI Table
CREATE TABLE Alumni (
    AlumniID INTEGER PRIMARY KEY,
    FirstName TEXT NOT NULL,
    LastName TEXT NOT NULL,
    -- NOTE: GraduationYear and Email are defined here, but not used in the CSV data for simplicity
    GraduationYear INTEGER,
    Email TEXT UNIQUE
);

-- 2. SKILLS Table (Master list of skills)
CREATE TABLE Skills (
    SkillID INTEGER PRIMARY KEY,
    SkillName TEXT UNIQUE NOT NULL
);

-- 3. ALUMNI_SKILLS Table (Many-to-Many relationship)
CREATE TABLE Alumni_Skills (
    AlumniSkillID INTEGER PRIMARY KEY,
    AlumniID INTEGER,
    SkillID INTEGER,
    -- ProficiencyLevel ensures data integrity by limiting values
    ProficiencyLevel TEXT CHECK(ProficiencyLevel IN ('Beginner', 'Intermediate', 'Expert')),
    FOREIGN KEY (AlumniID) REFERENCES Alumni(AlumniID),
    FOREIGN KEY (SkillID) REFERENCES Skills(SkillID)
);

-- NOTE: All INSERT statements (for Sample Skills, Alumni, and Matches) are REMOVED.
-- Data will be inserted by the create_db.py script from the alumni_data.csv file.