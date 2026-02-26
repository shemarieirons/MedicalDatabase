"""
backend.py
This module handles all SQLite database connections and queries for the Medical Records System.
It provides functions to initialize the database schema and perform CRUD operations
for patients, treatments, tests, diagnoses, and visit records.
"""
import sqlite3
import os

DB_FILE = 'medical_records.db'

def get_connection():
    """Establish and return a connection to the SQLite database."""
    return sqlite3.connect(DB_FILE)

def initialize_database():
    """Create database tables if they do not exist."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Table: patient
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS patient (
            pid INTEGER PRIMARY KEY AUTOINCREMENT,
            fname TEXT NOT NULL,
            lname TEXT NOT NULL,
            address1 TEXT,
            address2 TEXT,
            city TEXT,
            parish TEXT,
            country TEXT,
            gender TEXT
        )
    ''')
    
    # Table: treat
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS treat (
            treatid INTEGER PRIMARY KEY AUTOINCREMENT,
            tname TEXT NOT NULL
        )
    ''')
    
    # Table: test
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS test (
            testid INTEGER PRIMARY KEY AUTOINCREMENT,
            testname TEXT NOT NULL
        )
    ''')
    
    # Table: Diagnosis
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Diagnosis (
            diagid INTEGER PRIMARY KEY AUTOINCREMENT,
            dname TEXT NOT NULL,
            diagtreatid INTEGER,
            diagtestid INTEGER,
            FOREIGN KEY (diagtreatid) REFERENCES treat(treatid),
            FOREIGN KEY (diagtestid) REFERENCES test(testid)
        )
    ''')
    
    # Table: PtVisit
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS PtVisit (
            visitcode INTEGER PRIMARY KEY AUTOINCREMENT,
            visitptid INTEGER,
            visitdiagid INTEGER,
            visitdate TEXT NOT NULL,
            doctor TEXT NOT NULL,
            visittestid INTEGER,
            FOREIGN KEY (visitptid) REFERENCES patient(pid),
            FOREIGN KEY (visitdiagid) REFERENCES Diagnosis(diagid),
            FOREIGN KEY (visittestid) REFERENCES test(testid)
        )
    ''')
    
    conn.commit()
    conn.close()

def add_patient(fname, lname, address1, address2, city, parish, country, gender):
    """
    Insert a new patient record into the database.
    
    Args:
        fname (str): Patient's first name.
        lname (str): Patient's last name.
        address1 (str): Address line 1.
        address2 (str): Address line 2.
        city (str): City of residence.
        parish (str): Parish/state of residence.
        country (str): Country of residence.
        gender (str): Gender of the patient.
        
    Returns:
        int: The auto-generated patient ID (pid).
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO patient (fname, lname, address1, address2, city, parish, country, gender)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (fname, lname, address1, address2, city, parish, country, gender))
    conn.commit()
    pid = cursor.lastrowid
    conn.close()
    return pid

def add_treatment(tname):
    """
    Add a new treatment to the treat table.
    
    Args:
        tname (str): The name of the treatment.
        
    Returns:
        int: The auto-generated treatment ID (treatid).
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO treat (tname) VALUES (?)', (tname,))
    conn.commit()
    tid = cursor.lastrowid
    conn.close()
    return tid

def add_test(testname):
    """
    Add a new medical test to the test table.
    
    Args:
        testname (str): The name of the test.
        
    Returns:
        int: The auto-generated test ID (testid).
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO test (testname) VALUES (?)', (testname,))
    conn.commit()
    tid = cursor.lastrowid
    conn.close()
    return tid

def add_diagnosis(dname, diagtreatid, diagtestid):
    """
    Add a new diagnosis mapped to a treatment and a test.
    
    Args:
        dname (str): The name of the diagnosis.
        diagtreatid (int or None): The ID of the associated treatment.
        diagtestid (int or None): The ID of the associated test.
        
    Returns:
        int: The auto-generated diagnosis ID (diagid).
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO Diagnosis (dname, diagtreatid, diagtestid)
        VALUES (?, ?, ?)
    ''', (dname, diagtreatid, diagtestid))
    conn.commit()
    did = cursor.lastrowid
    conn.close()
    return did

def record_visit(visitptid, visitdiagid, visitdate, doctor, visittestid):
    """
    Record a new patient visit.
    
    Args:
        visitptid (int): ID of the patient.
        visitdiagid (int or None): ID of the diagnosis (if any).
        visitdate (str): Date of the visit in YYYY-MM-DD format.
        doctor (str): Name of the attending physician.
        visittestid (int or None): ID of the test performed (if any).
        
    Returns:
        int: The auto-generated visit code (visitcode).
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO PtVisit (visitptid, visitdiagid, visitdate, doctor, visittestid)
        VALUES (?, ?, ?, ?, ?)
    ''', (visitptid, visitdiagid, visitdate, doctor, visittestid))
    conn.commit()
    vid = cursor.lastrowid
    conn.close()
    return vid

def get_patient_history(pid):
    """Retrieve visit history for a specific patient."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT v.visitdate, v.doctor, d.dname, t.tname, ts.testname
        FROM PtVisit v
        LEFT JOIN Diagnosis d ON v.visitdiagid = d.diagid
        LEFT JOIN treat t ON d.diagtreatid = t.treatid
        LEFT JOIN test ts ON v.visittestid = ts.testid
        WHERE v.visitptid = ?
        ORDER BY v.visitdate DESC
    ''', (pid,))
    results = cursor.fetchall()
    conn.close()
    return results

def basic_analytics():
    """Return dictionary of basic analytical insights."""
    conn = get_connection()
    cursor = conn.cursor()
    
    analytics = {}
    
    # Total patients
    cursor.execute('SELECT COUNT(*) FROM patient')
    analytics['total_patients'] = cursor.fetchone()[0]
    
    # Total visits
    cursor.execute('SELECT COUNT(*) FROM PtVisit')
    analytics['total_visits'] = cursor.fetchone()[0]
    
    # Most common diagnosis
    cursor.execute('''
        SELECT d.dname, COUNT(v.visitcode) as count
        FROM PtVisit v
        JOIN Diagnosis d ON v.visitdiagid = d.diagid
        GROUP BY d.diagid
        ORDER BY count DESC
        LIMIT 1
    ''')
    row = cursor.fetchone()
    analytics['most_common_diagnosis'] = row if row else ("None", 0)
    
    conn.close()
    return analytics

def get_all_patients():
    """Retrieve all patients from the database."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM patient')
    results = cursor.fetchall()
    conn.close()
    return results

def get_all_diagnoses():
    """Retrieve all diagnoses from the database."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Diagnosis')
    results = cursor.fetchall()
    conn.close()
    return results

def get_all_tests():
    """Retrieve all tests from the database."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM test')
    results = cursor.fetchall()
    conn.close()
    return results

def get_all_treatments():
    """Retrieve all treatments from the database."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM treat')
    results = cursor.fetchall()
    conn.close()
    return results

def get_all_visits():
    """
    Retrieve all visit records augmented with patient and medical details.
    
    Returns:
        list of tuples: Each tuple contains (visitcode, patient_full_name, diagnosis_name,
                        visitdate, doctor, testname).
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    # Joins tables to get human-readable names instead of foreign keys
    cursor.execute('''
        SELECT v.visitcode, p.fname || ' ' || p.lname, d.dname, v.visitdate, v.doctor, t.testname
        FROM PtVisit v
        JOIN patient p ON v.visitptid = p.pid
        LEFT JOIN Diagnosis d ON v.visitdiagid = d.diagid
        LEFT JOIN test t ON v.visittestid = t.testid
    ''')
    results = cursor.fetchall()
    conn.close()
    return results
