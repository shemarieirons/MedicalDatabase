# 🏥 Medical Records Management System  

A modular, SQLite-backed medical records management system built in Python with a Tkinter GUI.  

This application demonstrates database design, relational modeling, backend architecture, and GUI integration in a healthcare-focused data environment.

---

## 📌 Project Summary  

This project implements a structured medical database capable of managing:

- Patient records  
- Diagnoses  
- Treatments  
- Medical tests  
- Patient visits  

The system uses a fully relational SQLite database and a modular Python backend to separate business logic from user interface components.

The GUI layer provides a clean interaction interface while preserving database integrity and backend structure.

---

## 🧠 Technical Highlights  

- Designed a normalized relational schema with multiple linked tables  
- Implemented one-to-many and many-to-one relationships  
- Built modular database access layers  
- Ensured automatic table creation and database initialization  
- Separated backend logic from GUI logic (clean architecture principle)  
- Implemented persistent local storage using SQLite  
- Structured the application for scalability and future analytics integration  

---

## 🛠 Tech Stack  

- **Language:** Python  
- **Database:** SQLite  
- **GUI Framework:** Tkinter  
- **Architecture:** Modular backend + UI separation  

No external database server required.

---

## 🗄 Database Design  

The system includes relational tables such as:

- `patient`  
- `diagnosis`  
- `treatment`  
- `tests`  
- `patientvisit`  

Key design features:

- A diagnosis can map to multiple treatments and tests  
- A patient can have multiple visits  
- Visits may include tests even without a diagnosis  
- Foreign key relationships enforce data consistency  

The database file (`medicalDatabase.db`) is automatically generated on first execution.

---

## 📁 Project Structure  
├── main.py              # Application entry point
├── gui.py               # Tkinter interface layer
├── backend.py           # Core database operations
├── patient.py           # Patient table module
├── treatment.py         # Treatment table module
├── visits.py            # Visit management module
├── tests.py             # Test management module
└── medicalDatabase.db   # SQLite database (auto-generated)

---

## ▶️ Running the Application  

```bash
python main.py
