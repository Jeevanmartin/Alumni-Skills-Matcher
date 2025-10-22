-- University Alumni Skills Matcher - Minimal Viable Schema
-- File: sql/schema.sql

-- 1. ALUMNI Table
CREATE TABLE Alumni (
    AlumniID INTEGER PRIMARY KEY,
    FirstName TEXT NOT NULL,
    LastName TEXT NOT NULL,
    GraduationYear INTEGER,
    Email TEXT UNIQUE NOT NULL
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
    ProficiencyLevel TEXT CHECK(ProficiencyLevel IN ('Beginner', 'Intermediate', 'Expert')),
    FOREIGN KEY (AlumniID) REFERENCES Alumni(AlumniID),
    FOREIGN KEY (SkillID) REFERENCES Skills(SkillID)
);

-- Insert Sample Skills
INSERT INTO Skills (SkillName) VALUES
('Python Programming'),
('Data Analysis'),
('SQL Database Management'),
('Cloud Computing (AWS)'),
('Web Design (UI/UX)'),
('Financial Modeling'),
('Machine Learning'),
('Project Management');

-- Insert Sample Alumni
INSERT INTO Alumni (FirstName, LastName, GraduationYear, Email) VALUES
('Alice', 'Johnson', 2018, 'alice@alumni.edu'),
('Bob', 'Smith', 2019, 'bob@alumni.edu'),
('Charlie', 'Brown', 2021, 'charlie@alumni.edu'),
('Diana', 'Prince', 2017, 'diana@alumni.edu');

-- Match Alumni to Skills
-- Alice (Python, SQL, Data Analysis)
INSERT INTO Alumni_Skills (AlumniID, SkillID, ProficiencyLevel) VALUES
(1, 1, 'Expert'),
(1, 3, 'Intermediate'),
(1, 2, 'Expert');

-- Bob (Cloud Computing, Project Management)
INSERT INTO Alumni_Skills (AlumniID, SkillID, ProficiencyLevel) VALUES
(2, 4, 'Expert'),
(2, 8, 'Intermediate');

-- Charlie (Web Design, Python)
INSERT INTO Alumni_Skills (AlumniID, SkillID, ProficiencyLevel) VALUES
(3, 5, 'Beginner'),
(3, 1, 'Intermediate');

-- Diana (Financial Modeling, Data Analysis, Machine Learning)
INSERT INTO Alumni_Skills (AlumniID, SkillID, ProficiencyLevel) VALUES
(4, 6, 'Expert'),
(4, 2, 'Expert'),
(4, 7, 'Intermediate');

-- ** DEMO QUERY **
-- Find all alumni who have 'Data Analysis' skills
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