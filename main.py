"""
main.py
Entry point for the Medical Records System.
Initializes the SQLite database schema and launches the Tkinter GUI application.
"""
import tkinter as tk
from backend import initialize_database
from gui import MedicalRecordsApp

def main():
    """Initialize DB schema if needed and start the GUI mainloop."""
    # 1. Initialize DB and create tables if they do not exist
    initialize_database()

    # 2. Launch Tkinter GUI
    root = tk.Tk()
    app = MedicalRecordsApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()